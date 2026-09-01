import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

docs = [
    "Computer networks enable communication between devices.",
    "Database systems organize and store information.",
    "Artificial intelligence supports intelligent decision making.",
    "Robotics combines mechanical and computer systems."
]

embeddings = model.encode(docs)
embeddings = np.asarray(embeddings, dtype="float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

question = "How is information stored and organized?"

q = model.encode([question])
q = np.asarray(q, dtype="float32")

distances, ids = index.search(q, 2)

print("Question:", question)

for rank, doc_id in enumerate(ids[0], 1):
    print("\nRank:", rank)
    print("Document:", docs[doc_id])
    print("Distance:", distances[0][rank - 1])