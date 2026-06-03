import os
from typing import Optional

import pandas as pd
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import lit
from pyspark.sql.types import DoubleType, StringType, StructField, StructType

from src.utils.normalization import (
    infer_model_from_filename,
    infer_year_from_filename,
    normalize_column_name,
    normalize_month_column,
    normalize_numeric_value,
)


def find_header_row(raw_pdf: pd.DataFrame) -> Optional[int]:
    for idx, row in raw_pdf.iterrows():
        first_value = str(row.iloc[0]).strip().upper()
        second_value = str(row.iloc[1]).strip().upper()

        if first_value == "GRUPO ECONÔMICO" and second_value == "VARIÁVEL":
            return idx

    return None


def ods_sheet_to_spark_dataframe(
    spark: SparkSession,
    ods_path: str,
    sheet_name: str,
) -> Optional[DataFrame]:
    raw_pdf = pd.read_excel(
        ods_path,
        engine="odf",
        sheet_name=sheet_name,
        header=None,
    )

    header_row = find_header_row(raw_pdf)

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
                normalize_numeric_value
            )

    renamed_columns = []

    for column in data_pdf.columns:
        if column in ["GRUPO ECONÔMICO", "VARIÁVEL"]:
            renamed_columns.append(normalize_column_name(column))
        else:
            renamed_columns.append(normalize_month_column(column))

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

    df = spark.createDataFrame(records, schema=schema)

    return df \
        .withColumn("arquivo_origem", lit(os.path.basename(ods_path))) \
        .withColumn("aba_origem", lit(sheet_name)) \
        .withColumn("modelo", lit(infer_model_from_filename(ods_path))) \
        .withColumn("ano_arquivo", lit(infer_year_from_filename(ods_path)))
