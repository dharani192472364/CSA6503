from transformers import BertTokenizer, BertModel
import torch

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

s1 = "The cat is sleeping."
s2 = "A cat is taking a nap."

inputs1 = tokenizer(s1, return_tensors="pt")
inputs2 = tokenizer(s2, return_tensors="pt")

with torch.no_grad():
    out1 = model(**inputs1)
    out2 = model(**inputs2)

print("Sentence 1 Shape:", out1.last_hidden_state.shape)
print("Sentence 2 Shape:", out2.last_hidden_state.shape)