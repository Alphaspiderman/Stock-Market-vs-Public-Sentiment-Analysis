# Sentiment Score and Time Series Analysis

import pandas as pd
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# load the model
model_name = "cardiffnlp/twitter-roberta-base-sentiment"

# define the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# define the sentiment pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Load CSV file
df = pd.read_csv("../temp/cleaned_comments.csv")

# Convert timestamp to datetime
df["publishedAt"] = pd.to_datetime(df["publishedAt"])

# Function to get sentiment score
def get_sentiment(comment):
    if pd.isna(comment) or comment.strip() == "":
        return 0  # Neutral for empty or missing comments
    result = sentiment_pipeline(comment)[0]
    sentiment = result["label"]
    if sentiment == "LABEL_0":  # Negative
        return -1
    elif sentiment == "LABEL_1":  # Neutral
        return 0
    elif sentiment == "LABEL_2":  # Positive
        return 1

# Apply sentiment analysis
df["sentiment_score"] = df["comment"].apply(get_sentiment)

# Aggregate sentiment over time
df.set_index("publishedAt", inplace=True)
df_resampled = df["sentiment_score"].resample("D").mean()  # Aggregate hourly

# Plot time series
plt.figure(figsize=(12, 6))
plt.plot(df_resampled, marker="o", linestyle="-", color="b")
plt.xlabel("Date")
plt.ylabel("Average Sentiment Score")
plt.title("Sentiment Analysis Over Time")
plt.grid()
plt.show()