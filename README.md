YouTube Data Collection and PostgreSQL Integration
This project uses the YouTube Data API to fetch information about YouTube channels and their videos. The data is then stored in a PostgreSQL database for further analysis or reporting.

Project Overview
This script:

Retrieves YouTube channel information (e.g., subscribers, total views, total videos).
Retrieves details about the latest videos from a specified YouTube channel.
Saves the data to a PostgreSQL database (youtube_data), consisting of two tables:
youtube_channel: Stores channel-related information.
youtube_videos: Stores video-related information.
Prerequisites
Before running the script, ensure you have the following:

Python 3.6+: Ensure Python is installed on your machine.

You can check this by running:
bash
Copy code
python --version
Required Python Libraries:

Install the necessary libraries using pip:
bash
Copy code
pip install google-api-python-client psycopg2
PostgreSQL Database:

Make sure you have a PostgreSQL instance running and a database (youtube_data) created.
The tables youtube_channel and youtube_videos will be created in the database automatically.
YouTube API Key:

Obtain a YouTube Data API key from the Google Developer Console.
Replace the placeholder in the script with your own API key:
python
Copy code
API_KEY = "your_youtube_api_key"
Database Schema
The project uses two tables:

youtube_channel
Stores information about a YouTube channel.

Column	Type	Description
channel_id	VARCHAR	Unique ID of the YouTube channel (Primary Key)
channel_name	TEXT	Name of the YouTube channel
subscribers	INT	Number of subscribers the channel has
total_views	INT	Total views across all videos in the channel
total_videos	INT	Total number of videos the channel has published
last_updated	TIMESTAMP	Date and time the data was last updated
youtube_videos
Stores information about the videos published by the YouTube channel.

Column	Type	Description
video_id	VARCHAR	Unique ID of the video (Primary Key)
channel_id	VARCHAR	ID of the channel to which the video belongs
title	TEXT	Title of the video
publish_date	TIMESTAMP	Publish date of the video
How to Run
Step 1: Set Up PostgreSQL Database
Ensure you have PostgreSQL installed and set up. Create a new database named youtube_data.

You can create the database using the following SQL commands in your PostgreSQL client:

sql
Copy code
CREATE DATABASE youtube_data;
Step 2: Update the API Key
Update the API_KEY variable in the script with your own YouTube Data API key.

Step 3: Run the Script
Run the Python script to fetch data from YouTube and store it in the PostgreSQL database:

bash
Copy code
python main3.py
Step 4: Verify the Data in PostgreSQL
Once the script runs successfully, you can connect to your PostgreSQL database and verify the data using a query like:

sql
Copy code
SELECT * FROM youtube_channel;
SELECT * FROM youtube_videos;
Functions
get_channel_data(youtube, channel_id)
Retrieves channel data from the YouTube Data API:

Channel ID
Channel Name
Subscribers Count
Total Views
Total Videos
Last Updated Timestamp
get_videos(youtube, channel_id)
Retrieves a list of video data from the YouTube Data API:

Video ID
Video Title
Video Publish Date
clean_text(text)
Cleans non-UTF-8 characters from the text to ensure the data can be safely inserted into PostgreSQL.

save_to_database(channel_data, videos_data)
Saves channel data and video data into the PostgreSQL database.

Troubleshooting
Character Encoding Issues: If you encounter issues related to character encoding (e.g., special characters not being inserted properly), make sure your PostgreSQL database is using UTF-8 encoding. If necessary, set the encoding using the following command:

sql
Copy code
SET client_encoding TO 'UTF8';
Connection Issues: If you get an error while connecting to PostgreSQL, ensure that the database is running, and the connection string is correct (dbname, user, password, host, port).

API Quotas: The YouTube Data API has usage quotas. If you exceed your quota, you'll need to wait for it to reset or apply for a higher quota in the Google Developer Console.

License
This project is licensed under the MIT License - see the LICENSE file for details.
