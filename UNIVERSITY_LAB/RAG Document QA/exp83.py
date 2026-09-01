import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Knowledge documents
documents = [
    "Artificial Intelligence enables machines to perform intelligent tasks.",
    "Machine learning allows computers to learn patterns from data.",
    "Deep learning uses neural networks with multiple layers.",
    "Natural Language Processing deals with human language.",
    "Computer Vision enables computers to understand images.",
    "Robotics is used for industrial automation."
]

# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Create document embeddings
document_vectors = model.encode(documents)
document_vectors = np.array(
    document_vectors,
    dtype="float32"
)

# Create FAISS vector database
index = faiss.IndexFlatL2(
    document_vectors.shape[1]
)

index.add(document_vectors)

# User question
question = input(
    "Enter your question: "
)

# Convert question to vector
question_vector = model.encode(
    [question]
)

question_vector = np.array(
    question_vector,
    dtype="float32"
)

# Retrieve top 2
distances, ids = index.search(
    question_vector,
    2
)

print("\n========== DOCUMENT QA ==========")

print("\nQuestion:")
print(question)

print("\nRetrieved Answers:")

for i in ids[0]:
    print("-", documents[i])

print("\n=================================")