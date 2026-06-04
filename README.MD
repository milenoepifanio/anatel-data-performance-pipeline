# PDI — Data Engineering Growth

## Objective

Strengthen modern Data Engineering skills by building an analytical pipeline using public Anatel datasets.

The project focuses on applying layered architecture concepts, scalable data processing, Analytics Engineering practices, reproducible environments, and DataOps fundamentals to consolidate a stronger technical profile inside the organization.

### Key Technologies

- **Python 3.11** with layered architecture
- **PySpark** for distributed data processing
- **dbt** for Analytics Engineering
- **DuckDB** for analytical querying
- **Selenium** for web scraping
- **Apache Airflow** ready architecture

---

## Project Architecture

### Data Pipeline Flow

```
Raw ODS Files (Anatel)
    ↓
Web Scraping (Selenium) → RAW Layer
    ↓
Temporary CSV Conversion
    ↓
PySpark Wide Standardization → STAGING (Wide)
    ↓
PySpark Long Transformation → STAGING (Long)
    ↓
dbt Staging Models
    ↓
dbt Mart Models → MARTS Layer
    ↓
Analytics & Reporting
```

### Layered Architecture

```
data/
├── raw/                    # Original downloaded ODS files
├── staging/
│   ├── wide/              # Standardized wide format parquet
│   └── long-files/        # Long format parquet (melted)
├── marts/                 # Final analytical tables
└── duckdb/
    └── anatel.duckdb      # Analytical database
```

---

## Current Implementation Status

### ✅ Completed

- Repository structure with layered architecture
- RAW ingestion process with Anatel ODS files
- Web scraping module (Selenium-based AnatelPerformanceScraper)
- PySpark wide format standardization
- PySpark wide-to-long transformation
- Parquet generation pipeline
- dbt project setup with staging and marts models
- Centralized utilities (paths, normalization, validation)
- Python scripts for all notebooks (removed .ipynb dependencies)
- Environment configuration with Python 3.11

### 🔄 In Progress

- dbt model refinement and testing
- Analytics engineering best practices
- Data quality validation

### 📋 Future Enhancements

- Apache Airflow orchestration
- Data quality monitoring
- Performance optimization
- Documentation automation

---

## Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
py -3.11 -m venv env311

# Activate environment (PowerShell)
.\env311\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Project Structure

Explore the key modules:
- `src/ingestion/` - Web scraping with Selenium
- `src/processing/` - PySpark transformations
- `src/utils/` - Reusable utilities and helpers
- `dbt/models/` - Analytics models (staging and marts)
- `notebooks/` - Analytical scripts in Python format

### 3. Running Transformations

```bash
# Execute main pipeline
python main.py

# Run PySpark transformations
python -m src.processing.silver_long_transformer

# Run dbt models
dbt run --project-dir dbt
dbt test --project-dir dbt
```

### 4. Web Scraping

The `AnatelPerformanceScraper` class downloads performance files:

```python
from src.ingestion.refactor_scraping_class import AnatelPerformanceScraper

scraper = AnatelPerformanceScraper(download_directory="./data/raw")
downloaded = scraper.run(source_url="https://dados.gov.br/...")
```

---

## Key Components

### Python Modules

#### `src/ingestion/`
- **refactor_scraping_class.py** - Anatel web scraper using Selenium
  - Automated ODS file downloads from dados.gov.br
  - Headless browser automation
  - Download directory management

#### `src/processing/`
- **silver_long_transformer.py** - PySpark wide-to-long transformation
- **upload_parquet_to_s3.py** - S3 upload utilities (LocalStack compatible)

#### `src/utils/`
- **paths.py** - Centralized directory management
- **ods_utils.py** - ODS file utilities
- **normalization.py** - Column and data standardization
- **spark_environment.py** - Spark session configuration
- **dataframe_utils.py** - DataFrame manipulation helpers
- **file_utils.py** - File system utilities
- **comparison.py** - Data comparison utilities
- **validation.py** - Data validation helpers

### Analytics Scripts

Located in `notebooks/` and `sandbox/`:

- **test_spark.py** - Spark session testing
- **test_read_s3.py** - S3/DuckDB integration testing
- **test_long_silver.py** - Long format data validation
- **view_dbt_marts_data.py** - dbt model inspection
- **initial_scraping.py** - Initial scraping experiments
- **refactor_scraping.py** - Refactored scraper class testing

### Analytics Engineering

#### dbt Configuration
- Models: `dbt/models/staging/` and `dbt/models/marts/`
- Seeds: `dbt/seeds/` - Static reference data
- Snapshots: `dbt/snapshots/` - Slowly changing dimensions
- Tests: `dbt/tests/` - Model validation
- Profile: DuckDB-based analytics database

