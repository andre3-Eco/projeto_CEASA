# CEASA Price Forecasting

This project scrapes daily fruit prices from CEASA Pernambuco, cleans the data, and forecasts future prices using Prophet.

## Setup

```bash
python -m venv .venv
.\\.venv\\Scripts\\activate
pip install -r requirements.txt
```

## Usage

1. Scrape today's data:
   ```bash
   python src/daily_scrape.py data/raw/frutas_prices.csv
   ```

2. Combine and clean all raw files:
   ```bash
   python src/make_dataset.py
   ```

3. Generate a 7‑day forecast for Banana:
   ```bash
   python src/forecast_cli.py --input data/processed/fruits_clean.csv --product Banana --days 7
   ```

## Collecting 5 years of historical fruit prices

Run the historical scraper (defaults to last 5 years from today):

```bash
python src/historical_scrape.py
```

To specify a custom date range:

```bash
python -c "from src.historical_scrape import run; run('01/01/2020','31/12/2024')"
```

Each day's data is saved as `data/raw/YYYY-MM-DD_frutas.csv`.  
After collection, generate the unified dataset with:

```bash
python src/make_dataset.py
```

## Project Structure

- `src/` – core modules (scraping, cleaning, features, modeling)
- `data/raw/` – daily scraped CSV files
- `data/processed/` – cleaned dataset
- `notebooks/` – exploratory analysis
- `tests/` – unit tests
- `scripts/` – helper batch/shell scripts

## Testing

Run the test suite with:
```bash
pytest
```