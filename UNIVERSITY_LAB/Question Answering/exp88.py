from transformers import pipeline

qa = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)

document = input("Enter document content:\n")

question = input("\nEnter your question: ")

result = qa(
    question=question,
    context=document
)

print("\nAnswer:")
print(result["answer"])