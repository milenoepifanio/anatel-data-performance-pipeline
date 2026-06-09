# Medallion Architecture

## Overview

This document describes the Medallion Architecture adopted in the Anatel Data Engineering project.

The architecture follows a layered approach designed to improve data quality, maintainability, governance, and analytical consumption.

The project currently implements a local Medallion Architecture using:

- Python
- PySpark
- DuckDB
- dbt
- LocalStack (S3 simulation)
- Parquet

The objective is to separate ingestion, transformation, and analytical consumption responsibilities into distinct layers.

---

# Architecture Overview

```text
Anatel ODS Files
        │
        ▼
┌─────────────────┐
│      RAW        │
│ Original ODS    │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│   SILVER        │
│ Standardized    │
│ Long Format     │
│ PySpark         │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│      GOLD       │
│ dbt Models      │
│ DuckDB          │
│ Analytics       │
└─────────────────┘
```

---

# Layer Responsibilities

## RAW Layer

### Purpose

Store the original source files exactly as downloaded from the official source.

No business transformation should occur in this layer.

### Location

```text
data/raw/
```

### Input Files

Examples:

```text
SCM2016.ods
SEAC2019.ods
SMP2014.ods
STFC2017.ods
```

### Characteristics

- Original files
- Immutable
- Source of truth
- No transformations
- No business rules

### Main Objective

Preserve source integrity and guarantee reproducibility.

---

# SILVER Layer

## Purpose

Standardize, clean, validate and normalize the source data.

This layer transforms heterogeneous source structures into a consistent analytical format.

### Location

```text
data/staging/long-files/
```

### Technology

```text
PySpark
```

### Main Processing Steps

```text
ODS Reading
    ↓
Header Detection
    ↓
Schema Standardization
    ↓
Numeric Normalization
    ↓
Wide Validation
    ↓
Wide → Long Transformation
    ↓
Long Validation
    ↓
Metadata Enrichment
    ↓
Parquet Generation
```

### Implemented Features

#### Schema Standardization

Examples:

```text
Grupo Econômico → grupo_economico
Variável → variavel
```

#### Numeric Standardization

Examples:

```text
1.234,56 → 1234.56
15,8     → 15.8
```

#### Date Standardization

Examples:

```text
2019/01 → mes_2019_01
```

Converted to:

```text
2019-01
```

during long transformation.

#### Wide-to-Long Transformation

Input:

| grupo_economico | variavel | mes_2019_01 | mes_2019_02 |
|----------------|-----------|------------|------------|
| OI | Reclamações | 100 | 120 |

Output:

| grupo_economico | variavel | competencia | valor |
|----------------|-----------|------------|--------|
| OI | Reclamações | 2019-01 | 100 |
| OI | Reclamações | 2019-02 | 120 |

#### Metadata Enrichment

Generated columns:

```text
arquivo_origem
aba_origem
modelo
ano_arquivo
_ingestion_timestamp
_processing_date
_record_hash
```

#### Data Quality Validation

Implemented validations:

- Required columns
- Null validation
- Empty dataset prevention
- Competência format validation
- Duplicate detection

### Output Format

```text
Apache Parquet
Compression: Snappy
```

### Example Output

```text
SCM2016_Banda_Larga_Fixa_long.parquet
SMP2014_Movel_Pessoal_long.parquet
SEAC2019_SeAC_long.parquet
```

---

# GOLD Layer

## Purpose

Provide business-ready datasets for analytical consumption.

This layer contains curated and aggregated datasets generated using dbt.

### Technologies

```text
DuckDB
dbt
```

### Current Architecture

```text
Silver Parquet
      ↓
DuckDB External Sources
      ↓
dbt Staging Models
      ↓
dbt Mart Models
```

---

## Staging Models

Purpose:

- Type casting
- Final standardization
- Source abstraction
- Governance

Example:

```text
stg_anatel_ida_smp
```

---

## Mart Models

Purpose:

- KPI generation
- Aggregations
- Business metrics

Examples:

```text
mart_anatel_smp_summary
mart_anatel_smp_kpis
```

---

## Current dbt Governance

Implemented:

- Source definitions
- Schema documentation
- Data tests
- Business key validation
- Accepted values validation
- Column descriptions

Current baseline:

| Item | Quantity |
|--------|----------|
| Sources | 1 |
| Models | 3 |
| Tests | 26 |

---

# Current Data Flow

```text
dados.gov.br
       │
       ▼
RAW
(data/raw/*.ods)
       │
       ▼
PySpark
       │
       ▼
SILVER
(data/staging/long-files/*.parquet)
       │
       ▼
LocalStack S3
(anatel-lake/silver/anatel_long/)
       │
       ▼
DuckDB
       │
       ▼
dbt
       │
       ▼
GOLD
(Marts & KPIs)
```

---

# Storage Architecture

## Local Processing

```text
data/
├── raw/
├── staging/
│   ├── wide/
│   └── long-files/
├── marts/
└── duckdb/
```

---

## Data Lake

Current implementation:

```text
LocalStack S3
```

Bucket:

```text
anatel-lake
```

Prefix:

```text
silver/anatel_long/
```

---

# Metadata Strategy

Current metadata fields:

```text
_ingestion_timestamp
_processing_date
_record_hash
arquivo_origem
aba_origem
modelo
ano_arquivo
```

Objectives:

- Traceability
- Lineage
- Auditing
- Reprocessing support

---

# Future Evolution

Planned improvements:

## Silver Layer

- Native Spark parquet writing
- Partitioning by model
- Partitioning by year
- Incremental processing
- Additional automated testing

## Gold Layer

- Additional analytical marts
- Additional domains (SCM, STFC, SEAC)
- KPI expansion
- Exposures

## Platform

- Airflow orchestration
- Docker execution
- CI/CD
- Monitoring
- Data quality framework

## Lakehouse

Potential future migration:

- Delta Lake
- Apache Iceberg
- Apache Hudi

---

# Architectural Principles

The project follows the following principles:

| Principle | Description |
|------------|------------|
| Reproducibility | Same input produces same output |
| Modularity | Clear separation of responsibilities |
| Governance | Documented transformations and validations |
| Traceability | Metadata and lineage preservation |
| Scalability | Architecture prepared for future growth |
| Maintainability | Modular and reusable components |

---

# Current Status

| Layer | Status |
|---------|---------|
| RAW | Implemented |
| SILVER | Implemented |
| GOLD | Partially Implemented |
| Data Lake | Implemented (LocalStack) |
| dbt Governance | Implemented |
| Orchestration | Planned |
| Observability | Planned |

---

**Version:** 1.0
**Architecture:** Medallion Architecture
**Status:** Active