from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_FOLDER = BASE_DIR / "documents"

DOCUMENTS_FOLDER.mkdir(exist_ok=True)


documents = {

"HR_Leave_Policy_2026.txt": """
HR LEAVE POLICY 2026

Document: HR Leave Policy 2026
Department: Human Resources
Effective Date: 1 January 2026
Source Page: Page 4

1. Annual Leave Policy

Employees are entitled to annual leave based on their length of service with the organization.

Employees with less than 3 years of service are entitled to 18 days of annual leave per year.

Employees with more than 3 years of service are entitled to 24 days of annual leave per year.

Annual leave requests must be submitted through the employee portal.

Employees should normally submit annual leave requests at least 3 working days before the planned leave date.

Managers are responsible for reviewing leave requests and confirming operational coverage.

Employees should check their available leave balance before submitting a request.

Leave approval depends on staffing requirements and business continuity.

2. Sick Leave

Employees who are unable to attend work because of illness should notify their reporting manager as soon as possible.

Supporting medical documentation may be required according to company procedures.

3. Public Holidays

Public holidays are handled according to the organization's annual holiday calendar.

4. Leave Records

The Human Resources department maintains employee leave records.

Employees can review their approved leave through the employee portal.

5. Responsibilities

Employees must provide accurate leave information.

Managers must review requests fairly and maintain adequate staffing.

Human Resources maintains the official leave records.

Source Page: Page 4
""",

"HR_Maternity_Policy_2026.txt": """
HR MATERNITY POLICY 2026

Document: HR Maternity Policy 2026
Department: Human Resources
Effective Date: 1 January 2026
Source Page: Page 5

1. Maternity Leave

Eligible employees are entitled to maternity leave according to the organization's maternity leave policy.

The standard maternity leave entitlement is 26 weeks for eligible employees.

Employees should notify Human Resources and their manager before the expected start of maternity leave.

Employees may be required to provide supporting medical documentation.

2. Leave Application

Maternity leave applications should be submitted through the employee portal.

Employees should provide the expected delivery date when submitting the application.

Human Resources verifies eligibility and records the approved leave period.

3. Return to Work

Employees should communicate their expected return date to their manager and Human Resources.

Any extension of leave must be requested through the appropriate HR procedure.

4. Benefits

Eligible employees continue to receive applicable employment benefits during approved maternity leave according to company rules.

5. Responsibilities

Human Resources maintains maternity leave records.

Managers should support employees during the leave process.

Employees should provide accurate information and required documentation.

Source Page: Page 5
""",

"HR_Travel_Policy_2026.txt": """
HR TRAVEL POLICY 2026

Document: HR Travel Policy 2026
Department: Human Resources
Effective Date: 1 January 2026
Source Page: Page 6

1. Business Travel

Employees travelling for official business must obtain the required approval before making travel arrangements.

Travel requests should be submitted through the company travel system.

2. Travel Expense Claims

Employees must submit travel expense claims through the employee expense portal.

Expense claims should normally be submitted within 10 working days after completion of the business trip.

Receipts and supporting documents must be attached to the claim.

3. Transportation

Reasonable transportation expenses incurred for approved business travel may be reimbursed.

Employees should select economical travel options where practical.

4. Accommodation

Hotel expenses for approved business trips may be reimbursed within applicable company limits.

Employees should use approved accommodation providers where required.

5. Meals

Reasonable meal expenses may be reimbursed according to company travel limits.

6. Approval

The employee's manager is responsible for approving business travel.

Finance reviews submitted expense claims before reimbursement.

7. Record Keeping

Employees should retain original receipts and supporting documents until the claim has been processed.

Source Page: Page 6
""",

"IT_Password_Policy_2026.txt": """
IT PASSWORD POLICY 2026

Document: IT Password Policy 2026
Department: Information Technology
Effective Date: 1 January 2026
Source Page: Page 7

1. Password Requirements

All employees must maintain strong passwords for company accounts.

Passwords must contain at least 12 characters.

Passwords should include a combination of uppercase letters, lowercase letters, numbers, and special characters.

Employees must not reuse company passwords for personal accounts.

2. Password Protection

Employees must never share their passwords with another person.

Passwords must not be written in publicly visible locations.

Employees should use the approved company password manager when storing credentials.

3. Password Changes

Employees must change their password when requested by the IT department.

Passwords must be changed immediately if an employee suspects that credentials have been compromised.

4. Account Security

Multi-factor authentication should be enabled for supported company services.

Employees must lock their workstation when leaving their desk.

5. Reporting

Suspected password compromise must be reported to the IT help desk immediately.

6. Responsibilities

Employees are responsible for protecting their account credentials.

The IT department monitors account security and assists with password recovery.

Source Page: Page 7
""",

"IT_VPN_Policy_2026.txt": """
IT VPN POLICY 2026

Document: IT VPN Policy 2026
Department: Information Technology
Effective Date: 1 January 2026
Source Page: Page 8

1. Remote Access

Employees working outside the company network must use the approved corporate VPN when accessing internal resources.

The VPN provides encrypted communication between the employee device and company network.

2. VPN Authentication

Employees must authenticate using their corporate username and password.

Multi-factor authentication may be required.

Employees must not share VPN credentials with other users.

3. Approved Devices

Only company-managed devices should be used for access to protected internal systems.

Personal devices may be restricted from accessing sensitive company resources.

4. VPN Usage

Employees should connect to the VPN before accessing internal applications.

The VPN connection should remain active while sensitive internal resources are being accessed.

5. Security

Employees should avoid accessing company resources from unsecured public networks.

Lost or stolen devices must be reported to IT immediately.

6. Troubleshooting

Employees experiencing VPN problems should contact the IT help desk.

IT support may verify the employee's account and device configuration.

Source Page: Page 8
""",

"IT_Laptop_Policy_2026.txt": """
IT LAPTOP POLICY 2026

Document: IT Laptop Policy 2026
Department: Information Technology
Effective Date: 1 January 2026
Source Page: Page 9

1. Company Laptop

Company laptops are provided to employees for authorized business activities.

Employees are responsible for protecting assigned equipment.

2. Laptop Security

Employees must use the assigned security controls and login credentials.

The laptop must be locked whenever it is unattended.

Employees must not install unauthorized software.

3. Damage

Any accidental damage or technical issue should be reported to the IT department.

Employees should not attempt unauthorized hardware repairs.

4. Return of Laptop

Employees must return the company laptop when their employment ends.

Laptops must also be returned when requested by the IT department or when an employee changes to a role that no longer requires the equipment.

The laptop should be returned together with assigned accessories such as the charger and docking equipment.

5. Asset Records

IT maintains records of company laptop assignments.

Employees should verify the asset details recorded against their assigned equipment.

6. Responsibilities

Employees are responsible for reasonable care of company equipment.

IT is responsible for maintenance and asset management.

Source Page: Page 9
""",

"QUALITY_SOP_Inspection.txt": """
QUALITY SOP - INSPECTION

Document: Quality SOP Inspection
Department: Quality Assurance
Effective Date: 1 January 2026
Source Page: Page 10

1. Purpose

This procedure defines the standard process for inspecting engineering work and delivered products.

2. Inspection Preparation

Inspectors must review the applicable specifications and inspection checklist before beginning an inspection.

Required measuring instruments must be available and calibrated.

3. Inspection Procedure

The inspector should verify the product identification.

The inspector must compare the product against approved specifications.

Measurements should be recorded on the inspection checklist.

Visual defects must be documented.

4. Inspection Results

Inspection results should be classified as accepted, rejected, or requiring additional review.

Any deviation from specification must be recorded.

5. Documentation

Inspection records must contain the inspection date, inspector identification, product information, measurements, and observations.

6. Corrective Action

Rejected items should be referred for corrective action.

The quality team should track corrective actions until closure.

7. Responsibilities

Inspectors are responsible for accurate inspection records.

Quality managers review inspection results and monitor recurring problems.

Source Page: Page 10
""",

"QUALITY_SOP_Defect.txt": """
QUALITY SOP - DEFECT MANAGEMENT

Document: Quality SOP Defect Management
Department: Quality Assurance
Effective Date: 1 January 2026
Source Page: Page 11

1. Purpose

This procedure defines how defects identified during engineering operations should be recorded, classified, and resolved.

2. Defect Classification

Defects are classified according to severity and potential impact.

Minor defects may be corrected during normal processing.

Major defects require documented corrective action.

Critical defects require immediate escalation.

3. Critical Defects

Critical defects must be reported to the quality manager immediately.

Affected products or processes should be placed on hold when necessary.

The quality team must investigate the root cause.

4. Corrective Action

Corrective actions must identify the cause of the defect.

Actions should include responsible personnel and expected completion dates.

5. Verification

Completed corrective actions must be verified by authorized quality personnel.

6. Records

Defect records should include defect description, severity, affected item, investigation results, corrective action, and closure information.

7. Continuous Improvement

Recurring defects should be reviewed to identify opportunities for process improvement.

Source Page: Page 11
""",

"SAFETY_SOP_Fire.txt": """
SAFETY SOP - FIRE EMERGENCY

Document: Safety SOP Fire Emergency
Department: Safety
Effective Date: 1 January 2026
Source Page: Page 12

1. Purpose

This procedure provides instructions for employees during a workplace fire emergency.

2. Immediate Response

Employees who discover a fire must raise the alarm immediately.

The emergency response team should be notified.

Employees must leave the affected area using the nearest safe emergency exit.

3. Evacuation

Employees must follow designated evacuation routes.

Elevators must not be used during a fire emergency.

Employees should proceed to the designated assembly point.

4. Emergency Assistance

Employees should assist visitors and persons requiring support when it is safe to do so.

Employees must not re-enter the building until authorized personnel declare the area safe.

5. Fire Extinguishers

Only trained employees should attempt to use fire extinguishers.

Employees should not take unnecessary risks.

6. Reporting

All fire incidents and near misses must be reported according to the safety reporting procedure.

7. Responsibilities

The safety team coordinates emergency response activities.

Employees must follow evacuation instructions and emergency announcements.

Source Page: Page 12
""",

"SAFETY_SOP_Chemical.txt": """
SAFETY SOP - CHEMICAL SPILL

Document: Safety SOP Chemical Spill
Department: Safety
Effective Date: 1 January 2026
Source Page: Page 13

1. Purpose

This procedure defines the required response to accidental chemical spills in the workplace.

2. Immediate Action

Employees who discover a chemical spill should move away from the affected area.

The incident must be reported to the laboratory or safety supervisor.

Untrained employees must not attempt to clean hazardous chemical spills.

3. Area Control

The affected area should be isolated when possible.

Warning signs should be placed around the contaminated area.

Access should be restricted until the spill has been assessed.

4. Personal Protection

Appropriate personal protective equipment must be used by trained personnel handling the spill.

The safety data sheet should be consulted for information about the chemical.

5. Spill Response

Trained personnel should follow the approved chemical spill response procedure.

Spill containment materials should be used according to the chemical hazard.

6. Medical Emergency

If a person is exposed to a hazardous chemical, emergency medical assistance must be requested.

Exposure incidents must be reported to the safety department.

7. Documentation

The chemical spill must be documented including the chemical involved, location, estimated quantity, response actions, and affected personnel.

Source Page: Page 13
""",

"PROJECT_REPORT_Alpha.txt": """
PROJECT ALPHA - ENGINEERING PROJECT REPORT

Document: Project Alpha Report
Department: Engineering
Project Period: January 2026 - June 2026
Source Page: Page 14

1. Project Overview

Project Alpha was developed to improve the efficiency of an engineering workflow.

The project team analyzed the existing process and identified several operational bottlenecks.

2. Baseline

The original process required an average processing time of 50 minutes per task.

The team collected performance measurements before implementing the improvement.

3. Improvement

After optimization, the average processing time was reduced to 40 minutes per task.

The improvement was achieved through workflow automation and process redesign.

4. Performance Improvement

The reduction from 50 minutes to 40 minutes represents a 20 percent improvement in processing time.

The project therefore achieved a measured improvement of 20 percent.

5. Results

The optimized workflow reduced repetitive manual activities.

The engineering team reported improved consistency in task completion.

6. Monitoring

Project performance should continue to be monitored using processing time, throughput, and error-rate indicators.

7. Conclusion

Project Alpha demonstrated that workflow automation and process redesign can improve operational efficiency.

Source Page: Page 14
""",

"COMPLIANCE_Data_Retention.txt": """
COMPLIANCE - DATA RETENTION AND LEGAL HOLD

Document: Data Retention and Legal Hold Policy
Department: Compliance
Effective Date: 1 January 2026
Source Page: Page 15

1. Purpose

This policy defines requirements for retaining company records and preserving information subject to legal hold.

2. Standard Retention

Business records must be retained according to the applicable company retention schedule.

Different record categories may have different retention periods.

3. Legal Hold

When a legal hold is issued, employees must preserve relevant records until the legal hold is formally released.

A legal hold overrides normal deletion schedules for information covered by the hold.

4. Duration

Records subject to an active legal hold must be retained for the entire duration of the legal hold.

Employees must not delete, modify, or destroy records covered by an active legal hold.

5. Notification

The Compliance or Legal department communicates legal hold instructions to affected employees.

Employees must acknowledge receipt when required.

6. Electronic Records

Emails, documents, messages, and other electronic information may be subject to legal hold requirements.

Employees must preserve relevant electronic records.

7. Release

Records may return to the normal retention schedule only after the legal hold has been formally released.

8. Responsibilities

Employees must comply with legal hold instructions.

Managers must support compliance activities.

The Legal and Compliance teams maintain legal hold records and provide guidance.

Source Page: Page 15
"""
}


# ============================================================
# WRITE DOCUMENTS
# ============================================================

print("=" * 70)
print("GENERATING Q8 EXPANDED KNOWLEDGEDESK DOCUMENTS")
print("=" * 70)

for filename, content in documents.items():

    file_path = DOCUMENTS_FOLDER / filename

    file_path.write_text(
        content.strip(),
        encoding="utf-8"
    )

    word_count = len(
        content.split()
    )

    print(
        f"{filename:<40} {word_count:>4} words"
    )

print("=" * 70)

print()
print(
    "Generated documents:",
    len(documents)
)

print(
    "Location:",
    DOCUMENTS_FOLDER
)

print()
print(
    "Q8 documents generated successfully."
)

print("=" * 70)