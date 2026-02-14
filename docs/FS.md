# FS - Functional Specification

| FS_ID | Maps To URS | Functional Requirement |
|---|---|---|
| FS-001 | URS-001 | RBAC checks in service layer block unauthorized roles from protected actions. |
| FS-002 | URS-002 | State machine validates transitions and rejects non-allowed paths. |
| FS-003 | URS-003 | Electronic signature stores signer, meaning, and deterministic signature hash bound to document/version. |
| FS-004 | URS-004 | Audit service auto-logs create/login/workflow/signature/version events; audit rows cannot be updated/deleted. |
| FS-005 | URS-005 | Document lock flag is set on approval; versioning and most transitions are blocked afterward. |
| FS-006 | URS-006 | Password policy (min length + PBKDF2 hash), JWT token issuance, and revocable user session control are implemented. |
| FS-007 | URS-007 | Version checksum, UTC timestamps, actor attribution, and traceable record IDs are enforced. |
