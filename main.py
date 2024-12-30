from googleapiclient.discovery import build
import pandas as pd
from sqlalchemy import create_engine
import datetime


API_KEY = "AIzaSyCqZUUSOYlT9brPp0OXQAI-uE67iCu0-PA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


DB_URL = "sqlite:///youtube_data.db"  
engine = create_engine(DB_URL)


def get_channel_data(youtube, channel_id):
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()

    for item in response["items"]:
        channel_data = {
            "channel_id": item["id"],
            "channel_name": item["snippet"]["title"],
            "subscribers": int(item["statistics"].get("subscriberCount", 0)),
            "total_views": int(item["statistics"].get("viewCount", 0)),
            "total_videos": int(item["statistics"].get("videoCount", 0)),
            "last_updated": datetime.datetime.now()
        }
    return channel_data


def get_videos(youtube, channel_id):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50,
        order="date",
        type="video"
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        videos.append({
            "video_id": item["id"]["videoId"],
            "channel_id": channel_id,
            "title": item["snippet"]["title"],
            "publish_date": item["snippet"]["publishedAt"]
        })
    return videos


def main():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    channel_id = "UCOhHO2ICt0ti9KAh-QHvttQ"  


    channel_data = get_channel_data(youtube, channel_id)
    print("Channel Data:", channel_data)


    pd.DataFrame([channel_data]).to_sql("channels", engine, if_exists="append", index=False)


    videos = get_videos(youtube, channel_id)
    print("Videos:", videos)


    pd.DataFrame(videos).to_sql("videos", engine, if_exists="append", index=False)

if __name__ == "__main__":

    main()