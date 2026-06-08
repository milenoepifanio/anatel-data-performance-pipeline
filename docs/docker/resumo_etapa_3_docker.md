# Etapa 3 — Capacitação em Docker

## Objetivo

Desenvolver conhecimentos sobre Docker e containerização, compreendendo conceitos de ambientes reproduzíveis e suas aplicações em projetos de dados.

---

# Tarefa 1 — Fundamentos de Docker

## O que é Docker

Docker é uma plataforma de containerização que permite empacotar aplicações, dependências e configurações em ambientes isolados chamados containers.

### Exemplo de chamada

```bash
docker --version
```

```bash
docker info
```

---

## Rodando um container no Docker

Executa um container a partir de uma imagem.

### Exemplo de chamada

```bash
docker run hello-world
```

---

# Tarefa 2 — Evolução prática no curso de Docker

## Containers

Containers são instâncias em execução criadas a partir de imagens Docker.

### Rodar um container

```bash
docker run nginx
```

### Rodar um container em modo interativo

```bash
docker run -it ubuntu bash
```

### Rodar um container em background

```bash
docker run -d nginx
```

### Expor porta de um container

```bash
docker run -d -p 8080:80 nginx
```

### Definir nome para um container

```bash
docker run -d --name meu_nginx nginx
```

### Verificar containers em execução

```bash
docker ps
```

### Verificar todos os containers

```bash
docker ps -a
```

### Parar um container

```bash
docker stop meu_nginx
```

### Reiniciar um container

```bash
docker restart meu_nginx
```

### Acessar logs de um container

```bash
docker logs meu_nginx
```

### Remover um container

```bash
docker rm meu_nginx
```

---

## Imagens Docker

Imagens são modelos imutáveis utilizados para criar containers.

### Listar imagens

```bash
docker images
```

### Baixar uma imagem

```bash
docker pull python:3.11
```

### Criar uma imagem a partir de um Dockerfile

```bash
docker build -t minha-imagem .
```

### Rodar um container usando uma imagem criada

```bash
docker run minha-imagem
```

### Nomear imagem no build

```bash
docker build -t meu-projeto:v1 .
```

### Remover uma imagem

```bash
docker rmi meu-projeto:v1
```

### Remover imagens não utilizadas

```bash
docker image prune
```

### Remover containers e imagens não utilizados

```bash
docker system prune
```

---

## Dockerfile

Arquivo utilizado para definir os passos de criação de uma imagem Docker.

### Exemplo de Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### Exemplo de build

```bash
docker build -t pipeline-dados .
```

### Exemplo de execução

```bash
docker run pipeline-dados
```

---

## Copiando arquivos do container

Permite copiar arquivos entre a máquina local e o container.

### Copiar arquivo do container para a máquina local

```bash
docker cp meu_container:/app/saida.csv ./saida.csv
```

### Copiar arquivo da máquina local para o container

```bash
docker cp ./entrada.csv meu_container:/app/entrada.csv
```

---

## Inspecionando containers

Permite visualizar detalhes técnicos do container.

### Exemplo de chamada

```bash
docker inspect meu_container
```

---

## Verificando processamento do container

Mostra uso de CPU, memória e rede dos containers.

### Exemplo de chamada

```bash
docker stats
```

---

## Autenticação no Docker Hub

Permite autenticar no Docker Hub para enviar ou baixar imagens privadas.

### Login

```bash
docker login
```

### Logout

```bash
docker logout
```

---

## Enviando imagens para o Docker Hub

### Criar tag para a imagem

```bash
docker tag minha-imagem usuario/minha-imagem:v1
```

### Enviar imagem

```bash
docker push usuario/minha-imagem:v1
```

### Utilizar imagem publicada

```bash
docker pull usuario/minha-imagem:v1
```

```bash
docker run usuario/minha-imagem:v1
```

---

# Volumes

Volumes permitem persistir dados fora do ciclo de vida do container.

## Criar volume manualmente

```bash
docker volume create meu_volume
```

## Listar volumes

```bash
docker volume ls
```

## Inspecionar volume

```bash
docker volume inspect meu_volume
```

## Usar volume nomeado

```bash
docker run -d --name banco -v meu_volume:/var/lib/mysql mysql
```

## Usar bind mount

```bash
docker run -d -v $(pwd):/app python:3.11
```

## Volume somente leitura

```bash
docker run -d -v $(pwd):/app:ro python:3.11
```

## Remover volume

```bash
docker volume rm meu_volume
```

## Remover volumes não utilizados

```bash
docker volume prune
```

---

# Networks

Networks permitem comunicação entre containers.

## Listar networks

```bash
docker network ls
```

## Criar uma network

```bash
docker network create minha_rede
```

## Rodar container conectado a uma network

```bash
docker run -d --name app --network minha_rede nginx
```

## Conectar container a uma network

```bash
docker network connect minha_rede meu_container
```

## Desconectar container de uma network

```bash
docker network disconnect minha_rede meu_container
```

## Inspecionar network

```bash
docker network inspect minha_rede
```

## Remover network

```bash
docker network rm minha_rede
```

## Remover networks não utilizadas

```bash
docker network prune
```

---

# YAML

YAML é uma linguagem de serialização utilizada para arquivos de configuração, como `docker-compose.yml` e manifestos Kubernetes.

## Exemplo básico de YAML

```yaml
nome: projeto-dados
ambiente: desenvolvimento
ativo: true
versao: 1

servicos:
  - api
  - banco
  - worker

configuracao:
  memoria: 512mb
  replicas: 2
```

---

# Docker Compose

Docker Compose permite gerenciar múltiplos containers com um único arquivo de configuração.

## Exemplo de docker-compose.yml

