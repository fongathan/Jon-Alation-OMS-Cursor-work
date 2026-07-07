# PRD — Feature 11: Data Sources & Connectors

## Document control
- **Feature ID:** 11
- **Slug / file:** `F11-data-sources-connectors.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/bdc-requirements-map.html (R-12 partial)`

## 1. Summary
Registration, credentialing, scheduling, and health of metadata connectors into OMS/BDC.

## 2. Problem statement
Stale or missing sources undermine trust in the entire catalog.

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
### 5.1 Connector catalog
Snowflake, Unity, Tableau, Airflow, etc. per OMS roadmap.

### 5.2 Sync jobs
Schedule, manual run, last success, error surfacing.

### 5.3 Scope controls
Include/exclude databases, schemas, projects.

### 5.4 Secrets management
Vault integration; no secrets in UI.

## 6. User stories
- As platform admin, I add a new Snowflake account with scoped schemas.
- As governance, I see connector lag SLAs.

## 7. Use cases & examples
- Connector fails; UI shows actionable error and ticket link.

## 8. UX & UI notes
Admin tab pattern in on-top BDC; or OMS native admin surface.

## 9. Data model & API considerations
Connector CRUD and trigger sync (admin scoped).

## 10. Non-functional requirements
Incremental sync where supported; full refresh windows communicated.

## 11. Acceptance criteria (testable)
- New table appears within agreed lag after warehouse DDL.
- Failed sync visible on datasource home.

## 12. Dependencies
Network, IAM roles, warehouse admin cooperation.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- BYO connector SDK in scope?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
