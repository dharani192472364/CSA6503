import faiss
from sentence_transformers import SentenceTransformer
from ollama import chat

from faq_data import FAQ_DATA


class FAQChatbot:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.questions = [
            item["question"]
            for item in FAQ_DATA
        ]

        self.answers = [
            item["answer"]
            for item in FAQ_DATA
        ]

        print("Creating FAQ embeddings...")

        embeddings = self.model.encode(
            self.questions,
            convert_to_numpy=True
        )

        embeddings = embeddings.astype("float32")

        # Normalize embeddings
        faiss.normalize_L2(embeddings)

        # Create FAISS index
        self.index = faiss.IndexFlatIP(
            embeddings.shape[1]
        )

        self.index.add(embeddings)

        print(
            f"Chatbot initialized with "
            f"{len(self.questions)} FAQs."
        )

    def retrieve_faq(self, user_query, top_k=3):

        query_embedding = self.model.encode(
            [user_query],
            convert_to_numpy=True
        ).astype("float32")

        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            results.append({
                "question": self.questions[index],
                "answer": self.answers[index],
                "score": float(score)
            })

        return results

    def generate_answer(self, user_query):

        results = self.retrieve_faq(
            user_query,
            top_k=3
        )

        best_result = results[0]

        # Fallback for unrelated questions
        if best_result["score"] < 0.35:

            return (
                "I'm sorry, but I don't have enough "
                "information to answer that question. "
                "Please ask about college academics, "
                "attendance, examinations, library, "
                "placements, facilities, or student services."
            ), results

        context = "\n\n".join(
            [
                f"FAQ Question: {r['question']}\n"
                f"FAQ Answer: {r['answer']}"
                for r in results
            ]
        )

        prompt = f"""
You are a helpful college FAQ assistant.

Answer the student's question using ONLY
the information provided in the FAQ context.

If the information is not available in the
context, clearly say that the information is
not available.

Do not invent college policies, fees,
dates, names, or rules.

FAQ CONTEXT:
{context}

STUDENT QUESTION:
{user_query}

Give a short, clear and helpful answer.
"""

        try:

            response = chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = response["message"]["content"]

            return answer, results

        except Exception:

            return (
                "The AI model could not be reached. "
                "Please make sure Ollama is running "
                "and the llama3.2 model is installed."
            ), results