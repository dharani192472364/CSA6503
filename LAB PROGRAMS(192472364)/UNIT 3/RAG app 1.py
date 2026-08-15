import fitz
import numpy as np
from sentence_transformers import SentenceTransformer
import requests

# 1. Extract PDF Text
def extract_pdf_text(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text() + "\n"

    return text
# 2. Create Text Chunks
def create_chunks(text, chunk_size=500, overlap=100):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks



# ==============================
# 3. Load PDF
# ==============================

pdf_file = "LAB PROGRAMS(192472364)/UNIT 3/cloud.pdf"


print("Extracting PDF text...")

text = extract_pdf_text(pdf_file)


print("Characters extracted:",
      len(text))



print("\nCreating chunks...")

chunks = create_chunks(text)


print("Total chunks:",
      len(chunks))



# ==============================
# 4. Create Embeddings
# ==============================

print("\nLoading embedding model...")


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



print("Generating embeddings...")


chunk_embeddings = embedding_model.encode(
    chunks,
    show_progress_bar=True
)


chunk_embeddings = np.array(
    chunk_embeddings
)



print("Embedding shape:",
      chunk_embeddings.shape)
# 5. Vector Search
def search_chunks(query, top_k=3):

    query_embedding = embedding_model.encode(
        [query]
    )[0]


    dot_product = np.dot(
        chunk_embeddings,
        query_embedding
    )


    chunk_norm = np.linalg.norm(
        chunk_embeddings,
        axis=1
    )


    query_norm = np.linalg.norm(
        query_embedding
    )


    similarity = (
        dot_product /
        (chunk_norm * query_norm)
    )


    top_indices = np.argsort(
        similarity
    )[::-1][:top_k]


    results = []


    for index in top_indices:

        results.append(
            (
                index,
                similarity[index],
                chunks[index]
            )
        )


    return results



# ==============================
# 6. Ollama API Generation
# ==============================


OLLAMA_API = "http://localhost:11434/api/generate"



def ask_ollama(question, top_k=3):


    # Retrieve context

    results = search_chunks(
        question,
        top_k
    )


    context = "\n\n".join(
        [
            chunk
            for _,_,chunk in results
        ]
    )



    prompt = f"""

You are an AI assistant.

Use the context below to answer.

Context:
{context}


Question:
{question}


Answer:

"""



    payload = {

        "model": "llama3.2:latest",

        "prompt": prompt,

        "stream": False

    }



    response = requests.post(
        OLLAMA_API,
        json=payload
    )



    if response.status_code == 200:

        data = response.json()

        return data["response"]

    else:

        return response.text




# ==============================
# 7. Test Query
# ==============================


question = "What is the title of capstone project?"


print("\nQuestion:")
print(question)


print("\nGenerating answer...")


answer = ask_ollama(question)



print("\n========================")

print("FINAL ANSWER")

print("========================")


print(answer)