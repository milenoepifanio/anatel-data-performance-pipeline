# Architecture — PDI

Documentation for the architecture, engineering standards, structural decisions, and technical evolution of the PDI project.

| Document | Content |
|----------|---------|
| [medallion_architecture.md](./medallion_architecture.md) | Overview of the Medallion architecture adopted in the project, including RAW, SILVER, GOLD, Data Lake, and Analytics Engineering layers |
| [project_standards.md](./project_standards.md) | Development conventions, repository organization, coding standards, best practices, and engineering guidelines |
| [technology_stack.md](./technology_stack.md) | Technologies used in the project, the role of each tool, and how they integrate into the architecture |
| [data_flow.md](./data_flow.md) | End-to-end data flow, from Anatel file ingestion to the generation of analytical datasets |
| [vault_of_future_improvements.md](./vault_of_future_improvements.md) | Technical backlog containing future improvements, architectural evolution, optimization opportunities, and roadmap items |

**Objective:** document the project's architectural structure, record adopted patterns, and centralize decisions that guide its technical evolution.

**Suggested order:** start with medallion_architecture.md, then move to data_flow.md and technology_stack.md, consult project_standards.md for conventions, and use vault_of_future_improvements.md as a reference for future evolution.