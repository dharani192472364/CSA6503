import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)

# Prompt
prompt = """
Generate a 4-line poem about my college.
The poem should be positive, simple, and creative.
"""

# Temperatures to test
temperatures = [0, 0.5, 1]

for temperature in temperatures:

    print("\n" + "=" * 50)
    print("TEMPERATURE:", temperature)
    print("=" * 50)

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config={
                "temperature": temperature
            }
        )

        print(response.text)

    except Exception as e:
        print("Error:", e)