# Workflow Matrix (Routing Rules)

## Purpose
Define default routing logic based on site, department, and document type.

## Routing Matrix
| Site | Department | Document Type | Authoring Owner | Required Reviewers | Required Approvers | Effective On | Periodic Review |
|---|---|---|---|---|---|---|---|
| Site-A | Quality | SOP | Process Owner | QA Reviewer + SME | QA Manager | Approval + 7 days | 24 months |
| Site-A | Manufacturing | WI | Line Supervisor | Production Reviewer | Production Manager + QA | Approval + 3 days | 24 months |
| Site-A | Engineering | Form | Document Owner | Engineering Reviewer | Engineering Manager | Approval date | 36 months |
| Site-B | Quality Control | SOP | Lab Lead | QC Reviewer + QA Reviewer | QC Manager + QA Manager | Approval + 7 days | 24 months |
| Site-B | Warehouse | WI | Warehouse Supervisor | Logistics Reviewer | Warehouse Manager | Approval + 3 days | 24 months |
| Global | Regulatory | Policy | Policy Owner | Regulatory Reviewer | Head of Regulatory + QA | Approval + 14 days | 12 months |

## Routing Rule Logic
1. **Site precedence:** Site-specific rules override global defaults.
2. **Department fallback:** If no department-specific route exists, use site-level default route by document type.
3. **Document-type controls:** SOP and Policy require dual approval (functional + QA/regulatory).
4. **Escalation:** If reviewer/approver task exceeds SLA (default 10 business days), escalate to role manager.
5. **Change impact:** Major revisions require full review cycle; minor revisions may follow streamlined route if QA-approved.
