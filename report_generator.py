"""
Report Generator for Sales Data Analysis
Creates charts and summary reports from sales data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from pathlib import Path
import os

class SalesReportGenerator:
    """Generates comprehensive sales reports with charts and analytics"""
    
    def __init__(self, data_folder='data', reports_folder='reports'):
        self.data_folder = Path(data_folder)
        self.reports_folder = Path(reports_folder)
        
        # Create reports folder if it doesn't exist
        self.reports_folder.mkdir(exist_ok=True)
        
        # Set up matplotlib style for professional looking charts
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def load_latest_data(self):
        """
        Load the most recent sales data file
        
        Returns:
            pandas.DataFrame: Latest sales data
        """
        # Get all CSV files in data folder
        csv_files = list(self.data_folder.glob('sales_data_*.csv'))
        
        if not csv_files:
            raise FileNotFoundError("No sales data files found!")
        
        # Sort by filename to get the latest date
        latest_file = sorted(csv_files)[-1]
        
        print(f"📊 Loading data from: {latest_file}")
        
        # Load and return the data
        df = pd.read_csv(latest_file)
        df['Date'] = pd.to_datetime(df['Date'])
        
        return df, latest_file.name
    
    def load_weekly_data(self):
        """
        Load data for the past 7 days for trend analysis
        
        Returns:
            pandas.DataFrame: Combined weekly data
        """
        csv_files = list(self.data_folder.glob('sales_data_*.csv'))
        
        if not csv_files:
            raise FileNotFoundError("No sales data files found!")
        
        # Load and combine all files
        weekly_data = []
        for file in csv_files:
            df = pd.read_csv(file)
            df['Date'] = pd.to_datetime(df['Date'])
            weekly_data.append(df)
        
        # Combine all dataframes
        combined_df = pd.concat(weekly_data, ignore_index=True)
        
        # Sort by date
        combined_df = combined_df.sort_values('Date')
        
        print(f"📈 Loaded {len(combined_df)} records from {len(csv_files)} files")
        
        return combined_df
    
    def generate_summary_stats(self, df):
        """
        Calculate key business metrics
        
        Args:
            df (pandas.DataFrame): Sales data
            
        Returns:
            dict: Summary statistics
        """
        stats = {
            'total_revenue': df['Total_Amount'].sum(),
            'total_transactions': len(df),
            'average_order_value': df['Total_Amount'].mean(),
            'top_product': df.groupby('Product')['Total_Amount'].sum().idxmax(),
            'top_salesperson': df.groupby('Salesperson')['Total_Amount'].sum().idxmax(),
            'top_region': df.groupby('Region')['Total_Amount'].sum().idxmax(),
            'date_range': f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}"
        }
        
        return stats
    
    def create_revenue_by_product_chart(self, df, filename='revenue_by_product.png'):
        """Create a bar chart showing revenue by product"""
        plt.figure(figsize=(12, 6))
        
        # Calculate revenue by product
        product_revenue = df.groupby('Product')['Total_Amount'].sum().sort_values(ascending=False)
        
        # Create bar chart
        bars = plt.bar(product_revenue.index, product_revenue.values)
        
        # Customize chart
        plt.title('Revenue by Product', fontsize=16, fontweight='bold')
        plt.xlabel('Product', fontsize=12)
        plt.ylabel('Revenue ($)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save chart
        chart_path = self.reports_folder / filename
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Chart saved: {chart_path}")
        return chart_path
    
    def create_sales_by_region_chart(self, df, filename='sales_by_region.png'):
        """Create a pie chart showing sales distribution by region"""
        plt.figure(figsize=(10, 8))
        
        # Calculate sales by region
        region_sales = df.groupby('Region')['Total_Amount'].sum()
        
        # Create pie chart
        wedges, texts, autotexts = plt.pie(region_sales.values, 
                                          labels=region_sales.index,
                                          autopct='%1.1f%%',
                                          startangle=90)
        
        # Customize chart
        plt.title('Sales Distribution by Region', fontsize=16, fontweight='bold')
        
        # Make percentage text more readable
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.axis('equal')
        
        # Save chart
        chart_path = self.reports_folder / filename
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"🥧 Chart saved: {chart_path}")
        return chart_path
    
    def create_daily_trend_chart(self, df, filename='daily_trend.png'):
        """Create a line chart showing daily sales trends"""
        plt.figure(figsize=(12, 6))
        
        # Calculate daily totals
        daily_sales = df.groupby('Date')['Total_Amount'].sum().reset_index()
        
        # Create line chart
        plt.plot(daily_sales['Date'], daily_sales['Total_Amount'], 
                marker='o', linewidth=2, markersize=8)
        
        # Customize chart
        plt.title('Daily Sales Trend', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Revenue ($)', fontsize=12)
        plt.xticks(rotation=45)
        
        # Add value labels
        for i, row in daily_sales.iterrows():
            plt.annotate(f'${row["Total_Amount"]:,.0f}', 
                        (row['Date'], row['Total_Amount']),
                        textcoords="offset points", 
                        xytext=(0,10), 
                        ha='center')
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save chart
        chart_path = self.reports_folder / filename
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 Chart saved: {chart_path}")
        return chart_path
    
    def generate_full_report(self):
        """
        Generate complete report with all charts and statistics
        
        Returns:
            tuple: (summary_stats, chart_paths)
        """
        print("🚀 Starting report generation...")
        
        # Load data
        daily_df, filename = self.load_latest_data()
        weekly_df = self.load_weekly_data()
        
        # Generate statistics
        daily_stats = self.generate_summary_stats(daily_df)
        weekly_stats = self.generate_summary_stats(weekly_df)
        
        # Create charts
        chart_paths = []
        
        # Daily charts
        chart_paths.append(self.create_revenue_by_product_chart(daily_df, 'daily_revenue_by_product.png'))
        chart_paths.append(self.create_sales_by_region_chart(daily_df, 'daily_sales_by_region.png'))
        
        # Weekly trend chart
        chart_paths.append(self.create_daily_trend_chart(weekly_df, 'weekly_trend.png'))
        
        print("✅ Report generation completed!")
        
        return {
            'daily_stats': daily_stats,
            'weekly_stats': weekly_stats,
            'chart_paths': chart_paths,
            'data_filename': filename
        }

def main():
    """Test the report generator"""
    generator = SalesReportGenerator()
    report_data = generator.generate_full_report()
    
    print("\n📊 DAILY STATISTICS:")
    for key, value in report_data['daily_stats'].items():
        print(f"  {key}: {value}")
    
    print(f"\n📈 Generated {len(report_data['chart_paths'])} charts")

if __name__ == "__main__":
    main() 