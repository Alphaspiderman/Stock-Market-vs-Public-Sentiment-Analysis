# TODO: Send cleaned comments thourgh various Sentiment Analysis models to get the sentiment and map to a time series

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

# Function to get sentiment label
def get_sentiment(comment):
    if pd.isna(comment) or comment.strip() == "":
        return "Neutral"  # Neutral for empty or missing comments
    result = sentiment_pipeline(comment)[0]
    sentiment = result["label"]
    if sentiment == "LABEL_0":  # Negative
        return "Negative"
    elif sentiment == "LABEL_1":  # Neutral
        return "Neutral"
    elif sentiment == "LABEL_2":  # Positive
        return "Positive"

# Apply sentiment analysis
df["sentiment_label"] = df["comment"].apply(get_sentiment)

# Create a new DataFrame with the selected columns
df_output = df[["publishedAt", "comment", "sentiment_label"]]

# Save to a new CSV file for frontend
df_output.to_csv("../../frontend/public/data/sentiment_analysis_results.csv", index=False)

# Saved in temp for trials
df_output.to_csv("../temp/sentiment_analysis_results.csv", index=False)

print("Sentiment analysis results saved to 'sentiment_analysis_results.csv'.")
