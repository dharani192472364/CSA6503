import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

prompt = input(
    "Enter an engineering image prompt: "
)

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print("\nGenerated Result:")
print(response)