from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

ai = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.6-flash"

prompt = """
You are demonstrating Zero-shot, One-shot and Few-shot prompting.

TASK:
Write a professional leave email to a faculty member because
a student is suffering from illness.

ZERO-SHOT:
Generate the email directly without any example.

ONE-SHOT:
Example:
Subject: Leave Request

Dear Professor,
I am unable to attend college today because I am unwell.
Kindly grant me leave for one day.

Regards,
Student

Now generate a similar professional leave email.

FEW-SHOT:
Example 1:
Use a polite and respectful tone.

Example 2:
Include subject, greeting, reason, leave duration and closing.

Now generate a complete professional leave email.

Return the answer in this format:

ZERO-SHOT:
<email>

ONE-SHOT:
<email>

FEW-SHOT:
<email>

After the three emails, give a short comparison based on:
1. Tone
2. Grammar
3. Formatting
4. Completeness
"""

try:
    response = ai.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    print("=" * 60)
    print("ZERO-SHOT / ONE-SHOT / FEW-SHOT PROMPTING")
    print("=" * 60)
    print(response.text)

except Exception as e:
    print("Error:", e)