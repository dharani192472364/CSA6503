import os
import time
import csv
from google import genai

# ============================================================
# GEMINI SETUP
# ============================================================

API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-flash-lite-latest"

# ============================================================
# FARMER INPUT
# ============================================================

params = {
    "language": "English",
    "crop": "Rice",
    "district": "Thanjavur",
    "soil": "Clay soil",
    "weather": "Heavy rain expected"
}

# ============================================================
# PROMPT
# ============================================================

PROMPT = """
You are an agricultural extension officer.

Write ONE advisory SMS under 160 characters in {language}.

Crop: {crop}
District: {district}
Soil: {soil}
Weather: {weather}

Rules:
- Give one actionable instruction.
- No greetings.
- No emojis.
- No chemical dosage.
- Use simple words.
- Do not invent facts.
"""

# ============================================================
# GENERATE ADVISORY
# ============================================================

def generate_advisory(params, temperature, top_p):

    prompt = PROMPT.format(**params)

    start_time = time.time()

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config={
                "temperature": temperature,
                "top_p": top_p,
                "max_output_tokens": 120
            }
        )

        latency = (time.time() - start_time) * 1000

        text = response.text.strip()

        # Token information
        usage = response.usage_metadata

        input_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count

        return {
            "text": text,
            "chars": len(text),
            "latency": round(latency, 2),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "safe": "YES" if len(text) <= 160 else "NO"
        }

    except Exception as e:

        print("ERROR:", e)

        return {
            "text": "Clear drainage channels to remove excess water from rice fields.",
            "chars": 0,
            "latency": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "safe": "FALLBACK"
        }


# ============================================================
# PARAMETER SWEEP
# ============================================================

settings = [
    (0.0, 1.0),
    (0.4, 1.0),
    (0.9, 1.0),
    (0.4, 0.5),
    (0.9, 0.5)
]

results = []

print("\n")
print("=" * 100)
print("EXERCISE 8 - PARAMETER SWEEP")
print("=" * 100)

for temperature, top_p in settings:

    print("\n" + "-" * 100)

    print("Temperature:", temperature)
    print("Top-p:", top_p)

    result = generate_advisory(
        params,
        temperature,
        top_p
    )

    print("\nAdvisory:")
    print(result["text"])

    print("\nCharacter Count:", result["chars"])
    print("Prompt Tokens:", result["input_tokens"])
    print("Completion Tokens:", result["output_tokens"])
    print("Latency:", result["latency"], "ms")
    print("Factually Safe:", result["safe"])

    results.append({
        "temperature": temperature,
        "top_p": top_p,
        "output": result["text"],
        "chars": result["chars"],
        "latency": result["latency"],
        "prompt_tokens": result["input_tokens"],
        "completion_tokens": result["output_tokens"],
        "factually_safe": result["safe"]
    })


# ============================================================
# OBSERVATION TABLE
# ============================================================

print("\n")
print("=" * 120)
print("OBSERVATION TABLE - PARAMETER SWEEP")
print("=" * 120)

print(
    f"{'Temp':<10}"
    f"{'Top-p':<10}"
    f"{'Output (first 40 chars)':<45}"
    f"{'Chars':<10}"
    f"{'Latency (ms)':<15}"
    f"{'Factually safe?':<15}"
)

print("-" * 120)

for r in results:

    first_40 = r["output"][:40]

    print(
        f"{r['temperature']:<10}"
        f"{r['top_p']:<10}"
        f"{first_40:<45}"
        f"{r['chars']:<10}"
        f"{r['latency']:<15}"
        f"{r['factually_safe']:<15}"
    )


# ============================================================
# SAVE CSV
# ============================================================

with open(
    "exercise8_parameter_sweep.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "temperature",
            "top_p",
            "output",
            "chars",
            "latency",
            "prompt_tokens",
            "completion_tokens",
            "factually_safe"
        ]
    )

    writer.writeheader()
    writer.writerows(results)


print("\n")
print("=" * 100)
print("CSV FILE CREATED")
print("=" * 100)

print("exercise8_parameter_sweep.csv")
print("\nExercise 8 parameter sweep completed successfully.")