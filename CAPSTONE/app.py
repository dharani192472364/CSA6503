import streamlit as st
import os
import json
import re
import pandas as pd

from dotenv import load_dotenv
from google import genai

from database import (
    create_tables,
    register_user,
    login_user,
    get_user,
    save_quiz_result,
    get_quiz_results,
    save_study_plan,
    save_tutor_history
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Study System",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# CREATE DATABASE
# =========================================================

create_tables()


# =========================================================
# LOAD GEMINI API KEY
# =========================================================

load_dotenv()

API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

if not API_KEY:

    st.error(
        "❌ Gemini API key not found."
    )

    st.info(
        "Make sure your .env file contains:"
    )

    st.code(
        "GEMINI_API_KEY=YOUR_API_KEY"
    )

    st.stop()


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=API_KEY
)


# Use a commonly available Gemini Flash model
MODEL = "gemini-3.6-flash"


# =========================================================
# SESSION STATE
# =========================================================

defaults = {

    "logged_in": False,

    "user_id": None,

    "username": "",

    "full_name": "",

    "quiz_data": None,

    "quiz_subject_value": "",

    "quiz_topic_value": "",

    "quiz_score": 0,

    "quiz_question": 0,

    "quiz_checked": False,

    "quiz_result_saved": False
}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# LOGIN / REGISTER PAGE
# =========================================================

if not st.session_state.logged_in:

    st.title(
        "🎓 AI Study System"
    )

    st.subheader(
        "Your Personal AI-Powered Learning Assistant"
    )

    st.divider()


    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Register"
        ]
    )


    # =====================================================
    # LOGIN
    # =====================================================

    with login_tab:

        st.header(
            "🔐 Student Login"
        )

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )


        if st.button(
            "🔐 Login",
            type="primary",
            width="stretch"
        ):

            if not username or not password:

                st.warning(
                    "Please enter username and password."
                )

            else:

                user = login_user(
                    username,
                    password
                )

                if user:

                    st.session_state.logged_in = True

                    st.session_state.user_id = user[0]

                    st.session_state.username = user[1]

                    st.session_state.full_name = user[2]

                    st.success(
                        f"Welcome {user[2]}! 🎉"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid username or password."
                    )


    # =====================================================
    # REGISTER
    # =====================================================

    with register_tab:

        st.header(
            "📝 Create Account"
        )

        full_name = st.text_input(
            "Full Name",
            key="register_full_name"
        )

        username = st.text_input(
            "Username",
            key="register_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm_password"
        )


        if st.button(
            "📝 Register",
            type="primary",
            width="stretch"
        ):

            if not full_name:

                st.warning(
                    "Enter your full name."
                )

            elif not username:

                st.warning(
                    "Enter a username."
                )

            elif not password:

                st.warning(
                    "Enter a password."
                )

            elif len(password) < 6:

                st.warning(
                    "Password must contain at least 6 characters."
                )

            elif password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            else:

                user_id = register_user(
                    username,
                    password,
                    full_name
                )

                if user_id:

                    st.success(
                        "✅ Account created successfully!"
                    )

                    st.info(
                        "Now open the Login tab and login."
                    )

                else:

                    st.error(
                        "❌ Username already exists."
                    )


    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(
    "🎓 AI Study System"
)

st.sidebar.success(
    f"👋 {st.session_state.full_name}"
)

st.sidebar.caption(
    f"Username: {st.session_state.username}"
)

st.sidebar.divider()


page = st.sidebar.radio(
    "Choose Module",
    [
        "📅 Study Planner",
        "🤖 AI Tutor",
        "📝 Quiz Generator",
        "📊 Progress Tracking"
    ]
)


# =========================================================
# LOGOUT
# =========================================================

if st.sidebar.button(
    "🚪 Logout",
    width="stretch"
):

    st.session_state.logged_in = False

    st.session_state.user_id = None

    st.session_state.username = ""

    st.session_state.full_name = ""

    st.session_state.quiz_data = None

    st.session_state.quiz_score = 0

    st.session_state.quiz_question = 0

    st.session_state.quiz_checked = False

    st.session_state.quiz_result_saved = False

    st.rerun()


# =========================================================
# STUDY PLANNER
# =========================================================

