"""
Shared helper utilities for the Sales Automation System.

Keeping cross-cutting concerns (logging setup, folder creation) in one place
avoids duplicated boilerplate across the data, report and email modules.
"""

from __future__ import annotations

import logging
from pathlib import Path


def ensure_folder(folder: Path | str) -> Path:
    """Create a folder (and parents) if needed and return it as a Path."""
    path = Path(folder)
    path.mkdir(parents=True, exist_ok=True)
    return path


def setup_logging(logs_folder: Path | str = "logs", log_level: str = "INFO",
                  log_file: str = "automation.log") -> logging.Logger:
    """
    Configure root logging to write both to a file and the console.

    Returns a logger ready to use. Safe to call multiple times: existing
    handlers are cleared so logs are not duplicated.
    """
    folder = ensure_folder(logs_folder)
    level = getattr(logging, str(log_level).upper(), logging.INFO)

    root = logging.getLogger()
    root.setLevel(level)

    # Avoid duplicate handlers when called more than once (e.g. via the CLI).
    for handler in list(root.handlers):
        root.removeHandler(handler)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    file_handler = logging.FileHandler(folder / log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    return logging.getLogger("sales_automation")
