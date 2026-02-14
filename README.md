# EDMS Baseline

This repository contains a baseline scaffold for an Electronic Document Management System (EDMS).

## Project Structure

- `backend/`: domain entities and API stubs for EDMS lifecycle operations.
- `frontend/`: placeholder for UI implementation.
- `docs/`: architecture and design references.
- `tests/`: automated test suites.
- `infra/`: deployment, environment, and operations artifacts.

## Local Run Steps

1. Ensure Python 3.11+ is installed.
2. (Optional) Create and activate a virtual environment.
3. Validate syntax for the initial backend scaffold:
   ```bash
   python -m compileall backend
   ```
4. Run unit/integration tests once they are added:
   ```bash
   python -m unittest discover -s tests
   ```

## Architecture Boundaries

- **Documents** (`backend/documents`): source of truth for documents and versions.
- **Workflows** (`backend/workflows`): review/approval orchestration and state transitions.
- **Signatures** (`backend/signatures`): signature capture and verification events.
- **Printing** (`backend/printing`): controlled printing and reconciliation operations.
- **Audit** (`backend/audit`): append-only audit logging and trace retrieval.
- **Auth** (`backend/auth`): identity context and authorization/role assignment.
- **Reports** (`backend/reports`): read-oriented compliance and KPI reporting.

See `docs/architecture.md` for module-to-lifecycle mapping.
