from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Zero-shot
p1 = """
Write a 200-word blog on Applications of Artificial Intelligence
in Healthcare.
"""

# One-shot
p2 = """
Write a 200-word blog on Applications of Artificial Intelligence
in Healthcare.

Example:
Topic: AI in Education
Blog: Artificial Intelligence helps education through personalized
learning, automated evaluation and intelligent tutoring.

Now write the healthcare blog.
"""

# Few-shot
p3 = """
Write a 200-word blog on Applications of Artificial Intelligence
in Healthcare.

Example 1:
Topic: AI in Education
Style: Informative and simple.

Example 2:
Topic: AI in Banking
Style: Informative and concise.

Now write the healthcare blog using the same style.
"""

for title, prompt in [
    ("ZERO-SHOT", p1),
    ("ONE-SHOT", p2),
    ("FEW-SHOT", p3)
]:
    result = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print("\n", title)
    print(result.text)