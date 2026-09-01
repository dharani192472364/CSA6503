from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "Artificial intelligence is used in engineering automation.",
    "Computer networks connect computers and devices.",
    "Database systems store and retrieve information.",
    "Robotics is used in industrial manufacturing.",
    "Machine learning can predict equipment failures."
]

query = "How can machines predict engineering failures?"

doc_embeddings = model.encode(documents)
query_embedding = model.encode([query])

scores = cosine_similarity(query_embedding, doc_embeddings)[0]

print("Query:", query)
print("\nRelevant Documents:")

for i in scores.argsort()[::-1]:
    print("\nSimilarity:", round(scores[i], 4))
    print(documents[i])