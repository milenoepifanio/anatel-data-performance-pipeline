# Guia Conceitual Docker — PDI

Este guia explica a arquitetura de containerização do projeto PDI e como os arquivos `Dockerfile` e `docker-compose.yaml` suportam o processamento Python + dbt + LocalStack.

## Por que Docker

O Docker permite:

- isolar dependências do projeto em um ambiente portátil
- evitar conflitos de versões locais (Python, Java, Spark, dbt)
- reproduzir a execução do pipeline em qualquer máquina que tenha Docker
- integrar a aplicação com serviços de apoio como LocalStack para testes de S3

## Arquitetura do container

O projeto usa dois serviços principais:

1. `app`
   - aplicação Python que roda as transformações PySpark e comandos dbt
   - monta o repositório no diretório `/app`
   - expõe variáveis de ambiente necessárias para LocalStack/S3 e Java

2. `localstack`
   - emula o serviço AWS S3 localmente
   - expõe a porta `4566`
   - permite que o pipeline grave e leia dados em um bucket `anatel-lake`

## `Dockerfile`

O `Dockerfile` do projeto define:

- base `python:3.11-slim`
- instalação do OpenJDK 17 para suportar o PySpark local
- cópia do `requirements.txt` e instalação das dependências Python
- cópia do código-fonte para `/app`
- variáveis de ambiente padrão para `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `LOCALSTACK_ENDPOINT_URL`, `BUCKET_NAME` e `S3_PREFIX`

Esse design garante que o contêiner tenha o runtime Python, o Spark compatível com Java e o código do PDI disponíveis para execução.

## `docker-compose.yaml`

O `docker-compose.yaml` define o ambiente de desenvolvimento:

- o serviço `app` depende de `localstack`
- o serviço `app` usa volumes para montar o código e os dados do host
- as variáveis de ambiente do projeto são passadas para o contêiner
- o LocalStack oferece S3 sem precisar de uma conta AWS real

## Como o projeto se beneficia

- `src/main.py` e `src/processing/silver_long_transformer.py` podem rodar dentro do contêiner com dependências instaladas
- `dbt` pode ser executado no mesmo contêiner usando o diretório de trabalho `/app`
- os pipelines que usam `boto3` e LocalStack conseguem ler/escrever no bucket `anatel-lake`
- o código que usa `src/utils/paths.py` agora aceita conexões por variáveis de ambiente, o que melhora a compatibilidade com Docker

## Observações importantes

- essa configuração é pensada para desenvolvimento local e validação de pipeline, não para produção em cluster
- o volume `./data` é montado no contêiner para preservar os artefatos de execução no host
- a execução do serviço `app` em `docker-compose` pode ser ajustada para rodar comandos específicos, em vez de apenas manter o container vivo
