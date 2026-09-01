import ollama

problem = input(
    "Enter Python programming requirement: "
)

prompt = f"""
Write a simple Python program for:

{problem}

Return ONLY executable Python code.
Do not use markdown.
"""

response = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

code = response["response"].strip()

print("\nGenerated Code:")
print(code)

print("\n========== VALIDATION ==========")

try:
    compile(code, "<generated_code>", "exec")
    print("Code validation successful.")
    print("The generated code has valid Python syntax.")

except SyntaxError as e:
    print("Syntax Error:")
    print(e)