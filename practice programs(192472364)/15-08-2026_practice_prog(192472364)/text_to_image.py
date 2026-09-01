import requests
import torch
from diffusers import StableDiffusionPipeline

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

# Get image description
description = input("Enter image description: ")

# Ask Ollama to improve the prompt
ollama_prompt = f"""
Create a detailed prompt for an AI image generator based on this description:

{description}

Return ONLY the image prompt.
"""

try:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": ollama_prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        print("Ollama Error:", response.text)
        exit()

    image_prompt = response.json()["response"].strip()

    print("\n" + "=" * 60)
    print("TEXT TO IMAGE")
    print("=" * 60)
    print("Input:", description)
    print("\nOllama Generated Prompt:")
    print(image_prompt)

except Exception as e:
    print("Ollama connection error:", e)
    exit()


# Load Stable Diffusion
print("\nLoading image generation model...")

model_id = "runwayml/stable-diffusion-v1-5"

device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)

pipe = pipe.to(device)

# Generate image
print("Generating image...")

image = pipe(
    image_prompt,
    num_inference_steps=20
).images[0]

# Save image
image.save("generated_image.png")

print("\n" + "=" * 60)
print("IMAGE GENERATION COMPLETE")
print("=" * 60)
print("Image saved as: generated_image.png")
print("Device used:", device)