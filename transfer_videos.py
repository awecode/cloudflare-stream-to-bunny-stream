# Step 0: Initialize the environment
from dotenv import load_dotenv
import os
import requests
# Load environment variables from .env file
load_dotenv()

# Step 1: Get download links for each video
# Set up the API endpoint and headers
base_url = "https://api.cloudflare.com/client/v4/accounts/{}/stream".format(os.getenv('CF_ACCOUNT_ID'))
headers = {
    "Authorization": "Bearer {}".format(os.getenv('CF_API_TOKEN')),
    "Content-Type": "application/json"
}

# First, get list of all videos
response = requests.get(base_url, headers=headers)

if response.status_code != 200:
    print("Failed to fetch videos:", response.status_code)
    print(response.text)
    exit(1)

videos = response.json()['result']
print(f"\nFound {len(videos)} videos")

# Get download links for each video
video_downloads = []
for video in videos:
    video_uid = video['uid']
    video_name = video.get('meta', {}).get('name', 'Untitled')
    
    # Get video download URL
    download_url = f"{base_url}/{video_uid}/downloads"
    response = requests.get(download_url, headers=headers)
    
    if response.status_code == 200:
        download_data = response.json()['result']
        default_download = download_data.get('default', {})
        
        if default_download.get('status') == 'ready' and default_download.get('url'):
            video_downloads.append({
                'name': video_name,
                'uid': video_uid,
                'download_url': default_download['url']
            })
            print(f"✓ Got download link for: {video_name}")
        else:
            print(f"✗ Download not ready for: {video_name}")
    else:
        print(f"✗ Failed to get download for {video_name}: {response.status_code}")
        print(f"Error: {response.text}")

print(f"\nSuccessfully got download links for {len(video_downloads)} videos")
