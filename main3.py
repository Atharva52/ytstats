from googleapiclient.discovery import build
import datetime
import psycopg2

API_KEY = "AIzaSyCqZUUSOYlT9brPp0OXQAI-uE67iCu0-PA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

CONN_STRING = "dbname='youtube_data' user='postgres' password='Mtnl@123' host='localhost' port='5432'"

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

def clean_text(text):
    return text.encode('utf-8', 'ignore').decode('utf-8')

def save_to_database(channel_data, videos_data):
    try:
        conn = psycopg2.connect(CONN_STRING)
        cursor = conn.cursor()

        channel_data['channel_name'] = clean_text(channel_data['channel_name'])
        for video in videos_data:
            video['title'] = clean_text(video['title'])

        cursor.execute("SELECT COUNT(*) FROM youtube_channel WHERE channel_id = %s", (channel_data['channel_id'],))
        result = cursor.fetchone()

        if result[0] == 0:
            cursor.execute("""
                INSERT INTO youtube_channel (channel_id, channel_name, subscribers, total_views, total_videos, last_updated)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (channel_data['channel_id'], channel_data['channel_name'], channel_data['subscribers'],
                  channel_data['total_views'], channel_data['total_videos'], channel_data['last_updated']))
        else:
            cursor.execute("""
                UPDATE youtube_channel
                SET channel_name = %s, subscribers = %s, total_views = %s, total_videos = %s, last_updated = %s
                WHERE channel_id = %s
            """, (channel_data['channel_name'], channel_data['subscribers'], channel_data['total_views'],
                  channel_data['total_videos'], channel_data['last_updated'], channel_data['channel_id']))

        for video in videos_data:
            cursor.execute("""
                INSERT INTO youtube_videos (video_id, channel_id, title, publish_date)
                VALUES (%s, %s, %s, %s)
            """, (video['video_id'], video['channel_id'], video['title'], video['publish_date']))

        conn.commit()
        print("Data successfully saved to the database.")

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        conn.close()


def main():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    channel_id = "UCOhHO2ICt0ti9KAh-QHvttQ"

    channel_data = get_channel_data(youtube, channel_id)
    videos_data = get_videos(youtube, channel_id)

    save_to_database(channel_data, videos_data)

if __name__ == "__main__":
    main()
