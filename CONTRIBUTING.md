# Contributing Guide

## Purpose

This document defines the contribution workflow for this repository.

For architecture decisions, engineering standards, and project conventions, refer to:

```text
docs/architecture/project_standards.md
```

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

Example:

```text
Summary
- Added new dbt mart model

Motivation
- Provide analytical KPI aggregation

Impact
- New table available for reporting

Validation
- dbt run
- dbt test
- DuckDB validation
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
```

---

# Documentation

Documentation updates should accompany architectural or structural changes.

Main documentation locations:

```text
README.md
docs/architecture/
```

---

# Questions

When in doubt, prioritize:

* readability
* maintainability
* reproducibility
* simplicity

```
```
