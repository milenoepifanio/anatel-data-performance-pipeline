# Guia conceitual dbt — Projeto Anatel (PDI)

Este documento explica **como as tabelas analíticas são criadas** neste repositório, para quem ainda não conhece dbt. Para comandos de execução passo a passo, veja [dbt_execution.md](./dbt_execution.md).

---

## 1. O que é o dbt neste projeto?

**dbt** (data build tool) é uma ferramenta de *Analytics Engineering*: você escreve SQL versionado, define dependências entre modelos, documenta colunas e roda testes de qualidade. O dbt **não extrai** dados da Anatel; ele **transforma** dados que já foram processados pelo pipeline Python/PySpark e gravados em Parquet no S3.

Neste projeto:

| Papel | Tecnologia |
|--------|------------|
| Ingestão / transformação pesada | Python, PySpark, Parquet |
| Modelagem analítica | dbt + DuckDB |
| Armazenamento das tabelas finais | `data/duckdb/anatel.duckdb` |
| Leitura da fonte bruta (silver) | S3 (`anatel-lake`) via DuckDB/httpfs |

---

## 2. Conceitos essenciais

### Source (fonte)

Arquivo: `dbt/models/staging/anatel/sources.yml`

Uma **source** declara de onde vêm os dados **antes** de existir qualquer modelo dbt. Não é uma tabela criada pelo dbt; é um **contrato documentado** apontando para arquivos externos (aqui, Parquet no S3).

- **Nome lógico:** `anatel` (grupo) → `smp_long` (tabela)
- **Uso no SQL:** `{{ source('anatel', 'smp_long') }}`
- **No DuckDB:** o adapter resolve isso para `read_parquet('s3://anatel-lake/silver/anatel_long/SMP*.parquet')`

**Por que usar source em vez de `read_parquet` direto no `.sql`?**

- Linhagem visível no `dbt docs`
- Documentação centralizada das colunas de origem
- Base para testes e freshness no futuro
- Padrão recomendado pela comunidade dbt

### Model (modelo)

Arquivos `.sql` em `dbt/models/`. Cada modelo vira uma **view** ou **table** no DuckDB quando você roda `dbt run`.

- **Staging:** limpeza, tipos, padronização (`stg_anatel_ida_smp`)
- **Marts:** agregações de negócio (`mart_anatel_smp_summary`, `mart_anatel_smp_kpis`)

**Referência entre modelos:** `{{ ref('stg_anatel_ida_smp') }}` — o dbt garante ordem de execução (DAG).

### Schema (no sentido dbt)

Palavra ambígua; neste projeto aparece em **dois sentidos**:

| Contexto | Significado |
|----------|-------------|
| **Arquivo `schema.yml`** | YAML com descrições, testes e metadados dos **modelos** (não cria tabela sozinho) |
| **Schema do banco (`main`)** | “Pasta” lógica no DuckDB onde as tabelas ficam (`main.mart_anatel_smp_kpis`) |

Os arquivos `schema.yml` em `staging/anatel/` e `marts/` definem:

- `description` do modelo e das colunas
- `tests` (`not_null`, `accepted_values`, unicidade via `dbt_utils`)
- `config.meta` (owner, purpose) e `tags`

### Target

No dbt, **target** é o **ambiente de execução** definido no perfil (`~/.dbt/profiles.yml`), por exemplo `dev`.

- Controla **qual banco** usar (`data/duckdb/anatel.duckdb`)
- Credenciais S3 para o DuckDB ler o bucket
- Você troca de target com `dbt run --target prod` (quando existir outro output no perfil)

**Não confundir com** a pasta `target/` do projeto: ali o dbt grava artefatos de compilação (`compiled/`, `manifest.json`, docs).

### Profile e `dbt_project.yml`

| Arquivo | Onde | Função |
|---------|------|--------|
| `profiles.yml` | `~/.dbt/` (máquina do dev) | Conexão: DuckDB, path, S3, target `dev` |
| `dbt_project.yml` | Raiz do repo `PDI/` | Nome do projeto, pastas de modelos, materialização padrão por camada |

O `dbt_project.yml` **não** guarda senhas; só configuração do projeto versionada no Git.

### Materialização

Define **o que o DuckDB persiste** após `dbt run`:

| Valor | Neste projeto | Comportamento |
|--------|----------------|---------------|
| `view` | Staging | Objeto leve; ao consultar, relê a source (S3) |
| `table` | Marts | Dados gravados no `.duckdb`; consulta offline |

Configurado em `dbt_project.yml` (padrão por pasta) e pode ser sobrescrito no topo de cada `.sql` com `{{ config(materialized='table') }}`.

