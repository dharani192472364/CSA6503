import ollama

print("======================================")
print(" Engineering Document Summarizer")
print("======================================")

text = input("\nEnter engineering text:\n")

if text.strip():

    prompt = f"""
Summarize the following engineering document.

Requirements:
- Keep the important information.
- Be accurate.
- Be concise.
- Remove unnecessary repetition.
- Use simple language.

Engineering Document:
{text}

Summary:
"""

    response = ollama.generate(
        model="llama3.2",
        prompt=prompt
    )

    print("\n========== SUMMARY ==========")
    print(response["response"])
    print("=============================")

else:
    print("Please enter some text.")