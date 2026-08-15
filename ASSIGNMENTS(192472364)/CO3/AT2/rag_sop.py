import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )


# ============================================================
# CONFIGURATION
# ============================================================

BASE_FOLDER = os.path.dirname(
    os.path.abspath(__file__)
)

DB_FOLDER = os.path.join(
    BASE_FOLDER,
    "db"
)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

COLLECTION_NAME = "lab_sop_collection"

# Number of SOP chunks retrieved
TOP_K = 6

# Maximum acceptable ChromaDB distance
MAX_DISTANCE = 0.9


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("\n" + "=" * 80)
print("LAB SOP ASSISTANT")
print("=" * 80)

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

print("Embedding model loaded.")


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

print("\nConnecting to ChromaDB...")

chroma_client = chromadb.PersistentClient(
    path=DB_FOLDER
)

try:

    collection = chroma_client.get_collection(
        name=COLLECTION_NAME
    )

except Exception:

    raise ValueError(
        f"ChromaDB collection '{COLLECTION_NAME}' "
        "was not found. Please run the indexing program first."
    )


print(
    "Documents in database:",
    collection.count()
)

print("\n" + "=" * 80)
print("DATABASE STATUS")
print("=" * 80)

print("PDF files indexed: 3")
print("Pages processed: 78")
print("Text chunks stored: 255")
print("Embedding model: all-MiniLM-L6-v2")
print("Embedding dimension: 384")
print("ChromaDB documents:", collection.count())

print("=" * 80)


# ============================================================
# RETRIEVAL FUNCTION
# ============================================================

def retrieve_documents(query):

    query_embedding = embedding_model.encode(
        [query]
    )[0]

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=TOP_K
    )

    return results


# ============================================================
# RELEVANCE CHECK
# ============================================================

def is_relevant(results):

    distances = results["distances"][0]

    if not distances:
        return False

    best_distance = distances[0]

    print(
        f"\nBest retrieval distance: {best_distance:.4f}"
    )

    print(
        f"Maximum allowed distance: {MAX_DISTANCE:.4f}"
    )

    return best_distance <= MAX_DISTANCE


# ============================================================
# BUILD CONTEXT
# ============================================================

def build_context(results):

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    context_parts = []

    for i, (document, metadata) in enumerate(
        zip(
            documents,
            metadatas
        ),
        start=1
    ):

        source = metadata.get(
            "source",
            "Unknown"
        )

        page = metadata.get(
            "page",
            "Unknown"
        )

        chunk = metadata.get(
            "chunk",
            "Unknown"
        )

        context_parts.append(
            f"""
============================================================
SOURCE {i}
============================================================

PDF:
{source}

PAGE:
{page}

CHUNK:
{chunk}

CONTENT:
{document}
"""
        )

    return "\n".join(context_parts)


# ============================================================
# GENERATE GEMINI ANSWER
# ============================================================

