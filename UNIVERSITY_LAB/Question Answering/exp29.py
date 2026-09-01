from transformers import pipeline

qa = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)

context = """
Artificial Intelligence is a branch of computer science that enables
machines to perform tasks that normally require human intelligence.
Machine learning is a part of AI that learns patterns from data.
"""

question = input("Enter your question: ")

result = qa(
    question=question,
    context=context
)

print("\nAnswer:")
print(result["answer"])