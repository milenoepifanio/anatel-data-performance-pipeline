# Pipeline Improvement Roadmap

## Overview

This document centralizes future technical improvements, architectural evolutions, optimization opportunities, and engineering ideas identified during the development of the Anatel ingestion and transformation pipeline.

The current project already implements:

- ODS ingestion
- normalization
- metadata enrichment
- wide-to-long transformation
- parquet generation
- PySpark processing

The next steps focus on scalability, maintainability, governance, observability, and preparation for production-grade data engineering environments.

---

# 1. Remove Temporary CSV Layer

## Current Architecture

```text
ODS → Temporary CSV → Spark → Parquet
```

## Proposed Future Architecture

```text
ODS → Spark DataFrame → Parquet
```

## Current Limitation

Spark does not natively support `.ods` files efficiently in the current local Windows environment.

Because of this, temporary CSV files are currently used as an intermediate layer.

## Future Improvement

Eliminate the temporary CSV dependency and perform direct ingestion into Spark DataFrames.

## Objectives

- reduce intermediate disk I/O
- reduce pipeline complexity
- improve performance
- reduce temporary storage usage
- reduce failure points
- simplify maintenance

## Expected Benefits

- cleaner architecture
- faster execution
- lower operational overhead
- easier orchestration

---

# 2. Incremental Processing Control

## Current Flow

- all `.ods` files are scanned
- existing parquet outputs are skipped

## Future Improvement

Implement true incremental ingestion and transformation control.

## Possible Strategies

### File-level validation

- hash comparison
- modified timestamp comparison
- checkpoint validation

### Metadata control table

```text
source_file
source_hash
source_modified_at
processed_at
processing_status
records_processed
```

## Objectives

- avoid unnecessary reprocessing
- improve execution time
- increase operational reliability
- simplify re-execution logic

## Expected Benefits

- faster pipelines
- lower compute usage
- better scalability
- operational traceability

---

# 3. Native Spark Parquet Writing

## Current Limitation

Native Spark parquet writing presented compatibility issues in the local Windows environment.

Current implementation uses:

```python
final_pdf.to_parquet()
```

after converting Spark DataFrames into pandas.

## Future Improvement

Use native distributed Spark parquet writing.

## Proposed Implementation

```python
df.write \
    .mode("overwrite") \
    .parquet(output_path)
```

## Recommended Environments

- Docker
- Linux
- WSL
- Databricks
- Cloud runtimes

## Expected Benefits

- distributed processing
- lower memory usage
- better scalability
- elimination of `.toPandas()`
- improved large dataset handling

---

# 4. Physical Partitioning Strategy

## Current Flow

One parquet file is generated per:

- source file
- worksheet

## Future Improvement

Implement physical partitioning by:

- model
- year

## Proposed Structure

```text
data/staging/long-files/
└── modelo=SCM/
    └── ano_arquivo=2016/
        └── SCM2016_Banda_Larga_Fixa_long.parquet
```

## Objectives

- improve query performance
- reduce scanning
- optimize analytical reads
- organize storage structure
- prepare for lakehouse architectures

## Expected Benefits

- partition pruning
- reduced I/O
- faster queries
- improved scalability

## Future Evolution

Potential compatibility with:

- Delta Lake
- Apache Iceberg
- Hive Metastore
- Lakehouse architectures

---

# 5. Automated Testing Layer

## Future Improvement

Implement automated validation and transformation tests.

## Suggested Coverage

### Functional tests

- column normalization
- month normalization
- metadata generation
- header detection
- schema consistency

### Transformation tests

- wide-to-long conversion
- numeric conversion
- duplicate prevention
- partition generation

## Suggested Structure

```text
tests/
├── test_column_normalization.py
├── test_numeric_conversion.py
├── test_metadata_columns.py
├── test_wide_to_long.py
├── test_partitioning.py
└── test_schema_consistency.py
```

## Objectives

- increase reliability
- reduce regressions
- improve maintainability
- facilitate refactoring

---

