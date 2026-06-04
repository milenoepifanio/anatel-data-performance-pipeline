# Project Rules & Engineering Standards

## Purpose

This document defines the engineering conventions, architectural decisions, organizational standards, 
and best practices adopted for this repository.

The goal is to maintain consistency, reproducibility, readability, and scalability throughout the 
project lifecycle.

---

# 1. Python Environment & Dependencies

## Required Python Version

```text
Python 3.11
```

All development and execution must use Python 3.11.

## Virtual Environment Setup

### Create Virtual Environment

```bash
py -3.11 -m venv env311
```

### Activate Environment (PowerShell)

```bash
.\env311\Scripts\Activate.ps1
```

### Activate Environment (Bash/Git Bash)

```bash
source env311/Scripts/activate
```

## Dependency Management

### Central Repository

All dependencies must be declared in:

```text
requirements.txt
```

**Rule**: Do not split dependencies across multiple requirement files unless explicitly justified.

### Installation

```bash
pip install -r requirements.txt
```

### Adding Dependencies

1. Add package to `requirements.txt` with pinned version or constraint
2. Update project documentation if introducing new major dependencies
3. Test with fresh environment install

---

# 2. Repository Structure

## Complete Project Organization

```text
PDI/
│
├── data/
│   ├── raw/                    # Original ODS files from Anatel
│   ├── staging/
│   │   ├── wide/               # Standardized wide-format parquet
│   │   └── long-files/         # Long-format (melted) parquet
│   ├── marts/                  # Final analytical tables (dbt output)
│   ├── temp/
│   │   ├── ods_csv/            # Temporary CSV from ODS conversion
│   │   └── ods_csv_long/       # Temporary long-format CSV
│   └── duckdb/
│       └── anatel.duckdb       # Analytical database
│
├── dbt/                        # Analytics Engineering
│   ├── models/
│   │   ├── staging/            # Staging layer models
│   │   └── marts/              # Analytical layer models
│   ├── seeds/                  # Static reference data
│   ├── snapshots/              # Slowly changing dimensions
│   ├── tests/                  # Data quality tests
│   ├── macros/                 # Reusable dbt logic
│   └── dbt_project.yml         # dbt configuration
│
├── docs/
│   ├── architecture/           # System design documentation
│   ├── learnings/              # Knowledge base
│   └── pipeline/               # Pipeline documentation
│
├── logs/                       # Execution logs
│
├── notebooks/                  # Analytical Python scripts
│   ├── test_spark.py           # Spark testing
│   ├── test_read_s3.py         # S3/DuckDB integration
│   ├── test_long_silver.py     # Long format validation
│   ├── view_dbt_marts_data.py  # dbt model inspection
│   └── compare_silver_outputs.py
│
├── sandbox/                    # Experimental code & prototypes
│   ├── initial_scraping.py
│   ├── refactor_scraping.py
│   └── raw_wide_silver_transformation.py
│
├── src/
│   ├── ingestion/              # Data ingestion modules
│   │   └── refactor_scraping_class.py  # Anatel web scraper
│   ├── processing/             # Data transformation modules
│   │   ├── silver_long_transformer.py  # PySpark wide→long
│   │   └── upload_parquet_to_s3.py     # S3 utilities
│   ├── utils/                  # Reusable utilities
│   │   ├── paths.py            # Centralized path management
│   │   ├── ods_utils.py        # ODS file utilities
│   │   ├── normalization.py    # Data standardization
│   │   ├── spark_environment.py # Spark configuration
│   │   ├── dataframe_utils.py  # DataFrame helpers
│   │   ├── file_utils.py       # File system utilities
│   │   ├── comparison.py       # Data comparison
│   │   └── validation.py       # Data validation
│   └── trash/                  # Deprecated code (keep for reference)
│
├── env/                        # Virtual environment (ignored in git)
├── env311/                     # Virtual environment (ignored in git)
│
├── .vscode/
│   ├── .rules.md               # This file
│   └── settings.json           # VS Code configuration
│
├── .gitignore
├── dbt_project.yml
├── docker-compose.yaml         # Docker services configuration
├── Dockerfile
├── LICENSE
├── main.py                     # Main pipeline entrypoint
├── README.md
└── requirements.txt
```

