import replicate

input = {
    "prompt": "A path going into the woods"
}

output = replicate.run(
    "arielreplicate/stable_diffusion_infinite_zoom:a2527c5074fc0cf9fa6015a40d75d080d1ddf7082fabe142f1ccd882c18fce61",
    input=input
)
print(output)