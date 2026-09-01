import ollama

print("LOCAL LLM TEXT GENERATION")
print("Type 'exit' to stop.")

while True:
    prompt = input("\nEnter your prompt: ")

    if prompt.lower() == "exit":
        break

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nGenerated Text:")
    print(response["message"]["content"])