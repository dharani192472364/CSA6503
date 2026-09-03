import requests

MODEL = "llama3.2:latest"
OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are KnowledgeDesk, an enterprise knowledge assistant.

Rules:
1. Answer ONLY using the supplied retrieved context.
2. Do not guess or use outside knowledge.
3. Every factual answer must include the document name and page.
4. If the context does not contain sufficient evidence, refuse to answer.
5. Use this refusal:
"I’m sorry, but I cannot answer this question from the available KnowledgeDesk documents."
6. Keep the response concise and professional.
"""

def ask(question, context):
    prompt = f"""
{SYSTEM_PROMPT}

RETRIEVED CONTEXT:
{context}

USER QUESTION:
{question}

RESPONSE FORMAT:
Answer: <answer>
Source: <document name>, Page <page number>
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 100
            }
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"]


context = """
Document: HR Leave Policy 2026
Page: 4

Employees with more than 3 years of service are entitled
to 24 days of annual leave per year.
"""

print("=" * 65)
print("KNOWLEDGEDESK - Q6 HALLUCINATION CONTROL TEST")
print("=" * 65)

print("\nTEST 1: IN-CORPUS QUESTION")
print("-" * 65)

print(ask(
    "How many annual leave days are provided to an employee with more than three years of service?",
    context
))

print("\nTEST 2: OUT-OF-CORPUS QUESTION")
print("-" * 65)

print(ask(
    "What is the company's maternity leave policy?",
    context
))

print("\nTEST 3: OUT-OF-CORPUS QUESTION")
print("-" * 65)

print(ask(
    "What is the company's travel reimbursement amount?",
    context
))

print("\n" + "=" * 65)
print("HALLUCINATION CONTROL TEST COMPLETED")
print("=" * 65)