```yaml
services:
  app:
    build: .
    container_name: app_dados
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - AMBIENTE=dev
    depends_on:
      - banco

  banco:
    image: postgres:16
    container_name: banco_dados
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin
      - POSTGRES_DB=dw
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Rodar Compose

```bash
docker compose up
```

## Rodar Compose em background

```bash
docker compose up -d
```

## Parar Compose

```bash
docker compose down
```

## Rebuildar imagens no Compose

```bash
docker compose up --build
```

## Verificar serviços

```bash
docker compose ps
```

## Ver logs dos serviços

```bash
docker compose logs
```

## Executar comando dentro de um serviço

```bash
docker compose exec app bash
```

---

# Docker Swarm

Docker Swarm é uma ferramenta de orquestração nativa do Docker.

## Inicializar Swarm

```bash
docker swarm init
```

## Listar nodes

```bash
docker node ls
```

## Criar serviço

```bash
docker service create --name web -p 8080:80 nginx
```

## Listar serviços

```bash
docker service ls
```

## Inspecionar serviço

```bash
docker service inspect web
```

## Escalar serviço

```bash
docker service scale web=3
```

## Atualizar imagem do serviço

```bash
docker service update --image nginx:latest web
```

## Remover serviço

```bash
docker service rm web
```

## Sair do Swarm

```bash
docker swarm leave
```

---

# Kubernetes

Kubernetes é uma plataforma de orquestração de containers utilizada para gerenciar aplicações distribuídas.

## Verificar versão do kubectl

```bash
kubectl version --client
```

## Inicializar Minikube

```bash
minikube start
```

## Parar Minikube

```bash
minikube stop
```

## Acessar dashboard

```bash
minikube dashboard
```

---

## Deployments

Deployment define como uma aplicação deve ser executada no cluster.

### Criar deployment

```bash
kubectl create deployment app-dados --image=nginx
```

### Listar deployments

```bash
kubectl get deployments
```

### Ver pods

```bash
kubectl get pods
```

### Escalar deployment

```bash
kubectl scale deployment app-dados --replicas=3
```

### Atualizar imagem

```bash
kubectl set image deployment/app-dados nginx=nginx:latest
```

### Desfazer alteração

```bash
kubectl rollout undo deployment/app-dados
```

### Deletar deployment

```bash
kubectl delete deployment app-dados
```

---

## Services

Services expõem aplicações executadas em pods.

### Criar service

```bash
kubectl expose deployment app-dados --type=NodePort --port=80
```

### Listar services

```bash
kubectl get services
```

### Gerar URL com Minikube

```bash
minikube service app-dados --url
```

### Deletar service

```bash
kubectl delete service app-dados
```

---

## Modo declarativo no Kubernetes

Permite criar recursos a partir de arquivos YAML.

### Exemplo de deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-dados
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app-dados
  template:
    metadata:
      labels:
        app: app-dados
    spec:
      containers:
        - name: app-dados
          image: nginx
          ports:
            - containerPort: 80
```

### Aplicar arquivo

```bash
kubectl apply -f deployment.yaml
```

### Remover recurso pelo arquivo

```bash
kubectl delete -f deployment.yaml
```

---

# Tarefa 3 — Registro e documentação dos aprendizados

## Principais aprendizados

Ao longo da capacitação foi possível compreender:

- Conceitos fundamentais de Docker e containerização.
- Diferença entre imagens e containers.
- Ciclo de vida dos containers.
- Construção de imagens com Dockerfile.
- Uso de volumes para persistência de dados.
- Uso de networks para comunicação entre containers.
- Utilização de YAML para arquivos de configuração.
- Gerenciamento de múltiplos containers com Docker Compose.
- Conceitos iniciais de orquestração com Docker Swarm.
- Conceitos fundamentais de Kubernetes.
- Importância de ambientes reproduzíveis em projetos de dados.

---

# Aplicação no Projeto

## Contexto

> Preencher posteriormente com a análise da aplicação dos conceitos de Docker no projeto do PDI.

## Possíveis pontos de aplicação

- [x] **Containerização da Pipeline PySpark**: Empacotar a aplicação de transformação com PySpark, pandas, pyarrow e dependências em um container isolado para garantir consistência entre ambientes.

- [x] **Ambientes Reproduzíveis para Desenvolvimento**: Criar containers para notebooks Jupyter e ambientes de desenvolvimento, eliminando problemas de "funciona na minha máquina" e garantindo paridade entre dev, staging e produção.

- [x] **Orquestração Multi-Serviços com Docker Compose**: Coordenar múltiplos serviços (aplicação PySpark, Spark Master/Worker, DuckDB, PostgreSQL para dbt, Jupyter) em um único arquivo `docker-compose.yml`.

- [x] **Persistência de Dados com Volumes**: Utilizar volumes Docker para persistir dados RAW, STAGING e MARTS, garantindo que os dados sobrevivam ao ciclo de vida dos containers.

- [x] **Isolamento da Pipeline dbt**: Criar container específico para execução de modelos dbt (staging e marts), separando a lógica de transformação analítica da ingestão.

- [x] **Cluster Spark Distribuído Localmente**: Configurar cluster Spark com múltiplos workers em containers, permitindo teste de processamento distribuído antes de deploy em produção.

- [x] **Networks Docker para Comunicação**: Implementar redes internas para permitir comunicação segura entre containers (Spark, DuckDB, dbt) sem expor todas as portas.

---

# Resultado Obtido

- Melhor entendimento sobre Docker.
- Maior conhecimento sobre containerização.
- Conhecimento introdutório sobre ambientes reproduzíveis.
- Evolução conceitual em práticas modernas de Engenharia de Dados.
- Maior familiaridade com comandos essenciais de Docker, Docker Compose, Docker Swarm e Kubernetes.
