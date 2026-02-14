# Pharmaceutical EDMS (Electronic Document Management System)

A compliant Electronic Document Management System (EDMS) for pharmaceutical organizations to manage controlled documents across their full lifecycle: **creation, review, approval, effectiveness, distribution, and controlled printing**.

## 1) Purpose and Scope
The system manages GxP-relevant documents used in pharmaceutical environments, including:
- SOPs
- Specifications
- Batch records and forms
- Validation protocols/reports
- Work instructions
- Policies and quality manuals

The platform is designed to support compliance with:
- **21 CFR Part 11** (electronic records and electronic signatures)
- **GAMP 5** principles (risk-based computerized system lifecycle)
- Applicable **GxP data integrity guidance** (e.g., ALCOA+ principles)

---

## 2) Core Workflow States
Each controlled document follows a configurable state machine:

1. **Draft / Creation**
   - Author creates document using approved template.
   - Metadata captured (document type, department, product/site, effective date target, etc.).

2. **Review**
   - Routed to one or more reviewers (e.g., SME, QA, Regulatory).
   - Review comments versioned and traceable.

3. **Approval**
   - Sequential or parallel approval based on configured workflow.
   - Electronic signatures applied with Part 11 controls.

4. **Effective**
   - Approved document becomes active/effective on controlled date.
   - Prior version automatically superseded and archived (read-only).

5. **Controlled Distribution & Print**
   - Access to effective versions by authorized roles.
   - Controlled print with unique copy number, watermark, print log, and reconciliation.

6. **Periodic Review / Revision / Retirement**
   - Scheduled review reminders.
   - Change control linkage for revisions.
   - Obsolete/retired handling with retention rules.

---

## 3) Functional Requirements

### 3.1 Document Creation and Versioning
- Template-based authoring for each document class.
- Auto document numbering based on configurable scheme.
- Version control (major/minor, status, revision history).
- Full comparison/diff between versions.

### 3.2 Review and Approval Management
- Configurable workflow builder (by document type/site/department).
- Dynamic routing based on role matrix.
- Due dates, reminders, escalations.
- Mandatory review comments for rejection/changes.

### 3.3 Role-Based Access Matrix
- Centralized **user-role-permission matrix** with least-privilege enforcement.
- Role examples: Author, Reviewer, Approver, QA Admin, Print Custodian, System Admin, Read-only User.
- Site/department/product-based segregation.
- Temporary delegation with validity period and audit trail.

### 3.4 Effective Document Control
- Only current effective version visible as default for operations.
- Obsolete versions clearly marked and restricted.
- Controlled acknowledgment/training linkage (optional integration).

### 3.5 21 CFR Part 11-Compliant E-Signatures
- Unique user ID and password re-authentication at signature.
- Signature meaning captured (reviewed, approved, authored, etc.).
- Timestamp, signer identity, reason/comment, and record linkage.
- Signature manifestation displayed with signed record.

### 3.6 21 CFR Part 11-Compliant Controlled Printing
- Print authorization by role and document status.
- Printed copies carry:
  - Unique print ID / copy number
  - Printed by, date/time, source version
  - "Controlled Copy" watermark
  - Expiry/revalidation marker where applicable
- Mandatory print issuance and return/destruction reconciliation log.
- Prevention/flagging of unauthorized reprints.

### 3.7 Search, Retrieval, and Reporting
- Advanced search by metadata, content, status, and lifecycle date.
- Dashboards for pending reviews/approvals, overdue tasks, effective documents.
- Audit and compliance reports exportable for inspections.

---

## 4) Compliance and Validation Requirements

### 4.1 21 CFR Part 11 Controls
- System validation evidence and traceability.
- Secure, computer-generated, time-stamped audit trails.
- Record protection, retention, and accurate/retrievable copies.
- Operational and authority checks.
- Device/session security and inactivity timeout.

### 4.2 GAMP 5 Alignment
- Risk-based validation approach.
- URS, FS/DS, configuration specifications.
- IQ/OQ/PQ support package and test evidence.
- Change control, incident/deviation, and CAPA linkage.

### 4.3 Data Integrity (ALCOA+)
- Attributable, Legible, Contemporaneous, Original, Accurate.
- Complete, Consistent, Enduring, and Available records.

---

## 5) Non-Functional Requirements
- High availability with backup and disaster recovery.
- Configurable retention and archival policies.
- Performance SLA for search and workflow operations.
- Multi-site support with timezone-aware timestamps.
- Scalable architecture and secure API integration.

---

## 6) Key Deliverables
- User Requirements Specification (URS).
- Validation Plan and Validation Summary Report.
- Role-permission matrix and workflow matrix.
- SOPs for EDMS operation, administration, and periodic review.
- Part 11 assessment checklist and traceability matrix.

---

## 7) Success Criteria
- 100% controlled documents routed through approved lifecycle.
- Full audit trail availability for inspections.
- Zero unauthorized document approval or printing events.
- Demonstrable Part 11 and GAMP-aligned validation package readiness.

---

## 8) Reference Implementation (Current Repository)

This repository now includes a lightweight Python domain implementation of core EDMS behaviors:
- Document creation and versioning
- Lifecycle transitions (Draft → Review → Approval → Effective)
- Role-based permission checks
- Part 11-style re-authentication at approval
- Controlled print issuance and reconciliation
- Audit-trail event capture per version

### Project structure
- `edms/models.py`: Domain entities and enums.
- `edms/system.py`: EDMS workflow service with state and permission enforcement.
- `tests/test_system.py`: Unit tests covering happy path and key control failures.

### Run tests
```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```
