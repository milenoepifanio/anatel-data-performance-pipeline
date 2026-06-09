# Architecture — PDI

Documentação da arquitetura, padrões de engenharia, decisões estruturais e evolução técnica do projeto PDI.

| Documento | Conteúdo |
|-----------|----------|
| [medallion_architecture.md](./medallion_architecture.md) | Visão geral da arquitetura Medallion adotada no projeto, incluindo camadas RAW, SILVER, GOLD, Data Lake e Analytics Engineering |
| [project_standards.md](./project_standards.md) | Convenções de desenvolvimento, organização do repositório, padrões de código, boas práticas e diretrizes de engenharia |
| [technology_stack.md](./technology_stack.md) | Tecnologias utilizadas no projeto, responsabilidades de cada ferramenta e como elas se integram na arquitetura |
| [data_flow.md](./data_flow.md) | Fluxo completo dos dados, desde a ingestão dos arquivos da Anatel até a geração dos datasets analíticos |
| [vault_of_future_improvements.md](./vault_of_future_improvements.md) | Backlog técnico contendo melhorias futuras, evoluções arquiteturais, oportunidades de otimização e roadmap do projeto |

**Objetivo:** documentar a estrutura arquitetural do projeto, registrar padrões adotados e centralizar as decisões que orientam sua evolução técnica.

**Ordem sugerida:** iniciar por `medallion_architecture.md`, seguir para `data_flow.md` e `technology_stack.md`, consultar `project_standards.md` para entender as convenções do projeto e utilizar `vault_of_future_improvements.md` como referência para futuras evoluções.