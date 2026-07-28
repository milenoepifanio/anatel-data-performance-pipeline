# Source Code — PDI

This directory contains the Python implementation of the PDI data pipeline. It brings together ingestion, transformation, orchestration, and reusable utilities to process Anatel data from raw ODS files through analytical outputs.

## Purpose

The source code in this folder is responsible for:

- downloading source files from the Anatel public dataset portal;
- converting raw ODS input into standardized data structures;
- applying PySpark-based transformations to produce long-format parquet files;
- uploading generated artifacts to a LocalStack-compatible S3 environment;
- triggering dbt models as part of the downstream analytics workflow.

---

## Main Entry Point

The main execution flow starts in [src/main.py](main.py):

```bash
python src/main.py
```

This script coordinates the whole pipeline by calling the ingestion, transformation, upload, and orchestration modules in sequence.

---

## Project Structure

| Area | Description |
|------|-------------|
| [ingestion](ingestion/) | Ingestion layer, including the scraper used to fetch Anatel performance files |
| [processing](processing/) | Data processing modules for transforming raw files into analytical parquet datasets |
| [orchestration](orchestration/) | Pipeline control and environment integration components |
| [utils](utils/) | Reusable helper modules shared across the pipeline |

### Key Modules

| Module | Purpose |
|--------|---------|
| [ingestion/refactor_scraping_class.py](ingestion/refactor_scraping_class.py) | Selenium-based scraper for downloading source ODS files |
| [processing/silver_long_transformer.py](processing/silver_long_transformer.py) | PySpark transformation from wide to long format |
| [processing/upload_parquet_to_s3.py](processing/upload_parquet_to_s3.py) | Upload logic for parquet files to S3/LocalStack |
| [orchestration/environment.py](orchestration/environment.py) | Validates required environment variables |
| [orchestration/localstack.py](orchestration/localstack.py) | Checks and initializes the LocalStack S3 bucket |
| [orchestration/dbt_runner.py](orchestration/dbt_runner.py) | Executes dbt steps after data preparation |
| [utils/paths.py](utils/paths.py) | Centralizes project directories and environment paths |
| [utils/ods_utils.py](utils/ods_utils.py) | Utilities for reading ODS files |
| [utils/normalization.py](utils/normalization.py) | Standardization of datasets and columns |
| [utils/spark_environment.py](utils/spark_environment.py) | Spark session configuration |
| [utils/validation.py](utils/validation.py) | Input and output validation checks |
| [utils/dataframe_utils.py](utils/dataframe_utils.py) | Helpers for DataFrame manipulation |
| [utils/file_utils.py](utils/file_utils.py) | File system utilities |
| [utils/comparison.py](utils/comparison.py) | Comparison utilities for validating transformations |

---

## Execution Flow

1. Environment validation
2. LocalStack/S3 readiness check
3. Raw data ingestion from the source portal
4. PySpark transformation into long-format parquet
5. File upload to the configured storage layer
6. dbt execution for downstream analytical models

---

## Notes

- The pipeline is designed to run from the repository root.
- A working Python 3.11 environment and the dependencies listed in the repository requirements are expected.
- LocalStack is used for local S3-like testing during development.
