from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Knowledge base
documents = [
    "Python is a programming language used for software development and AI.",
    "Computer networks allow computers to communicate with each other.",
    "SQL is used to store and retrieve data from databases.",
    "Artificial Intelligence enables machines to perform intelligent tasks.",
    "Robotics combines software, electronics and mechanical engineering."
]

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Vector database
vector_db = FAISS.from_texts(
    documents,
    embeddings
)

print("Engineering Chatbot")
print("Type exit to stop.")

while True:

    question = input("\nStudent: ")

    if question.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    results = vector_db.similarity_search(
        question,
        k=2
    )

    print("\nRelevant Information:")

    for result in results:
        print("-", result.page_content)