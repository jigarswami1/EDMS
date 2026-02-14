# Pharmaceutical EDMS

A compliant Electronic Document Management System (EDMS) starter focused on controlled pharmaceutical documentation workflows.

## Step-by-step progress

This increment adds a formal workflow state-machine module and tests to enforce document lifecycle rules.

## Repository structure

- `backend/`
  - `documents/`: document content and versioning services
  - `workflows/`: lifecycle routing and state transition guards
  - `signatures/`: electronic signature integration points
  - `printing/`: controlled print issuance and reconciliation
  - `audit/`: immutable audit trail interfaces
  - `auth/`: role and authority checks
  - `reports/`: inspection/reporting outputs
  - `domain/models.py`: shared EDMS domain models
  - `api/routes.py`: framework-agnostic API route stubs
- `docs/`: architecture and compliance-oriented documentation
- `tests/`: unit and integration test suites
- `frontend/`: UI application placeholder
- `infra/`: deployment/infrastructure placeholder

## Run tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Next development step

Implement role-based authority checks and signature-linked approval handlers that call the workflow guard before state mutation.
