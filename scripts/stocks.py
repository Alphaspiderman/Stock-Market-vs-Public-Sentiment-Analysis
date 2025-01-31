import yfinance as yf
import pandas as pd

# Define the start and end date
START_DATE = "2025-01-01"
END_DATE = "2025-01-31"

# Names of companies and their stock tickers
COMPANY_NAMES = {
    "NVDA": "NVIDIA Corporation",
    "MSFT": "Microsoft Corporation",
    "AVGO": "Broadcom Inc.",
}


# Function to fetch the stock data
def fetch_stock_data(ticker):
    data = yf.Ticker(ticker)
    df = data.history(start=START_DATE, end=END_DATE)
    df["Ticker"] = ticker
    return df


# Fetch the stock data for each company
all_stock_data = []
for stock in COMPANY_NAMES.keys():
    stock_data = fetch_stock_data(stock)
    all_stock_data.append(stock_data)

# Combine the stock data
combined_stock_data = pd.concat(all_stock_data)

# Save the stock data to a CSV file
combined_stock_data.to_csv("stock_data.csv")