---

# 3. Layered Architecture

## Architecture Philosophy

The project implements a **medallion architecture** (Bronze/Silver/Gold) adapted to local execution:

- **RAW Layer**: Original, unmodified source data
- **STAGING Layer**: Standardized, cleaned data (wide and long formats)
- **MARTS Layer**: Analytical aggregations and business logic (dbt)

## Data Flow

```
Anatel ODS (dados.gov.br)
    ↓ [Selenium Web Scraper]
RAW Layer (data/raw/*.ods)
    ↓ [Python/ODS utilities]
TEMP Layer (data/temp/ods_csv/*.csv)
    ↓ [PySpark Wide Standardization]
STAGING Wide (data/staging/wide/*.parquet)
    ↓ [PySpark Long Transformation]
STAGING Long (data/staging/long-files/*.parquet)
    ↓ [dbt Staging Models]
    ↓ [dbt Mart Models]
MARTS Layer (data/marts/*.parquet or DuckDB)
    ↓
Analytics & Reporting
```

## Layer Responsibilities

### RAW Layer (`data/raw/`)

- **Purpose**: Store original, unmodified source files
- **Format**: ODS files from Anatel datasets
- **Processing**: Only extraction, no transformation
- **Maintenance**: Append-only (preserve source integrity)

### STAGING Layer (`data/staging/`)

#### Wide Format (`data/staging/wide/`)
- **Purpose**: Standardized source data in original wide structure
- **Processing**: Column normalization, header cleaning, data type standardization
- **Output**: Parquet files
- **Usage**: Intermediate layer for transformations

#### Long Format (`data/staging/long-files/`)
- **Purpose**: Analytical-ready long format (normalized structure)
- **Processing**: Wide-to-long transformation (melt/unpivot)
- **Output**: Parquet files
- **Columns**: `competencia`, `unidade`, `variavel`, `valor`

### MARTS Layer (`data/marts/`)

- **Purpose**: Analytical, business-oriented datasets
- **Owner**: dbt models
- **Processing**: Aggregations, business logic, KPIs
- **Output**: Parquet and DuckDB tables
- **Usage**: Analytics, reporting, dashboards

### TEMP Layer (`data/temp/`)

- **Purpose**: Temporary processing artifacts
- **Maintenance**: Safe to delete between runs
- **Usage**: Intermediate CSV files during ODS conversion
- **Note**: Minimize usage, prefer direct Spark processing

---

# 4. Path Management

## Rule: Centralized Paths

All file paths must be defined in:

```text
src/utils/paths.py
```

### Path Management Standards

```python
from src.utils.paths import (
    PROJECT_ROOT,
    DATA_DIR,
    RAW_DIR,
    STAGING_DIR,
    MARTS_DIR,
    TEMP_DIR,
    LOGS_DIR,
    DOCS_DIR,
    create_directories,
)
```

### Rules

1. **No hardcoded paths** - Never hardcode local paths in scripts
2. **Reuse centralized variables** - Use imports from `paths.py`
3. **Relative to PROJECT_ROOT** - All paths computed relative to project root
4. **Automatic directory creation** - Call `create_directories()` in main workflows

---

# 5. Module Standards

## Core Modules

### Ingestion Module (`src/ingestion/`)

**refactor_scraping_class.py**
- Class: `AnatelPerformanceScraper`
- Purpose: Automated download of Anatel performance files from dados.gov.br
- Features:
  - Selenium headless browser automation
  - Dynamic element waiting
  - Automatic download directory management
  - Error logging and recovery
- Usage:
  ```python
  from src.ingestion.refactor_scraping_class import AnatelPerformanceScraper
  
  scraper = AnatelPerformanceScraper(download_directory="./data/raw")
  downloaded_files = scraper.run(source_url="https://dados.gov.br/...")
  ```

### Processing Module (`src/processing/`)

