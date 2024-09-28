from .prompt_to_stock_video import prompt_to_stock_video, prompt_to_local_videos
from .prompt_to_video import prompt_to_video, find_model
from .prompt_to_image import prompts_to_foreground_images
from .prompt_to_instagram_videos import prompt_to_instagram_videos
from .script_to_prompt import gpt_step_0, gpt_step_1
import json

from .script_snippet_to_audio import extract_text_list, generate_speech_and_transcription
from .audio_video import combine_video_audio, combine_videos

# (rohan): Imports for MusicGen
from moviepy.editor import AudioFileClip
from . import music_gen


def agent_pipeline(script, output_path, style, generate_forground=True):
    prompt = prompt_to_local_videos(script, use_presaved_annotations=True)
    
    i = 0
    output_video_paths = []
    for item in script:
        i += 1
        # create audio from script
        audio_path, transcription_data = generate_speech_and_transcription(item['text'], filename="Generate_speech_"+str(i))
        print(f"Audio File Saved: {audio_path}")
        print(f"transcription_data: {transcription_data}")

        # combine video and audio
        output_video_path = "data/output_"+str(i)+".mp4"
        combine_video_audio(item['video_path'], audio_path, transcription_data.words, output_video_path, None)
        output_video_paths.append(output_video_path)

    # combine all videos together
    #output_video_paths = ['./data/output_1.mp4', './data/output_2.mp4', './data/output_3.mp4']#, '../data/output_4.mp4', '../data/output_5.mp4', '../data/output_6.mp4', '../data/output_7.mp4']
    print(output_video_paths)
    combined_script = ' '.join([x['text'] for x in script])
    combine_videos(output_video_paths, output_path, combined_script)