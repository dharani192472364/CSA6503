import ollama

prompt = input(
    "Enter an engineering topic: "
)

response = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

print("\nGenerated Text:")
print(response["response"])