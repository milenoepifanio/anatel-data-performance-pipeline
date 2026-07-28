# dbt Documentation — PDI

Documentation for the Analytics Engineering layer (Anatel / SMP).

| Document                                           | Content                                                                                                                                           |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| [guia_conceitual_dbt.md](./guia_conceitual_dbt.md) | Concepts such as sources, schema, target, models, table creation flow, project files, and requirements — recommended reading for those new to dbt |
| [dbt_execution.md](./dbt_execution.md)             | Operational commands such as deps, run, test, and docs, along with execution prerequisites                                                        |
| [profiles.yml.example](./profiles.yml.example)     | Example DuckDB/S3 profile template to copy to ~/.dbt/profiles.yml                                                                                 |

**Suggested order:** conceptual → execution → run dbt build --select staging.anatel+ from the repository root.
