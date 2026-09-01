from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

text = """
Cloud computing provides on-demand access to computing resources
such as servers, storage and software through the Internet.
It helps organizations reduce infrastructure costs, improve
scalability and access computing services whenever required.
"""

prompts = [
    ("ZERO-SHOT", f"""
Summarize this article in exactly 50 words:

{text}
"""),

    ("ONE-SHOT", f"""
Summarize the article in exactly 50 words.

Example:
Input: Cloud computing provides computing resources through
the Internet.
Output: Cloud computing delivers computing resources through
the Internet, reducing infrastructure requirements and
supporting flexible access.

Article:
{text}
"""),

    ("FEW-SHOT", f"""
Summarize the article in exactly 50 words.

Example 1:
Focus on accuracy and important information.

Example 2:
Use clear and simple language.

Article:
{text}
""")
]

for name, prompt in prompts:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print("\n", name)
    print(response.text)