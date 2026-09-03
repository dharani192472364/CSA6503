# ============================================================
# Q8 - RETRIEVAL EVALUATION
# KnowledgeDesk Enterprise Knowledge Assistant
# ============================================================

from pathlib import Path
import re
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi


# ============================================================
# SETTINGS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_FOLDER = BASE_DIR / "documents"

EMBEDDING_DIMENSION = 768
TOP_K = 5


# ============================================================
# EVALUATION QUESTIONS
# ============================================================

QUESTIONS = [
    {
        "question": "How many days of annual leave are employees with more than 3 years of service entitled to?",
        "source": "HR_Leave_Policy_2026.txt"
    },
    {
        "question": "What is the maternity leave entitlement?",
        "source": "HR_Maternity_Policy_2026.txt"
    },
    {
        "question": "How should employees submit travel expense claims?",
        "source": "HR_Travel_Policy_2026.txt"
    },
    {
        "question": "What are the password requirements?",
        "source": "IT_Password_Policy_2026.txt"
    },
    {
        "question": "How can employees access the company VPN remotely?",
        "source": "IT_VPN_Policy_2026.txt"
    },
    {
        "question": "When should an employee return a company laptop?",
        "source": "IT_Laptop_Policy_2026.txt"
    },
    {
        "question": "What is the quality inspection procedure?",
        "source": "QUALITY_SOP_Inspection.txt"
    },
    {
        "question": "How should critical defects be handled?",
        "source": "QUALITY_SOP_Defect.txt"
    },
    {
        "question": "What should an employee do during a fire emergency?",
        "source": "SAFETY_SOP_Fire.txt"
    },
    {
        "question": "What is the procedure for a chemical spill?",
        "source": "SAFETY_SOP_Chemical.txt"
    },
    {
        "question": "What percentage improvement was achieved in Project Alpha?",
        "source": "PROJECT_REPORT_Alpha.txt"
    },
    {
        "question": "How long should records be retained under the legal hold policy?",
        "source": "COMPLIANCE_Data_Retention.txt"
    }
]


# ============================================================
# LOAD DOCUMENTS
# ============================================================

def load_documents():

    documents = []

    for file_path in sorted(
        DOCUMENTS_FOLDER.glob("*.txt")
    ):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append({
            "filename": file_path.name,
            "text": text
        })

    return documents


# ============================================================
# CREATE OVERLAPPING CHUNKS
# ============================================================

def create_chunks(
    documents,
    chunk_size,
    overlap
):

    chunks = []

    for document in documents:

        words = document["text"].split()

        if not words:
            continue

        step = chunk_size - overlap

        if step <= 0:
            raise ValueError(
                "Chunk size must be greater than overlap."
            )

        start = 0

        while start < len(words):

            chunk_words = words[
                start:start + chunk_size
            ]

            if not chunk_words:
                break

            chunk_text = " ".join(
                chunk_words
            )

            chunks.append({
                "filename": document["filename"],
                "text": chunk_text,
                "chunk_id": len(chunks),
                "start_word": start,
                "end_word": start + len(chunk_words)
            })

            if start + chunk_size >= len(words):
                break

            start += step

    return chunks


# ============================================================
# BUILD 768-DIMENSION TF-IDF REPRESENTATION
# ============================================================

def build_tfidf(chunks):

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        max_features=EMBEDDING_DIMENSION
    )

    matrix = vectorizer.fit_transform(
        texts
    ).toarray()

    # Force exactly 768 dimensions
    if matrix.shape[1] < EMBEDDING_DIMENSION:

        padding = np.zeros(
            (
                matrix.shape[0],
                EMBEDDING_DIMENSION
                - matrix.shape[1]
            )
        )

        matrix = np.hstack(
            [matrix, padding]
        )

    elif matrix.shape[1] > EMBEDDING_DIMENSION:

        matrix = matrix[
            :,
            :EMBEDDING_DIMENSION
        ]

    # Normalize document vectors
    norms = np.linalg.norm(
        matrix,
        axis=1,
        keepdims=True
    )

    norms[norms == 0] = 1

    matrix = matrix / norms

    return vectorizer, matrix


# ============================================================
# DENSE RETRIEVAL
# ============================================================

