from pathlib import Path
import requests
import re

# ============================================================
# KNOWLEDGEDESK - Q9 MULTI-STEP AI AGENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_FOLDER = BASE_DIR / "documents"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:latest"


# ============================================================
# STEP 1 - LOAD DOCUMENTS
# ============================================================

def load_documents():
    documents = []

    for file_path in DOCUMENTS_FOLDER.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "filename": file_path.name,
            "text": text
        })

    return documents


# ============================================================
# STEP 2 - SIMPLE KEYWORD RETRIEVAL
# ============================================================

def retrieve_documents(question, documents, top_k=3):

    question_words = set(
        re.findall(r"\b[a-zA-Z]{3,}\b", question.lower())
    )

    scores = []

    for doc in documents:

        doc_words = set(
            re.findall(r"\b[a-zA-Z]{3,}\b", doc["text"].lower())
        )

        overlap = question_words.intersection(doc_words)

        score = len(overlap)

        scores.append({
            "filename": doc["filename"],
            "text": doc["text"],
            "score": score
        })

    scores.sort(key=lambda x: x["score"], reverse=True)

    return scores[:top_k]


# ============================================================
# STEP 3 - CHECK WHETHER EVIDENCE EXISTS
# ============================================================

def check_evidence(retrieved_documents):

    if not retrieved_documents:
        return False

    best_score = retrieved_documents[0]["score"]

    return best_score >= 2


# ============================================================
# STEP 4 - GENERATE GROUNDED ANSWER
# ============================================================

def generate_answer(question, retrieved_documents):

    context_parts = []

    for doc in retrieved_documents:

        context_parts.append(
            f"DOCUMENT: {doc['filename']}\n"
            f"{doc['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are KnowledgeDesk, an enterprise knowledge assistant.

Answer the user's question ONLY using the supplied documents.

Rules:
1. Do not invent information.
2. If the documents do not contain sufficient evidence, say:
   "I’m sorry, but I cannot answer this question from the available KnowledgeDesk documents."
3. Give a concise answer.
4. Include the document filename as the source.
5. Preserve important factual details.

USER QUESTION:
{question}

RETRIEVED DOCUMENTS:
{context}

ANSWER:
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 200
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"].strip()


# ============================================================
# STEP 5 - COMPLETE AGENT WORKFLOW
# ============================================================

def run_agent(question):

    print("\n" + "=" * 70)
    print("KNOWLEDGEDESK MULTI-STEP AI AGENT")
    print("=" * 70)

    # Step 1
    print("\n[STEP 1] Loading KnowledgeDesk documents...")
    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    # Step 2
    print("\n[STEP 2] Retrieving relevant documents...")

    retrieved = retrieve_documents(
        question,
        documents,
        top_k=3
    )

    for i, doc in enumerate(retrieved, start=1):

        print(
            f"{i}. {doc['filename']} "
            f"(keyword score: {doc['score']})"
        )

    # Step 3
    print("\n[STEP 3] Checking evidence...")

    evidence_available = check_evidence(retrieved)

    if evidence_available:
        print("Evidence sufficient: YES")
    else:
        print("Evidence sufficient: NO")

    # Step 4
    print("\n[STEP 4] Generating grounded answer...")

    if not evidence_available:

        answer = (
            "I’m sorry, but I cannot answer this question "
            "from the available KnowledgeDesk documents."
        )

    else:

        answer = generate_answer(
            question,
            retrieved
        )

    # Step 5
    print("\n[STEP 5] FINAL ANSWER")
    print("-" * 70)
    print(answer)
    print("-" * 70)

    print("\nAgent execution completed.")


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    question = input(
        "\nEnter your KnowledgeDesk question: "
    )

    run_agent(question)