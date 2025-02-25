import pandas as pd
import matplotlib.pyplot as plt

# Load the data
sentiment_df = pd.read_csv("./temp/sentiment_analysis_results.csv", parse_dates=["publishedAt"])
stock_df = pd.read_csv("./temp/stock_data.csv", parse_dates=["Date"])

# Convert dates to match (removes time and timezone)
sentiment_df["publishedAt"] = pd.to_datetime(sentiment_df["publishedAt"]).dt.date
stock_df["Date"] = pd.to_datetime(stock_df["Date"]).dt.date

# Filter for NVDA ticker only
stock_df = stock_df[stock_df["Ticker"] == "NVDA"]

# Convert sentiment labels to numeric (-1, 0, 1)
sentiment_mapping = {"Negative": -1, "Neutral": 0, "Positive": 1}
sentiment_df["sentiment_score"] = sentiment_df["sentiment_label"].map(sentiment_mapping)

# Aggregate sentiment by date (average per day)
daily_sentiment = sentiment_df.groupby("publishedAt", as_index=False)["sentiment_score"].mean()

# Merge daily sentiment with stock data
merged_df = pd.merge(daily_sentiment, stock_df, left_on="publishedAt", right_on="Date", how="inner")

# Plot
fig, ax1 = plt.subplots(figsize=(10, 5))

# Primary Y-axis (Stock Price)
ax1.set_xlabel("Date")
ax1.set_ylabel("Stock Price", color="blue")
ax1.plot(merged_df["Date"], merged_df["Close"], color="blue", label="Stock Price")
ax1.tick_params(axis="y", labelcolor="blue")

# Secondary Y-axis (Sentiment Score)
ax2 = ax1.twinx()
ax2.set_ylabel("Sentiment Score", color="red")
ax2.plot(merged_df["Date"], merged_df["sentiment_score"], color="red", label="Sentiment Score")
ax2.tick_params(axis="y", labelcolor="red")

plt.title("NVIDIA Stock Price vs Daily Sentiment Score")
plt.show()
