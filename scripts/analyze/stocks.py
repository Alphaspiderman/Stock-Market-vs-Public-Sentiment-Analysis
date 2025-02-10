import pandas as pd
import matplotlib.pyplot as plt

# Assuming your data is loaded as df
df = pd.read_csv("../temp/stock_data.csv", parse_dates=["Date"])

# Set Date as index for time series analysis
df.set_index("Date", inplace=True)

# List unique tickers (companies)
tickers = df["Ticker"].unique()

# Loop through each ticker and plot the data separately
for ticker in tickers:
    # Filter data for the current ticker
    ticker_data = df[df["Ticker"] == ticker]
    
    # Create a figure for the Closing Price plot
    plt.figure(figsize=(12, 6))

    # Plot the Closing Price
    plt.plot(ticker_data.index, ticker_data["Close"], label="Closing Price", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)", color="blue")
    plt.tick_params(axis="y", labelcolor="blue")
    
    # Add title and grid
    plt.title(f"Stock Price for {ticker}")
    plt.grid(True)
    
    # Display the plot
    plt.tight_layout()
    plt.show()