---

## 3. Fluxo de criação das tabelas (DAG)

Ordem real de dependência:

```text
[S3 Parquet SMP*]
        │
        ▼  source: anatel.smp_long
┌───────────────────────────┐
│  stg_anatel_ida_smp       │  VIEW — staging
│  (trim, cast, rename)     │
└───────────┬───────────────┘
            │ ref()
     ┌──────┴──────┐
     ▼             ▼
┌─────────────┐ ┌──────────────────┐
│ mart_       │ │ mart_            │
│ anatel_smp_ │ │ anatel_smp_kpis  │  TABLE — marts
│ summary     │ │                  │
└─────────────┘ └──────────────────┘
```

### Passo a passo (o que acontece em `dbt run`)

1. **Source** — dbt registra a fonte; no compile, vira SQL com `read_parquet(...)`.
2. **Staging** — cria/recria a view `main.stg_anatel_ida_smp` lendo a source.
3. **Marts** — leem a view via `ref()`, agregam e gravam tabelas `main.mart_anatel_smp_*`.

Com `dbt build --select staging.anatel+`, o dbt ainda roda os **testes** após cada modelo (run + test na ordem do DAG).

---

## 4. Estrutura de arquivos do projeto

```text
PDI/
├── dbt_project.yml          # Configuração global do projeto dbt
├── packages.yml             # Dependências reutilizáveis (dbt_utils)
├── dbt/
│   └── models/
│       ├── staging/anatel/
│       │   ├── sources.yml       # Declara fonte S3
│       │   ├── schema.yml        # Docs + testes do staging
│       │   └── stg_anatel_ida_smp.sql
│       └── marts/
│           ├── schema.yml
│           ├── mart_anatel_smp_summary.sql
│           └── mart_anatel_smp_kpis.sql
├── data/duckdb/
│   └── anatel.duckdb        # Banco gerado/atualizado pelo dbt run
└── docs/dbt/
    ├── guia_conceitual_dbt.md   # Este arquivo
    └── dbt_execution.md         # Comandos operacionais
```

Pastas previstas mas ainda vazias no repo: `dbt/seeds/`, `dbt/macros/`, `dbt/tests/`, `dbt/snapshots/`.

---

## 5. Arquivos explicados um a um

### `dbt_project.yml` (raiz)

```yaml
name: anatel_dbt
profile: anatel_dbt          # Nome do bloco em ~/.dbt/profiles.yml

model-paths: ["dbt/models"]

models:
  anatel_dbt:                # Deve coincidir com `name` acima
    staging:
      +materialized: view    # Tudo em staging vira VIEW
      anatel:
        +tags: ["staging", "anatel"]
    marts:
      +materialized: table  # Tudo em marts vira TABLE
      +tags: ["mart", "anatel"]
```

- **`name` / `profile`:** ligam o projeto ao perfil de conexão.
- **`model-paths`:** onde o dbt procura `.sql` e `.yml`.
- **`models.anatel_dbt.staging`:** regras em cascata para subpastas (convenção de pastas = namespace do modelo).

### `packages.yml`

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: "1.3.0"
```

Instala macros e testes prontos (ex.: `unique_combination_of_columns`). Após alterar: `dbt deps`.

### `sources.yml`

Declara a fonte `anatel.smp_long` com:

- Descrições e `meta` (bucket, prefix, owner)
- `external_location` para o adapter DuckDB
- Lista de colunas documentadas

Trecho central:

```yaml
tables:
  - name: smp_long
    config:
      meta:
        external_location: "read_parquet('s3://anatel-lake/silver/anatel_long/SMP*.parquet')"
```

### `stg_anatel_ida_smp.sql`

```sql
from {{ source('anatel', 'smp_long') }}   -- fonte documentada

-- depois: trim, upper(modelo), cast de datas e números
```

Saída: view com colunas padronizadas (`ingestion_timestamp`, `record_hash`, etc.).

### `mart_anatel_smp_summary.sql`

```sql
from {{ ref('stg_anatel_ida_smp') }}

-- GROUP BY grupo_economico, modelo, variavel
-- métricas: min/max competência, sum/avg/min/max valor
```

Saída: tabela com **uma linha por** grupo + modelo + variável.

### `mart_anatel_smp_kpis.sql`

```sql
from {{ ref('stg_anatel_ida_smp') }}

