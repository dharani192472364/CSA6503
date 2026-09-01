import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Create external document
os.makedirs("external_docs", exist_ok=True)

text = """
Python is a high-level programming language.
Python is widely used in artificial intelligence and data science.
SQL is used to manage relational databases.
Computer networks allow computers to communicate.
Cloud computing provides computing resources through the Internet.
"""

with open("external_docs/technical.txt", "w", encoding="utf-8") as f:
    f.write(text)

# Load external document
with open("external_docs/technical.txt", "r", encoding="utf-8") as f:
    document = f.read()

# Create chunks
chunks = [
    line.strip()
    for line in document.split(".")
    if line.strip()
]

# Embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

vectors = model.encode(chunks)
vectors = np.array(vectors).astype("float32")

# FAISS
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

# User question
question = input("Ask a question: ")

query = model.encode([question])
query = np.array(query).astype("float32")

# Retrieve
distance, ids = index.search(query, 2)

print("\nAI Assistant Answer")

for i in ids[0]:
    print("•", chunks[i])