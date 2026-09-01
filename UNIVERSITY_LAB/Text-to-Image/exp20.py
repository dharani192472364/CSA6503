import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

prompts = [
    "Generate an image of a robotic arm.",
    "Generate a realistic industrial robotic arm.",
    "Generate a futuristic AI-powered industrial robotic arm working in a smart factory."
]

for i, prompt in enumerate(prompts, 1):

    print("\n==============================")
    print("Prompt", i)
    print("==============================")
    print(prompt)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print(response)