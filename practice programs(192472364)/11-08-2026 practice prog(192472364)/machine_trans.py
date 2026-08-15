import ollama

text = "Artificial Intelligence is changing the world."

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": f"Translate the following English text into Tamil:\n{text}"
        }
    ],
    options={
        "temperature": 0.2
    }
)

print("Original Text:")
print(text)

print("\nTranslated Text:")
print(response["message"]["content"])