def dense_search(
    question,
    vectorizer,
    matrix,
    chunks,
    top_k=5
):

    query_vector = vectorizer.transform(
        [question]
    ).toarray()

    # Normalize query
    norm = np.linalg.norm(
        query_vector
    )

    if norm != 0:

        query_vector = (
            query_vector / norm
        )

    # Make query exactly 768 dimensions
    if query_vector.shape[1] < EMBEDDING_DIMENSION:

        padding = np.zeros(
            (
                query_vector.shape[0],
                EMBEDDING_DIMENSION
                - query_vector.shape[1]
            )
        )

        query_vector = np.hstack(
            [
                query_vector,
                padding
            ]
        )

    elif query_vector.shape[1] > EMBEDDING_DIMENSION:

        query_vector = query_vector[
            :,
            :EMBEDDING_DIMENSION
        ]

    # Cosine similarity
    scores = np.dot(
        matrix,
        query_vector.T
    ).flatten()

    ranked_indices = np.argsort(
        scores
    )[::-1]

    results = []

    for index in ranked_indices[:top_k]:

        results.append({
            "chunk": chunks[index],
            "score": float(
                scores[index]
            )
        })

    return results


# ============================================================
# BM25
# ============================================================

def build_bm25(chunks):

    tokenized_documents = []

    for chunk in chunks:

        tokens = re.findall(
            r"\b\w+\b",
            chunk["text"].lower()
        )

        tokenized_documents.append(
            tokens
        )

    return BM25Okapi(
        tokenized_documents
    )


def bm25_search(
    question,
    bm25,
    chunks,
    top_k=5
):

    query_tokens = re.findall(
        r"\b\w+\b",
        question.lower()
    )

    scores = bm25.get_scores(
        query_tokens
    )

    ranked_indices = np.argsort(
        scores
    )[::-1]

    results = []

    for index in ranked_indices[:top_k]:

        results.append({
            "chunk": chunks[index],
            "score": float(
                scores[index]
            )
        })

    return results


# ============================================================
# HYBRID RETRIEVAL
# ============================================================

def hybrid_search(
    question,
    vectorizer,
    matrix,
    bm25,
    chunks,
    top_k=5
):

    dense_results = dense_search(
        question,
        vectorizer,
        matrix,
        chunks,
        top_k=len(chunks)
    )

    bm25_results = bm25_search(
        question,
        bm25,
        chunks,
        top_k=len(chunks)
    )

    # Reciprocal Rank Fusion
    fusion_scores = {}

    for rank, result in enumerate(
        dense_results,
        start=1
    ):

        chunk_id = result["chunk"]["chunk_id"]

        fusion_scores.setdefault(
            chunk_id,
            0
        )

        fusion_scores[chunk_id] += (
            1 / (60 + rank)
        )

    for rank, result in enumerate(
        bm25_results,
        start=1
    ):

        chunk_id = result["chunk"]["chunk_id"]

        fusion_scores.setdefault(
            chunk_id,
            0
        )

        fusion_scores[chunk_id] += (
            1 / (60 + rank)
        )

    ranked_ids = sorted(
        fusion_scores,
        key=fusion_scores.get,
        reverse=True
    )

    results = []

    for chunk_id in ranked_ids[:top_k]:

        results.append({
            "chunk": chunks[chunk_id],
            "score": fusion_scores[chunk_id]
        })

    return results


# ============================================================
# METRICS
# ============================================================

def precision_at_5(
    results,
    expected_source
):

    relevant = 0

    for result in results[:5]:

        if (
            result["chunk"]["filename"]
            == expected_source
        ):

            relevant += 1

    return relevant / 5


def recall_at_5(
    results,
    expected_source
):

    for result in results[:5]:

        if (
            result["chunk"]["filename"]
            == expected_source
        ):

            return 1.0

    return 0.0


def reciprocal_rank(
    results,
    expected_source
):

    for rank, result in enumerate(
        results,
        start=1
    ):

        if (
            result["chunk"]["filename"]
            == expected_source
        ):

            return 1 / rank

    return 0.0


# ============================================================
# EVALUATE ONE CONFIGURATION
# ============================================================

