import googleapiclient.discovery
import os
import re
import csv

with open("scripts/yt_links.txt", "r") as file:
    content = file.read()
    links = content.split(',')
# print(links)

# extract video id
video_ids = []
for link in links:

    video_ids.append(re.findall(r'v=([a-zA-Z0-9_-]+)', link)[0])
# print(video_ids)

api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=os.environ.get("DEVELOPER_KEY")
)


def fetch_all_comments(video_id, max_comments):
    comments_data = []
    next_page_token = None

    while len(comments_data) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            order="relevance",
            pageToken=next_page_token
        )
        response = request.execute()

        # comments and likes counts
        comments_data.extend([
            {
                'id': item['snippet']['topLevelComment']['id'],
                'comment': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                'likeCount': item['snippet']['topLevelComment']['snippet']['likeCount'],
                'publishedAt': item['snippet']['topLevelComment']['snippet']['publishedAt'],
            }
            for item in response['items']
        ])

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return comments_data[:max_comments]


# fetch all the comments
all_comments = fetch_all_comments(video_ids[0], max_comments=200)

print(all_comments[:10])
