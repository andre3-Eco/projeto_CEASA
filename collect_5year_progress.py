#!/usr/bin/env python
"""
Collect 5 years of historical CEASA fruit price data with progress display.
This script can run for several hours - it shows progress and saves data incrementally.
"""
import sys
import os
import time
import signal
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scrape import scrape_frutas_date

# Global flag for graceful shutdown
keep_running = True

def signal_handler(sig, frame):
    global keep_running
    print('\n\nReceived shutdown signal. Finishing current request...')
    keep_running = False

def daterange(start_date, end_date):
    """Generate dates from start to end inclusive."""
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(days=n)

def collect_5year_data(start_date_str, end_date_str, output_dir="data/raw", delay_between_requests=1.5):
    """
    Collect 5 years of historical fruit price data.
    Saves progress incrementally and can be interrupted safely.
    """
    global keep_running
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
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
    
    start_time = time.time()
    
    print("=" * 60)
    print("CEASA FRUIT PRICE - 5 YEAR HISTORICAL DATA COLLECTION")
    print("=" * 60)
    print(f"Date range: {start_date_str} to {end_date_str}")
    print(f"Total days to process: {total_days:,}")
    print(f"Estimated time: {total_days * delay_between_requests / 3600:.1f} hours")
    print(f"Delay between requests: {delay_between_requests}s")
    print(f"Output directory: {os.path.abspath(output_dir)}")
    print("Press Ctrl+C to stop gracefully (will finish current request)")
    print("=" * 60)
    
    # Iterate through each date
    for single_date in daterange(start_date, end_date):
        # Check if we should stop
        if not keep_running:
            print("\nShutdown requested. Stopping after current date...")
            break
            
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
            
            # If we get too many errors in a row, something might be wrong
            if errors > 10 and errors > processed * 0.5:  # More than 50% error rate
                print(f"\nWARNING: High error rate ({errors}/{processed}). Consider checking connection.")
        
        # Print progress (every 50 days or for milestones)
        if processed <= 10 or processed % 50 == 0 or processed == total_days or \
           processed >= total_days - 10 or processed in [100, 500, 1000, 2000]:
            elapsed = time.time() - start_time
            rate = processed / elapsed if elapsed > 0 else 0
            eta_seconds = (total_days - processed) / rate if rate > 0 else 0
            eta_hours = eta_seconds / 3600
            
            print(f"[{processed:5d}/{total_days}] {date_str}: {status}")
            print(f"         Progress: {processed/total_days*100:5.1f}% | "
                  f"Saved: {saved:4d} | No Data: {no_data:4d} | Errors: {errors:4d} | "
                  f"ETA: {eta_hours:5.1f}h")
        
        # Be respectful to the server - delay between requests
        if keep_running and processed < total_days:  # Don't delay after the last request
            time.sleep(delay_between_requests)
    
    # Final summary
    elapsed = time.time() - start_time
    print("=" * 60)
    print("COLLECTION FINISHED")
    print("=" * 60)
    print(f"Processed: {processed:,} days")
    print(f"Saved: {saved:,} files ({saved/total_days*100:.1f}%)")
    print(f"No data: {no_data:,} days ({no_data/total_days*100:.1f}%)")
    print(f"Errors: {errors:,} days ({errors/total_days*100:.1f}%)")
    print(f"Total time: {elapsed/3600:.2f} hours ({elapsed/60:.1f} minutes)")
    print(f"Average rate: {processed/elapsed:.2f} requests/second")
    print(f"Files saved to: {os.path.abspath(output_dir)}")
    print("=" * 60)

if __name__ == "__main__":
    # Collect exactly 5 years of data (5 * 365 = 1825 days, accounting for leap years roughly)
    end_date = datetime.today()
    start_date = end_date - timedelta(days=5*365)  # Approximate 5 years
    
    start_str = start_date.strftime("%d/%m/%Y")
    end_str = end_date.strftime("%d/%m/%Y")
    
    actual_days = (end_date - start_date).days + 1
    print(f"Actual date range: {start_str} to {end_str}")
    print(f"Total days: {actual_days:,} (approximately 5 years)")
    print()
    
    # You can adjust the delay here - 1.5 seconds is respectful but not too slow
    # For faster collection (use at your own risk): try 0.5-1.0
    # For very safe collection: use 2.0-3.0
    collect_5year_data(start_str, end_str, delay_between_requests=1.5)