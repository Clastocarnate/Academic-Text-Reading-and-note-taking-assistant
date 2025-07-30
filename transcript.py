import os
import time
import json
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
CHANNEL_NAME = "3Blue1Brown"
API_KEY = "AIzaSyDIVBO6Gw2-KDt9CCyP0Ou6AmdFjlLVTsA"  # Get from Google Cloud Console
OUTPUT_FILE = "kurzgesagt_transcripts.txt"
MAX_RESULTS = 50  # Number of videos to process per API call

def get_channel_id(api_key, channel_name):
    """Get channel ID from channel name"""
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    try:
        search_response = youtube.search().list(
            q=channel_name,
            type='channel',
            part='id,snippet',
            maxResults=1
        ).execute()
        
        if search_response['items']:
            return search_response['items'][0]['id']['channelId']
        else:
            print(f"Channel '{channel_name}' not found")
            return None
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return None

def get_channel_videos(api_key, channel_id, max_results=50):
    """Get all video IDs from a channel"""
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_ids = []
    next_page_token = None
    
    try:
        while True:
            # Get channel's uploads playlist ID
            channel_response = youtube.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            playlist_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=max_results,
                pageToken=next_page_token
            ).execute()
            
            # Extract video IDs and titles
            for item in playlist_response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video_title = item['snippet']['title']
                video_ids.append((video_id, video_title))
            
            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break
                
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
    
    return video_ids

def get_transcript(video_id):
    """Get transcript for a single video"""
    try:
        # Try different methods based on library version
        try:
            # Method for newer versions of youtube-transcript-api
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            try:
                # Try to get manually created transcript first
                transcript = transcript_list.find_manually_created_transcript(['en'])
                transcript_data = transcript.fetch()
            except:
                try:
                    # Fall back to auto-generated transcript
                    transcript = transcript_list.find_generated_transcript(['en'])
                    transcript_data = transcript.fetch()
                except:
                    # Try any available transcript and translate to English
                    available_transcripts = list(transcript_list)
                    if available_transcripts:
                        transcript = available_transcripts[0].translate('en')
                        transcript_data = transcript.fetch()
                    else:
                        return None
        
        except AttributeError:
            # Method for older versions of youtube-transcript-api
            # Try different language codes
            language_codes = ['en', 'en-US', 'en-GB']
            transcript_data = None
            
            for lang_code in language_codes:
                try:
                    transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang_code])
                    break
                except:
                    continue
            
            # If no English transcript found, try getting any available transcript
            if not transcript_data:
                try:
                    transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
                except:
                    return None
        
        # Combine all text
        if transcript_data:
            full_text = ' '.join([entry['text'] for entry in transcript_data])
            return full_text
        else:
            return None
        
    except Exception as e:
        print(f"Could not retrieve transcript for video {video_id}: {str(e)}")
        return None

def main():
    # Check if API key is set
    if API_KEY == "YOUR_YOUTUBE_API_KEY_HERE":
        print("Please set your YouTube API key in the API_KEY variable")
        print("Get your API key from: https://console.cloud.google.com/")
        return
    
    print(f"Starting transcript scraping for channel: {CHANNEL_NAME}")
    
    # Get channel ID
    print("Getting channel ID...")
    channel_id = get_channel_id(API_KEY, CHANNEL_NAME)
    if not channel_id:
        return
    
    print(f"Channel ID: {channel_id}")
    
    # Get all video IDs
    print("Getting video list...")
    video_data = get_channel_videos(API_KEY, channel_id, MAX_RESULTS)
    print(f"Found {len(video_data)} videos")
    
    # Create or open output file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"Transcripts from {CHANNEL_NAME}\n")
        f.write("=" * 50 + "\n\n")
        
        successful = 0
        failed = 0
        
        for i, (video_id, video_title) in enumerate(video_data, 1):
            print(f"Processing video {i}/{len(video_data)}: {video_title}")
            
            transcript = get_transcript(video_id)
            
            if transcript:
                f.write(f"VIDEO: {video_title}\n")
                f.write(f"URL: https://youtube.com/watch?v={video_id}\n")
                f.write("-" * 30 + "\n")
                f.write(transcript)
                f.write("\n\n" + "=" * 50 + "\n\n")
                successful += 1
            else:
                f.write(f"FAILED TO GET TRANSCRIPT: {video_title}\n")
                f.write(f"URL: https://youtube.com/watch?v={video_id}\n")
                f.write("-" * 30 + "\n\n")
                failed += 1
            
            # Add delay to be respectful to the API
            time.sleep(1)
    
    print(f"\nCompleted! Successfully processed {successful} videos, {failed} failed.")
    print(f"Results saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()