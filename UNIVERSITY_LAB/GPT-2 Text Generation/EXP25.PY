from transformers import pipeline

text_generator = pipeline("text-generation", model="gpt2")

sentence = "The future of engineering technology depends on"

output = text_generator(
    sentence,
    max_new_tokens=40,
    num_return_sequences=1
)

print("Input:")
print(sentence)

print("\nContinuation:")
print(output[0]["generated_text"])