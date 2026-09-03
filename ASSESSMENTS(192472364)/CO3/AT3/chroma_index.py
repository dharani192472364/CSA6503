import pandas as pd
import numpy as np
import chromadb
import time
import os

print("=" * 60)
print("CHROMADB - EVENT DESCRIPTION MATCHER")
print("=" * 60)

# Load dataset
df = pd.read_csv("events.csv")

# Load the SAME embeddings used by FAISS
embeddings = np.load("event_embeddings.npy")

print("Number of events:", len(df))
print("Embedding shape:", embeddings.shape)

# Create persistent ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")

# Delete old collection if it exists
try:
    client.delete_collection("event_collection")
    print("Old collection removed.")
except:
    pass

# Create collection
collection = client.create_collection(
    name="event_collection",
    metadata={"description": "Campus event semantic search"}
)

print("ChromaDB collection created.")

# Start indexing timer
start_time = time.perf_counter()

# Add all events using SAME embeddings
collection.add(
    ids=[str(x) for x in df["event_id"]],
    documents=df["description"].tolist(),
    metadatas=[
        {
            "title": row["title"],
            "category": row["category"]
        }
        for _, row in df.iterrows()
    ],
    embeddings=embeddings.tolist()
)

indexing_time = time.perf_counter() - start_time

print("\nChromaDB indexing completed.")
print("Number of documents:", collection.count())
print("Indexing time:", round(indexing_time, 6), "seconds")

# Calculate approximate database folder size
total_size = 0

for root, dirs, files in os.walk("chroma_db"):
    for file in files:
        filepath = os.path.join(root, file)
        total_size += os.path.getsize(filepath)

size_kb = total_size / 1024

print("ChromaDB storage size:", round(size_kb, 2), "KB")

print("=" * 60)
print("STEP 6 COMPLETED")
print("=" * 60)