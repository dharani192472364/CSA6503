import ollama
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

documents = [
    "The motor should be inspected regularly for overheating.",
    "Check electrical connections when the motor does not start.",
    "Lubrication reduces friction between moving components.",
    "Replace damaged cables before operating the machine."
]

# Embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

vectors = model.encode(documents)
vectors = np.asarray(
    vectors,
    dtype="float32"
)

# FAISS
index = faiss.IndexFlatL2(
    vectors.shape[1]
)

index.add(vectors)

# Question
question = input(
    "Describe your engineering problem: "
)

query_vector = model.encode([question])
query_vector = np.asarray(
    query_vector,
    dtype="float32"
)

# Retrieve
distances, ids = index.search(
    query_vector,
    2
)

context = "\n".join(
    documents[i]
    for i in ids[0]
)

prompt = f"""
You are an engineering maintenance assistant.

Use only the following manual information.

Manual:
{context}

Problem:
{question}

Give clear step-by-step recommendations.
"""

response = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

print("\nTroubleshooting Answer:")
print(response["response"])