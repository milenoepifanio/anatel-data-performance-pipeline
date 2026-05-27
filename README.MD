# PDI — Data Engineering Growth (Cycle until 2026-06-30)

## Objective

Strengthen modern Data Engineering skills by building an analytical pipeline
using public Anatel datasets.

The project focuses on applying layered architecture concepts, scalable data
processing, Analytics Engineering practices, reproducible environments, and
DataOps fundamentals to consolidate a stronger technical profile inside the
organization.

The pipeline currently includes:

- `.ods` ingestion from public Anatel datasets
- layered data architecture
- metadata enrichment
- normalization and standardization
- wide-to-long analytical transformation
- PySpark processing
- parquet generation
- reproducible local execution environment

---

# Project Stages

## Stage 1 — Repository Structure & RAW Ingestion

### Description

Create the initial project foundation, organize repository layers, and build
the first ingestion pipeline for public `.ods` datasets.

### Actions

- Create initial repository structure
- Organize project using layered architecture
- Implement RAW ingestion process
- Standardize project paths and directories
- Centralize reusable utilities and configurations

### Expected Outcome

- Organized repository structure
- Running RAW ingestion pipeline
- Reusable project scaffolding
- Standardized directory management

---

## Stage 2 — PySpark Processing & Analytical Transformation

### Description

Implement scalable analytical transformations using PySpark and normalize
datasets for analytical consumption.

### Actions

- Implement PySpark processing pipeline
- Normalize column names and metadata
- Convert datasets from wide → long format
- Standardize dates and schema structure
- Generate parquet datasets
- Remove temporary CSV dependency from the transformation flow

### Expected Outcome

- Analytical long-format datasets
- Standardized parquet outputs
- Simplified transformation architecture
- Reduced intermediate processing overhead

### Current Architecture

```text
ODS → pandas → Spark DataFrame → Parquet
```

---

## Stage 3 — Analytics Engineering with dbt

### Description

Apply Analytics Engineering principles using `dbt` to separate ingestion,
transformation, and analytical consumption layers.

### Actions

- Set up `dbt` project structure
- Create `staging` models
- Create `marts` models
- Standardize analytical transformations
- Add basic model testing
- Organize analytical business logic

### Expected Outcome

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