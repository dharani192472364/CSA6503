from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

questions = [
    "What is Python?",
    "What is a database?",
    "What is computer networking?",
    "What is artificial intelligence?",
    "What is machine learning?"
]

answers = [
    "Python is a high-level programming language.",
    "A database is used to store and manage data.",
    "Computer networking connects devices for communication.",
    "Artificial intelligence enables machines to perform intelligent tasks.",
    "Machine learning allows computers to learn from data."
]

vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(questions)

print("Engineering Support Chatbot")
print("Type exit to stop.")

while True:

    user = input("\nStudent: ")

    if user.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    user_vector = vectorizer.transform([user])

    scores = cosine_similarity(
        user_vector,
        vectors
    )[0]

    best = scores.argmax()

    if scores[best] < 0.2:
        print("Chatbot: Sorry, I don't know the answer.")
    else:
        print("Chatbot:", answers[best])