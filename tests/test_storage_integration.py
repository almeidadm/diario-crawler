"""Integração mínima com diario_utils.storage (medallion local)."""

from datetime import date
from pathlib import Path

from diario_contract.article.article import Article
from diario_contract.article.content import ArticleContent
from diario_contract.article.metadata import ArticleMetadata
from diario_contract.enums.content_type import ContentType
from diario_contract.gazette.edition import GazetteEdition
from diario_contract.gazette.metadata import GazetteMetadata
from diario_utils.storage import StorageClient, StorageConfig


def _sample_edition() -> GazetteEdition:
    metadata = GazetteMetadata(
        edition_id="ed1",
        publication_date="2026-03-01",
        edition_number=1,
        supplement=False,
        edition_type_id=1,
        edition_type_name="regular",
        pdf_url="http://example.com",
    )
    article = Article(
        metadata=ArticleMetadata(
            article_id="a1",
            edition_id="ed1",
            hierarchy_path=["root"],
            title="title",
            identifier="id-1",
            protocol=None,
        ),
        content=ArticleContent(raw_content="content", content_type=ContentType.TEXT),
    )
    return GazetteEdition(metadata=metadata, articles=[article])


def test_append_gazettes_creates_medallion_layout(tmp_path: Path):
    storage = StorageClient(StorageConfig(base_path=str(tmp_path), duckdb_path=":memory:"))
    edition = _sample_edition()

    storage.append_gazettes([edition], city_id="123")

    pub_date = edition.metadata.publication_date
    yyyymm = pub_date.strftime("%Y%m") if hasattr(pub_date, "strftime") else str(pub_date)[:7].replace("-", "")
    target_dir = tmp_path / "bronze" / "city_id=123" / f"yyyymm={yyyymm}"
    assert target_dir.exists(), "Diretório bronze/partition não foi criado"

    parquet_files = list(target_dir.glob("*.parquet"))
    assert parquet_files, "Arquivos Parquet não foram gerados no bronze layer"
