from transformers import pipeline

gpt = pipeline("text-generation", model="gpt2")

prompt = "Our engineering project proposes a smart system that"

generated = gpt(
    prompt,
    max_length=70,
    temperature=0.8,
    num_return_sequences=1
)

print("Engineering Project Proposal:")
print(generated[0]["generated_text"])