import streamlit as st
from transformers import pipeline

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Engineering College AI Chatbot",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Engineering College AI Chatbot")
st.write("Ask questions related to an engineering college.")

# -------------------------------
# LOAD PRE-TRAINED MODEL
# -------------------------------
@st.cache_resource
def load_model():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-base"
    )

chatbot = load_model()

# -------------------------------
# COLLEGE KNOWLEDGE
# -------------------------------
college_information = {
    "attendance": """
Attendance is important because it helps students regularly attend
lectures, understand concepts, participate in laboratory activities,
and maintain academic progress. Engineering colleges generally have
minimum attendance requirements that students must satisfy.
""",

    "laboratory": """
Laboratory sessions are important because they provide practical
experience. Students can apply theoretical concepts, perform
experiments, develop technical skills, and understand engineering
systems through hands-on learning.
""",

    "library": """
The college library provides textbooks, reference books, journals,
research materials and other learning resources. Students can use
the library to support their academic studies and research work.
""",

    "placement": """
The placement department helps students prepare for employment by
conducting aptitude training, technical training, soft-skill training,
mock interviews and recruitment activities with companies.
""",

    "examination": """
Examinations evaluate a student's understanding of the subjects
studied during the semester. Students should prepare regularly,
follow the examination schedule and meet the required academic
criteria.
""",

    "departments": """
Engineering colleges may have departments such as Computer Science
and Engineering, Information Technology, Electronics and Communication
Engineering, Electrical and Electronics Engineering, Mechanical
Engineering and Civil Engineering.
""",

    "academics": """
Academic activities include lectures, tutorials, laboratory sessions,
assignments, projects, internal assessments and semester examinations.
Students should participate regularly to improve their academic
performance.
"""
}

# -------------------------------
# QUESTION INPUT
# -------------------------------
question = st.text_input(
    "Enter your question:",
    placeholder="Example: What is the importance of attendance?"
)

# -------------------------------
# ASK BUTTON
# -------------------------------
if st.button("Ask Chatbot"):

    if question.strip():

        question_lower = question.lower()

        # Find relevant college information
        selected_context = ""

        for keyword, information in college_information.items():
            if keyword in question_lower:
                selected_context = information
                break

        # If relevant information is found
        if selected_context:

            prompt = f"""
Answer the student's question using the information below.

Information:
{selected_context}

Student Question:
{question}

Give a clear and concise answer.
Do not repeat the information as instructions.
Answer the question directly.
"""

        else:

            prompt = f"""
You are an AI assistant for an engineering college.

Student Question:
{question}

Give a short, clear and helpful answer.
If the question requires college-specific information that is
not provided, tell the student to contact the college administration.
"""

        # Generate response
        with st.spinner("Generating answer..."):

            result = chatbot(
                prompt,
                max_new_tokens=120,
                do_sample=False
            )

        answer = result[0]["generated_text"]

        # -------------------------------
        # DISPLAY ANSWER
        # -------------------------------
        st.subheader("🤖 Chatbot Answer")
        st.write(answer)

    else:
        st.warning("Please enter a question.")