def evaluate_configuration(
    name,
    retrieval_type,
    chunk_size,
    overlap,
    documents
):

    print()
    print("=" * 70)

    print(name)

    print("=" * 70)

    print(
        "Chunk size       :",
        chunk_size,
        "words"
    )

    print(
        "Chunk overlap    :",
        overlap,
        "words"
    )

    print(
        "Retrieval method :",
        retrieval_type
    )

    # Create chunks
    chunks = create_chunks(
        documents,
        chunk_size,
        overlap
    )

    print(
        "Chunks           :",
        len(chunks)
    )

    # Build TF-IDF
    vectorizer, matrix = build_tfidf(
        chunks
    )

    print(
        "Vector dimension :",
        matrix.shape[1]
    )

    # Build BM25
    bm25 = build_bm25(
        chunks
    )

    precision_scores = []
    recall_scores = []
    rr_scores = []

    print()
    print(
        "Question Results"
    )

    print("-" * 70)

    # Evaluate 12 questions
    for number, item in enumerate(
        QUESTIONS,
        start=1
    ):

        question = item["question"]
        expected_source = item["source"]

        if retrieval_type == "Dense":

            results = dense_search(
                question,
                vectorizer,
                matrix,
                chunks,
                TOP_K
            )

        else:

            results = hybrid_search(
                question,
                vectorizer,
                matrix,
                bm25,
                chunks,
                TOP_K
            )

        precision = precision_at_5(
            results,
            expected_source
        )

        recall = recall_at_5(
            results,
            expected_source
        )

        rr = reciprocal_rank(
            results,
            expected_source
        )

        precision_scores.append(
            precision
        )

        recall_scores.append(
            recall
        )

        rr_scores.append(
            rr
        )

        # Find rank
        rank = 0

        for position, result in enumerate(
            results,
            start=1
        ):

            if (
                result["chunk"]["filename"]
                == expected_source
            ):

                rank = position
                break

        print(
            f"Q{number:02d} | "
            f"Expected: {expected_source:<35} | "
            f"Rank: {rank}"
        )

    # Average metrics
    avg_precision = np.mean(
        precision_scores
    )

    avg_recall = np.mean(
        recall_scores
    )

    avg_mrr = np.mean(
        rr_scores
    )

    print()
    print(
        "Average Precision@5 :",
        round(avg_precision, 4)
    )

    print(
        "Average Recall@5    :",
        round(avg_recall, 4)
    )

    print(
        "Mean Reciprocal Rank:",
        round(avg_mrr, 4)
    )

    return {
        "configuration": name,
        "precision": avg_precision,
        "recall": avg_recall,
        "mrr": avg_mrr
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print(
        "KNOWLEDGEDESK - Q8 RETRIEVAL EVALUATION"
    )
    print("=" * 70)

    print()

    print(
        "KnowledgeDesk folder :",
        BASE_DIR
    )

    print(
        "Documents folder     :",
        DOCUMENTS_FOLDER
    )

    # Check folder
    if not DOCUMENTS_FOLDER.exists():

        print()
        print(
            "ERROR: documents folder was not found."
        )

        print(
            DOCUMENTS_FOLDER
        )

        return

    # Load documents
    documents = load_documents()

    print()

    print(
        "Documents loaded :",
        len(documents)
    )

    if len(documents) == 0:

        print(
            "ERROR: No TXT documents found."
        )

        return

    print()

    print(
        "Embedding representation"
    )

    print(
        "Dimension :",
        EMBEDDING_DIMENSION
    )

    print(
        "Method    : TF-IDF feature representation"
    )

    # ========================================================
    # CONFIGURATION 1
    # 100-word chunks, 20-word overlap
    # ========================================================

    result1 = evaluate_configuration(
        "CONFIGURATION 1 - Dense Retrieval",
        "Dense",
        100,
        20,
        documents
    )

    # ========================================================
    # CONFIGURATION 2
    # 200-word chunks, 40-word overlap
    # ========================================================

    result2 = evaluate_configuration(
        "CONFIGURATION 2 - Dense Retrieval",
        "Dense",
        200,
        40,
        documents
    )

    # ========================================================
    # CONFIGURATION 3
    # 200-word chunks, 40-word overlap
    # Hybrid Dense + BM25
    # ========================================================

    result3 = evaluate_configuration(
        "CONFIGURATION 3 - Hybrid Retrieval",
        "Hybrid",
        200,
        40,
        documents
    )

    # ========================================================
    # FINAL COMPARISON
    # ========================================================

    print()
    print()
    print("=" * 70)

    print(
        "FINAL RETRIEVAL CONFIGURATION COMPARISON"
    )

    print("=" * 70)

    print()

    print(
        f"{'Configuration':<38}"
        f"{'Precision@5':<18}"
        f"{'Recall@5':<15}"
        f"{'MRR':<10}"
    )

    print("-" * 81)

    all_results = [
        result1,
        result2,
        result3
    ]

    for result in all_results:

        print(
            f"{result['configuration']:<38}"
            f"{result['precision']:<18.4f}"
            f"{result['recall']:<15.4f}"
            f"{result['mrr']:<10.4f}"
        )

    # ========================================================
    # SELECT BEST CONFIGURATION
    # ========================================================

    print()
    print("=" * 70)

    best = max(
        all_results,
        key=lambda x: (
            x["recall"],
            x["mrr"],
            x["precision"]
        )
    )

    print(
        "Best configuration:",
        best["configuration"]
    )

    print(
        "Best Recall@5:",
        round(
            best["recall"],
            4
        )
    )

    print(
        "Best MRR:",
        round(
            best["mrr"],
            4
        )
    )

    print("=" * 70)

    print()
    print(
        "Q8 evaluation completed successfully."
    )

    print("=" * 70)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()