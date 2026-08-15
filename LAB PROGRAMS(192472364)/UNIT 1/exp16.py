from transformers import BertTokenizer, GPT2Tokenizer

bert = BertTokenizer.from_pretrained("bert-base-uncased")
gpt2 = GPT2Tokenizer.from_pretrained("gpt2")

text = "Artificial Intelligence"

print("BERT Tokens:")
print(bert.tokenize(text))

print("\nGPT-2 Tokens:")
print(gpt2.tokenize(text))
