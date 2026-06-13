"""
Centralized configuration loader for the Sales Automation System.

Loading priority (highest first):
    1. Environment variables (optionally provided via a local ``.env`` file)
    2. Values defined in ``config.ini``
    3. Built-in safe defaults

This layered approach keeps secrets (SMTP passwords, recipient lists) out of
source control while still allowing a simple ``config.ini`` for local testing.
"""

from __future__ import annotations

import configparser
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

try:
    # python-dotenv is optional. If it is installed we automatically load a
    # local .env file so environment variables can be defined per-project.
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover - dotenv is a convenience, not required
    pass


@dataclass
class EmailSettings:
    """SMTP / email related configuration."""

    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = ""
    sender_password: str = ""
    recipients: List[str] = field(default_factory=list)

    @property
    def is_configured(self) -> bool:
        """True only when we have enough information to attempt a send."""
        return bool(self.sender_email and self.sender_password and self.recipients)


@dataclass
class AppSettings:
    """Top-level application settings."""

    email: EmailSettings
    data_folder: Path = Path("data")
    reports_folder: Path = Path("reports")
    logs_folder: Path = Path("logs")
    report_frequency: str = "daily"
    chart_style: str = "seaborn-v0_8"
    log_level: str = "INFO"


def _split_recipients(raw: str) -> List[str]:
    """Turn a comma/semicolon separated string into a clean list of emails."""
    if not raw:
        return []
    separators = raw.replace(";", ",")
    return [item.strip() for item in separators.split(",") if item.strip()]


def _read_ini(config_file: str) -> configparser.ConfigParser:
    """Read config.ini if it exists. Missing file is not an error here."""
    parser = configparser.ConfigParser()
    if Path(config_file).exists():
        parser.read(config_file)
    return parser


def _get(parser: configparser.ConfigParser, section: str, key: str, fallback: str = "") -> str:
    """Safe getter that never raises for missing section/key."""
    try:
        return parser.get(section, key, fallback=fallback)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return fallback


def load_settings(config_file: str = "config.ini") -> AppSettings:
    """
    Build an :class:`AppSettings` object from environment variables and/or
    ``config.ini``. Environment variables always win so production deployments
    can inject secrets without touching files on disk.
    """
    ini = _read_ini(config_file)

    email = EmailSettings(
        smtp_server=os.getenv("SMTP_SERVER", _get(ini, "EMAIL", "smtp_server", "smtp.gmail.com")),
        smtp_port=int(os.getenv("SMTP_PORT", _get(ini, "EMAIL", "smtp_port", "587") or "587")),
        sender_email=os.getenv("SENDER_EMAIL", _get(ini, "EMAIL", "sender_email", "")),
        sender_password=os.getenv("SENDER_PASSWORD", _get(ini, "EMAIL", "sender_password", "")),
        recipients=_split_recipients(
            os.getenv("RECIPIENT_EMAIL", _get(ini, "EMAIL", "recipient_email", ""))
        ),
    )

    return AppSettings(
        email=email,
        data_folder=Path(os.getenv("DATA_FOLDER", _get(ini, "PATHS", "data_folder", "data"))),
        reports_folder=Path(os.getenv("REPORTS_FOLDER", _get(ini, "PATHS", "reports_folder", "reports"))),
        logs_folder=Path(os.getenv("LOGS_FOLDER", _get(ini, "PATHS", "logs_folder", "logs"))),
        report_frequency=os.getenv("REPORT_FREQUENCY", _get(ini, "SETTINGS", "report_frequency", "daily")),
        chart_style=os.getenv("CHART_STYLE", _get(ini, "SETTINGS", "chart_style", "seaborn-v0_8")),
        log_level=os.getenv("LOG_LEVEL", _get(ini, "SETTINGS", "log_level", "INFO")),
    )


if __name__ == "__main__":
    # Quick manual check: print the resolved configuration without secrets.
    settings = load_settings()
    print("Resolved configuration:")
    print(f"  SMTP server : {settings.email.smtp_server}:{settings.email.smtp_port}")
    print(f"  Sender      : {settings.email.sender_email or '(not set)'}")
    print(f"  Recipients  : {settings.email.recipients or '(none)'}")
    print(f"  Email ready : {settings.email.is_configured}")
    print(f"  Data folder : {settings.data_folder}")
    print(f"  Reports     : {settings.reports_folder}")
    print(f"  Logs        : {settings.logs_folder}")
    print(f"  Log level   : {settings.log_level}")
