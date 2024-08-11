import os
import requests
import replicate
from abc import ABC

import logging

from .base import GraphicsGenBase    

class ReplicateGenerator(GraphicsGenBase, ABC):
    extension = ".png" # ".mp4"
    
    def __init__(self, model_id, *args, params={}, **kwargs):
        self.model_id = model_id
        self.params = params
        super().__init__(*args, **kwargs)

    def generate(self, prompt, save_path=None):
        
        # Run the model
        logging.info(f'ReplicateGenerator: Ready to run text2img model with input {prompt}')
        try:
            output = replicate.run(
                self.model_id,
                input = {
                    "prompt": prompt,
                    **self.params
                }
            )
            if output and len(output) > 0:
                url = output[0]
            else:
                raise ValueError("Empty output from Replicate")
        except replicate.exceptions.ReplicateError as e:
            logging.error(f"Replicate API error: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise
        logging.info(f'ReplicateGenerator: Replicate has returned output: {output}')
        
        # Download the image
        return self.download_from_url(url, save_path=save_path)

class ReplicateImage(ReplicateGenerator):
    extension = ".png"
    
class ReplicateVideo(ReplicateGenerator):
    extension = ".mp4"