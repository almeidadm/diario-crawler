"""Logging helper that delegates to diario_utils.logger when available."""

from __future__ import annotations

import logging
from typing import Any

try:
    from diario_utils import logger as du_logger
except Exception:  # pragma: no cover - fallback for missing dependency
    du_logger = None  # type: ignore


def setup_logging(level: str = "INFO", log_file: str | None = None) -> None:
    """
    Configure application logging.

    Prefers diario_utils.logger defaults (structlog-friendly). Falls back to
    basic logging when the upstream helper is unavailable.
    """
    if du_logger:
        configure = getattr(du_logger, "configure", None) or getattr(
            du_logger, "configure_logging", None
        )
        if configure:
            try:
                configure(level=level, log_file=log_file, service_name="diario-crawler")
                return
            except Exception:
                # If diario_utils is present but configuration fails, drop to fallback.
                pass

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def get_logger(name: str) -> Any:
    """Return a structlog/logger instance."""
    if du_logger and hasattr(du_logger, "get_logger"):
        try:
            return du_logger.get_logger(name)
        except Exception:
            pass
    return logging.getLogger(name)


__all__ = ["setup_logging", "get_logger"]
