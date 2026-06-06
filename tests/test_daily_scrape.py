import os
import tempfile
import pandas as pd
import sys
sys.path.insert(0, os.path.abspath('src'))

def test_daily_scrape_creates_file():
    from src.daily_scrape import scrape_and_save
    # Create a temporary file name that does not exist
    out_file = tempfile.mktemp(suffix='.csv')
    try:
        scrape_and_save(out_file)
        assert os.path.exists(out_file)
        # Read the CSV
        df = pd.read_csv(out_file)
        # Check that scrape_date column exists
        assert "scrape_date" in df.columns
        # Check that we have at least one row of data (the CSV will have header + data)
        assert df.shape[0] > 0
        # Optionally, check that the scrape_date values are not null
        assert df["scrape_date"].notna().all()
    finally:
        if os.path.exists(out_file):
            os.unlink(out_file)