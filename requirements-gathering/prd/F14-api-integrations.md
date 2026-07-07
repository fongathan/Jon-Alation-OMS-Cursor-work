# PRD — Feature 14: API & Integrations

## Document control
- **Feature ID:** 14
- **Slug / file:** `F14-api-integrations.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/bdc-requirements-map.html (R-08)`

## 1. Summary
REST/GraphQL-style APIs and tokens for automation, CI/CD metadata updates, and BI embedding.

## 2. Problem statement
Manual catalog updates lag code changes; integrators need stable contracts.

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
### 5.1 Public contract
Versioned OpenAPI; deprecation policy.

### 5.2 Auth
SSO for humans; service principals / PAT for automation with scopes.

### 5.3 Bulk endpoints
Batch PATCH, async job for large uploads.

### 5.4 Webhooks
Optional events: asset updated, tag applied.

## 6. User stories
- As a DE, I update descriptions from CI when dbt model changes.
- As a tool vendor, I embed catalog iframe with SSO.

## 7. Use cases & examples
- Nightly job reconciles owners from internal CMDB.

## 8. UX & UI notes
Developer portal page: keys, examples, rate limit status.

## 9. Data model & API considerations
Core of feature—documented limits and error codes.

## 10. Non-functional requirements
Idempotency keys for bulk writes; SLO for read APIs.

## 11. Acceptance criteria (testable)
- 429 with Retry-After when throttled.
- Invalid payload returns field-level errors.

## 12. Dependencies
API gateway, audit store.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- GraphQL vs REST only?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
