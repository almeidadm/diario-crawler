# Changelog

## [2.0.0] - 2026-03-08

### Breaking Changes
- Armazenamento migrou para `diario_utils.storage` (layout medallion local). Removidos backends internos `local`, `minio` e `ParquetStorage`.
- CLI simplificada: removidos flags de MinIO/S3, particionamento e estatísticas; apenas `--output-dir` e `--duckdb-path` controlam o storage local.

### Added
- Dependência `diario-utils` v1.3.0 (git tag) para storage e logging estruturado.
- Teste de integração `test_storage_integration.py` verificando criação do layout bronze.

### Changed
- Logging agora delega para `diario_utils.logger` com fallback simples.
- `GazetteCrawler` passa a persistir via `StorageClient.append_gazettes`.
- Documentação (README, arquitetura, operação) atualizada para refletir o storage medallion local.
- Dependências alinhadas: `diario-contract` v1.2.0 e `polars` 0.20.x para compatibilidade com `diario-utils`.

### Removed
- Pacote `diario_crawler.storage` e suporte a MinIO/S3 na CLI.

## [1.0.0] - 2026-02-27

### Breaking Changes
- Parquet schema: `edition_number`, `edition_type_id`, `total_articles` mudaram de `int32` para `int64` em `src/diario_crawler/storage/base.py`.

### Changed
- Dependencia `diario-contract` atualizada de `v1.0.3` para `v1.1.2` (ver `pyproject.toml` e `uv.lock`).

### Documentation
- Adicionados documentos: `docs/README.md`, `docs/visao-geral.md`, `docs/glossario.md`, `docs/guia-rapido.md`, `docs/operacao.md`, `docs/arquitetura.md`, `docs/desenvolvimento.md`, `docs/versioning.md`.
