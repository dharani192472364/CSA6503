import ollama

# Input prompt
prompt = "Write a short paragraph about Artificial Intelligence."

# Generate text using Ollama
response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

# Display generated text
print("Generated Text:")
print(response["message"]["content"])