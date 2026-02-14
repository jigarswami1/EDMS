# Requirements Traceability Matrix (RTM)

## Purpose
Map URS requirements to design modules and planned verification tests.

## Matrix
| URS ID | Requirement Summary | Design Module(s) | Planned Test Case ID(s) | Verification Level |
|---|---|---|---|---|
| URS-DOC-001 | Unique doc number + immutable revision | `backend/documents` | TC-DOC-001, TC-DOC-002 | OQ |
| URS-DOC-002 | Mandatory metadata before workflow | `backend/documents`, `backend/workflows` | TC-DOC-003, TC-WKF-001 | OQ |
| URS-DOC-003 | Version history + superseded read-only | `backend/documents` | TC-DOC-004 | OQ |
| URS-DOC-006 | Periodic review due dates | `backend/workflows`, `backend/reports` | TC-REV-001, TC-REV-002 | OQ/PQ |
| URS-SIG-001 | Signature manifestation fields | `backend/signatures` | TC-SIG-001 | OQ |
| URS-SIG-002 | Two-factor signing control | `backend/signatures`, `backend/auth` | TC-SIG-002, TC-AUTH-002 | OQ |
| URS-SIG-003 | Signature-record binding/invalidation | `backend/signatures`, `backend/documents` | TC-SIG-003 | OQ |
| URS-SIG-004 | No proxy signing / non-repudiation | `backend/signatures`, `backend/auth` | TC-SIG-004, TC-AUTH-003 | OQ |
| URS-PRN-001 | Controlled print watermark/metadata | `backend/printing` | TC-PRN-001, TC-PRN-002 | OQ |
| URS-PRN-003 | Print audit logging | `backend/printing`, `backend/audit` | TC-PRN-003, TC-AUD-003 | OQ |
| URS-WKF-001 | Routing by site/dept/doc type | `backend/workflows` | TC-WKF-002, TC-WKF-003 | OQ/PQ |
| URS-WKF-004 | Self-approval prevention | `backend/workflows`, `backend/auth` | TC-WKF-004 | OQ |
| URS-AUD-001 | Secure timestamped audit trail | `backend/audit` | TC-AUD-001 | OQ |
| URS-AUD-002 | Audit immutability | `backend/audit` | TC-AUD-002 | OQ |
| URS-SEC-001 | Role-based access control | `backend/auth` | TC-AUTH-001 | OQ |
| URS-RET-001 | Retention by class/region | `backend/documents`, `backend/reports` | TC-RET-001, TC-RET-002 | OQ/PQ |

## Notes
- Test case identifiers are planning placeholders and should be formalized in approved protocols.
- Additional non-functional requirements (performance, backup/recovery) should be mapped in a supplemental RTM where required.
