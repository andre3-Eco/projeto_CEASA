@echo off
REM Change to the project directory
cd /d C:\Users\André Elias\ceasa_forecast
REM Activate the virtual environment
call .venv\Scripts\activate
REM Run the daily scrape script, outputting to data/raw/frutas_prices.csv
python src/daily_scrape.py data/raw/frutas_prices.csv