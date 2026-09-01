import ollama

schema = """
Database: College

Table: Students
student_id
name
department
marks

Table: Courses
course_id
course_name
credits
"""

task = input(
    "Enter database task: "
)

prompt = f"""
Generate SQL using the following database information.

{schema}

Task:
{task}

Rules:
1. Use only the provided tables.
2. Use valid SQL.
3. Return only the SQL query.
"""

result = ollama.generate(
    model="llama3.2",
    prompt=prompt
)

print("\nSQL Query:")
print(result["response"])