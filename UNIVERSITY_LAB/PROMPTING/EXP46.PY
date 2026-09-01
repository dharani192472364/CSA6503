from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

article = """
Machine learning enables computers to learn patterns from data
without being explicitly programmed. Engineering applications
include fault detection, prediction, quality control, robotics
and intelligent automation.
"""

zero_prompt = f"""
Give a 50-word summary of this technical article:

{article}
"""

one_prompt = f"""
Summarize this article in 50 words.

Example:
Input: Robotics combines mechanical systems and computer control.
Output: Robotics combines mechanical systems, sensors and software
to create machines capable of performing automated tasks.

Article:
{article}
"""

few_prompt = f"""
Summarize this article in exactly 50 words.

Example 1:
Keep all major technical points.

Example 2:
Use readable language and avoid unnecessary details.

Article:
{article}
"""

for label, prompt in [
    ("Zero Shot", zero_prompt),
    ("One Shot", one_prompt),
    ("Few Shot", few_prompt)
]:
    result = ai.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print(f"\n{label}")
    print("-" * 40)
    print(result.text)