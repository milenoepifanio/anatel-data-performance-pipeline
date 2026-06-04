"""
Test Long Silver

Test reading CSV and parquet files in long format.
"""

# ============================================================================
# Cell 1: Read CSV File
# ============================================================================

import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.read_csv(
    r"C:\Users\Mileno\Downloads\PDI\data\temp\ods_csv\SCM2016_Banda_Larga_Fixa.csv",
    encoding="utf-8-sig"
)

print(df.head())
print(df.iloc[0])

# ============================================================================
# Cell 2: Read Parquet File
# ============================================================================

df = pd.read_parquet(
    r"C:\Users\Mileno\Downloads\PDI\data\staging\long-files\SCM2016_Banda_Larga_Fixa_long.parquet",
    engine="fastparquet"
)

print(df.head())
print(df.iloc[0])
print(df.dtypes)

# ============================================================================
# Cell 3: Empty Cell
# ============================================================================
