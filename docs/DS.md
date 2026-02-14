# DS - Design Specification

| DS_ID | Maps To FS | Design |
|---|---|---|
| DS-001 | FS-001 | `backend/auth/rbac.py` provides role guard patterns; services validate role before mutation. |
| DS-002 | FS-002 | `backend/workflow/state_machine.py` defines canonical states + allowed transition map. |
| DS-003 | FS-003 | `backend/signatures/models.py` and `service.py` persist electronic signature linked to doc + version and then approve workflow. |
| DS-004 | FS-004 | `backend/audit/models.py` adds SQLAlchemy update/delete listeners to enforce append-only immutability; `log_event` called by all services. |
| DS-005 | FS-005 | `backend/documents/models.py` has `locked` flag set when state reaches Approved; service rejects further versioning edits. |
| DS-006 | FS-006 | `backend/auth/service.py` implements PBKDF2 password hashing, HMAC JWT, token validation, and session revocation checks. |
| DS-007 | FS-007 | `backend/documents/service.py` computes SHA-256 checksums for document versions and writes actor+timestamp audit metadata. |
