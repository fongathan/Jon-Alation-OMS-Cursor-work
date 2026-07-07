# PRD — Feature 22: Domains

## Document control
- **Feature ID:** 22
- **Slug / file:** `F22-domains.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../AGENTS.md (DEEPT context)`

## 1. Summary
Business grouping for search scope, stewardship defaults, and policy application (e.g., DEEPT, Ad Platforms).

## 2. Problem statement
Enterprise catalog is too large without domain boundaries.

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
### 5.1 Domain registry
Name, charter, leads, member groups.

### 5.2 Asset membership
Manual, inherited from path rules, or hybrid.

### 5.3 Scoped experiences
Default filters, dashboards, steward queues per domain.

## 6. User stories
- As a domain lead, I see only my assets in default view.
- As enterprise governance, I compare coverage across domains.

## 7. Use cases & examples
- DEEPT domain auto-includes tables under approved database prefixes.

## 8. UX & UI notes
Domain switcher; badges on assets; domain admin settings.

## 9. Data model & API considerations
Domain CRUD; membership rules engine.

## 10. Non-functional requirements
Membership recomputation jobs observable.

## 11. Acceptance criteria (testable)
- User in two domains can switch context without re-login.
- Asset cannot be orphaned if policy requires domain.

## 12. Dependencies
IdP groups for membership.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Overlap / multi-domain assets?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
