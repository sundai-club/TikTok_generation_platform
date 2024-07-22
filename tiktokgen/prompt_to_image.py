import replicate
import requests
import os

model_id = "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc"
model_input = {}


def prompts_to_foreground_images(parsed_script):
    
    result = []
    
    for idx, prompt in enumerate(parsed_script):
        if prompt.get("foreground_img"):
            result.append(prompt)
            continue
        
        model_input['prompt'] = prompt['prompt']
        print(f'Ready to run text2img model with input')

        output = replicate.run(
            model_id,
            input = model_input
        )
        url = output[0]
        print(f'Replicate has returned output: {output}')

        #download the video from the returned replicate url
        response = requests.get(url)
        
        prompt["foreground_img"] = 'data/foreground_img_'+str(idx)+'.png'
        with open(prompt["foreground_img"], 'wb') as file:
            # Write the content of the response to the file
            file.write(response.content)
        result.append(prompt)
        
    return result