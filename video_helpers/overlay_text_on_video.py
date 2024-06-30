from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont

# Load the video file
video = VideoFileClip("src/output.mp4")

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

# Function to create an image with text using Pillow
def create_text_image(text, size, fontsize=24):
    img = Image.new('RGB', size, color=(0, 0, 0))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
    except IOError:
        font = ImageFont.load_default()

    # Split text into multiple lines to fit within the image width
    lines = []
    words = text.split()
    line = ""
    for word in words:
        if d.textbbox((0, 0), line + " " + word, font=font)[2] <= size[0]:
            line = line + " " + word if line else word
        else:
            lines.append(line)
            line = word
    lines.append(line)

    # Calculate text height
    text_height = sum([d.textbbox((0, 0), line, font=font)[3] for line in lines])

    y = (size[1] - text_height) // 2
    for line in lines:
        line_width = d.textbbox((0, 0), line, font=font)[2]
        d.text(((size[0] - line_width) // 2, y), line, font=font, fill=(255, 255, 255))
        y += d.textbbox((0, 0), line, font=font)[3]

    return img

text_img = create_text_image(SCRIPT, video.size)

# Save the image to a temporary file
text_img_path = "src/temp_text.png"
text_img.save(text_img_path)

# Create an ImageClip from the saved text image
txt_clip = ImageClip(text_img_path, duration=video.duration)

# Overlay the text clip on the video clip
video_with_text = CompositeVideoClip([video, txt_clip.set_pos('bottom')])

# Write the result to a file
output_path = "src/output_with_text.mp4"
video_with_text.write_videofile(output_path, codec='libx264', audio_codec='aac')

print(f"Video with text overlay has been saved to {output_path}")
