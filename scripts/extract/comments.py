import csv
import re
from os import getenv

import googleapiclient.discovery
from dotenv import load_dotenv

# Load the ENV variables
load_dotenv()

# Get the developer key
DEV_KEY = getenv("DEVELOPER_KEY", None)

# Check if the developer key is present
if DEV_KEY is None:
    raise ValueError("No developer key found")

# Read the video ids from the file
video_ids = []
with open("./yt_links.txt", "r") as file:
    content = file.readlines()
    video_ids = [re.findall(r"v=([a-zA-Z0-9_-]+)", link)[0] for link in content]

# Set the API service name and version
api_service_name = "youtube"
api_version = "v3"

# Create the youtube service
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEV_KEY
)


# Function to fetch all the comments
def fetch_all_comments(video_id):
    comments_data = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            order="relevance",
            pageToken=next_page_token,
        )
        response = request.execute()

        # comments and likes counts
        comments_data.extend(
            [
                {
                    "comment": item["snippet"]["topLevelComment"]["snippet"][
                        "textDisplay"
                    ],
                    "likeCount": item["snippet"]["topLevelComment"]["snippet"][
                        "likeCount"
                    ],
                    "publishedAt": item["snippet"]["topLevelComment"]["snippet"][
                        "publishedAt"
                    ],
                }
                for item in response["items"]
            ]
        )

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return comments_data


# Fetch all the comments for each video
all_comments = []
comment_id = 1

# Loop over all videos and get the comments
for v_id in video_ids:
    video_comments = fetch_all_comments(v_id)
    for comment in video_comments:
        comment["id"] = comment_id
        comment["video_id"] = v_id
        all_comments.append(comment)
        comment_id += 1

# Save the comments to a CSV file
headers = ["id", "video_id", "comment", "likeCount", "publishedAt"]

# Write the comments to a CSV file
with open("scripts/comments.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_comments)
