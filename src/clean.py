import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Rename columns to standardized names
    df = df.rename(columns={
        "Product": "product",
        "Minimum Price": "min_price",
        "Maximum Price": "max_price"
    })
    # Convert price strings: replace comma with dot and strip
    for col in ["min_price", "max_price"]:
        df[col] = df[col].astype(str).str.replace(",", ".").str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce")
    # Ensure date is datetime
    df["date"] = pd.to_datetime(df["scrape_date"])
    # Keep relevant columns
    cleaned = df[["date", "product", "min_price", "max_price"]].copy()
    # Sort by date and product
    cleaned = cleaned.sort_values(["product", "date"]).reset_index(drop=True)
    return cleaned