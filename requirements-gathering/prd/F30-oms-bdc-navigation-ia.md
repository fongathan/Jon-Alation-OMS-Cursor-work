# PRD — Feature 30: OMS / BDC Navigation & Information Architecture

## Document control
- **Feature ID:** 30
- **Slug / file:** `F30-oms-bdc-navigation-ia.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/BDC-OMS-integrated-vs-on-top-decision.md`
- `../../business-data-catalog/bdc-requirements-map.html (R-06)`

## 1. Summary
How users enter catalog experiences: integrated contextual catalog vs dedicated Business Data Catalog shell, breadcrumbs, and deep links.

## 2. Problem statement
Two valid mental models—engineers live in OMS; stewards need a named BDC—must coexist without duplicate backends.

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
### 5.1 Integrated path
BDC chips/strips on existing datasource pages; no new top-level nav item required.

### 5.2 On-top path
Business Data Catalog under Main Pages with sub-nav: Overview, Catalog, Lineage, Glossary, Policies, Requests, Admin.

### 5.3 Breadcrumbs & back
Snowflake drill hides subnav; back returns to BDC home without losing context.

### 5.4 Deep links
URL scheme opens specific asset, tab, and filter state; shareable.

### 5.5 Hybrid contract
Open full technical OMS view from BDC in one click and reverse.

## 6. User stories
- As a steward, I start from BDC Overview KPIs.
- As an engineer, I never leave OMS home but still edit business fields.

## 7. Use cases & examples
- Exec demo: bookmark goes straight to BDC Policies tab filtered to domain.

## 8. UX & UI notes
See BDC-OMS-integrated-vs-on-top-decision.md evaluation table.

## 9. Data model & API considerations
Stable asset URLs across shells.

## 10. Non-functional requirements
Accessibility: landmarks for nav regions; keyboard order consistent.

## 11. Acceptance criteria (testable)
- Deep link survives SSO redirect.
- Integrated and on-top show same asset id in URL or resolve equivalently.

## 12. Dependencies
Program decision on primary pattern; single metadata API.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Default landing for hybrid users?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
