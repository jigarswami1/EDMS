# EDMS Architecture and Lifecycle Mapping

## Lifecycle States

The baseline EDMS lifecycle used for initial module boundaries:

1. **Draft**
2. **In Review**
3. **Approved / Rejected**
4. **Effective**
5. **Printed / Issued**
6. **Reconciled**
7. **Archived**

## Module-to-Lifecycle Mapping

| Module | Primary Responsibility | Lifecycle States |
| --- | --- | --- |
| `documents` | Document master records and version control | Draft, In Review, Approved/Rejected, Effective, Archived |
| `workflows` | Review routing, approval decisions, escalation | In Review, Approved/Rejected |
| `signatures` | Signature intent and completion events | Approved/Rejected, Effective |
| `printing` | Print request, issue, reconciliation control | Printed/Issued, Reconciled |
| `audit` | Immutable event journaling for every transition | All states |
| `auth` | Role assignment and permission enforcement | All states |
| `reports` | Cross-module reporting and compliance outputs | Effective, Printed/Issued, Reconciled, Archived |

## Core API Actions in Baseline

Defined in `backend/api/routes.py`:

- Create draft
- Submit review
- Approve/reject
- Make effective
- Request print
- Issue print
- Reconcile print
- Retrieve audit trail

## Domain Entities in Baseline

Defined in `backend/domain/models.py`:

- `Document`
- `DocumentVersion`
- `WorkflowInstance`
- `SignatureEvent`
- `PrintEvent`
- `AuditEntry`
- `RoleAssignment`
