from transformers import BertTokenizer, pipeline

# Load BERT tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Student feedback sentences
feedback = [
    "The course was very useful and informative.",
    "The teaching was excellent and easy to understand.",
    "The laboratory sessions were difficult and confusing.",
    "The course was average and okay."
]

# Process each feedback sentence
for sentence in feedback:

    # Tokenization
    tokens = tokenizer.tokenize(sentence)
    token_ids = tokenizer.convert_tokens_to_ids(tokens)

    # Sentiment classification
    sentiment = sentiment_analyzer(sentence)[0]

    print("\n----------------------------------------")
    print("Feedback:", sentence)
    print("Sentiment:", sentiment["label"])
    print("Confidence:", round(sentiment["score"], 4))
    print("Tokens:", tokens)
    print("Token IDs:", token_ids)