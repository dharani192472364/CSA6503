from transformers import pipeline

model = pipeline("sentiment-analysis")

reviews = [
    "The campus is very clean and beautiful.",
    "The hostel facilities are not good.",
    "The library is excellent and spacious."
]

for review in reviews:
    output = model(review)[0]

    print("Review:", review)
    print("Result:", output["label"])
    print("Score:", round(output["score"], 3))
    print()