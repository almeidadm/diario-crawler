# Operacao e configuracao

## Objetivo

Documentar os parametros da CLI e as variaveis de ambiente suportadas.

## Parametros principais

Tabela de parametros mais usados.

| Parametro | Descricao | Exemplo |
| --- | --- | --- |
| `--municipality` | Seleciona o crawler do municipio | `--municipality sp_sao_jose_dos_campos` |
| `--days` | Numero de dias retroativos | `--days 7` |
| `--start-date` | Data inicial | `--start-date 2025-01-01` |
| `--end-date` | Data final | `--end-date 2025-01-31` |
| `--batch-size` | Tamanho do lote | `--batch-size 30` |
| `--max-concurrent` | Concorrencia de requisicoes | `--max-concurrent 10` |
| `--output-dir` | Diretorio base da camada bronze | `--output-dir data` |

## DuckDB

| Parametro | Descricao | Exemplo |
| --- | --- | --- |
| `--duckdb-path` | Caminho do arquivo DuckDB | `--duckdb-path data/diarios.duckdb` |

## Logs e utilitarios

| Parametro | Descricao |
| --- | --- |
| `--log-level` | Nivel de log: DEBUG, INFO, WARNING, ERROR |
| `--log-file` | Arquivo de log | 
| `--list-crawlers` | Lista crawlers disponiveis |
| `--dry-run` | Simula execucao sem salvar dados |

## Variaveis de ambiente

As variaveis abaixo definem valores padrao para a CLI.

| Variavel | Descricao | Padrao |
| --- | --- | --- |
| `DUCKDB_PATH` | Caminho DuckDB | vazio (usa in-memory) |
