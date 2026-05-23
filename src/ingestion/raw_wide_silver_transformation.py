import os
import sys
import re
import pandas as pd
from typing import List, Optional
from datetime import datetime


def configure_environment():
    java_home = r"C:\Program Files\Java\jdk-17"
    spark_home = r"C:\Users\Mileno\Downloads\PDI\env\Lib\site-packages\pyspark"

    os.environ["JAVA_HOME"] = java_home
    os.environ["SPARK_HOME"] = spark_home
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    os.environ["PATH"] = (
        os.path.join(java_home, "bin")
        + os.pathsep
        + os.path.join(spark_home, "bin")
        + os.pathsep
        + os.environ.get("PATH", "")
    )


configure_environment()

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StringType

from pyspark.sql.functions import (
    col,
    lit,
    trim,
    current_timestamp,
    current_date,
    date_format,
    md5,
    concat_ws
)

class AnatelWidePySparkTransformer:

    def __init__(self, spark: Optional[SparkSession] = None):
        self.spark = spark or SparkSession.builder \
            .appName("AnatelWidePySparkTransformer") \
            .master("local[1]") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
            .config("spark.sql.parquet.compression.codec", "snappy") \
            .getOrCreate()

    def ods_to_csv(self, ods_path: str, temp_dir: str) -> List[str]:
        """
        Converte cada aba do ODS para CSV temporário.
        Necessário porque Spark não lê ODS nativamente.
        """
        os.makedirs(temp_dir, exist_ok=True)

        csv_paths = []
        xls = pd.ExcelFile(ods_path, engine="odf")

        for sheet_name in xls.sheet_names:
            raw_pdf = pd.read_excel(
                ods_path,
                engine="odf",
                sheet_name=sheet_name,
                header=None
            )

            header_row = None

            for idx, row in raw_pdf.iterrows():
                first_value = str(row.iloc[0]).strip().upper()
                second_value = str(row.iloc[1]).strip().upper()

                if first_value == "GRUPO ECONÔMICO" and second_value == "VARIÁVEL":
                    header_row = idx
                    break

            if header_row is None:
                continue

            header = raw_pdf.iloc[header_row].tolist()
            data_pdf = raw_pdf.iloc[header_row + 1:].copy()
            data_pdf.columns = header

            data_pdf = data_pdf.dropna(how="all")

            data_pdf = data_pdf[
                data_pdf["GRUPO ECONÔMICO"].notna()
                & data_pdf["VARIÁVEL"].notna()
            ].copy()

            file_name = os.path.basename(ods_path).replace(".ods", "")
            safe_sheet = re.sub(r"[^a-zA-Z0-9_]", "_", sheet_name)

            csv_path = os.path.join(temp_dir, f"{file_name}_{safe_sheet}.csv")
            
            def normalize_numeric_value(value):
                if pd.isna(value):
                    return None

                # Se já veio como número, mantém como está
                if isinstance(value, (int, float)):
                    return value

                value = str(value).strip()
                
                if value == "":
                    return None

                # Caso brasileiro: 1.234,56
                if "," in value:
                    value = value.replace(".", "").replace(",", ".")

                return pd.to_numeric(value, errors="coerce")

            for column in data_pdf.columns:
                if column not in ["GRUPO ECONÔMICO", "VARIÁVEL"]:
                    data_pdf[column] = data_pdf[column].apply(normalize_numeric_value)
                    
            data_pdf.to_csv(csv_path, index=False, encoding="utf-8-sig")

            csv_paths.append(csv_path)

        return csv_paths

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

    def read_csv_with_pyspark(self, csv_path: str, ods_origin_path: str) -> DataFrame:
        df = self.spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .option("encoding", "UTF-8") \
            .option("multiLine", "true") \
            .option("escape", '"') \
            .csv(csv_path)

        renamed_columns = []

        for c in df.columns:
            if c in ["GRUPO ECONÔMICO", "VARIÁVEL"]:
                renamed_columns.append(self.normalize_column_name(c))
            else:
                renamed_columns.append(self.normalize_month_column(c))

        for old_name, new_name in zip(df.columns, renamed_columns):
            df = df.withColumnRenamed(old_name, new_name)

        df = df \
            .withColumn("arquivo_origem", lit(os.path.basename(ods_origin_path))) \
            .withColumn("modelo", lit(self.infer_model_from_filename(ods_origin_path))) \
            .withColumn("ano_arquivo", lit(self.infer_year_from_filename(ods_origin_path)))

        return df

    def trim_string_columns(self, df: DataFrame) -> DataFrame:
        string_columns = [
            field.name
            for field in df.schema.fields
            if isinstance(field.dataType, StringType)
        ]

        for c in string_columns:
            df = df.withColumn(c, trim(col(c)))

        return df

    def add_metadata_columns(self, df: DataFrame) -> DataFrame:
        business_columns = df.columns

        return df \
            .withColumn(
                "_ingestion_timestamp",
                current_timestamp()) \
            .withColumn(
                "_processing_date",
                date_format(current_date(), 'yyyy-MM-dd')) \
            .withColumn(
                "_record_hash",
                md5(concat_ws("|",*[col(c).cast("string") for c in business_columns]))
            )

    def transform_files_to_wide_parquet(
        self,
        input_files: List[str],
        temp_csv_dir: str,
        output_path: str
    ):
        os.makedirs(output_path, exist_ok=True)

        saved_files = []
        total_records = 0

        for ods_path in input_files:
            csv_paths = self.ods_to_csv(ods_path, temp_csv_dir)

            for csv_path in csv_paths:
                df = self.read_csv_with_pyspark(csv_path, ods_path)

                df = self.trim_string_columns(df)
                df = self.add_metadata_columns(df)

                output_file_name = (
                    os.path.basename(csv_path)
                    .replace(".csv", ".parquet")
                )

                output_file = os.path.join(output_path, output_file_name)

                final_pdf = df.toPandas()

                final_pdf.to_parquet(
                    output_file,
                    engine="pyarrow",
                    compression="snappy",
                    index=False
                )

                records = len(final_pdf)
                total_records += records
                saved_files.append(output_file)

                print(f"Parquet salvo em: {output_file} | Registros: {records}")

        if not saved_files:
            raise ValueError("Nenhum arquivo válido foi processado.")

        return {
            "status": "success",
            "files_saved": len(saved_files),
            "total_records": total_records,
            "output_path": output_path,
            "saved_files": saved_files,
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":

    transformer = AnatelWidePySparkTransformer()

    input_files = [
        r"C:\Users\Mileno\Downloads\PDI\data\raw\SCM2016.ods",
        r"C:\Users\Mileno\Downloads\PDI\data\raw\SEAC2019.ods",
        r"C:\Users\Mileno\Downloads\PDI\data\raw\SMP2014.ods",
        r"C:\Users\Mileno\Downloads\PDI\data\raw\STFC2017.ods",
    ]

    result = transformer.transform_files_to_wide_parquet(
        input_files=input_files,
        temp_csv_dir=r"C:\Users\Mileno\Downloads\PDI\data\temp\ods_csv",
        output_path=r"C:\Users\Mileno\Downloads\PDI\data\staging\wide\ida_anatel"
    )

    print(result)
