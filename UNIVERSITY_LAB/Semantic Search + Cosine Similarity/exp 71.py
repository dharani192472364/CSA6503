from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

library = [
    "Digital electronics deals with digital signals and logic circuits.",
    "Operating systems manage computer hardware and software.",
    "Machine learning allows computers to learn from data.",
    "Computer networks provide communication between devices.",
    "Structural engineering deals with the design of buildings."
]

question = "How do computers learn from information?"

library_embeddings = model.encode(library)
question_embedding = model.encode([question])

similarities = cosine_similarity(
    question_embedding,
    library_embeddings
)[0]

top = similarities.argsort()[::-1][:3]

print("Question:", question)
print("\nTop 3 Documents:")

for position in top:
    print("\nSimilarity:", round(similarities[position], 4))
    print(library[position])