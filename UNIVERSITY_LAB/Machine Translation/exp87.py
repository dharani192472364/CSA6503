from transformers import pipeline

translator = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-en-hi"
)

print("Engineering Translation System")

text = input(
    "\nEnter English text: "
)

output = translator(text)

print("\nTranslated Text:")
print(
    output[0]["translation_text"]
)