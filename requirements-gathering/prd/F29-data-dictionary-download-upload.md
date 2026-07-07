# PRD — Feature 29: Data Dictionary Download & Uploads

## Document control
- **Feature ID:** 29
- **Slug / file:** `F29-data-dictionary-download-upload.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
Spreadsheet round-trip for titles, descriptions, custom fields across many assets for stewards and audits.

## 2. Problem statement
Stewards work faster in Excel; audits need frozen extracts.

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
### 5.1 Export
Scoped export by datasource/domain; column chooser.

### 5.2 Template stability
Versioned headers; FQN stable keys.

### 5.3 Import validation
Type checks, unknown rows, permission checks per row.

### 5.4 Diff report
What would change before commit.

## 6. User stories
- As a steward, I edit 500 descriptions offline and upload.
- As audit, I download dictionary quarterly.

## 7. Use cases & examples
- Acquisition: merge two catalogs via spreadsheet mapping.

## 8. UX & UI notes
Export/import wizard under toolbar actions.

## 9. Data model & API considerations
Same as bulk job with file upload multipart.

## 10. Non-functional requirements
File size limits; virus scan on upload.

## 11. Acceptance criteria (testable)
- Round-trip: export → unchanged re-import is no-op.
- Row-level errors downloadable.

## 12. Dependencies
F7 custom fields schema, F26 bulk permissions.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Excel macro support or CSV only MVP?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
