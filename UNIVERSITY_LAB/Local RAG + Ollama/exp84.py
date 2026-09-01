import ollama
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

manual = [
    "If a motor overheats, switch it off and allow it to cool.",
    "Check whether the cooling fan is working properly.",
    "Inspect electrical connections for loose wires.",
    "Check the power supply before restarting the equipment.",
    "Damaged components should be replaced by qualified personnel."
]

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(manual)
embeddings = np.asarray(
    embeddings,
    dtype="float32"
)

index = faiss.IndexFlatL2(
    embeddings.shape[1]
)

index.add(embeddings)

problem = input(
    "Enter maintenance problem: "
)

query = model.encode([problem])
query = np.asarray(
    query,
    dtype="float32"
)

_, ids = index.search(query, 3)

context = "\n".join(
    manual[i]
    for i in ids[0]
)

prompt = f"""
You are a technical maintenance assistant.

Based only on the manual information below,
provide step-by-step troubleshooting advice.

Manual:
{context}

Problem:
{problem}
"""

answer = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

print("\n========== SOLUTION ==========")
print(answer["response"])