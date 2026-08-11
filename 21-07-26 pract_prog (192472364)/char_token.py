from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("google/byt5-small")
text = "Artificial Intelligence"
tokens = tokenizer.tokenize(text)
print("Character Tokens:")
print(tokens)