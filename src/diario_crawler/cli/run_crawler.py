"""Script CLI principal para execução do crawler do Diário Oficial."""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Type

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from diario_utils.storage import StorageClient, StorageConfig

from diario_crawler.core import GazetteCrawler
from diario_crawler.crawler_configs.base import BaseCrawlerConfig
from diario_crawler.utils import get_logger, setup_logging

logger = get_logger(__name__)
console = Console()


# Registro de crawlers disponíveis
AVAILABLE_CRAWLERS = {
    "sp_sao_jose_dos_campos": "diario_crawler.crawler_configs.sp_sao_jose_dos_campos.SpSaoJoseDosCampos",
    "rj_rio_de_janeiro": "diario_crawler.crawler_configs.rj_rio_de_janeiro.RjRioDeJaneiro",
    "es_associacao_municipios": "diario_crawler.crawler_configs.es_associacao_municipios.EsAssociacaoMunicipios",
    "ro_jaru": "diario_crawler.crawler_configs.ro_jaru.RoJaru",
    "ms_corumba": "diario_crawler.crawler_configs.ms_corumba.MsCorumba",
}


class DryRunStorage:
    """Storage no-op usado para modo dry-run."""

    def append_gazettes(self, editions, city_id: str | None = None):  # pragma: no cover - trivial
        logger.info("Dry-run: dados não serão persistidos", city_id=city_id)
        return {"editions": len(editions), "city_id": city_id}


def load_crawler_config(municipality: str) -> Type[BaseCrawlerConfig]:
    """Carrega dinamicamente a configuração do crawler para o município."""
    if municipality not in AVAILABLE_CRAWLERS:
        available = ", ".join(AVAILABLE_CRAWLERS.keys())
        raise ValueError(
            f"Município '{municipality}' não encontrado. Disponíveis: {available}"
        )

    module_path = AVAILABLE_CRAWLERS[municipality]
    module_name, class_name = module_path.rsplit(".", 1)

    try:
        import importlib

        module = importlib.import_module(module_name)
        config_class = getattr(module, class_name)
        return config_class
    except (ImportError, AttributeError) as exc:
        raise ImportError(f"Erro ao carregar configuração para '{municipality}': {exc}")


def list_available_crawlers():
    """Lista crawlers disponíveis."""
    table = Table(title="🏛️  Crawlers Disponíveis", show_header=True)
    table.add_column("ID", style="cyan", width=30)
    table.add_column("Classe", style="green")

    for crawler_id, class_path in AVAILABLE_CRAWLERS.items():
        class_name = class_path.split(".")[-1]
        table.add_row(crawler_id, class_name)

    console.print(table)
    console.print()


def parse_arguments():
    """Parse argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Crawler de Diários Oficiais Multi-Município",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Listar crawlers disponíveis
  cli --list-crawlers
  
  # Crawler de São José dos Campos (últimos 7 dias)
  cli --municipality sp_sao_jose_dos_campos --days 7
  
  # Crawler ES (com output customizado)
  cli --municipality es_associacao_municipios --days 30 --output-dir data
        """,
    )

    parser.add_argument(
        "--municipality",
        "--m",
        type=str,
        choices=list(AVAILABLE_CRAWLERS.keys()),
        help="Município/região para crawler (obrigatório)",
    )

    parser.add_argument(
        "--list-crawlers",
        action="store_true",
        help="Listar crawlers disponíveis e sair",
    )

    date_group = parser.add_argument_group("Configurações de Data")
    date_group.add_argument(
        "--start-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        help="Data de início (YYYY-MM-DD)",
    )
    date_group.add_argument(
        "--end-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        help="Data de fim (YYYY-MM-DD)",
    )
    date_group.add_argument(
        "--days",
        type=int,
        default=7,
        help="Número de dias para retroceder a partir de hoje (padrão: 7)",
    )

    config_group = parser.add_argument_group("Configurações do Crawler")
    config_group.add_argument(
        "--batch-size",
        type=int,
        default=30,
        help="Tamanho do lote de processamento (padrão: 30)",
    )
    config_group.add_argument(
        "--max-concurrent",
        type=int,
        default=10,
        help="Número máximo de requisições concorrentes (padrão: 10)",
    )

    storage_group = parser.add_argument_group("Configurações de Storage")
    storage_group.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data"),
        help="Diretório base para o medallion local (padrão: data)",
    )
    storage_group.add_argument(
        "--duckdb-path",
        type=Path,
        default=None,
        help="Caminho opcional para o catálogo DuckDB (padrão: in-memory)",
    )

    log_group = parser.add_argument_group("Configurações de Log")
    log_group.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Nível de logging (padrão: INFO)",
    )
    log_group.add_argument(
        "--log-file", type=Path, help="Arquivo para salvar logs (opcional)"
    )

    util_group = parser.add_argument_group("Utilitários")
    util_group.add_argument(
        "--dry-run", action="store_true", help="Simular execução sem salvar dados"
    )

    return parser.parse_args()


