import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Document
document = """
Artificial Intelligence is a technology that enables machines
to perform tasks requiring human intelligence.

Machine learning allows computers to learn from data.
Deep learning uses neural networks with multiple layers.
Natural language processing enables computers to understand
human language.

AI is used in engineering for automation, robotics and
predictive maintenance.
"""

# Chunking
sentences = document.split(".")

chunks = []

for sentence in sentences:
    if sentence.strip():
        chunks.append(sentence.strip())

# Embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)
embeddings = np.array(embeddings).astype("float32")

# Vector database
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# User query
question = input("Ask a question: ")

query_embedding = model.encode([question])
query_embedding = np.array(query_embedding).astype("float32")

# Retrieval
distance, ids = index.search(query_embedding, 2)

print("\n========== RAG SYSTEM ==========")

print("\nQuestion:")
print(question)

print("\nRetrieved Context:")

for i in ids[0]:
    print("-", chunks[i])

print("\n================================")