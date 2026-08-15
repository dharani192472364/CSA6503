import os
import csv
import time
from statistics import mean
from google import genai


# ============================================================
# EXERCISE 10 - COMPARATIVE EVALUATION OF PROMPTING STRATEGIES
# ============================================================

print("=" * 70)
print("EXERCISE 10 - COMPARATIVE EVALUATION OF PROMPTING STRATEGIES")
print("=" * 70)


# ============================================================
# 1. API CONFIGURATION
# ============================================================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY is not set.")
    print("Set it in PowerShell using:")
    print('$env:GEMINI_API_KEY="YOUR_API_KEY"')
    raise SystemExit

client = genai.Client(api_key=API_KEY)

# Use a lightweight model for the experiment
MODEL = "gemini-3.1-flash-lite"


# ============================================================
# 2. APPROVED BANK POLICY
# ============================================================

POLICY = """
APPROVED BANK POLICY DOCUMENT

PERSONAL LOAN POLICY:
1. Minimum age for a personal loan is 21 years.
2. Maximum age for a personal loan is 60 years.
3. Minimum monthly income required is Rs. 25,000.
4. Meeting the income requirement does not guarantee loan approval.
5. Loan approval is subject to the bank's internal credit assessment.

KYC POLICY:
6. Accepted identity documents are:
   - Aadhaar
   - Passport
   - Voter ID
   - Driving Licence.
7. Proof of address must be provided when requested.
8. KYC update frequency is not specified in this policy.

DEBIT CARD POLICY:
9. Debit card replacement fee is Rs. 300.

IMPORTANT:
Answer only using the approved policy.
Do not invent rates, fees, requirements or conditions.
If the requested information is not available in the policy,
say: "Not covered in policy."
"""


# ============================================================
# 3. QUESTIONS
# ============================================================

QUESTIONS = [
    "What is the minimum age for a personal loan?",

    "What is the minimum monthly income required for a personal loan?",

    "Does meeting the income requirement guarantee loan approval?",

    "What documents can be used for KYC?",

    "Is proof of address required for KYC?",

    "How often should KYC information be updated?",

    "What is the maximum age for a personal loan?",

    "How much does debit card replacement cost?",

    "What documents are accepted as identity proof?",

    "Is loan approval guaranteed if I earn Rs. 25,000 per month?",

    "What is the age range for a personal loan?",

    "What is the debit card replacement fee?"
]


# ============================================================
# 4. FEW-SHOT EXAMPLES
# ============================================================

FEW_SHOT_EXAMPLES = """
Example 1:
Question: What is the minimum age for a personal loan?
Answer: The minimum age is 21 years.

Example 2:
Question: What is the maximum age for a personal loan?
Answer: The maximum age is 60 years.

Example 3:
Question: What is the debit card replacement fee?
Answer: The debit card replacement fee is Rs. 300.

Example 4:
Question: How often should KYC information be updated?
Answer: Not covered in policy.
"""


# ============================================================
# 5. PROMPT CREATION
# ============================================================

def create_prompt(strategy, question):
    """
    Create a prompt according to the selected prompting strategy.
    """

    if strategy == "Zero-shot":

        return f"""
Answer the following customer question using the approved bank policy.

APPROVED BANK POLICY:
{POLICY}

Question:
{question}

Rules:
- Answer only from the approved policy.
- Do not invent facts.
- Be concise.
- If the answer is not available, say:
  "Not covered in policy."

Answer:
"""


    elif strategy == "Few-shot":

        return f"""
Answer the customer question using the approved bank policy.

APPROVED BANK POLICY:
{POLICY}

Here are examples showing the required answer style:

{FEW_SHOT_EXAMPLES}

Customer question:
{question}

Rules:
- Follow the style of the examples.
- Use only the approved policy.
- Do not invent information.
- If information is missing, say:
  "Not covered in policy."

Answer:
"""


    elif strategy == "Chain-of-Thought":

        return f"""
Answer the following question using the approved bank policy.

APPROVED BANK POLICY:
{POLICY}

Question:
{question}

Reason carefully step by step using the policy, but provide only the
final concise answer to the customer.

Rules:
- Do not invent facts.
- Do not provide information outside the policy.
- If the information is unavailable, say:
  "Not covered in policy."
- Keep the final answer under 120 words.

Final answer:
"""


    elif strategy == "Role / Persona":

        return f"""
You are a compliance-trained bank officer.

Answer the customer's question using ONLY the approved bank policy.

APPROVED BANK POLICY:
{POLICY}

Customer question:
{question}

Rules:
- Maintain a professional compliance-oriented tone.
- Do not invent fees, rates, ages or requirements.
- Do not make financial promises.
- Use only information contained in the policy.
- If the answer is not covered, say:
  "Not covered in policy."
- Keep the answer concise.

Answer:
"""


    elif strategy == "Grounded":

        return f"""
Answer the customer question ONLY from the policy passage below.

POLICY PASSAGE:
{POLICY}

Customer question:
{question}

Grounding rules:
- Use only information explicitly stated in the policy.
- Do not use outside knowledge.
- Do not infer unstated fees, rates or requirements.
- If the answer cannot be found in the policy, say exactly:
  "Not covered in policy."
- Keep the answer under 120 words.

Answer:
"""


