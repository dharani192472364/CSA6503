import pandas as pd
import numpy as np
import faiss
import chromadb
import time
from sentence_transformers import SentenceTransformer

print("=" * 80)
print("FAISS vs CHROMADB - SEMANTIC SEARCH BENCHMARK")
print("=" * 80)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv("events.csv")

embeddings = np.load("event_embeddings.npy")

print("Total events:", len(df))
print("Embedding dimension:", embeddings.shape[1])

# ------------------------------------------------------------
# LOAD MODEL
# ------------------------------------------------------------

print("\nLoading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded.")

# ------------------------------------------------------------
# LOAD FAISS
# ------------------------------------------------------------

faiss_index = faiss.read_index("events_faiss.index")

# ------------------------------------------------------------
# LOAD CHROMADB
# ------------------------------------------------------------

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection("event_collection")

# ------------------------------------------------------------
# 10 SEMANTIC QUERIES
# ------------------------------------------------------------

queries = [
    "machine learning projects",
    "artificial intelligence workshop",
    "robotics competition",
    "data analytics training",
    "startup funding session",
    "music and dance festival",
    "football tournament",
    "cyber security awareness",
    "leadership development",
    "cyber security expert speaker"
]

# ------------------------------------------------------------
# RESULTS STORAGE
# ------------------------------------------------------------

faiss_latencies = []
chroma_latencies = []

all_results = []

# ------------------------------------------------------------
# RUN BENCHMARK
# ------------------------------------------------------------

for query_number, query in enumerate(queries, start=1):

    print("\n" + "=" * 80)
    print(f"QUERY {query_number}: {query}")
    print("=" * 80)

    # Generate query embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    # --------------------------------------------------------
    # FAISS
    # --------------------------------------------------------

    start = time.perf_counter()

    distances, indices = faiss_index.search(
        query_embedding,
        5
    )

    faiss_time = (time.perf_counter() - start) * 1000

    faiss_latencies.append(faiss_time)

    faiss_results = []

    print("\nFAISS TOP-5")

    for rank, idx in enumerate(indices[0], start=1):

        event_id = int(df.iloc[idx]["event_id"])
        title = df.iloc[idx]["title"]

        faiss_results.append(event_id)

        print(
            f"{rank}. {title} "
            f"(ID: {event_id})"
        )

    print(
        "FAISS latency:",
        round(faiss_time, 4),
        "ms"
    )

    # --------------------------------------------------------
    # CHROMADB
    # --------------------------------------------------------

    start = time.perf_counter()

    chroma_results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=5
    )

    chroma_time = (time.perf_counter() - start) * 1000

    chroma_latencies.append(chroma_time)

    chroma_ids = [
        int(x)
        for x in chroma_results["ids"][0]
    ]

    print("\nCHROMADB TOP-5")

    for rank, event_id in enumerate(chroma_ids, start=1):

        row = df[df["event_id"] == event_id].iloc[0]

        print(
            f"{rank}. {row['title']} "
            f"(ID: {event_id})"
        )

    print(
        "ChromaDB latency:",
        round(chroma_time, 4),
        "ms"
    )

    # --------------------------------------------------------
    # OVERLAP
    # --------------------------------------------------------

    overlap = len(
        set(faiss_results) &
        set(chroma_ids)
    )

    print("\nTop-5 overlap:", overlap, "/ 5")

    all_results.append({
        "Query Number": query_number,
        "Query": query,
        "FAISS Results": faiss_results,
        "ChromaDB Results": chroma_ids,
        "Overlap": overlap,
        "FAISS Latency (ms)": faiss_time,
        "ChromaDB Latency (ms)": chroma_time
    })


# ------------------------------------------------------------
# AVERAGE LATENCY
# ------------------------------------------------------------

avg_faiss = sum(faiss_latencies) / len(faiss_latencies)

avg_chroma = sum(chroma_latencies) / len(chroma_latencies)

# ------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("FINAL BENCHMARK SUMMARY")
print("=" * 80)

print(
    "\nAverage FAISS Query Latency:",
    round(avg_faiss, 4),
    "ms"
)

print(
    "Average ChromaDB Query Latency:",
    round(avg_chroma, 4),
    "ms"
)

print(
    "\nAverage Top-5 Overlap:",
    round(
        sum(r["Overlap"] for r in all_results)
        / len(all_results),
        2
    ),
    "/ 5"
)

# ------------------------------------------------------------
# SAVE RESULTS
# ------------------------------------------------------------

# ------------------------------------------------------------
# SAVE RESULTS
# ------------------------------------------------------------

summary_rows = []

for result in all_results:

    summary_rows.append({
        "Query Number": result["Query Number"],
        "Query": result["Query"],
        "Top-5 Overlap": result["Overlap"],
        "FAISS Latency (ms)": round(
            result["FAISS Latency (ms)"], 4
        ),
        "ChromaDB Latency (ms)": round(
            result["ChromaDB Latency (ms)"], 4
        )
    })

summary_df = pd.DataFrame(summary_rows)

summary_df.to_csv(
    "benchmark_results.csv",
    index=False
)

print("\nResults saved to:")
print("benchmark_results.csv")

print("\n" + "=" * 80)
print("STEP 8 COMPLETED")
print("=" * 80)