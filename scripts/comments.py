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


def fetch_all_comments(video_id):
    comments_data = []
    next_page_token = None

    while True:
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
                'comment': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                'likeCount': item['snippet']['topLevelComment']['snippet']['likeCount'],
                'publishedAt': item['snippet']['topLevelComment']['snippet']['publishedAt'],
            }
            for item in response['items']
        ])

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return comments_data


'''
all_comments = fetch_all_comments(video_ids[0], max_comments=200)

print(all_comments[:10])
'''
# fetch all the comments

all_comments = []
comment_id = 1

for v_id in video_ids:
    video_comments = fetch_all_comments(v_id)
    for comment in video_comments:
        comment['id'] = comment_id
        comment['video_id'] = v_id
        all_comments.append(comment)
        comment_id += 1

# save to csv

headers = ['id', 'video_id', 'comment', 'likeCount', 'publishedAt']


with open("scripts/comments.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_comments)
