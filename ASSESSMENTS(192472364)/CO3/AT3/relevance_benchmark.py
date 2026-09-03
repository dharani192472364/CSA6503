import pandas as pd
import numpy as np
import faiss
import chromadb
from sentence_transformers import SentenceTransformer

print("=" * 80)
print("TOP-5 RELEVANCE BENCHMARK")
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

# ------------------------------------------------------------
# Queries and expected categories
# ------------------------------------------------------------

query_data = [
    ("machine learning projects", "Machine Learning"),
    ("artificial intelligence workshop", "Artificial Intelligence"),
    ("robotics competition", "Robotics"),
    ("data analytics training", "Data Science"),
    ("startup funding session", "Business"),
    ("music and dance festival", "Culture"),
    ("football tournament", "Sports"),
    ("cyber security awareness", "Cybersecurity"),
    ("leadership development", "Business"),
    ("cyber security expert speaker", "Cybersecurity")
]

results = []

for number, (query, expected_category) in enumerate(
    query_data, start=1
):

    print("\n" + "=" * 80)
    print(f"QUERY {number}: {query}")
    print("Expected category:", expected_category)
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

    faiss_relevant = 0

    print("\nFAISS:")

    for rank, idx in enumerate(indices[0], start=1):

        category = df.iloc[idx]["category"]
        title = df.iloc[idx]["title"]

        is_relevant = (
            category == expected_category
        )

        if is_relevant:
            faiss_relevant += 1

        print(
            f"{rank}. {title} | "
            f"{category} | "
            f"Relevant: {is_relevant}"
        )

    faiss_score = faiss_relevant / 5

    # --------------------------------------------------------
    # CHROMADB
    # --------------------------------------------------------

    chroma = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=5
    )

    chroma_relevant = 0

    print("\nChromaDB:")

    for rank, event_id in enumerate(
        chroma["ids"][0],
        start=1
    ):

        event_id = int(event_id)

        row = df[
            df["event_id"] == event_id
        ].iloc[0]

        category = row["category"]
        title = row["title"]

        is_relevant = (
            category == expected_category
        )

        if is_relevant:
            chroma_relevant += 1

        print(
            f"{rank}. {title} | "
            f"{category} | "
            f"Relevant: {is_relevant}"
        )

    chroma_score = chroma_relevant / 5

    print("\nFAISS relevance:",
          f"{faiss_relevant}/5",
          f"({faiss_score * 100:.2f}%)")

    print("ChromaDB relevance:",
          f"{chroma_relevant}/5",
          f"({chroma_score * 100:.2f}%)")

    results.append({
        "Query Number": number,
        "Query": query,
        "Expected Category": expected_category,
        "FAISS Relevant": faiss_relevant,
        "FAISS Relevance (%)": faiss_score * 100,
        "ChromaDB Relevant": chroma_relevant,
        "ChromaDB Relevance (%)": chroma_score * 100
    })


# ------------------------------------------------------------
# FINAL AVERAGE
# ------------------------------------------------------------

result_df = pd.DataFrame(results)

avg_faiss = result_df[
    "FAISS Relevance (%)"
].mean()

avg_chroma = result_df[
    "ChromaDB Relevance (%)"
].mean()

print("\n" + "=" * 80)
print("FINAL RELEVANCE SUMMARY")
print("=" * 80)

print(
    "Average FAISS Top-5 Relevance:",
    f"{avg_faiss:.2f}%"
)

print(
    "Average ChromaDB Top-5 Relevance:",
    f"{avg_chroma:.2f}%"
)

# Save results
result_df.to_csv(
    "relevance_results.csv",
    index=False
)

print("\nResults saved as: relevance_results.csv")

print("=" * 80)
print("STEP 9 COMPLETED")
print("=" * 80)