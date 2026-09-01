import ollama

print("======================================")
print("     Engineering Text Summarizer")
print("======================================")

text = input("\nEnter the engineering text:\n")

if text.strip():

    prompt = f"""
Summarize the following engineering text.

Requirements:
1. Keep the main ideas.
2. Remove unnecessary details.
3. Make the summary concise.
4. Maintain the original meaning.
5. Use clear and simple language.

Text:
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