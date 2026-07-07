# PRD — Feature 34: In-Catalog SQL Exploration, Query History & Sample Content

## Document control
- **Feature ID:** 34
- **Slug / file:** `F34-in-catalog-sql-query-sample.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/bdc-requirements-map.html (R-10)`

## 1. Summary
Optional SQL workspace on asset: editor, run history, column vs sample toggle, pending-change highlighting for business fields.

## 2. Problem statement
Users jump to warehouse consoles losing catalog context.

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
### 5.1 SQL editor
Syntax highlight; limits on rows/cost; role-checked warehouse creds.

### 5.2 Query history
Previous runs on this asset with timestamp and user.

### 5.3 Columns & sample
Toggle between schema grid and masked sample rows.

### 5.4 Change highlighting
Pending business edits in light red until saved.

### 5.5 Provenance
Show where sample data came from (env, policy).

## 6. User stories
- As an analyst, I validate a column without leaving catalog.
- As governance, I enforce masked samples only.

## 7. Use cases & examples
- Analyst runs SELECT COUNT(*) FROM mart before requesting access.

## 8. UX & UI notes
Queries tab + SQL tab per integrated prototype; on-top may deep link to OMS for full SQL.

## 9. Data model & API considerations
Proxy query execution service; audit all runs.

## 10. Non-functional requirements
Cost guardrails; query timeout; no PII in logs.

## 11. Acceptance criteria (testable)
- Unauthorized warehouse role cannot run.
- Sample respects row-level security if enabled.

## 12. Dependencies
Warehouse compute, SSO to warehouse, F20 RBAC.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- MVP: read-only vs full run?
- On-top: always deep link vs embed?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