---

## Dependencies

### Core Data Processing
- **pandas** ≥2.0.0 - Data manipulation
- **pyarrow** ≥15.0.0 - Parquet I/O
- **pyspark** ≥4.0.0 - Distributed processing
- **odfpy** ≥1.4.1 - ODS file reading
- **python-dotenv** ≥1.0.0 - Environment management

### Web Scraping
- **selenium** ≥4.10.0 - Browser automation
- **webdriver-manager** ≥4.0.0 - WebDriver management
- **beautifulsoup4** ≥4.12.0 - HTML parsing
- **requests** ≥2.28.0 - HTTP requests
- **lxml** ≥4.9.0 - XML processing

### Development & Analytics
- **jupyter** & **ipykernel** - Interactive notebooks
- **dbt-core** - Analytics engineering framework

---

## Project Rules & Conventions

See [.vscode/.rules.md](.vscode/.rules.md) for detailed engineering conventions,
code standards, and architectural decisions.

Key highlights:
- Python 3.11 required
- Layered data architecture (RAW → STAGING → MARTS)
- Centralized dependency management
- dbt for analytical transformations
- Reproducible local environment

- Decoupled analytical transformations
- Reusable dbt models
- Analytics-ready datasets
- Better separation of concerns

---

## Stage 4 — DataOps & Reproducibility

### Description

Introduce DataOps practices to improve reliability, maintainability, and
technical reproducibility.

### Actions

- Implement logging improvements
- Add basic error handling
- Maintain Git versioning practices
- Improve technical documentation
- Configure reproducible Python environments
- Introduce Docker concepts for reproducibility

### Expected Outcome

- Reproducible pipeline execution
- Better operational organization
- Improved debugging capability
- Cleaner development workflow

---

## Stage 5 — Architecture Consolidation

### Description

Refine the overall pipeline architecture and improve maintainability,
organization, and engineering scalability.

### Actions

- Improve separation between processing layers
- Refine modularization of the pipeline
- Expand architecture documentation
- Compare processing approaches between Python and dbt
- Improve repository organization and cleanup

### Expected Outcome

- Cleaner architecture
- Better maintainability
- Improved engineering reasoning
- Production-oriented project organization

---

## Stage 6 — DevOps/DataOps Upskilling

### Description

Connect DevOps and DataOps concepts studied externally with practical
applications inside the project.

### Actions

- Continue DevOps/DataOps studies
- Apply concepts incrementally to the project
- Explore observability and orchestration concepts
- Consolidate operational engineering fundamentals

### Expected Outcome

- Stronger operational perspective
- Better understanding of scalable data systems
- Improved engineering maturity

---

# Continuous Conceptual Foundation

## Description

Consolidate theoretical foundations of modern Data Engineering and relate
studied concepts to real architectural decisions implemented in the project.

## Actions

- Progressive reading of *Fundamentals of Data Engineering*
- Map theoretical concepts to implementation decisions
- Study layered architectures and analytical modeling
- Reinforce DataOps and scalability concepts

## Expected Outcome

- Stronger conceptual understanding
- Better alignment between theory and practice
- Improved architectural decision-making

---

# Final Expected Results

- Functional analytical pipeline
- Layered architecture (`raw` / `staging` / `marts`)
- PySpark processing experience
- Parquet-based analytical datasets
- Reproducible local execution environment
- Improved DataOps practices
- Hands-on Analytics Engineering experience
- Stronger internal technical positioning
- Better architectural reasoning in Data Engineering

---

# Current Pipeline Flow

```text
ODS → pandas → Spark DataFrame → Parquet
```

---

# Quick Start

## 1. Create virtual environment

### Python 3.11 recommended

```bash
py -3.11 -m venv env311
```

---

## 2. Activate virtual environment

### PowerShell

```bash
.\env311\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run transformation pipeline

```bash
python -m src.processing.silver_long_transformation
```

---

# Supporting Files

- `requirements.txt` → project dependencies
- `src/utils/paths.py` → centralized project paths
- `docs/` → architecture and future improvements
- `LICENSE` → personal usage license

---

# Future Improvements

Some future architectural ideas already mapped include:

- Spark-native ingestion improvements
- Orchestration concepts
- Incremental processing
- Observability improvements
- Data quality validation
- Better partitioning strategies
- Dockerized execution
- Cloud-oriented architecture evolution

Detailed ideas are documented in:

```text
docs/architecture/vault_of_future_improvements.md
```