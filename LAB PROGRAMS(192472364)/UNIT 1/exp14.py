from transformers import pipeline

qa = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)

context = """
Artificial Intelligence enables machines to learn from data.
"""

question = "What enables machines to learn from data?"

answer = qa(question=question, context=context)

print(answer)