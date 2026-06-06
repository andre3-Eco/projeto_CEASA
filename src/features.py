
import pandas as pd

def add_features(df: pd.DataFrame, lags: list[int] = [1,7], windows: list[int] = [7,30]) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["product", "date"])
    for lag in lags:
        df[f"min_price_lag{lag}"] = df.groupby("product")["min_price"].shift(lag)
        df[f"max_price_lag{lag}"] = df.groupby("product")["max_price"].shift(lag)
    for window in windows:
        df[f"min_price_roll_mean_{window}"] = df.groupby("product")["min_price"].transform(lambda x: x.rolling(window, min_periods=1).mean())
        df[f"max_price_roll_mean_{window}"] = df.groupby("product")["max_price"].transform(lambda x: x.rolling(window, min_periods=1).mean())
    # Date features
    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["day_of_month"] = df["date"].dt.day
    return df
