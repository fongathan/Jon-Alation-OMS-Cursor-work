# PRD — Feature 6: Tags & Classification

## Document control
- **Feature ID:** 6
- **Slug / file:** `F06-tags-classification.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../1-Feature-Inventory-Matrix.md Appendix Tags`

## 1. Summary
Controlled and extensible tags for sensitivity, domain, lifecycle, and custom programs.

## 2. Problem statement
Manual email-driven classification does not scale; filters for compliance are unreliable.

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
### 5.1 Tag dictionary
Admin-defined tags with categories, colors, descriptions.

### 5.2 Application UI
Multi-select on asset, column-level tags optional.

### 5.3 Bulk tag
Ties to mass edit and rules engine.

### 5.4 Reporting
Filter catalog and exports by tag combinations.

## 6. User stories
- As governance, I require 'PII' tag before prod promotion.
- As a steward, I bulk-remove obsolete program tags.

## 7. Use cases & examples
- Tag 'GDPR-Relevant' applied to 400 tables via CSV import with audit.

## 8. UX & UI notes
Pills on detail; filter row on tables; import tags action in integrated toolbar.

## 9. Data model & API considerations
Tag CRUD; bulk apply endpoint.

## 10. Non-functional requirements
Tag changes audited with actor and timestamp.

## 11. Acceptance criteria (testable)
- Cannot apply retired tag.
- Facet counts match authoritative index within refresh window.

## 12. Dependencies
RBAC for who can create vs apply tags.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Hierarchical tags?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
