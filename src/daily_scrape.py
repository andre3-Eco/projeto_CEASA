import pandas as pd
from datetime import datetime
import os
import sys
from pathlib import Path

# Ensure the project root is in the Python path so that `src` can be imported as a package
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.scrape import scrape_frutas


def scrape_and_save(output_path: str):
    df = scrape_frutas()
    df["scrape_date"] = datetime.now().strftime("%Y-%m-%d")
    # If file exists, append without header; else write with header
    if os.path.exists(output_path):
        df.to_csv(output_path, mode="a", header=False, index=False)
    else:
        df.to_csv(output_path, mode="w", header=True, index=False)


if __name__ == "__main__":
    # Default output path
    default_path = os.path.join("data", "raw", "frutas_prices.csv")
    # Allow override via command line argument
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    else:
        output_path = default_path
    scrape_and_save(output_path)