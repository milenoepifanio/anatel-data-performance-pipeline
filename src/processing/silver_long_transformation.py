import os
import sys
import re
import pandas as pd
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from src.utils.paths import (
    RAW_DIR,
    STAGING_LONG_FILES_DIR,
    JAVA_HOME,
    SPARK_HOME,
    create_directories,
)


def configure_environment() -> None:
    hadoop_home = HADOOP_HOME

    os.environ["JAVA_HOME"] = str(JAVA_HOME)
    os.environ["SPARK_HOME"] = str(SPARK_HOME)
    os.environ["HADOOP_HOME"] = str(hadoop_home)
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    os.environ["PATH"] = (
        str(hadoop_home / "bin")
        + os.pathsep
        + str(JAVA_HOME / "bin")
        + os.pathsep
        + str(SPARK_HOME / "bin")
        + os.pathsep
        + os.environ.get("PATH", "")
    )


configure_environment()

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
)
from pyspark.sql.functions import (
    col,
    lit,
    trim,
    current_timestamp,
    current_date,
    date_format,
    md5,
    concat_ws,
    expr,
)


class AnatelLongPySparkTransformer:

    def __init__(self, spark: Optional[SparkSession] = None):
        self.spark = spark or SparkSession.builder \
            .appName("AnatelLongPySparkTransformer") \
            .master("local[1]") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.python.worker.faulthandler.enabled", "true") \
            .config("spark.sql.execution.pyspark.udf.faulthandler.enabled", "true") \
            .config("spark.python.worker.reuse", "false") \
            .getOrCreate()

    def normalize_column_name(self, column_name: str) -> str:
        value = str(column_name).strip().lower()

        replacements = {
            "á": "a", "à": "a", "ã": "a", "â": "a",
            "é": "e", "ê": "e",
            "í": "i",
            "ó": "o", "ô": "o", "õ": "o",
            "ú": "u",
            "ç": "c",
        }

        for old, new in replacements.items():
            value = value.replace(old, new)

        value = value.replace(" ", "_")
        value = value.replace("-", "_")
        value = value.replace("/", "_")
        value = re.sub(r"[^a-z0-9_]", "", value)
        value = re.sub(r"_+", "_", value)

        return value.strip("_")

    def normalize_month_column(self, column_name: str) -> str:
        value = str(column_name)

        match = re.search(r"(20\d{2})[-/](\d{1,2})", value)

        if match:
            year = match.group(1)
            month = int(match.group(2))
            return f"mes_{year}_{month:02d}"

        return self.normalize_column_name(value)

    def infer_model_from_filename(self, file_path: str) -> str:
        file_name = os.path.basename(file_path).upper()

        if "SCM" in file_name:
            return "SCM"
        if "SEAC" in file_name:
            return "SEAC"
        if "STFC" in file_name:
            return "STFC"
        if "SMP" in file_name:
            return "SMP"

        return "UNKNOWN"

    def infer_year_from_filename(self, file_path: str) -> Optional[int]:
        match = re.search(r"(20\d{2})", os.path.basename(file_path))
        return int(match.group(1)) if match else None

    def normalize_numeric_value(self, value):
        if pd.isna(value):
            return None

        if isinstance(value, (int, float)):
            return value

        value = str(value).strip()

        if value == "":
            return None

        if "," in value:
            value = value.replace(".", "").replace(",", ".")

        return pd.to_numeric(value, errors="coerce")

    def find_header_row(self, raw_pdf: pd.DataFrame) -> Optional[int]:
        for idx, row in raw_pdf.iterrows():
            first_value = str(row.iloc[0]).strip().upper()
            second_value = str(row.iloc[1]).strip().upper()

            if first_value == "GRUPO ECONÔMICO" and second_value == "VARIÁVEL":
                return idx

        return None

    def ods_sheet_to_spark_dataframe(
        self,
        ods_path: str,
        sheet_name: str,
    ) -> Optional[DataFrame]:

        raw_pdf = pd.read_excel(
            ods_path,
            engine="odf",
            sheet_name=sheet_name,
            header=None,
        )

        header_row = self.find_header_row(raw_pdf)

        if header_row is None:
            return None

        header = raw_pdf.iloc[header_row].tolist()
        data_pdf = raw_pdf.iloc[header_row + 1:].copy()
        data_pdf.columns = header

        data_pdf = data_pdf.dropna(how="all")

        data_pdf = data_pdf[
            data_pdf["GRUPO ECONÔMICO"].notna()
            & data_pdf["VARIÁVEL"].notna()
        ].copy()

        for column in data_pdf.columns:
            if column not in ["GRUPO ECONÔMICO", "VARIÁVEL"]:
                data_pdf[column] = data_pdf[column].apply(
                    self.normalize_numeric_value
                )

        renamed_columns = []

        for column in data_pdf.columns:
            if column in ["GRUPO ECONÔMICO", "VARIÁVEL"]:
                renamed_columns.append(
                    self.normalize_column_name(column)
                )
            else:
                renamed_columns.append(
                    self.normalize_month_column(column)
                )

        data_pdf.columns = renamed_columns

        string_columns = ["grupo_economico", "variavel"]

        schema = StructType([
            StructField(
                column,
                StringType() if column in string_columns else DoubleType(),
                True,
            )
            for column in data_pdf.columns
        ])

        records = []

        for _, row in data_pdf.iterrows():
            record = {}

            for column in data_pdf.columns:
                value = row[column]

                if pd.isna(value):
                    record[column] = None
                elif column in string_columns:
                    record[column] = str(value)
                else:
                    record[column] = float(value)

            records.append(record)

        df = self.spark.createDataFrame(
            records,
            schema=schema,
        )

        df = df \
            .withColumn("arquivo_origem", lit(os.path.basename(ods_path))) \
            .withColumn("aba_origem", lit(sheet_name)) \
            .withColumn("modelo", lit(self.infer_model_from_filename(ods_path))) \
            .withColumn("ano_arquivo", lit(self.infer_year_from_filename(ods_path)))

        return df

    def trim_string_columns(self, df: DataFrame) -> DataFrame:
        string_columns = [
            field.name
            for field in df.schema.fields
            if isinstance(field.dataType, StringType)
        ]

        for column in string_columns:
            df = df.withColumn(column, trim(col(column)))

        return df

    def wide_to_long(self, df: DataFrame) -> DataFrame:
        id_columns = [
            "grupo_economico",
            "variavel",
            "arquivo_origem",
            "aba_origem",
            "modelo",
            "ano_arquivo",
        ]

        month_columns = [
            column for column in df.columns
            if re.match(r"^mes_\d{4}_\d{2}$", column)
        ]

        if not month_columns:
            raise ValueError("Nenhuma coluna mensal encontrada para transformação long.")

        for column in month_columns:
            df = df.withColumn(column, col(column).cast("double"))

        stack_expression = "stack({}, {}) as (competencia, valor)".format(
            len(month_columns),
            ", ".join([f"'{column}', `{column}`" for column in month_columns]),
        )

        long_df = df.select(
            *[col(column) for column in id_columns],
            expr(stack_expression),
        )

        long_df = long_df \
            .withColumn(
                "competencia",
                expr("replace(replace(competencia, 'mes_', ''), '_', '-')"),
            ) \
            .filter(col("valor").isNotNull())

        return long_df

    def add_metadata_columns(self, df: DataFrame) -> DataFrame:
        business_columns = df.columns

        return df \
            .withColumn("_ingestion_timestamp", current_timestamp()) \
            .withColumn(
                "_processing_date",
                date_format(current_date(), "yyyy-MM-dd"),
            ) \
            .withColumn(
                "_record_hash",
                md5(
                    concat_ws(
                        "|",
                        *[col(column).cast("string") for column in business_columns],
                    )
                ),
            )

    def get_ods_files_from_raw(self, raw_path: str) -> List[str]:
        input_files = []

        for file_name in os.listdir(raw_path):
            if file_name.lower().endswith(".ods"):
                input_files.append(os.path.join(raw_path, file_name))

        if not input_files:
            raise ValueError(f"Nenhum arquivo .ods encontrado em: {raw_path}")

        return input_files

    def transform_raw_to_long_parquet(
        self,
        raw_path: str,
        output_path: str,
    ):
        os.makedirs(output_path, exist_ok=True)

        input_files = self.get_ods_files_from_raw(raw_path)

        saved_files = []
        skipped_files = []
        total_records = 0

        for ods_path in input_files:
            xls = pd.ExcelFile(ods_path, engine="odf")

            for sheet_name in xls.sheet_names:
                try:
                    df = self.ods_sheet_to_spark_dataframe(
                        ods_path=ods_path,
                        sheet_name=sheet_name,
                    )

                    if df is None:
                        skipped_files.append(
                            f"{ods_path} | {sheet_name} | header_not_found"
                        )
                        continue

                    df = self.trim_string_columns(df)
                    df = self.wide_to_long(df)
                    df = self.add_metadata_columns(df)

                    file_name = os.path.basename(ods_path).replace(".ods", "")
                    safe_sheet = re.sub(r"[^a-zA-Z0-9_]", "_", sheet_name)

                    output_file = os.path.join(
                        output_path,
                        f"{file_name}_{safe_sheet}_long.parquet",
                    )

                    if os.path.exists(output_file):
                        print(f"Arquivo já existe. Ignorando: {output_file}")
                        skipped_files.append(output_file)
                        continue

                    final_pdf = df.toPandas()

                    final_pdf.to_parquet(
                        output_file,
                        engine="pyarrow",
                        compression="snappy",
                        index=False,
                    )

                    records = len(final_pdf)
                    total_records += records
                    saved_files.append(output_file)

                    print(
                        f"Long parquet salvo em: {output_file} | Registros: {records}"
                    )

                except Exception as e:
                    error_message = f"{ods_path} | {sheet_name} | {str(e)}"

                    print(f"Erro ao processar arquivo/aba: {ods_path} | {sheet_name}")
                    print(f"Erro: {e}")

                    skipped_files.append(error_message)
                    continue

        return {
            "status": "success",
            "files_saved": len(saved_files),
            "files_skipped": len(skipped_files),
            "total_records": total_records,
            "output_path": output_path,
            "saved_files": saved_files,
            "skipped_files": skipped_files,
            "timestamp": datetime.now().isoformat(),
        }


if __name__ == "__main__":
    create_directories()

    transformer = AnatelLongPySparkTransformer()

    result = transformer.transform_raw_to_long_parquet(
        raw_path=str(RAW_DIR),
        output_path=str(STAGING_LONG_FILES_DIR),
    )

    print(result)