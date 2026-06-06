import pandas as pd
from pathlib import Path
from src.clean import clean_data

RAW_DIR = Path("data/raw")
OUTPUT_PATH = Path("data/processed/fruits_clean.csv")

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    all_files = list(RAW_DIR.glob("*.csv"))
    if not all_files:
        print("No raw files found")
        return
    df_list = [pd.read_csv(f) for f in all_files]
    raw = pd.concat(df_list, ignore_index=True)
    cleaned = clean_data(raw)
    cleaned.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved cleaned data to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()