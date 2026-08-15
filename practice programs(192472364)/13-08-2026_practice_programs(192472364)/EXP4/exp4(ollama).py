import os
import requests

MODEL = "llama3.2"

# Get the folder where this Python file is located
folder = os.path.dirname(os.path.abspath(__file__))

# Build the correct syllabus path
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
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        }
    )

    if response.status_code == 200:
        result = response.json()

        print("\n" + "=" * 60)
        print("SYLLABUS QUESTION ANSWERING")
        print("=" * 60)
        print("Question:", question)
        print("Answer:", result["response"].strip())

    else:
        print("Ollama Error:", response.text)

except Exception as e:
    print("Error connecting to Ollama:", e)