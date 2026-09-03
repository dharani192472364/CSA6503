import os
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# JOB DESCRIPTION
# =========================================================

job_description = """
We are looking for a Software Engineer with experience in
Python, backend development, REST APIs, Django, Node.js,
AWS, Docker, Kubernetes, cloud deployment, microservices
and SaaS application development.
"""


# =========================================================
# GET PROGRAM FOLDER
# =========================================================

folder = os.path.dirname(os.path.abspath(__file__))


# =========================================================
# RESUME FILES
# =========================================================

resume_files = [
    "resume1.pdf",
    "resume2.pdf",
    "resume3.pdf"
]


# =========================================================
# READ RESUMES
# =========================================================

def read_resumes():

    resumes = {}

    for file in resume_files:

        file_path = os.path.join(folder, file)

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

        resumes[file] = text

    return resumes


# =========================================================
# METHOD 1: WITHOUT API
# TF-IDF + COSINE SIMILARITY
# =========================================================

def without_api(resumes):

    print("\n======================================")
    print("   RESUME SCREENING - WITHOUT API")
    print("======================================")

    documents = [job_description] + list(resumes.values())

    # Convert text into TF-IDF vectors
    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    # Compare job description with resumes
    similarity_scores = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    )[0]

    results = []

    for i in range(len(resume_files)):

        score = similarity_scores[i] * 100

        results.append(
            (resume_files[i], score)
        )

    # Highest score first
    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    print("\nCANDIDATE RANKING")
    print("--------------------------------------")

    for rank, (resume, score) in enumerate(results, 1):

        print(
            f"{rank}. {resume} "
            f"--> Relevance Score: {score:.2f}%"
        )

    print("--------------------------------------")


# =========================================================
# METHOD 2: WITH GEMINI API
# =========================================================

def with_api(resumes):

    print("\n======================================")
    print("      RESUME SCREENING - API")
    print("======================================")

    try:

        from dotenv import load_dotenv
        from google import genai

        # Load .env file
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:

            print("\nGemini API key not found.")
            print("Create a .env file containing:")
            print("GEMINI_API_KEY=YOUR_API_KEY")
            return

        # Create Gemini client
        client = genai.Client(
            api_key=api_key
        )

        # Combine resumes
        resume_data = ""

        for file, text in resumes.items():

            resume_data += f"""
            
            RESUME: {file}
            
            {text}
            
            """

        # AI prompt
        prompt = f"""
You are an AI Resume Screening System.

Compare the candidates with the following job description.

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUMES:
{resume_data}

For every candidate:

1. Give a relevance score from 0 to 100.
2. List matching skills.
3. List missing skills.
4. Give a short reason.

Finally, rank all candidates from highest
to lowest score.

Use this format:

RANK 1:
Candidate:
Score:
Matching Skills:
Missing Skills:
Reason:

RANK 2:
Candidate:
Score:
Matching Skills:
Missing Skills:
Reason:

RANK 3:
Candidate:
Score:
Matching Skills:
Missing Skills:
Reason:

FINAL RANKING:
1.
2.
3.
"""

        # Send request to Gemini
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        print("\nAI SCREENING RESULT")
        print("--------------------------------------")
        print(response.text)
        print("--------------------------------------")

    except ImportError:

        print("\nRequired API libraries are not installed.")

        print("\nRun:")
        print("pip install google-genai python-dotenv")


# =========================================================
# MAIN PROGRAM
# =========================================================

print("\n======================================")
print("       AI RESUME SCREENING SYSTEM")
print("======================================")

print("\nSelect Screening Method:")
print("1. Without API")
print("2. With Gemini API")
print("3. Run Both")

choice = input("\nEnter your choice (1/2/3): ")


# Read all resumes
try:

    resumes = read_resumes()

except FileNotFoundError as e:

    print("\nERROR: Resume file not found.")
    print(e)
    print("\nMake sure these files are inside the same folder:")
    print("resume1.pdf")
    print("resume2.pdf")
    print("resume3.pdf")
    exit()


# Run selected method

if choice == "1":

    without_api(resumes)


elif choice == "2":

    with_api(resumes)


elif choice == "3":

    without_api(resumes)

    with_api(resumes)


else:

    print("\nInvalid choice.")

print("\nProgram completed.")