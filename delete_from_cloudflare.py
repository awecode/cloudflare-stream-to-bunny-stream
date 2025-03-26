import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_all_videos():
    # Set up the API endpoint and headers
    base_url = "https://api.cloudflare.com/client/v4/accounts/{}/stream".format(os.getenv('CF_ACCOUNT_ID'))
    headers = {
        "Authorization": "Bearer {}".format(os.getenv('CF_API_TOKEN')),
        "Content-Type": "application/json"
    }

    # Get list of all videos
    response = requests.get(base_url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch videos:", response.status_code)
        print(response.text)
        exit(1)
    
    return response.json()['result']

def delete_video(video_uid, headers):
    base_url = "https://api.cloudflare.com/client/v4/accounts/{}/stream".format(os.getenv('CF_ACCOUNT_ID'))
    delete_url = f"{base_url}/{video_uid}"
    
    response = requests.delete(delete_url, headers=headers)
    return response.status_code == 200

def main():
    # Set up headers
    headers = {
        "Authorization": "Bearer {}".format(os.getenv('CF_API_TOKEN')),
        "Content-Type": "application/json"
    }

    # Get all videos
    videos = get_all_videos()
    
    if not videos:
        print("No videos found in Cloudflare Stream.")
        return

    # Display warning and video list
    print("\n⚠️  WARNING: This will delete ALL videos from your Cloudflare Stream account!")
    print(f"Found {len(videos)} videos to delete:")
    print("\nVideos to be deleted:")
    print("-" * 50)
    for video in videos:
        video_name = video.get('meta', {}).get('name', 'Untitled')
        print(f"- {video_name} (ID: {video['uid']})")
    print("-" * 50)
    
    # Ask for confirmation
    print("\n⚠️  This action cannot be undone!")
    confirmation = input("\nType 'agree' to confirm deletion: ")
    
    if confirmation.lower() != 'agree':
        print("\nDeletion cancelled.")
        return
    
    # Proceed with deletion
    print("\nStarting deletion process...")
    success_count = 0
    fail_count = 0
    
    for video in videos:
        video_name = video.get('meta', {}).get('name', 'Untitled')
        video_uid = video['uid']
        
        if delete_video(video_uid, headers):
            print(f"✓ Successfully deleted: {video_name}")
            success_count += 1
        else:
            print(f"✗ Failed to delete: {video_name}")
            fail_count += 1
    
    # Print summary
    print("\nDeletion Summary:")
    print(f"Successfully deleted: {success_count} videos")
    print(f"Failed to delete: {fail_count} videos")
    print(f"Total videos processed: {len(videos)}")

if __name__ == "__main__":
    main()
