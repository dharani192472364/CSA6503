import ollama

context = """
Artificial Intelligence (AI) is a branch of computer science.
It enables computers to learn, reason, solve problems, and make decisions.
AI is used in healthcare, education, banking, and transportation.
"""

question = "Where is AI used?"

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": f"""
Answer the question using only the given context.

Context:
{context}

Question:
{question}
"""
        }
    ]
)

print("Question:", question)
print("Answer:", response["message"]["content"])