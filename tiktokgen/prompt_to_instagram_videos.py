from litellm import completion
from dotenv import load_dotenv
from tqdm import tqdm
import os
import requests
from dotenv import load_dotenv, find_dotenv

from apify_client import ApifyClient
import requests

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Initialize the ApifyClient with your API token
APIFY_API_KEY = "apify_api_CP7KyH7SaM98Z15LsuHm03pNj3OFuR2lvAFv" #os.getenv("APIFY_API_KEY")
print(f"Initializing Apify Client... with key: !{APIFY_API_KEY}!")
apify_client = ApifyClient(APIFY_API_KEY)

def scrape_instagram_video(hashtag, save_path):
    # Prepare the Actor input
    run_input = {
        "hashtags": [hashtag],
        "resultsPerPage": 1,
        "excludePinnedPosts": False,
        "searchSection": "",
        "maxProfilesPerQuery": 2,
        "shouldDownloadVideos": True,
        "shouldDownloadCovers": False,
        "shouldDownloadSubtitles": False,
        "shouldDownloadSlideshowImages": True,
    }

    # Run the Actor and wait for it to finish
    run = apify_client.actor("shu8hvrXbJbY3Eb9W").call(run_input=run_input)
    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items():
        video_url=item['mediaUrls'][0]
        # The local path where the video will be saved]
        print(run_input["hashtags"])
        # save_path = run_input["hashtags"][0]+'_'+str(item['id']) + ".mp4"

        # Send a GET request to the video URL
        # Send a GET request to the video URL
        response = requests.get(video_url, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            # Open a file in write-binary mode
            with open(save_path, 'wb') as file:
                # Write the content of the response to the file in chunks
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Video successfully downloaded and saved to {save_path}")
            return save_path
        else:
            print(f"Failed to download video. Status code: {response.status_code}")

def prompt_to_instagram_videos(parsed_script, save_dir="data"):
  print("Getting videos from Instagram...")
  result = []
  
  for i, snippet in enumerate(tqdm(parsed_script)):
      result.append(
        scrape_instagram_video(
          snippet.get("prompt"), 
          os.path.join(save_dir, 'video_'+str(i)+'.mp4')
        )
      )

  return result
