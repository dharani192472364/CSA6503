import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    token=os.getenv("HF_TOKEN")
)

prompt = input(
    "Enter your prompt: "
)

response = client.text_generation(
    prompt,
    model="distilgpt2",
    max_new_tokens=100
)

print("\nGenerated Text:")
print(response)