if page == "📅 Study Planner":

    st.title(
        "📅 Personalized Adaptive Study Planner"
    )

    st.write(
        "Create a personalized study plan using Gemini AI."
    )

    st.divider()


    name = st.text_input(
        "Student Name",
        value=st.session_state.full_name,
        key="planner_name"
    )


    subjects = st.text_input(
        "Subjects",
        placeholder="Python, AI, DBMS, Computer Networks",
        key="planner_subjects"
    )


    hours = st.number_input(
        "Study Hours Per Day",
        min_value=1,
        max_value=12,
        value=3,
        key="planner_hours"
    )


    goal = st.text_area(
        "Study Goal",
        placeholder="Prepare for semester examinations",
        key="planner_goal"
    )


    weak = st.text_input(
        "Weak Subjects",
        placeholder="DBMS, Computer Networks",
        key="planner_weak"
    )


    exam_date = st.date_input(
        "Upcoming Exam Date",
        key="planner_exam"
    )


    if st.button(
        "🚀 Generate Study Plan",
        type="primary",
        width="stretch"
    ):

        if not subjects or not goal:

            st.warning(
                "Please enter subjects and study goal."
            )

        else:

            prompt = f"""
You are an intelligent academic study planner.

Student Name:
{name}

Subjects:
{subjects}

Study Hours Per Day:
{hours}

Study Goal:
{goal}

Weak Subjects:
{weak}

Upcoming Exam Date:
{exam_date}

Create a personalized study plan.

Include:

1. Daily schedule
2. Subject priorities
3. Time allocation
4. Weak subject improvement
5. Revision strategy
6. Exam preparation tips
7. Daily targets

Make it practical for an engineering college student.
"""


            with st.spinner(
                "🤖 Creating study plan..."
            ):

                try:

                    response = client.models.generate_content(
                        model=MODEL,
                        contents=prompt
                    )

                    plan = response.text


                    save_study_plan(
                        st.session_state.user_id,
                        subjects,
                        hours,
                        goal,
                        weak,
                        exam_date,
                        plan
                    )


                    st.success(
                        "✅ Study plan generated and saved!"
                    )


                    st.markdown(
                        "## 📚 Personalized Study Plan"
                    )

                    st.write(
                        plan
                    )


                except Exception as e:

                    st.error(
                        f"Gemini Error: {e}"
                    )


# =========================================================
# AI TUTOR
# =========================================================

elif page == "🤖 AI Tutor":

    st.title(
        "🤖 AI Tutor"
    )

    st.write(
        "Ask your personal AI tutor any engineering question."
    )

    st.divider()


    subject = st.selectbox(
        "Select Subject",
        [
            "Artificial Intelligence",
            "Machine Learning",
            "Python",
            "C Programming",
            "C++",
            "Java",
            "DBMS",
            "Computer Networks",
            "Operating Systems",
            "Computer Vision",
            "Generative AI",
            "other"
        ],
        key="tutor_subject"
    )


    level = st.selectbox(
        "Knowledge Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        key="tutor_level"
    )


    question = st.text_area(
        "Ask your question",
        placeholder="Example: Explain neural networks in simple words.",
        key="tutor_question"
    )


    if st.button(
        "🤖 Ask AI Tutor",
        type="primary",
        width="stretch"
    ):

        if not question:

            st.warning(
                "Please enter a question."
            )

        else:

            prompt = f"""
You are an AI engineering college tutor.

Subject:
{subject}

Student Level:
{level}

Question:
{question}

Explain clearly and simply.

Include:

1. Simple definition
2. Step-by-step explanation
3. Practical example
4. Important examination points
5. Code example if appropriate
6. Two practice questions
"""


            with st.spinner(
                "🤖 AI Tutor is thinking..."
            ):

                try:

                    response = client.models.generate_content(
                        model=MODEL,
                        contents=prompt
                    )

                    answer = response.text


                    save_tutor_history(
                        st.session_state.user_id,
                        subject,
                        question,
                        answer
                    )


                    st.success(
                        "✅ Answer generated!"
                    )


                    st.markdown(
                        "### 🤖 Tutor Answer"
                    )

                    st.write(
                        answer
                    )


                except Exception as e:

                    st.error(
                        f"Gemini Error: {e}"
                    )


