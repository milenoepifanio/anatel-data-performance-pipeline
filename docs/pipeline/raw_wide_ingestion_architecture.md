# Anatel Bronze Wide Ingestion Architecture

## Overview

This document describes the ingestion and standardization process for Anatel ODS files using PySpark.

The current pipeline focuses on converting raw `.ods` files into a standardized **wide parquet** structure. This stage preserves the original wide format of the source files while removing non-tabular headers, cleaning numeric values, standardizing column names and adding lineage metadata.

This implementation is part of the Bronze/Staging layer of the project.

---

# 1. Architecture Overview

## 1.1 Data Flow

```text
RAW ODS files
    ↓
Temporary CSV conversion
    ↓
PySpark wide ingestion
    ↓
Standardized wide parquet output
```

## 1.2 Current Layer Responsibility

```text
data/raw/
    Original ODS files downloaded from Anatel

data/temp/ods_csv/
    Temporary CSV files generated from each ODS sheet

data/staging/wide/ida_anatel/
    Standardized wide parquet output
```

---

# 2. Current Pipeline Scope

The current pipeline processes the following test files:

```text
data/raw/SCM2016.ods
data/raw/SEAC2019.ods
data/raw/SMP2014.ods
data/raw/STFC2017.ods
```

These files were selected as representative samples because each service has specific structural characteristics.

Supported models:

```python
["SCM", "SEAC", "STFC", "SMP"]
```

---

# 3. Why Wide First?

The source files are not clean tabular datasets. They contain:

- Initial descriptive rows
- Specific header positions
- Different sheets depending on the service
- Wide monthly columns
- Notes and non-data rows
- Brazilian numeric format using comma as decimal separator

For this reason, the first objective is to preserve the wide structure and validate that the ingestion process correctly reads and standardizes the files.

The long format transformation will be handled in a later stage.

Recommended flow:

```text
ODS raw
→ Bronze/Staging wide parquet
→ Silver long parquet
→ Analytics/Gold datasets
```

---

# 4. Main Component

Current script:

```text
src/ingestion/anatel_bronze_wide_ingestion.py
```

Main class:

```python
AnatelWidePySparkTransformer
```

## Main Responsibilities

```text
1. Configure local PySpark environment
2. Read ODS files using pandas/odfpy
3. Identify the real header row
4. Remove non-tabular rows
5. Convert ODS sheets to temporary CSV files
6. Read temporary CSV files with PySpark
7. Standardize column names
8. Normalize numeric values
9. Add lineage metadata
10. Save output as parquet
```

---

# 5. Important Technical Decisions

## 5.1 ODS Reading

PySpark does not natively read `.ods` files.

Because of this, the pipeline uses pandas only as an auxiliary conversion layer:

```text
ODS → CSV temporary file
```

After that, the processing is handled by PySpark.

---

## 5.2 Encoding

The CSV intermediate output uses:

```python
encoding="utf-8-sig"
```

This was necessary to preserve Portuguese accents correctly.

---

## 5.3 Numeric Normalization

Before writing the temporary CSV files, numeric columns are normalized from Brazilian format to standard decimal format:

```text
"1.234,56" → "1234.56"
"15,8"     → "15.8"
```

---

## 5.4 Output Format

The final output is saved as parquet using Snappy compression:

```text
data/staging/wide/ida_anatel/
```

At this stage, partitioning was intentionally removed to avoid unnecessary Hadoop/Windows local complexity.

---

# 6. Output Structure

The wide parquet output contains columns similar to:

```text
grupo_economico
variavel
mes_2014_01
mes_2014_02
...
arquivo_origem
modelo
ano_arquivo
_ingestion_timestamp
_processing_date
_record_hash
```

The monthly columns vary depending on the source file and year.

---

# 7. Environment Notes

The local PySpark environment requires explicit configuration for:

```text
JAVA_HOME
SPARK_HOME
PYSPARK_PYTHON
PYSPARK_DRIVER_PYTHON
```

Example:

```python
java_home = r"C:\Program Files\Java\jdk-17"
spark_home = r"C:\Users\Mileno\Downloads\PDI\env\Lib\site-packages\pyspark"
```

This avoids issues with incorrect terminal-level `SPARK_HOME` values.

---

# 8. Dependencies

Required packages:

```text
pyspark
pandas
odfpy
```

Install with:

```bash
python -m pip install pyspark pandas odfpy
```

---

# 9. Current Status

The current version successfully:

- Reads representative `.ods` files
- Converts sheets to temporary CSV
- Preserves UTF-8 accents
- Normalizes decimal commas
- Loads files with PySpark
- Generates wide parquet output

---

# 10. Next Steps

Recommended next steps:

```text
1. Validate the generated wide parquet files
2. Apply the pipeline to all available years and models
3. Create a Silver transformation from wide to long
4. Standardize service/model dimensions
5. Add data quality checks
6. Add logging and execution summaries
7. Revisit partitioning only when the long layer is created
```

---

# 11. Project Structure

```text
project/
│
├── data/
│   ├── raw/
│   │   ├── SCM2016.ods
│   │   ├── SEAC2019.ods
│   │   ├── SMP2014.ods
│   │   └── STFC2017.ods
│   │
│   ├── temp/
│   │   └── ods_csv/
│   │
│   └── staging/
│       └── wide/
│           └── ida_anatel/
│
├── src/
│   └── ingestion/
│       └── anatel_bronze_wide_ingestion.py
│
└── README.md
```

---

# 12. Execution Example

```bash
python src/ingestion/anatel_bronze_wide_ingestion.py
```

---

# 13. Example Output

```python
{
    "status": "success",
    "records": 15420,
    "output_path": "data/staging/wide/ida_anatel",
    "timestamp": "2026-05-23T16:40:00"
}
```

---

# 14. References

- Apache Spark: https://spark.apache.org/
- PySpark Documentation: https://spark.apache.org/docs/latest/api/python/
- Medallion Architecture: https://www.databricks.com/glossary/medallion-architecture

---

**Version**: 1.1  
**Last Updated**: 2026-05-23  
**Status**: Active  
**Script**: `src/ingestion/anatel_bronze_wide_ingestion.py`
**branch**: `feat/raw-wide-transformation`