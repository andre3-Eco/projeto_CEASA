
import os
import sys
import tempfile
import pandas as pd
import numpy as np

def test_add_lag_feature():
    # Add the src directory to the path so we can import src.features
    sys.path.insert(0, os.path.abspath('src'))
    from src.features import add_features
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-06-01", "2026-06-02", "2026-06-03"]),
        "product": ["Banana"]*3,
        "min_price": [5.0, 5.5, 6.0],
        "max_price": [7.0, 7.5, 8.0]
    })
    featured = add_features(df, lags=[1])
    assert "min_price_lag1" in featured.columns
    assert "max_price_lag1" in featured.columns
    assert pd.isna(featured.loc[0, "min_price_lag1"])
    assert featured.loc[1, "min_price_lag1"] == 5.0
    assert pd.isna(featured.loc[0, "max_price_lag1"])
    assert featured.loc[1, "max_price_lag1"] == 7.0
