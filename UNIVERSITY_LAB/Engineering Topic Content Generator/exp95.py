import ollama

topic = input(
    "Enter engineering topic: "
)

prompt = f"""
You are an engineering content generator.

Topic:
{topic}

Create a structured explanation containing:

Introduction:
Key Concepts:
Applications:
Advantages:
Challenges:
Conclusion:

Make the content technically clear and easy
for engineering students to understand.
"""

result = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

print("\n========== GENERATED CONTENT ==========")
print(result["response"])