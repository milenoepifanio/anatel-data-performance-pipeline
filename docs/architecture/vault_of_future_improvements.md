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
- **dbt governance and quality baseline** for the Anatel SMP layer (sources, staging, marts, schema tests, documentation)

The next steps focus on scalability, maintainability, extended governance (orchestration, CI, freshness automation), observability, and preparation for production-grade data engineering environments.

**Reference:** [dbt conceptual guide](../dbt/guia_conceitual_dbt.md) · [dbt execution runbook](../dbt/dbt_execution.md)

---

# 1. Remove Temporary CSV Layer

## Status

✅ Implemented

## Previous Architecture

```text
ODS → Temporary CSV → Spark → Parquet
```

## Proposed Future Architecture

```text
ODS → pandas DataFrame → Spark DataFrame → Parquet
```

## Previous Limitation

Spark does not natively support .ods files efficiently in the current local Windows environment.

Because of this, temporary CSV files were previously used as an intermediate layer between ingestion and Spark processing.

## Implemented Improvement

The temporary CSV dependency was removed by converting ODS sheets directly from pandas DataFrames into Spark DataFrames before transformation and parquet generation.

This improvement eliminated the intermediate disk-write/read step previously required for Spark ingestion.

## Objectives

- reduced intermediate disk I/O
- reduced pipeline complexity
- improvded performance
- reduced temporary storage usage
- reduced failure points
- simplified maintenance
- improved maintainability

## Achieved Benefits

- cleaner architecture
- more direct ingestion flow
- fewer temporary artifacts
- simplified execution lifecycle
- improved pipeline readability
- improved engineering maintainability

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

The current local execution environment runs on Windows, where native Spark parquet writing may fail due to Hadoop NativeIO compatibility issues.

Because of this, the pipeline currently uses Spark for data processing and transformation, but persists the final parquet files using pandas/PyArrow.

## Current Implementation

```python
final_pdf = df.toPandas()

final_pdf.to_parquet(
    output_file,
    engine="pyarrow",
    compression="snappy",
    index=False,
)
```

## Reason for Current Approach

This approach was adopted to keep the local pipeline stable and reproducible during development.

Spark is still responsible for the main transformation logic, including:

* ODS ingestion into Spark DataFrames
* column normalization
* wide-to-long transformation
* validation
* metadata enrichment

Pandas is used only as the local persistence layer for parquet writing.

## Future Improvement

Replace pandas/PyArrow parquet persistence with native distributed Spark parquet writing.

## Proposed Future Implementation

```python
df.write \
    .mode("overwrite") \
    .parquet(output_path)
```

## Recommended Environments

* Docker
* Linux
* WSL
* Databricks
* cloud Spark runtimes

## Expected Benefits

* distributed parquet writing
* lower driver memory usage
* better scalability
* elimination of `.toPandas()`
* improved production readiness


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

## Status

🔄 Partially implemented (dbt schema tests on SMP models; PySpark/pytest suite still open)

## Implemented (dbt — SMP baseline)

- 26 data tests on staging and marts (`not_null`, `accepted_values`, `dbt_utils.unique_combination_of_columns`)
- Validated via `dbt test` / `dbt build --select staging.anatel+`
- Tests live in `dbt/models/**/schema.yml`

## Future Improvement

Extend automated validation beyond the current dbt baseline and add Python transformation tests.

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

## Status

🔄 Partially implemented (GOLD layer started via dbt marts in DuckDB)

## Current Architecture

```text
RAW
 └── ODS source files

SILVER
 └── normalization
 └── standardization
 └── wide → long transformation
 └── metadata enrichment
 └── S3 Parquet (anatel-lake / silver / anatel_long)

GOLD (dbt — SMP baseline)
 └── staging: stg_anatel_ida_smp (view)
 └── marts: mart_anatel_smp_summary, mart_anatel_smp_kpis (tables in DuckDB)
```

## Target Architecture

```text
RAW → SILVER → GOLD (dbt marts per domain/model)
```

## Possible GOLD Outputs (remaining / expansion)

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

## Status

🔄 Partially implemented (dbt schema tests + PySpark `validation.py` on silver; no Great Expectations yet)

## Implemented (dbt)

- Uniqueness on business keys (staging and marts)
- `not_null` on critical columns
- `accepted_values` for regulatory model (`SMP`)
- Source contract documented in `sources.yml`

## Future Improvement

Broaden data quality across all models (SCM, STFC, TV) and add cross-layer checks.

## Suggested Validations (remaining)

- duplicated rows (beyond current dbt keys)
- invalid dates (source-level freshness)
- schema inconsistencies across ODS versions
- unexpected numeric ranges
- reconciliation silver ↔ marts

## Possible Tools

- Great Expectations (lake/silver contracts)
- **dbt tests** — extend current baseline
- custom PySpark validations — already used in silver pipeline

## Objectives

- improve data reliability
- reduce analytical inconsistencies
- improve governance
- increase trust in datasets

---

# 9. Migration to Analytics Engineering Layer

## Status

✅ Baseline implemented (SMP scope)

## Implemented Architecture

```text
RAW
 └── ODS source ingestion

SILVER
 └── PySpark normalization / wide → long
 └── Parquet on S3 (anatel-lake)

DBT (SMP)
 ├── sources.yml     → anatel.smp_long (S3 Parquet)
 ├── staging/anatel/ → stg_anatel_ida_smp
 └── marts/          → mart_anatel_smp_summary, mart_anatel_smp_kpis
```

