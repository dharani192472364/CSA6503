from pypdf import PdfReader

def load_pdf(path):
    reader = PdfReader(path)
    return "\n".join(
        page.extract_text() for page in reader.pages
    )

text = load_pdf("LAB PROGRAMS(192472364)/UNIT 3/cloud.pdf")
print(f"Loaded {len(text)} characters")

def chunk_text(text, size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap

    return chunks

chunks = chunk_text(text)
print(f"Created {len(chunks)} chunks")

import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./db")
col = client.get_or_create_collection("curriculum")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

if col.count() == 0:
    embeddings = embedder.encode(chunks).tolist()

    col.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {
                "source": "cloud.pdf",
                "chunk": i
            }
            for i in range(len(chunks))
        ],
        ids=[f"c{i}" for i in range(len(chunks))]
    )

print(f"Vector DB has {col.count()} chunks")

def retrieve(question, k=3):
    query_embedding = embedder.encode([question]).tolist()

    res = col.query(
        query_embeddings=query_embedding,
        n_results=k
    )

    return res["documents"][0], res["metadatas"][0]

PROMPT = """
You are an AI assistant.

Answer ONLY from the context below.
Do not use outside knowledge.
If the answer is not found in the context, reply exactly:
"I don't know."

Always cite the chunk number after every fact, like [c4].

Context:
{context}

Question:
{question}

Answer:
"""

def build_prompt(question):
    docs, metas = retrieve(question)

    context = "\n".join(
        [f"[c{m['chunk']}] {d}"
         for d, m in zip(docs, metas)]
    )

    return PROMPT.format( context=context,question=question)

from openai import OpenAI

# Connect to Ollama
llm = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"   # Can be any string
)

def answer(question):
    prompt = build_prompt(question)

    resp = llm.chat.completions.create(
        model="llama3.2",   # Your Ollama model
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return resp.choices[0].message.content
if __name__ == "__main__":
    print("Curriculum assistant ready. Type 'quit' to exit.")

    while True:
        q = input("\nAsk: ")

        if q.strip().lower() == "quit":
            break

        print(answer(q))