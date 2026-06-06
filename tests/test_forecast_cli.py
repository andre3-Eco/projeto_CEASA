import os
import sys
import tempfile
import subprocess

def test_forecast_cli_runs():
    # Ensure we have a minimal cleaned file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('date,product,min_price,max_price\n2026-06-01,Banana,5.0,7.0\n2026-06-02,Banana,5.5,7.5\n')
        cleaned_path = f.name
    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, 'src/forecast_cli.py', '--input', cleaned_path, '--product', 'Banana', '--days', '3'],
            capture_output=True, text=True, cwd=r'C:\Users\André Elias\ceasa_forecast'
        )
        # Check that the script ran successfully
        assert result.returncode == 0, f"Script failed with stderr: {result.stderr}"
        # Check that the output contains the word "Forecast"
        assert "Forecast" in result.stdout, f"Expected 'Forecast' in stdout, got: {result.stdout}"
        # Check that an output file was created (default forecast.csv)
        output_path = 'forecast.csv'
        assert os.path.exists(output_path), f"Output file {output_path} not found"
        # Optionally, check the content of the output file
        with open(output_path, 'r') as out_f:
            lines = out_f.readlines()
            assert len(lines) > 1, "Output file should have header and at least one data row"
    finally:
        # Clean up the temporary file
        os.unlink(cleaned_path)
        # Clean up the default output file if it exists
        if os.path.exists('forecast.csv'):
            os.unlink('forecast.csv')