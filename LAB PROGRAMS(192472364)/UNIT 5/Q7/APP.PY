import ollama

print("LOCAL LLM HALLUCINATION DEMONSTRATION")

reference = """
Saveetha School of Engineering offers engineering education.
The college provides various undergraduate and postgraduate
engineering programs.
"""

print("\nREFERENCE INFORMATION:")
print(reference)

question = input("\nEnter a question about the reference: ")

prompt = f"""
You are answering questions using the reference information below.

REFERENCE:
{reference}

QUESTION:
{question}

Answer the question using ONLY the reference.
If the answer cannot be found in the reference, say:
"I don't know based on the given reference."
"""

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

answer = response["message"]["content"]

print("\nLLM ANSWER:")
print(answer)

# Hallucination analysis
analysis_prompt = f"""
Analyze the following answer against the reference.

REFERENCE:
{reference}

QUESTION:
{question}

LLM ANSWER:
{answer}

Determine whether the answer contains hallucinated information.

Give the result in this format:

HALLUCINATION: YES or NO
REASON: Explain briefly whether the answer is supported by the reference.
"""

analysis = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": analysis_prompt
        }
    ]
)

print("\nHALLUCINATION ANALYSIS:")
print(analysis["message"]["content"])