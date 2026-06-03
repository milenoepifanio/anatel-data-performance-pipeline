import os
import re
from typing import Optional

import pandas as pd


def normalize_column_name(column_name: str) -> str:
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


def normalize_month_column(column_name: str) -> str:
    value = str(column_name)

    match = re.search(r"(20\d{2})[-/](\d{1,2})", value)

    if match:
        year = match.group(1)
        month = int(match.group(2))
        return f"mes_{year}_{month:02d}"

    return normalize_column_name(value)


def infer_model_from_filename(file_path: str) -> str:
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


def infer_year_from_filename(file_path: str) -> Optional[int]:
    match = re.search(r"(20\d{2})", os.path.basename(file_path))
    return int(match.group(1)) if match else None


def normalize_numeric_value(value):
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
