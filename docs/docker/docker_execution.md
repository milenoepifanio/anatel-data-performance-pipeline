# Execução Docker — PDI

Este documento descreve como executar e testar o projeto PDI usando Docker e Docker Compose.

## Pré-requisitos

- Docker instalado
- Docker Compose instalado ou Docker Desktop com compose integrado
- estar na raiz do repositório `PDI/`

## Passo 1 — Build da imagem

```bash
docker compose build app
```

Esse comando monta a imagem do serviço `app` a partir do `Dockerfile` e instala as dependências do `requirements.txt`.

## Passo 2 — Iniciar serviços

```bash
docker compose up -d
```

Isso inicia os serviços:

- `app` → contêiner da aplicação Python
- `localstack` → serviço S3 local emulado

## Passo 3 — Verificar status

```bash
docker compose ps
```

## Passo 4 — Acessar o container `app`

```bash
docker compose exec app bash
```

Dentro do shell do contêiner, você pode executar os comandos do projeto usando o código montado em `/app`.

## Passo 5 — Rodar transformação Python

Dentro do contêiner `app`:

```bash
python src/main.py
```

ou

```bash
python src/processing/silver_long_transformer.py
```

## Passo 6 — Executar dbt

Dentro do contêiner `app`, execute os comandos dbt a partir da raiz do repositório:

```bash
dbt deps

dbt debug

dbt build --select staging.anatel+
```

> Observação: o perfil dbt ainda precisa ser configurado localmente em `~/.dbt/profiles.yml` ou no contêiner com o mesmo layout do host.

## Passo 7 — Parar os serviços

```bash
docker compose down
```

## Ajustes rápidos

- Rebuild após alterações no `Dockerfile`: `docker compose up -d --build`
- Recriar o volume LocalStack caso haja problema: `docker compose down -v` seguido de `docker compose up -d`

## Boas práticas

- mantenha o diretório `data/` montado para preservar os artefatos gerados
- use `docker compose exec app bash` para testar comandos interativos
- verifique se o LocalStack está disponível em `http://localhost:4566`
