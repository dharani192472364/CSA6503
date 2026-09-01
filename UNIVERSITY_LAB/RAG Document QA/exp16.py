import os
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# ==========================================
# 1. CREATE DOCUMENT AUTOMATICALLY
# ==========================================

os.makedirs("documents", exist_ok=True)

document_path = "documents/engineering.txt"

document_text = """
Artificial Intelligence is a branch of computer science.
It enables machines to perform tasks that normally require
human intelligence.

Artificial Intelligence is used in engineering for robotics,
automation, predictive maintenance and design optimization.

Machine learning is a part of Artificial Intelligence.
It allows computers to learn patterns from data and make
predictions without being explicitly programmed.

Robotics combines computer science, electronics and mechanical
engineering to develop automated machines.

Predictive maintenance uses machine learning to predict
equipment failures before they occur.
"""

with open(document_path, "w", encoding="utf-8") as file:
    file.write(document_text)

print("Document created successfully.")

# ==========================================
# 2. LOAD DOCUMENT
# ==========================================

with open(document_path, "r", encoding="utf-8") as file:
    text = file.read()

print("Document loaded successfully.")

# ==========================================
# 3. TEXT CHUNKING
# ==========================================

words = text.split()

chunks = []

for i in range(0, len(words), 50):

    chunk = " ".join(words[i:i + 50])

    if chunk:
        chunks.append(chunk)

print("Number of chunks:", len(chunks))

# ==========================================
# 4. CREATE EMBEDDINGS
# ==========================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(chunks)

embeddings = np.array(
    embeddings,
    dtype="float32"
)

# ==========================================
# 5. CREATE FAISS VECTOR DATABASE
# ==========================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("FAISS vector database created.")

# ==========================================
# 6. USER QUESTION
# ==========================================

question = input(
    "\nEnter your question: "
)

# ==========================================
# 7. EMBED QUESTION
# ==========================================

query_embedding = model.encode(
    [question]
)

query_embedding = np.array(
    query_embedding,
    dtype="float32"
)

# ==========================================
# 8. RETRIEVE RELEVANT CHUNKS
# ==========================================

k = min(2, len(chunks))

distances, indices = index.search(
    query_embedding,
    k
)

# ==========================================
# 9. DISPLAY ANSWER CONTEXT
# ==========================================

print("\n========== RAG RESULT ==========")

print("\nQuestion:")
print(question)

print("\nRelevant Information:")

for i in indices[0]:

    print("\n-------------------------")
    print(chunks[i])

print("\n==============================")