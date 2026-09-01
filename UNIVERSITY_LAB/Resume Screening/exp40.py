import ollama

job = """
Python Developer

Required skills:
Python, SQL, Machine Learning, Git
"""

resume = input(
    "Paste candidate resume:\n"
)

prompt = f"""
You are a resume screening assistant.

Job Description:
{job}

Candidate Resume:
{resume}

Analyze the candidate.

Provide:
1. Matching skills
2. Missing skills
3. Experience relevance
4. Overall suitability
5. Score out of 100
"""

response = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

print("\n========== RESUME SCREENING ==========")
print(response["response"])