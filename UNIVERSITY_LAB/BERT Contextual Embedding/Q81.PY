import torch
from transformers import BertModel,BertTokenizer

tokenizer=BertTokenizer.from_pretrained("bert-base-uncased")
model=BertModel.from_pretrained("bert-base-uncased")

sentences = [
    "The robotic system uses sensors to detect obstacles.",
    "The electric vehicle uses a battery management system.",
    "The solar panel converts sunlight into electrical energy.",
    "The IoT system monitors temperature and humidity.",
    "The neural network classifies images using extracted features."
]

inputs=tokenizer(sentences,return_tensors="pt",padding=True,truncation=True)
with torch.no_grad():
    output=model(**inputs)

embedding=output.last_hidden_state

print("Sentences:")
for i, sentence in enumerate(sentences, 1):
    print(i, sentence)

print("\nContextual Embeddings:")
print(embedding)
