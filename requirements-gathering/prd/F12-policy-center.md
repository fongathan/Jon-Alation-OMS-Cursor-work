# PRD — Feature 12: Policy Center

## Document control
- **Feature ID:** 12
- **Slug / file:** `F12-policy-center.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/bdc-requirements-map.html (R-03, R-05)`

## 1. Summary
Map organizational policies to catalog objects: retention, classification, handling instructions.

## 2. Problem statement
Policies live in PDFs; engineers cannot see actionable rules next to data.

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
### 5.1 Policy definitions
Title, version, applicability rules (tags, domains, sensitivity).

### 5.2 Attachments
Link policies to assets; display summary + deep link to GRC system optional.

### 5.3 Compliance views
Reports of coverage and exceptions.

## 6. User stories
- As compliance, I attach retention policy to all customer PII datasets.
- As an engineer, I read handling rules on the asset page.

## 7. Use cases & examples
- Policy pack v3 rolls out; catalog shows banner until assets re-attested.

## 8. UX & UI notes
Policies tab/section in on-top pattern; chips on integrated strip.

## 9. Data model & API considerations
Policy association CRUD; read filters for catalog export.

## 10. Non-functional requirements
Policy changes audited.

## 11. Acceptance criteria (testable)
- Removing policy requires permission.
- Conflicting policies flagged to admin.

## 12. Dependencies
Glossary and tags for applicability.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Authoritative system of record: OMS vs external GRC?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
