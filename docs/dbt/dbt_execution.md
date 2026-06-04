# Execução do projeto dbt — Anatel

Guia reproduzível para rodar o projeto de Analytics Engineering do PDI com DuckDB e fontes S3 (LocalStack).

## Pré-requisitos

- Python 3.11 com dependências instaladas (`pip install -r requirements.txt`)
- `dbt-core` e `dbt-duckdb` no ambiente virtual
- Perfil `anatel_dbt` configurado em `~/.dbt/profiles.yml` apontando para `data/duckdb/anatel.duckdb`
- LocalStack/S3 com bucket `anatel-lake` e parquet em `silver/anatel_long/` (quando usar fontes externas)
- Extensões DuckDB `httpfs` e `parquet` habilitadas no perfil para leitura S3

Copie o template versionado no repositório:

```text
docs/dbt/profiles.yml.example  →  %USERPROFILE%\.dbt\profiles.yml
```

(Não commite o arquivo pessoal em `~/.dbt/`.)

Todos os comandos abaixo devem ser executados na **raiz do repositório** (`PDI/`).

---

## 1. Instalar dependências dbt (`dbt deps`)

Baixa pacotes declarados em `packages.yml` (ex.: `dbt_utils`) para `dbt_packages/`.

```bash
dbt deps
```

---

## 2. Validar conexão e projeto (`dbt debug`)

Confirma perfil, credenciais DuckDB/S3 e estrutura do projeto.

```bash
dbt debug
```

---

## 3. Executar modelos (`dbt run`)

Materializa staging (views) e marts (tables) conforme o DAG.

```bash
dbt run
```

Executar apenas uma camada ou modelo:

```bash
dbt run --select staging.anatel
dbt run --select mart_anatel_smp_summary mart_anatel_smp_kpis
```

---

## 4. Executar testes (`dbt test`)

Roda testes de schema e genéricos (`not_null`, `accepted_values`, `unique_combination_of_columns`, etc.).

```bash
dbt test
```

Testes por camada:

```bash
dbt test --select staging.anatel
dbt test --select mart_anatel_smp_summary mart_anatel_smp_kpis
```

---

## 5. Gerar documentação (`dbt docs generate`)

Gera artefatos em `target/` com lineage, descrições, tags e meta dos modelos/sources.

```bash
dbt docs generate
```

Visualizar no navegador:

```bash
dbt docs serve --port 8001
```

---

## Fluxo recomendado (ordem)

```bash
dbt deps
dbt debug
dbt run
dbt test
dbt docs generate
```

---

## Estrutura relevante

```text
dbt/models/
├── staging/anatel/
│   ├── sources.yml          # Fonte S3/DuckDB (smp_long)
│   ├── schema.yml           # Testes e documentação staging
│   └── stg_anatel_ida_smp.sql
└── marts/
    ├── schema.yml           # Testes e documentação marts
    ├── mart_anatel_smp_summary.sql
    └── mart_anatel_smp_kpis.sql

packages.yml                 # dbt-labs/dbt_utils
dbt_project.yml              # Configuração do projeto
```

---

## Consultar dados no DuckDB (após `dbt run`)

SQL **não roda direto no PowerShell**. Use uma das opções abaixo.

### Opção A — Script Python (recomendado)

```bash
python notebooks/view_dbt_marts_data.py
```

### Opção B — CLI DuckDB

```bash
duckdb data/duckdb/anatel.duckdb -c "SELECT COUNT(*) FROM main.stg_anatel_ida_smp;"
```

### Opção C — Python one-liner

```bash
python -c "import duckdb; from src.utils.paths import DUCKDB_FILE; c=duckdb.connect(str(DUCKDB_FILE)); print(c.execute('SELECT COUNT(*) FROM main.mart_anatel_smp_kpis').fetchone())"
```

---

## Referências

- [dbt sources](https://docs.getdbt.com/docs/build/sources)
- [dbt data tests](https://docs.getdbt.com/docs/build/data-tests)
- [dbt packages](https://docs.getdbt.com/docs/build/packages)
- [dbt-duckdb external sources](https://docs.getdbt.com/reference/resource-configs/duckdb-configs)
