# GxP / 21 CFR Part 11 EDMS Backend

Audit-ready EDMS backend using FastAPI + SQLAlchemy with enforceable compliance controls and validation evidence generation.

## Features
- Role-based access control: Author, Reviewer, Approver, Admin
- Workflow enforcement: Draft → Review → Approved → Archived
- Electronic signatures bound to document/version/meaning
- Immutable append-only audit trail with UTC timestamps
- Record lock after approval
- Password hashing (PBKDF2) + JWT session control
- ALCOA+ data integrity controls via attribution, checksums, and timestamps

## Project layout
- `backend/auth`: users, roles, password/JWT/session services, RBAC
- `backend/documents`: document/version entities and lifecycle logic
- `backend/workflow`: validated transition state machine
- `backend/audit`: immutable audit models and logging service
- `backend/signatures`: electronic signature model/service
- `backend/api`: FastAPI routes
- `backend/db`: SQLAlchemy base/session
- `docs`: URS/FS/DS and traceability matrix
- `tests`: compliance-focused pytest suite
- `scripts/generate_validation_evidence.py`: creates validation outputs

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/test_auth_part11.py tests/test_workflow_enforcement.py tests/test_audit_trail_integrity.py tests/test_signature_binding.py tests/test_data_integrity.py --junitxml=test_results.xml --cov=backend --cov-report=xml
python scripts/generate_validation_evidence.py
```

## Validation evidence outputs
Generated locally and in CI:
- `validation_summary.md`
- `artifacts/validation_report.md`
- `artifacts/test_results.xml`
- `artifacts/traceability_snapshot.csv`
- `coverage.xml`

## FastAPI app
App entrypoint: `backend/api/routes.py`.

Example startup:
```bash
uvicorn backend.api.routes:app --reload
```
