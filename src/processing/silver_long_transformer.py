import os
import re
import pandas as pd
from pathlib import Path
from typing import Optional
from datetime import datetime

from src.utils.paths import (
    RAW_DIR,
    STAGING_LONG_FILES_DIR,
    create_directories,
)
from src.utils.spark_environment import configure_environment
from src.utils.dataframe_utils import add_metadata_columns, trim_string_columns
from src.utils.file_utils import get_ods_files_from_raw
from src.utils.ods_utils import ods_sheet_to_spark_dataframe
from src.utils.validation import validate_long_dataframe, validate_wide_dataframe


configure_environment()

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, expr


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

    def _write_parquet(self, df: DataFrame, output_file: str) -> int:
        final_pdf = df.toPandas()

        final_pdf.to_parquet(
            output_file,
            engine="pyarrow",
            compression="snappy",
            index=False,
        )

        return len(final_pdf)

    def transform_raw_to_long_parquet(
        self,
        raw_path: str,
        output_path: str,
    ):
        os.makedirs(output_path, exist_ok=True)

        input_files = get_ods_files_from_raw(raw_path)

        saved_files = []
        skipped_files = []
        total_records = 0

        for ods_path in input_files:
            xls = pd.ExcelFile(ods_path, engine="odf")

            for sheet_name in xls.sheet_names:
                try:
                    df = ods_sheet_to_spark_dataframe(
                        self.spark,
                        ods_path=ods_path,
                        sheet_name=sheet_name,
                    )

                    if df is None:
                        skipped_files.append(
                            f"{ods_path} | {sheet_name} | header_not_found"
                        )
                        continue

                    df = trim_string_columns(df)
                    validate_wide_dataframe(df)
                    df = self.wide_to_long(df)
                    validate_long_dataframe(df)
                    df = add_metadata_columns(df)

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

                    records = self._write_parquet(df, output_file)
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