-- GROUP BY competencia, grupo_economico
-- KPIs: contagens, soma/média de valor, última ingestão
```

Saída: tabela com **uma linha por** competência + grupo econômico.

### `schema.yml` (staging e marts)

Exemplo de teste com pacote:

```yaml
tests:
  - dbt_utils.unique_combination_of_columns:
      arguments:
        combination_of_columns:
          - competencia
          - grupo_economico
```

Isso vira SQL de validação executado em `dbt test` — não altera dados, só verifica regras.

---

## 6. Requisitos para rodar

### Software

| Requisito | Versão usada no projeto | Observação |
|-----------|-------------------------|------------|
| Python | 3.11 | Ambiente `env311` |
| dbt-core | 1.12.x (exemplo) | CLI `dbt` |
| dbt-duckdb | 1.10.x | Adapter para DuckDB + S3 |
| duckdb | compatível com o adapter | Leitura local + httpfs |
| Git | qualquer recente | `dbt deps` clona pacotes |

Instalação típica (além do `requirements.txt` do pipeline Python):

```bash
pip install dbt-core dbt-duckdb duckdb
```

> O `requirements.txt` atual foca PySpark/ingestão; as libs dbt costumam ser instaladas no mesmo venv quando você trabalha na camada analítica.

### Infraestrutura de dados

| Requisito | Para quê |
|-----------|----------|
| LocalStack ou S3 com bucket `anatel-lake` | Source `smp_long` no `dbt run` / view staging |
| Parquet em `silver/anatel_long/SMP*.parquet` | Conteúdo lido pela source |
| Perfil `anatel_dbt` em `~/.dbt/profiles.yml` | Conexão DuckDB + credenciais S3 |
| Arquivo `data/duckdb/anatel.duckdb` | Criado/atualizado no primeiro `dbt run` bem-sucedido |

### Perfil mínimo (`profiles.yml`)

```yaml
anatel_dbt:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: data/duckdb/anatel.duckdb
      extensions:
        - httpfs
      settings:
        s3_region: us-east-1
        s3_endpoint: localhost:4566
        s3_access_key_id: test
        s3_secret_access_key: test
        s3_use_ssl: false
        s3_url_style: path
```

O `path` é relativo à pasta onde você executa o dbt (raiz `PDI/`).

---

## 7. Do código SQL ao objeto no DuckDB

| Comando | O que faz |
|---------|-----------|
| `dbt compile` | Gera SQL final em `target/compiled/` (útil para debug) |
| `dbt run` | Executa SQL no DuckDB e cria view/tables |
| `dbt test` | Roda testes definidos em `schema.yml` |
| `dbt build` | `run` + `test` na ordem do DAG |
| `dbt docs generate` | Site de documentação + lineage |

**Consultar resultados** (SQL não roda no PowerShell):

```bash
python notebooks/view_dbt_marts_data.py
```

Marts são tabelas físicas; a view de staging só consulta com S3 ativo.

---

## 8. Glossário rápido

| Termo | Significado neste repo |
|--------|-------------------------|
| **DAG** | Grafo de dependências: source → staging → marts |
| **ref()** | “Use o modelo X já definido no projeto” |
| **source()** | “Use a fonte externa declarada em sources.yml” |
| **macro** | Função Jinja/SQL reutilizável (ex.: pacote `dbt_utils`) |
| **seed** | CSV estático versionado (não usado ainda) |
| **snapshot** | Histórico de mudanças SCD (não usado ainda) |
| **manifest** | JSON em `target/` com metadados após cada run |
| **linhagem** | Visualização de quem depende de quem no `dbt docs` |

---

## 9. Perguntas frequentes

**Por que a view staging falha no script Python mas os marts funcionam?**  
A view relê o S3 a cada query. Os marts são tabelas materializadas no último `dbt run` (dados já gravados no `.duckdb`).

**O que valida `dbt test`?**  
Regras do `schema.yml` (nulos, valores permitidos, chaves únicas). Não substitui validação PySpark na camada silver.

**Preciso rodar PySpark antes do dbt?**  
Sim, para popular o S3/local com Parquet long-format; o dbt assume que essa camada já existe.

**Onde aprender mais?**  
- [Documentação dbt](https://docs.getdbt.com/)  
- [dbt-duckdb — external sources](https://docs.getdbt.com/reference/resource-configs/duckdb-configs)  
- [dbt_execution.md](./dbt_execution.md) neste repositório  

---

## 10. Resumo em uma frase

O pipeline Python entrega **Parquet no S3**; o dbt **declara essa entrada como source**, **limpa na staging (view)**, **agrega nos marts (tables)** no DuckDB, e o **schema.yml** documenta e testa tudo — com `dbt_project.yml` e `packages.yml` amarrando configuração e dependências do projeto.
