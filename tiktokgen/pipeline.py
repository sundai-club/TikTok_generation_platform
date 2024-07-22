from .prompt_to_stock_video import prompt_to_stock_video
from .prompt_to_video import prompt_to_video, find_model
from .prompt_to_image import prompts_to_foreground_images
from .script_to_prompt import gpt_step_0, gpt_step_1
import json

from .script_snippet_to_audio import extract_text_list, generate_speech_and_transcription
from .audio_video import combine_video_audio, combine_videos


def pipeline(script, output_path, style, generate_forground=True):
    model = find_model(style)

    parsed_script = [{"text": t["text"]} for t in script] 
    # Convert parsed_script into a prity print string of the json
    parsed_script = json.dumps(parsed_script, indent=4)
    print("parsed_script_1", parsed_script)
    parsed_script = gpt_step_1(parsed_script, model["prompt"])
    print("parsed_script_2", parsed_script)
    parsed_script = [{
        "text": script[k]["text"],
        "foreground_img": script[k]["foreground_img"],
        "prompt": parsed_script[k]["prompt"]} 
            for k in range(len(parsed_script))
    ]
    
    if style == 'Internet Videos':
        prompt = prompt_to_stock_video(parsed_script = parsed_script)
        print (f'Internet videos output: ' + str(prompt))
    else:
        prompt = prompt_to_video(parsed_script = parsed_script, style = style)
        print (f'Replicate videos output: ' + str(prompt))
        
    # Generate foreground images with Stable Diff
    if generate_forground:
        print(f'\n\nForeground images input: ' + str(prompt))
        prompt = prompts_to_foreground_images(parsed_script=parsed_script)
        print(f'\n\nForeground images output: ' + str(prompt))
    
    i = 0
    output_video_paths = []
    for item in prompt:
        i += 1
        # create audio from script
        audio_path, transcription_data = generate_speech_and_transcription(item['text'], filename="Generate_speech_"+str(i))
        print(f"Audio File Saved: {audio_path}")
        print(f"transcription_data: {transcription_data}")
        # combine video and audio
        output_video_path = "data/output_"+str(i)+".mp4"
        combine_video_audio(item['video_path'], audio_path, transcription_data.words, output_video_path, item['foreground_img'])
        output_video_paths.append(output_video_path)
    
    # combine all videos together
    # output_video_paths = ['../data/output_1.mp4', '../data/output_2.mp4', '../data/output_3.mp4', '../data/output_4.mp4', '../data/output_5.mp4', '../data/output_6.mp4', '../data/output_7.mp4']
    print(output_video_paths)
    combine_videos(output_video_paths, output_path)
        
        
SCRIPT = [
    {
        "text": "Imagine controlling a swarm of drones in the sky without them crashing into each other. Sounds impossible? Well, not anymore!",
        "foreground_img": None
    },
    {
        "text": "In air traffic control, autonomous vehicles, and robotics, the order in which decisions are made can mean the difference between seamless coordination and catastrophic failure. Optimizing this order is critical for safety and efficiency.",
        "foreground_img": "data/img_samples/2.png"
    },
    {
        "text": "Researchers at Princeton have developed a groundbreaking algorithm called Branch-and-Play. Think of it as a master conductor for robots, ensuring they play their parts in perfect harmony, avoiding collisions and delays.",
        "foreground_img": "data/img_samples/3.png"
    },
    {
        "text": "This algorithm was tested in air traffic control, drone swarms, and delivery fleets, consistently outperforming other methods. It finds the best sequence for decisions, achieving the safest and most efficient outcomes.",
        "foreground_img": "data/img_samples/4.png"
    },
    {
        "text": "What\’s next? Integrating this algorithm into real-world applications like city traffic management and advanced robotics, pushing the boundaries of what\’s possible with autonomous systems.",
        "foreground_img": "data/img_samples/5.png"
    },
    {
        "text": "What do you think about using AI to optimize decision-making in robots? Where else could this be useful? Let us know in the comments!",
        "foreground_img": None
    }
]

pipeline(SCRIPT, "data/output.mp4", style='Internet Videos', generate_forground=False)

