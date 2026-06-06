import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_frutas():
    url = "https://www.ceasape.org.br/cotacao"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # Find the box that contains the Frutas heading
    boxes = soup.find_all("div", class_="box")
    box = None
    for b in boxes:
        heading = b.find("h3", string=lambda t: t and t.strip() == "Frutas")
        if heading:
            box = b
            break
    if not box:
        raise ValueError("FRUTAS heading not found")
    # Within this box, find the link with text "Saiba Mais"
    link = box.find("a", string=lambda t: t and t.strip() == "Saiba Mais")
    if not link or not link.get("href"):
        raise ValueError("Saiba Mais link not found")
    detail_url = link["href"]
    # If relative, make absolute (should already be absolute)
    if detail_url.startswith("/"):
        detail_url = f"https://www.ceasape.org.br{detail_url}"
    detail_resp = requests.get(detail_url, timeout=10)
    detail_resp.raise_for_status()
    detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
    # Find the first table
    table = detail_soup.find("table")
    if not table:
        raise ValueError("Price table not found")
    # Use pandas to read HTML table
    df_list = pd.read_html(str(table))
    df = df_list[0]
    # Clean column names (strip whitespace)
    df.columns = [col.strip() for col in df.columns]
    # Rename columns to English for consistency (as expected by cleaning)
    rename_map = {
        "Produto": "Product",
        "Und.": "Unit",
        "Proced.": "Origin",
        "Tipo": "Type",
        "Pr.Min.": "Minimum Price",
        "Pr.M.Com.": "Average Price",
        "Pr.Máx.": "Maximum Price",
        "Sit.Merc.": "Market Situation",
        "Gráfico": "Chart"
    }
    df = df.rename(columns=rename_map)
    return df

def scrape_frutas_date(date_str):
    """
    Scrape fruit prices for a given date (DD/MM/YYYY).
    Returns a DataFrame with an added 'scrape_date' column.
    If no data found for the date, returns an empty DataFrame with expected columns.
    """
    url = "https://www.ceasape.org.br/cotacao/frutas"
    params = {"data": date_str}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # Check for "Nenhum produto encontrado para esta cotação"
    if soup.find(string="Nenhum produto encontrado para esta cotação"):
        # Return empty DataFrame with expected columns plus scrape_date
        df = pd.DataFrame(columns=[
            "Product", "Unit", "Origin", "Type",
            "Minimum Price", "Average Price", "Maximum Price",
            "Market Situation", "Chart"
        ])
        df["scrape_date"] = pd.to_datetime(date_str, format="%d/%m/%Y")
        return df
    # Find the first table
    table = soup.find("table")
    if not table:
        raise ValueError("Price table not found")
    # Use pandas to read HTML table
    df_list = pd.read_html(str(table))
    df = df_list[0]
    # Clean column names (strip whitespace)
    df.columns = [col.strip() for col in df.columns]
    # Rename columns to English for consistency
    rename_map = {
        "Produto": "Product",
        "Und.": "Unit",
        "Proced.": "Origin",
        "Tipo": "Type",
        "Pr.Min.": "Minimum Price",
        "Pr.M.Com.": "Average Price",
        "Pr.Máx.": "Maximum Price",
        "Sit.Merc.": "Market Situation",
        "Gráfico": "Chart"
    }
    df = df.rename(columns=rename_map)
    # Add scrape_date column
    df["scrape_date"] = pd.to_datetime(date_str, format="%d/%m/%Y")
    return df