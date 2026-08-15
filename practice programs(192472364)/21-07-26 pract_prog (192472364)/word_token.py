from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
text = "Artificial Intelligence is transforming the world."
tokens = tokenizer.tokenize(text)
print("Word Tokens:")
for token in tokens:
    print(token)