## Validation baseline

| Item | Result |
|------|--------|
| Models | 3 |
| Sources | 1 (`anatel.smp_long`) |
| Data tests | 26 |
| `dbt build --select staging.anatel+` | Successful |
| Documentation | `docs/dbt/` |

## Achieved objectives

- modular SQL transformations (`ref`, `source`)
- lineage and `dbt docs generate`
- schema tests on staging and marts
- documented sources and columns
- reproducible workflow (`deps`, `parse`, `compile`, `debug`, `run`, `test`, `build`)

## Next evolution (still open)

- **Intermediate models** between staging and marts (if logic grows)
- **Additional domains:** SCM, STFC, TV (mirror `staging/anatel/` pattern)
- **dbt exposures** for BI/consumers
- **`dbt source freshness`** automated in CI
- **CI pipeline** running `dbt build` on merge requests
- **Incremental models** where applicable

## Expected Benefits (ongoing)

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

## Status

🔄 Partially implemented (LocalStack S3 + dbt external sources; not production cloud)

## Current local lake pattern

- Bucket `anatel-lake`, prefix `silver/anatel_long/`
- DuckDB `httpfs` + dbt `sources.yml` `external_location`
- Profile `anatel_dbt` in `~/.dbt/profiles.yml`

## Future Possibilities

Production or shared cloud-native architecture.

## Possible Stack

- S3 / ADLS / GCS (beyond LocalStack)
- Spark cluster
- Delta Lake
- dbt (extend current project)
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

---

# 16. dbt Governance — Next Improvements

## Status

Baseline complete for SMP; items below are the recommended next increment.

## Suggested improvements

| Priority | Item | Rationale |
|----------|------|-----------|
| High | `dbt source freshness` in CI | Detect stale S3 silver data |
| High | GitHub Actions / CI `dbt build` | Prevent regressions on PRs |
| Medium | **Exposures** for marts | Document downstream dashboards/APIs |
| Medium | Replicate pattern for SCM, STFC, TV | Full regulatory coverage |
| Done | Pin `dbt-core` / `dbt-duckdb` / `duckdb` in `requirements.txt` | Implemented in `requirements.txt` |
| Low | Intermediate models | Split complex mart logic |
| Low | Generic tests in `dbt/tests/` | SQL tests not tied to one column |

## Observability tie-in

- Stop versioning `logs/query_log.sql` (gitignored); optional structured run logs aligned with section 10

## Documentation

Keep `docs/dbt/` in sync when adding models, sources, or changing the validated workflow.

---

# 17. GitHub Repository and DevOps Hygiene

## Status

Not started — tracked as repository ergonomics and collaboration improvements (complements §7 orchestration and §16 dbt CI).

## Context

Core contributor-facing docs already exist:

- `README.MD` — overview and quick start
- `CONTRIBUTING.md` — workflow, PR validation, repository hygiene
- `LICENSE` — PCML terms
- `docs/dbt/` — analytics layer documentation
- `docs/dbt/profiles.yml.example` — local dbt profile template (not committed under `~/.dbt/`)

The items below close gaps for **standard GitHub practice**, **repeatable local S3**, and **automated dbt validation** on pull requests.

## Suggested improvements

| Priority | Item | Rationale |
|----------|------|-----------|
| High | **CI (GitHub Actions):** `dbt deps`, `dbt parse`, `dbt build --select staging.anatel+` | Prevent regressions on PRs; aligns with §16 dbt CI row |
| Medium | **`.github/pull_request_template.md`** | Standardize PR descriptions (Summary / Motivation / Impact / Validation — mirror `CONTRIBUTING.md`) |
| Medium | **`docker-compose` for LocalStack** | Reproducible S3 (`anatel-lake`) for staging sources and `upload_parquet_to_s3` without manual setup |
| Low | **`CODE_OF_CONDUCT.md`** | Recommended if the repository becomes public or receives external contributors |
| Low | **`SECURITY.md`** | Document how to report security issues responsibly |
| Low | **Rename `README.MD` → `README.md`** | GitHub convention; current name works on Windows but is non-standard on the platform |

## CI workflow sketch (future)

```yaml
# Illustrative — not implemented yet
# triggers: pull_request, push to main
# steps: checkout → setup Python 3.11 → pip install -r requirements.txt
#        → copy profiles.yml.example with CI-safe paths (or mock S3)
#        → dbt deps → dbt parse → dbt build --select staging.anatel+
```

**Note:** `dbt build` in CI requires a strategy for the S3 source (LocalStack service container, fixture Parquet, or scoped `dbt parse` only until lake is available in the runner).

## LocalStack compose sketch (future)

```text
services:
  localstack:
    image: localstack/localstack
    ports:
      - "4566:4566"
    environment:
      - SERVICES=s3
# post-up: create bucket anatel-lake, upload silver parquet
```

Document startup in `README.MD` and `docs/dbt/dbt_execution.md` once added.

## Objectives

- Lower onboarding friction for new contributors
- Enforce the validated dbt workflow on every merge request
- Align repository layout with common open-source / internal GitHub expectations

## Expected benefits

- Fewer “works on my machine” failures for dbt and S3
- PRs with consistent validation evidence
- Clear path from local development → CI → merge
```