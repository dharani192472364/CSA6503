from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

documents = [
    "Python is used for artificial intelligence.",
    "Machine learning learns patterns from data.",
    "FAISS is a vector database used for similarity search.",
    "RAG retrieves relevant documents before generating answers."
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_texts(
    documents,
    embeddings
)

history = []

print("Context-Aware Chatbot")
print("Type exit to stop.")

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    # Add previous question to current query
    context = " ".join(history)

    combined_query = context + " " + question

    results = db.similarity_search(
        combined_query,
        k=2
    )

    print("\nBot:")

    for result in results:
        print(result.page_content)

    history.append(question)