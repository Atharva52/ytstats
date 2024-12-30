from googleapiclient.discovery import build
import datetime
import pyodbc

# YouTube API credentials
API_KEY = "AIzaSyCqZUUSOYlT9brPp0OXQAI-uE67iCu0-PA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# SQL Server connection details
CONN_STRING = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=user_teams;UID=Atharva;PWD=Google@1'



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


def save_to_database(channel_data, videos_data):
    conn = pyodbc.connect(CONN_STRING)
    cursor = conn.cursor()

    # Insert channel data
    cursor.execute("""
        INSERT INTO youtube_channel (channel_id, channel_name, subscribers, total_views, total_videos, last_updated)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (channel_data['channel_id'], channel_data['channel_name'], channel_data['subscribers'],
          channel_data['total_views'], channel_data['total_videos'], channel_data['last_updated']))

    # Insert videos data
    for video in videos_data:
        cursor.execute("""
            INSERT INTO youtube_videos (video_id, channel_id, title, publish_date)
            VALUES (?, ?, ?, ?)
        """, (video['video_id'], video['channel_id'], video['title'], video['publish_date']))

    conn.commit()
    conn.close()


def main():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    channel_id = "UCOhHO2ICt0ti9KAh-QHvttQ"

    # Fetch data
    channel_data = get_channel_data(youtube, channel_id)
    videos_data = get_videos(youtube, channel_id)

    # Save to database
    save_to_database(channel_data, videos_data)

    print("Data successfully saved to the database.")


if __name__ == "__main__":
    main()
