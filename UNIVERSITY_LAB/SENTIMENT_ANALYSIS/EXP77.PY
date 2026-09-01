from transformers import pipeline

sentiment_analyzer = pipeline(
    task="sentiment-analysis"
)

feedback = [
    "The teaching and campus facilities are excellent.",
    "The canteen service is very disappointing.",
    "The department provides good academic support."
]

for item in feedback:
    prediction = sentiment_analyzer(item)

    label = prediction[0]["label"]
    score = prediction[0]["score"]

    print("Student Feedback:", item)
    print("Predicted Sentiment:", label)
    print("Confidence Score:", f"{score:.4f}")
    print("=" * 50)