# PRD — Feature 9: Ownership / Stewardship

## Document control
- **Feature ID:** 9
- **Slug / file:** `F09-ownership-stewardship.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
Clear accountability: data owner, technical owner, stewards, escalation paths on assets and domains.

## 2. Problem statement
No single accountable party when quality or access issues arise.

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
### 5.1 Role assignments
Owner, steward, delegate; inherit from domain with override.

### 5.2 Directory integration
Resolve people from corporate directory; show contact.

### 5.3 Coverage metrics
Dashboard widgets: % assets with owner in domain.

### 5.4 Escalation
Link to request workflow for ownership disputes.

## 6. User stories
- As leadership, I see owner coverage by domain.
- As a user, I request access from the listed steward.

## 7. Use cases & examples
- Domain reorg: bulk reassign stewards via CSV.

## 8. UX & UI notes
People chips with avatar; empty state prompts assignment for stewards.

## 9. Data model & API considerations
PATCH owners; bulk assign.

## 10. Non-functional requirements
Invalid user ids rejected at API boundary.

## 11. Acceptance criteria (testable)
- Inherited owner visible with source badge.
- Removing last steward blocked if policy requires one.

## 12. Dependencies
HR/directory API, domain model.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Co-owner vs single owner policy?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
