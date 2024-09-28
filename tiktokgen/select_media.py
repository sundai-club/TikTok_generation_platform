import os
from openai import OpenAI
from typing import List

def match_media_to_scenes(media_descriptions: List[str], scene_descriptions: List[str]) -> List[int]:
    """
    Match media descriptions to scene descriptions using OpenAI API.

    Args:
    media_descriptions (List[str]): List of media descriptions.
    scene_descriptions (List[str]): List of scene descriptions.

    Returns:
    List[int]: List of indices of the best matching media descriptions for each scene.
    """
    client = OpenAI(api_key="")

    matches = []

    for scene in scene_descriptions:
        prompt = f"""
        Given the following scene description:
        "{scene}"

        And the following list of available media descriptions:
        {media_descriptions}

        Which media description best matches the scene? Return only the exact media description that best matches, without any additional text or explanation.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that matches scene descriptions to media descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        best_match = response.choices[0].message.content.strip()
        best_match_index = media_descriptions.index(best_match)
        matches.append(best_match_index)

    return matches

# Example usage:
media_descriptions = [
    "A serene beach at sunset",
    "A bustling city street at night",
    "A lush green forest with a waterfall"
]
scene_descriptions = [
    "A romantic evening by the ocean",
    "An exciting night out in the city"
]
results = match_media_to_scenes(media_descriptions, scene_descriptions)
for i, scene in enumerate(scene_descriptions):
    print(f"Scene: {scene}\nBest matching media index: {results[i]}\n")
