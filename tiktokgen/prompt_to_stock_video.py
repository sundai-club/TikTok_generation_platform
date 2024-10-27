from litellm import completion
from dotenv import load_dotenv
from tqdm import tqdm
import os
import requests


TEST_SCRIPT= [
  {
    "text": "In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go.",
    "prompt": "Discussing travel efficiency and remote living"
  },
  {
    "text": "Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere.",
    "prompt": "Introducing digital mail for nomads"
  }
]


def script2url(script, augment_prompt=True):
  # through 1:
  # scene
  if augment_prompt:
    scene_res = completion(
      model="gpt-3.5-turbo",
      messages=[
        { "content": "Imagine the following script is a part of a video book. What is the perfect background video for the script? It can only be a single shot of some scene: \n" + script, "role": "user"}
        ]
    )

    # through 2:
    # query keywords

    query_keywords_res = completion(
      model="gpt-4o",
      messages=[
        { "content": "Imagine the following script is a part of a video book. What is the perfect background video for the script? It can only be a single shot of some scene" + script, "role": "user"}, 
        scene_res.choices[0].message, 
        { "content": "Describe this video with up to 5 keywords for a video search query. Write them single line, space separated", "role": "user"}
        ]
    )
    query_kerywords = query_keywords_res.choices[0].message["content"].replace("\n", "").replace(".", "").replace(",", "").lower()
  else:
    query_kerywords = script
  # out:
  # stock video
  
  # print("Query keywords: ", query_kerywords, os.getenv("PEXELS_API_KEY"))

  # This line of code is making a GET request to the Pexels API to search for videos based on the
  # query keywords obtained earlier in the script. Here is a breakdown of the components:
  try:
      video_res = requests.get(
          "https://api.pexels.com/videos/search?orientation=portrait&query=" + query_kerywords + "&per_page=1",
          headers={
            "Authorization": os.getenv("PEXELS_API_KEY"),
            "User-Agent": "Not Python"
          },
          timeout=30  # Increase the timeout to 30 seconds
      )
      video_res.raise_for_status()  # Raise an error for bad status codes
      
  except requests.exceptions.RequestException as e:
      print(f"Failed to fetch video from Pexels API: {str(e)}")
      return None
  except requests.exceptions.Timeout:
      print("Request to Pexels API timed out after 30 seconds")
      return None
    
  print("\n\n\n Video Return result" + video_res.text + "\n\n\n")
  video_res = video_res.json()
  
  print(video_res.keys())
  print(video_res)
  
  video_url = video_res["videos"][0]["video_files"][0]["link"]

  return video_url


def prompt_to_stock_video(parsed_script, filedir="data", augment_prompt=True):
  print("Getting videos...")
  result = []
  
  for i, snippet in enumerate(tqdm(parsed_script)):    
      print("Snippet: ", snippet)  
      output_url = script2url(snippet.get("prompt"), augment_prompt=augment_prompt)
      snippet["url"] = output_url
      response = requests.get(snippet["url"])

      if not os.path.exists(filedir):
          os.makedirs(filedir) 

      snippet["video_path"] = os.path.join(filedir, 'video_'+str(i)+'.mp4')
      with open(snippet["video_path"], 'wb') as file:
        # Write the content of the response to the file
        file.write(response.content)

      result.append(snippet)

  return result
