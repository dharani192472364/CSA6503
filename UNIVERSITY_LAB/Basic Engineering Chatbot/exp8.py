from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = {
    "admission": "Admissions are handled by the college admission office.",
    "attendance": "Students should maintain the required attendance percentage.",
    "examination": "Examination schedules are published by the examination cell.",
    "library": "The library provides textbooks, journals and digital resources.",
    "laboratory": "Engineering laboratories provide equipment for practical experiments."
}

keys = list(data.keys())

vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(keys)

print("College Student Assistant")
print("Type exit to stop.")

while True:

    query = input("\nStudent: ")

    if query.lower() == "exit":
        break

    q_vector = vectorizer.transform([query])

    similarity = cosine_similarity(
        q_vector,
        matrix
    )[0]

    best = similarity.argmax()

    print("Assistant:", data[keys[best]])