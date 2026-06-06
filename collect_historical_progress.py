#!/usr/bin/env python
"""
Historical data collection script for CEASA fruit prices.
Collects data for the last N days and shows progress.
"""
import sys
import os
import time
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scrape import scrape_frutas_date

def daterange(start_date, end_date):
    """Generate dates from start to end inclusive."""
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(days=n)

def collect_historical_data(start_date_str, end_date_str, output_dir="data/raw", delay_between_requests=1.0):
    """
    Collect historical fruit price data for each day in the date range.
    
    Args:
        start_date_str: Start date in DD/MM/YYYY format
        end_date_str: End date in DD/MM/YYYY format
        output_dir: Directory to save CSV files
        delay_between_requests: Seconds to wait between requests (to be respectful)
    """
    # Parse dates
    start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
    end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate totals
    total_days = int((end_date - start_date).days) + 1
    processed = 0
    saved = 0
    no_data = 0
    errors = 0
    
    print(f"Starting collection from {start_date_str} to {end_date_str}")
    print(f"Total days to process: {total_days}")
    print(f"Delay between requests: {delay_between_requests}s")
    print("-" * 50)
    
    # Iterate through each date
    for single_date in daterange(start_date, end_date):
        date_str = single_date.strftime("%d/%m/%Y")
        processed += 1
        
        try:
            # Scrape data for this date
            df = scrape_frutas_date(date_str)
            
            if df.empty:
                no_data += 1
                status = "NO DATA"
            else:
                # Save to CSV
                filename = f"{single_date.date()}_frutas.csv"
                filepath = os.path.join(output_dir, filename)
                df.to_csv(filepath, index=False)
                saved += 1
                status = f"SAVED ({len(df)} rows)"
                
        except Exception as e:
            errors += 1
            status = f"ERROR: {str(e)[:50]}..."
        
        # Print progress (every 5 days or for first/last few days)
        if processed <= 5 or processed % 5 == 0 or processed == total_days or processed >= total_days - 5:
            print(f"[{processed:3d}/{total_days}] {date_str}: {status}")
        
        # Be respectful to the server - delay between requests
        if processed < total_days:  # Don't delay after the last request
            time.sleep(delay_between_requests)
    
    # Print summary
    print("-" * 50)
    print("COLLECTION FINISHED")
    print(f"Processed: {processed} days")
    print(f"Saved: {saved} files")
    print(f"No data: {no_data} days")
    print(f"Errors: {errors} days")
    print(f"Files saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    # Collect last 30 days by default (adjustable via command line if needed)
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)  # Last 30 days
    
    start_str = start_date.strftime("%d/%m/%Y")
    end_str = end_date.strftime("%d/%m/%Y")
    
    print(f"CEASA Fruit Price Historical Data Collection")
    print(f"Collecting data for the last 30 days")
    print(f"Date range: {start_str} to {end_str}")
    print()
    
    collect_historical_data(start_str, end_str, delay_between_requests=1.5)