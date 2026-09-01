import os
import ollama
import chromadb

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


# -----------------------------------------
# 1. Load embedding model
# -----------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# -----------------------------------------
# 2. Create ChromaDB
# -----------------------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="engineering_documents"
)


# -----------------------------------------
# 3. Read PDF documents
# -----------------------------------------

documents_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "documents"
)

chunks = []
ids = []

chunk_number = 0

for filename in os.listdir(documents_folder):

    if filename.lower().endswith(".pdf"):

        filepath = os.path.join(
            documents_folder,
            filename
        )

        print("\nReading:", filename)

        reader = PdfReader(filepath)

        for page_number, page in enumerate(reader.pages):

            text = page.extract_text()

            if not text:
                continue

            # Remove unnecessary spaces
            text = " ".join(text.split())

            # Split text into chunks
            words = text.split()

            chunk_size = 150

            for i in range(
                0,
                len(words),
                chunk_size
            ):

                chunk = " ".join(
                    words[i:i + chunk_size]
                )

                if chunk.strip():

                    chunks.append(chunk)

                    ids.append(
                        f"{filename}_page_{page_number}_chunk_{chunk_number}"
                    )

                    chunk_number += 1


print("\nTotal chunks created:", len(chunks))


# -----------------------------------------
# 4. Generate embeddings
# -----------------------------------------

print("\nGenerating embeddings...")

embeddings = embedding_model.encode(
    chunks
).tolist()

print("Embedding dimension:", len(embeddings[0]))


# -----------------------------------------
# 5. Store in ChromaDB
# -----------------------------------------

existing_data = collection.get()

if len(existing_data["ids"]) == 0:

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    print("Documents stored in ChromaDB.")

else:

    print("Documents already exist in ChromaDB.")


# -----------------------------------------
# 6. Get technical question
# -----------------------------------------

question = input(
    "\nEnter your technical question: "
)


# -----------------------------------------
# 7. Create embedding for question
# -----------------------------------------

question_embedding = embedding_model.encode(
    [question]
).tolist()


# -----------------------------------------
# 8. Retrieve relevant chunks
# -----------------------------------------

results = collection.query(
    query_embeddings=question_embedding,
    n_results=3
)

retrieved_documents = results["documents"][0]


for i, document in enumerate(
    retrieved_documents,
    start=1
):

    print(f"\n--- Retrieved Chunk {i} ---")
    print(document)


# -----------------------------------------
# 10. Create context
# -----------------------------------------

context = "\n\n".join(
    retrieved_documents
)


# -----------------------------------------
# 11. Create RAG prompt
# -----------------------------------------

prompt = f"""
You are an engineering question-answering assistant.

Answer the user's technical question using ONLY
the information provided in the context.

Do not invent information.

If the answer is not available in the context,
say:
"The answer is not available in the provided documents."

CONTEXT:
{context}

QUESTION:
{question}

Give a clear and concise technical answer.
"""


# -----------------------------------------
# 12. Send prompt to Ollama
# -----------------------------------------

print("\nGenerating answer using Ollama...")

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a reliable engineering assistant. "
                "Use only the supplied document context."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)


# -----------------------------------------
# 13. Display final answer
# -----------------------------------------

answer = response["message"]["content"]

print("\nFINAL ANSWER")
print("=" * 50)
print(answer)