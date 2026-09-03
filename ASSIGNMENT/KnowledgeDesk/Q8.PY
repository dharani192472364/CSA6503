from pathlib import Path

# ============================================================
# KNOWLEDGEDESK - Q8 RETRIEVAL EVALUATION DATASET
# ============================================================

# Always use the folder where Q8.py is located
BASE_DIR = Path(__file__).resolve().parent

DOCUMENTS_FOLDER = BASE_DIR / "documents"
EVALUATION_FILE = BASE_DIR / "q8_evaluation_questions.txt"


# ============================================================
# DOCUMENT DATA
# ============================================================

DOCUMENTS = {

    "HR_Leave_Policy_2026.txt": """
Document: HR Leave Policy 2026
Department: Human Resources
Page: 4

Employees with more than 3 years of service are entitled to 24 days
of annual leave per year.

Employees with less than 3 years of service are entitled to 18 days
of annual leave per year.

Annual leave requests should normally be submitted at least 3 working
days before the planned leave date.
""",

    "HR_Maternity_Policy_2026.txt": """
Document: HR Maternity Policy 2026
Department: Human Resources
Page: 7

Eligible employees are entitled to 26 weeks of maternity leave.

The maternity leave request must be submitted through the HR portal.
""",

    "HR_Travel_Policy_2026.txt": """
Document: HR Travel Policy 2026
Department: Human Resources
Page: 12

Employees travelling for approved business purposes can claim eligible
travel expenses.

Travel reimbursement claims must be submitted within 30 days of
completing the trip.
""",

    "IT_Password_Policy_2026.txt": """
Document: IT Password Policy 2026
Department: Information Technology
Page: 3

Employees must change their corporate password every 90 days.

Passwords must not be shared with other employees.
""",

    "IT_VPN_Policy_2026.txt": """
Document: IT VPN Policy 2026
Department: Information Technology
Page: 6

Remote employees must connect to the corporate VPN before accessing
internal systems.

Multi-factor authentication is required for VPN access.
""",

    "IT_Laptop_Policy_2026.txt": """
Document: IT Laptop Policy 2026
Department: Information Technology
Page: 9

Company laptops must be returned to the IT department when an employee
leaves the company.

Employees must report lost or stolen laptops to IT immediately.
""",

    "QUALITY_SOP_Inspection.txt": """
Document: Quality SOP Inspection
Department: Quality Assurance
Page: 5

All manufactured components must undergo final quality inspection
before shipment.

Inspection results must be recorded in the quality management system.
""",

    "QUALITY_SOP_Defect.txt": """
Document: Quality SOP Defect Handling
Department: Quality Assurance
Page: 8

Products with critical defects must be isolated and labelled as
non-conforming.

The quality manager must be notified of critical defects.
""",

    "SAFETY_SOP_Fire.txt": """
Document: Safety SOP Fire Emergency
Department: Safety
Page: 2

During a fire emergency, employees must use the nearest safe emergency
exit.

Employees must not use elevators during a fire emergency.
""",

    "SAFETY_SOP_Chemical.txt": """
Document: Safety SOP Chemical Spill
Department: Safety
Page: 11

Chemical spills must be reported immediately to the safety officer.

Employees should avoid direct contact with unknown chemicals.
""",

    "PROJECT_REPORT_Alpha.txt": """
Document: Project Alpha Report
Department: Engineering Projects
Page: 18

Project Alpha completed its prototype testing phase in June 2026.

The prototype achieved 94 percent of the defined functional test
requirements.
""",

    "COMPLIANCE_Data_Retention.txt": """
Document: Compliance Data Retention Policy
Department: Compliance
Page: 14

Business records must be retained according to the company's approved
retention schedule.

Employees must not permanently delete records that are subject to a
legal hold.
"""
}


# ============================================================
# 12 EVALUATION QUESTIONS
# ============================================================

QUESTIONS = [

    (
        "How many annual leave days are provided to employees with more than three years of service?",
        "HR_Leave_Policy_2026.txt"
    ),

    (
        "How many weeks of maternity leave are eligible employees entitled to?",
        "HR_Maternity_Policy_2026.txt"
    ),

    (
        "Within how many days must travel reimbursement claims be submitted?",
        "HR_Travel_Policy_2026.txt"
    ),

    (
        "How often must employees change their corporate password?",
        "IT_Password_Policy_2026.txt"
    ),

    (
        "What must remote employees use before accessing internal systems?",
        "IT_VPN_Policy_2026.txt"
    ),

    (
        "What should happen to a company laptop when an employee leaves?",
        "IT_Laptop_Policy_2026.txt"
    ),

    (
        "What must happen before manufactured components are shipped?",
        "QUALITY_SOP_Inspection.txt"
    ),

    (
        "What should be done with products that have critical defects?",
        "QUALITY_SOP_Defect.txt"
    ),

    (
        "What should employees do during a fire emergency?",
        "SAFETY_SOP_Fire.txt"
    ),

    (
        "Who must be notified immediately about a chemical spill?",
        "SAFETY_SOP_Chemical.txt"
    ),

    (
        "What percentage of functional test requirements did Project Alpha achieve?",
        "PROJECT_REPORT_Alpha.txt"
    ),

    (
        "What should employees do with records subject to a legal hold?",
        "COMPLIANCE_Data_Retention.txt"
    )
]


# ============================================================
# CREATE DOCUMENTS IN KNOWLEDGEDESK/DOCUMENTS
# ============================================================

DOCUMENTS_FOLDER.mkdir(exist_ok=True)

for filename, content in DOCUMENTS.items():

    file_path = DOCUMENTS_FOLDER / filename

    file_path.write_text(
        content.strip(),
        encoding="utf-8"
    )


# ============================================================
# CREATE EVALUATION QUESTIONS FILE
# ============================================================

with EVALUATION_FILE.open("w", encoding="utf-8") as file:

    file.write("KNOWLEDGEDESK - Q8 RETRIEVAL EVALUATION DATASET\n")
    file.write("=" * 70 + "\n\n")

    for number, (question, source) in enumerate(QUESTIONS, start=1):

        file.write(f"{number}. Question: {question}\n")
        file.write(f"   Correct Source: {source}\n\n")


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("=" * 70)
print("KNOWLEDGEDESK - Q8 RETRIEVAL EVALUATION DATASET")
print("=" * 70)

print(f"\nKnowledgeDesk folder : {BASE_DIR}")
print(f"Documents folder    : {DOCUMENTS_FOLDER}")

print(f"\nDocuments created   : {len(DOCUMENTS)}")
print(f"Questions created   : {len(QUESTIONS)}")

print("\nEvaluation Questions")
print("-" * 70)

for number, (question, source) in enumerate(QUESTIONS, start=1):

    print(f"\n{number}. {question}")
    print(f"   Correct Source: {source}")


print("\n" + "=" * 70)
print("DATASET CREATION COMPLETED")
print("=" * 70)