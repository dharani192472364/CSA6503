import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

reports = [
    "The project uses Python for data processing.",
    "The system uses sensors to collect environmental data.",
    "The database stores student and project information.",
    "The application provides a web interface for users.",
    "Machine learning is used to predict future system conditions.",
    "The system uses cloud computing for data storage."
]

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

vectors = model.encode(reports)
vectors = np.array(vectors).astype("float32")

# Create vector database
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

# Question
question = input("Ask about the technical reports: ")

query_vector = model.encode([question])
query_vector = np.array(query_vector).astype("float32")

# Retrieve top 3
distances, ids = index.search(query_vector, 3)

print("\n========== TECHNICAL AI ASSISTANT ==========")

print("\nQuestion:", question)

print("\nRelevant Information:")

for i in ids[0]:
    print("\n", reports[i])

print("\n============================================")