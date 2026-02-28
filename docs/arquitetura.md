# Arquitetura

## Objetivo

Explicar como o crawler e estruturado e como os dados percorrem o sistema.

## Fluxo de dados

1. O crawler gera URLs de metadados por data
2. Baixa metadados JSON das edicoes
3. Baixa HTML de estrutura de cada edicao
4. Parseia a estrutura para obter artigos
5. Baixa o conteudo dos artigos
6. Agrega edicoes e artigos em modelos do contrato
7. Persiste em Parquet e blobs de conteudo quando necessario

## Componentes principais

- CLI e orquestracao: `src/diario_crawler/cli/run_crawler.py`
- Orquestrador: `src/diario_crawler/core/crawler.py`
- Clientes HTTP: `src/diario_crawler/core/clients.py`
- Parsers: `src/diario_crawler/parsers/structure.py`, `src/diario_crawler/parsers/metadata.py`, `src/diario_crawler/parsers/content.py`
- Processamento e agregacao: `src/diario_crawler/processors/aggregator.py`
- Storage Parquet e DuckDB: `src/diario_crawler/storage/parquet.py`
- Backends de storage: `src/diario_crawler/storage/local.py`, `src/diario_crawler/storage/minio.py`
- Configuracoes por municipio: `src/diario_crawler/crawler_configs/*.py`

## Contrato de dados

Os modelos seguem o repositorio `diario-contract` na versao `v1.1.1`. As entidades centrais sao `GazetteEdition`, `GazetteMetadata` e `ArticleMetadata`.

## Formato de saida

Os dados sao gravados em Parquet com estes caminhos base.

- `gazettes/batch_YYYYMMDD_HHMMSS.parquet`
- `articles/batch_YYYYMMDD_HHMMSS.parquet`
- `relationships/batch_YYYYMMDD_HHMMSS.parquet`
- `content/xx/yy/<hash>.bin` para conteudos grandes
