from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="sshleifer/tiny-gpt2"
)

prompts = [
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning"
]

for prompt in prompts:
    print("\nPrompt:", prompt)
    result = generator(
        prompt,
        max_length=30,
        num_return_sequences=1
    )
    print(result[0]["generated_text"])