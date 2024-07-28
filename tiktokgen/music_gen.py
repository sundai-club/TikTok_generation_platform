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

import replicate
import requests

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
        with open(save_path, 'rb') as f: f.write(res.content)
        return save_path
    return None
