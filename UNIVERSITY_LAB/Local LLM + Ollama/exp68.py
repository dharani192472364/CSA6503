import ollama

context = """
Artificial Intelligence enables machines to perform
tasks that normally require human intelligence.

Machine learning allows computers to learn patterns
from data and make predictions.
"""

question = input(
    "Ask a question: "
)

prompt = f"""
Answer the question using only the following information.

Context:
{context}

Question:
{question}
"""

response = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

print("\nAnswer:")
print(response["response"])