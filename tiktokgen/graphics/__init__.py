from .stock_videos import StockVideoFinder
from .replicate_generator import ReplicateImage, ReplicateVideo

def get_generator(config):
    type = config.get("type", "Replicate Image")
    
    if type == "Diffusion Image":
        return ReplicateImage(
            config.get("model_id", "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc"),
            meta_prompt=config.get("meta_prompt", ""),
            params=config.get("params", {})
        )
    if type == "Infinite Zoom":
        return ReplicateVideo(
            config.get("model_id", "arielreplicate/stable_diffusion_infinite_zoom:a2527c5074fc0cf9fa6015a40d75d080d1ddf7082fabe142f1ccd882c18fce61"),
            meta_prompt=config.get("meta_prompt",
                "These should be place-specific scenes, such as the middle aisle of an airplane, "\
                "a path through a tropical jungle, or the middle of a city street surrounded by high-rises. "\
                "Write a short succinct clear prompt (max 9 words) to generate each video."
            ),
            params=config.get("params", {
                "inpaint_iter": 3
            })
        )
    if type == "Anime":
        return ReplicateImage(
            config.get("model_id", "lucataco/animate-diff:beecf59c4aee8d81bf04f0381033dfa10dc16e845b4ae00d281e2fa377e48a9f"),
            meta_prompt=config.get("meta_prompt", 
                "Each prompt should be a series of adjectives of a concrete object (such as a place or a person),"\
                "Write a clear prompt (at least 18 words) to generate each image."
            ),
            params=config.get("params", 
                {
                    "path": "toonyou_beta3.safetensors",
                    "seed": 0,
                    "steps": 10,
                    "n_prompt": "badhandv4, easynegative, ng_deepnegative_v1_75t, verybadimagenegative_v1.3, bad-artist, bad_prompt_version2-neg, teeth",
                    "motion_module": "mm_sd_v14",
                    "guidance_scale": 7.5
                }
            )
        )
    if type == "Stock Video":
        return StockVideoFinder()

    raise ValueError(f"Unknown graphics generator type: {type}")


