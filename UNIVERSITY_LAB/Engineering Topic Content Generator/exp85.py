import ollama

topic = input(
    "Enter engineering topic: "
)

prompt = f"""
Generate educational content about:

{topic}

Include:

1. Introduction
2. Key Concepts
3. Applications
4. Advantages
5. Challenges
6. Conclusion

Use simple language suitable for engineering students.
"""

response = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

print("\n========== ENGINEERING CONTENT ==========")
print(response["response"])