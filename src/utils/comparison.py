from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd

SUPPORTED_EXTENSIONS = [".parquet", ".csv"]


def _is_supported_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS


def normalize_file_key(path: Path) -> str:
    """
    Normaliza nomes para permitir comparação lógica entre:
    - SCM2015_SeAC.csv
    - SCM2015_SeAC_long.parquet
    """
    name = path.name

    if name.endswith("_long.parquet"):
        return name.replace("_long.parquet", "")

    if name.endswith(".parquet"):
        return name.replace(".parquet", "")

    if name.endswith(".csv"):
        return name.replace(".csv", "")

    return path.stem


def list_data_files(directory: str) -> List[Path]:
    directory_path = Path(directory)

    if not directory_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    return sorted([
        path for path in directory_path.iterdir()
        if _is_supported_file(path)
    ])


def map_data_files(directory: str) -> Dict[str, Path]:
    return {
        normalize_file_key(path): path
        for path in list_data_files(directory)
    }


def _read_data_file(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)

    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, encoding="utf-8-sig")

    raise ValueError(f"Unsupported file extension: {path.suffix}")


def get_file_record_counts(directory: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}

    for key, path in map_data_files(directory).items():
        counts[key] = len(_read_data_file(path))

    return counts


def get_schema(path: Path) -> List[Tuple[str, str]]:
    df = _read_data_file(path)
    return [(column, str(dtype)) for column, dtype in zip(df.columns, df.dtypes)]


def compare_file_counts(reference_dir: str, target_dir: str) -> Dict[str, object]:
    reference_files = map_data_files(reference_dir)
    target_files = map_data_files(target_dir)

    reference_keys = set(reference_files.keys())
    target_keys = set(target_files.keys())

    common_keys = sorted(reference_keys & target_keys)

    return {
        "reference_count": len(reference_files),
        "target_count": len(target_files),
        "only_in_reference": sorted(list(reference_keys - target_keys)),
        "only_in_target": sorted(list(target_keys - reference_keys)),
        "common_files": common_keys,
        "matched_files": {
            key: {
                "reference_file": str(reference_files[key]),
                "target_file": str(target_files[key]),
            }
            for key in common_keys
        },
    }


def compare_record_counts(reference_dir: str, target_dir: str) -> Dict[str, object]:
    reference_counts = get_file_record_counts(reference_dir)
    target_counts = get_file_record_counts(target_dir)

    common_keys = sorted(set(reference_counts.keys()) & set(target_counts.keys()))

    per_file_comparison = {
        key: {
            "reference_rows": reference_counts[key],
            "target_rows": target_counts[key],
            "delta_rows": target_counts[key] - reference_counts[key],
        }
        for key in common_keys
    }

    return {
        "reference_total": sum(reference_counts.values()),
        "target_total": sum(target_counts.values()),
        "total_delta": sum(target_counts.values()) - sum(reference_counts.values()),
        "reference_counts": reference_counts,
        "target_counts": target_counts,
        "per_file_comparison": per_file_comparison,
    }


def compare_schema(reference_path: Path, target_path: Path) -> Dict[str, object]:
    reference_schema = get_schema(reference_path)
    target_schema = get_schema(target_path)

    return {
        "reference_file": str(reference_path),
        "target_file": str(target_path),
        "same_schema": reference_schema == target_schema,
        "reference_schema": reference_schema,
        "target_schema": target_schema,
    }


def get_sample_rows(
    path: Path,
    order_by: Optional[List[str]] = None,
    n: int = 20,
) -> pd.DataFrame:
    df = _read_data_file(path)

    if order_by:
        valid_columns = [column for column in order_by if column in df.columns]

        if valid_columns:
            df = df.sort_values(valid_columns)

    return df.head(n)


def compare_sample_rows(
    reference_path: Path,
    target_path: Path,
    order_by: Optional[List[str]] = None,
    n: int = 20,
) -> Dict[str, pd.DataFrame]:
    return {
        "reference_sample": get_sample_rows(reference_path, order_by=order_by, n=n),
        "target_sample": get_sample_rows(target_path, order_by=order_by, n=n),
    }