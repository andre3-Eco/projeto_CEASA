import sys
import os
import pandas as pd
sys.path.insert(0, os.path.abspath('src'))

def test_scrape_frutas_returns_dataframe():
    from src.scrape import scrape_frutas
    df = scrape_frutas()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    # Expect columns: Product, Minimum Price, Maximum Price, etc.
    assert "Product" in df.columns