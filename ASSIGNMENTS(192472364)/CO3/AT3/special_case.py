import pandas as pd
import numpy as np
import faiss
import chromadb
from sentence_transformers import SentenceTransformer

print("=" * 80)
print("SPECIAL CASE - GUEST SPEAKER FIELD MATCH")
print("=" * 80)

df = pd.read_csv("events.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

faiss_index = faiss.read_index("events_faiss.index")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("event_collection")

query = "cyber security expert speaker"

print("\nQuery:", query)

query_embedding = model.encode(
    [query],
    convert_to_numpy=True
).astype("float32")

# ------------------------------------------------------------
# FAISS
# ------------------------------------------------------------

distances, indices = faiss_index.search(
    query_embedding,
    5
)

print("\n" + "=" * 80)
print("FAISS TOP-5")
print("=" * 80)

for rank, idx in enumerate(indices[0], start=1):

    row = df.iloc[idx]

    print(f"\nRank {rank}")
    print("Event ID:", row["event_id"])
    print("Title:", row["title"])
    print("Category:", row["category"])
    print("Description:", row["description"])
    print("Distance:", round(float(distances[0][rank - 1]), 4))


# ------------------------------------------------------------
# CHROMADB
# ------------------------------------------------------------

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=5
)

print("\n" + "=" * 80)
print("CHROMADB TOP-5")
print("=" * 80)

for rank, event_id in enumerate(
    results["ids"][0],
    start=1
):

    event_id = int(event_id)

    row = df[
        df["event_id"] == event_id
    ].iloc[0]

    print(f"\nRank {rank}")
    print("Event ID:", row["event_id"])
    print("Title:", row["title"])
    print("Category:", row["category"])
    print("Description:", row["description"])
    print(
        "Distance:",
        round(float(results["distances"][0][rank - 1]), 4)
    )


# ------------------------------------------------------------
# SPECIAL CASE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("SPECIAL CASE ANALYSIS")
print("=" * 80)

special_event = df[
    df["event_id"] == 245
].iloc[0]

print("\nSpecial Event:")
print("Title:", special_event["title"])
print("Category:", special_event["category"])
print("Description:")
print(special_event["description"])

print("\nWhy is it relevant?")

print(
    "The query asks for a cybersecurity expert speaker."
)

print(
    "Event 245 includes a guest speaker who is "
    "a cybersecurity researcher."
)

print(
    "Therefore, the semantic match occurs through "
    "the guest speaker's professional field."
)

print(
    "\nThis demonstrates that sentence embeddings can "
    "retrieve semantically related events even when "
    "the main event category is different."
)

print("\n" + "=" * 80)
print("STEP 10 COMPLETED")
print("=" * 80)