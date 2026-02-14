# Role-Permission Matrix

## Purpose
Define baseline role permissions and constraints for EDMS access control.

## Permission Key
- **C** = Create
- **R** = Read
- **U** = Update
- **A** = Approve/Sign
- **P** = Print Controlled Copy
- **X** = Administer/Configure

## Matrix
| Role | SOP/WI | Forms | Policies | Obsolete Docs | Audit Trail | User Admin | Workflow Config |
|---|---|---|---|---|---|---|---|
| Author | C,R,U | C,R,U | C,R,U | R | R (own actions) |  |  |
| Reviewer | R,U | R,U | R,U | R | R (assigned scope) |  |  |
| Approver | R,A | R,A | R,A | R | R (assigned scope) |  |  |
| QA | R,U,A,P | R,U,A,P | R,U,A,P | R | R (all) |  | R (quality rules) |
| Trainer | R | R | R | R |  |  |  |
| Reader | R | R | R | R |  |  |  |
| Print Operator | R,P | R,P | R,P | R | R (print events) |  |  |
| System Administrator | R | R | R | R | R (all) | X | X |

## Constraints and Segregation Rules
1. Approvers must not approve documents they are designated as sole authors for, unless formal exception workflow is enabled and QA co-approval is required.
2. System Administrators cannot perform business approvals unless separately assigned an approver role with dual-account control.
3. Privileged actions (role changes, workflow rule edits) require audit logging and periodic review.
4. Site-level access is restricted by assigned organization unit unless global role is explicitly approved.