def validate_arguments(args) -> bool:
    """Valida os argumentos fornecidos."""
    errors = []

    if args.list_crawlers:
        return True

    if not args.municipality:
        errors.append(
            "Argumento --municipality é obrigatório. Use --list-crawlers para ver opções."
        )
        return False

    try:
        ConfigClass = load_crawler_config(args.municipality)
        min_date = ConfigClass.DEFAULT_START_DATE
    except Exception as exc:  # pragma: no cover - defensive
        errors.append(f"Erro ao carregar configuração: {exc}")
        return False

    if args.start_date and args.end_date and args.start_date > args.end_date:
        errors.append("Data inicial não pode ser maior que data final")

    if args.start_date and args.start_date < min_date:
        errors.append(
            f"Data inicial ({args.start_date}) não pode ser anterior a {min_date} "
            f"para {args.municipality}"
        )

    if args.batch_size <= 0:
        errors.append("Batch size deve ser positivo")

    if args.max_concurrent <= 0:
        errors.append("Número de requisições concorrentes deve ser positivo")

    if args.days < 0:
        errors.append("Número de dias deve ser não-negativo")

    if errors:
        for error in errors:
            logger.error(f"❌ {error}")
        return False

    return True


def calculate_dates(args) -> tuple[date, date]:
    """Calcula as datas de início e fim baseado nos argumentos."""
    end_date = args.end_date or date.today()

    if args.start_date:
        start_date = args.start_date
    elif args.days > 0:
        start_date = end_date - timedelta(days=args.days - 1)
    else:
        start_date = end_date

    return start_date, end_date


def create_storage(args) -> StorageClient:
    """Cria instância do StorageClient (medallion local)."""
    config = StorageConfig(
        base_path=str(args.output_dir),
        duckdb_path=str(args.duckdb_path) if args.duckdb_path else ":memory:",
    )
    return StorageClient(config)


def display_config_summary(
    args, config_class: Type[BaseCrawlerConfig], start_date: date, end_date: date
):
    """Exibe resumo da configuração usando Rich."""
    table = Table(title="⚙️  Configuração do Crawler", show_header=False)
    table.add_column("Parâmetro", style="cyan", width=25)
    table.add_column("Valor", style="green")

    table.add_row("🏛️  Município", args.municipality)
    table.add_row("🌐 Domínio", config_class.DOMAIN_URL)
    table.add_row("📅 Data mínima", str(config_class.DEFAULT_START_DATE))

    table.add_row("", "")
    table.add_row("📅 Período", f"{start_date} até {end_date}")
    total_days = (end_date - start_date).days + 1
    table.add_row("📊 Total de dias", str(total_days))

    table.add_row("", "")
    table.add_row("📦 Batch size", str(args.batch_size))
    table.add_row("⚡ Concorrência", str(args.max_concurrent))

    table.add_row("", "")
    table.add_row("💾 Storage base", str(args.output_dir))
    table.add_row("🦆 DuckDB", str(args.duckdb_path or ':memory:'))

    console.print(table)
    console.print()


