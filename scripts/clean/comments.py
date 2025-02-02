# TODO: Load comments and clean them

import csv
import html
import re
from langdetect import detect
import os

# Function to clean each comment
def clean_comment(comment):
    # Convert HTML entities to text
    comment = html.unescape(comment)
    
    # Replace <br> with a space
    comment = re.sub(r'<br\s*/?>', ' ', comment)
    
    # Remove non-English comments using language detection
    try:
        if detect(comment) != 'en':
            return None  # Return None for non-English comments
    except:
        return None  # In case language detection fails

    # Return cleaned comment
    return comment

# Read the existing comments from the CSV file
input_file = "../extract/comments.csv"
output_file = "./cleaned_comments.csv"
cleaned_comments = []

# Open the CSV file and read its contents
with open(input_file, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    headers = reader.fieldnames
    
    # Loop through each comment and clean it
    for row in reader:
        cleaned_comment = clean_comment(row["comment"])
        
        if cleaned_comment:  # Only include valid comments
            row["comment"] = cleaned_comment
            cleaned_comments.append(row)

# Check if the output file exists, if not create it
if not os.path.exists(os.path.dirname(output_file)):
    os.makedirs(os.path.dirname(output_file))

# Write the cleaned comments to a new CSV file
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(cleaned_comments)

print(f"Cleaned comments saved to {output_file}")