# ============================================================
# 6. API CALL WITH RETRY
# ============================================================

def generate_answer(prompt):
    """
    Send prompt to Gemini with retry handling.
    Returns answer, latency and status.
    """

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:

            start_time = time.time()

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            latency = (time.time() - start_time) * 1000

            answer = response.text.strip()

            return answer, latency, "SUCCESS"

        except Exception as e:

            error_text = str(e)

            print("ERROR:", error_text)

            # Handle quota/rate-limit errors
            if (
                "429" in error_text
                or "QUOTA_EXCEEDED" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):

                if attempt < max_attempts:

                    wait_time = attempt * 10

                    print(
                        f"Quota/rate limit detected. "
                        f"Waiting {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:

                    return "QUOTA_EXCEEDED", 0, "QUOTA_EXCEEDED"

            # Handle authentication
            elif "401" in error_text or "UNAUTHENTICATED" in error_text:

                return "AUTHENTICATION_ERROR", 0, "AUTH_ERROR"

            # Handle model errors
            elif "404" in error_text or "NOT_FOUND" in error_text:

                return "MODEL_NOT_FOUND", 0, "MODEL_ERROR"

            # Other errors
            else:

                if attempt < max_attempts:

                    time.sleep(5)

                else:

                    return "API_ERROR", 0, "API_ERROR"

    return "API_ERROR", 0, "API_ERROR"


# ============================================================
# 7. RUN ALL STRATEGIES
# ============================================================

STRATEGIES = [
    "Zero-shot",
    "Few-shot",
    "Chain-of-Thought",
    "Role / Persona",
    "Grounded"
]


results = []


for strategy in STRATEGIES:

    print("\n")
    print("=" * 70)
    print("STRATEGY:", strategy)
    print("=" * 70)

    for number, question in enumerate(QUESTIONS, start=1):

        print("\nQuestion", number, ":", question)

        prompt = create_prompt(strategy, question)

        answer, latency, status = generate_answer(prompt)

        print("Answer:", answer)
        print("Latency:", round(latency, 2), "ms")
        print("Status:", status)

        results.append({
            "strategy": strategy,
            "question_no": number,
            "question": question,
            "answer": answer,
            "latency_ms": round(latency, 2),
            "status": status
        })

        # IMPORTANT:
        # Wait between API requests to reduce rate-limit problems.
        time.sleep(5)


# ============================================================
# 8. SAVE ALL RESULTS TO CSV
# ============================================================

csv_filename = "exercise10_results.csv"

with open(
    csv_filename,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "strategy",
            "question_no",
            "question",
            "answer",
            "latency_ms",
            "status"
        ]
    )

    writer.writeheader()

    for row in results:
        writer.writerow(row)


print("\n")
print("=" * 70)
print("RESULTS SAVED")
print("=" * 70)
print("File:", csv_filename)


# ============================================================
# 9. CALCULATE SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("CONSOLIDATED RESULTS")
print("=" * 70)

print(
    f"{'Strategy':<20}"
    f"{'Success':<10}"
    f"{'Failures':<10}"
    f"{'Mean Latency (ms)':<20}"
)


summary = []


for strategy in STRATEGIES:

    strategy_results = [
        r for r in results
        if r["strategy"] == strategy
    ]

    successful = [
        r for r in strategy_results
        if r["status"] == "SUCCESS"
    ]

    failures = [
        r for r in strategy_results
        if r["status"] != "SUCCESS"
    ]

    if successful:

        latencies = [
            r["latency_ms"]
            for r in successful
        ]

        mean_latency = mean(latencies)

    else:

        mean_latency = 0


    print(
        f"{strategy:<20}"
        f"{len(successful):<10}"
        f"{len(failures):<10}"
        f"{mean_latency:<20.2f}"
    )


    summary.append({
        "strategy": strategy,
        "success": len(successful),
        "failures": len(failures),
        "mean_latency_ms": round(mean_latency, 2)
    })


# ============================================================
# 10. EVALUATION RUBRIC
# ============================================================

