# PRD — Feature 2: Business Glossary

## Document control
- **Feature ID:** 2
- **Slug / file:** `F02-business-glossary.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../2-Persona-Feature-Matrix.md`

## 1. Summary
Controlled vocabulary of business terms with definitions, synonyms, stewardship, and links to physical data elements.

## 2. Problem statement
Teams use inconsistent labels for the same concept; policies and reports reference terms that are not tied to actual columns.

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
### 5.1 Term CRUD
Create/edit/retire terms; status (draft/published/deprecated); rich-text definition.

### 5.2 Synonyms & abbreviations
Alternate labels for search and documentation.

### 5.3 Stewardship
Primary owner, backup, domain linkage, review cadence.

### 5.4 Mappings
Link terms to tables/columns/metrics; cardinality and confidence optional.

### 5.5 Consumption surfaces
Term appears on asset detail, search snippets, policy references.

## 6. User stories
- As a steward, I publish a term and map it to the authoritative columns.
- As an analyst, I hover a column and see the glossary definition.

## 7. Use cases & examples
- Finance publishes 'ARPU' with formula narrative and maps to three warehouse columns across envs.

## 8. UX & UI notes
Glossary list + term detail; mapping UI with picker for catalog objects; change history.

## 9. Data model & API considerations
REST for term lifecycle and bulk mapping import.

## 10. Non-functional requirements
Published terms immutable without new version or audit reason.

## 11. Acceptance criteria (testable)
- Published term visible on all mapped assets.
- Search finds term by synonym.
- Deprecation blocks new mappings and surfaces banner on assets.

## 12. Dependencies
Domain model, RBAC for publishers vs consumers.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Workflow for approving new terms?
- Integration with external glossary?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
