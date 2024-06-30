import replicate

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
    for snippet in parsed_script:
        input = {
            "prompt": snippet.get("prompt")
        }

        output = replicate.run(
            model,
            input=input
        )
        snippet["mp4"] = output.get("mp4")
        result.append(snippet)

    return result