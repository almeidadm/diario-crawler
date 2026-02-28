# Desenvolvimento

## Objetivo

Padronizar o setup local e as tarefas de qualidade.

## Ambiente local

Instalar dependencias de runtime:

```bash
uv sync
```

Instalar dependencias de desenvolvimento:

```bash
uv sync --group dev
```

## Comandos de qualidade

Formatacao:

```bash
task format
```

Lint:

```bash
task lint
```

Checagem completa:

```bash
task check
```

Testes:

```bash
task test
```

## Adicionar um novo municipio

1. Crie uma configuracao em `src/diario_crawler/crawler_configs/` baseada em `base.py`.
2. Registre o novo crawler em `AVAILABLE_CRAWLERS` no arquivo `src/diario_crawler/cli/run_crawler.py`.
3. Adicione testes ou ajuste cassetes VCR em `tests/fixtures/vcr_cassettes/`.

## Atualizar o contrato de dados

1. Atualize a referencia em `pyproject.toml`.
2. Atualize o lockfile `uv.lock`.
3. Ajuste parsers e processamento se o contrato mudou.
