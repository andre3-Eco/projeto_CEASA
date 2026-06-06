import os
import tempfile
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, os.path.abspath('src'))

def test_make_dataset_outputs_file():
    from src.make_dataset import main
    # Create a temporary directory for raw data
    raw_dir = Path(tempfile.mkdtemp())
    try:
        # Create a dummy raw file with columns as expected from scraper + scrape_date
        # We'll create a DataFrame and write it to CSV to ensure proper quoting.
        df_raw = pd.DataFrame({
            'Product': ['Banana'],
            'Minimum Price': ['5,00'],
            'Maximum Price': ['7,00'],
            # Add other columns that the scraper produces (optional)
            'Unit': ['Kg'],
            'Origin': ['SP-MG-PE'],
            'Type': ['Comum'],
            'Average Price': ['6,00'],
            'Market Situation': ['Est'],
            'Chart': ['abrir gráfico'],
            'scrape_date': ['2026-06-01']
        })
        raw_file = raw_dir / "frutas_prices.csv"
        # Write CSV with quoting to preserve commas inside fields
        df_raw.to_csv(raw_file, index=False)
        # Create output directory
        output_dir = raw_dir / "processed"
        output_dir.mkdir(exist_ok=True)
        out_file = output_dir / "frutas_clean.csv"
        # Monkeypatch the paths in the make_dataset module
        import src.make_dataset as mod
        original_raw = mod.RAW_DIR
        original_out = mod.OUTPUT_PATH
        mod.RAW_DIR = raw_dir
        mod.OUTPUT_PATH = out_file
        try:
            main()
            assert out_file.exists()
            df = pd.read_csv(out_file)
            assert "min_price" in df.columns
            assert "max_price" in df.columns
            assert "product" in df.columns
            assert "date" in df.columns
            # Check that the conversion worked (should be numeric)
            assert df.loc[0, "min_price"] == 5.0
            assert df.loc[0, "max_price"] == 7.0
        finally:
            mod.RAW_DIR = original_raw
            mod.OUTPUT_PATH = original_out
    finally:
        # Clean up
        import shutil
        shutil.rmtree(raw_dir)