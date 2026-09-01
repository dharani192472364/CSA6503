from transformers import BertTokenizer

tokenizer=BertTokenizer.from_pretrained("bert-base-uncased")

sent="i am studying well"

tokens=tokenizer.tokenize(sent)

token_ids=tokenizer.convert_tokens_to_ids(tokens)

print("original sentence: ")
print(sent)

print ("bert tokens: ")
print(tokens)

print("token ids: ")
print(token_ids)