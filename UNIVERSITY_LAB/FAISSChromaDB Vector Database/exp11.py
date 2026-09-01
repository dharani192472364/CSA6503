import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "Artificial intelligence is used in engineering.",
    "Python is a programming language.",
    "SQL manages relational databases.",
    "Networks connect computers.",
    "Robotics is used in automation."
]

vectors = model.encode(documents)
vectors = np.array(vectors).astype("float32")

dimension = vectors.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(vectors)

query = "Which technology is used for automation?"

query_vector = model.encode([query])
query_vector = np.array(query_vector).astype("float32")

distance, result = index.search(query_vector, 3)

print("Query:", query)
print("\nTop Results:")

for i in result[0]:
    print(documents[i])