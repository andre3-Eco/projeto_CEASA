#!/usr/bin/env python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import time
from datetime import datetime, timedelta
from src.scrape import scrape_frutas_date

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(days=n)

def run(start_date_str, end_date_str, output_dir="data/raw", delay=1.0):
    """
    Iterate over each day from start_date_str to end_date_str (inclusive),
    scrape fruit prices for that date, and save to a CSV file.
    Prints progress.
    """
    start = datetime.strptime(start_date_str, "%d/%m/%Y")
    end = datetime.strptime(end_date_str, "%d/%m/%Y")
    os.makedirs(output_dir, exist_ok=True)
    total_days = int((end - start).days) + 1
    processed = 0
    saved = 0
    errors = 0
    for single_date in daterange(start, end):
        date_str = single_date.strftime("%d/%m/%Y")
        try:
            df = scrape_frutas_date(date_str)
            if not df.empty:
                out_file = os.path.join(output_dir, f"{single_date.date()}_frutas.csv")
                df.to_csv(out_file, index=False)
                saved += 1
                status = "SAVED"
            else:
                status = "NO DATA"
        except Exception as e:
            status = f"ERROR: {e}"
            errors += 1
        processed += 1
        # Print progress every day for now (since we'll limit days)
        print(f"[{processed}/{total_days}] {date_str}: {status}")
        # Be respectful to the server
        time.sleep(delay)
    print(f"\nFinished. Processed: {processed}, Saved: {saved}, Errors: {errors}")

if __name__ == '__main__':
    # Collect last 30 days as a demo to show progress
    end = datetime.today()
    start = end - timedelta(days=30)
    print(f"Collecting from {start.strftime('%d/%m/%Y')} to {end.strftime('%d/%m/%Y')} ({ (end-start).days + 1 } days)")
    run(start.strftime('%d/%m/%Y'), end.strftime('%d/%m/%Y'), delay=1.0)