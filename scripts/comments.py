import googleapiclient.discovery
import os
import re

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
