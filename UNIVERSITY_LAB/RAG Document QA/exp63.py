import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Create folder
os.makedirs("multiple_docs", exist_ok=True)

# Create multiple documents
files = {
    "python.txt":
        "Python is a programming language used for AI and data science.",

    "network.txt":
        "Computer networks connect computers and allow communication.",

    "database.txt":
        "Databases store and manage structured information.",

    "robotics.txt":
        "Robotics combines software, electronics and mechanical engineering."
}

for filename, content in files.items():

    with open(
        "multiple_docs/" + filename,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(content)

# Load all documents
chunks = []
file_names = []

for filename in os.listdir("multiple_docs"):

    if filename.endswith(".txt"):

        with open(
            "multiple_docs/" + filename,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        chunks.append(text)
        file_names.append(filename)

# Embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

vectors = model.encode(chunks)
vectors = np.array(vectors).astype("float32")

# FAISS database
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

# Query
question = input(
    "Ask a question across all documents: "
)

query_vector = model.encode([question])
query_vector = np.array(query_vector).astype("float32")

# Top 3
k = min(3, len(chunks))

distance, ids = index.search(
    query_vector,
    k
)

print("\n========== MULTI-DOCUMENT SEARCH ==========")

for i in ids[0]:

    print("\nFile:", file_names[i])
    print("Information:", chunks[i])

print("\n===========================================")