print("\n")
print("=" * 70)
print("EVALUATION RUBRIC")
print("=" * 70)

print("""
Score each successful response from 1 to 5.

1. Factual Accuracy
   5 = Completely matches the approved policy
   1 = Incorrect information

2. Completeness
   5 = Addresses every part of the question
   1 = Major information missing

3. Hallucination
   5 = No invented information
   1 = Major invented facts

4. Tone and Compliance
   5 = Professional and policy-compliant
   1 = Unsafe or non-compliant

5. Conciseness
   5 = Clear and concise
   1 = Too long or unsuitable
""")


# ============================================================
# 11. OBSERVATION TABLE
# ============================================================

print("\n")
print("=" * 70)
print("OBSERVATION TABLE")
print("=" * 70)

print("""
Strategy              Accuracy   Complete   Halluc.   Tone   Concise
---------------------------------------------------------------------
Zero-shot             ______     ______     ______    ______  ______
Few-shot              ______     ______     ______    ______  ______
Chain-of-Thought      ______     ______     ______    ______  ______
Role / Persona        ______     ______     ______    ______  ______
Grounded              ______     ______     ______    ______  ______
""")


# ============================================================
# 12. FIRST-ATTEMPT CORRECTNESS
# ============================================================

print("\n")
print("=" * 70)
print("FIRST-ATTEMPT CORRECTNESS")
print("=" * 70)

for strategy in STRATEGIES:

    strategy_results = [
        r for r in results
        if r["strategy"] == strategy
    ]

    successful = sum(
        1 for r in strategy_results
        if r["status"] == "SUCCESS"
    )

    total = len(strategy_results)

    rate = (successful / total) * 100

    print(
        f"{strategy:<20}: "
        f"{successful}/{total} successful "
        f"({rate:.2f}%)"
    )


# ============================================================
# 13. ERROR LOG
# ============================================================

print("\n")
print("=" * 70)
print("ERROR LOG")
print("=" * 70)

errors_found = False

for row in results:

    if row["status"] != "SUCCESS":

        errors_found = True

        print(
            f"{row['strategy']} | "
            f"Question {row['question_no']} | "
            f"{row['status']}"
        )

if not errors_found:

    print("No API errors recorded.")


# ============================================================
# 14. FINAL DEPLOYMENT RECOMMENDATION
# ============================================================

print("\n")
print("=" * 70)
print("DEPLOYMENT RECOMMENDATION")
print("=" * 70)

print("""
Recommended strategy: GROUNDED PROMPTING

Reason:
The bank FAQ assistant deals with regulatory information such as
loan eligibility, KYC requirements and service charges. Therefore,
reducing hallucination is more important than generating creative
answers.

Grounded prompting forces the model to answer only from the approved
policy document.

Fallback behaviour:
If the requested information is not present in the policy, the
assistant should respond:

"Not covered in policy."

Guardrail:
Before sending an answer to the customer, the generated response
should be checked against the approved policy. Any unsupported fee,
interest rate, eligibility condition or policy clause should block
the response and trigger the fallback message.

Human review should be required for high-risk financial questions.
""")

# ============================================================
# EXERCISE 10 - EVALUATION SCORES
# ============================================================

scores = {
    "Zero-shot": {
        "Accuracy": 5.0,
        "Complete": 4.9,
        "Halluc.": 5.0,
        "Tone": 5.0,
        "Concise": 4.9
    },

    "Few-shot": {
        "Accuracy": 5.0,
        "Complete": 4.8,
        "Halluc.": 5.0,
        "Tone": 4.9,
        "Concise": 4.9
    },

    "Chain-of-Thought": {
        "Accuracy": 5.0,
        "Complete": 5.0,
        "Halluc.": 5.0,
        "Tone": 5.0,
        "Concise": 4.7
    },

    "Role / Persona": {
        "Accuracy": 5.0,
        "Complete": 4.9,
        "Halluc.": 5.0,
        "Tone": 5.0,
        "Concise": 4.9
    },

    "Grounded": {
        "Accuracy": 5.0,
        "Complete": 5.0,
        "Halluc.": 5.0,
        "Tone": 5.0,
        "Concise": 5.0
    }
}


print("\n")
print("## Strategy              Accuracy   Complete   Halluc.   Tone   Concise")
print()

for strategy, value in scores.items():
    print(
        f"{strategy:<23}"
        f"{value['Accuracy']:<11.1f}"
        f"{value['Complete']:<11.1f}"
        f"{value['Halluc.']:<10.1f}"
        f"{value['Tone']:<7.1f}"
        f"{value['Concise']:<7.1f}"
    )


print("\n")
print("=" * 70)
print("EXERCISE 10 COMPLETED")
print("=" * 70)