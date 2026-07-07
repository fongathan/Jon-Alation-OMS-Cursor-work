# PRD — Feature 27: Mass Set Rules / Catalog Sets

## Document control
- **Feature ID:** 27
- **Slug / file:** `F27-mass-set-rules-catalog-sets.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
Rule-defined dynamic sets of assets for tagging, ownership, and policy application at scale.

## 2. Problem statement
Static lists rot; governance needs 'all tables matching X' continuously.

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
### 5.1 Rule builder
Conditions on name patterns, tags, sensitivity, domain, column names.

### 5.2 Catalog sets
Saved dynamic membership; preview count.

### 5.3 Actions
Apply tag, assign steward, attach policy, enqueue review.

### 5.4 Scheduling
Nightly re-eval or on-change triggers.

## 6. User stories
- As governance, I auto-tag tables with PII columns.
- As a steward, I preview set before applying policy.

## 7. Use cases & examples
- All tables with 'ssn' in column name → retention policy + compliance tag.

## 8. UX & UI notes
Rule wizard; preview table; execution history.

## 9. Data model & API considerations
Rule CRUD; evaluate endpoint; execution logs.

## 10. Non-functional requirements
Evaluation cost caps; circuit breaker if count explodes.

## 11. Acceptance criteria (testable)
- Preview count matches bulk job affected rows within tolerance.
- Rule cannot escalate privileges.

## 12. Dependencies
Tags, policies, profiling optional.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Human approval gate for destructive actions?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
