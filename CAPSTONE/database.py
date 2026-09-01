import sqlite3
from datetime import datetime


DB_NAME = "study_system.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return sqlite3.connect(DB_NAME)


# =========================================================
# ADD MISSING COLUMNS
# =========================================================

def add_column_if_missing(cursor, table, column, definition):

    cursor.execute(f"PRAGMA table_info({table})")

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if column not in columns:

        cursor.execute(
            f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
        )


# =========================================================
# CREATE TABLES
# =========================================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================================
    # USERS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            full_name TEXT NOT NULL
        )
    """)


    # =====================================================
    # QUIZ RESULTS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            subject TEXT NOT NULL,

            topic TEXT NOT NULL,

            score REAL NOT NULL,

            total_questions INTEGER NOT NULL,

            correct_answers INTEGER NOT NULL,

            quiz_date TEXT NOT NULL
        )
    """)


    # =====================================================
    # STUDY PLANS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_plans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            subjects TEXT,

            hours INTEGER,

            goal TEXT,

            weak_subjects TEXT,

            exam_date TEXT,

            plan TEXT,

            created_at TEXT
        )
    """)


    # =====================================================
    # TUTOR HISTORY
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tutor_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            subject TEXT,

            question TEXT,

            answer TEXT,

            created_at TEXT
        )
    """)


    # =====================================================
    # DATABASE MIGRATION
    # =====================================================

    # STUDY_PLANS
    add_column_if_missing(
        cursor,
        "study_plans",
        "user_id",
        "INTEGER"
    )

    add_column_if_missing(
        cursor,
        "study_plans",
        "subjects",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "study_plans",
        "hours",
        "INTEGER"
    )

    add_column_if_missing(
        cursor,
        "study_plans",
        "goal",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "study_plans",
        "weak_subjects",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "study_plans",
        "exam_date",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "study_plans",
        "plan",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "study_plans",
        "created_at",
        "TEXT"
    )


    # TUTOR HISTORY
    add_column_if_missing(
        cursor,
        "tutor_history",
        "user_id",
        "INTEGER"
    )

    add_column_if_missing(
        cursor,
        "tutor_history",
        "subject",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "tutor_history",
        "question",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "tutor_history",
        "answer",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "tutor_history",
        "created_at",
        "TEXT"
    )


    # QUIZ RESULTS
    add_column_if_missing(
        cursor,
        "quiz_results",
        "user_id",
        "INTEGER"
    )

    add_column_if_missing(
        cursor,
        "quiz_results",
        "subject",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "quiz_results",
        "topic",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "quiz_results",
        "score",
        "REAL"
    )

    add_column_if_missing(
        cursor,
        "quiz_results",
        "total_questions",
        "INTEGER"
    )

    add_column_if_missing(
        cursor,
        "quiz_results",
        "correct_answers",
        "INTEGER"
    )

    add_column_if_missing(
        cursor,
        "quiz_results",
        "quiz_date",
        "TEXT"
    )


    conn.commit()

    conn.close()


# =========================================================
# REGISTER USER
# =========================================================

def register_user(username, password, full_name):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (
                username,
                password,
                full_name
            )
            VALUES (?, ?, ?)
        """, (
            username,
            password,
            full_name
        ))

        conn.commit()

        user_id = cursor.lastrowid

        conn.close()

        return user_id

    except sqlite3.IntegrityError:

        conn.close()

        return None


# =========================================================
# LOGIN USER
# =========================================================

def login_user(username, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            full_name
        FROM users
        WHERE username = ?
        AND password = ?
    """, (
        username,
        password
    ))

    user = cursor.fetchone()

    conn.close()

    return user


# =========================================================
# GET USER
# =========================================================

def get_user(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            full_name
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return user


# =========================================================
# SAVE QUIZ RESULT
# =========================================================

def save_quiz_result(
    user_id,
    subject,
    topic,
    percentage,
    total_questions,
    correct_answers
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quiz_results
        (
            user_id,
            subject,
            topic,
            score,
            total_questions,
            correct_answers,
            quiz_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        subject,
        topic,
        percentage,
        total_questions,
        correct_answers,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    conn.commit()

    conn.close()


# =========================================================
# GET QUIZ RESULTS
# =========================================================

def get_quiz_results(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            user_id,
            subject,
            topic,
            score,
            total_questions,
            correct_answers,
            quiz_date
        FROM quiz_results
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    results = cursor.fetchall()

    conn.close()

    return results


# =========================================================
# SAVE STUDY PLAN
# =========================================================

def save_study_plan(
    user_id,
    subjects,
    hours,
    goal,
    weak_subjects,
    exam_date,
    plan
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO study_plans
        (
            user_id,
            subjects,
            hours,
            goal,
            weak_subjects,
            exam_date,
            plan,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        subjects,
        hours,
        goal,
        weak_subjects,
        str(exam_date),
        plan,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    conn.commit()

    conn.close()


# =========================================================
# SAVE AI TUTOR HISTORY
# =========================================================

def save_tutor_history(
    user_id,
    subject,
    question,
    answer
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tutor_history
        (
            user_id,
            subject,
            question,
            answer,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        subject,
        question,
        answer,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    conn.commit()

    conn.close()