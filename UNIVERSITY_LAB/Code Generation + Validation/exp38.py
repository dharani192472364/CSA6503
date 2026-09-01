import ollama

problem = input(
    "Enter programming problem: "
)

prompt = f"""
You are a Python programming assistant.

Generate a Python program for the following problem.

Problem:
{problem}

Requirements:
- Use Python.
- Include input and output.
- Handle normal cases.
- Return only executable Python code.
"""

response = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

code = response["response"]

print("\nGenerated Code:")
print(code)