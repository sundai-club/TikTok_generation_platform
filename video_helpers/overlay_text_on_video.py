from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Load the video file
video = VideoFileClip("/mnt/data/output.mp4")

# Define the script text
SCRIPT = (
    "In a world where efficient travel and remote living were becoming increasingly important, "
    "a group of savvy globetrotters shared their secrets for streamlining life on the go. "
    "Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere. "
    "Andrew chimed in, adding that he used GreenByPhone to process checks electronically, creating a seamless financial system across different states. "
    "A seasoned female traveler and new mom then offered her insights, recommending quick-dry, versatile clothing from Athleta, and essential gadgets like a portable sound machine for better sleep on the road. "
    "She didn't stop there, sharing her must-haves for traveling with a baby, including a comfortable sling and a portable tent that doubled as a familiar sleep space. "
    "The conversation concluded with tips on navigating air travel with little ones, from choosing the right carry-on size to keeping babies comfortable during takeoff and landing. "
    "These modern adventurers had cracked the code to effortless, family-friendly globe-trotting, turning the dream of a flexible, location-independent lifestyle into a reality."
)

# Create a TextClip
txt_clip = TextClip(SCRIPT, fontsize=24, color='white', size=video.size, method='caption', align='South')

# Set the duration of the text clip to match the video duration
txt_clip = txt_clip.set_duration(video.duration)

# Overlay the text clip on the video clip
video_with_text = CompositeVideoClip([video, txt_clip.set_pos('bottom')])

# Write the result to a file
output_path = "/mnt/data/output_with_text.mp4"
video_with_text.write_videofile(output_path, codec='libx264', audio_codec='aac')

print(f"Video with text overlay has been saved to {output_path}")
