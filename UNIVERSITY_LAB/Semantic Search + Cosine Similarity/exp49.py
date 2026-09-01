from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

query1 = "Where can students borrow engineering books?"
query2 = "How can learners get books from the engineering library?"

embedding1 = model.encode([query1])
embedding2 = model.encode([query2])

score = cosine_similarity(
    embedding1,
    embedding2
)[0][0]

print("Query 1:", query1)
print("Query 2:", query2)

print("\nCosine Similarity:", round(score, 4))

if score > 0.5:
    print("Result: Queries have similar meanings.")
else:
    print("Result: Queries have different meanings.")