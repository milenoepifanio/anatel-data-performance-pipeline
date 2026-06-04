# Contributing Guide

## Purpose

This document defines the contribution workflow for this repository.

For architecture decisions, engineering standards, and project conventions, refer to:

```text
docs/architecture/project_standards.md
docs/dbt/
```

---

# Prerequisites (first-time setup)

1. **Python 3.11** and `pip install -r requirements.txt`
2. **dbt profile:** copy `docs/dbt/profiles.yml.example` to `~/.dbt/profiles.yml` (never commit personal profiles)
3. **Spark/Java/Hadoop** paths as documented in `docs/architecture/project_standards.md` (Windows local setup)
4. **S3 / LocalStack** when running dbt staging sources or uploading silver Parquet (`anatel-lake` bucket)
5. **Git** for `dbt deps` (package installation)

---

# Development Workflow

## Create a Branch

Use conventional branch prefixes:

```text
feat/
fix/
refactor/
docs/
chore/
```

Examples:

```text
feat/dbt-governance-and-testing
feat/dbt-mart-models
fix/scraper-download-logic
refactor/notebooks-py-conversion
docs/update-readme
chore/dependency-update
```

---

# Commit Standards

Use clear and descriptive commit messages.

Examples:

```text
feat: add SMP mart models

fix: correct scraper target filtering

refactor: convert notebooks to python scripts

docs: update project documentation

chore: update repository configuration
```

---

# Pull Request Standards

Every Merge Request should contain:

## Summary

Describe what was changed.

## Motivation

Explain why the change was necessary.

## Impact

Describe expected impact on the project.

## Validation

Explain how the change was tested.

Example (dbt governance / quality baseline):

```text
Summary
- dbt governance baseline for Anatel SMP (sources, schema tests, docs)

Motivation
- Lineage, documented sources, and automated quality checks before marts

Impact
- 3 models, 1 source, 26 schema tests; reproducible dbt workflow

Validation
- dbt deps && dbt parse && dbt compile --select staging.anatel+
- dbt debug
- dbt build --select staging.anatel+  (PASS: 29 nodes)
- dbt docs generate
- python notebooks/view_dbt_marts_data.py
```

---

# Development Rules

Before opening a Merge Request:

* Ensure code executes successfully.
* Remove obsolete code.
* Remove debugging artifacts.
* Update documentation when necessary.
* Validate imports and paths.
* Confirm no generated artifacts are being committed.

---

# Repository Hygiene

Never commit:

```text
env/
env311/
__pycache__/
.ipynb_checkpoints/
data/temp/
*.parquet
*.duckdb
logs/
.env
target/
dbt_packages/
~/.dbt/profiles.yml   # local credentials — use profiles.yml.example only
```

---

# Documentation

Documentation updates should accompany architectural or structural changes.

Main documentation locations:

```text
README.md
docs/architecture/
docs/dbt/                    # dbt conceptual guide + execution runbook
```

When changing dbt models, sources, or tests, update `docs/dbt/` if behavior or workflow changes.

---

# Questions

When in doubt, prioritize:

* readability
* maintainability
* reproducibility
* simplicity
