# PRD — Feature 21: Flags (Endorsements, Warnings, Deprecations)

## Document control
- **Feature ID:** 21
- **Slug / file:** `F21-flags-endorsements-deprecations.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/bdc-requirements-map.html (R-11)`
- `../../business-data-catalog/bdc-trust-flags.js`

## 1. Summary
Trust signals: endorsed, experimental, deprecated—with reasons, dates, and attribution.

## 2. Problem statement
Analysts cannot tell curated vs legacy junk without tribal knowledge.

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
### 5.1 Flag types
Trusted/endorsed, warning, deprecated; optional custom.

### 5.2 Scope
Schema, table, column level per program.

### 5.3 Attribution
Who set flag, when, reason text, optional successor link.

### 5.4 UX enforcement
Query tools may warn on deprecated (integration point optional).

## 6. User stories
- As a steward, I deprecate a table with successor URL.
- As an analyst, I see red banner before running SQL.

## 7. Use cases & examples
- Migration: bulk mark legacy Alation-endorsed assets in OMS.

## 8. UX & UI notes
Trust strip under title; column-level toggles in schema grid (see prototype).

## 9. Data model & API considerations
PATCH trust state with validation transitions.

## 10. Non-functional requirements
High visibility changes notify subscribers.

## 11. Acceptance criteria (testable)
- Deprecation requires reason if policy enabled.
- Column flag visible in inventory export.

## 12. Dependencies
Notification optional, stewardship roles.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Endorsement governance: who can endorse?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
