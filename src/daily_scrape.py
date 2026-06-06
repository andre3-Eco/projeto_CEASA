import pandas as pd
from datetime import datetime
import os
from src.scrape import scrape_frutas

def scrape_and_save(output_path: str):
    df = scrape_frutas()
    df["scrape_date"] = datetime.now().strftime("%Y-%m-%d")
    # If file exists, append without header; else write with header
    if os.path.exists(output_path):
        df.to_csv(output_path, mode="a", header=False, index=False)
    else:
        df.to_csv(output_path, mode="w", header=True, index=False)