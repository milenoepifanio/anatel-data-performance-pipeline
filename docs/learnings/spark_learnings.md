# Aprendizados sobre Spark — PDI

> Registro dos principais conceitos e lições aprendidas ao utilizar PySpark no projeto para transformar dados em formato analítico.

---

## 1. O que foi aprendido com o Spark

O PySpark foi utilizado como motor principal para transformar os arquivos ODS e gerar datasets em formato Parquet. Durante o projeto, foi possível entender melhor como o Spark lida com grandes volumes de dados e como estruturar transformações de forma mais escalável.

O principal aprendizado foi perceber que o Spark é muito útil quando a transformação exige:

- processamento tabular estruturado;
- execução distribuída ou local com boa performance;
- leitura e escrita de arquivos em formatos como Parquet;
- validação de dados em pipelines mais robustos.

---

## 2. Conceitos importantes aplicados

### DataFrames

O uso de DataFrames foi essencial para organizar a lógica de transformação. Eles tornam o código mais legível e permitem aplicar operações de forma declarativa.

### Transformações e ações

Um ponto importante aprendido foi a diferença entre transformações e ações:

- transformações definem um novo fluxo de dados;
- ações executam o processamento efetivamente.

Isso é fundamental para evitar comportamentos inesperados e entender melhor o custo das operações.

### Schema e validação

Durante a implementação, tornou-se claro que validar o schema antes de processar os dados é uma boa prática. Isso ajuda a encontrar problemas cedo e evita falhas em etapas posteriores do pipeline.

---

## 3. Aprendizados práticos no projeto

### Transformação wide-to-long

Uma das partes mais relevantes do projeto foi a transformação de dados em formato wide para long. Esse tipo de transformação mostrou-se muito útil porque facilita a análise temporal e o uso posterior em modelos analíticos.

### Uso de funções do Spark SQL

O projeto também ajudou a consolidar o uso de funções como:

- `select`;
- `withColumn`;
- `filter`;
- `expr`;
- `cast`.

Essas operações foram suficientes para estruturar grande parte do fluxo de transformação.

### Limpeza e normalização

Outro aprendizado importante foi que a transformação não é apenas sobre mover dados de um formato para outro. Também é necessário:

- padronizar nomes de colunas;
- tratar valores nulos;
- ajustar tipos;
- remover inconsistências.

---

## 4. Desafios enfrentados

Alguns desafios foram observados durante o uso do Spark:

- entender corretamente o comportamento de certas funções;
- lidar com arquivos com estrutura heterogênea;
- garantir que as validações fossem aplicadas antes da escrita final;
- equilibrar simplicidade e robustez no código.

Esses desafios fizeram com que o projeto se tornasse uma boa base para aprender Spark de forma prática.

---

## 5. Boas práticas que ficaram claras

- manter as transformações em etapas pequenas e claras;
- validar os dados antes de salvar os arquivos finais;
- usar nomes de colunas padronizados;
- separar responsabilidades entre leitura, transformação e escrita;
- documentar as regras de negócio aplicadas nas transformações.

---

## 6. Conclusão

O aprendizado principal com o Spark foi que ele é uma excelente ferramenta para transformar dados de forma estruturada, escalável e organizada. No projeto, ele mostrou-se adequado para a camada intermediária de processamento, especialmente quando combinado com Python e Parquet.
