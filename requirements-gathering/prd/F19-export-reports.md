# PRD — Feature 19: Export / Reports

## Document control
- **Feature ID:** 19
- **Slug / file:** `F19-export-reports.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
CSV/Excel exports and scheduled reports for catalog state, usage, and compliance.

## 2. Problem statement
Execs and auditors need snapshots outside the UI.

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
### 5.1 Ad hoc export
From any filtered inventory view.

### 5.2 Templates
Standard compliance column packs.

### 5.3 Scheduling
Email delivery or S3 drop (phase 2).

## 6. User stories
- As governance, I export all PII-tagged tables monthly.
- As PM, I export backlog of missing descriptions.

## 7. Use cases & examples
- Audit workbook with owner, domain, last access, policies.

## 8. UX & UI notes
Export button with column picker; progress for large exports.

## 9. Data model & API considerations
Async export job with download URL.

## 10. Non-functional requirements
Exports watermarked or access-logged if sensitive.

## 11. Acceptance criteria (testable)
- Export respects current filters and RBAC.
- Large export emails link with expiry.

## 12. Dependencies
Object storage for temp files.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Max rows per export?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
