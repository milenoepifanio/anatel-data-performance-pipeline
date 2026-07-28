# Data — PDI

This directory contains the project's data assets and intermediate outputs generated during the pipeline execution.

## Purpose

The data folder is organized to support the layered architecture of the pipeline, including:

- raw input files downloaded from the source portal;
- staging datasets produced after transformation;
- analytical marts used for downstream consumption;
- local DuckDB storage for analytical querying;
- temporary working files used during processing.

---

## Structure

| Area                | Description                                                       |
| ------------------- | ----------------------------------------------------------------- |
| [raw](raw/)         | Raw source files ingested into the pipeline                       |
| [staging](staging/) | Intermediate datasets in wide and long formats                    |
| [marts](marts/)     | Final analytical data models produced for consumption             |
| [duckdb](duckdb/)   | Local DuckDB database used for analytics and validation           |
| [temp](temp/)       | Temporary files generated during preprocessing and transformation |

---

## Notes

This directory is a working data repository for the project and may contain generated artifacts as well as source inputs.
