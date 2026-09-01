from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

knowledge = [
    "Artificial Intelligence is used in engineering automation.",
    "Machine learning is a branch of Artificial Intelligence.",
    "Deep learning uses neural networks.",
    "Computer vision processes images and videos."
]

model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_texts(
    knowledge,
    model
)

conversation = ""

print("Context-Aware Engineering Assistant")

while True:

    user = input("\nStudent: ")

    if user.lower() == "exit":
        break

    conversation += " " + user

    results = db.similarity_search(
        conversation,
        k=2
    )

    print("\nAssistant:")

    for result in results:
        print(result.page_content)