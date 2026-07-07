# PRD — Feature 23: Folders

## Document control
- **Feature ID:** 23
- **Slug / file:** `F23-folders.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
Hierarchical organization for articles and documentation separate from technical hierarchy.

## 2. Problem statement
Flat article lists become unnavigable at scale.

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
### 5.1 Folder tree
Nested folders; permissions inherit with override.

### 5.2 Move / copy
Articles relocate with audit.

### 5.3 Navigation
Breadcrumb in knowledge section.

## 6. User stories
- As a steward, I group onboarding articles under 'Q1 2027'.
- As a reader, I browse folder structure like a mini wiki.

## 7. Use cases & examples
- How-to folder vs project-specific collections per matrix notes.

## 8. UX & UI notes
Left tree + content pane; drag-drop optional phase 2.

## 9. Data model & API considerations
Folder CRUD; list children.

## 10. Non-functional requirements
Max depth / count limits to prevent abuse.

## 11. Acceptance criteria (testable)
- Circular moves prevented.
- Unauthorized folder hidden from search.

## 12. Dependencies
Articles feature, RBAC.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Shared with Confluence hierarchy?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
