import ollama

print("Local AI Assistant")
print("Type exit to stop.")

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    print("\nAI:", response["message"]["content"])