# Documentação de Pipelines — PDI

Documentação dos pipelines de ingestão e transformação de dados implementados no projeto PDI.

| Documento | Conteúdo |
|-----------|----------|
| [raw_wide_ingestion_architecture.md](./raw_wide_ingestion_architecture.md) | Processo de ingestão dos arquivos ODS da Anatel, identificação de cabeçalhos, padronização de schemas, normalização de dados e geração da camada Wide em Parquet |
| [silver_long_transformation_pipeline.md](./silver_long_transformation_pipeline.md) | Transformação da camada Wide para Long utilizando PySpark, incluindo validações, enriquecimento com metadados, controles de qualidade e geração da camada Silver |

**Ordem sugerida:** ler primeiro a documentação de ingestão (`raw_wide_ingestion_architecture.md`) e depois a documentação da transformação Silver (`silver_long_transformation_pipeline.md`).