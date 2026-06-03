import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.comparison import (
    compare_file_counts,
    compare_record_counts,
    map_data_files,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compara CSV wide de referência com parquet long gerado pelo PySpark."
    )

    parser.add_argument("--reference-dir", required=True)
    parser.add_argument("--target-dir", required=True)
    parser.add_argument("--sample-files", required=False, default="")
    parser.add_argument("--sample-size", required=False, type=int, default=20)

    return parser.parse_args()


def normalize_input_key(value: str) -> str:
    value = value.strip()

    if value.endswith("_long.parquet"):
        return value.replace("_long.parquet", "")

    if value.endswith(".parquet"):
        return value.replace(".parquet", "")

    if value.endswith(".csv"):
        return value.replace(".csv", "")

    return value


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(
        columns={
            "GRUPO ECONÔMICO": "grupo_economico",
            "VARIÁVEL": "variavel",
        }
    )


def read_reference_as_long(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    df = normalize_columns(df)

    id_columns = ["grupo_economico", "variavel"]

    month_columns = [
        column
        for column in df.columns
        if column not in id_columns
    ]

    df_long = df.melt(
        id_vars=id_columns,
        value_vars=month_columns,
        var_name="competencia",
        value_name="valor",
    )

    df_long["grupo_economico"] = df_long["grupo_economico"].astype(str).str.strip()
    df_long["variavel"] = df_long["variavel"].astype(str).str.strip()
    df_long["competencia"] = df_long["competencia"].astype(str).str.strip()
    df_long["valor"] = pd.to_numeric(df_long["valor"], errors="coerce")
    df_long = df_long.dropna(subset=["valor"])

    return df_long[["grupo_economico", "variavel", "competencia", "valor"]]


def read_target_long(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)

    df["grupo_economico"] = df["grupo_economico"].astype(str).str.strip()
    df["variavel"] = df["variavel"].astype(str).str.strip()
    df["competencia"] = df["competencia"].astype(str).str.slice(0, 7)
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

    return df[["grupo_economico", "variavel", "competencia", "valor"]]


def compare_long_content(reference_path: Path, target_path: Path) -> dict:
    reference_df = read_reference_as_long(reference_path)
    target_df = read_target_long(target_path)

    key_columns = ["grupo_economico", "variavel", "competencia"]

    merged = reference_df.merge(
        target_df,
        on=key_columns,
        how="outer",
        suffixes=("_reference", "_target"),
        indicator=True,
    )

    both = merged[merged["_merge"] == "both"].copy()

    both["valor_reference"] = both["valor_reference"].round(6)
    both["valor_target"] = both["valor_target"].round(6)

    value_diff = both[
        both["valor_reference"] != both["valor_target"]
    ]

    only_reference = merged[merged["_merge"] == "left_only"]
    only_target = merged[merged["_merge"] == "right_only"]

    return {
        "reference_rows_long": len(reference_df),
        "target_rows": len(target_df),
        "matched_keys": len(both),
        "only_in_reference": len(only_reference),
        "only_in_target": len(only_target),
        "value_differences": len(value_diff),
        "only_reference_sample": only_reference.head(10),
        "only_target_sample": only_target.head(10),
        "value_diff_sample": value_diff.head(10),
    }


def main():
    args = parse_args()

    reference_dir = args.reference_dir
    target_dir = args.target_dir

    sample_files = [
        normalize_input_key(file)
        for file in args.sample_files.split(",")
        if file.strip()
    ]

    print("COMPARAÇÃO DE ARQUIVOS")
    print("=====================")

    file_counts = compare_file_counts(reference_dir, target_dir)

    print(f"Arquivos referência: {file_counts['reference_count']}")
    print(f"Arquivos PySpark: {file_counts['target_count']}")
    print(f"Arquivos apenas na referência: {file_counts['only_in_reference']}")
    print(f"Arquivos apenas no PySpark: {file_counts['only_in_target']}")
    print(f"Arquivos em comum: {file_counts['common_files']}")

    print()
    print("COMPARAÇÃO DE REGISTROS BRUTOS")
    print("==============================")

    record_counts = compare_record_counts(reference_dir, target_dir)

    print(f"Total referência wide: {record_counts['reference_total']}")
    print(f"Total PySpark long: {record_counts['target_total']}")
    print(f"Delta bruto: {record_counts['total_delta']}")
    print("Observação: esse delta é esperado quando a referência está wide e o target está long.")

    if not sample_files:
        print()
        print("Nenhum arquivo informado em --sample-files.")
        print("Comparação concluída.")
        return

    reference_files_map = map_data_files(reference_dir)
    target_files_map = map_data_files(target_dir)

    common_keys = set(reference_files_map.keys()) & set(target_files_map.keys())

    print()
    print("COMPARAÇÃO WIDE → LONG")
    print("======================")

    for sample_file in sample_files:
        if sample_file not in common_keys:
            print(f"Arquivo solicitado não encontrado: {sample_file}")
            continue

        reference_path = reference_files_map[sample_file]
        target_path = target_files_map[sample_file]

        result = compare_long_content(reference_path, target_path)

        print()
        print(f"Arquivo: {sample_file}")
        print(f"Referência CSV wide: {reference_path}")
        print(f"PySpark parquet long: {target_path}")

        print(f"Linhas referência após melt: {result['reference_rows_long']}")
        print(f"Linhas PySpark: {result['target_rows']}")
        print(f"Chaves encontradas nos dois lados: {result['matched_keys']}")
        print(f"Somente na referência: {result['only_in_reference']}")
        print(f"Somente no PySpark: {result['only_in_target']}")
        print(f"Diferenças de valor: {result['value_differences']}")

        if result["only_in_reference"] > 0:
            print()
            print("Amostra somente na referência:")
            print(result["only_reference_sample"])

        if result["only_in_target"] > 0:
            print()
            print("Amostra somente no PySpark:")
            print(result["only_target_sample"])

        if result["value_differences"] > 0:
            print()
            print("Amostra de diferenças de valor:")
            print(result["value_diff_sample"])

    print()
    print("Comparação concluída.")


if __name__ == "__main__":
    main()