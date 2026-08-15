from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
text = """Artificial Intelligence is transforming the world.
Machine Learning is a subset of AI.
Deep Learning uses neural networks."""
sentences = [s.strip() for s in text.split(".") if s.strip()]
print("Sentence Tokenization:")
for i, sentence in enumerate(sentences, start=1):
    print(f"{i}. {sentence}")