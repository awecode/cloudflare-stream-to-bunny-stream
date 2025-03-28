import os
import requests
import json
from dotenv import load_dotenv

# Leave empty to allow all cloudflare stream video ids
ALLOWED_VIDEOS_IDS = []

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

    if len(ALLOWED_VIDEOS_IDS) > 0 and video_uid not in ALLOWED_VIDEOS_IDS:
        continue

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

# Step 2: Create video objects in Bunny.net

# For each video, create a video object in Bunny.net

bunny_base_url = f"https://video.bunnycdn.com/library/{os.getenv('BUNNY_VIDEO_LIBRARY_ID')}/videos"
bunny_headers = {
    "AccessKey": os.getenv('BUNNY_API_KEY'),
    "accept": "application/json",
    "content-type": "application/json"
}

# Step 2: Fetch video files from Cloudflare and upload to Bunny.net
cloudflare_to_bunny_map = {}

for video in video_downloads:
    # Construct fetch URL for Bunny.net
    fetch_url = f"{bunny_base_url}/fetch"
    
    # Make fetch request to Bunny.net with Cloudflare download URL
    fetch_response = requests.post(
        fetch_url,
        headers=bunny_headers,
        json={"url": video['download_url'], "title": video['name']}
    )
    
    if fetch_response.status_code == 200:
        bunny_video_id = fetch_response.json()['id']
        cloudflare_to_bunny_map[video['uid']] = bunny_video_id
        print(f"✓ Started fetch for video: {video['name']}")
    else:
        print(f"✗ Failed to fetch video {video['name']}: {fetch_response.status_code}")
        print(f"Error: {fetch_response.text}")

print("\nFinished initiating video fetches in Bunny.net")

print("\nMapping:")
print(json.dumps(cloudflare_to_bunny_map, indent=2))
