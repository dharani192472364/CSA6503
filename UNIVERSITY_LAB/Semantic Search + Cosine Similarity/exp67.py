from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "Cloud computing provides computing resources through the Internet.",
    "Artificial intelligence enables machines to perform intelligent tasks.",
    "Cybersecurity protects computer systems from attacks.",
    "Computer vision allows computers to understand images.",
    "Natural language processing works with human language."
]

query = "How can computers understand pictures?"

doc_vectors = model.encode(documents)
query_vector = model.encode([query])

scores = cosine_similarity(
    query_vector,
    doc_vectors
)[0]

print("Search Query:", query)

for index in scores.argsort()[::-1]:
    print(
        "\nScore:",
        round(scores[index], 4),
        "\nDocument:",
        documents[index]
    )