**silver_long_transformer.py**
- Class: `AnatelLongPySparkTransformer`
- Purpose: Convert wide-format standardized data to long-format analytical structure
- Process:
  1. Read wide parquet from `STAGING_DIR`
  2. Apply PySpark transformations (melt/unpivot)
  3. Standardize column names
  4. Write long-format parquet to `STAGING_LONG_FILES_DIR`

**upload_parquet_to_s3.py**
- Purpose: Upload generated parquet files to S3 (LocalStack compatible)
- Configuration: Uses environment variables for S3 credentials

### Utilities Module (`src/utils/`)

#### **paths.py**
- Centralized directory management
- Exports: `PROJECT_ROOT`, `DATA_DIR`, `RAW_DIR`, `STAGING_DIR`, `MARTS_DIR`, `LOGS_DIR`
- Function: `create_directories()` - Creates missing directories

#### **ods_utils.py**
- ODS file reading and conversion
- Pandas integration for tabular extraction

#### **normalization.py**
- Column name standardization
- Data type conversion
- Schema harmonization

#### **spark_environment.py**
- Spark session configuration
- Java environment setup
- Local[*] optimization settings

#### **dataframe_utils.py**
- DataFrame manipulation helpers
- PySpark and Pandas utilities
- Schema utilities

#### **validation.py**
- Data quality checks
- Schema validation
- Null/anomaly detection

#### **comparison.py**
- Data comparison utilities
- Row-by-row validation
- Diff reporting

---

# 6. Analytics Engineering with dbt

## dbt Configuration

### Project Setup
- **Profile**: `anatel_dbt`
- **Database**: DuckDB (`data/duckdb/anatel.duckdb`)
- **Models Path**: `dbt/models/`
- **Seeds Path**: `dbt/seeds/` (static reference data)
- **Tests Path**: `dbt/tests/`
- **Snapshots Path**: `dbt/snapshots/`

### Model Organization

#### Staging Models (`dbt/models/staging/`)
- **Purpose**: Clean, standardized transformations of STAGING layer data
- **Materialization**: Views (ephemeral references)
- **Naming**: `stg_[source]_[entity]`
- **Responsibility**: Column renaming, type casting, basic filtering

#### Mart Models (`dbt/models/marts/`)
- **Purpose**: Analytical, business-oriented aggregations
- **Materialization**: Tables (persistent storage)
- **Naming**: `mart_[domain]_[entity]`
- **Responsibility**: Business logic, KPIs, aggregations
- **Examples**: `mart_anatel_smp_summary`, `mart_anatel_smp_kpis`

### dbt Best Practices

1. **Model Documentation** - Add descriptions to models and columns
2. **Testing** - Implement uniqueness, null, and referential tests
3. **Source Definitions** - Define sources pointing to parquet/DuckDB tables
4. **Lineage** - Maintain clear upstream/downstream dependencies
5. **Freshness** - Monitor source data freshness

### Execution

```bash
# Test dbt project structure
dbt parse --project-dir dbt

# Run models
dbt run --project-dir dbt

# Run tests
dbt test --project-dir dbt

# Generate documentation
dbt docs generate --project-dir dbt

# View lineage
dbt docs serve --project-dir dbt --port 8001
```

---

# 7. Processing Standards

## Main Pipeline Execution

**Entrypoint**: `python main.py`

**Flow**:
1. Initialize directories via `create_directories()`
2. Run PySpark transformations
3. Generate parquet outputs
4. Execute dbt models
5. Log results

## Data Processing Philosophy

### Prefer

- Modular functions with single responsibility
- Explicit transformations with clear intent
- Deterministic processing (same input → same output)
- Reproducible outputs with versioning
- Schema standardization before processing
- Native Spark operations (avoid `.toPandas()`)

### Avoid

- Hidden side effects
- Hardcoded transformations
- Duplicated logic across modules
- Unnecessary intermediate layers
- Implicit data type conversions
- Non-deterministic operations

---

# 8. PySpark Standards

## Objectives

PySpark is used for:
- Scalable distributed-style transformations
- Wide-to-long format conversions (melt/unpivot)
- Large-scale parquet generation
- Performance-critical data manipulations

## Guidelines

