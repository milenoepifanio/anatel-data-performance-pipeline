"""
Visualization of dbt marts data

Este notebook conecta ao arquivo DuckDB usado pelo perfil dbt e exibe os 
resultados dos modelos analíticos.
"""

# ============================================================================
# Cell 1: Connect to DuckDB and List Tables
# ============================================================================

import duckdb
import pandas as pd

con = duckdb.connect('../data/duckdb/anatel.duckdb')

tables = con.execute('SHOW TABLES').fetchdf()

print(tables)

# ============================================================================
# Cell 2: View mart_anatel_smp_summary Data
# ============================================================================

# Visualizar os primeiros registros de mart_anatel_smp_summary
query_summary = 'SELECT * FROM mart_anatel_smp_summary LIMIT 20'
summary_df = con.execute(query_summary).fetchdf()
print(summary_df)

# ============================================================================
# Cell 3: View mart_anatel_smp_kpis Data
# ============================================================================

# Visualizar os primeiros registros de mart_anatel_smp_kpis
query_kpis = 'SELECT * FROM mart_anatel_smp_kpis LIMIT 20'
kpis_df = con.execute(query_kpis).fetchdf()
print(kpis_df)

# ============================================================================
# Cell 4: Empty Cell
# ============================================================================
