import ollama

problem = input(
    "Enter computational problem: "
)

prompt = f"""
Generate a Python solution for this problem:

{problem}

Return only Python code.
"""

response = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

code = response["response"]

print("\nGenerated Program:")
print(code)

print("\nCode generation completed.")
print("Validate the program with suitable test cases.")