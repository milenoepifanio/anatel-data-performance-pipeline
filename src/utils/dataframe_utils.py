from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    concat_ws,
    current_date,
    current_timestamp,
    date_format,
    lit,
    md5,
    trim,
)


def trim_string_columns(df: DataFrame) -> DataFrame:
    string_columns = [
        field.name
        for field in df.schema.fields
        if field.dataType.simpleString() == "string"
    ]

    for column in string_columns:
        df = df.withColumn(column, trim(col(column)))

    return df


def add_metadata_columns(df: DataFrame) -> DataFrame:
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
