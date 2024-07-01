import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import json
import re
from pipeline import pipeline
# Locate the .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# SCRIPT = "In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go. Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere. Andrew chimed in, adding that he used GreenByPhone to process checks electronically, creating a seamless financial system across different states. A seasoned female traveler and new mom then offered her insights, recommending quick-dry, versatile clothing from Athleta, and essential gadgets like a portable sound machine for better sleep on the road. She didn't stop there, sharing her must-haves for traveling with a baby, including a comfortable sling and a portable tent that doubled as a familiar sleep space. The conversation concluded with tips on navigating air travel with little ones, from choosing the right carry-on size to keeping babies comfortable during takeoff and landing. These modern adventurers had cracked the code to effortless, family-friendly globe-trotting, turning the dream of a flexible, location-independent lifestyle into a reality."
# prompt: make a claude api call and pass in the chapter
prompt = '''You are the world's best video creator for viral tiktok videos. You chunk and convert books into second 60 second infotainment tiktoc videos for each chapter. take into account the following [[key elements]] to generate a script for this [[chapter]]. Always remember to prioritize making the script feel natural, and conversational.
[[Key Elements]] for Popular Infotainment Videos:
Script Elements:
Strong hook (first 3-5 seconds)
Clear, concise information
Storytelling approach
Actionable tips or takeaways
Call-to-action (CTA)
Voice Elements:
Engaging and energetic tone
Clear enunciation
Pacing that matches visual elements
Use of pauses for emphasis
Video Elements:
Eye-catching visuals
On-screen text for key points
Transitions and effects
Relevant background music
Subtitles for accessibility
'''
import anthropic

client = anthropic.Anthropic()


def get_script_from_chunk(chunk):   
    message = client.messages.create(
      model="claude-3-5-sonnet-20240620",
      max_tokens=1000,
      temperature=0,
      system=prompt,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": "Summarize this chapter and just output the script, nothing else [[chapter]] " + chunk
                  }
              ]
          }
      ]
  )
    return message.content[0].text

def get_all_scripts_from_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    
    for i, item in enumerate(data):
        chunk = item['content']
        script = get_script_from_chunk(chunk)
        data[i]['script'] = script

# Given the json file, and chunk number, create the video for it
def make_video(json_file, i):
    with open(json_file) as f:
        data = json.load(f)

    script = data[i][script]
    pipeline(script)


    
