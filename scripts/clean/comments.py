# TODO: Load comments and clean them

import csv
import html
import re
from langdetect import detect
import os
import pytz
from datetime import datetime, timezone
from transformers import AutoTokenizer

# Define like count threshold to filter out comments
min_likes = 0

# Define keywords to filter out comments
banned_keywords = {"palestine"}

# Load tokenizer for truncation
tokenizer = AutoTokenizer.from_pretrained("roberta-base")
max_tokens = 512  # Maximum allowed tokens

# Define time zones
utc_zone = timezone.utc
est_zone = pytz.timezone("US/Eastern")

# Function to convert timestamp to EST and format it
def convert_to_est(utc_str):
    try:
        utc_time = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=utc_zone)
        est_time = utc_time.astimezone(est_zone)
        return est_time  # Format to match stock data
    except ValueError:
        return None  # Return None if parsing fails

# Function to convert the data string to a datetime object for sorting
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None  # Return None if parsing fails

# Function to clean each comment
def clean_comment(comment):
    if not comment:
        return None  # Skip empty comments

    # Convert HTML entities to text
    comment = html.unescape(comment)

    # Replace <br> with a space and remove HTML tags & links
    comment = re.sub(r"<br\s*/?>", " ", comment)
    comment = re.sub(r"<.*?>", "", comment)  # Remove HTML tags
    comment = re.sub(r"http\S+", "", comment)  # Remove links

    # Remove non-English comments using language detection
    try:
        if detect(comment) != "en":
            return None  # Return None for non-English comments
    except:
        return None  # In case language detection fails

    # Remove comments containing banned keywords
    if any(keyword in comment.lower() for keyword in banned_keywords):
        return None

    # Tokenize and truncate the comment properly
    comment = tokenizer.decode(
        tokenizer(comment, truncation=True, max_length=max_tokens, return_tensors="pt")["input_ids"][0],
        skip_special_tokens=True
    )

    # Return cleaned comment
    return comment

# Read the existing comments from the CSV file
input_file = "../temp/comments_5090.csv"
output_file = "../temp/cleaned_comments.csv"
cleaned_comments = []

# Open the CSV file and read its contents
with open(input_file, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    headers = reader.fieldnames

    if headers is None:
        raise ValueError("CSV file is empty or malformed.")

    # Remove 'id' from headers
    headers = [header for header in headers if header not in ["id","video_id"]]

    # Loop through each comment and clean it
    for row in reader:
        try:
            like_count = int(row["likeCount"].strip()) if row["likeCount"].strip() else 0
        except ValueError:
            print(f"Skipping row with invalid likeCount: {row['likeCount']}")
            continue  # Skip rows with invalid like_counts

        # Keep only comments with at least min_likes
        if like_count < min_likes:
            continue

        cleaned_comment = clean_comment(row["comment"])

        if cleaned_comment:  # Only include valid comments
            row["comment"] = cleaned_comment
            est_time = convert_to_est(row["publishedAt"])  # Convert timestamp to EST
            if est_time:
                row["publishedAt"] = est_time  # Replace with EST formatted time
                row.pop("id", None)  # Ensure "id" is removed
                row.pop("video_id", None)
                cleaned_comments.append(row)


# Sort comments by publishedAt (datetime object)
cleaned_comments.sort(key=lambda x: x["publishedAt"])

for row in cleaned_comments:
    row["publishedAt"] = row["publishedAt"].strftime("%Y-%m-%d %H:%M:%S%z")  # Convert back to string


# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Write the cleaned comments to a new CSV file
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(cleaned_comments)

print(f"Cleaned comments saved to {output_file}")
