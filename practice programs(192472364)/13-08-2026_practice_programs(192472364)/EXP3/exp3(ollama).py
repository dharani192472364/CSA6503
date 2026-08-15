import requests

# Ollama model
MODEL = "llama3.2"

# Get input
error_message = input("Enter English error message: ")
language = input("Enter your mother tongue/language: ")

# Prompt
prompt = f"""
Translate the following English error message into {language}.

English error message:
{error_message}

Rules:
- Give ONLY the translated error message.
- Do not give any explanation.
- Keep the meaning clear and natural.
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
        translation = result["response"].strip()

        print("\n" + "=" * 60)
        print("ERROR MESSAGE TRANSLATOR")
        print("=" * 60)
        print("English :", error_message)
        print("Language:", language)
        print("Translation:", translation)

    else:
        print("Ollama Error:", response.text)

except Exception as e:
    print("Error connecting to Ollama:", e)