# =========================================================
# QUIZ GENERATOR
# =========================================================

elif page == "📝 Quiz Generator":

    st.title(
        "📝 Interactive AI Quiz"
    )

    st.write(
        "Generate MCQs and automatically update your performance."
    )

    st.divider()


    # -----------------------------------------------------
    # QUIZ SETTINGS
    # -----------------------------------------------------

    subject = st.selectbox(
        "Select Subject",
        [
            "Artificial Intelligence",
            "Machine Learning",
            "Python",
            "C Programming",
            "C++",
            "Java",
            "DBMS",
            "Computer Networks",
            "Operating Systems",
            "Computer Vision",
            "Generative AI",
            "OTHERS"
        ],
        key="quiz_subject_select"
    )


    topic = st.text_input(
        "Enter Topic",
        placeholder="Example: Neural Networks",
        key="quiz_topic_input"
    )


    difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ],
        key="quiz_difficulty"
    )


    number = st.selectbox(
        "Number of Questions",
        [5, 10],
        key="quiz_number"
    )


    # -----------------------------------------------------
    # GENERATE QUIZ
    # -----------------------------------------------------

    if st.button(
        "🚀 Generate Quiz",
        type="primary",
        width="stretch"
    ):

        if not topic:

            st.warning(
                "Please enter a topic."
            )

        else:

            prompt = f"""
Create exactly {number} multiple-choice questions.

Subject:
{subject}

Topic:
{topic}

Difficulty:
{difficulty}

Return ONLY valid JSON.

Use exactly this format:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option A",
    "explanation": "Short explanation"
  }}
]

Rules:

1. Create exactly {number} questions.
2. Every question must have exactly 4 options.
3. Only one option must be correct.
4. The answer must exactly match one option.
5. Return JSON only.
6. Do not use markdown.
7. Do not write anything before or after the JSON.
8. Questions should be suitable for engineering college students.
"""


            with st.spinner(
                "🤖 Generating quiz..."
            ):

                try:

                    response = client.models.generate_content(
                        model=MODEL,
                        contents=prompt
                    )


                    quiz_text = response.text.strip()


                    # Remove markdown fences
                    quiz_text = re.sub(
                        r"```json\s*",
                        "",
                        quiz_text,
                        flags=re.IGNORECASE
                    )


                    quiz_text = re.sub(
                        r"```\s*$",
                        "",
                        quiz_text
                    ).strip()


                    quiz = json.loads(
                        quiz_text
                    )


                    if not isinstance(
                        quiz,
                        list
                    ):

                        raise ValueError(
                            "Gemini did not return a quiz list."
                        )


                    if len(quiz) != number:

                        raise ValueError(
                            f"Expected {number} questions but received {len(quiz)}."
                        )


                    # Validate questions

                    for q in quiz:

                        if "question" not in q:

                            raise ValueError(
                                "Question field missing."
                            )


                        if "options" not in q:

                            raise ValueError(
                                "Options field missing."
                            )


                        if "answer" not in q:

                            raise ValueError(
                                "Answer field missing."
                            )


                        if "explanation" not in q:

                            raise ValueError(
                                "Explanation field missing."
                            )


                        if len(q["options"]) != 4:

                            raise ValueError(
                                "Every question must have exactly 4 options."
                            )


                        if q["answer"] not in q["options"]:

                            raise ValueError(
                                "Correct answer does not match an option."
                            )


                    # -------------------------------------------------
                    # SAVE QUIZ
                    # -------------------------------------------------

                    st.session_state.quiz_data = quiz

                    st.session_state.quiz_subject_value = subject

                    st.session_state.quiz_topic_value = topic

                    st.session_state.quiz_score = 0

                    st.session_state.quiz_question = 0

                    st.session_state.quiz_checked = False

                    st.session_state.quiz_result_saved = False


                    st.success(
                        "✅ Interactive quiz generated!"
                    )


                    st.rerun()


                except json.JSONDecodeError:

                    st.error(
                        "❌ Gemini returned invalid JSON. Please generate again."
                    )


                except Exception as e:

                    st.error(
                        f"Quiz Error: {e}"
                    )


    # =====================================================
    # DISPLAY QUIZ
    # =====================================================

    if st.session_state.quiz_data:

        quiz = st.session_state.quiz_data

        current = st.session_state.quiz_question

        total = len(quiz)

        score = st.session_state.quiz_score


        # =================================================
        # QUIZ COMPLETED
        # =================================================

        if current >= total:

            percentage = (
                score / total
            ) * 100


            st.success(
                "🎉 Quiz Completed!"
            )


            st.divider()


            st.header(
                "📊 Your Quiz Result"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Correct Answers",
                    f"{score}/{total}"
                )


            with col2:

                st.metric(
                    "Percentage",
                    f"{percentage:.1f}%"
                )


            with col3:

                if percentage >= 80:

                    grade = "Excellent"

                elif percentage >= 60:

                    grade = "Good"

                elif percentage >= 40:

                    grade = "Needs Practice"

                else:

                    grade = "Needs Improvement"


                st.metric(
                    "Performance",
                    grade
                )


            st.divider()


            # =================================================
            # SAVE RESULT
            # =================================================

            if not st.session_state.quiz_result_saved:

                try:

                    save_quiz_result(
                        st.session_state.user_id,
                        st.session_state.quiz_subject_value,
                        st.session_state.quiz_topic_value,
                        round(
                            percentage,
                            2
                        ),
                        total,
                        score
                    )


                    st.session_state.quiz_result_saved = True


                    st.success(
                        "💾 Performance automatically saved to SQLite!"
                    )


                except Exception as e:

                    st.error(
                        f"Database Error: {e}"
                    )


            # =================================================
            # PERFORMANCE MESSAGE
            # =================================================

            if percentage >= 80:

                st.success(
                    "🌟 Excellent performance! Keep it up!"
                )

            elif percentage >= 60:

                st.info(
                    "👍 Good performance! A little more practice will help."
                )

            elif percentage >= 40:

                st.warning(
                    "📚 You need more practice on this topic."
                )

            else:

                st.error(
                    "💪 Revise this topic and try again."
                )


            st.info(
                "📊 Open Progress Tracking to view your performance."
            )


            # =================================================
            # NEW QUIZ
            # =================================================

            if st.button(
                "🔄 Create New Quiz",
                key="new_quiz_button"
            ):

                st.session_state.quiz_data = None

                st.session_state.quiz_subject_value = ""

                st.session_state.quiz_topic_value = ""

                st.session_state.quiz_score = 0

                st.session_state.quiz_question = 0

                st.session_state.quiz_checked = False

                st.session_state.quiz_result_saved = False

                st.rerun()


        # =================================================
        # CURRENT QUESTION
        # =================================================

        else:

            q = quiz[current]


            st.progress(
                (current + 1) / total
            )


            st.write(
                f"### Question {current + 1} of {total}"
            )


            st.subheader(
                q["question"]
            )


            # -------------------------------------------------
            # ANSWER OPTIONS
            # -------------------------------------------------

            selected = st.radio(
                "Choose your answer:",
                q["options"],
                key=f"answer_{current}"
            )


            # =================================================
            # CHECK ANSWER
            # =================================================

            if not st.session_state.quiz_checked:

                if st.button(
                    "✅ Check Answer",
                    type="primary",
                    key=f"check_answer_{current}"
                ):

                    st.session_state.quiz_checked = True


                    if selected == q["answer"]:

                        st.session_state.quiz_score += 1


                    st.rerun()


            # =================================================
            # SHOW RESULT
            # =================================================

            else:

                if selected == q["answer"]:

                    st.success(
                        "✅ Correct Answer!"
                    )

                else:

                    st.error(
                        "❌ Wrong Answer!"
                    )

                    st.info(
                        f"Correct Answer: {q['answer']}"
                    )


                st.markdown(
                    "### 💡 Explanation"
                )


                st.write(
                    q["explanation"]
                )


                # =================================================
                # NEXT QUESTION
                # =================================================

                if st.button(
                    "➡️ Next Question",
                    type="primary",
                    key=f"next_question_{current}"
                ):

                    st.session_state.quiz_question += 1

                    st.session_state.quiz_checked = False

                    st.rerun()

