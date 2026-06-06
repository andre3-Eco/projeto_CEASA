import os
from datetime import datetime, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(days=n)

def run(start_date_str, end_date_str, output_dir="data/raw"):
    """
    Iterate over each day from start_date_str to end_date_str (inclusive),
    scrape fruit prices for that date, and save to a CSV file.
    """
    from src.scrape import scrape_frutas_date  # Import inside function to avoid circular issues if any

    start = datetime.strptime(start_date_str, "%d/%m/%Y")
    end = datetime.strptime(end_date_str, "%d/%m/%Y")
    os.makedirs(output_dir, exist_ok=True)
    for single_date in daterange(start, end):
        date_str = single_date.strftime("%d/%m/%Y")
        try:
            df = scrape_frutas_date(date_str)
            if not df.empty:
                out_file = os.path.join(output_dir, f"{single_date.date()}_frutas.csv")
                df.to_csv(out_file, index=False)
        except Exception as e:
            print(f"Error for {date_str}: {e}")

if __name__ == "__main__":
    # default: last 5 years
    end = datetime.today()
    start = end - timedelta(days=5*365)
    run(start.strftime("%d/%m/%Y"), end.strftime("%d/%m/%Y"))