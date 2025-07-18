"""
Email Automation System for Sales Reports
Automatically generates and emails daily/weekly sales reports
"""

import smtplib
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import logging
from pathlib import Path
import schedule
import time

from report_generator import SalesReportGenerator

class EmailAutomator:
    """Handles automated email sending with reports and attachments"""
    
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = self.load_config()
        self.setup_logging()
        
    def load_config(self):
        """Load configuration from INI file"""
        config = configparser.ConfigParser()
        
        if not Path(self.config_file).exists():
            raise FileNotFoundError(f"Configuration file {self.config_file} not found!")
        
        config.read(self.config_file)
        return config
    
    def setup_logging(self):
        """Set up logging for the automation system"""
        log_level = self.config.get('SETTINGS', 'log_level', fallback='INFO')
        log_folder = Path(self.config.get('PATHS', 'logs_folder', fallback='logs'))
        log_folder.mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_folder / 'email_automation.log'),
                logging.StreamHandler()  # Also print to console
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Email automation system initialized")
    
    def create_html_email_body(self, report_data):
        """
        Create professional HTML email body with embedded statistics
        
        Args:
            report_data (dict): Report data from SalesReportGenerator
            
        Returns:
            str: HTML email body
        """
        daily_stats = report_data['daily_stats']
        weekly_stats = report_data['weekly_stats']
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #2E86AB; color: white; padding: 20px; text-align: center; }}
                .stats-container {{ display: flex; flex-wrap: wrap; gap: 20px; margin: 20px 0; }}
                .stat-box {{ background-color: #f8f9fa; border-left: 4px solid #2E86AB; padding: 15px; flex: 1; min-width: 200px; }}
                .stat-value {{ font-size: 24px; font-weight: bold; color: #2E86AB; }}
                .stat-label {{ color: #666; font-size: 14px; }}
                .section {{ margin: 20px 0; }}
                .charts-note {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Daily Sales Report</h1>
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <div class="section">
                <h2>🎯 Today's Performance</h2>
                <div class="stats-container">
                    <div class="stat-box">
                        <div class="stat-value">${daily_stats['total_revenue']:,.2f}</div>
                        <div class="stat-label">Total Revenue</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{daily_stats['total_transactions']}</div>
                        <div class="stat-label">Total Transactions</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">${daily_stats['average_order_value']:,.2f}</div>
                        <div class="stat-label">Average Order Value</div>
                    </div>
                </div>
                
                <div class="stats-container">
                    <div class="stat-box">
                        <div class="stat-value">{daily_stats['top_product']}</div>
                        <div class="stat-label">Top Product</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{daily_stats['top_salesperson']}</div>
                        <div class="stat-label">Top Salesperson</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{daily_stats['top_region']}</div>
                        <div class="stat-label">Top Region</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>📈 Weekly Overview</h2>
                <div class="stats-container">
                    <div class="stat-box">
                        <div class="stat-value">${weekly_stats['total_revenue']:,.2f}</div>
                        <div class="stat-label">Weekly Revenue</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{weekly_stats['total_transactions']}</div>
                        <div class="stat-label">Weekly Transactions</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{weekly_stats['date_range']}</div>
                        <div class="stat-label">Date Range</div>
                    </div>
                </div>
            </div>
            
            <div class="charts-note">
                <h3>📊 Attached Visual Reports</h3>
                <p>This email includes detailed charts and visualizations:</p>
                <ul>
                    <li><strong>Revenue by Product:</strong> Bar chart showing which products generated the most revenue</li>
                    <li><strong>Sales by Region:</strong> Pie chart displaying regional sales distribution</li>
                    <li><strong>Weekly Trend:</strong> Line chart showing daily sales trends over the past week</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>This report was automatically generated by the Sales Analytics System</p>
                <p>Data source: {report_data['data_filename']}</p>
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def send_email_report(self, report_data):
        """
        Send email with report data and chart attachments
        
        Args:
            report_data (dict): Report data from SalesReportGenerator
        """
        try:
            self.logger.info("Starting email sending process...")
            
            # Get email configuration
            smtp_server = self.config.get('EMAIL', 'smtp_server')
            smtp_port = self.config.getint('EMAIL', 'smtp_port')
            sender_email = self.config.get('EMAIL', 'sender_email')
            sender_password = self.config.get('EMAIL', 'sender_password')
            recipient_emails_raw = self.config.get('EMAIL', 'recipient_email')
            
            # Handle multiple recipients (comma-separated)
            recipient_emails = [email.strip() for email in recipient_emails_raw.split(',')]
            
            # Create message container
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 Daily Sales Report - {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = sender_email
            msg['To'] = ', '.join(recipient_emails)  # Join all emails for display
            
            # Create HTML email body
            html_body = self.create_html_email_body(report_data)
            msg.attach(MIMEText(html_body, 'html'))
            
            # Attach chart images
            for chart_path in report_data['chart_paths']:
                self.attach_image(msg, chart_path)
            
            # Send email
            self.logger.info(f"Connecting to SMTP server: {smtp_server}:{smtp_port}")
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Enable TLS encryption
                server.login(sender_email, sender_password)
                
                self.logger.info(f"Sending email to: {', '.join(recipient_emails)}")
                server.send_message(msg, to_addrs=recipient_emails)
            
            self.logger.info("✅ Email sent successfully!")
            print("✅ Email sent successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to send email: {str(e)}")
            print(f"❌ Failed to send email: {str(e)}")
            raise
    
    def attach_image(self, msg, image_path):
        """
        Attach an image file to the email message
        
        Args:
            msg (MIMEMultipart): Email message object
            image_path (Path): Path to the image file
        """
        try:
            with open(image_path, 'rb') as f:
                img_data = f.read()
            
            image = MIMEImage(img_data)
            image.add_header('Content-Disposition', 
                           f'attachment; filename="{image_path.name}"')
            
            msg.attach(image)
            self.logger.info(f"Attached image: {image_path.name}")
            
        except Exception as e:
            self.logger.warning(f"Failed to attach image {image_path}: {str(e)}")
    
    def generate_and_send_report(self):
        """Complete workflow: generate report and send email"""
        try:
            self.logger.info("🚀 Starting automated report generation and email sending...")
            
            # Generate report
            report_generator = SalesReportGenerator()
            report_data = report_generator.generate_full_report()
            
            # Send email
            self.send_email_report(report_data)
            
            self.logger.info("✅ Automated report process completed successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Automated report process failed: {str(e)}")
            print(f"❌ Error: {str(e)}")

def schedule_daily_reports():
    """Set up scheduled daily reports"""
    automator = EmailAutomator()
    
    # Schedule report to run every day at 9:00 AM
    schedule.every().day.at("09:00").do(automator.generate_and_send_report)
    
    print("📅 Scheduled daily reports at 9:00 AM")
    print("Press Ctrl+C to stop the scheduler")
    
    # Keep the program running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def main():
    """Main function - run once immediately"""
    print("🚀 Running email automation once...")
    
    automator = EmailAutomator()
    automator.generate_and_send_report()

if __name__ == "__main__":
    # For testing, run once immediately
    main()
    
    # Uncomment the line below to enable daily scheduling
    # schedule_daily_reports() 