"""
Sales Automation System - Unified Command Line Interface
========================================================

A single entry point that exposes every part of the pipeline as a subcommand,
so the whole tool behaves like a real CLI application instead of a set of
loose scripts.

Examples
--------
    python main.py generate-data --days 7
    python main.py report
    python main.py email
    python main.py schedule --time 09:00

Run ``python main.py --help`` or ``python main.py <command> --help`` for
details on any command.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta

from config_loader import load_settings
from utils import setup_logging


def cmd_generate_data(args: argparse.Namespace) -> int:
    """Create sample sales CSV files for the last N days."""
    import random
    from data_generator import SalesDataGenerator

    generator = SalesDataGenerator()
    for i in range(args.days):
        date = datetime.now().date() - timedelta(days=i)
        records = random.randint(args.min_records, args.max_records)
        df = generator.generate_daily_data(date, records)
        generator.save_data(df, folder=args.data_folder)
    print(f"\nGenerated {args.days} day(s) of sample data in '{args.data_folder}/'.")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    """Generate charts and print summary statistics (no email)."""
    from report_generator import SalesReportGenerator

    generator = SalesReportGenerator(args.data_folder, args.reports_folder)
    report_data = generator.generate_full_report()

    print("\nDAILY STATISTICS")
    print("-" * 40)
    for key, value in report_data["daily_stats"].items():
        print(f"  {key:<22}: {value}")
    print(f"\nGenerated {len(report_data['chart_paths'])} charts in '{args.reports_folder}/'.")
    return 0


def cmd_email(args: argparse.Namespace) -> int:
    """Generate a report and email it to the configured recipients."""
    from email_automation import EmailAutomator

    automator = EmailAutomator(args.config)
    if not automator.settings.email.is_configured:
        print(
            "Email is not configured. Create a .env file (see .env.example) or a "
            "config.ini with SENDER_EMAIL, SENDER_PASSWORD and RECIPIENT_EMAIL."
        )
        return 1
    automator.generate_and_send_report()
    return 0


def cmd_excel(args: argparse.Namespace) -> int:
    """Export a styled multi-sheet Excel workbook with native charts."""
    from excel_exporter import ExcelReportExporter

    exporter = ExcelReportExporter(args.data_folder, args.reports_folder)
    exporter.export(args.output)
    return 0


def cmd_pdf(args: argparse.Namespace) -> int:
    """Export a print-ready PDF report with KPIs and charts."""
    from pdf_exporter import PDFReportExporter

    exporter = PDFReportExporter(args.data_folder, args.reports_folder)
    exporter.export(args.output)
    return 0


def cmd_dashboard(args: argparse.Namespace) -> int:
    """Launch the Flask web dashboard."""
    from dashboard import run

    run(host=args.host, port=args.port, debug=args.debug)
    return 0


def cmd_schedule(args: argparse.Namespace) -> int:
    """Run the email report automatically every day at a given time."""
    import time
    import schedule
    from email_automation import EmailAutomator

    automator = EmailAutomator(args.config)
    schedule.every().day.at(args.time).do(automator.generate_and_send_report)
    print(f"Scheduled daily reports at {args.time}. Press Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Construct the top-level argument parser and all subcommands."""
    parser = argparse.ArgumentParser(
        prog="sales-automation",
        description="Automated sales reporting toolkit (data, charts, Excel, PDF, email).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--config", default="config.ini",
                        help="Path to config.ini (default: config.ini).")

    sub = parser.add_subparsers(dest="command", required=True)

    # generate-data
    p_gen = sub.add_parser("generate-data", help="Create sample sales CSV data.")
    p_gen.add_argument("--days", type=int, default=7, help="Number of days to generate (default: 7).")
    p_gen.add_argument("--min-records", type=int, default=30, help="Minimum records per day.")
    p_gen.add_argument("--max-records", type=int, default=80, help="Maximum records per day.")
    p_gen.add_argument("--data-folder", default="data", help="Output folder for CSV files.")
    p_gen.set_defaults(func=cmd_generate_data)

    # report
    p_rep = sub.add_parser("report", help="Generate charts and print statistics.")
    p_rep.add_argument("--data-folder", default="data", help="Folder containing CSV data.")
    p_rep.add_argument("--reports-folder", default="reports", help="Folder for generated charts.")
    p_rep.set_defaults(func=cmd_report)

    # email
    p_email = sub.add_parser("email", help="Generate a report and email it.")
    p_email.set_defaults(func=cmd_email)

    # excel
    p_excel = sub.add_parser("excel", help="Export a styled Excel workbook with charts.")
    p_excel.add_argument("--data-folder", default="data", help="Folder containing CSV data.")
    p_excel.add_argument("--reports-folder", default="reports", help="Folder for the workbook.")
    p_excel.add_argument("--output", default=None, help="Output filename (default: dated name).")
    p_excel.set_defaults(func=cmd_excel)

    # pdf
    p_pdf = sub.add_parser("pdf", help="Export a print-ready PDF report.")
    p_pdf.add_argument("--data-folder", default="data", help="Folder containing CSV data.")
    p_pdf.add_argument("--reports-folder", default="reports", help="Folder for the PDF.")
    p_pdf.add_argument("--output", default=None, help="Output filename (default: dated name).")
    p_pdf.set_defaults(func=cmd_pdf)

    # dashboard
    p_dash = sub.add_parser("dashboard", help="Launch the web dashboard in the browser.")
    p_dash.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1).")
    p_dash.add_argument("--port", type=int, default=5000, help="Port to bind (default: 5000).")
    p_dash.add_argument("--debug", action="store_true", help="Enable Flask debug mode.")
    p_dash.set_defaults(func=cmd_dashboard)

    # schedule
    p_sched = sub.add_parser("schedule", help="Send the email report daily on a schedule.")
    p_sched.add_argument("--time", default="09:00", help="Daily run time HH:MM (default: 09:00).")
    p_sched.set_defaults(func=cmd_schedule)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Initialise logging once for the whole CLI run.
    settings = load_settings(getattr(args, "config", "config.ini"))
    setup_logging(settings.logs_folder, settings.log_level)

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
