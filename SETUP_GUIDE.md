# 🚀 Email Automation Setup Guide

## Prerequisites

1. **Python 3.7+** installed
2. **Gmail account** (for sending emails)
3. **App Password** generated for Gmail

## Step 1: Gmail App Password Setup

### For Gmail Users:

1. **Enable 2-Factor Authentication** on your Gmail account
2. Go to [Google Account Settings](https://myaccount.google.com/)
3. Click "Security" → "2-Step Verification"
4. Scroll down to "App passwords"
5. Select "Mail" and "Windows Computer" (or your device)
6. **Copy the 16-character app password** (save it somewhere safe!)

### Why App Password?
- Gmail blocks regular passwords for security
- App passwords allow automated scripts to send emails safely
- More secure than using your actual Gmail password

## Step 2: Configure Your Email Settings

You can configure credentials in **either** of two ways. Environment
variables (`.env`) take priority and are the recommended, more secure option.

### Option A (recommended): `.env` file

Copy the template and fill in your values:

```bash
cp .env.example .env      # Windows: copy .env.example .env
```

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=YOUR_GMAIL@gmail.com
SENDER_PASSWORD=YOUR_16_CHAR_APP_PASSWORD
RECIPIENT_EMAIL=recipient@example.com
```

### Option B: `config.ini` file

Copy `config.ini.example` to `config.ini` and edit it:

```ini
[EMAIL]
smtp_server = smtp.gmail.com
smtp_port = 587
sender_email = YOUR_GMAIL@gmail.com          # ← Replace with your Gmail
sender_password = YOUR_16_CHAR_APP_PASSWORD   # ← Replace with app password
recipient_email = RECIPIENT@example.com       # ← Replace with recipient email

[PATHS]
data_folder = data
reports_folder = reports
logs_folder = logs

[SETTINGS]
report_frequency = daily
chart_style = seaborn-v0_8
log_level = INFO
```

Both `.env` and `config.ini` are git-ignored and must never be committed.

## Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

## Step 4: Test the System

All features run through the unified CLI (`main.py`).

### Generate Sample Data (if not already done):
```bash
python main.py generate-data --days 7
```

### Test Report Generation (without email):
```bash
python main.py report
```

### Test Complete Email System:
```bash
python main.py email
```

## How to Run Different Components

### 1. Generate New Sample Data
```bash
python main.py generate-data --days 7
```
- Creates sample sales data in the `data/` folder
- Each day has 30-80 random sales records (configurable)

### 2. Generate Reports Only (No Email)
```bash
python main.py report
```
- Creates charts in `reports/` folder
- Shows statistics in console
- Good for testing without sending emails

### 3. Export Excel / PDF
```bash
python main.py excel
python main.py pdf
```

### 4. Launch the Web Dashboard
```bash
python main.py dashboard
```
- Opens a live view at http://127.0.0.1:5000

### 5. Send Email Report Once
```bash
python main.py email
```
- Generates reports AND sends email
- Use this for testing your email setup

### 6. Schedule Daily Reports
```bash
python main.py schedule --time 09:00
```
- Runs continuously and sends reports daily at the given time
- Press Ctrl+C to stop

## Troubleshooting

### "Authentication failed" Error
- Double-check your Gmail app password
- Make sure 2-factor authentication is enabled
- Verify sender_email is correct

### "No sales data files found" Error
- Run `python data_generator.py` first
- Check if `data/` folder exists with CSV files

### Charts not generating
- Install matplotlib: `pip install matplotlib seaborn`
- Check if `reports/` folder has write permissions

### Email not received
- Check spam/junk folder
- Verify recipient_email is correct
- Check logs in `logs/email_automation.log`

## Security Best Practices

1. **Never commit** `config.ini` with real passwords to version control
2. **Use app passwords**, not your main Gmail password
3. **Keep logs secure** - they may contain sensitive info
4. **Regularly rotate** app passwords

## File Structure After Setup

```
project1_email_reporter/
├── data/                          # Sales data CSV files
│   ├── sales_data_2025-07-18.csv
│   └── ...
├── reports/                       # Generated charts
│   ├── daily_revenue_by_product.png
│   ├── daily_sales_by_region.png
│   └── weekly_trend.png
├── logs/                          # System logs
│   └── email_automation.log
├── config.ini                     # Your email settings
├── data_generator.py              # Creates sample data
├── report_generator.py            # Creates charts
├── email_automation.py            # Main automation script
└── SETUP_GUIDE.md                # This file
```

## Next Steps

1. **Test with sample data** first
2. **Replace with real data** sources later
3. **Customize charts** and reports for your needs
4. **Add more recipients** by modifying the email logic
5. **Schedule at different times** by changing the schedule

## Example Email Output

The automated email will include:
- 📊 Professional HTML formatting
- 💰 Revenue statistics
- 📈 Transaction counts
- 🏆 Top performers (products, salespeople, regions)
- 📊 3 attached chart images
- 📅 Date ranges and trends

Perfect for daily business reporting! 