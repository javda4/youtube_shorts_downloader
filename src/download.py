import os
import datetime
import pytube
import request
from googleapiclient.discovery import build

# YouTube Data API credentials
API_KEY = ''


def get_most_viewed_shorts():
    # Build YouTube Data API client
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Calculate the start and end date for the past week
    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=7)

    # Format the dates for the API request
    start_date_str = start_date.strftime('%Y-%m-%dT00:00:00Z')
    end_date_str = end_date.strftime('%Y-%m-%dT23:59:59Z')

    # Make API request to get the most viewed YouTube shorts of the week
    request = youtube.search().list(
        part='id',
        q='shorts',
        maxResults=10,
        type='video',
        videoDuration='short',
        order='viewCount',
        publishedAfter=start_date_str,
        publishedBefore=end_date_str
    )
    response = request.execute()

    # Extract video IDs
    video_ids = [item['id']['videoId'] for item in response['items']]

    return video_ids


def download_shorts(video_ids):
    for video_id in video_ids:
        try:
            # Create a YouTube video URL
            url = f'https://www.youtube.com/watch?v={video_id}'

            # Create a PyTube YouTube object
            youtube = pytube.YouTube(url)

            # Get the highest resolution video stream
            stream = youtube.streams.get_highest_resolution()

            # Download the video
            print(f'Downloading video: {video_id}')
            stream.download()

            print(f'Video {video_id} downloaded successfully!')

        except Exception as e:
            print(f'Error downloading video {video_id}: {str(e)}')


if __name__ == '__main__':
    # Create a directory for the downloaded videos
    os.makedirs('youtube_shorts', exist_ok=True)
    os.chdir('youtube_shorts')

    # Get the most viewed YouTube shorts of the week
    video_ids = get_most_viewed_shorts()

    # Download the videos
    download_shorts(video_ids)
    directory_path = os.getcwd()
    print(f'Videos are saved in the directory: {directory_path}')
