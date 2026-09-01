import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("all-MiniLM-L6-v2")

reports = [
    "A report about artificial intelligence applications.",
    "A report about computer network security.",
    "A report about database management systems.",
    "A report about robotic automation.",
    "A report about machine learning algorithms."
]

vectors = encoder.encode(reports)
vectors = np.array(vectors, dtype="float32")

faiss_db = faiss.IndexFlatL2(vectors.shape[1])
faiss_db.add(vectors)

query = "Technical report about robots and automation"

query_vector = encoder.encode([query])
query_vector = np.array(query_vector, dtype="float32")

distances, indexes = faiss_db.search(
    query_vector,
    2
)

print("Query:", query)

for index in indexes[0]:
    print("\nRetrieved Report:")
    print(reports[index])