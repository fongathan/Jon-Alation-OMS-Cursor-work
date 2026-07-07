# PRD — Feature 8: Documentation / Articles

## Document control
- **Feature ID:** 8
- **Slug / file:** `F08-documentation-articles.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
Rich-text knowledge attached to catalog objects or organized in folders for how-tos and data product docs.

## 2. Problem statement
Tribal knowledge lives outside the catalog; onboarding is slow.

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
### 5.1 Editor
Markdown or WYSIWYG; attachments; internal links to assets.

### 5.2 Linking model
Many-to-many articles ↔ assets; primary article flag optional.

### 5.3 Folders / spaces
See Folders feature for hierarchy.

### 5.4 Permissions
Author vs reader; draft/publish workflow optional.

## 6. User stories
- As a steward, I attach a getting-started article to a complex dataset.
- As an analyst, I read the article from asset detail.

## 7. Use cases & examples
- How-to for quarterly close checks linked to finance marts.

## 8. UX & UI notes
Articles tab on asset; print-friendly view.

## 9. Data model & API considerations
CRUD articles; link endpoints.

## 10. Non-functional requirements
Full-text search included in global search index.

## 11. Acceptance criteria (testable)
- Broken internal links detected on publish (optional).
- Unpublished drafts invisible to readers.

## 12. Dependencies
SSO groups for authoring.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Confluence coexistence / embed?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
