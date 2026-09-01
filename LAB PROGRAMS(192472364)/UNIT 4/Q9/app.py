import streamlit as st
from sentence_transformers import SentenceTransformer, util
from pypdf import PdfReader

st.title("AI Resume Screening System")

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

job = st.text_area(
    "Enter Engineering Job Description:",
    "Python developer with machine learning, SQL and AI skills"
)

files = st.file_uploader(
    "Upload resumes",
    type="pdf",
    accept_multiple_files=True
)

if st.button("Rank Resumes"):

    if files:

        job_embedding = model.encode(job)

        results = []

        for file in files:

            reader = PdfReader(file)

            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

            resume_embedding = model.encode(text)

            score = util.cos_sim(
                job_embedding,
                resume_embedding
            ).item()

            results.append(
                (file.name, score)
            )

        results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        st.write("### Resume Ranking")

        for i, (name, score) in enumerate(results, 1):

            st.write(
                f"{i}. {name} - Score: {score:.2f}"
            )