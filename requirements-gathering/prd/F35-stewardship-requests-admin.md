# PRD — Feature 35: Stewardship Requests, Approvals & Admin Operations

## Document control
- **Feature ID:** 35
- **Slug / file:** `F35-stewardship-requests-admin.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/bdc-requirements-map.html (R-05)`

## 1. Summary
Queues for access and metadata change requests; admin for connectors, sync, roles, import/export catalog actions.

## 2. Problem statement
Email-based access and stewardship approvals do not scale; admins need one place for catalog ops.

## 3. Goals & non-goals
### Goals
- Deliver the outcomes described in user stories and acceptance criteria below.
- Stay compatible with OMS as system of record for technical metadata unless explicitly scoped otherwise.

### Non-goals (unless pulled into scope by program)
- Re-implement full warehouse observability or BI server admin outside catalog boundaries.

## 4. Users & primary personas
| Persona | Why they care |
|---------|----------------|
| Data Steward / Owner | Maintain accurate metadata and policies.
| Data Analyst / BI | Find and trust data for reporting.
| Data Engineer | Lineage, technical context, automation hooks.
| Governance / Compliance | Risk reduction, attestations, exports.
| Platform Admin | Connectors, access, operational health.

## 5. Functional requirements (decomposed)
### 5.1 Requests queue
Intake, assignee, SLA, approve/deny with reason, link to asset.

### 5.2 Access vs metadata requests
Separate templates and approver pools if needed.

### 5.3 Admin tab
Connectors, sync triggers, role assignment, feature flags.

### 5.4 Toolbar actions
Import tags, export catalog CSV in integrated pattern.

## 6. User stories
- As a user, I request description update from asset page.
- As domain admin, I approve batch tag change requests.

## 7. Use cases & examples
- Access request routes to table owner and data platform if external share.

## 8. UX & UI notes
Requests tab in on-top BDC; notifications on state change.

## 9. Data model & API considerations
Ticket CRUD; webhook to ITSM optional.

## 10. Non-functional requirements
SLA metrics for time-to-first-response.

## 11. Acceptance criteria (testable)
- Request always references asset version at submission.
- Denial requires reason visible to requester.

## 12. Dependencies
Identity, email/Slack notify, F9 ownership.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Integrate with ServiceNow / Jira?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
