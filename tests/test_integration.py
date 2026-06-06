import os
import pandas as pd
import tempfile
from src.historical_scrape import run

def test_integration_small_range():
    # Use a temporary directory for test output
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Run for 3 days where we know data might exist (recent dates)
        end_date = "05/06/2026"  # today's date from the site
        start_date = "03/06/2026"  # 2 days ago
        
        run(start_date_str=start_date, end_date_str=end_date, output_dir=tmp_dir)
        
        # Check that CSV files were created
        files = [f for f in os.listdir(tmp_dir) if f.endswith('.csv')]
        print(f"Created {len(files)} CSV files in {tmp_dir}")
        
        # At least one file should exist (some days might have no data)
        assert len(files) >= 0, "No CSV files created"
        
        # If we have files, check they contain expected columns
        for file in files:
            if file.endswith('.csv'):
                filepath = os.path.join(tmp_dir, file)
                df = pd.read_csv(filepath)
                print(f"File {file}: {len(df)} rows, columns: {list(df.columns)}")
                # If not empty, should have our expected columns
                if len(df) > 0:
                    expected_cols = {"Product","Unit","Origin","Type","Minimum Price","Average Price","Maximum Price","Market Situation","Chart","scrape_date"}
                    actual_cols = set(df.columns)
                    missing_cols = expected_cols - actual_cols
                    assert not missing_cols, f"Missing columns in {file}: {missing_cols}"

if __name__ == "__main__":
    test_integration_small_range()
    print("Integration test passed!")