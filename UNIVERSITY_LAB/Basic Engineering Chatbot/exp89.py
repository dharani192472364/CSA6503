from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

topics = [
    "college facilities",
    "engineering laboratories",
    "library services",
    "examination information",
    "engineering departments",
    "academic activities"
]

responses = [
    "The college provides classrooms, laboratories, library and sports facilities.",
    "Laboratories contain equipment required for engineering practical sessions.",
    "The library provides books, journals and digital learning resources.",
    "The examination cell manages examination schedules and results.",
    "The college has different engineering departments for various specializations.",
    "Academic activities include lectures, seminars, workshops and practical sessions."
]

vectorizer = TfidfVectorizer()
topic_vectors = vectorizer.fit_transform(topics)

print("Engineering College Helpdesk")

question = input("Enter your query: ")

query_vector = vectorizer.transform([question])

scores = cosine_similarity(
    query_vector,
    topic_vectors
)[0]

best = scores.argmax()

print("\nAnswer:")
print(responses[best])