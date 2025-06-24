import yfinance as yf
import pandas as pd

def fetch_data(ticker, period="6mo"):
    """Fetch stock data and return clean DataFrame"""
    data = yf.download(ticker, period=period, progress=False)
    # Simplify MultiIndex if present
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
    return data

if __name__ == "__main__":
    print("Testing data fetcher...")
    test_data = fetch_data("RELIANCE.NS")
    print("Columns:", test_data.columns.tolist())
    print(test_data.head())