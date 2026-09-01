from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

documents = [
    "Engineering laboratories contain equipment for practical experiments.",
    "Students must follow safety rules inside the laboratory.",
    "The engineering library provides textbooks and journals.",
    "Students can borrow books using their college ID card.",
    "Technical departments conduct seminars and workshops."
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_texts(
    documents,
    embeddings
)

print("Domain-Specific Engineering Chatbot")

question = input("Ask your question: ")

results = db.similarity_search(
    question,
    k=2
)

print("\nAnswer:")

for result in results:
    print(result.page_content)