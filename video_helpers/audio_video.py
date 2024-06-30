from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def combine_video_audio(video_path, audio_path, output_path):
    
    # Load the video and audio files
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    # Adjust video length to match audio length by repeating and cutting the video
    repeat_times = int(audio.duration // video.duration) + 1
    videos = [video] * repeat_times
    edited_video = concatenate_videoclips(videos)
    edited_video = edited_video.subclip(0, audio.duration)
    
    # Resize the video to 9:16 aspect ratio and 1080x1920 resolution
    edited_video = edited_video.resize(newsize=(1080, 1920))
    
    edited_video = edited_video.set_audio(audio)
    edited_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage
combine_video_audio("../data/video1.mp4", "../data/audio1.wav", "../data/output.mp4")