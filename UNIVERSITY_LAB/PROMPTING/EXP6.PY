from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

zero = """
Create an attractive product description for a Smart Fitness Watch
designed for engineering college students.
"""

one = """
Create a product description for a Smart Fitness Watch.

Example:
Product: Smart Backpack
Description: A modern backpack with laptop protection, USB charging
and multiple compartments for students.

Now create the Smart Fitness Watch description.
"""

few = """
Create a product description for a Smart Fitness Watch.

Example 1:
Product: Smart Backpack
Style: Modern and student-friendly.

Example 2:
Product: Wireless Earbuds
Style: Short and attractive.

Now create the Smart Fitness Watch description.
"""

for name, prompt in [
    ("ZERO-SHOT", zero),
    ("ONE-SHOT", one),
    ("FEW-SHOT", few)
]:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)
    print(response.text)