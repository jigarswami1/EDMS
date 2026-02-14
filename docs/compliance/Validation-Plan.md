# Validation Plan (VP) — EDMS

## 1. Purpose
Define the validation strategy for EDMS in alignment with GAMP 5 and risk-based testing principles, demonstrating fitness for intended use and compliance with applicable regulations.

## 2. Scope
Includes infrastructure qualification interfaces, application configuration, security roles, document lifecycle workflows, e-signatures, audit trails, print controls, integrations, migration (if applicable), and reporting.

## 3. References
- GAMP 5 (Second Edition) lifecycle framework
- 21 CFR Part 11
- Internal Quality Management System procedures for CSV/CSA

## 4. Validation Strategy (GAMP 5 Lifecycle)
### 4.1 Concept / Planning
- Define intended use and critical quality/data integrity attributes.
- Perform supplier and solution assessment.
- Classify functionality by risk and GAMP category as applicable.

### 4.2 Project / Specification
- Baseline requirements (URS) and map to functional/design specifications.
- Define acceptance criteria and traceability approach.

### 4.3 Build / Configuration
- Configure EDMS modules with controlled configuration records.
- Apply change control and peer review for configuration changes.

### 4.4 Verification / Testing
- Execute risk-based testing with emphasis on high-risk, high-impact controls.
- Include negative/challenge tests for signature bypass, unauthorized access, and workflow control failures.
- Test levels:
  - **IQ (as applicable):** environment readiness and installation evidence.
  - **OQ:** functional verification of configured requirements.
  - **PQ/UAT:** process use by trained business users in representative scenarios.

### 4.5 Release / Operation
- Resolve or justify deviations.
- Approve validation summary and release authorization.
- Transition to operational monitoring and periodic review.

## 5. Risk Management Approach
- Use a documented risk assessment to rank requirements by patient/product quality/data integrity impact and detectability.
- Derive test depth from risk ranking:
  - **High Risk:** detailed scripted positive/negative tests with objective evidence.
  - **Medium Risk:** scripted or structured exploratory tests with defined acceptance criteria.
  - **Low Risk:** targeted verification and supplier leverage where justified.

## 6. Deliverables
- Validation Plan (this document)
- Risk Assessment
- URS / FS / DS (as applicable)
- Traceability Matrix
- IQ/OQ/PQ protocols and executed evidence
- Deviation log and CAPA linkage
- Validation Summary Report (VSR)

## 7. Roles and Responsibilities
- **System Owner:** intended use definition, business acceptance.
- **Quality Assurance:** compliance oversight, approval of lifecycle records.
- **Validation Lead:** planning, coordination, traceability, reporting.
- **IT/System Admin:** environment and access control implementation.
- **Business SMEs:** user acceptance and process validation.

## 8. Entry and Exit Criteria
### Entry Criteria
- Approved URS and risk assessment
- Defined test environment and test accounts
- Approved protocols

### Exit Criteria
- Required tests executed with acceptable pass rate
- Critical/high deviations resolved or formally accepted
- Traceability complete (requirements to tests)
- VSR approved by QA and System Owner

## 9. Deviation and Change Control
All deviations identified during testing will be logged, investigated for impact, and resolved via defect management and/or CAPA. Post-release changes follow formal change control with risk-based revalidation impact assessment.
