from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM


# ============================================================
# 1. LOAD PDF
# ============================================================

def load_pdf(path):
    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"

    return text


text = load_pdf("LAB PROGRAMS(192472364)/UNIT 3/cloud.pdf")

print(f"Loaded {len(text)} characters")


# ============================================================
# 2. SPLIT TEXT INTO CHUNKS
# ============================================================

def chunk_text(text, size=500, overlap=50):

    chunks = []
    start = 0

    while start < len(text):

        chunk = text[start:start + size]

        if chunk.strip():
            chunks.append(chunk)

        start += size - overlap

    return chunks


chunks = chunk_text(text)

print(f"Created {len(chunks)} chunks")


# ============================================================
# 3. CREATE EMBEDDINGS
# ============================================================

embedder = SentenceTransformer("all-MiniLM-L6-v2")


# ============================================================
# 4. CREATE CHROMADB VECTOR DATABASE
# ============================================================

client = chromadb.PersistentClient(path="./db")

collection = client.get_or_create_collection(
    name="curriculum"
)


# ============================================================
# 5. STORE EMBEDDINGS IN CHROMADB
# ============================================================

if collection.count() == 0:

    embeddings = embedder.encode(
        chunks,
        show_progress_bar=True
    ).tolist()

    collection.add(

        documents=chunks,

        embeddings=embeddings,

        metadatas=[
            {
                "source": "cloud.pdf",
                "chunk": i
            }
            for i in range(len(chunks))
        ],

        ids=[
            f"c{i}"
            for i in range(len(chunks))
        ]
    )

    print("Embeddings stored in ChromaDB.")

else:

    print("Existing vector database found.")


print(
    f"Vector DB contains {collection.count()} chunks"
)


# ============================================================
# 6. SEMANTIC SIMILARITY SEARCH
# ============================================================

def retrieve(question, k=3):

    query_embedding = embedder.encode(
        [question]
    ).tolist()

    results = collection.query(

        query_embeddings=query_embedding,

        n_results=k
    )

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    return documents, metadatas


# ============================================================
# 7. CONVERT RETRIEVED TEXT TO LANGCHAIN DOCUMENTS
# ============================================================

def get_documents(question):

    documents, metadatas = retrieve(question)

    langchain_documents = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        langchain_documents.append(

            Document(
                page_content=document,
                metadata=metadata
            )
        )

    return langchain_documents


# ============================================================
# 8. LANGCHAIN PROMPT
# ============================================================

prompt = PromptTemplate(

    input_variables=[
        "context",
        "question"
    ],

    template="""
You are a document-based AI assistant.

Answer ONLY using the information provided
in the context.

Do not use outside knowledge.

If the answer is not available in the context,
reply exactly:

I don't know.

Always mention the source chunk after the
relevant information using the format [c0],
[c1], [c2], etc.

Context:
{context}

Question:
{question}

Answer:
"""
)


# ============================================================
# 9. OLLAMA LLM
# ============================================================

llm = OllamaLLM(
    model="llama3.2",
    temperature=0.2
)


# ============================================================
# 10. RAG FUNCTION
# ============================================================

def answer(question):

    docs = get_documents(question)

    context = ""

    for doc in docs:

        chunk_number = doc.metadata["chunk"]

        context += (
            f"[c{chunk_number}] "
            f"{doc.page_content}\n\n"
        )

    formatted_prompt = prompt.format(

        context=context,

        question=question
    )

    response = llm.invoke(
        formatted_prompt
    )

    return response


# ============================================================
# 11. CHATBOT
# ============================================================

if __name__ == "__main__":

    print("\n===================================")
    print("   DOCUMENT RAG AI ASSISTANT")
    print("===================================")

    print("Document: cloud.pdf")
    print("Vector Database: ChromaDB")
    print("Embedding Model: all-MiniLM-L6-v2")
    print("LLM: Ollama llama3.2")
    print("Framework: LangChain")

    print("\nAssistant ready!")
    print("Type 'quit' to exit.")

    while True:

        question = input("\nAsk: ")

        if question.strip().lower() == "quit":
            print("Goodbye!")
            break

        if not question.strip():
            continue

        print("\nAnswer:")

        try:

            result = answer(question)

            print(result)

        except Exception as e:

            print("Error:", e)