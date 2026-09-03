from pathlib import Path
import requests
import re


# ============================================================
# KNOWLEDGEDESK - Q12 INTELLIGENT ENTERPRISE ASSISTANT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_FOLDER = BASE_DIR / "documents"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:latest"


# ============================================================
# STEP 1 - LOAD KNOWLEDGE BASE
# ============================================================

def load_documents():

    documents = []

    for file_path in DOCUMENTS_FOLDER.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append({
            "filename": file_path.name,
            "text": text
        })

    return documents


# ============================================================
# STEP 2 - RETRIEVE RELEVANT DOCUMENTS
# ============================================================

def retrieve_documents(question, documents, top_k=3):

    question_words = set(
        re.findall(
            r"\b[a-zA-Z]{3,}\b",
            question.lower()
        )
    )

    results = []

    for document in documents:

        document_words = set(
            re.findall(
                r"\b[a-zA-Z]{3,}\b",
                document["text"].lower()
            )
        )

        matching_words = question_words.intersection(
            document_words
        )

        score = len(matching_words)

        results.append({
            "filename": document["filename"],
            "text": document["text"],
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


# ============================================================
# STEP 3 - CHECK EVIDENCE
# ============================================================

def evidence_available(results):

    if not results:
        return False

    return results[0]["score"] >= 2


# ============================================================
# STEP 4 - GENERATE GROUNDED ANSWER
# ============================================================

def generate_answer(question, results):

    # Use the highest-ranked document as the primary evidence
    best_result = results[0]

    context = (
        f"DOCUMENT: {best_result['filename']}\n"
        f"{best_result['text']}\n"
    )

    prompt = f"""
You are KnowledgeDesk, an intelligent enterprise knowledge assistant.

Answer the user's question ONLY using the supplied document.

IMPORTANT RULES:

1. Use only the supplied document.
2. Do not use outside knowledge.
3. Do not invent information.
4. Identify the answer directly from the document.
5. Give a concise and clear answer.
6. Include the source document name.
7. If the answer is not present in the supplied document, respond exactly:

I'm sorry, but I cannot answer this question from the available KnowledgeDesk documents.

USER QUESTION:
{question}

SUPPLIED DOCUMENT:
{context}

FINAL ANSWER:
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 250
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
# STEP 5 - MAIN APPLICATION
# ============================================================

def main():

    print("=" * 75)
    print("KNOWLEDGEDESK - INTELLIGENT ENTERPRISE ASSISTANT")
    print("=" * 75)

    # --------------------------------------------------------
    # LOAD DOCUMENTS
    # --------------------------------------------------------

    print("\nLoading KnowledgeDesk knowledge base...")

    documents = load_documents()

    print(
        f"Documents available: {len(documents)}"
    )

    # --------------------------------------------------------
    # EXAMPLE QUESTIONS
    # --------------------------------------------------------

    print("\nExample questions:")

    print(
        "1. What is the annual leave entitlement?"
    )

    print(
        "2. What should an employee do during a fire emergency?"
    )

    print(
        "3. What are the password requirements?"
    )

    print(
        "4. What is the procedure for a chemical spill?"
    )

    print("\n" + "-" * 75)

    # --------------------------------------------------------
    # USER QUESTION
    # --------------------------------------------------------

    question = input(
        "Enter your KnowledgeDesk question: "
    )

    if not question.strip():

        print(
            "Please enter a question."
        )

        return

    # --------------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------------

    print(
        "\n[1] Searching enterprise knowledge base..."
    )

    results = retrieve_documents(
        question,
        documents,
        top_k=3
    )

    print("\nRetrieved documents:")

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"{index}. "
            f"{result['filename']} "
            f"(score: {result['score']})"
        )

    # --------------------------------------------------------
    # EVIDENCE CHECK
    # --------------------------------------------------------

    print(
        "\n[2] Checking evidence..."
    )

    if not evidence_available(results):

        print(
            "Evidence sufficient: NO"
        )

        print(
            "\nFINAL ANSWER:"
        )

        print(
            "I'm sorry, but I cannot answer this question "
            "from the available KnowledgeDesk documents."
        )

        return

    print(
        "Evidence sufficient: YES"
    )

    # --------------------------------------------------------
    # LLM GENERATION
    # --------------------------------------------------------

    print(
        "\n[3] Generating grounded response using Llama 3.2..."
    )

    try:

        answer = generate_answer(
            question,
            results
        )

    except requests.exceptions.RequestException as error:

        print(
            "\nERROR: Could not connect to Ollama."
        )

        print(
            f"Details: {error}"
        )

        return

    # --------------------------------------------------------
    # FINAL ANSWER
    # --------------------------------------------------------

    print(
        "\n[4] FINAL ANSWER"
    )

    print("-" * 75)

    print(answer)

    print("-" * 75)

    # --------------------------------------------------------
    # SOURCE
    # --------------------------------------------------------

    print(
        "\nPrimary source:"
    )

    print(
        results[0]["filename"]
    )

    print(
        "\nKnowledgeDesk intelligent application completed."
    )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()