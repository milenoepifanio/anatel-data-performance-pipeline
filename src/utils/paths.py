from pathlib import Path
import sys

# =========================================================
# PROJECT ROOT
# =========================================================

# Returns the project root directory:
# PDI/
PROJECT_ROOT = Path(__file__).resolve().parents[2]


# =========================================================
# MAIN PROJECT DIRECTORIES
# =========================================================

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"

TEMP_DIR = DATA_DIR / "temp"

STAGING_DIR = DATA_DIR / "staging"

MARTS_DIR = DATA_DIR / "marts"

DUCKDB_DIR = DATA_DIR / "duckdb"

DUCKDB_FILE = DUCKDB_DIR / "anatel.duckdb"

LOGS_DIR = PROJECT_ROOT / "logs"

DOCS_DIR = PROJECT_ROOT / "docs"

NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"


# =========================================================
# TEMP DIRECTORIES
# =========================================================

TEMP_ODS_CSV_DIR = TEMP_DIR / "ods_csv"

TEMP_ODS_CSV_LONG_DIR = TEMP_DIR / "ods_csv_long"


# =========================================================
# STAGING DIRECTORIES
# =========================================================

# staging/long-files
STAGING_LONG_FILES_DIR = (
    STAGING_DIR / "long-files"
)

# staging/wide
STAGING_WIDE_DIR = (
    STAGING_DIR / "wide"
)

# staging/wide/ida_anatel
STAGING_WIDE_IDA_ANATEL_DIR = (
    STAGING_WIDE_DIR / "ida_anatel"
)


# =========================================================
# SOURCE URLS
# =========================================================

SOURCE_URL_IDA_ANATEL = (
    "https://dados.gov.br/dados/conjuntos-dados/"
    "indice-desempenho-atendimento"
)


# =========================================================
# RAW INPUT FILES
# =========================================================

RAW_INPUT_FILES = [
    RAW_DIR / "SCM2016.ods",
    RAW_DIR / "SEAC2019.ods",
    RAW_DIR / "SMP2014.ods",
    RAW_DIR / "STFC2017.ods",
]


# =========================================================
# LOCAL ENVIRONMENT
# =========================================================

JAVA_HOME = Path(
    r"C:\Program Files\Java\jdk-17"
)

HADOOP_HOME = Path(
    r"C:\hadoop"
)

SPARK_HOME = (
    Path(sys.executable).resolve().parents[1]
    / "Lib"
    / "site-packages"
    / "pyspark"
)

# =========================================================
# DIRECTORY HELPERS
# =========================================================

ALL_DIRECTORIES = [
    DATA_DIR,
    RAW_DIR,
    TEMP_DIR,
    STAGING_DIR,
    MARTS_DIR,
    DUCKDB_DIR,
    LOGS_DIR,
    DOCS_DIR,
    NOTEBOOKS_DIR,
    TEMP_ODS_CSV_DIR,
    TEMP_ODS_CSV_LONG_DIR,
    STAGING_LONG_FILES_DIR,
    STAGING_WIDE_DIR,
    STAGING_WIDE_IDA_ANATEL_DIR,
]


def create_directories() -> None:
    """
    Automatically creates required project directories
    if they do not exist.
    """

    for directory in ALL_DIRECTORIES:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )
        
        

# =========================================================
# S3 / LOCALSTACK CREDENCIALS
# =========================================================  
        
LOCALSTACK_ENDPOINT_URL = "http://localhost:4566"
AWS_ACCESS_KEY_ID = "test"
AWS_SECRET_ACCESS_KEY = "test"
AWS_REGION = "us-east-1"

BUCKET_NAME = "anatel-lake"
S3_PREFIX = "silver/anatel_long"