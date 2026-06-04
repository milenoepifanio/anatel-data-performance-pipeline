# Documentação dbt — PDI

Documentação da camada de Analytics Engineering (Anatel / SMP).

| Documento | Conteúdo |
|-----------|----------|
| [guia_conceitual_dbt.md](./guia_conceitual_dbt.md) | Conceitos (source, schema, target, modelos), fluxo de criação das tabelas, arquivos do projeto e requisitos — **leitura para quem não conhece dbt** |
| [dbt_execution.md](./dbt_execution.md) | Comandos operacionais (`deps`, `run`, `test`, `docs`) e pré-requisitos de execução |

**Ordem sugerida:** conceitual → execução → rodar `dbt build --select staging.anatel+` na raiz do repositório.