1. **Prefer native operations** - Use Spark SQL and DataFrame API
2. **Minimize pandas conversions** - Avoid `.toPandas()` for large datasets
3. **Explicit transformations** - Make data lineage clear
4. **Schema first** - Define schemas before ingestion
5. **Partition awareness** - Optimize for partition pruning
6. **Caching strategy** - Cache reused DataFrames strategically

---

# 9. Python Scripts & Notebooks

## Script Standards

All analytical scripts in `notebooks/` and `sandbox/` should:

1. **Be executable** - Run directly: `python script.py`
2. **Have docstrings** - Module-level documentation at top
3. **Use centralized imports** - Import from `src/utils/` modules
4. **Handle errors gracefully** - Try/except with logging
5. **Clean output** - Use print() or logging appropriately

## Python Notebook Conversion (No .ipynb)

**Policy**: Use `.py` files instead of `.ipynb` files

- `.py` files are version-control friendly
- Better integration with IDEs and linters
- Easier to incorporate into CI/CD pipelines
- Cell structure preserved with comments

### Script Template

```python
"""
Module docstring describing purpose and key functions.
"""

# ============================================================================
# Cell 1: Imports and Setup
# ============================================================================

import pandas as pd
from src.utils.paths import RAW_DIR

# ============================================================================
# Cell 2: Data Loading
# ============================================================================

def load_data():
    """Load and return sample data."""
    ...

# ============================================================================
# Cell 3: Analysis
# ============================================================================

if __name__ == "__main__":
    data = load_data()
    print(data.head())
```

---

# 10. Naming Conventions

## Python Files

Use snake_case with descriptive names:

```text
silver_long_transformer.py
refactor_scraping_class.py
```

Avoid abbreviations unless industry-standard.

## Functions & Methods

Use snake_case:

```python
def process_wide_to_long():
    pass

def transform_raw_data():
    pass
```

## Classes

Use PascalCase:

```python
class AnatelPerformanceScraper:
    pass

class AnatelLongPySparkTransformer:
    pass
```

## Variables

Use descriptive snake_case:

```python
parquet_output_path = RAW_DIR / "output.parquet"
source_dataframe = spark.read.parquet(input_path)
```

## Database/Table Names

Use snake_case with prefixes:

```sql
stg_anatel_smp_raw
mart_anatel_smp_summary
```

---

# 11. Version Control

## Branch Strategy

Use conventional prefixes:

```text
feat/      Feature implementation
fix/       Bug fixes
refactor/  Code restructuring
docs/      Documentation updates
chore/     Maintenance tasks
```

### Branch Examples

```text
feat/dbt-mart-models
fix/spark-memory-issue
refactor/simplify-ingestion
docs/architecture-update
chore/dependency-update
```

## Commit Messages

Use clear, descriptive messages:

```
feat: add mart_anatel_smp_kpis model

refactor: simplify path management logic

fix: handle missing values in normalization
```

---

# 12. Git Rules

## Do Not Version Control

Never commit:

```text
env/                       # Virtual environments
env311/
__pycache__/               # Python caches
.ipynb_checkpoints/
*.pyc
data/temp/                 # Temporary processing
data/raw/                  # Large source files (consider .gitignore)
*.parquet                  # Generated outputs
*.duckdb                   # Generated databases
dbt/target/                # dbt outputs
dbt/dbt_packages/          # dbt dependencies
logs/                      # Execution logs
target/                    # dbt legacy target
.env                       # Environment secrets
```

## Maintain Clean Repository

1. Remove obsolete scripts after refactors
2. Avoid duplicated modules
3. Keep module responsibilities distinct
4. Archive experimental code in `sandbox/` or `src/trash/`
5. Document deprecated code with comments

---

# 13. Documentation Standards

## README.md

Must explain:
- Project purpose and objectives
- Architecture and data flow
- Key technologies and dependencies
- Quick start instructions
- Project structure
- Main components
- Future enhancements

## Architecture Documentation

System design decisions belong in:

```text
docs/architecture/
```

### Key Architecture Docs

- `raw_wide_ingestion_architecture.md` - RAW to STAGING wide layer
- `vault_of_future_improvements.md` - Planned enhancements

