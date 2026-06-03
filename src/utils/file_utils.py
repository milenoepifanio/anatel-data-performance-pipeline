import os
from typing import List


def get_ods_files_from_raw(raw_path: str) -> List[str]:
    input_files = []

    for file_name in os.listdir(raw_path):
        if file_name.lower().endswith(".ods"):
            input_files.append(os.path.join(raw_path, file_name))

    if not input_files:
        raise ValueError(f"Nenhum arquivo .ods encontrado em: {raw_path}")

    return input_files
