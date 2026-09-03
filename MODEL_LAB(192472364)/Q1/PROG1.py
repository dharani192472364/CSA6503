import os
from pypdf import PdfReader
from transformers import BertTokenizer

# Get the folder where PROG1.py is located
folder = os.path.dirname(os.path.abspath(__file__))

# Resume path
resume_file = os.path.join(folder, "resume.pdf")

# Read resume
reader = PdfReader(resume_file)

resume_text = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        resume_text += text + "\n"

# Load BERT tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Tokenize resume
tokens = tokenizer.tokenize(resume_text)

# Convert tokens to IDs
token_ids = tokenizer.convert_tokens_to_ids(tokens)

# Display
print("\n===== RESUME TEXT =====")
print(resume_text)

print("\n===== BERT TOKENS =====")
print(tokens)

print("\n===== TOKEN IDs =====")
print(token_ids)

print("\n===== NUMBER OF TOKENS =====")
print(len(tokens))