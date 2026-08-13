import os
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)

# Get the folder where this Python file is located
folder = os.path.dirname(os.path.abspath(__file__))

# Correct path to syllabus.txt
syllabus_path = os.path.join(folder, "syllabus.txt")

# Load syllabus
try:
    with open(syllabus_path, "r", encoding="utf-8") as file:
        syllabus = file.read()

    print("Syllabus loaded successfully.")

except FileNotFoundError:
    print("ERROR: syllabus.txt not found.")
    print("Expected location:", syllabus_path)
    exit()

# Ask question
question = input("\nAsk a question about the syllabus: ")

# Prompt
prompt = f"""
Answer the question using ONLY the information provided in the syllabus.

If the answer is not available in the syllabus, say:
"Answer not found in the syllabus."

Do not use outside knowledge.

SYLLABUS:
{syllabus}

QUESTION:
{question}

Answer:
"""

try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "temperature": 0
        }
    )

    print("\n" + "=" * 60)
    print("SYLLABUS QUESTION ANSWERING")
    print("=" * 60)
    print("Question:", question)
    print("Answer:", response.text.strip())

except Exception as e:
    print("Error:", e)