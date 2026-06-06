#!/usr/bin/env python
"""
Quick test of historical data collection with progress display.
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

def test_collection(start_date_str, end_date_str, output_dir="data/raw_test", delay_between_requests=2.0):
    """
    Test collection with progress display.
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
    
    print(f"TEST: Collection from {start_date_str} to {end_date_str}")
    print(f"Total days: {total_days}, Delay: {delay_between_requests}s")
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
            status = f"ERROR: {type(e).__name__}"
        
        # Print progress for every date in this small test
        print(f"[{processed:2d}/{total_days}] {date_str}: {status}")
        
        # Be respectful to the server - delay between requests
        if processed < total_days:  # Don't delay after the last request
            time.sleep(delay_between_requests)
    
    # Print summary
    print("-" * 50)
    print("TEST FINISHED")
    print(f"Processed: {processed} days")
    print(f"Saved: {saved} files")
    print(f"No data: {no_data} days")
    print(f"Errors: {errors} days")
    print(f"Files saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    # Test last 3 days
    end_date = datetime.today()
    start_date = end_date - timedelta(days=2)  # Last 3 days (today + 2 days ago)
    
    start_str = start_date.strftime("%d/%m/%Y")
    end_str = end_date.strftime("%d/%m/%Y")
    
    print(f"CEASA Fruit Price - QUICK TEST")
    print(f"Collecting data for last 3 days")
    print(f"Date range: {start_str} to {end_str}")
    print()
    
    test_collection(start_str, end_str, delay_between_requests=2.0)