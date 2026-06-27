# Etapa 4 — Capacitação em MongoDB

## Objetivo

Desenvolver conhecimentos em bancos de dados NoSQL, compreendendo os conceitos fundamentais do MongoDB, modelagem orientada a documentos, operações CRUD, indexação e agregações para aplicação em projetos de Engenharia de Dados.

---

# Tarefa 1 — Fundamentos do MongoDB

## Banco Relacional x Não Relacional

Os bancos de dados relacionais armazenam informações em tabelas estruturadas e relacionamentos previamente definidos. Já os bancos NoSQL oferecem maior flexibilidade de modelagem e escalabilidade horizontal, sendo indicados para cenários de grande volume e variedade de dados.

## O que é o MongoDB

MongoDB é um banco de dados NoSQL orientado a documentos que armazena dados no formato BSON (Binary JSON), permitindo estruturas dinâmicas e sem esquema rígido.

## Principais Entidades do MongoDB

- **Database:** conjunto de collections.
- **Collection:** agrupamento de documentos, equivalente a uma tabela.
- **Document:** unidade básica de armazenamento, equivalente a um registro.
- **Field:** atributo presente em um documento.

Exemplo:

```json
{
  "nome": "Mileno",
  "idade": 29,
  "cidade": "Mossoró"
}
```

## MongoDB e JSON

Os documentos são armazenados em BSON, uma extensão binária do JSON que suporta tipos adicionais, como datas, arrays e ObjectId.

## Drivers do MongoDB

O MongoDB disponibiliza drivers para diversas linguagens, permitindo a integração com aplicações:

- Python (PyMongo)
- Java
- Node.js
- C#
- Go
- PHP

---

# Tarefa 2 — Gerenciamento de Bancos de Dados

## Selecionando ou criando um banco

```javascript
use cadastro
```

## Exibindo todos os bancos

```javascript
show dbs
```

## Criando uma collection

```javascript
db.createCollection("usuarios");
```

## Exibindo collections

```javascript
show collections
```

## Removendo uma collection

```javascript
db.usuarios.drop();
```

## Removendo um banco de dados

```javascript
db.dropDatabase();
```

## Importando dados em JSON

```bash
mongoimport --db cadastro --collection usuarios --file usuarios.json --jsonArray
```

## Exportando dados

```bash
mongoexport --db cadastro --collection usuarios --out usuarios.json
```

---

# Tarefa 3 — Inserção de Dados (Create)

## Inserindo um documento

```javascript
db.usuarios.insertOne({
  nome: "Mileno",
  idade: 29,
});
```

## Inserindo múltiplos documentos

```javascript
db.usuarios.insertMany([
  { nome: "João", idade: 30 },
  { nome: "Maria", idade: 25 },
]);
```

## Definindo o campo `_id`

```javascript
db.usuarios.insertOne({
  _id: 1,
  nome: "Pedro",
});
```

## Write Concern

Permite definir o nível de confirmação de escrita dos dados.

```javascript
db.usuarios.insertOne({ nome: "Teste" }, { writeConcern: { w: 1 } });
```

---

# Tarefa 4 — Leitura de Dados (Read)

## Buscar todos os documentos

```javascript
db.usuarios.find();
```

## Formatar o retorno

```javascript
db.usuarios.find().pretty();
```

## Buscar um documento específico

```javascript
db.usuarios.find({
  nome: "Mileno",
});
```

## Buscar por múltiplos critérios

```javascript
db.usuarios.find({
  idade: 29,
  cidade: "Mossoró",
});
```

## Operadores de comparação

Maior que:

```javascript
db.usuarios.find({
  idade: { $gt: 25 },
});
```

Menor que:

```javascript
db.usuarios.find({
  idade: { $lt: 30 },
});
```

## Operador OR

```javascript
db.usuarios.find({
  $or: [{ cidade: "Natal" }, { cidade: "Mossoró" }],
});
```

## Contagem de documentos

```javascript
db.usuarios.countDocuments();
```

---

# Tarefa 5 — Atualização de Dados (Update)

## Atualizar um documento

```javascript
db.usuarios.updateOne({ nome: "Mileno" }, { $set: { idade: 30 } });
```

## Atualizar vários documentos

```javascript
db.usuarios.updateMany({}, { $set: { ativo: true } });
```

## Substituir um documento inteiro

```javascript
db.usuarios.replaceOne(
  { nome: "Mileno" },
  {
    nome: "Mileno",
    idade: 30,
  },
);
```

---

# Tarefa 6 — Remoção de Dados (Delete)

## Remover um documento

```javascript
db.usuarios.deleteOne({
  nome: "Mileno",
});
```

## Remover vários documentos

