# Step 0: Initialize the environment
from dotenv import load_dotenv
import os
import requests
# Load environment variables from .env file
load_dotenv()

# Print environment variables
print("Cloudflare Account ID:", os.getenv('CF_ACCOUNT_ID'))
print("Cloudflare API Token:", os.getenv('CF_API_TOKEN'))

# Step 1: List all videos in Cloudflare Stream

# Set up the API endpoint and headers
base_url = "https://api.cloudflare.com/client/v4/accounts/{}/stream".format(os.getenv('CF_ACCOUNT_ID'))
headers = {
    "Authorization": "Bearer {}".format(os.getenv('CF_API_TOKEN')),
    "Content-Type": "application/json"
}

# Make the API request to list all videos
response = requests.get(base_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    videos = response.json()['result']
    print("\nFound {} videos:".format(len(videos)))
    for video in videos:
        # Some videos may not have meta.name, so use get() with a default value
        video_name = video.get('meta', {}).get('name', 'Untitled')
        print(f"- {video_name} (ID: {video['uid']})")
else:
    print("Failed to fetch videos:", response.status_code)
    print(response.text)

# Step 2: Enable download for each video
print("\nEnabling downloads for each video...")
for video in videos:
    video_uid = video['uid']
    video_name = video.get('meta', {}).get('name', 'Untitled')
    
    # Set up the API endpoint for enabling downloads
    download_url = f"{base_url}/{video_uid}/downloads"
    
    # Make the POST request to enable downloads
    response = requests.post(download_url, headers=headers)
    
    if response.status_code == 200:
        print(f"✓ Successfully enabled downloads for: {video_name}")
    else:
        print(f"✗ Failed to enable downloads for {video_name}: {response.status_code}")
        print(f"Error: {response.text}")

# Step 3: Download the video

# Step 4: Upload the video to Bunny.net

