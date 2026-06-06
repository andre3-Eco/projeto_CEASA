import os
import pandas as pd
from datetime import datetime
from unittest.mock import patch

def test_historical_scrape_creates_files(tmp_path, monkeypatch):
    # Mock scrape_frutas_date to return a simple DataFrame
    def mock_scrape(date_str):
        return pd.DataFrame({"Product": ["Test"], "Price": [10]})
    
    # Patch the function in the module where it is defined (src.scrape)
    monkeypatch.setattr("src.scrape.scrape_frutas_date", mock_scrape)
    
    # We don't need to mock datetime because we are passing explicit strings
    from src.historical_scrape import run
    
    # Run for 2 days
    run(start_date_str="01/01/2021", end_date_str="02/01/2021", output_dir=str(tmp_path))
    
    # Check that two files were created
    assert (tmp_path / "2021-01-01_frutas.csv").exists()
    assert (tmp_path / "2021-01-02_frutas.csv").exists()
    
    # Check the content of one file
    df = pd.read_csv(tmp_path / "2021-01-01_frutas.csv")
    assert len(df) == 1
    assert df.iloc[0]["Product"] == "Test"