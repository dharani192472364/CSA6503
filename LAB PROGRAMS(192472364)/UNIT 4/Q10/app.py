from diffusers import StableDiffusionPipeline
import torch

# Load pre-trained text-to-image model
model = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
)

model = model.to("cuda" if torch.cuda.is_available() else "cpu")

# Different prompts
prompts = [
    "A modern suspension bridge",
    "A modern suspension bridge at night",
    "A modern suspension bridge over a river",
    "A futuristic suspension bridge with smart technology"
]

# Generate images
for i, prompt in enumerate(prompts):
    image = model(prompt).images[0]
    image.save(f"engineering_image_{i+1}.png")
    print("Generated:", prompt)

print("All images generated successfully.")