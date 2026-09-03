# ============================================================
# KNOWLEDGEDESK - Q12 STREAMLIT INTELLIGENT ASSISTANT APP
# app.py
# ============================================================

import streamlit as st
from pathlib import Path
import requests
import re
import csv
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_FOLDER = BASE_DIR / "documents"
FEEDBACK_FILE = BASE_DIR / "feedback_log.csv"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:latest"

REFUSAL_MESSAGE = (
    "I'm sorry, but I cannot answer this question "
    "from the available KnowledgeDesk documents."
)


# ============================================================
# STEP 1 - LOAD KNOWLEDGE BASE (reused from Q9/Q12)
# ============================================================

@st.cache_data
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
# STEP 2 - RETRIEVE RELEVANT DOCUMENTS (reused)
# ============================================================

def retrieve_documents(question, documents, top_k=3):
    question_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", question.lower()))

    results = []
    for document in documents:
        document_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", document["text"].lower()))
        matching_words = question_words.intersection(document_words)
        score = len(matching_words)
        results.append({
            "filename": document["filename"],
            "text": document["text"],
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


# ============================================================
# STEP 3 - EVIDENCE CHECK (reused)
# ============================================================

def evidence_available(results):
    if not results:
        return False
    return results[0]["score"] >= 2


# ============================================================
# STEP 4 - ROUTING RULE (plain RAG vs agent, from Q9 design)
# ============================================================

def route_query(question):
    multi_step_keywords = ["compare", "raise a ticket", "then", "and also", "difference between"]
    q_lower = question.lower()
    if any(keyword in q_lower for keyword in multi_step_keywords):
        return "AGENT"
    return "RAG"


# ============================================================
# STEP 5 - GENERATE GROUNDED ANSWER (reused from Q12_APP.py)
# ============================================================

def generate_answer(question, results):
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

{REFUSAL_MESSAGE}

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

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()["response"].strip()


# ============================================================
# FEEDBACK LOGGING
# ============================================================

def log_feedback(question, answer, source, feedback):
    file_exists = FEEDBACK_FILE.exists()

    with open(FEEDBACK_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "question", "answer", "source", "feedback"])
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            question,
            answer,
            source,
            feedback
        ])


# ============================================================
# STREAMLIT UI
# ============================================================

st.set_page_config(page_title="KnowledgeDesk", layout="wide")

st.title("KnowledgeDesk – Enterprise Knowledge Assistant")
st.caption("This assistant is powered by AI (Llama 3.2 via Ollama) and only answers from retrieved KnowledgeDesk documents.")

documents = load_documents()

with st.sidebar:
    st.header("Pipeline Details")
    st.write(f"Documents loaded: **{len(documents)}**")
    st.write("---")

question = st.text_input("Enter your KnowledgeDesk question:")

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None
    st.session_state.last_question = None
    st.session_state.last_source = None

if st.button("Ask") and question.strip():

    route = route_query(question)

    with st.spinner("Retrieving relevant documents..."):
        results = retrieve_documents(question, documents, top_k=3)

    has_evidence = evidence_available(results)

    with st.sidebar:
        st.subheader("Route Taken")
        st.write(f"**{route}**" + (" (multi-step)" if route == "AGENT" else " (plain RAG)"))

        st.subheader("Retrieved Documents")
        for i, r in enumerate(results, start=1):
            st.write(f"{i}. `{r['filename']}` — score: {r['score']}")

        st.subheader("Evidence Check")
        st.write("Sufficient: **YES**" if has_evidence else "Sufficient: **NO**")

    if not has_evidence:
        answer = REFUSAL_MESSAGE
        source = "N/A"
    else:
        with st.spinner("Generating grounded answer..."):
            try:
                answer = generate_answer(question, results)
                source = results[0]["filename"]
            except requests.exceptions.RequestException as e:
                answer = f"ERROR: Could not connect to Ollama. Details: {e}"
                source = "N/A"

    st.session_state.last_answer = answer
    st.session_state.last_question = question
    st.session_state.last_source = source

if st.session_state.last_answer:
    st.subheader("Answer")
    st.write(st.session_state.last_answer)

    if st.session_state.last_source != "N/A":
        st.markdown(f"**Source:** {st.session_state.last_source}")

    st.write("Was this answer helpful?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Yes"):
            log_feedback(
                st.session_state.last_question,
                st.session_state.last_answer,
                st.session_state.last_source,
                "positive"
            )
            st.success("Feedback recorded.")

    with col2:
        if st.button("👎 No"):
            log_feedback(
                st.session_state.last_question,
                st.session_state.last_answer,
                st.session_state.last_source,
                "negative"
            )
            st.success("Feedback recorded.")