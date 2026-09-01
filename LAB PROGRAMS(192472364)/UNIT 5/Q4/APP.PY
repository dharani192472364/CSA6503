import ollama

print("LOCAL LLM TRANSLATION AND PARAPHRASING")
print("1. Translation")
print("2. Paraphrasing")

choice = input("\nEnter your choice: ")

text = input("Enter the text: ")

if choice == "1":
    language = input("Enter target language: ")

    prompt = f"""
    Translate the following text into {language}.
    Preserve the original meaning accurately.

    Text:
    {text}
    """

elif choice == "2":

    prompt = f"""
    Paraphrase the following text.
    Preserve the original meaning but use different
    words and sentence structure.

    Text:
    {text}
    """

else:
    print("Invalid choice")
    exit()

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\nResult:")
print(response["message"]["content"])