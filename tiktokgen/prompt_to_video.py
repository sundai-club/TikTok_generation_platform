import replicate
import requests
import os
import json

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

style_json = [
  {
        "name": "Local video",
        "prompt": "Each 'text' section in the following code is a part of a script. Come up a unique scene for each section."
  },
  {
      "name": "Internet Videos",
      "prompt": "Each 'text' section in the following code is a part of a script. Come up a unique scene for each section."
  },
  {
      "name": "Infinite Zoom",
      "model": "arielreplicate/stable_diffusion_infinite_zoom:a2527c5074fc0cf9fa6015a40d75d080d1ddf7082fabe142f1ccd882c18fce61",
      "prompt": "Each 'text' section in the following code is a part of a script. Come up a unique scene for each section. These should be place-specific scenes, such as the middle aisle of an airplane, a path through a tropical jungle, or the middle of a city street surrounded by high-rises. Write a short succinct clear prompt (max 9 words) to generate each video.",
      "modelInput": {
          "inpaint_iter": 3
      }
  },
  {
      "name": "Anime",
      "model": "lucataco/animate-diff:beecf59c4aee8d81bf04f0381033dfa10dc16e845b4ae00d281e2fa377e48a9f",
      "prompt": "Each 'text' section in the following code is a part of a script. Each prompt should be a series of adjectives of a concrete object(such as a place or a person), such as'masterpiece, best quality, 1girl, solo, cherry blossoms, hanami, pink flower, white flower, spring season, wisteria, petals, flower, plum blossoms, outdoors, falling petals, white hair, black eyes'. Write a clear prompt (at least 18 words) to generate each video.",
      "modelInput": {
          "path": "toonyou_beta3.safetensors",
          "seed": 255224557,
          "steps": 10,
          "n_prompt": "badhandv4, easynegative, ng_deepnegative_v1_75t, verybadimagenegative_v1.3, bad-artist, bad_prompt_version2-neg, teeth",
          "motion_module": "mm_sd_v14",
          "guidance_scale": 7.5
      }
  }
]

def find_model(style):
    print('Video style json file loaded successfully!')
    for model in style_json:
        if model['name'] == style:
            print('Found model preference: ')
            print(model)
            return model
    print (f'{style} does not exist in the json file.')
    return None

def process_replicate_output(output):
    if isinstance(output, str):
        return output
    elif isinstance(output, dict) and "mp4" in output:
        return output["mp4"]
    else:
        return None 

def prompt_to_video(parsed_script, style):
    
    #find the model parameters in json file
    model = find_model(style)

    if model:
      model_id = model['model']
      model_input = model['modelInput']

      result = []
      i = 0
      for snippet in parsed_script:
          print("Snippet: ", snippet)
          model_input['prompt'] = snippet['prompt']
          print(f'Ready to run {style} model with input: ')
          print(model_input)
          
          i += 1

          output = replicate.run(
              model_id,
              input = model_input
          )
          snippet["url"] = process_replicate_output(output)
          print(f'Replicate has returned output: ')
          print(output)

          #download the video from the returned replicate url
          response = requests.get(snippet["url"])
          if not os.path.exists("data"):         
              # if the demo_folder directory is not present  
              # then create it. 
              os.makedirs("data") 

          snippet["video_path"] = 'data/video_'+str(i)+'.mp4'
          with open(snippet["video_path"], 'wb') as file:
            # Write the content of the response to the file
            file.write(response.content)

          result.append(snippet)
      return result

#example
# test_result = prompt_to_video(parsed_script = YOUR_SCRIPT)
# print(test_result)
# [{'text': 'In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go.', 'prompt': 'Discussing travel efficiency and remote living', 'mp4': 'https://replicate.delivery/yhqm/cgSR0J05zFI4Bl6pVZvlGVG4TQIQpY3fME5FOXsedUaEI3DTA/infinit_zoom.mp4'%7D, {'text': 'Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere.', 'prompt': 'Introducing digital mail for nomads', 'mp4': 'https://replicate.delivery/yhqm/HCWOIYoB3exMW6kyvn8YfrIsfjxvWfB5X7KjxjxRWarOhcPMB/infinit_zoom.mp4'%7D]

if __name__ == "__main__":
    prompt_to_video()
