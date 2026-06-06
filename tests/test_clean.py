import os
import sys
sys.path.insert(0, os.path.abspath('src'))
import pandas as pd
from src.clean import clean_data

def test_clean_converts_prices():
    raw = pd.DataFrame({
        "Product": ["Banana", "Banana"],
        "Minimum Price": ["5,00", "6,50"],
        "Maximum Price": ["7,00", "8,00"],
        "scrape_date": ["2026-06-01", "2026-06-02"]
    })
    cleaned = clean_data(raw)
    assert cleaned["min_price"].dtype == float
    assert cleaned["max_price"].dtype == float
    assert cleaned.loc[0, "min_price"] == 5.0