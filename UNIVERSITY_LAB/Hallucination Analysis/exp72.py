import ollama

question = input(
    "Enter a technical question: "
)

prompt = f"""
Answer the following technical question.

Question:
{question}

If you are uncertain, clearly state that
you do not have enough information.
Do not invent facts.
"""

response = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

print("\n========== AI RESPONSE ==========")
print(response["response"])

print("\n========== REFERENCE ==========")
print("Verify the answer using a trusted technical source.")

print("\nHallucination analysis:")
print("Check whether every factual claim in the response")
print("is supported by the reference information.")