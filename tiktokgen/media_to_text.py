import os
import base64
from openai import OpenAI
from PIL import Image
import cv2
import dotenv

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path):
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

def describe_media(file_path):
    # Initialize OpenAI client

    # Check if the file is an image
    try:
        with Image.open(file_path) as img:
            # It's an image
            return analyze_image(file_path)
    except IOError:
        # It's not an image, try processing as video
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            # Try opening with different backend for MOV files
            cap = cv2.VideoCapture(file_path, cv2.CAP_FFMPEG)
            if not cap.isOpened():
                return "Error: Unable to open file. Please ensure it's a valid image or video file."

        descriptions = []
        frame_interval = 30  # Process every 30th frame
        temp_image_path = "temp_frame.jpg"

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                cv2.imwrite(temp_image_path, frame)
                description = analyze_image(temp_image_path)
                descriptions.append(description)

            frame_count += 1

        cap.release()
        
        # Remove temporary image file
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

        print(descriptions)
        # Combine descriptions
        if descriptions:
            return " ".join(descriptions)
        else:
            return "No description could be generated for the video."

# Example usage
# result = describe_media("media/team.webp")  # or .mp4
# result = describe_media("media/IMG_7475.mp4")
# print(result)