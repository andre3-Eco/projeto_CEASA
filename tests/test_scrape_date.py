import sys
import os
import pandas as pd
sys.path.insert(0, os.path.abspath('src'))

def test_scrape_frutas_date_returns_dataframe():
    from src.scrape import scrape_frutas_date
    df = scrape_frutas_date("2024-01-01")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "Product" in df.columns