import json
from dotenv import load_dotenv
from omegaconf import OmegaConf
from moviepy.editor import AudioFileClip

load_dotenv()


from .script_snippet_to_audio import extract_text_list, generate_speech_and_transcription
from .audio_video import combine_video_audio, combine_videos

# (rohan): Imports for MusicGen
from . import music_gen

import tiktokgen.graphics as graphics_gen


def pipeline(config='configs/sample.yaml'):
    config = OmegaConf.load(config)
    
    background_generator = graphics_gen.get_generator(config.get("background"))
    background_generator(config.get("script"))

    # i = 0
    # output_video_paths = []
    # for item in prompt:
    #     i += 1
    #     # create audio from script
    #     audio_path, transcription_data = generate_speech_and_transcription(item['text'], filename="Generate_speech_"+str(i))
    #     print(f"Audio File Saved: {audio_path}")
    #     print(f"transcription_data: {transcription_data}")

    #     # combine video and audio
    #     output_video_path = "data/output_"+str(i)+".mp4"
    #     combine_video_audio(item['video_path'], audio_path, transcription_data.words, output_video_path, item['foreground_img'])
    #     output_video_paths.append(output_video_path)
    
    # # combine all videos together
    # # output_video_paths = ['data/output_1.mp4', 'data/output_2.mp4', 'data/output_3.mp4', 'data/output_4.mp4', 'data/output_5.mp4', 'data/output_6.mp4', 'data/output_7.mp4']
    # print(output_video_paths)
    # combined_script = ' '.join([x['text'] for x in script])
    # combine_videos(output_video_paths, output_path, combined_script)

# pipeline(SCRIPT, "data/output.mp4", style='Internet Videos', generate_forground=False)

