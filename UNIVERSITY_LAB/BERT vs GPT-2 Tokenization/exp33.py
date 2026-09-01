from transformers import BertTokenizer, GPT2Tokenizer

# Load tokenizers
bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Same engineering sentence
sentence = "Artificial intelligence improves engineering design."

# BERT tokenization
bert_tokens = bert_tokenizer.tokenize(sentence)
bert_ids = bert_tokenizer.convert_tokens_to_ids(bert_tokens)

# GPT-2 tokenization
gpt2_tokens = gpt2_tokenizer.tokenize(sentence)
gpt2_ids = gpt2_tokenizer.convert_tokens_to_ids(gpt2_tokens)

print("====================================")
print("       BERT vs GPT-2 TOKENIZATION")
print("====================================")

print("\nOriginal Sentence:")
print(sentence)

print("\n----- BERT -----")
print("Tokens:")
print(bert_tokens)

print("Token IDs:")
print(bert_ids)

print("\n----- GPT-2 -----")
print("Tokens:")
print(gpt2_tokens)

print("Token IDs:")
print(gpt2_ids)

print("\n----- COMPARISON -----")
print("BERT uses WordPiece tokenization.")
print("GPT-2 uses Byte-Level BPE tokenization.")
print("Therefore, the same sentence can produce")
print("different tokens and token IDs.")