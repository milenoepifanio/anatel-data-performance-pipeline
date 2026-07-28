# Notebooks — PDI

This directory contains Python-based analytical scripts and exploratory notebooks alternatives used to inspect, validate, and compare pipeline outputs.

## Purpose

The notebooks folder is used for:

- validating transformations and intermediate datasets;
- comparing expected and generated outputs;
- testing integrations with Spark, S3, dbt marts, and DuckDB;
- supporting analysis and debugging during development.

---

## Contents

| File | Purpose |
|------|---------|
| [compare_silver_outputs.py](compare_silver_outputs.py) | Compares generated silver outputs and checks consistency |
| [test_long_silver.py](test_long_silver.py) | Validates long-format silver transformation results |
| [test_read_s3.py](test_read_s3.py) | Tests S3 and DuckDB integration scenarios |
| [test_spark.py](test_spark.py) | Verifies Spark environment and basic execution |
| [view_dbt_marts_data.py](view_dbt_marts_data.py) | Inspects dbt mart data for debugging and analysis |

---

## Notes

These scripts are primarily intended for development, validation, and exploratory analysis rather than production orchestration.
