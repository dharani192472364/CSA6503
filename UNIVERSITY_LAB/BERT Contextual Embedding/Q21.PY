import torch 
from transformers import BertTokenizer,BertModel

tokenizer=BertTokenizer.from_pretrained("bert-base-uncased")
model=BertModel.from_pretrained("bert-base-uncased")

sent="Artificial intelligence is used in engineering applications."

token_ids=tokenizer(sent,return_tensors="pt")

with torch.no_grad():
    output=model(**token_ids)

embeddings=output.last_hidden_state

print("Original Sentence:")
print(sent)

print("\nEmbedding Shape:")
print(embeddings.shape)

print("\nContextual Embedding:")
print(embeddings)