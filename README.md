**A [Sundai Club](https://sundai.club/) Project**

# Book-Digest

### Instead of re-reading a book -- refresh your memory with a series of short TikTok style videos

## Pipeline

1. Upload a book and break it into individual video script (using RAG and LLMs)
2. Turn each video into sub-sections using GPT-4 (save these as a JSON object)
3. Generate text-to-video prompts for each sub-section, add these to the JSON object
4. Generate relevant video for the background using Runway's Stable-diffusion inpainting model to create an infinite loop .mp4
5. Generate audio from the script, combine with video (because the video is an infinite loop, it can be repeated to match the length of the audio)
6. Add captions to video
7. Export & watch!

## How to Run

### Create a virtual environment

 macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv env
.\env\Scripts\activate
```

## Install the requirements

```bash
pip install -r requirements.txt
```

## Install ImageMagick (Mac)

```bash
brew install imagemagick
```

# Running web UI & pipeline

## Production

Update your prod.env:

```
DOMAIN=digest.sundai.club
EXTERNAL_ACCESS=outside_container
NODE_ENV=production
APP_NAME=sundai-digest
ADMIN_PASSWORD=replace-with-a-random-value
REPLICATE_API_TOKEN=replace-with-real-api-key
OPENAI_API_KEY=replace-with-real-api-key
ANTHROPIC_API_KEY=replace-with-real-api-key
```

Deploy: `.devops/run --deploy prod.env`

The server to which it's deployed (`digest.sundai.club`, in this case) will be running the app at `http://localhost:3569/`, so a reverse proxy (like nginx) should be set up to proxy the real traffic (in this case, at `https://digest.sundai.club/` to `http://localhost:3569/`).

## Dev mode

Update your .env: Same as prod.env above but change NODE_ENV to `development`

Run: `.devops/run`

Access locally at `http://localhost:3569/`
