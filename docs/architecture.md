# EDMS Architecture Baseline

## Core backend modules

- `backend/domain/models.py`
  - Canonical entities such as `Document`, `DocumentVersion`, `WorkflowInstance`,
    `SignatureEvent`, `PrintEvent`, `AuditEntry`, and `RoleAssignment`.
- `backend/api/routes.py`
  - Route/action stubs for lifecycle operations and controlled print workflows.
- `backend/workflows/state_machine.py`
  - Transition policy for document states and guard function used by services.
- `backend/*`
  - Package boundaries for `documents`, `workflows`, `signatures`, `printing`,
    `audit`, `auth`, and `reports` modules.

## Lifecycle mapping

1. **Draft**: document creation initiated.
2. **In review**: review and comments in progress.
3. **Approved**: reviewer/approver endorsement completed.
4. **Effective**: active controlled version for operations.
5. **Archived**: obsolete/retired version retained read-only.

The state machine currently enforces allowed transitions:

- `draft -> in_review`
- `in_review -> approved | rejected`
- `rejected -> draft`
- `approved -> effective`
- `effective -> archived`

## Extension points

- Add authority checks before transition execution (role + site/department scope).
- Link transition actions to immutable audit append operations.
- Add signature manifestation storage for approval transitions.
- Add controlled print issuance/reconciliation records to reporting exports.
