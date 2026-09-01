import os
import ollama
import chromadb

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


# 1. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# 2. Create ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="technical_troubleshooting"
)


# 3. Read technical PDF documents
folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "technical_docs"
)

chunks = []
ids = []

counter = 0

for filename in os.listdir(folder):

    if filename.lower().endswith(".pdf"):

        filepath = os.path.join(folder, filename)

        print("\nReading:", filename)

        reader = PdfReader(filepath)

        for page_number, page in enumerate(reader.pages):

            text = page.extract_text()

            if not text:
                continue

            text = " ".join(text.split())

            words = text.split()

            chunk_size = 150

            for i in range(0, len(words), chunk_size):

                chunk = " ".join(
                    words[i:i + chunk_size]
                )

                if chunk.strip():

                    chunks.append(chunk)

                    ids.append(
                        f"{filename}_page_{page_number}_chunk_{counter}"
                    )

                    counter += 1


print("\nTotal chunks:", len(chunks))


# 4. Generate embeddings
print("\nGenerating embeddings...")

embeddings = model.encode(chunks).tolist()

print("Embedding dimension:", len(embeddings[0]))


# 5. Store documents in ChromaDB
existing = collection.get()

if len(existing["ids"]) == 0:

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    print("Documents stored in ChromaDB.")

else:

    print("Documents already stored.")


# 6. Get troubleshooting problem
problem = input(
    "\nDescribe the technical problem: "
)


# 7. Generate problem embedding
problem_embedding = model.encode(
    [problem]
).tolist()


# 8. Retrieve relevant information
results = collection.query(
    query_embeddings=problem_embedding,
    n_results=4
)

documents = results["documents"][0]


# 9. Display retrieved information
print("\nRETRIEVED INFORMATION")
print("=" * 50)

for i, document in enumerate(documents, start=1):

    print(f"\n--- Source {i} ---")
    print(document)


# 10. Create context
context = "\n\n".join(documents)


# 11. Create troubleshooting prompt
prompt = f"""
You are an engineering troubleshooting assistant.

Use ONLY the technical information given in the context.

TECHNICAL PROBLEM:
{problem}

CONTEXT:
{context}

Provide a clear troubleshooting procedure.

Use the following format:

1. Problem Identification
2. Possible Causes
3. Step-by-Step Troubleshooting
4. Recommended Solution
5. Safety Precautions

Do not invent information.

If the required information is not available
in the context, clearly state:
"Required information is not available in
the provided documents."
"""


# 12. Send request to Ollama
print("\nGenerating troubleshooting recommendations...")

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a careful engineering "
                "troubleshooting assistant."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)


# 13. Display final answer
print("\n")
print("=" * 60)
print("ENGINEERING TROUBLESHOOTING RESULT")
print("=" * 60)

print(response["message"]["content"])