## Code Comments

- Add docstrings to all functions and classes
- Comment complex business logic
- Document assumptions and limitations
- Keep comments concise and up-to-date

---

# 14. Engineering Philosophy

This project prioritizes:

| Principle | Over |
|-----------|------|
| Clarity | Cleverness |
| Reproducibility | Convenience |
| Maintainability | Quick fixes |
| Modularity | Monolithic scripts |
| Learning | Premature optimization |
| Documentation | Implicit knowledge |

---

# 15. Future Engineering Direction

## Planned Enhancements

- **Orchestration**: Apache Airflow DAG implementation
- **Cloud Evolution**: AWS/GCP cloud-ready architecture
- **Performance**: Distributed Spark cluster capabilities
- **Monitoring**: Data quality and pipeline observability
- **Containerization**: Docker-based reproducible execution
- **CI/CD**: Automated testing and deployment
- **Incremental**: Incremental processing strategies

## Technology Roadmap

- [ ] Airflow orchestration
- [ ] Cloud storage integration
- [ ] Advanced dbt tests and exposures
- [ ] Data quality frameworks
- [ ] Monitoring and alerting
- [ ] API layer for data access
- [ ] Containerized execution

---

# 16. Quick Reference

## Environment Setup
```bash
py -3.11 -m venv env311
.\env311\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Common Commands

```bash
# Run main pipeline
python main.py

# Test Spark
python notebooks/test_spark.py

# Run dbt
dbt run --project-dir dbt

# Test dbt models
dbt test --project-dir dbt
```

## File Organization Checklist

- [ ] All paths in `src/utils/paths.py`
- [ ] Python files use snake_case
- [ ] Classes use PascalCase
- [ ] Functions have docstrings
- [ ] dbt models documented
- [ ] No hardcoded paths
- [ ] No .ipynb files
- [ ] No __pycache__ committed

---

# Processing Standards

## Transformation Execution

Current transformation entrypoint:

```bash
python -m src.processing.silver_long_transformation
```

## Data Processing Philosophy

Prefer:

- modular functions
- explicit transformations
- deterministic processing
- reproducible outputs
- schema standardization

Avoid:

- hidden side effects
- hardcoded transformations
- duplicated logic
- unnecessary temporary layers

---

# PySpark Standards

## Objectives

PySpark is used for:

- scalable transformations
- distributed-style processing simulation
- analytical restructuring
- parquet generation

## Guidelines

- Avoid unnecessary `.toPandas()` usage.
- Prefer native Spark transformations whenever possible.
- Keep transformations explicit and readable.
- Standardize schemas before Spark ingestion.

---

# Naming Conventions

## Python Files

Use:

```text
snake_case.py
```

## Functions

Use:

```python
def process_data():
```

## Classes

Use:

```python
class DataTransformer:
```

## Variables

Use descriptive snake_case names.

Avoid abbreviations unless widely recognized.

---

# Version Control

## Branch Strategy

Recommended prefixes:

```text
feat/
fix/
refactor/
docs/
chore/
```

Examples:

```text
feat/parquet-layer
refactor/remove-temp-csv-layer
docs/architecture-update
chore/repository-cleanup
```

---

# Git Rules

## Do Not Version

Never commit:

```text
env/
env311/
__pycache__/
.ipynb_checkpoints/
data/temp/
generated parquet outputs
```

## Keep Repository Clean

- Remove obsolete files after refactors.
- Avoid duplicated scripts.
- Keep folder responsibilities clear.

---

# Documentation Standards

## README

The README should explain:

- project purpose
- architecture
- execution steps
- repository organization

## Architecture Notes

Architecture decisions and future improvements belong in:

```text
docs/architecture/
```

---

# Future Engineering Direction

Planned future evolutions include:

- improved Spark-native ingestion
- incremental processing
- orchestration concepts
- observability improvements
- Dockerized execution
- dbt integration
- cloud-oriented architecture evolution

---

# Engineering Philosophy

This repository prioritizes:

- clarity over cleverness
- reproducibility over convenience
- maintainability over shortcuts
- modularity over monolithic scripts
- engineering learning over premature optimization