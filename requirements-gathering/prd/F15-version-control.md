# PRD — Feature 15: Version Control

## Document control
- **Feature ID:** 15
- **Slug / file:** `F15-version-control.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
History of business metadata changes with optional compare and restore.

## 2. Problem statement
Regulators and incident reviews need to know who changed what and when.

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
### 5.1 Audit log UI
Per-asset timeline of field changes.

### 5.2 Diff view
Before/after for text fields.

### 5.3 Restore
Admin/steward restore prior value with new audit entry.

## 6. User stories
- As compliance, I export change history for an asset for 2 years.
- As a steward, I undo a mistaken bulk description.

## 7. Use cases & examples
- Incident: prove deprecation notice was added before outage.

## 8. UX & UI notes
History tab; filters by field and actor.

## 9. Data model & API considerations
GET history; POST restore with reason.

## 10. Non-functional requirements
Immutable append-only audit store.

## 11. Acceptance criteria (testable)
- No silent overwrites without version bump in audit.
- Restore requires reason string.

## 12. Dependencies
Identity service for stable actor ids.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Retention of audit events?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
