from transformers import pipeline

classifier = pipeline("sentiment-analysis")

comments = [
    "The college provides excellent facilities.",
    "The classroom infrastructure is poor.",
    "I am happy with the laboratory facilities."
]

results = classifier(comments)

for text, result in zip(comments, results):
    print(f"Text: {text}")
    print(f"Sentiment: {result['label']}")
    print(f"Confidence: {result['score']:.2f}")
    print("-" * 40)