import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Function to convert price string to float
def price_to_float(price_str):
    if isinstance(price_str, str):
        # Remove 'R$' and spaces, replace comma with dot
        cleaned = price_str.replace('R$', '').strip().replace(',', '.')
        try:
            return float(cleaned)
        except:
            return np.nan
    return np.nan

# Path to raw data
raw_path = os.path.join('data', 'raw')
files = glob.glob(os.path.join(raw_path, '*.csv'))
# Exclude the consolidated frutas_prices.csv if it exists (optional)
files = [f for f in files if not os.path.basename(f).startswith('frutas_prices')]
print(f"Found {len(files)} daily CSV files.")

# List to hold data
data_list = []

for file in files:
    # Extract date from filename (format: YYYY-MM-DD_frutas.csv)
    fname = os.path.basename(file)
    try:
        date_str = fname.split('_')[0]
        # Validate date format
        pd.to_datetime(date_str)
    except:
        # If filename parsing fails, try to get date from first row's scrape_date
        try:
            df_temp = pd.read_csv(file, nrows=1)
            date_str = df_temp['scrape_date'].iloc[0]
        except:
            print(f"Skipping {file}: cannot determine date")
            continue
    
    # Read the file
    try:
        df = pd.read_csv(file)
    except Exception as e:
        print(f"Error reading {file}: {e}")
        continue
    
    # Clean price columns
    for col in ['Minimum Price', 'Average Price', 'Maximum Price']:
        if col in df.columns:
            df[col] = df[col].apply(price_to_float)
    
    # We'll use Average Price as the target
    # Group by Product and take mean of Average Price
    df = df.dropna(subset=['Average Price'])
    if df.empty:
        continue
    
    # Group by Product and compute mean average price
    daily_avg = df.groupby('Product')['Average Price'].mean().reset_index()
    daily_avg['date'] = date_str
    data_list.append(daily_avg)

# Combine all data
if not data_list:
    raise ValueError("No data processed")
    
df_all = pd.concat(data_list, ignore_index=True)
# Convert date to datetime
df_all['date'] = pd.to_datetime(df_all['date'])
# Sort by date and product
df_all = df_all.sort_values(['date', 'Product'])

print(f"Total records: {len(df_all)}")
print(f"Date range: {df_all['date'].min()} to {df_all['date'].max()}")
print(f"Unique products: {df_all['Product'].nunique()}")

# Pivot to have time series per product (optional, but we'll loop)
# We'll forecast for top N products by number of non-null observations
product_counts = df_all['Product'].value_counts()
top_n = 10  # number of products to forecast
top_products = product_counts.head(top_n).index.tolist()
print(f"Top {top_n} products: {top_products}")

# Create output directory for plots
output_dir = 'forecast_output'
os.makedirs(output_dir, exist_ok=True)

# For each top product, fit Exponential Smoothing and forecast
for product in top_products:
    print(f"\nProcessing {product}...")
    # Filter data for this product
    df_product = df_all[df_all['Product'] == product][['date', 'Average Price']].copy()
    # Set date as index and resample to daily frequency, forward fill missing values
    df_product = df_product.set_index('date').asfreq('D')
    df_product['Average Price'] = df_product['Average Price'].ffill()
    df_product = df_product.reset_index()
    df_product.columns = ['ds', 'y']
    # Remove any remaining NaNs in y (shouldn't be any after ffill, but just in case)
    df_product = df_product.dropna(subset=['y'])
    if df_product.shape[0] < 10:
        print(f"  Not enough data for {product}, skipping")
        continue
    
    # Determine seasonality period: if we have at least 2 years (730 days) of data, use yearly seasonality
    if len(df_product) >= 730:
        seasonal_periods = 365
    else:
        seasonal_periods = None
    
    try:
        # Initialize and fit Exponential Smoothing model
        model = ExponentialSmoothing(
                    df_product['y'],
                    trend='add',
                    seasonal='add' if seasonal_periods else None,
                    seasonal_periods=seasonal_periods
                ).fit()
        
        # Forecast for 2 years (730 days)
        forecast = model.predict(start=len(df_product), end=len(df_product)+730-1)
        
        # Create a dataframe for plotting: historical + forecast
        historic = df_product['y']
        # Create date index for forecast
        last_date = df_product['ds'].iloc[-1]
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=730, freq='D')
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(historic.index, historic.values, label='Historical')
        plt.plot(forecast_dates, forecast.values, label='Forecast', color='red')
        plt.title(f'Price Forecast for {product}')
        plt.xlabel('Date')
        plt.ylabel('Average Price (R$)')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        # Save plot
        plot_path = os.path.join(output_dir, f'{product.replace(" ", "_")}_forecast.png')
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()
        print(f"  Saved plot to {plot_path}")
        
        # Also save forecast data (optional)
        forecast_df = pd.DataFrame({'date': forecast_dates, 'forecast': forecast.values})
        forecast_path = os.path.join(output_dir, f'{product.replace(" ", "_")}_forecast.csv')
        forecast_df.to_csv(forecast_path, index=False)
        print(f"  Saved forecast data to {forecast_path}")
        
    except Exception as e:
        print(f"  Error fitting model for {product}: {e}")
        continue

print("\nForecasting completed.")
