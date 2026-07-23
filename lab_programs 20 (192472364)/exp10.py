from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)

text = "Artificial Intelligence is very useful."

result = classifier(text)

print(result)