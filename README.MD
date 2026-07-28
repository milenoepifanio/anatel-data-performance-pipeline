# PDI — Data Engineering Growth

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PySpark](https://img.shields.io/badge/PySpark-Data_Processing-orange)
![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-yellow)
![LocalStack](https://img.shields.io/badge/LocalStack-S3-green)
![dbt](https://img.shields.io/badge/dbt-Analytics_Engineering-orange)

![Status](https://img.shields.io/badge/Status-In_Development-yellow)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

## Objective

Build a practical Data Engineering learning project around public Anatel datasets by combining ingestion, transformation, storage, and analytics in a layered architecture.

The repository currently implements a local pipeline that covers:

- ingestion of Anatel ODS files;
- Python and PySpark-based transformation steps;
- Parquet generation and S3-compatible storage via LocalStack;
- dbt models for staging and marts in DuckDB;
- documentation and experimental scripts for validation and exploration.

---

## Current Architecture

### Data Flow

```text
Anatel ODS files
    ↓
Selenium-based ingestion
    ↓
Raw data storage in data/raw
    ↓
PySpark wide-to-long transformation
    ↓
Parquet output in data/staging/long-files
    ↓
LocalStack / S3-compatible upload
    ↓
dbt staging and marts models
    ↓
DuckDB analytical output
```

### Repository Layout

```text
PDI/
├── src/                    # Python pipeline modules
├── dbt/                    # dbt models, sources, and tests
├── data/                   # raw, staging, marts, temp, and DuckDB storage
├── notebooks/              # validation and analysis scripts
├── sandbox/                # experiments and prototypes
├── docs/                   # architecture, dbt, docker, and learnings
├── docker-compose.yaml     # LocalStack + app environment
└── requirements.txt        # Python dependencies
```

---

## What Is Implemented

### ✅ Completed

- Python-based pipeline entry point in [src/main.py](src/main.py)
- Selenium ingestion module for downloading Anatel ODS files
- PySpark transformation for wide-to-long data preparation
- Parquet writing into the staging layer
- S3-compatible upload flow using LocalStack and boto3
- dbt project structure with staging and marts models
- DuckDB-based analytical output and dbt documentation assets
- Folder-level documentation under [docs/](docs/), [src/](src/), [notebooks/](notebooks/), [sandbox/](sandbox/), and [data/](data/)

### 🔄 In Progress

- orchestration and observability improvements across the Python and dbt layers
- broader data quality monitoring beyond the current schema tests

---

## Main Execution Flow

The main pipeline entry point is [src/main.py](src/main.py):

```bash
python src/main.py
```

That script orchestrates:

1. environment validation;
2. LocalStack / S3 readiness checks;
3. ingestion of Anatel source files;
4. PySpark transformation into long-format Parquet;
5. upload to the configured storage layer;
6. dbt model execution.

---

## Quick Start

### 1. Create and activate the environment

```bash
py -3.11 -m venv env311
.\env311\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure dbt

Copy the example profile to your local dbt profile location:

```bash
# Example path on Windows
copy docs\dbt\profiles.yml.example %USERPROFILE%\.dbt\profiles.yml
```

### 4. Run the pipeline

```bash
python src/main.py
```

### 5. Optional: run with Docker Compose

```bash
docker compose up -d
```

---

## Key Components

### Python pipeline

- [src/ingestion/refactor_scraping_class.py](src/ingestion/refactor_scraping_class.py) — scraper for downloading Anatel ODS files
- [src/processing/silver_long_transformer.py](src/processing/silver_long_transformer.py) — PySpark transformation logic
- [src/processing/upload_parquet_to_s3.py](src/processing/upload_parquet_to_s3.py) — upload flow for Parquet files
- [src/orchestration/environment.py](src/orchestration/environment.py) — environment validation
- [src/orchestration/localstack.py](src/orchestration/localstack.py) — LocalStack connection and bucket setup
- [src/orchestration/dbt_runner.py](src/orchestration/dbt_runner.py) — dbt execution wrapper

### dbt layer

- [dbt/models/staging/anatel/](dbt/models/staging/anatel/) — staging models and source definitions
- [dbt/models/marts/](dbt/models/marts/) — marts for analytical consumption
- [dbt_project.yml](dbt_project.yml) — dbt project configuration
- [docs/dbt/](docs/dbt/) — conceptual and operational dbt documentation

### Supporting folders

- [notebooks/](notebooks/) — validation and exploratory scripts
- [sandbox/](sandbox/) — experiments and prototypes
- [data/](data/) — raw, staging, marts, temp, and DuckDB data
- [docs/](docs/) — architecture, pipeline, and learning documentation

---

## Documentation Map

| Area                                       | Purpose                                |
| ------------------------------------------ | -------------------------------------- |
| [docs/architecture/](docs/architecture/)   | architecture and engineering standards |
| [docs/pipeline/](docs/pipeline/)           | pipeline documentation                 |
| [docs/dbt/](docs/dbt/)                     | dbt concepts and execution             |
| [docs/docker/](docs/docker/)               | Docker and container usage             |
| [docs/learnings/](docs/learnings/)         | technical learnings and project notes  |
| [src/README.md](src/README.md)             | source code overview                   |
| [data/README.md](data/README.md)           | data folder organization               |
| [notebooks/README.md](notebooks/README.md) | notebooks and analysis scripts         |
| [sandbox/README.md](sandbox/README.md)     | sandbox experiments                    |

---

## Dependencies

Core dependencies are declared in [requirements.txt](requirements.txt) and include:

- Python 3.11
- pandas
- pyarrow
- PySpark
- ODFPY
- python-dotenv
- boto3
- dbt-core
- dbt-duckdb
- DuckDB
- Selenium and related scraping packages

---

## Notes

This project is still evolving as a hands-on learning environment for modern Data Engineering practices. The structure is intentionally modular so that ingestion, transformation, analytics modeling, and documentation can be studied and improved independently.
