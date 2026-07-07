# PRD — Feature 16: Recommendations / Suggestions

## Document control
- **Feature ID:** 16
- **Slug / file:** `F16-recommendations.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
Lightweight suggestions for descriptions, tags, stewards based on heuristics or ML (distinct from full chat assistant).

## 2. Problem statement
Metadata debt grows faster than steward capacity.

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
### 5.1 Suggestion engine
Rules: copy from similar asset name patterns; optional ML.

### 5.2 Inbox UX
Accept/dismiss per suggestion; batch accept.

### 5.3 Feedback loop
Dismissal trains suppression (phase 2).

## 6. User stories
- As a steward, I accept 10 tag suggestions generated from column names.
- As governance, I tune which rules run per domain.

## 7. Use cases & examples
- Suggest 'email' PII tag when column names match regex.

## 8. UX & UI notes
Badge on asset; queue in steward dashboard.

## 9. Data model & API considerations
Generate suggestions job; POST accept/dismiss.

## 10. Non-functional requirements
Suggestions never auto-apply without policy flag.

## 11. Acceptance criteria (testable)
- User sees confidence or rule name for each suggestion.
- Dismiss is audited.

## 12. Dependencies
Feature 6 tags, profiling optional.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- ML vs rules-only MVP?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