# =========================================================
# PROGRESS TRACKING
# =========================================================
# =========================================================
# PROGRESS TRACKING
# =========================================================

elif page == "📊 Progress Tracking":

    st.title("📊 Student Performance Dashboard")

    st.write(
        "Your quiz performance is automatically loaded from SQLite."
    )

    st.divider()

    try:

        results = get_quiz_results(
            st.session_state.user_id
        )

    except Exception as e:

        st.error(
            f"Database Error: {e}"
        )

        st.stop()


    if not results:

        st.info(
            "📝 No quiz results found."
        )

        st.write(
            "Complete a quiz to see your performance here."
        )

    else:

        data = []

        for row in results:

            data.append({
                "Date": row[7],
                "Subject": row[2],
                "Topic": row[3],
                "Score": row[4],
                "Total Questions": row[5],
                "Correct Answers": row[6],
                "Percentage": row[4]
            })


        df = pd.DataFrame(data)


        # =====================================================
        # QUIZ HISTORY
        # =====================================================

        st.header("📋 Quiz History")

        display_df = df[
            [
                "Date",
                "Subject",
                "Topic",
                "Score",
                "Total Questions",
                "Correct Answers",
                "Percentage"
            ]
        ].copy()


        display_df["Percentage"] = display_df[
            "Percentage"
        ].map(
            lambda x: f"{x:.1f}%"
        )


        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True
        )


        st.divider()


        # =====================================================
        # METRICS
        # =====================================================

        average = df["Percentage"].mean()

        highest = df["Percentage"].max()

        lowest = df["Percentage"].min()

        total_quizzes = len(df)


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "📊 Average",
                f"{average:.1f}%"
            )


        with col2:

            st.metric(
                "🏆 Highest",
                f"{highest:.1f}%"
            )


        with col3:

            st.metric(
                "📉 Lowest",
                f"{lowest:.1f}%"
            )


        with col4:

            st.metric(
                "📝 Quizzes",
                total_quizzes
            )


        st.divider()


        # =====================================================
        # PERFORMANCE GRAPH
        # =====================================================

        st.header("📈 Quiz Performance")


        chart_data = df[
            ["Date", "Percentage"]
        ].copy()


        chart_data = chart_data.set_index(
            "Date"
        )


        st.line_chart(
            chart_data
        )


        st.divider()


        # =====================================================
        # SUBJECT PERFORMANCE
        # =====================================================

        st.header("🎯 Subject Performance")


        subject_average = (
            df.groupby("Subject")["Percentage"]
            .mean()
            .sort_values()
        )


        st.bar_chart(
            subject_average
        )


        st.divider()


        # =====================================================
        # STRONGEST / WEAKEST
        # =====================================================

        weakest_subject = subject_average.index[0]

        strongest_subject = subject_average.index[-1]


        col1, col2 = st.columns(2)


        with col1:

            st.error(
                f"🔴 Weakest Subject: {weakest_subject}"
            )


        with col2:

            st.success(
                f"🟢 Strongest Subject: {strongest_subject}"
            )


        st.divider()


        # =====================================================
        # AI PERFORMANCE ANALYSIS
        # =====================================================

        st.header(
            "🤖 AI Performance Analysis"
        )


        if st.button(
            "🧠 Analyze My Performance",
            type="primary"
        ):

            performance_prompt = f"""
You are an AI academic performance advisor.

Analyze the following quiz results:

{df.to_string(index=False)}

Provide:

1. Overall performance analysis
2. Strong subjects
3. Weak subjects
4. Topics needing revision
5. Recommended study schedule
6. Improvement strategies
7. Exam preparation advice

Give practical recommendations for an engineering college student.
"""


            with st.spinner(
                "🤖 AI is analyzing your performance..."
            ):

                try:

                    response = client.models.generate_content(
                        model=MODEL,
                        contents=performance_prompt
                    )


                    st.success(
                        "✅ Analysis completed!"
                    )


                    st.markdown(
                        "### 📚 Personalized Recommendations"
                    )


                    st.write(
                        response.text
                    )


                except Exception as e:

                    st.error(
                        f"Gemini Error: {e}"
                    )