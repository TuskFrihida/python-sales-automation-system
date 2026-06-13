# 📊 Sales Automation System

> An end-to-end **Python automation toolkit** that turns raw sales data into business insights and delivers them as **charts, Excel workbooks, PDF reports, automated emails, and a live web dashboard** — all from one command-line tool.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Flask](https://img.shields.io/badge/Web-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)

---

## 🎯 The Problem It Solves

Many businesses still build sales reports by hand every day: open a spreadsheet, calculate totals, copy numbers into a deck, make a few charts, and email it to the team. It's slow, repetitive, and easy to get wrong.

**This project automates the entire workflow.** Point it at your sales data and it will:

1. Crunch the numbers (revenue, transactions, average order value, top performers)
2. Build professional charts
3. Package the results as an **Excel workbook**, a **PDF report**, an **HTML email**, or a **web dashboard**
4. Optionally run **on a daily schedule** with no human involvement

It's a practical showcase of the building blocks of real-world Python automation: data processing, file generation, document automation, email/SMTP, web apps, scheduling, secure configuration, logging, and a clean CLI.

---

## ✨ Features

| Capability | What it does | Tech used |
|---|---|---|
| 🧮 **Data processing** | Aggregates sales into KPIs and rankings | pandas |
| 📊 **Chart generation** | Bar, pie and trend charts saved as PNG | matplotlib / seaborn |
| 📗 **Excel automation** | Multi-sheet styled workbook with native Excel charts | openpyxl |
| 📄 **PDF automation** | Branded, print-ready executive one-pager | fpdf2 |
| 📧 **Email automation** | HTML email with embedded stats + chart attachments | smtplib / email |
| 🌐 **Web dashboard** | Live browser view with download buttons | Flask |
| ⏰ **Scheduling** | Hands-off daily report delivery | schedule |
| 🔐 **Secure config** | `.env`-first secrets, never committed | python-dotenv |
| 🧰 **Unified CLI** | One entry point, clear subcommands | argparse |
| 📝 **Logging** | File + console logs of every run | logging |

---

## 🗂️ Project Structure

```
python-sales-automation-system/
├── main.py                 # ⭐ Unified CLI entry point (start here)
├── config_loader.py        # Layered .env + config.ini settings loader
├── utils.py                # Shared logging / folder helpers
├── data_generator.py       # Generates realistic sample sales data
├── report_generator.py     # KPIs + matplotlib charts
├── excel_exporter.py       # Styled multi-sheet Excel workbook
├── pdf_exporter.py         # Print-ready PDF report
├── email_automation.py     # HTML email delivery + scheduling
├── dashboard.py            # Flask web dashboard
├── templates/              # Dashboard HTML templates
├── requirements.txt        # Python dependencies
├── .env.example            # Copy to .env and fill in (git-ignored)
├── config.ini.example      # Optional alternative to .env
├── SETUP_GUIDE.md          # Detailed email / Gmail setup
└── README.md
```

> Generated `data/`, `reports/`, and `logs/` folders plus `.env` / `config.ini` are **git-ignored** so no data or secrets ever land in the repo.

---

## 🚀 Quick Start

### 1. Clone and install

```bash
git clone https://github.com/TuskFrihida/python-sales-automation-system.git
cd python-sales-automation-system

# (recommended) create a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Generate sample data

No real data? No problem — generate a realistic week of sales:

```bash
python main.py generate-data --days 7
```

### 3. See it work (no email or credentials needed)

```bash
# Build charts + print KPIs to the console
python main.py report

# Export a styled Excel workbook  -> reports/sales_report_<date>.xlsx
python main.py excel

# Export a PDF report             -> reports/sales_report_<date>.pdf
python main.py pdf

# Launch the live web dashboard   -> http://127.0.0.1:5000
python main.py dashboard
```

That's the fastest way to **visualise the solution**: run the dashboard and open it in your browser, or open the generated Excel/PDF files in the `reports/` folder.

---

## 🖥️ The CLI

Everything is driven through `main.py`. Run `python main.py --help` or `python main.py <command> --help` for details.

| Command | Description | Useful options |
|---|---|---|
| `generate-data` | Create sample sales CSVs | `--days`, `--min-records`, `--max-records` |
| `report` | Generate charts + print stats | `--data-folder`, `--reports-folder` |
| `excel` | Export a styled `.xlsx` workbook | `--output` |
| `pdf` | Export a print-ready PDF | `--output` |
| `email` | Generate a report and email it | (uses `.env` / `config.ini`) |
| `dashboard` | Launch the Flask web dashboard | `--host`, `--port`, `--debug` |
| `schedule` | Email the report daily | `--time HH:MM` |

Examples:

```bash
python main.py generate-data --days 14 --max-records 120
python main.py excel --output q3_summary.xlsx
python main.py dashboard --port 8080
python main.py schedule --time 08:30
```

---

## 📧 Email Setup (optional)

Email is only needed for the `email` and `schedule` commands. Credentials are loaded from environment variables first, then `config.ini`.

**Recommended — use a `.env` file:**

```bash
cp .env.example .env      # Windows: copy .env.example .env
```

Then edit `.env`:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_16_char_app_password
RECIPIENT_EMAIL=person1@email.com, person2@email.com
```

For Gmail you need a **16-character App Password** (not your normal password). Step-by-step instructions are in [SETUP_GUIDE.md](SETUP_GUIDE.md).

Then:

```bash
python main.py email            # send once
python main.py schedule         # send daily at 09:00
```

> 🔒 `.env` and `config.ini` are listed in `.gitignore` and are never committed. The repo only ships `.env.example` / `config.ini.example` templates.

---

## 🔐 Security

- Secrets live in `.env` (or `config.ini`) and are **git-ignored** — only `*.example` templates are tracked.
- Email uses **TLS encryption** and **app passwords** rather than account passwords.
- The system fails safe: if email isn't configured, it tells you instead of crashing.
- Generated data, reports and logs stay local and out of version control.

---

## 🛠️ Tech Stack

**Python 3.8+** · pandas · matplotlib · seaborn · openpyxl · fpdf2 · Flask · python-dotenv · schedule · smtplib

---

## 🧭 How It Fits Together

```
                 ┌──────────────────┐
   CSV data ──▶  │ report_generator │ ──▶ KPIs + PNG charts
                 └──────────────────┘
                          │
       ┌──────────────────┼─────────────────────┐
       ▼                  ▼                      ▼
 excel_exporter     pdf_exporter          email_automation
   (.xlsx)             (.pdf)              (HTML + charts)
       └──────────────────┼─────────────────────┘
                          ▼
                     dashboard.py
                  (Flask web view)
```

All of it is orchestrated by `main.py`.

---

## 🚀 Possible Next Steps

- Read real data from a database (PostgreSQL / MySQL) or a CRM API
- Slack / Microsoft Teams notifications
- Predictive sales forecasting with scikit-learn
- Dockerfile for one-command deployment

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

> Built to demonstrate production-style Python automation: data → documents → delivery, with secure config, logging, a CLI, and a web UI.
