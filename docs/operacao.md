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
| `--storage` | Tipo de storage | `--storage local` |
| `--output-dir` | Diretorio local de saida | `--output-dir data/raw` |
| `--partition-by` | Particionamento | `--partition-by day` |

## Parametros MinIO e S3

| Parametro | Descricao | Exemplo |
| --- | --- | --- |
| `--minio-endpoint` | Endpoint MinIO ou S3 | `--minio-endpoint localhost:9000` |
| `--minio-bucket` | Bucket | `--minio-bucket gazettes` |
| `--minio-access-key` | Access key | `--minio-access-key minioadmin` |
| `--minio-secret-key` | Secret key | `--minio-secret-key minioadmin` |
| `--minio-secure` | Usa HTTPS | `--minio-secure` |
| `--minio-region` | Regiao | `--minio-region us-east-1` |
| `--minio-prefix` | Prefixo de chaves | `--minio-prefix diarios` |

## DuckDB

| Parametro | Descricao | Exemplo |
| --- | --- | --- |
| `--enable-duckdb` | Habilita consultas locais | `--enable-duckdb` |
| `--duckdb-path` | Caminho do arquivo DuckDB | `--duckdb-path data/diarios.duckdb` |

## Logs e utilitarios

| Parametro | Descricao |
| --- | --- |
| `--log-level` | Nivel de log: DEBUG, INFO, WARNING, ERROR |
| `--log-file` | Arquivo de log | 
| `--list-crawlers` | Lista crawlers disponiveis |
| `--migrate-to-minio` | Migra dados locais para MinIO |
| `--show-stats` | Exibe estatisticas do storage |
| `--dry-run` | Simula execucao sem salvar dados |

## Variaveis de ambiente

As variaveis abaixo definem valores padrao para a CLI.

| Variavel | Descricao | Padrao |
| --- | --- | --- |
| `STORAGE_TYPE` | Tipo de storage | `local` |
| `STORAGE_PATH` | Diretorio local | `data/raw` |
| `MINIO_ENDPOINT` | Endpoint MinIO | `localhost:9000` |
| `MINIO_BUCKET` | Bucket | `gazettes` |
| `MINIO_ACCESS_KEY` | Access key | `minioadmin` |
| `MINIO_SECRET_KEY` | Secret key | `minioadmin` |
| `MINIO_SECURE` | HTTPS no MinIO | `false` |
| `MINIO_REGION` | Regiao | `us-east-1` |
| `MINIO_PREFIX` | Prefixo de chaves | vazio |
| `ENABLE_DUCKDB` | Habilita DuckDB | `true` |
| `DUCKDB_PATH` | Caminho DuckDB | vazio |
