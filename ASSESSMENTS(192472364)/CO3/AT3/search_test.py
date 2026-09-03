import pandas as pd
import numpy as np
import faiss
import chromadb
import time
from sentence_transformers import SentenceTransformer

print("=" * 70)
print("SEMANTIC SEARCH TEST")
print("=" * 70)

# Load dataset
df = pd.read_csv("events.csv")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
faiss_index = faiss.read_index("events_faiss.index")

# Load ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("event_collection")

# Query
query = "machine learning projects"

print("\nQuery:", query)

# Generate query embedding
query_embedding = model.encode(
    [query],
    convert_to_numpy=True
).astype("float32")


# ============================================================
# FAISS SEARCH
# ============================================================

print("\n" + "=" * 70)
print("FAISS TOP-5 RESULTS")
print("=" * 70)

start = time.perf_counter()

distances, indices = faiss_index.search(
    query_embedding,
    5
)

faiss_latency = (time.perf_counter() - start) * 1000

for rank, idx in enumerate(indices[0], start=1):
    print(f"\nRank {rank}")
    print("Event ID:", df.iloc[idx]["event_id"])
    print("Title:", df.iloc[idx]["title"])
    print("Category:", df.iloc[idx]["category"])
    print("Distance:", round(float(distances[0][rank - 1]), 4))

print("\nFAISS Query Latency:",
      round(faiss_latency, 4), "ms")


# ============================================================
# CHROMADB SEARCH
# ============================================================

print("\n" + "=" * 70)
print("CHROMADB TOP-5 RESULTS")
print("=" * 70)

start = time.perf_counter()

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=5
)

chroma_latency = (time.perf_counter() - start) * 1000

for rank in range(5):
    event_id = int(results["ids"][0][rank])

    row = df[df["event_id"] == event_id].iloc[0]

    print(f"\nRank {rank + 1}")
    print("Event ID:", event_id)
    print("Title:", row["title"])
    print("Category:", row["category"])
    print("Distance:", round(float(results["distances"][0][rank]), 4))

print("\nChromaDB Query Latency:",
      round(chroma_latency, 4), "ms")

print("\n" + "=" * 70)
print("SEARCH TEST COMPLETED")
print("=" * 70)