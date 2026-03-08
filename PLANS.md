
# Refact diario-crawler to integrate diario-utils v1.3.0

## Purpose / Big Picture

Este projeto de TCC em Data Science e Analytics propõe um sistema RAG voltado a diários oficiais municipais. O foco é entregar uma pipeline replicável, aberta e pronta para evoluir em produção, demonstrando impacto profissional e acadêmico. O MVP contemplará coleta, tratamento, indexação e um chatbot de consulta, com documentação completa da arquitetura e decisões de pesquisa.O projeto visa construir um framework. Veja os objetivos do TCC:
  - Construir uma pipeline completa e replicável de RAG a partir dos diários oficiais disponíveis na plataforma.
  - Avaliar métodos de chunking adequados ao domínio.
  - Enriquecer metadados com regras e NER específicas do contexto municipal.
  - Comparar modelos de embeddings (tamanho, domínio jurídico/pt-BR) e suas representações.
  - Testar pelo menos duas estratégias de retrieval (por exemplo, híbrido BM25+vectores e denso puro) e seus impactos.
  - Entregar um chatbot funcional para experimentação em produção.

  - **Organização em repositórios**
    - `diario-crawler`: webscraping da plataforma.
    - `diario-parser`: parsing, chunking, enriquecimento de metadados, aplicação de NER.
    - `diario-embedding`: geração de embeddings com múltiplos modelos.
    - `diario-retrieval`: definição e testes das estratégias de busca sobre vector DB.
    - `diario-chatbot`: monólito fullstack integrando retrieval para atendimento.
    - Possíveis apoios: `diario-contract` (modelos Pydantic compartilhados), `diario-utils` (funções comuns), `diario-core` (orquestração e `docker-compose` para pipeline e chatbot).

Estamos trabalhando no repositório diario-crawler. Este repositório foi o primeiro módulo a ser implementado e mais crítico do sistema atualmente. Ele é responsável pela coleta dos diários oficiais no formato diario_contract.gazette.GazetteEdition. Atualmente o projeto diario-crawler implementa o prórpio método de interação com o processo de armazenamento de dados através do sub módulo diario-crawler.storage. Com o desenvolvimento dos novos projetos a decisão arquietetural de utilizar arquitetura medallion surgiu e foi feita uma nova implementação do módulo de storage, mas agora salva em diario-utils.storage. A tarefa atual é refatorar o projeto diario-crawler para integrar o novo submódulo diario-utils.storage e diario-utils.logger para o projeto atual. 

## Progress

Examples:
- [x] (2025-10-01 13:00Z) Example completed step.
- [ ] Example incomplete step.
- [ ] Example partially completed step (completed: X; remaining: Y).

Progress
- [x] (2026-03-08 15:20 UTC-3) Update the project dependencies to include the latest diario-utils v1.3.0
- [ ] Install de updated project to download the included lib
- [x] (2026-03-08 15:22 UTC-3) Verify the diario-crawler.storage usage cases and replace it for the diario-utils.storage
- [x] (2026-03-08 15:22 UTC-3) Verify the diario-crawler.utils.logging usage cases and replace it for the diario-utils.logging
- [ ] Update the pytests config and tests and execute it; Verify the output and fix all needs
- [x] (2026-03-08 15:30 UTC-3) Refact the docs/ to mirror the current state of repository
- [x] (2026-03-08 15:35 UTC-3) Update CHANGELOG.md and README.md files;
- [x] (2026-03-08 15:24 UTC-3) Delete unused submodules (expected diario-crawler.storage and diario-crawler.utils.logging)
- [ ] Create commits and new tags for the modifications
- [ ] Push to main and the latest tag


Use timestamps to measure rates of progress. 

## Surprises & Discoveries

None at this moment
- Observation: …
  Evidence: …

## Decision Log

- Decision: Integrate the diario-utils.storage v1.3.0 to the diario-crawler
  Rationale: 
    Minimizar uso de disco com formatos colunares comprimidos e deduplicação. Garantir reprodutibilidade e trilha de auditoria (tags de versão de crawler/parser/embedding). Suportar consultas leves (amostras, contagens) e intensas (scans para embedding/retrieval offline). Manter API única, isolando detalhes de storage para futura migração cloud (S3/GCS + catalog/iceberg/delta).
  Date/Author: 08/03/2026, Diego Miranda
