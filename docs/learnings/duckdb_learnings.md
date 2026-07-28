# Aprendizados sobre DuckDB — PDI

> Registro dos principais conceitos e lições aprendidas ao utilizar DuckDB como camada analítica local no projeto.

---

## 1. O que é o DuckDB

O DuckDB é um banco de dados analítico embutido, leve e muito eficiente para workloads de leitura e agregação. No projeto, ele foi utilizado como camada de análise local, principalmente para consultar os dados já transformados e para integrar com a camada dbt.

O principal atrativo do DuckDB neste contexto foi a possibilidade de trabalhar com dados analíticos sem precisar de uma infraestrutura pesada.

---

## 2. Por que foi usado no projeto

O DuckDB foi adotado porque o projeto precisava de uma solução simples e rápida para:

- explorar os dados gerados em Parquet;
- criar uma camada analítica local;
- servir como alvo de execução para os modelos dbt;
- facilitar validações e análises sem depender de um banco tradicional.

---

## 3. Principais aprendizados

### Simplicidade de uso

Um dos maiores aprendizados foi perceber que o DuckDB é muito fácil de integrar em fluxos de dados locais. Ele funciona bem como ferramenta de execução analítica e de validação intermediária.

### Boa integração com Parquet

A integração com arquivos Parquet foi particularmente útil no projeto, pois permitiu consultar dados gerados pela pipeline sem a necessidade de carregar tudo em outro sistema.

### Uso com dbt

O DuckDB também mostrou-se adequado como alvo de execução do dbt. Isso permitiu unir a camada de transformação SQL com a camada de armazenamento analítico local de forma prática.

---

## 4. Conceitos aplicados no projeto

### Banco local

O DuckDB foi usado com um arquivo local no repositório, o que facilita o desenvolvimento e a reproducibilidade da análise.

### Consultas analíticas

Ele se mostrou eficiente para consultas agregadas e exploração de dados, principalmente quando o objetivo era validar a qualidade e a estrutura dos datasets gerados.

### Integração com S3 e Parquet

O projeto também mostrou que o DuckDB pode ser integrado a cenários com leitura de arquivos externos e armazenamento em S3, o que amplia o seu uso em pipelines modernos.

---

## 5. Vantagens percebidas

- leve e rápido;
- fácil de configurar localmente;
- ótimo para analítica e validação;
- bom suporte a consultas SQL e leitura de Parquet;
- útil para integração com dbt.

---

## 6. Desafios enfrentados

Alguns pontos exigiram mais atenção:

- garantir a configuração correta do ambiente de execução;
- manter a consistência entre os dados armazenados e os dados lidos pelos modelos;
- entender o papel do DuckDB dentro da arquitetura mais ampla do projeto.

---

## 7. Conclusão

O DuckDB foi uma escolha muito adequada para o projeto porque uniu simplicidade, performance e integração com o fluxo analítico. O aprendizado principal foi que ele funciona muito bem como camada analítica local em pipelines de dados em desenvolvimento, principalmente quando combinado com dbt e Parquet.
