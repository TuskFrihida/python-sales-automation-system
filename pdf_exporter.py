"""
PDF report automation.

Combines the KPI summary and the generated chart images into a single,
print-ready PDF document using fpdf2. This is the classic "executive
one-pager" that gets attached to emails or shared with stakeholders.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fpdf import FPDF

from report_generator import SalesReportGenerator
from utils import ensure_folder

# Brand palette (RGB) ----------------------------------------------------------
BRAND = (46, 134, 171)      # #2E86AB
LIGHT = (248, 249, 250)     # #F8F9FA
GREY = (102, 102, 102)      # #666666


class SalesReportPDF(FPDF):
    """Custom FPDF with a branded header and footer."""

    def header(self) -> None:
        self.set_fill_color(*BRAND)
        self.rect(0, 0, self.w, 26, "F")
        self.set_y(8)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, "Sales Performance Report", align="C")
        self.ln(20)
        self.set_text_color(0, 0, 0)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_text_color(*GREY)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Automatically generated - page {self.page_no()}", align="C")


class PDFReportExporter:
    """Builds a PDF report from the sales data and chart images."""

    def __init__(self, data_folder: str = "data", reports_folder: str = "reports"):
        self.reports_folder = ensure_folder(reports_folder)
        self.generator = SalesReportGenerator(data_folder, reports_folder)

    def export(self, filename: str | None = None) -> Path:
        """Generate charts (if needed), assemble the PDF and return its path."""
        report_data = self.generator.generate_full_report()
        stats = report_data["daily_stats"]

        pdf = SalesReportPDF(orientation="P", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=True, margin=18)
        pdf.add_page()

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*GREY)
        pdf.cell(0, 6, f"Generated {datetime.now():%B %d, %Y at %I:%M %p}", ln=True)
        pdf.cell(0, 6, f"Reporting period: {stats['date_range']}", ln=True)
        pdf.ln(4)

        self._kpi_table(pdf, stats)
        self._charts(pdf, report_data["chart_paths"])

        if filename is None:
            filename = f"sales_report_{datetime.now():%Y-%m-%d}.pdf"
        path = self.reports_folder / filename
        pdf.output(str(path))
        print(f"PDF report saved: {path}")
        return path

    # -- sections --------------------------------------------------------------
    def _kpi_table(self, pdf: FPDF, stats: dict) -> None:
        pdf.set_text_color(*BRAND)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, "Key Metrics", ln=True)
        pdf.ln(1)

        rows = [
            ("Total Revenue", f"${stats['total_revenue']:,.2f}"),
            ("Total Transactions", f"{stats['total_transactions']}"),
            ("Average Order Value", f"${stats['average_order_value']:,.2f}"),
            ("Top Product", str(stats["top_product"])),
            ("Top Salesperson", str(stats["top_salesperson"])),
            ("Top Region", str(stats["top_region"])),
        ]

        label_w, value_w, row_h = 70.0, 110.0, 9.0
        for i, (label, value) in enumerate(rows):
            pdf.set_fill_color(*(LIGHT if i % 2 == 0 else (255, 255, 255)))
            pdf.set_text_color(68, 68, 68)
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(label_w, row_h, f"  {label}", border=1, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(value_w, row_h, f"  {value}", border=1, fill=True, ln=True)
        pdf.ln(6)

    def _charts(self, pdf: FPDF, chart_paths) -> None:
        pdf.set_text_color(*BRAND)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, "Visual Analytics", ln=True)
        pdf.ln(2)

        usable_w = pdf.w - pdf.l_margin - pdf.r_margin
        for chart_path in chart_paths:
            path = Path(chart_path)
            if not path.exists():
                continue
            # Start a new page if the next chart would overflow the page.
            if pdf.get_y() > pdf.h - 90:
                pdf.add_page()
            pdf.image(str(path), w=usable_w)
            pdf.ln(4)


def main() -> None:
    PDFReportExporter().export()


if __name__ == "__main__":
    main()
