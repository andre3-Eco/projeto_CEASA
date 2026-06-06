
import os
import sys
import pandas as pd
import numpy as np

def test_evaluate_returns_metrics():
    # Add the src directory to the path so we can import src.evaluate
    sys.path.insert(0, os.path.abspath('src'))
    from src.evaluate import evaluate_forecast
    # Create a simple predictable series: y = ds.dayofweek * 0.5 + 10
    dates = pd.date_range("2026-01-01", periods=100, freq="D")
    df = pd.DataFrame({
        "ds": dates,
        "y": dates.dayofweek * 0.5 + 10
    })
    mae, rmse = evaluate_forecast(df, test_days=30)
    assert isinstance(mae, float)
    assert isinstance(rmse, float)
    assert mae >= 0
    assert rmse >= 0
