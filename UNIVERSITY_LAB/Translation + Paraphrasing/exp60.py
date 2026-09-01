import ollama

text = input(
    "Enter engineering text: "
)

language = input(
    "Enter target language: "
)

prompt = f"""
You are an engineering language assistant.

Original Text:
{text}

Tasks:

1. Translate the text into {language}.
2. Paraphrase the translated text using simple language.
3. Preserve the original technical meaning.

Display:

TRANSLATION:
PARAPHRASED VERSION:
"""

response = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

print("\n========== RESULT ==========")
print(response["response"])