import requests

MODEL = "llama3.2"

abstract = """
Artificial intelligence and machine learning techniques are increasingly
being used for intelligent traffic management. This paper proposes a
machine learning-based approach for predicting traffic conditions using
historical traffic data. The proposed system analyzes vehicle counts,
time, and traffic patterns to improve traffic prediction accuracy and
support intelligent transportation systems.
"""

prompt = f"""
Summarize this IEEE abstract in LESS THAN 280 CHARACTERS.

STRICT RULES:
1. Return ONLY the summary.
2. Do NOT write "Here is a summary".
3. Do NOT use labels such as "Main problem", "Method", or "Result".
4. Do NOT use bullet points.
5. Maximum 250 characters to leave a safety margin.

Abstract:
{abstract}
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
        summary = result["response"].strip()

        # Remove common unwanted prefixes
        unwanted = [
            "Here is a summary:",
            "Here is the summary:",
            "Summary:",
            "Main problem:",
            "Proposed method:",
            "Main result:"
        ]

        for text in unwanted:
            summary = summary.replace(text, "").strip()

        # If still above 280 characters, ask Ollama to shorten it
        if len(summary) > 280:

            shorten_prompt = f"""
Shorten the following text to LESS THAN 250 CHARACTERS.
Return ONLY the shortened sentence.
Do not add explanations or labels.

Text:
{summary}
"""

            response2 = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": MODEL,
                    "prompt": shorten_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0
                    }
                }
            )

            if response2.status_code == 200:
                summary = response2.json()["response"].strip()

        print("=" * 60)
        print("IEEE ABSTRACT SUMMARY")
        print("=" * 60)
        print(summary)
        print("\nCharacter count:", len(summary))

        if len(summary) <= 280:
            print("✓ Summary is within 280 characters.")
        else:
            print("✗ Summary exceeds 280 characters.")

    else:
        print("Ollama Error:", response.text)

except Exception as e:
    print("Error connecting to Ollama:", e)