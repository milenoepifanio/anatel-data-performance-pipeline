# Pipeline Documentation — PDI

Documentation for the data ingestion and transformation pipelines implemented in the PDI project.

| Document                                                                           | Content                                                                                                                              |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| [raw_wide_ingestion_architecture.md](./raw_wide_ingestion_architecture.md)         | Anatel ODS ingestion process, header identification, schema standardization, data normalization, and Wide-layer Parquet generation   |
| [silver_long_transformation_pipeline.md](./silver_long_transformation_pipeline.md) | Wide-to-Long transformation using PySpark, including validations, metadata enrichment, quality controls, and Silver-layer generation |

**Suggested order:** read the ingestion documentation first and then the Silver transformation documentation.
