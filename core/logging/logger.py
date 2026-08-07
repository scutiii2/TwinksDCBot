from __future__ import annotations
import logging
from pathlib import Path


def setup_logging(log_path: Path) -> None:
    log_path.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)-8s] %(name)s: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    file = logging.FileHandler(
        log_path / "twinks.log",
        encoding="utf-8",
    )
    file.setFormatter(formatter)
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            console,
            file,
        ],
    )