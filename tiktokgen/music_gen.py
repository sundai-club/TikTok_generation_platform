'''
Open Source model Self Hosting

# pip install transformers
# pip install scipy
#text conditional generation

import scipy
from transformers import AutoProcessor, MusicgenForConditionalGeneration

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

def generate_music(prompt: str, save_path: str):
    inputs = processor(
        text=["indian classical instrumental", "90s rock song with loud guitars and heavy drums"],
        padding=True,
        return_tensors="pt",
    )
    audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=256)


    sampling_rate = model.config.audio_encoder.sampling_rate
    scipy.io.wavfile.write("indian_music_drums.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())
'''

import openai
import os
import re
import replicate
import requests
from typing import Optional

sys_prompt = f'''You are an expert at creating prompts for AI systems that generate background music for movies and theater and videos.

The user will give you text from the script and your job is to first think out loud what the mood of the script is. What should be the target mood for the script. Any music references you can think of that would go nicely. Any modifications to these references that would better suit the mood you described and the script.

While responding generate 2 sections. Section 1 will be all the planning that we mentioned above and it will be enclosed in triple backticks like ```planning ... ```. Section 2 will be a simple text again enclosed in ```ai_prompt ... ```.

Generate 5 samples each separated using double newline chars ('\n\n').

Example Output:

```planning
The mood of this script is exhilarating and groundbreaking. It aims to leave the audience in awe of the technological advancements. The target mood should be thrilling, awe-inspiring, and progressive.

Music references that align well:
1. "Time" by Hans Zimmer from Inception
2. Michael Giacchino's "Roar! (Cloverfield Overture)"
3. Ramin Djawadi's "Pacific Rim"
4. Audiomachine's "Blood and Stone"

Modifications:
- Utilize powerful, resonant chords to emphasize the groundbreaking aspect.
- Add electronic and synthetic layers to highlight technology.
- Focus on a high-energy buildup to keep the audience engaged.
```
```ai_prompt
Create a thrilling and awe-inspiring soundtrack that incorporates powerful, resonant chords to emphasize the groundbreaking aspect of technological advancements. Utilize a mix of electronic and synthetic layers to highlight the cutting-edge technology, building up to a high-energy climax that leaves the audience in awe.

Compose a cinematic score that captures the essence of innovation and progress, drawing inspiration from the likes of Hans Zimmer and Michael Giacchino. Focus on creating a sense of tension and anticipation, culminating in a breathtaking reveal that showcases the thrill of discovery.

Design an energetic and pulsating soundtrack that embodies the spirit of technological revolution. Incorporate driving rhythms and soaring melodies, blending electronic and orchestral elements to create a sense of unstoppable momentum. Aim to evoke a sense of wonder and excitement in the audience.

Craft a dramatic and awe-inspiring theme that highlights the intersection of human ingenuity and technological advancement. Draw inspiration from Ramin Djawadi's "Pacific Rim" and Audiomachine's "Blood and Stone," emphasizing the sense of scale and majesty that comes with pushing the boundaries of what is possible.

Create a heart-pumping, adrenaline-fueled soundtrack that propels the audience through a thrilling journey of discovery and exploration. Utilize a combination of electronic and synthetic elements to create a sense of futuristic excitement, building up to a triumphant finale that leaves the audience breathless and inspired.
```

Keep the format like this!
'''

def generate_prompt_for_bg_music(script: str) ->Optional[str]:
    max_iterations = 3
    while max_iterations > 0:
        try:
            client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])
            res = client.chat.completions.create(
                model = "gpt-4o",
                messages=[{'role': 'system', 'content': sys_prompt}, {'role': 'user', 'content': script}],
                max_tokens=1024,
                stop=['---'],
            )
            output = res.choices[0].message.content
            ptrn = re.compile(r'```ai_prompt(.*?)```', re.DOTALL)
            prompt_options = [x for x in re.search(ptrn, output).group(1).strip().split('\n\n') if x]
            ret = prompt_options[0]
            print('Music Prompt:', ret)
            return ret
        except Exception as e:
            print(e)
            max_iterations -= 1

def generate_music(prompt: str, duration: int, save_path: str) -> Optional[str]:
    output = replicate.run(
        "meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
        input={
            "top_k": 250,
            "top_p": 0,
            "prompt": prompt,
            "duration": duration,
            "temperature": 1,
            "continuation": False,
            "model_version": "stereo-large",
            "output_format": "mp3",
            "continuation_start": 0,
            "multi_band_diffusion": False,
            "normalization_strategy": "peak",
            "classifier_free_guidance": 3
        }
    )
    res = requests.get(output)
    if res.status_code == 200:
        with open(save_path, 'wb') as f: f.write(res.content)
        return save_path
    return None
