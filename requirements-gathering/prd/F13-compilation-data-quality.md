# PRD — Feature 13: Compilation / Data Quality

## Document control
- **Feature ID:** 13
- **Slug / file:** `F13-compilation-data-quality.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
Profiling, rules, and compilation signals surfaced where OMS already captures them; optional expansion for BDC.

## 2. Problem statement
Consumers discover broken data only after shipping reports.

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
### 5.1 Profiles
Null rates, cardinality, min/max where supported.

### 5.2 Rules & alerts
Pass/warn/fail with schedule; link to incident workflow optional.

### 5.3 Compilation
dbt/test or platform-specific compile errors if integrated.

## 6. User stories
- As an engineer, I see last profile timestamp on column.
- As governance, I see failing assets in a domain report.

## 7. Use cases & examples
- Freshness SLA breach highlights asset in steward inbox (phase 2).

## 8. UX & UI notes
Quality tab or subsection; avoid duplicating full observability product—link out when needed.

## 9. Data model & API considerations
Read profile snapshots; optional webhook on rule failure.

## 10. Non-functional requirements
Profiling cost controls (sample size, schedule).

## 11. Acceptance criteria (testable)
- If no profile exists, UI states 'not run' not silent empty.
- PII columns masked in profile views for restricted roles.

## 12. Dependencies
Compute for profiling, warehouse permissions.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- MVP depth: profile only vs full rules engine?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
