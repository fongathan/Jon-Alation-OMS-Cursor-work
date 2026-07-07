# PRD — Feature 7: Custom Fields

## Document control
- **Feature ID:** 7
- **Slug / file:** `F07-custom-fields.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../1-Feature-Inventory-Matrix.md Appendix Custom Fields`

## 1. Summary
Configurable metadata fields per object type to capture domain-specific attributes beyond core schema.

## 2. Problem statement
One-size metadata misses retention category, cost center, data product IDs, etc.

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
### 5.1 Field definitions
Types: text, number, date, enum, URL; required/optional per type or domain.

### 5.2 Rendering
Dynamic form sections on asset detail and exports.

### 5.3 Validation
Regex, max length, enum enforcement.

### 5.4 Dictionary round-trip
Include in download/upload templates.

## 6. User stories
- As a domain admin, I add 'Data Product ID' to all tables in my domain.
- As an analyst, I filter by that field.

## 7. Use cases & examples
- DEET adds enum for 'Consumer jurisdiction' on sensitive marts.

## 8. UX & UI notes
Collapsible 'Custom attributes' card; empty vs filled states.

## 9. Data model & API considerations
Schema registry for custom fields; PATCH validates against schema.

## 10. Non-functional requirements
Schema migrations backward compatible or versioned.

## 11. Acceptance criteria (testable)
- Invalid enum rejected with clear error.
- Field appears in CSV export column set.

## 12. Dependencies
Tag and domain scoping rules.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Who can define fields globally vs per domain?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
