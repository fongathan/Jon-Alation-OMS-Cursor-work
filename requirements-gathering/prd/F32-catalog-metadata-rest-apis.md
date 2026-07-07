# PRD — Feature 32: Catalog & Metadata REST APIs (Developer Surface)

## Document control
- **Feature ID:** 32
- **Slug / file:** `F32-catalog-metadata-rest-apis.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/bdc-requirements-map.html (R-08)`

## 1. Summary
Documented REST shape for assets, search, export hooks, and PATCH semantics used by UI and automation.

## 2. Problem statement
Undocumented stubs block parallel UI/engineering work.

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
### 5.1 Resource model
Assets, domains, tags, terms, policies with stable ids.

### 5.2 PATCH semantics
Partial updates, ETags, optimistic concurrency.

### 5.3 Error contract
Problem+json or consistent error envelope.

### 5.4 Developer docs
Examples for curl, Postman collection, changelog.

## 6. User stories
- As a frontend dev, I mock against published OpenAPI.
- As integrator, I rotate PAT without downtime.

## 7. Use cases & examples
- UI drawer calls PATCH /catalog/assets/{id} for inline edit.

## 8. UX & UI notes
N/A server-side; optional API explorer page.

## 9. Data model & API considerations
Core deliverable—mirror prototype references in requirements map.

## 10. Non-functional requirements
Backward compatible minor versions.

## 11. Acceptance criteria (testable)
- OpenAPI published in CI artifact.
- Breaking changes require major version bump.

## 12. Dependencies
Auth gateway, audit middleware.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- GraphQL read layer?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
