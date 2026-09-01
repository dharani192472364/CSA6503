import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

documents = [
    "Students must maintain the required attendance percentage.",
    "Students must carry their identity card inside the campus.",
    "Laboratory students must follow all safety instructions.",
    "Students must submit laboratory records before the deadline.",
    "Students must follow examination rules and regulations.",
    "The library provides textbooks, journals and digital resources."
]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
vectors = model.encode(documents)
vectors = np.array(vectors).astype("float32")

# Create vector database
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

# Question
question = input("Ask about college regulations: ")

query = model.encode([question])
query = np.array(query).astype("float32")

# Retrieve
distance, ids = index.search(query, 2)

print("\n========== RAG RESULT ==========")

print("\nQuestion:", question)

print("\nRelevant Information:")

for i in ids[0]:
    print("-", documents[i])

print("\n================================")