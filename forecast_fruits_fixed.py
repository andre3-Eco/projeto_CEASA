import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import warnings
import re
warnings.filterwarnings('ignore')
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def price_to_float(price_str):
    if isinstance(price_str, str):
        cleaned = price_str.replace('R$', '').strip().replace(',', '.')
        try:
            return float(cleaned)
        except:
            return np.nan
    return np.nan

def sanitize_filename(name):
    name = re.sub(r'[^\w\s-]', '_', name)
    name = re.sub(r'[-\s]+', '_', name)
    return name

raw_path = os.path.join('data', 'raw')
files = glob.glob(os.path.join(raw_path, '*.csv'))
files = [f for f in files if not os.path.basename(f).startswith('frutas_prices')]
print(f"Found {len(files)} daily CSV files.")

data_list = []
for file in files:
    fname = os.path.basename(file)
    try:
        date_str = fname.split('_')[0]
        pd.to_datetime(date_str)  # validate
    except:
        try:
            df_temp = pd.read_csv(file, nrows=1)
            date_str = df_temp['scrape_date'].iloc[0]
        except:
            print(f"Skipping {file}: cannot determine date")
            continue
    try:
        df = pd.read_csv(file)
    except Exception as e:
        print(f"Error reading {file}: {e}")
        continue
    for col in ['Minimum Price', 'Average Price', 'Maximum Price']:
        if col in df.columns:
            df[col] = df[col].apply(price_to_float)
    df = df.dropna(subset=['Average Price'])
    if df.empty:
        continue
    daily_avg = df.groupby('Product')['Average Price'].mean().reset_index()
    daily_avg['date'] = date_str
    data_list.append(daily_avg)

if not data_list:
    raise ValueError("No data processed")
df_all = pd.concat(data_list, ignore_index=True)
df_all['date'] = pd.to_datetime(df_all['date'])
df_all = df_all.sort_values(['date', 'Product'])
print(f"Total records: {len(df_all)}")
print(f"Date range: {df_all['date'].min()} to {df_all['date'].max()}")
print(f"Unique products: {df_all['Product'].nunique()}")

product_counts = df_all['Product'].value_counts()
top_n = 10
top_products = product_counts.head(top_n).index.tolist()
print(f"Top {top_n} products: {top_products}")

output_dir = 'forecast_output_fixed'
os.makedirs(output_dir, exist_ok=True)

for product in top_products:
    print(f"\nProcessing {product}...")
    df_product = df_all[df_all['Product'] == product][['date', 'Average Price']].copy()
    # Ensure sorted by date
    df_product = df_product.sort_values('date')
    # Set date as index and resample to daily, forward fill
    df_product = df_product.set_index('date').asfreq('D')
    df_product['Average Price'] = df_product['Average Price'].ffill()
    df_product = df_product.reset_index()
    df_product.columns = ['ds', 'y']
    df_product = df_product.dropna(subset=['y'])
    if df_product.shape[0] < 10:
        print(f"  Not enough data for {product}, skipping")
        continue

    # Determine seasonality
    if len(df_product) >= 730:
        seasonal_periods = 365
    else:
        seasonal_periods = None

    try:
        model = ExponentialSmoothing(
                    df_product['y'],
                    trend='add',
                    seasonal='add' if seasonal_periods else None,
                    seasonal_periods=seasonal_periods
                ).fit()
        forecast = model.predict(start=len(df_product), end=len(df_product)+730-1)

        historic = df_product['y']
        historic_dates = df_product['ds']
        last_date = historic_dates.iloc[-1]
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=730, freq='D')

        plt.figure(figsize=(10, 6))
        plt.plot(historic_dates, historic.values, label='Historical')
        plt.plot(forecast_dates, forecast.values, label='Forecast', color='red')
        plt.title(f'Price Forecast for {product}')
        plt.xlabel('Date')
        plt.ylabel('Average Price (R$)')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        safe_name = sanitize_filename(product)
        plot_path = os.path.join(output_dir, f'{safe_name}_forecast.png')
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()
        print(f"  Saved plot to {plot_path}")

        forecast_df = pd.DataFrame({'date': forecast_dates, 'forecast': forecast.values})
        forecast_path = os.path.join(output_dir, f'{safe_name}_forecast.csv')
        forecast_df.to_csv(forecast_path, index=False)
        print(f"  Saved forecast data to {forecast_path}")
    except Exception as e:
        print(f"  Error fitting model for {product}: {e}")
        continue

print("\nForecasting completed.")