# 6. Medallion Architecture Evolution

## Current Architecture

```text
RAW
 └── ODS source files

SILVER
 └── normalization
 └── standardization
 └── wide → long transformation
 └── metadata enrichment
```

## Future Architecture

```text
RAW → SILVER → GOLD
```

## Possible GOLD Outputs

- KPI analytical marts
- operator rankings
- SLA monitoring
- historical indicators
- aggregated analytical datasets

## Objectives

- separate analytical consumption
- improve governance
- simplify BI usage
- improve reusability

---

# 7. Execution Orchestration

## Future Improvement

Implement orchestration and scheduling layer.

## Possible Tools

- Airflow
- Dagster
- Prefect
- IOMETE
- GitHub Actions

## Objectives

- scheduling
- retries
- dependency management
- execution monitoring
- observability
- centralized logging

## Expected Benefits

- automated executions
- improved reliability
- operational visibility
- easier maintenance

---

# 8. Data Quality Framework

## Future Improvement

Implement data quality validations.

## Suggested Validations

- duplicated rows
- invalid dates
- schema inconsistencies
- null critical fields
- unexpected numeric ranges

## Possible Tools

- Great Expectations
- dbt tests
- custom PySpark validations

## Objectives

- improve data reliability
- reduce analytical inconsistencies
- improve governance
- increase trust in datasets

---

# 9. Migration to Analytics Engineering Layer

## Future Improvement

Use dbt for analytical modeling after Silver ingestion.

## Proposed Architecture

```text
RAW
 └── source ingestion

SILVER
 └── normalization
 └── standardization

DBT
 ├── staging
 ├── intermediate
 └── marts
```

## Objectives

- modular SQL transformations
- lineage
- testing
- documentation
- governance
- analytical standardization

## Expected Benefits

- reusable transformations
- better maintainability
- analytical consistency
- improved collaboration

---

# 10. Logging and Observability Layer

## Future Improvement

Implement structured execution logging.

## Suggested Metadata

```text
execution_id
file_name
sheet_name
records_processed
status
started_at
finished_at
error_message
```

## Objectives

- execution traceability
- easier debugging
- operational monitoring
- execution auditing

## Future Possibilities

- centralized logging
- dashboards
- execution metrics
- alerts

---


# 11. Cloud and Data Lake Evolution

## Future Possibilities

Potential migration to cloud-native architecture.

## Possible Stack

- S3 / ADLS / GCS
- Spark cluster
- Delta Lake
- dbt
- Airflow
- Databricks

## Objectives

- scalability
- distributed compute
- lakehouse architecture
- production-grade pipelines

## Expected Benefits

- elastic processing
- lower operational limitations
- improved scalability
- enterprise-ready architecture

---

# 12. Schema Evolution Strategy

## Future Improvement

Implement schema evolution support.

## Objectives

- support new columns automatically
- reduce ingestion failures
- improve flexibility
- support source evolution

## Possible Approaches

- schema merge
- metadata-driven ingestion
- dynamic column handling

---

# 13. Reprocessing Strategy

## Future Improvement

Implement controlled reprocessing capabilities.

## Possible Scenarios

- source correction
- corrupted outputs
- transformation changes
- historical reloads

## Objectives

- reproducibility
- operational recovery
- historical consistency

---

# 14. Metadata Layer Expansion

## Current Metadata

```text
_ingestion_timestamp
_processing_date
_record_hash
```

## Future Metadata

```text
_source_file
_source_sheet
_pipeline_version
_execution_id
_processing_status
_created_at
_updated_at
```

## Objectives

- improve traceability
- improve governance
- simplify auditing
- facilitate debugging

---

# 15. Future Migration to Lakehouse Standards

## Possible Evolution

Future migration from plain parquet files to transactional lakehouse formats.

## Potential Technologies

- Delta Lake
- Apache Iceberg
- Apache Hudi

## Expected Benefits

- ACID transactions
- schema evolution
- time travel
- merge/upsert support
- scalable metadata handling
```