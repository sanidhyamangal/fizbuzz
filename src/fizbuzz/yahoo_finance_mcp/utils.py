import logging
import typing as t

from rich.console import Console
from rich.logging import RichHandler


def configure_logging(
    level: t.Literal["DEBUG", "INFO", "WARN", "CRITICAL", "ERROR"] = "INFO",
):
    handlers: list[logging.Handler] = []

    handlers.append(
        RichHandler(level=level, console=Console(stderr=True), rich_tracebacks=True)
    )

    if not handlers:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(level=level, format="%(message)s", handlers=handlers)
