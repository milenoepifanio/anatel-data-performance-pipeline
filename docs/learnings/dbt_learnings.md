# Aprendizados sobre dbt — PDI

> Registro dos principais conceitos, práticas e lições aprendidas ao aplicar dbt no projeto PDI.

---

## 1. O que o dbt representa neste projeto

dbt foi introduzido como a camada de Analytics Engineering da pipeline. Seu papel não é ingerir dados, mas transformar dados que já foram preparados por Python e PySpark e armazenados em formato Parquet.

Neste projeto, o dbt passou a ser responsável por:

- organizar transformações de forma estruturada e versionada;
- definir dependências entre modelos;
- documentar colunas e regras de negócio;
- aplicar testes automatizados na camada analítica;
- gerar uma linhagem mais clara entre os dados de origem e os marts finais.

---

## 2. Principais lições aprendidas

### O dbt funciona melhor como camada de transformação

Uma das maiores aprendizagens foi que o dbt deve ser usado após as camadas raw e silver já estarem preparadas. Neste repositório, Python e PySpark cuidam do processamento mais pesado e da geração dos arquivos Parquet, enquanto o dbt foca na modelagem e na estrutura analítica.

Essa separação deixa a arquitetura mais fácil de compreender:

- Python / PySpark: ingestão, padronização, transformação e escrita em Parquet;
- dbt: modelagem, testes, documentação e exposição analítica.

### As sources são importantes para a clareza

O uso de uma definição de source no dbt ajudou a deixar o contrato dos dados de entrada mais explícito. Em vez de escrever SQL direto contra um caminho ou localização de armazenamento, o projeto consegue descrever os dados externos como uma source e referenciá-los por meio de uma interface documentada.

Isso melhora:

- legibilidade;
- linhagem;
- manutenção futura;
- colaboração entre engenheiros de dados e analistas.

### Staging e marts são conceitualmente diferentes

Uma lição arquitetural importante foi separar:

- modelos staging: voltados para limpeza, padronização e preparação dos dados;
- marts: voltados para agregações e visões prontas para análise de negócio.

Essa organização torna os modelos mais fáceis de entender e reduz o risco de misturar lógica de transformação com lógica de negócio.

---

## 3. Conceitos que ficaram claros durante a implementação

### Source

Uma source é o ponto de entrada declarado para dados externos. Neste projeto, ela representa os dados Parquet disponíveis na camada S3/LocalStack e é usada pelos modelos staging.

### Model

Um model é uma transformação em SQL que vira um objeto do dbt no banco de destino. Neste repositório, os modelos foram usados para criar views de staging e tabelas de marts.

### Macros ref() e source()

O uso de `ref()` e `source()` representou uma melhora significativa em termos de manutenibilidade. Essas macros deixam as dependências explícitas e permitem que o dbt monte a ordem de execução automaticamente.

### Materialização

A distinção entre views e tabelas ficou mais clara na prática:

- views são mais leves e ficam mais próximas da source;
- tabelas são persistidas e mais adequadas para consumo analítico final.

Isso foi especialmente relevante ao organizar as camadas staging e marts.

### Testes e documentação

Um dos aspectos mais valiosos do dbt foi perceber que testes e documentação fazem parte do próprio produto de dados, e não apenas extras opcionais. Adicionar testes como not null, accepted values e unicidade aumenta a confiança no modelo analítico.

---

## 4. Fluxo prático usado no projeto

O fluxo do projeto seguiu esta lógica:

1. Python e PySpark geram arquivos Parquet em formato long.
2. O dbt declara esses arquivos como sources.
3. Modelos staging padronizam e preparam os dados.
4. Marts agregam e expõem a saída analítica.
5. Testes e documentação validam e descrevem os modelos.

Isso torna a pipeline mais modular e mais fácil de evoluir.

---

## 5. Aprendizados específicos do repositório

### O projeto usa uma estrutura analítica em camadas

A camada dbt ficou alinhada com a arquitetura mais ampla do projeto:

- ingestão e transformação acontecem em Python / PySpark;
- o dbt constrói a camada analítica acima disso;
- o DuckDB é usado como mecanismo analítico de destino.

### Os modelos são organizados por propósito

Os principais modelos dbt do projeto refletem bem essa separação:

- modelo staging para os dados SMP;
- marts para summaries e KPIs;
- testes e metadados organizados nos arquivos YAML do dbt.

### O projeto se beneficia de convenções bem definidas

Usar nomes consistentes, organização de pastas e propósito claro para cada modelo deixou o projeto mais fácil de seguir e expandir no futuro.

---

## 6. Comandos e fluxo aprendido

Os principais comandos operacionais usados durante a implementação foram:

```bash
dbt deps
dbt parse
dbt compile
dbt run
dbt test
dbt build
dbt docs generate
```

A lição prática mais importante foi que o `dbt build` é extremamente útil porque executa o modelo e seus testes juntos, facilitando a validação de todo o fluxo.

---

## 7. Desafios enfrentados

Alguns dos principais desafios encontrados foram:

- entender como o dbt deveria se encaixar em uma pipeline já existente com Python e PySpark;
- configurar corretamente a conexão com o DuckDB e o ambiente S3;
- garantir que o caminho da source e a localização dos Parquet gerados coincidissem com a estrutura esperada;
- manter a lógica de transformação limpa e não sobrecarregar a camada de marts.

Esses problemas foram resolvidos principalmente ao manter a camada dbt focada em modelagem e governança, em vez de tentar reproduzir todo o processamento pesado em SQL.

---

## 8. Recomendações para trabalhos futuros

Para futuras iterações do projeto, seria valioso:

- continuar usando modelos staging como uma camada limpa de contrato;
- expandir os testes além do baseline atual;
- documentar melhor as definições de negócio nos modelos dbt;
- explorar recursos mais avançados do dbt, como macros, seeds ou snapshots, conforme o projeto evoluir;
- manter a camada dbt alinhada com a arquitetura em estilo medallion já adotada.

---

## 9. Resumo

A principal aprendizagem dessa experiência é que o dbt agrega valor quando é usado como uma camada disciplinada de modelagem e governança sobre uma pipeline sólida de processamento de dados. Neste projeto, ele ajudou a transformar dados raw e silver em modelos analíticos organizados, documentados e testáveis.
