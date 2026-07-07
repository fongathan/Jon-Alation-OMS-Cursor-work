# PRD — Feature 4: Table / Asset Detail

## Document control
- **Feature ID:** 4
- **Slug / file:** `F04-table-asset-detail.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/BDC-OMS-integrated-vs-on-top-decision.md`

## 1. Summary
Authoritative asset page combining technical metadata, business metadata, lineage entry points, and stewardship.

## 2. Problem statement
Fragmented views force users to open many tools before trusting data.

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
### 5.1 Overview
Name, type, description, owners, tags, trust flags, key stats.

### 5.2 Technical metadata
Row counts, partitioning, retention hints, operational fields as available from OMS.

### 5.3 Business metadata
Sensitivity, policies, glossary links, custom fields.

### 5.4 Schema / columns
Grid with technical + business columns; inline or drawer edit.

### 5.5 Tabs / drawers
Lineage, queries, samples per program decision (integrated vs on-top).

## 6. User stories
- As a steward, I edit description and owner with pending-change UX.
- As an analyst, I read trust flag and deprecation reason before querying.

## 7. Use cases & examples
- Deprecated table shows red banner, successor link, and read-only technical stats.

## 8. UX & UI notes
Integrated: full technical + business. On-top: business-first with deep link to full OMS technical page.

## 9. Data model & API considerations
GET asset; PATCH business fields with ETag.

## 10. Non-functional requirements
Field-level audit trail for business edits.

## 11. Acceptance criteria (testable)
- All mandatory business fields visible per policy.
- Unauthorized user cannot PATCH.
- Lineage button opens same modal/page as browse.

## 12. Dependencies
Trust flags feature, glossary mappings.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Which tabs ship MVP vs later?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
