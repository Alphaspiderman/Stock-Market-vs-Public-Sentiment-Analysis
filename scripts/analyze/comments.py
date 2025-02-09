# TODO: Send cleaned comments thourgh various Sentiment Analysis models to get the sentiment and map to a time series

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# load the model
model_name = "cardiffnlp/twitter-roberta-base-sentiment"

# define the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# define the sentiment pipeline
sentiment_pipeline = pipeline(
    "sentiment-analysis", model=model, tokenizer=tokenizer)

# test input
txt = 'Nvidia has done a good job in the AI sector'

output = sentiment_pipeline(txt)
print(output)
