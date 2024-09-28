from litellm import completion
from dotenv import load_dotenv
from tqdm import tqdm
import os
import requests
import json
import subprocess
import random
from .media_to_text import describe_media

from ai21 import AI21Client
from ai21.models.chat import ChatMessage

a21client = AI21Client()





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
    
  print("Stock video keywords: ", query_kerywords)
  # out:
  # stock video

  # This line of code is making a GET request to the Pexels API to search for videos based on the
  # query keywords obtained earlier in the script. Here is a breakdown of the components:
  video_res = requests.get(
      "https://api.pexels.com/videos/search?&query=" + query_kerywords + "&per_page=1", #orientation=portrait
      headers={"Authorization": os.getenv("PEXELS_API_KEY")},
      timeout=30  # Increase the timeout to 30 seconds
  )

  print("\n\n\n" + video_res.text + "\n\n\n")
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


def run_data_description(local_media_path):
  print("Annotating videos...")
  
  acceptible_media_ext = lambda x: x.endswith('.mp4') or x.endswith('.png') or x.endswith('.mov') or x.endswith('.MOV')
  local_files = [os.path.join(local_media_path, f) for f in os.listdir(local_media_path) if acceptible_media_ext(f)]
  print("Local files: ", local_files)
  
  annotations = {}
  for f in local_files:
    annotations[f] = describe_media(f)
    with open("data/local_media/video_annotations.json", "w") as file:
      json.dump(annotations, file)
  
  print("Finished annotating videos")
  return annotations

def generate_aligment(descriptions, script_texts):
  
  full_video_description = "\n".join([f"{i}. {desc}" for i, desc in enumerate(descriptions)])
  
  
  messages = [
    ChatMessage(content="""
      You are a helpful agent that can choose the best video for a given script.
      You will be given a script and a list of videos. You need to choose the best video for each scene in the script.
      You need to return the index of the video that you think is the best for each of the scenes in the script.
      Make sure the the nymber of indices is the same as the number of scenes in the script.
      Return your response in the following format:
        idx_1, idx_2, ..., idx_n
      Do not repeat the indices. Make sure that the indices are valid.
    """, role="system"),
    ChatMessage(content=f"""
      Video descriptions:
      {full_video_description}
      
      Script texts:
      {script_texts}
    """, role="user")
  ]
  response = a21client.chat.completions.create(
  messages=messages,
  model="jamba-1.5-large",
  stream=True
)

  final_response = ""
  for chunk in response:
    cur_response = chunk.choices[0].delta.content
    if cur_response is not None:
      final_response += cur_response

  # convert to list of ints
  final_response = final_response.replace(".", "")
  print(final_response)
  
  parsed_response = [int(x) for x in final_response.split(",")]
  parsed_response = [max(x, 0) for x in parsed_response]
  parsed_response = [min(x, len(descriptions) - 1) for x in parsed_response]
  
  if len(parsed_response) > len(script_texts):
    parsed_response = parsed_response[:len(script_texts)]
  if len(parsed_response) < len(script_texts):
    # augment with random indices
    parsed_response = parsed_response + [random.randint(0, len(descriptions) - 1) for _ in range(len(script_texts) - len(parsed_response))]
  return parsed_response


def prompt_to_local_videos(script, filedir="data", local_media_path="data/local_media", use_presaved_annotations=False):
  if use_presaved_annotations:
    with open("data/local_media/video_annotations.json", "r") as file:
      annotations = json.loads(file.read())
  else:
    annotations = run_data_description(local_media_path)
    
  video_paths = list(annotations.keys())
  video_descriptions = [annotations[p].replace("\n", " ") for p in video_paths]
  
  if not os.path.exists(filedir):
    os.makedirs(filedir) 
    
  #concatenate descriptions with a number in front of them
  parsed_script = [snippet.get('text') for i, snippet in enumerate(script)]
  indices = generate_aligment(video_descriptions, parsed_script)
  
  print(indices)
  for i, snippet in enumerate(script):
    snippet["video_path"] = os.path.join(filedir, 'video_'+str(i)+'.mp4')
    orig_video_path = video_paths[indices[i]]
    
    # convert the original video from .MOV to .mp4
    if orig_video_path.endswith('.MOV'):
      print(f"Converting {orig_video_path} to .mp4")
      subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', orig_video_path, '-c:v', 'libx264', snippet["video_path"]])
  
  return script

