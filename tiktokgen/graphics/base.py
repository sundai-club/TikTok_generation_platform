import requests
import logging
from abc import ABC, abstractmethod

class GraphicsGenBase(ABC):
    def __init__(self, meta_prompt=""):
        self.meta_prompt = meta_prompt
    
    def create_prompts(self, script):
        '''
        Create prompts for the graphics generation.
        '''
        
        #TODO: better prompting with dspy
        
        PROMPT_BEGGINING =\
            "Below is a script for a TikTok video."\
            "For each line generate a prompt to generate a background with "\
            "a relevant content to the text in the script."
        
        prompts = [f'an image of {t["text"]} {self.meta_prompt}' for t in script]
        return prompts
    
    def download_from_url(self, url, save_path=None):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            if save_path:
                save_path = save_path + self.extension
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return save_path
            return response.content
        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading image: {str(e)}")
            raise
    
    @abstractmethod
    def generate(self, script, save_path=None):
        raise NotImplementedError
    
    def __call__(self, script, save_prefix=None):
        generated_prompts = self.create_prompts(script)
        
        generations = []
        for i, prompt in enumerate(generated_prompts):
            save_path = f"{save_prefix}_{i}" if save_prefix else None
            generations.append(self.generate(prompt, save_path))
        
        return generations