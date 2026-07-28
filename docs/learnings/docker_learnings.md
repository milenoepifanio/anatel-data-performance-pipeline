# Docker

> Documentação de estudos sobre Docker, seus principais conceitos, comandos e boas práticas, com foco em desenvolvimento e Engenharia de Dados.

---

# Sumário

- [1. Introdução](#1-introdução)
- [2. O que é Docker?](#2-o-que-é-docker)
- [3. Virtualização vs Containers](#3-virtualização-vs-containers)
- [4. Arquitetura do Docker](#4-arquitetura-do-docker)
- [5. Instalação](#5-instalação)
- [6. Conceitos Fundamentais](#6-conceitos-fundamentais)
- [7. Comandos Essenciais](#7-comandos-essenciais)
- [8. Dockerfile](#8-dockerfile)
- [9. Volumes](#9-volumes)
- [10. Redes](#10-redes)
- [11. Docker Compose](#11-docker-compose)
- [12. Boas Práticas](#12-boas-práticas)
- [13. Docker na Engenharia de Dados](#13-docker-na-engenharia-de-dados)
- [14. Casos de Uso](#14-casos-de-uso)
- [15. Cheat Sheet](#15-cheat-sheet)

---

# 1. Introdução

Docker é uma plataforma que permite empacotar aplicações juntamente com todas as suas dependências em unidades chamadas **containers**.

Seu principal objetivo é garantir que uma aplicação execute da mesma forma em qualquer ambiente, eliminando problemas de compatibilidade entre máquinas.

---

# 2. O que é Docker?

Docker é uma plataforma de conteinerização que utiliza recursos do próprio sistema operacional para isolar aplicações.

Cada container possui:

- Aplicação
- Bibliotecas
- Dependências
- Configurações

Tudo isso é executado de forma isolada do restante do sistema.

## Principais benefícios

- Portabilidade
- Facilidade de implantação
- Ambientes reproduzíveis
- Escalabilidade
- Maior produtividade
- Melhor utilização de recursos

---

# 3. Virtualização vs Containers

## Máquinas Virtuais

Cada máquina virtual possui:

- Sistema Operacional completo
- Kernel próprio
- Bibliotecas
- Aplicações

Isso aumenta o consumo de memória e processamento.

### Vantagens

- Isolamento elevado
- Suporte a diferentes sistemas operacionais

### Desvantagens

- Inicialização lenta
- Alto consumo de recursos

---

## Containers

Containers compartilham o kernel do sistema operacional.

Cada container possui apenas:

- Aplicação
- Dependências
- Bibliotecas

### Vantagens

- Inicialização rápida
- Baixo consumo de memória
- Leves
- Fácil distribuição

---

# 4. Arquitetura do Docker

A arquitetura do Docker é composta por:

## Docker Client

Interface utilizada pelo usuário.

Exemplo:

```bash
docker run nginx
```

---

## Docker Daemon

Serviço responsável por:

- Criar containers
- Gerenciar imagens
- Redes
- Volumes

---

## Docker Registry

Local onde as imagens ficam armazenadas.

Exemplos:

- Docker Hub
- GitHub Container Registry
- Azure Container Registry
- Amazon ECR

---

## Docker Engine

É o conjunto formado por:

- Docker Client
- Docker Daemon
- APIs

---

# 5. Instalação

## Windows

Instalar:

- Docker Desktop

Necessário:

- WSL2
- Virtualização habilitada

---

## Linux

Instalar:

- Docker Engine

Verificar instalação:

```bash
docker --version
```

Executar container de teste:

```bash
docker run hello-world
```

---

# 6. Conceitos Fundamentais

## Image

Modelo utilizado para criar containers.

É imutável.

---

## Container

Instância em execução de uma imagem.

---

## Dockerfile

Arquivo responsável por construir imagens Docker.

---

## Registry

Servidor que armazena imagens.

---

## Repository

Coleção de versões de uma imagem.

Exemplo:

```
python
```

---

## Tag

Representa uma versão específica.

Exemplo:

```
python:3.12
```

---

## Volume

Permite persistência de dados.

Os dados continuam existindo mesmo após remover um container.

---

## Bind Mount

Mapeia uma pasta do computador para dentro do container.

---

## Network

Permite comunicação entre containers.

---

# 7. Comandos Essenciais

## Baixar imagem

```bash
docker pull nginx
```

---

## Listar imagens

```bash
docker images
```

---

## Criar container

```bash
docker run nginx
```

---

## Executar em background

```bash
docker run -d nginx
```

---

## Nomear container

```bash
docker run --name web nginx
```

---

## Publicar porta

```bash
docker run -p 8080:80 nginx
```

---

## Listar containers

```bash
docker ps
```

Todos:

```bash
docker ps -a
```

---

## Parar container

```bash
docker stop nome
```

---

## Iniciar container

```bash
docker start nome
```

---

## Reiniciar

```bash
docker restart nome
```

---

## Remover container

```bash
docker rm nome
```

---

## Remover imagem

```bash
docker rmi imagem
```

---

## Executar terminal

```bash
docker exec -it container bash
```

ou

```bash
docker exec -it container sh
```

---

## Ver logs

```bash
docker logs container
```

---

## Informações detalhadas

```bash
docker inspect container
```

---

# 8. Dockerfile

## Estrutura básica

```Dockerfile
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
```

---

## Principais instruções

### FROM

Imagem base.

### WORKDIR

Diretório de trabalho.

### COPY

Copia arquivos.

### ADD

Copia arquivos com recursos adicionais.

### RUN

Executa comandos durante a construção.

### CMD

Comando executado quando o container inicia.

### ENTRYPOINT

Define o processo principal.

### ENV

Variáveis de ambiente.

### EXPOSE

Documenta portas utilizadas.

---

## Construindo uma imagem

```bash
docker build -t minha-imagem .
```

---

# 9. Volumes

Volumes permitem persistência dos dados.

Criar:

```bash
docker volume create dados
```

Utilizar:

```bash
docker run -v dados:/var/lib/mysql mysql
```

Listar:

```bash
docker volume ls
```

Remover:

```bash
docker volume rm dados
```

---

# 10. Redes

Listar redes:

```bash
docker network ls
```

Criar:

```bash
docker network create minha-rede
```

Executar container na rede:

```bash
docker run --network minha-rede nginx
```

Remover:

```bash
docker network rm minha-rede
```

---

# 11. Docker Compose

Docker Compose permite executar múltiplos containers através de um único arquivo.

Exemplo:

```yaml
services:
  app:
    build: .

    ports:
      - "8000:8000"

  postgres:
    image: postgres:17

    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
```

Executar:

```bash
docker compose up
```

Background:

```bash
docker compose up -d
```

Parar:

```bash
docker compose down
```

---

# 12. Boas Práticas

## Utilize imagens oficiais

Sempre que possível utilize imagens oficiais do Docker Hub.

---

## Utilize versões específicas

Evite:

```text
latest
```

Prefira:

```text
python:3.12
```

---

## Utilize .dockerignore

Evita copiar arquivos desnecessários.

Exemplo:

```
.git
venv
__pycache__
.env
```

---

## Utilize Multi-stage Build

Reduz significativamente o tamanho da imagem final.

---

## Não execute containers como root

Sempre que possível utilize usuários específicos.

---

## Mantenha imagens pequenas

Escolha imagens leves, como:

- alpine
- slim

---

# 13. Docker na Engenharia de Dados

Docker é amplamente utilizado para padronizar ambientes de desenvolvimento e produção em projetos de dados.

## Ferramentas frequentemente utilizadas

- PostgreSQL
- MySQL
- MongoDB
- Redis
- MinIO
- Apache Spark
- Apache Airflow
- Kafka
- dbt
- Jupyter Notebook

## Benefícios

- Ambiente reproduzível
- Fácil compartilhamento entre equipes
- Isolamento de dependências
- Integração com pipelines CI/CD
- Facilidade para testes locais

---

# 14. Casos de Uso

## Desenvolvimento Local

Criar ambientes completos rapidamente.

---

## Testes

Executar aplicações isoladas sem interferir no sistema operacional.

---

## Deploy

Empacotar aplicações para produção.

---

## Microserviços

Executar cada serviço em seu próprio container.

---

## Engenharia de Dados

Executar localmente ambientes completos contendo:

- Banco de Dados
- Spark
- Airflow
- Kafka
- MinIO
- dbt

---

# 15. Cheat Sheet

| Comando               | Descrição              |
| --------------------- | ---------------------- |
| `docker pull`         | Baixa imagem           |
| `docker build`        | Constrói imagem        |
| `docker images`       | Lista imagens          |
| `docker run`          | Cria container         |
| `docker ps`           | Lista containers       |
| `docker stop`         | Para container         |
| `docker start`        | Inicia container       |
| `docker restart`      | Reinicia container     |
| `docker rm`           | Remove container       |
| `docker rmi`          | Remove imagem          |
| `docker exec`         | Acessa container       |
| `docker logs`         | Exibe logs             |
| `docker inspect`      | Informações detalhadas |
| `docker volume ls`    | Lista volumes          |
| `docker network ls`   | Lista redes            |
| `docker compose up`   | Inicia ambiente        |
| `docker compose down` | Finaliza ambiente      |

---

# Referências

- Documentação oficial do Docker
- Docker Hub
- Docker Compose
- Boas práticas para conteinerização
