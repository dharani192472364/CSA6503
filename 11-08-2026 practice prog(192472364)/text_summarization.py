import ollama

text = """Artificial Intelligence (AI) is a branch of computer science that focuses
on creating machines capable of performing tasks that normally require
human intelligence. These tasks include learning, reasoning, problem-solving,
understanding language, recognizing images, and making decisions.
AI is widely used in healthcare, education, banking, transportation,
and many other industries.."""

response = ollama.chat(
    model="llama3.2",
    messages=[{
        "role": "user",
        "content": f"Summarize this text in exactly two lines:\n{text}"
    }]
)

print(response["message"]["content"])