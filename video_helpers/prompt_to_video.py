import replicate
import requests
import os

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
MODEL_INFINITE_ZOOM = "arielreplicate/stable_diffusion_infinite_zoom:a2527c5074fc0cf9fa6015a40d75d080d1ddf7082fabe142f1ccd882c18fce61"

def prompt_to_video(model=MODEL_INFINITE_ZOOM, 
                    parsed_script = TEST_SCRIPT):
    result = []
    i = 0
    for snippet in parsed_script:
        input = {
            "prompt": snippet.get("prompt"),
            "inpaint_iter": 4
        }
        i += 1

        output = replicate.run(
            model,
            input=input
        )
        print(output)
        snippet["url"] = output.get("mp4")
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