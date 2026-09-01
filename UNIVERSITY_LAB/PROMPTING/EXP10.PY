from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

article = """
Artificial Intelligence is widely used in engineering for automation,
robotics, predictive maintenance, design optimization and intelligent
manufacturing. It improves accuracy, reduces operational costs and
helps engineers solve complex problems efficiently.
"""

zero = f"""
Summarize the following article in exactly 50 words.

ARTICLE:
{article}
"""

one = f"""
Summarize the following article in exactly 50 words.

Example:
Article: Renewable energy uses natural sources such as sunlight
and wind to produce clean electricity.

Summary: Renewable energy provides clean electricity using natural
resources and helps reduce environmental pollution.

ARTICLE:
{article}
"""

few = f"""
Summarize the article in exactly 50 words.

Example 1:
Make the summary accurate and concise.

Example 2:
Use simple language suitable for college students.

ARTICLE:
{article}
"""

for name, prompt in [
    ("ZERO-SHOT", zero),
    ("ONE-SHOT", one),
    ("FEW-SHOT", few)
]:
    result = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print("\n", name)
    print(result.text)