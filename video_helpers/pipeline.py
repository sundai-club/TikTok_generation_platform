from prompt_to_video import prompt_to_video
from script_to_prompt import gpt_step_0, gpt_step_1
import json

# create script from text files
SCRIPT = "In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go. Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere. Andrew chimed in, adding that he used GreenByPhone to process checks electronically, creating a seamless financial system across different states. A seasoned female traveler and new mom then offered her insights, recommending quick-dry, versatile clothing from Athleta, and essential gadgets like a portable sound machine for better sleep on the road. She didn't stop there, sharing her must-haves for traveling with a baby, including a comfortable sling and a portable tent that doubled as a familiar sleep space. The conversation concluded with tips on navigating air travel with little ones, from choosing the right carry-on size to keeping babies comfortable during takeoff and landing. These modern adventurers had cracked the code to effortless, family-friendly globe-trotting, turning the dream of a flexible, location-independent lifestyle into a reality."

PROMPT = json.loads('''[{'text': 'In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go.', 'prompt': 'Animation of globe spinning with transportation icons', 'mp4': 'https://replicate.delivery/yhqm/fu5nbjZ1YZxzfUBVqqiesfinUcbBH9lF8iqfSnUkl1oKOBfwE/infinit_zoom.mp4'}, {'text': 'Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere.', 'prompt': 'Animated smartphone showing Earth Class Mail app', 'mp4': 'https://replicate.delivery/yhqm/WbfXB7VqbWVBRKLOedVQsQgekImdYJeyFSRfMGstBXKFRBfwE/infinit_zoom.mp4'}, {'text': 'Andrew chimed in, adding that he used GreenByPhone to process checks electronically, creating a seamless financial system across different states.', 'prompt': 'Illustrated device doing digital check depositing', 'mp4': 'https://replicate.delivery/yhqm/mUguWgDLWF57JdQrFFsadXqHrcm0jLesVtLLPgiwnj7PF8hJA/infinit_zoom.mp4'}, {'text': 'A seasoned female traveler and new mom then offered her insights, recommending quick-dry, versatile clothing from Athleta, and essential gadgets like a portable sound machine for better sleep on the road.', 'prompt': 'Fast animation of packing suitcase with essentials', 'mp4': 'https://replicate.delivery/yhqm/Mz70ZfmY5hVhe068L9CwHVP1qPqlKe9YBuRyvQA8pZttVwHmA/infinit_zoom.mp4'}, {'text': "She didn't stop there, sharing her must-haves for traveling with a baby, including a comfortable sling and a portable tent that doubled as a familiar sleep space.", 'prompt': 'Animation of baby-friendly traveling kit', 'mp4': 'https://replicate.delivery/yhqm/zYZrZFpQYfRuTSLyi0YWozv7TFS5GqN2RNfb12G7KS6NL4DTA/infinit_zoom.mp4'}, {'text': 'The conversation concluded with tips on navigating air travel with little ones, from choosing the right carry-on size to keeping babies comfortable during takeoff and landing.', 'prompt': 'Animation of airplane cabin during takeoff', 'mp4': 'https://replicate.delivery/yhqm/qjYexZFH6hQjCaOKQqwkEVV5fKh7ILTtEaVJ7gBnovfJXwHmA/infinit_zoom.mp4'}, {'text': 'These modern adventurers had cracked the code to effortless, family-friendly globe-trotting, turning the dream of a flexible, location-independent lifestyle into a reality.', 'prompt': 'Animated globe with happy family traveling around it', 'mp4': 'https://replicate.delivery/yhqm/SYu2yA7yXfVXV6W8tHmwsdyJSikARhcYRfitEb4t3mc7L4DTA/infinit_zoom.mp4'}]''')

def pipeline(script, output_path):
    
    # create video from script
    # parsed_script = gpt_step_0(script)
    # parsed_script = gpt_step_1(parsed_script)
    # print(prompt_to_video(parsed_script = parsed_script))
    
    # create audio from script
    
    # combine video and audio
    
    # save video to output_path
    
    
pipeline(SCRIPT, "../data/output.mp4")