def generate_answer(
    question,
    context
):

    prompt = f"""
You are a Laboratory SOP Assistant.

Answer the user's question ONLY from the provided
laboratory SOP context.

STRICT SAFETY AND GROUNDING RULES:

1. Do NOT invent laboratory procedures, quantities,
   thresholds, PPE requirements, emergency conditions,
   or cleanup methods.

2. Use ONLY information contained in the supplied
   laboratory SOP context.

3. Treat every SOP source independently.

4. If two SOP documents provide different quantities
   or thresholds, DO NOT combine them into one rule.

5. Always identify which chemical, material, or situation
   a threshold applies to.

6. Never generalize an acid-specific threshold to all
   chemical spills.

7. Never generalize a highly-toxic-material threshold
   to acids, bases, mercury, gases, or other chemicals
   unless the SOP explicitly says so.

8. Preserve exact numerical values from the SOP context.

9. If multiple SOPs provide relevant information,
   clearly distinguish the information by source.

10. For emergency situations, prioritize evacuation,
    notifying appropriate safety personnel, and following
    institutional emergency procedures when supported
    by the SOP.

11. Do not encourage inexperienced personnel to perform
    hazardous cleanup.

12. Do NOT use outside knowledge.

13. Do NOT make assumptions.

14. Do NOT merge procedures belonging to different
    chemicals.

15. When the SOP provides a specific quantity or
    threshold, reproduce it accurately.

16. If different documents have different thresholds,
    explicitly state that the thresholds belong to
    different SOP sources.

17. If the context does not contain enough information
    to answer the question safely, say:

    "The available SOP documents do not provide enough
    information to answer this safely."

18. Do not provide an answer merely because the question
    sounds related to laboratory safety. The answer must
    be supported by the retrieved SOP context.

LABORATORY SOP CONTEXT:

{context}

USER QUESTION:

{question}

Provide a clear, concise, safety-focused answer.

If numerical thresholds are present:

- State the exact threshold.
- State exactly what chemical or material it applies to.
- State the corresponding action.
- Identify the SOP source supporting that threshold.
- Do not merge thresholds from different SOPs.

At the end provide:

SOURCE:
Relevant PDF filename(s)

PAGE:
Relevant page number(s)
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# ============================================================
# INTERACTIVE SOP ASSISTANT
# ============================================================

print("\n" + "=" * 80)
print("LAB SOP ASSISTANT READY")
print("=" * 80)

print(
    "\nAsk questions about the laboratory SOP documents."
)

print(
    "Type 'exit' or 'quit' to stop."
)


while True:

    print("\n" + "-" * 80)

    question = input(
        "USER: "
    ).strip()


    # ========================================================
    # EXIT
    # ========================================================

    if question.lower() in [
        "exit",
        "quit"
    ]:

        print(
            "\nExiting Lab SOP Assistant."
        )

        break


    # ========================================================
    # EMPTY INPUT
    # ========================================================

    if not question:

        print(
            "Please enter a question."
        )

        continue


    # ========================================================
    # RETRIEVE SOP DOCUMENTS
    # ========================================================

    print(
        "\nRetrieving relevant SOP sections..."
    )

    try:

        results = retrieve_documents(
            question
        )

    except Exception as e:

        print(
            "\nRETRIEVAL ERROR:"
        )

        print(e)

        continue


    # ========================================================
    # DISPLAY RETRIEVED SOURCES
    # ========================================================

    print("\n" + "=" * 80)
    print("RETRIEVED SOP SOURCES")
    print("=" * 80)

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]


    for i, (
        document,
        metadata,
        distance
    ) in enumerate(
        zip(
            documents,
            metadatas,
            distances
        ),
        start=1
    ):

        print(
            "\n" + "-" * 80
        )

        print(
            f"RANK: {i}"
        )

        print(
            f"Distance: {distance:.4f}"
        )

        print(
            "Source:",
            metadata.get(
                "source",
                "Unknown"
            )
        )

        print(
            "Page:",
            metadata.get(
                "page",
                "Unknown"
            )
        )

        print(
            "Chunk:",
            metadata.get(
                "chunk",
                "Unknown"
            )
        )

        print(
            "\nCONTENT:"
        )

        print(
            document
        )


    # ========================================================
    # CHECK RETRIEVAL RELEVANCE
    # ========================================================

    if not is_relevant(
        results
    ):

        print(
            "\n" + "=" * 80
        )

        print(
            "INSUFFICIENT SOP EVIDENCE"
        )

        print(
            "=" * 80
        )

        print(
            "\nThe available SOP documents do not provide "
            "enough relevant information to answer this safely."
        )

        continue


    # ========================================================
    # BUILD CONTEXT
    # ========================================================

    context = build_context(
        results
    )


    # ========================================================
    # GENERATE GEMINI ANSWER
    # ========================================================

    print(
        "\n" + "=" * 80
    )

    print(
        "GENERATING SOP ANSWER"
    )

    print(
        "=" * 80
    )

    try:

        answer = generate_answer(
            question,
            context
        )

    except Exception as e:

        print(
            "\nGEMINI ERROR:"
        )

        print(e)

        continue


    # ========================================================
    # DISPLAY FINAL ANSWER
    # ========================================================

    print(
        "\n" + "=" * 80
    )

    print(
        "LAB SOP ASSISTANT"
    )

    print(
        "=" * 80
    )

    print(
        answer
    )

    print(
        "\n" + "=" * 80
    )