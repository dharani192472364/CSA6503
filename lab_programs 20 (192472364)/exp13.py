from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="sshleifer/tiny-gpt2"
)

result = generator(
    "Artificial Intelligence is",
    max_length=30,
    num_return_sequences=1
)

print(result[0]["generated_text"])
