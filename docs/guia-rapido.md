# Guia rapido

## Objetivo

Rodar o crawler com o minimo de configuracao.

## Requisitos

- Python 3.12 ou 3.13
- Acesso aos sites dos diarios

## Instalar dependencias

Usando uv:

```bash
uv sync
```

Usando pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Primeira execucao

Listar municipios disponiveis:

```bash
cli --list-crawlers
```

Executar ultimos 7 dias para Sao Jose dos Campos:

```bash
cli --municipality sp_sao_jose_dos_campos --days 7
```

Executar intervalo fechado:

```bash
cli --municipality rj_rio_de_janeiro --start-date 2025-01-01 --end-date 2025-01-31
```

## Onde os dados ficam

Por padrao, os arquivos ficam em `data/raw` com particoes por dia. Para mudar o destino, use `--output-dir`.

## Quando usar MinIO ou S3

Se quiser armazenar em MinIO ou S3, use `--storage minio` ou `--storage s3` e informe as variaveis de ambiente listadas em `docs/operacao.md`.
