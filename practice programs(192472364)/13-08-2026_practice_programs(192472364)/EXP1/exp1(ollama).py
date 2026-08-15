import requests

# Ollama model
MODEL = "llama3.2"

# Prompt
prompt = """
Generate a 4-line poem about my college.
The poem should be positive, simple, and creative.
"""

# Temperatures to test
temperatures = [0, 0.5, 1]

for temperature in temperatures:

    print("\n" + "=" * 60)
    print("TEMPERATURE:", temperature)
    print("=" * 60)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }
        )

        if response.status_code == 200:
            result = response.json()
            print(result["response"])
        else:
            print("Error:", response.text)

    except Exception as e:
        print("Error connecting to Ollama:", e)