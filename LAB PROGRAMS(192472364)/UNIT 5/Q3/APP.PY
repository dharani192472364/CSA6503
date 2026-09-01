import ollama

print("LOCAL LLM QUESTION ANSWERING SYSTEM")
print("Type 'exit' to stop.")

while True:
    question = input("\nEnter your question: ")

    if question.lower() == "exit":
        break

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful question-answering assistant. "
                           "Give clear and accurate answers."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response["message"]["content"]

    print("\nAnswer:")
    print(answer)