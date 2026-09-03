import pandas as pd
import numpy as np
import faiss
import chromadb
from sentence_transformers import SentenceTransformer

print("=" * 80)
print("FAISS vs CHROMADB - TOP-5 COMPARISON")
print("=" * 80)

# Load dataset
df = pd.read_csv("events.csv")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS
faiss_index = faiss.read_index("events_faiss.index")

# Load ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("event_collection")


queries = [
    "machine learning projects",
    "music and dance festival",
    "cyber security expert speaker"
]


for number, query in enumerate(queries, start=1):

    print("\n" + "=" * 80)
    print(f"QUERY {number}: {query}")
    print("=" * 80)

    # Query embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    # --------------------------------------------------------
    # FAISS
    # --------------------------------------------------------

    distances, indices = faiss_index.search(
        query_embedding,
        5
    )

    faiss_ids = [
        int(df.iloc[idx]["event_id"])
        for idx in indices[0]
    ]

    print("\nFAISS Top-5 Event IDs:")
    print(faiss_ids)

    # --------------------------------------------------------
    # CHROMADB
    # --------------------------------------------------------

    chroma_results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=5
    )

    chroma_ids = [
        int(event_id)
        for event_id in chroma_results["ids"][0]
    ]

    print("ChromaDB Top-5 Event IDs:")
    print(chroma_ids)

    # --------------------------------------------------------
    # OVERLAP
    # --------------------------------------------------------

    overlap = set(faiss_ids) & set(chroma_ids)

    faiss_only = set(faiss_ids) - set(chroma_ids)

    chroma_only = set(chroma_ids) - set(faiss_ids)

    print("\nCommon results:")
    print(sorted(overlap))

    print("\nFAISS-only results:")
    print(sorted(faiss_only))

    print("\nChromaDB-only results:")
    print(sorted(chroma_only))

    print(
        "\nOverlap:",
        len(overlap),
        "/ 5"
    )

    if faiss_ids == chroma_ids:
        print("Result order: IDENTICAL")
    else:
        print("Result order: DIFFERENT")


print("\n" + "=" * 80)
print("COMPARISON COMPLETE")
print("=" * 80)