def display_results(stats: dict, execution_time: float):
    """Exibe resultados da execução usando Rich."""
    panel = Panel.fit(
        f"""
[bold green]✅ EXECUÇÃO CONCLUÍDA[/bold green]

[cyan]Estatísticas:[/cyan]
  • Edições processadas: [bold]{stats.get('editions', 0)}[/bold]
  • Artigos processados: [bold]{stats.get('articles', 0)}[/bold]
  • Batch ID: [dim]{stats.get('batch_id', 'N/A')}[/dim]

[cyan]Performance:[/cyan]
  • Tempo total: [bold]{execution_time:.2f}s[/bold]
  • Taxa edições: [bold]{stats.get('editions', 0)/execution_time:.2f}[/bold] ed/s
  • Taxa artigos: [bold]{stats.get('articles', 0)/execution_time:.2f}[/bold] art/s

[cyan]Timestamp:[/cyan]
  • Início: [dim]{stats.get('start_time', 'N/A')}[/dim]
  • Fim: [dim]{stats.get('end_time', 'N/A')}[/dim]
        """,
        title="📊 Resultados",
        border_style="green",
    )
    console.print(panel)


async def cli():
    """Função principal."""
    args = parse_arguments()

    setup_logging(level=args.log_level, log_file=str(args.log_file) if args.log_file else None)

    console.print(
        Panel.fit(
            "[bold blue]Crawler de Diários Oficiais Multi-Município[/bold blue]\n"
            "[dim]Sistema unificado de coleta de publicações oficiais[/dim]",
            border_style="blue",
        )
    )
    console.print()

    if args.list_crawlers:
        list_available_crawlers()
        return

    if not validate_arguments(args):
        sys.exit(1)

    try:
        ConfigClass = load_crawler_config(args.municipality)
        logger.info(f"✅ Configuração carregada: {ConfigClass.NAME}")
    except Exception as exc:
        logger.error(f"❌ Erro ao carregar configuração: {exc}")
        sys.exit(1)

    try:
        storage = create_storage(args)
    except Exception as exc:
        logger.error(f"❌ Erro ao criar storage: {exc}")
        sys.exit(1)

    start_date, end_date = calculate_dates(args)
    display_config_summary(args, ConfigClass, start_date, end_date)

    if args.dry_run:
        console.print("[yellow]⚠️  Modo DRY-RUN: dados não serão salvos[/yellow]\n")

    try:
        config = ConfigClass(
            start_date=start_date,
            end_date=end_date,
            batch_size=args.batch_size,
            max_concurrent=args.max_concurrent,
        )

        crawler = GazetteCrawler(
            config=config, storage=storage if not args.dry_run else DryRunStorage()
        )

        console.print(
            f"[bold green]🚀 Iniciando crawler para {ConfigClass.NAME}...[/bold green]\n"
        )

        start_time = datetime.now()
        n_editions, n_articles = await crawler.run()
        end_time = datetime.now()

        execution_time = (end_time - start_time).total_seconds()

        stats = {
            "editions": n_editions,
            "articles": n_articles,
            "batch_id": "DRY-RUN"
            if args.dry_run
            else f"batch_{start_time.strftime('%Y%m%d_%H%M%S')}",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "municipality": args.municipality,
        }

        display_results(stats, execution_time)

    except KeyboardInterrupt:  # pragma: no cover - CLI path
        console.print("\n[yellow]⚠️  Execução interrompida pelo usuário[/yellow]")
        sys.exit(1)
    except Exception as exc:
        logger.exception(f"❌ Erro durante execução: {exc}")
        console.print(f"\n[bold red]❌ Erro: {exc}[/bold red]")
        sys.exit(1)


def main():
    asyncio.run(cli())


if __name__ == "__main__":  # pragma: no cover
    main()
