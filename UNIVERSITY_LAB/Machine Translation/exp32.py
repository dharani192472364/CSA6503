from transformers import pipeline

translator = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-en-hi"
)

text = input(
    "Enter English engineering text: "
)

result = translator(text)

print("\nHindi Translation:")
print(result[0]["translation_text"])