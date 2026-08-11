import ollama

text = "Artificial Intelligence is changing the world."

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": f"Translate the following English text into Telugu:\n{text}"
        }
    ]
)

print("Translated Text:")
print(response["message"]["content"])