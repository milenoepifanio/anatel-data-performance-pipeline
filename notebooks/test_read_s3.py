"""
Test Read S3

Tests reading parquet files from S3 using DuckDB.
"""

# ============================================================================
# Cell 1: Import Required Libraries
# ============================================================================

import duckdb
import sys
from pathlib import Path

PROJECT_ROOT = Path.cwd().parents[0]

sys.path.append(str(PROJECT_ROOT))

from src.utils.paths import (
    LOCALSTACK_ENDPOINT_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    BUCKET_NAME,
    S3_PREFIX,
)

# ============================================================================
# Cell 2: Query S3 Data
# ============================================================================

con = duckdb.connect()

con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

con.execute(f"SET s3_region='{AWS_REGION}';")

con.execute(
    f"SET s3_endpoint='{LOCALSTACK_ENDPOINT_URL.replace('http://', '')}';""
)

con.execute(
    f"SET s3_access_key_id='{AWS_ACCESS_KEY_ID}';"
)

con.execute(
    f"SET s3_secret_access_key='{AWS_SECRET_ACCESS_KEY}';"
)

con.execute("SET s3_use_ssl=false;")

con.execute("SET s3_url_style='path';")

query = f"""
    SELECT *
    FROM read_parquet(
        's3://{BUCKET_NAME}/{S3_PREFIX}/*.parquet'
    )
    LIMIT 10
"""

df = con.execute(query).fetchdf()

print(df)
