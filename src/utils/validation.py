import re

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, trim, sum as spark_sum, when


def _assert_required_columns(df: DataFrame, required_columns: list[str]) -> None:
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def _count_null_or_empty(df: DataFrame, columns: list[str]) -> dict[str, int]:
    null_counts = df.select([
        spark_sum(
            when(col(column).isNull() | (trim(col(column)) == ""), 1).otherwise(0)
        ).alias(column)
        for column in columns
    ]).collect()[0].asDict()

    return null_counts


def find_month_columns(df: DataFrame) -> list[str]:
    return [
        column for column in df.columns
        if re.match(r"^mes_\d{4}_\d{2}$", column)
    ]


def validate_wide_dataframe(df: DataFrame) -> dict:
    required_columns = ["grupo_economico", "variavel"]
    _assert_required_columns(df, required_columns)

    month_columns = find_month_columns(df)

    if not month_columns:
        raise ValueError(
            "DataFrame wide não contém colunas mensais no formato esperado."
        )

    null_counts = _count_null_or_empty(df, required_columns)

    if any(value > 0 for value in null_counts.values()):
        invalid_fields = [
            column for column, value in null_counts.items() if value > 0
        ]
        raise ValueError(
            f"Wide validation failed. Required key columns contain null or empty values: {invalid_fields}"
        )

    return {
        "row_count": df.count(),
        "month_columns_count": len(month_columns),
        "required_columns": required_columns,
    }


def validate_long_dataframe(df: DataFrame) -> dict:
    required_columns = [
        "grupo_economico",
        "variavel",
        "competencia",
        "valor",
        "arquivo_origem",
        "aba_origem",
        "modelo",
        "ano_arquivo",
    ]
    _assert_required_columns(df, required_columns)

    row_count = df.count()

    if row_count == 0:
        raise ValueError("Transformação wide-to-long resultou em zero registros.")

    required_non_null = ["grupo_economico", "variavel", "competencia", "valor"]
    null_counts = _count_null_or_empty(df, required_non_null)

    invalid_competencia_count = df.filter(
        ~col("competencia").rlike(r"^\d{4}-\d{2}$")
    ).count()

    duplicate_key_count = df.groupBy(
        "arquivo_origem",
        "aba_origem",
        "grupo_economico",
        "variavel",
        "competencia",
    ).count().filter(col("count") > 1).count()

    failures = []

    for column, count_value in null_counts.items():
        if count_value > 0:
            failures.append(
                f"{count_value} registros com {column} nulo/vazio"
            )

    if invalid_competencia_count > 0:
        failures.append(
            f"{invalid_competencia_count} registros com competencia fora do formato YYYY-MM"
        )

    if duplicate_key_count > 0:
        failures.append(
            f"{duplicate_key_count} registros duplicados na chave de negócio"
        )

    if failures:
        raise ValueError("Long validation failed: " + "; ".join(failures))

    return {
        "row_count": row_count,
        **null_counts,
        "invalid_competencia_count": invalid_competencia_count,
        "duplicate_key_count": duplicate_key_count,
    }
