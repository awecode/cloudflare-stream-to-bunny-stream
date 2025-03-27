from dotenv import load_dotenv
import os
import requests

# Add video IDs to reencode here
BUNNY_VIDEO_IDS = []

# Set up the API endpoint and headers
load_dotenv()
library_id = os.getenv('BUNNY_VIDEO_LIBRARY_ID')
api_key = os.getenv('BUNNY_API_KEY')
# https://docs.bunny.net/reference/video_reencodevideo
base_url = f"https://video.bunnycdn.com/library/{library_id}/videos"
headers = {
    "AccessKey": api_key,
    "Content-Type": "application/json"
}

# Reencode each video
print("\nReencoding videos...")
for video_id in BUNNY_VIDEO_IDS:
    # Set up the reencode endpoint
    reencode_url = f"{base_url}/{video_id}/reencode"
    
    # Make the POST request to reencode
    response = requests.post(reencode_url, headers=headers)
    
    if response.status_code == 200:
        print(f"✓ Successfully initiated reencoding for video: {video_id}")
    else:
        print(f"✗ Failed to reencode video {video_id}: {response.status_code}")
        print(f"Error: {response.text}")
