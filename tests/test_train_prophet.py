
import os
import sys
import pandas as pd
import numpy as np

def test_prophet_train_outputs_model():
    # Add the src directory to the path so we can import src.train_prophet
    sys.path.insert(0, os.path.abspath('src'))
    from src.train_prophet import train_model
    df = pd.DataFrame({
        "ds": pd.date_range("2026-01-01", periods=100, freq="D"),
        "y": np.random.rand(100)*10 + 5
    })
    model = train_model(df)
    assert model is not None
    # Check that we can make a forecast
    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)
    assert "yhat" in forecast.columns
