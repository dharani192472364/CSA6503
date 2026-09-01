from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

zero = """
Write a professional leave email to a faculty member because
a student is suffering from illness.
"""

one = """
Write a professional leave email because of illness.

Example:
Dear Sir,
I am unable to attend today's class due to illness.
Kindly grant me leave for one day.
Thank you.

Now write a similar professional email.
"""

few = """
Write a professional leave email because of illness.

Example 1:
Use a polite and formal tone.

Example 2:
Include a subject, greeting, reason, leave request and closing.

Generate the complete email.
"""

for title, prompt in [
    ("ZERO-SHOT", zero),
    ("ONE-SHOT", one),
    ("FEW-SHOT", few)
]:
    answer = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print("\n", title)
    print(answer.text)