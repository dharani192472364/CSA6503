from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

task = """
Explain the importance of Artificial Intelligence in engineering
in about 100 words.
"""

zero_shot = task

one_shot = """
Explain the importance of Artificial Intelligence in engineering
in about 100 words.

Example:
Topic: Cloud Computing
Answer: Cloud computing provides flexible access to computing
resources, reduces infrastructure costs and supports scalable
applications.

Now answer the engineering question.
"""

few_shot = """
Explain the importance of Artificial Intelligence in engineering
in about 100 words.

Example 1:
Topic: Robotics
Answer: Robotics combines software, sensors and mechanical
systems to automate engineering tasks.

Example 2:
Topic: IoT
Answer: IoT connects physical devices and enables them to
exchange data for monitoring and automation.

Now answer the question about Artificial Intelligence.
"""

for method, prompt in [
    ("ZERO-SHOT", zero_shot),
    ("ONE-SHOT", one_shot),
    ("FEW-SHOT", few_shot)
]:

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print("\n" + "=" * 60)
    print(method)
    print("=" * 60)
    print(response.text)

print("\nCOMPARISON")
print("-" * 60)
print("Zero-shot : Simple but less control over the output.")
print("One-shot  : Better control using one example.")
print("Few-shot  : Usually more consistent and follows the desired style.")