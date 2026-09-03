from dataclasses import dataclass


# ============================================================
# KNOWLEDGEDESK - Q11 LATENCY CONFIGURATION ANALYSIS
# ============================================================

@dataclass
class Configuration:
    name: str
    retrieval_ms: int
    reranking_ms: int
    llm_ms: int
    overhead_ms: int


configurations = [

    Configuration(
        name="Configuration 1 - Standard RAG",
        retrieval_ms=350,
        reranking_ms=300,
        llm_ms=1800,
        overhead_ms=250
    ),

    Configuration(
        name="Configuration 2 - Optimized RAG",
        retrieval_ms=200,
        reranking_ms=150,
        llm_ms=1500,
        overhead_ms=200
    ),

    Configuration(
        name="Configuration 3 - Fast RAG",
        retrieval_ms=120,
        reranking_ms=80,
        llm_ms=1100,
        overhead_ms=150
    )
]


# ============================================================
# CALCULATE TOTAL LATENCY
# ============================================================

def calculate_latency(config):
    return (
        config.retrieval_ms
        + config.reranking_ms
        + config.llm_ms
        + config.overhead_ms
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("=" * 75)
print("KNOWLEDGEDESK - Q11 LATENCY CONFIGURATION ANALYSIS")
print("=" * 75)

print("\nSystem Requirements")
print("-" * 75)
print("Concurrent users          : 500")
print("Target latency (90%)      : <= 3000 ms")
print("Available GPU             : 24 GB VRAM")
print("Vector database           : <= 100 GB")


print("\nLatency Configurations")
print("-" * 75)

results = []

for config in configurations:

    total = calculate_latency(config)

    meets_requirement = total <= 3000

    results.append((config.name, total, meets_requirement))

    print(f"\n{config.name}")
    print(f"  Retrieval latency       : {config.retrieval_ms} ms")
    print(f"  Re-ranking latency      : {config.reranking_ms} ms")
    print(f"  LLM generation latency  : {config.llm_ms} ms")
    print(f"  System overhead         : {config.overhead_ms} ms")
    print(f"  --------------------------------")
    print(f"  Total latency            : {total} ms")
    print(
        f"  Meets <= 3 second target : "
        f"{'YES' if meets_requirement else 'NO'}"
    )


# ============================================================
# BEST CONFIGURATION
# ============================================================

valid_results = [
    result for result in results
    if result[2]
]

print("\n" + "=" * 75)
print("FINAL LATENCY COMPARISON")
print("=" * 75)

print(
    f"{'Configuration':35}"
    f"{'Latency (ms)':15}"
    f"{'<= 3000 ms':15}"
)

print("-" * 75)

for name, latency, valid in results:

    print(
        f"{name:35}"
        f"{latency:<15}"
        f"{'YES' if valid else 'NO':<15}"
    )


if valid_results:

    best = min(valid_results, key=lambda x: x[1])

    print("\nRecommended configuration:")
    print(best[0])

    print(f"Latency: {best[1]} ms")

else:

    print("\nNo configuration meets the 3-second target.")


# ============================================================
# ARCHITECTURAL OPTIMIZATION
# ============================================================

print("\n" + "=" * 75)
print("RECOMMENDED LATENCY OPTIMIZATIONS")
print("=" * 75)

optimizations = [
    "Use FAISS or another low-latency vector index.",
    "Keep frequently accessed embeddings in memory.",
    "Use top-k retrieval with a small candidate set.",
    "Use a lightweight re-ranker only when necessary.",
    "Use a quantized local LLM to reduce generation latency.",
    "Stream LLM responses to improve perceived responsiveness.",
    "Batch embedding operations for multiple requests.",
    "Use asynchronous request handling for concurrent users.",
    "Cache repeated queries and retrieval results.",
    "Monitor p50, p90 and p95 latency continuously."
]

for i, item in enumerate(optimizations, start=1):
    print(f"{i}. {item}")


print("\nQ11 latency analysis completed.")
print("=" * 75)