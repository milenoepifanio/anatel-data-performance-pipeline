# Aprendizados sobre LocalStack — PDI

> Registro dos principais conceitos e aprendizados adquiridos ao utilizar LocalStack para simular serviços AWS no ambiente local do projeto.

---

## 1. O que é o LocalStack

O LocalStack é uma ferramenta que permite emular serviços da AWS localmente, sem depender de uma conta real ou de recursos cloud. No projeto, ele foi utilizado principalmente para simular o funcionamento de um bucket S3 durante o desenvolvimento da pipeline.

Essa abordagem foi útil porque permitiu:

- testar a integração com S3 sem custos;
- validar o fluxo de upload de arquivos Parquet;
- desenvolver e depurar a pipeline em um ambiente local controlado.

---

## 2. Por que foi usado no projeto

No contexto do PDI, o LocalStack foi importante para representar o armazenamento intermediário da camada Silver. O pipeline precisou enviar arquivos Parquet para um endpoint compatível com S3, e o LocalStack possibilitou essa validação com mais rapidez e segurança.

O benefício principal foi reduzir a dependência de infraestrutura externa durante a fase de desenvolvimento.

---

## 3. Principais aprendizados

### Simulação local de S3

O uso do LocalStack mostrou que é possível reproduzir boa parte do comportamento de um bucket S3 em ambiente local. Isso facilitou testes de upload, listagem e organização de prefixos.

### Importância do endpoint e das credenciais

Uma parte importante do aprendizado foi entender que a integração com S3 exige configuração correta de:

- endpoint local;
- chave de acesso;
- chave secreta;
- região;
- nome do bucket.

Sem essa configuração adequada, a comunicação com o serviço simulado falha.

### Desenvolvimento mais ágil

Com o LocalStack, a equipe conseguiu iterar mais rapidamente sobre a pipeline, sem depender de um ambiente cloud real para validar o fluxo de dados.

---

## 4. Boas práticas observadas

- manter o LocalStack rodando durante os testes de integração;
- usar nomes de bucket e prefixos consistentes com o projeto;
- validar a estrutura de pastas e arquivos antes de publicar no armazenamento;
- separar claramente os testes locais dos fluxos de produção.

---

## 5. Limitações percebidas

Apesar de ser muito útil, o LocalStack não substitui completamente um ambiente AWS real. Algumas diferenças podem aparecer em relação a:

- comportamento específico de alguns serviços;
- compatibilidade com recursos mais avançados;
- cenários de produção mais complexos.

Mesmo assim, ele mostrou-se excelente para desenvolvimento local e validação inicial.

---

## 6. Conclusão

O LocalStack foi uma peça importante na evolução do projeto porque permitiu testar a camada de integração com armazenamento em S3 de forma prática e local. O aprendizado principal foi que ele acelera o desenvolvimento e reduz riscos, desde que seja usado com uma configuração clara e com entendimento de suas limitações.
