# PRD — Feature 25: Admin Analytics Dashboard

## Document control
- **Feature ID:** 25
- **Slug / file:** `F25-admin-analytics-dashboard.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/partials/bdc-alation-admin.html`

## 1. Summary
Pre-built and exploratory analytics for catalog adoption, curation, search, and governance—admin role.

## 2. Problem statement
Program sponsors cannot prove value; stewards lack backlog signals.

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
### 5.1 Dashboards
Executive summary, adoption, curation progress, search quality.

### 5.2 Ad hoc query
SQL or guided query over telemetry warehouse.

### 5.3 Filters
Time, team, asset type, domain.

### 5.4 Export
CSV from widgets.

## 6. User stories
- As admin, I view MAU and top searches.
- As governance, I find domains with declining description coverage.

## 7. Use cases & examples
- Quarterly business review slide data exported from dashboard.

## 8. UX & UI notes
Dedicated admin section; Chart.js or embedded BI per platform choice.

## 9. Data model & API considerations
Read-only analytics API or reuse warehouse connection.

## 10. Non-functional requirements
PII minimization in telemetry; retention policy published.

## 11. Acceptance criteria (testable)
- Only admin role sees user-level detail if exposed.
- Dashboards load within agreed time with cache.

## 12. Dependencies
Telemetry pipeline into warehouse.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Overlap with feature 12 R-12 prototype consolidation?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
