# PRD — Feature 17: Saved Queries / Favorites

## Document control
- **Feature ID:** 17
- **Slug / file:** `F17-saved-queries-favorites.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
Bookmark assets, saved searches, and optional shared lists for teams.

## 2. Problem statement
Repeat navigation for recurring analysis work.

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
### 5.1 Favorites
Star asset; list in home sidebar.

### 5.2 Saved search
Persist filter + query string; optional alert on new matches.

### 5.3 Collections
Curated lists for onboarding packs (phase 2).

## 6. User stories
- As an analyst, I star my five weekly KPI tables.
- As a lead, I share a saved search for 'unowned marts'.

## 7. Use cases & examples
- New team member clones starter collection from lead.

## 8. UX & UI notes
Star icon on rows; Favorites page; save search dialog.

## 9. Data model & API considerations
CRUD favorites and saved searches per user.

## 10. Non-functional requirements
Privacy: shared lists respect RBAC on contained assets.

## 11. Acceptance criteria (testable)
- Cannot favorite asset user cannot read.
- Deleting asset removes from favorites gracefully.

## 12. Dependencies
User identity.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Org-wide curated lists ownership model?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
