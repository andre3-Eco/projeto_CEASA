#!/usr/bin/env python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from historical_scrape import run
from datetime import datetime, timedelta

if __name__ == '__main__':
    # Collect last 7 days as a demo
    end = datetime.today()
    start = end - timedelta(days=7)
    print(f"Collecting from {start.strftime('%d/%m/%Y')} to {end.strftime('%d/%m/%Y')}")
    run(start.strftime('%d/%m/%Y'), end.strftime('%d/%m/%Y'), delay=1.0)