import pandas as pd
import numpy as np
import faiss
import time
import os

print("=" * 60)
print("FAISS DATABASE - EVENT DESCRIPTION MATCHER")
print("=" * 60)

# Load dataset
df = pd.read_csv("events.csv")

# Load the SAME embeddings generated in Step 4
embeddings = np.load("event_embeddings.npy")

print("Number of events:", len(df))
print("Embedding shape:", embeddings.shape)

# FAISS requires float32
embeddings = embeddings.astype("float32")

# Get embedding dimension
dimension = embeddings.shape[1]

print("Embedding dimension:", dimension)

# Create FAISS index
print("\nCreating FAISS index...")

start_time = time.perf_counter()

index = faiss.IndexFlatL2(dimension)

# Add embeddings
index.add(embeddings)

indexing_time = time.perf_counter() - start_time

print("\nFAISS index created successfully.")
print("Number of vectors in FAISS:", index.ntotal)
print("Indexing time:", round(indexing_time, 6), "seconds")

# Save index
index_path = "events_faiss.index"
faiss.write_index(index, index_path)

print("FAISS index saved as:", index_path)

# Check file size
file_size = os.path.getsize(index_path) / 1024

print("FAISS index size:", round(file_size, 2), "KB")

print("=" * 60)
print("STEP 5 COMPLETED")
print("=" * 60)