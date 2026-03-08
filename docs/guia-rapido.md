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

O storage é local em layout Medallion:

- bronze: `data/bronze/city_id=<id>/yyyymm=<AAAAMM>/`
- silver/gold são opcionais e controlados por `diario_utils.storage`.

Use `--output-dir` para trocar a base (`data` por padrão).
