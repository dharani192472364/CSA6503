import os
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)

# Get error message from user
error_message = input("Enter English error message: ")

# Get target language
language = input("Enter your mother tongue/language: ")

# Prompt
prompt = f"""
Translate the following English error message into {language}.

English error message:
{error_message}

Rules:
- Give only the translated error message.
- Do not give explanations.
- Keep the meaning clear and natural.
"""

try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "temperature": 0
        }
    )

    print("\n" + "=" * 60)
    print("ERROR MESSAGE TRANSLATOR")
    print("=" * 60)
    print("English :", error_message)
    print("Language:", language)
    print("Translation:", response.text.strip())

except Exception as e:
    print("Error:", e)