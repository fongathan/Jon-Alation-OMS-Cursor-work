# PRD — Feature 18: Comments / Discussions

## Document control
- **Feature ID:** 18
- **Slug / file:** `F18-comments-discussions.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
Threaded discussion on assets for Q&A and change coordination.

## 2. Problem statement
Questions repeat in Slack without durable record on the asset.

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
### 5.1 Threads
Top-level comment, replies, @mentions optional.

### 5.2 Moderation
Steward can lock or hide abusive content.

### 5.3 Notifications
Email or in-app on reply.

## 6. User stories
- As an analyst, I ask if a column is still populated.
- As a steward, I pin official answer.

## 7. Use cases & examples
- Schema migration discussion attached to table for audit.

## 8. UX & UI notes
Comments tab; markdown lite; sort by newest.

## 9. Data model & API considerations
CRUD comments; pagination.

## 10. Non-functional requirements
Retention and export for legal hold.

## 11. Acceptance criteria (testable)
- Deleted user shows as 'Former user' without PII leak.
- Pinning limited to stewards.

## 12. Dependencies
Notification service.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Integration with Slack threads?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
