from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "Python is commonly used for artificial intelligence.",
    "SQL is used for managing relational databases.",
    "TCP/IP is an important networking protocol.",
    "Robots are used for industrial automation."
]

query = "Which technology is useful for AI development?"

documents_vector = model.encode(documents)
query_vector = model.encode([query])

similarity = cosine_similarity(
    query_vector,
    documents_vector
)[0]

best = similarity.argmax()

print("Query:", query)
print("\nMost Relevant Document:")
print(documents[best])
print("\nSimilarity Score:", round(similarity[best], 4))