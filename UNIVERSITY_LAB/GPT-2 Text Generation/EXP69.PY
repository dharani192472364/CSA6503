from transformers import pipeline

model = pipeline("text-generation", model="gpt2")

prompt = "Robotics plays an important role in modern engineering"

answer = model(
    prompt,
    max_new_tokens=50,
    do_sample=True,
    num_return_sequences=1
)

print("Prompt:", prompt)
print("\nPredicted Continuation:")
print(answer[0]["generated_text"])