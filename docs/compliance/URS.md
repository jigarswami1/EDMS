# User Requirements Specification (URS)

## Document Control
- **Document ID:** URS-EDMS-001
- **System:** Electronic Document Management System (EDMS)
- **Regulatory Context:** 21 CFR Part 11, GMP/GDP, data integrity (ALCOA+)
- **Version:** 0.1 (Draft)

## Purpose
Define user requirements for the EDMS to ensure compliant management of controlled documents, electronic signatures, print controls, workflow approvals, and archival/retention.

## Scope
This URS applies to document authoring, review, approval, issuance, training acknowledgement, change control integration, controlled printing, periodic review, and retirement of controlled documents across sites and departments.

## URS Requirements

### 1) Document Control Requirements
| Requirement ID | Requirement Statement | Priority | Risk Category |
|---|---|---|---|
| URS-DOC-001 | The system shall assign a unique document number and immutable revision identifier for each controlled document. | High | Compliance |
| URS-DOC-002 | The system shall enforce metadata completion (site, department, document type, owner, effective date, review period) before routing for approval. | High | Compliance |
| URS-DOC-003 | The system shall maintain version history and provide read-only access to superseded versions. | High | Compliance |
| URS-DOC-004 | The system shall prevent concurrent conflicting edits and track check-in/check-out events. | Medium | Integrity |
| URS-DOC-005 | The system shall support document templates by document type (e.g., SOP, WI, Form, Policy). | Medium | Operational |
| URS-DOC-006 | The system shall enforce periodic review due dates based on configurable intervals per document type. | High | Compliance |

### 2) Electronic Signature Requirements
| Requirement ID | Requirement Statement | Priority | Risk Category |
|---|---|---|---|
| URS-SIG-001 | The system shall capture legally binding electronic signatures including printed name, date/time (with timezone), meaning of signature, and unique user ID. | High | Compliance |
| URS-SIG-002 | The system shall require two distinct identification components at signing (authenticated session + re-entry of credential or step-up authentication). | High | Compliance |
| URS-SIG-003 | The system shall cryptographically bind signatures to signed records and invalidate signatures when content changes post-signature. | High | Integrity |
| URS-SIG-004 | The system shall prevent users from signing on behalf of another user and enforce non-repudiation controls. | High | Compliance |
| URS-SIG-005 | The system shall retain signature manifestation in both on-screen view and printed/exported copies. | High | Compliance |

### 3) Printing and Distribution Requirements
| Requirement ID | Requirement Statement | Priority | Risk Category |
|---|---|---|---|
| URS-PRN-001 | The system shall mark printed controlled copies with status watermark (e.g., “Controlled Copy” or “Uncontrolled when printed”), copy number, and print timestamp. | High | Compliance |
| URS-PRN-002 | The system shall restrict printing rights by role and document status. | Medium | Compliance |
| URS-PRN-003 | The system shall log all print events in an audit trail with user, document revision, destination, and reason code (if configured). | High | Integrity |

### 4) Workflow and Authority Requirements
| Requirement ID | Requirement Statement | Priority | Risk Category |
|---|---|---|---|
| URS-WKF-001 | The system shall enforce predefined routing rules by site, department, and document type. | High | Compliance |
| URS-WKF-002 | The system shall require independent reviewer/approver segregation of duties where configured. | High | Compliance |
| URS-WKF-003 | The system shall support parallel and sequential approval steps with quorum logic. | Medium | Operational |
| URS-WKF-004 | The system shall prevent self-approval where role policy disallows it. | High | Compliance |

### 5) Audit Trail and Data Integrity Requirements
| Requirement ID | Requirement Statement | Priority | Risk Category |
|---|---|---|---|
| URS-AUD-001 | The system shall generate secure, computer-generated, time-stamped audit trails for create/read/update/delete/approve/print actions on GxP records. | High | Compliance |
| URS-AUD-002 | Audit trail entries shall be non-modifiable by end users and protected from unauthorized alteration. | High | Integrity |
| URS-AUD-003 | The system shall include previous and new values for metadata changes where applicable. | High | Integrity |
| URS-AUD-004 | The system shall provide query and export of audit trails for inspections. | Medium | Compliance |

### 6) Security and Access Requirements
| Requirement ID | Requirement Statement | Priority | Risk Category |
|---|---|---|---|
| URS-SEC-001 | The system shall provide role-based access control with least privilege principles. | High | Compliance |
| URS-SEC-002 | The system shall enforce password/session policies per corporate security standards and applicable regulations. | High | Compliance |
| URS-SEC-003 | The system shall support periodic access review and deprovisioning controls for terminated/transferred users. | High | Compliance |

### 7) Retention and Archival Requirements
| Requirement ID | Requirement Statement | Priority | Risk Category |
|---|---|---|---|
| URS-RET-001 | The system shall retain records and signatures for configured retention periods based on document type and region. | High | Compliance |
| URS-RET-002 | The system shall prevent deletion of records under retention or legal hold. | High | Compliance |
| URS-RET-003 | The system shall support secure archival and controlled retrieval with complete readability over retention period. | High | Integrity |

## Acceptance Criteria Summary
Each URS requirement will be verified through risk-based testing (IQ/OQ/PQ aligned where applicable), traceability in the matrix, and documented objective evidence in validation deliverables.
