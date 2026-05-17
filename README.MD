# PDI — Data Engineering Growth (Cycle until 2026-06-30)

## Objective

Strengthen modern Data Engineering skills by building an analytical pipeline
using public data from Anatel. Apply layered architecture, Analytics
Engineering practices, automation, and DataOps to increase technical maturity
and consolidate a stronger technical profile inside the organization.
---

## Etapas do Projeto

### Stage 1 — Project Setup

Description

Structure a data project organized in layers (`raw`, `staging`, `marts`) and
build an initial ingestion pipeline in Python for storage and data preparation.

Actions

- Create initial repository structure
- Organize the pipeline into layers
- Implement ingestion for `.ods` files
- Build the initial Python ingestion pipeline

Expected outcome

- Organized project structure
- Running RAW ingestion pipeline
- Reusable project scaffolding

### Stage 2 — Analytical Transformations & Analytics Engineering

Description

Apply Analytics Engineering principles using `dbt` to organize transformations,
standardize datasets, and separate ingestion from analytical consumption.

Actions

- Set up a `dbt` project
- Create `staging` and `marts` models
- Convert data from wide → long where applicable
- Standardize dates, column names and types
- Add basic tests

Expected outcome

- Decoupled, organized transformations
- Analytics-ready datasets
- Reusable dbt models

### Stage 3 — DataOps & Reproducibility

Description

Introduce initial DataOps practices to increase reliability, technical
organization, and reproducibility of the pipeline.

Actions

- Add simple logging
- Implement basic error handling and retries
- Maintain versioning with Git
- Document pipeline execution
- Introduce Docker concepts for reproducible environments

Expected outcome

- Reproducible pipeline runs
- Documented technical process
- Improved understanding of reproducible environments

### Stage 4 — Architecture Consolidation

Description

Refine the pipeline architecture and reinforce best practices for separating
ingestion, transformation, and consumption stages.

Actions

- Refine pipeline organization and orchestration
- Improve separation of concerns between stages
- Expand technical documentation
- Compare implementation choices between Python scripts and `dbt`

Expected outcome

- Clearer, more maintainable architecture
- Improved reasoning about technical trade-offs
- Reusable, production-ready structure

### Stage 5 — Complementary DevOps/DataOps Upskilling

Description

Relate DevOps/DataOps concepts studied to practical applications within the
project to strengthen operational understanding.

Actions

- Continue training in DevOps/DataOps
- Map learned concepts to this project
- Consolidate fundamentals in automation, observability, and reproducibility

Expected outcome

- Broadened operational perspective on data projects
- Better grasp of modern engineering practices
- Stronger ability to design sustainable pipelines
---


## Continuous Conceptual Foundation

Description

Consolidate theoretical foundations of Data Engineering and map studied
concepts to practical decisions made during the project.

Actions

- Progressive reading of "Fundamentals of Data Engineering"
- Map theoretical concepts to project decisions

Expected outcome

- Stronger understanding of applied concepts
- Better alignment between theory and practice

---

## Final Expected Results

- Functional analytical pipeline
- Layered architecture (raw / staging / marts)
- Hands-on Docker experience
- Improved DataOps practices
- Increased maturity in Data Engineering
- Stronger internal technical positioning

---

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Example: run the scraper (RAW ingestion):

```bash
python src/data/refactor_scraping_class.py
```

3. Suggested `dbt` and Docker steps are outlined in the `docs/` folder.

---

## Supporting files

- `requirements.txt`: project dependencies
- `LICENSE`: personal copy-and-modify license

---

If you want, I can also add a `Contributing` section and an initial `docs/`
folder with `dbt` and Docker setup examples.

