# PRD — Feature 31: Metadata Quality & Completeness Scoring

## Document control
- **Feature ID:** 31
- **Slug / file:** `F31-metadata-quality-completeness.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/bdc-requirements-map.html (R-07)`

## 1. Summary
Signals for description presence, stewardship coverage, and composite quality score on inventory and dashboards.

## 2. Problem statement
Programs need measurable curation progress beyond subjective reviews.

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
### 5.1 Field-level signals
Empty description chip; missing owner; missing glossary link for key columns.

### 5.2 Quality score
Weighted formula configurable by governance; color-coded column.

### 5.3 Rollups
Domain and datasource averages on Overview KPIs.

### 5.4 Facets
Filter catalog to low-quality assets for sprint planning.

## 6. User stories
- As a steward lead, I sort by lowest quality in my domain.
- As PMO, I track average score weekly.

## 7. Use cases & examples
- OKR: raise average quality score from 42 to 70 by Q4.

## 8. UX & UI notes
Quality column on tables; optional sparkline on Overview.

## 9. Data model & API considerations
GET score breakdown per asset for transparency.

## 10. Non-functional requirements
Recompute incremental on metadata change.

## 11. Acceptance criteria (testable)
- Score formula versioned and displayed in UI help.
- Changing weight recalculates within SLA.

## 12. Dependencies
Custom fields, owners, glossary mappings.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Who configures formula globally?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
