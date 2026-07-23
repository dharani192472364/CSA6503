from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

sentence = "Machine Learning is amazing."

tokens = tokenizer.tokenize(sentence)

print(tokens)
