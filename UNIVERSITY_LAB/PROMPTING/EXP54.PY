from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

zero = """
Write an attractive Instagram promotional post for a college
Artificial Intelligence Workshop.
"""

one = """
Write an Instagram promotional post for an AI Workshop.

Example:
Join our Web Development Workshop!
Learn modern web technologies, build projects and improve
your development skills.

Now create an AI Workshop post.
"""

few = """
Create an Instagram post promoting an AI Workshop.

Example 1:
Keep it short and energetic.

Example 2:
Mention AI learning, hands-on sessions and student benefits.

Now create the final promotional post.
"""

for method, prompt in [
    ("Zero-shot", zero),
    ("One-shot", one),
    ("Few-shot", few)
]:
    result = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print("\n" + method)
    print(result.text)