# PRD — Feature 26: Mass / Bulk Edit

## Document control
- **Feature ID:** 26
- **Slug / file:** `F26-mass-bulk-edit.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
Select many assets and apply metadata changes once; CSV upload with validation and audit.

## 2. Problem statement
One-by-one edits block migration and domain-wide policy updates.

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
### 5.1 Selection UI
Checkboxes, select all in page, select all matching filter with warning.

### 5.2 Bulk form
Apply tags, owners, descriptions pattern, clear fields.

### 5.3 CSV pipeline
Template download, upload, dry-run, error report, commit.

### 5.4 Job tracking
Async for large jobs; email on completion.

## 6. User stories
- As a steward, I assign owner to 200 tables.
- As governance, I dry-run CSV before apply.

## 7. Use cases & examples
- Reorg: mapping file table FQN → new steward imported.

## 8. UX & UI notes
Bulk action bar; progress modal; downloadable error CSV.

## 9. Data model & API considerations
Bulk PATCH job creation; status polling.

## 10. Non-functional requirements
Idempotent retries; partial failure semantics documented.

## 11. Acceptance criteria (testable)
- Dry-run shows row-level errors without writes.
- Every committed row has audit actor=batch job+user.

## 12. Dependencies
RBAC bulk permission, dictionary upload F29.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Max assets per job?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
