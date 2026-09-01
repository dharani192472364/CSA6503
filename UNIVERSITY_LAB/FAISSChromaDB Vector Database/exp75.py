import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "Electrical engineering studies electrical circuits and systems.",
    "Mechanical engineering focuses on machines and mechanisms.",
    "Civil engineering deals with buildings and infrastructure.",
    "Computer engineering combines hardware and software.",
    "Chemical engineering deals with industrial chemical processes."
]

embeddings = model.encode(documents)
embeddings = embeddings.astype("float32")

database = faiss.IndexFlatL2(embeddings.shape[1])
database.add(embeddings)

query = "Which branch studies machines?"

query_embedding = model.encode([query]).astype("float32")

distances, indices = database.search(
    query_embedding,
    3
)

print("Query:", query)
print("\nTop-K Results:")

for i in range(3):
    print("\nRank:", i + 1)
    print(documents[indices[0][i]])