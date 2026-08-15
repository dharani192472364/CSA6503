import os
from dotenv import load_dotenv
from google import genai

# Load Gemini API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found.")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)

# IEEE paper abstract
abstract = """
Artificial intelligence and machine learning techniques are increasingly
being used for intelligent traffic management. This paper proposes a
machine learning-based approach for predicting traffic conditions using
historical traffic data. The proposed system analyzes vehicle counts,
time, and traffic patterns to improve traffic prediction accuracy and
support intelligent transportation systems.
"""

# Prompt
prompt = f"""
Summarize the following IEEE paper abstract in LESS THAN 280 CHARACTERS.

STRICT RULES:
1. Return ONLY the summary.
2. Do not write "Here is a summary".
3. Do not use labels such as Main problem, Method, or Result.
4. Do not use bullet points.
5. Keep the summary below 250 characters to provide a safety margin.
6. Include the main problem, method, and purpose/result.

IEEE Abstract:
{abstract}
"""

try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "temperature": 0
        }
    )

    summary = response.text.strip()

    print("=" * 60)
    print("IEEE ABSTRACT SUMMARY")
    print("=" * 60)
    print(summary)
    print("\nCharacter count:", len(summary))

    if len(summary) <= 280:
        print("✓ Summary is within 280 characters.")
    else:
        print("✗ Summary exceeds 280 characters.")

except Exception as e:
    print("Error:", e)