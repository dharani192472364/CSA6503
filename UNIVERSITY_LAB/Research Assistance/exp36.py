import ollama

topic = input(
    "Enter engineering research topic: "
)

prompt = f"""
You are an engineering research assistant.

Research Topic:
{topic}

Provide:

1. Introduction
2. Important concepts
3. Applications
4. Research keywords
5. Current challenges
6. Future scope
7. Short summary
"""

response = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

print("\n========== RESEARCH ASSISTANCE ==========")
print(response["response"])