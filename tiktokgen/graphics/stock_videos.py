import os
import requests
from abc import ABC

import logging

from .base import GraphicsGenBase


class StockVideoFinder(GraphicsGenBase):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
    def generate(self, prompt, save_path=None):
        logging.info("StockVideoFinder: Getting videos")
        
        query_kerywords = prompt.replace("\n", "").replace(".", "").replace(",", "").lower()
        video_res = requests.get(
            "https://api.pexels.com/videos/search?orientation=portrait&query=" + query_kerywords + "&per_page=1", 
            headers={"Authorization": os.getenv("PEXELS_API_KEY")},
            timeout=30  # Increase the timeout to 30 seconds
        )
        logging.debug(f"StockVideoFinder: Raw API response: {video_res.text}")
        video_res = video_res.json()
        
        logging.debug(f"StockVideoFinder: API response keys: {video_res.keys()}")
        url = video_res["videos"][0]["video_files"][0]["link"]
        
        return self.download_from_url(url, save_path=save_path)