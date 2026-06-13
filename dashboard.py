"""
Web dashboard for the Sales Automation System.

A lightweight Flask app that renders the latest report in the browser:
KPI cards, the generated charts, and one-click downloads of the Excel and
PDF deliverables. Great for live demos and portfolio screenshots.

Run with:
    python main.py dashboard
    # or
    python dashboard.py
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta

from flask import (Flask, abort, redirect, render_template,
                   send_from_directory, url_for)

from config_loader import load_settings
from data_generator import SalesDataGenerator
from excel_exporter import ExcelReportExporter
from pdf_exporter import PDFReportExporter
from report_generator import SalesReportGenerator

settings = load_settings()
DATA_FOLDER = str(settings.data_folder)
REPORTS_FOLDER = str(settings.reports_folder)

app = Flask(__name__)


def _build_context() -> dict:
    """Generate the latest report and return template context."""
    generator = SalesReportGenerator(DATA_FOLDER, REPORTS_FOLDER)
    report = generator.generate_full_report()
    charts = [p.name for p in report["chart_paths"]]
    return {
        "daily": report["daily_stats"],
        "weekly": report["weekly_stats"],
        "charts": charts,
        "source": report["data_filename"],
        "generated_at": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
    }


@app.route("/")
def index():
    try:
        context = _build_context()
    except FileNotFoundError:
        # No data yet - guide the user instead of crashing.
        return render_template("empty.html")
    return render_template("dashboard.html", **context)


@app.route("/charts/<path:filename>")
def charts(filename: str):
    return send_from_directory(REPORTS_FOLDER, filename)


@app.route("/download/excel")
def download_excel():
    path = ExcelReportExporter(DATA_FOLDER, REPORTS_FOLDER).export()
    return send_from_directory(REPORTS_FOLDER, path.name, as_attachment=True)


@app.route("/download/pdf")
def download_pdf():
    path = PDFReportExporter(DATA_FOLDER, REPORTS_FOLDER).export()
    return send_from_directory(REPORTS_FOLDER, path.name, as_attachment=True)


@app.route("/regenerate", methods=["POST"])
def regenerate():
    """Generate a fresh week of sample data, then reload the dashboard."""
    generator = SalesDataGenerator()
    for i in range(7):
        date = datetime.now().date() - timedelta(days=i)
        df = generator.generate_daily_data(date, random.randint(30, 80))
        generator.save_data(df, folder=DATA_FOLDER)
    return redirect(url_for("index"))


def run(host: str = "127.0.0.1", port: int = 5000, debug: bool = False) -> None:
    """Entry point used by the CLI and by ``python dashboard.py``."""
    print(f"Dashboard running at http://{host}:{port}  (press Ctrl+C to stop)")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run()
