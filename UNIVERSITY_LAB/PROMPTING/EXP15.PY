from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

zero = """
Create an attractive promotional social media post for an
Artificial Intelligence Workshop conducted by an engineering college.
"""

one = """
Create a promotional social media post for an AI Workshop.

Example:
Event: Python Workshop
Post: Join our Python Workshop and learn programming through
hands-on activities and exciting projects.

Now create a similar post for an AI Workshop.
"""

few = """
Create a promotional social media post for an AI Workshop.

Example 1:
Use an energetic tone and short sentences.

Example 2:
Mention learning opportunities, practical activities and registration.

Now create the AI Workshop promotional post.
"""

for title, prompt in [
    ("ZERO-SHOT", zero),
    ("ONE-SHOT", one),
    ("FEW-SHOT", few)
]:
    output = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print("\n###", title, "###")
    print(output.text)