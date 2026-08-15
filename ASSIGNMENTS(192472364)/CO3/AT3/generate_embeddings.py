import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import time

print("=" * 60)
print("EVENT DESCRIPTION EMBEDDING GENERATION")
print("=" * 60)

# Load dataset
df = pd.read_csv("events.csv")

print("Total events:", len(df))

# Load sentence embedding model
print("\nLoading model: all-MiniLM-L6-v2")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully.")

# Generate embeddings
print("\nGenerating embeddings...")

start_time = time.time()

embeddings = model.encode(
    df["description"].tolist(),
    show_progress_bar=True,
    convert_to_numpy=True
)

embedding_time = time.time() - start_time

print("\nEmbeddings generated successfully.")

# Display information
print("\nEmbedding Information")
print("-" * 40)
print("Number of embeddings:", len(embeddings))
print("Embedding dimension:", embeddings.shape[1])
print("Embedding shape:", embeddings.shape)
print("Generation time:", round(embedding_time, 4), "seconds")

# Save embeddings
np.save("event_embeddings.npy", embeddings)

print("\nEmbeddings saved as: event_embeddings.npy")

print("=" * 60)
print("STEP 4 COMPLETED")
print("=" * 60)