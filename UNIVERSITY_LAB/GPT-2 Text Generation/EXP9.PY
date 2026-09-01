from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

prompt = "Artificial Intelligence is useful in engineering because"

result = generator(
    prompt,
    max_length=60,
    num_return_sequences=1
)

print("Generated Text:")
print(result[0]["generated_text"])