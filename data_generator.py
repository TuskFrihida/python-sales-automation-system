"""
Data Generator for Sales Reports
Generates sample sales data for demonstration purposes
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import os
from pathlib import Path

class SalesDataGenerator:
    """Generates realistic sales data for testing automation"""
    
    def __init__(self):
        self.products = [
            'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones',
            'Webcam', 'Tablet', 'Phone', 'Charger', 'Speaker'
        ]
        
        self.regions = ['North', 'South', 'East', 'West', 'Central']
        
        self.salespeople = [
            'Alice Johnson', 'Bob Smith', 'Carol Williams', 'David Brown',
            'Eva Davis', 'Frank Miller', 'Grace Wilson', 'Henry Moore'
        ]
    
    def generate_daily_data(self, date=None, num_records=50):
        """
        Generate sales data for a specific date
        
        Args:
            date (datetime): Date for the sales data
            num_records (int): Number of sales records to generate
            
        Returns:
            pandas.DataFrame: Generated sales data
        """
        if date is None:
            date = datetime.now().date()
        
        data = []
        
        for _ in range(num_records):
            # Generate random sales record
            record = {
                'Date': date,
                'Product': random.choice(self.products),
                'Quantity': random.randint(1, 10),
                'Unit_Price': round(random.uniform(10, 1000), 2),
                'Region': random.choice(self.regions),
                'Salesperson': random.choice(self.salespeople)
            }
            
            # Calculate total amount
            record['Total_Amount'] = round(record['Quantity'] * record['Unit_Price'], 2)
            
            data.append(record)
        
        df = pd.DataFrame(data)
        return df
    
    def save_data(self, df, folder='data'):
        """
        Save generated data to CSV file
        
        Args:
            df (pandas.DataFrame): Data to save
            folder (str): Folder to save the data
        """
        # Create folder if it doesn't exist
        Path(folder).mkdir(exist_ok=True)
        
        # Create filename with date
        date_str = df['Date'].iloc[0].strftime('%Y-%m-%d')
        filename = f"{folder}/sales_data_{date_str}.csv"
        
        # Save to CSV
        df.to_csv(filename, index=False)
        print(f"✅ Data saved to {filename}")
        
        return filename

def main():
    """Generate sample data for the last 7 days"""
    generator = SalesDataGenerator()
    
    # Generate data for the last 7 days
    for i in range(7):
        date = datetime.now().date() - timedelta(days=i)
        df = generator.generate_daily_data(date, random.randint(30, 80))
        generator.save_data(df)

if __name__ == "__main__":
    main() 