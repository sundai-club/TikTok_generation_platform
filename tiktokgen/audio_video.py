from turtle import width
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip, CompositeAudioClip, concatenate_audioclips

from .overlay_text_on_video import subtitles_main

from . import music_gen

def crop_and_resize(video,target_width=1080,target_height=1350):
    # Resize if necessary
    if video.w < target_width or video.h < target_height:
        resize_factor = max(target_width / video.w, target_height / video.h)
        video = video.resize(resize_factor)    
        
    # Calculate the center coordinates of the video
    center_x = video.w / 2
    center_y = video.h / 2
    
    # Calculate the top-left coordinates of the crop box
    crop_x = center_x - target_width / 2
    crop_y = center_y - target_height / 2
    
    # Crop the video
    cropped_video = video.crop(x1=crop_x, y1=crop_y, width=target_width, height=target_height)

    return cropped_video
    
    

# (rohan): added support for bg_music
def combine_video_audio(video_path, audio_path, words, output_path, foreground_img=None):
    # Load the video and audio files
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    # Adjust video length to match audio length by repeating and cutting the video
    repeat_times = int(audio.duration // video.duration) + 1
    videos = [video] * repeat_times
    edited_video = concatenate_videoclips(videos)
    edited_video = edited_video.subclip(0, audio.duration)
    
    # Resize the video to 9:16 aspect ratio and 1080x1920 resolution
    #edited_video = edited_video.resize(newsize=(1080, 1920))
    cropped_video = crop_and_resize(edited_video, target_width=1080,target_height=1350)

    cropped_video = cropped_video.set_audio(audio)
    cropped_video = subtitles_main(words, cropped_video)
    
    print("Ready to add foreground image")
    if foreground_img:
        foreground_img = ImageClip(foreground_img)
        foreground_img = foreground_img.set_duration(cropped_video.duration)
        
        height_max_scale = 0.4
        width_scale = 0.8
        print(foreground_img.h, foreground_img.w)
        if foreground_img.h * width_scale > cropped_video.h * height_max_scale:
            width_scale = cropped_video.h * height_max_scale / cropped_video.w
        final_width = int(cropped_video.w * width_scale)
        print("Final width", final_width)
        foreground_img = foreground_img.resize(width=final_width)
        print(foreground_img.h, foreground_img.w)
        foreground_img = foreground_img.set_position(("center", 200))
        cropped_video = CompositeVideoClip([cropped_video, foreground_img])
        print("Composed Video")
    
    # TODO (rohan): Decide on increasing the playback speed a bit?
    cropped_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

def combine_videos(video_paths, output_path, combined_script):
    # Load all video clips
    video_clips = [VideoFileClip(video) for video in video_paths]
    
    # Concatenate the video clips
    final_clip = concatenate_videoclips(video_clips, method="compose")

    # (rohan): Add a code to generate bg music
    # get duration of audio path
    bg_music_path = None
    prompt_for_music_gen = music_gen.generate_prompt_for_bg_music(combined_script)
    if prompt_for_music_gen:
        filename = f"data/bg_music.mp3"
        bg_music_duration = int(final_clip.duration + 1)
        bg_music_path = music_gen.generate_music(prompt_for_music_gen, bg_music_duration, filename)
        if bg_music_path:
            bg_music = AudioFileClip(bg_music_path).subclip(0, final_clip.duration)
            print('Setting bg music')
            curr_audio = final_clip.audio
            final_audio = CompositeAudioClip([bg_music.volumex(0.075), curr_audio.volumex(4)])
            final_clip = final_clip.set_audio(final_audio)


    #add water mark
    watermark = ImageClip("./web/src/sundai_logo.png")
    watermark = watermark.set_opacity(0.6)
    watermark = watermark.set_duration(final_clip.duration)
    watermark = watermark.set_position(("right", "bottom"))

    final_video = CompositeVideoClip([final_clip, watermark])

    print("Watermark duration:", watermark.duration)
    print("Final video duration:", final_clip.duration)
    print("Final video size:", final_clip.size)

    # Write the final output video to the specified path
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage
#combine_video_audio("../data/video1.mp4", "../data/audio1.wav", "../data/output.mp4")
# combine_video_audio("src/output.mp4", "src/replicate-prediction-evvvrghn4drj60cgd8xrtc403g.wav", "src/output-main.mp4")
