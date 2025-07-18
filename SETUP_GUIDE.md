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

Edit the `config.ini` file with your real information:

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
chart_style = seaborn
log_level = INFO
```

## Step 3: Install Required Packages

```bash
pip install pandas openpyxl matplotlib seaborn schedule
```

## Step 4: Test the System

### Generate Sample Data (if not already done):
```bash
python data_generator.py
```

### Test Report Generation (without email):
```bash
python report_generator.py
```

### Test Complete Email System:
```bash
python email_automation.py
```

## How to Run Different Components

### 1. Generate New Sample Data
```bash
python data_generator.py
```
- Creates 7 days of sales data in `data/` folder
- Each day has 30-80 random sales records

### 2. Generate Reports Only (No Email)
```bash
python report_generator.py
```
- Creates charts in `reports/` folder
- Shows statistics in console
- Good for testing without sending emails

### 3. Send Email Report Once
```bash
python email_automation.py
```
- Generates reports AND sends email
- Use this for testing your email setup

### 4. Schedule Daily Reports
Edit `email_automation.py` and uncomment the last line:
```python
# schedule_daily_reports()  # ← Remove the # to enable
```

Then run:
```bash
python email_automation.py
```
- Runs continuously
- Sends reports daily at 9:00 AM
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