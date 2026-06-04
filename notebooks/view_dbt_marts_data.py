"""
Visualization of dbt marts data

Conecta ao DuckDB usado pelo perfil dbt e exibe contagens e amostras
dos modelos staging e marts. Execute na raiz do projeto:

    python notebooks/view_dbt_marts_data.py
"""

import sys
from pathlib import Path

import duckdb
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.paths import DUCKDB_FILE

TABLES = [
    "main.stg_anatel_ida_smp",
    "main.mart_anatel_smp_summary",
    "main.mart_anatel_smp_kpis",
]

if not DUCKDB_FILE.exists():
    raise FileNotFoundError(
        f"Banco DuckDB não encontrado: {DUCKDB_FILE}\n"
        "Execute antes: dbt run --select staging.anatel+"
    )

con = duckdb.connect(str(DUCKDB_FILE))

print(f"DuckDB: {DUCKDB_FILE}\n")

print("=== Tabelas no schema main ===")
print(con.execute("SHOW TABLES").fetchdf())
print()

for table in TABLES:
    try:
        count = con.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()[0]
        print(f"{table}: {count:,} registros")
    except duckdb.HTTPException as exc:
        print(
            f"{table}: indisponível (view lê S3; suba LocalStack ou use só os marts)\n"
            f"  Detalhe: {exc}"
        )

print("\n=== Amostra mart_anatel_smp_summary (20 linhas) ===")
print(con.execute("SELECT * FROM main.mart_anatel_smp_summary LIMIT 20").fetchdf())

print("\n=== Amostra mart_anatel_smp_kpis (20 linhas) ===")
print(con.execute("SELECT * FROM main.mart_anatel_smp_kpis LIMIT 20").fetchdf())

con.close()