```javascript
db.usuarios.deleteMany({
  ativo: false,
});
```

## Remover todos os documentos

```javascript
db.usuarios.deleteMany({});
```

---

# Tarefa 7 — Tipos de Dados

Principais tipos de dados suportados pelo MongoDB:

- String
- Number
- Boolean
- Date
- Array
- Object (Document)
- ObjectId
- Null

Exemplo:

```javascript
{
  nome: "Mileno",
  idade: 29,
  ativo: true,
  criadoEm: new Date(),
  telefones: ["99999-9999"]
}
```

---

# Tarefa 8 — Operadores de Query

## Operador de igualdade

```javascript
db.usuarios.find({
  cidade: "Mossoró",
});
```

## Operador `$in`

```javascript
db.usuarios.find({
  cidade: {
    $in: ["Mossoró", "Natal"],
  },
});
```

## Operador `$ne`

```javascript
db.usuarios.find({
  idade: {
    $ne: 30,
  },
});
```

## Operador `$exists`

```javascript
db.usuarios.find({
  telefone: {
    $exists: true,
  },
});
```

## Operador `$text`

```javascript
db.usuarios.find({
  $text: {
    $search: "engenheiro",
  },
});
```

---

# Tarefa 9 — Relacionamentos e Modelagem

## Embedded Documents

```javascript
{
  nome: "Mileno",
  endereco: {
    cidade: "Mossoró",
    estado: "RN"
  }
}
```

## Tipos de relacionamento

- One to One
- One to Many
- Many to Many

A modelagem em MongoDB deve equilibrar:

- Performance;
- Facilidade de consulta;
- Duplicação de dados;
- Manutenção.

---

# Tarefa 10 — Arrays e Documents

## Buscar em Embedded Documents

```javascript
db.usuarios.find({
  "endereco.cidade": "Mossoró",
});
```

## Buscar em Arrays

```javascript
db.usuarios.find({
  tags: "python",
});
```

## Operador `$all`

```javascript
db.usuarios.find({
  tags: {
    $all: ["python", "mongodb"],
  },
});
```

## Operador `$elemMatch`

```javascript
db.usuarios.find({
  cursos: {
    $elemMatch: {
      nome: "MongoDB",
      concluido: true,
    },
  },
});
```

---

# Tarefa 11 — Operadores de Update

## Incrementar valores

```javascript
$inc;
```

## Definir valor mínimo

```javascript
$min;
```

## Definir valor máximo

```javascript
$max;
```

## Multiplicar valores

```javascript
$mul;
```

## Renomear campos

```javascript
$rename;
```

## Remover campos

```javascript
$unset;
```

## Manipular Arrays

```javascript
$push;
$addToSet;
$pop;
$pullAll;
```

---

# Tarefa 12 — Índices

## Criando um índice

```javascript
db.usuarios.createIndex({
  nome: 1,
});
```

## Índice composto

```javascript
db.usuarios.createIndex({
  nome: 1,
  cidade: 1,
});
```

## Índice de texto

```javascript
db.usuarios.createIndex({
  descricao: "text",
});
```

## Verificando índices

```javascript
db.usuarios.getIndexes();
```

## Removendo um índice

```javascript
db.usuarios.dropIndex("nome_1");
```

---

# Tarefa 13 — Aggregation Framework

## Estrutura básica

```javascript
db.usuarios.aggregate([
  {
    $match: {
      ativo: true,
    },
  },
]);
```

## Ordenação

```javascript
{
  $sort: {
    idade: -1;
  }
}
```

## Limitação de resultados

```javascript
{
  $limit: 10;
}
```

## Paginação

```javascript
{
  $skip: 10;
}
```

## Desconstrução de Arrays

```javascript
{
  $unwind: "$tags";
}
```

## Agrupamento

```javascript
{
  $group: {
    _id: "$cidade",
    total: {
      $sum: 1
    }
  }
}
```

## Criando uma nova collection

```javascript
{
  $out: "usuarios_resumo";
}
```

---

# Conhecimentos Consolidados

Ao final da capacitação foram adquiridos conhecimentos sobre:

- Conceitos de bancos de dados NoSQL;
- Estrutura e modelagem orientada a documentos;
- Operações CRUD;
- Consultas avançadas;
- Manipulação de arrays e documentos embutidos;
- Operadores de atualização;
- Indexação e otimização de consultas;
- Aggregation Framework;
- Importação e exportação de dados;
- Administração básica do MongoDB.

Os conhecimentos adquiridos servem como base para utilização do MongoDB em projetos de Engenharia de Dados, aplicações distribuídas e ambientes de desenvolvimento local, especialmente em conjunto com Docker e ferramentas de processamento de dados.
