import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

documents = [
    "The college library provides engineering textbooks.",
    "Students can borrow books using their college identity card.",
    "Laboratory attendance is compulsory for practical courses.",
    "Students must follow laboratory safety procedures.",
    "Internal examinations are conducted according to the academic schedule.",
    "Students should submit assignments before the specified deadline."
]

model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert documents to embeddings
embeddings = model.encode(documents)
embeddings = np.array(embeddings).astype("float32")

# Vector database
database = faiss.IndexFlatL2(embeddings.shape[1])
database.add(embeddings)

# User question
question = input("Enter your academic question: ")

query_vector = model.encode([question])
query_vector = np.array(query_vector).astype("float32")

# Search
distances, indices = database.search(
    query_vector,
    2
)

print("\nQuestion:")
print(question)

print("\nAnswer from Documents:")

for i in indices[0]:
    print(documents[i])