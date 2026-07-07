# PRD — Feature 5: Data Lineage

## Document control
- **Feature ID:** 5
- **Slug / file:** `F05-data-lineage.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/bdc-requirements-map.html (R-04)`

## 1. Summary
Upstream/downstream relationships at table, column, and pipeline granularity for impact analysis and onboarding.

## 2. Problem statement
Schema changes break unknown downstream consumers; root-cause analysis is slow.

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
### 5.1 Graph / list hybrid
Visual graph where supported; tabular upstream/downstream fallback.

### 5.2 Column lineage
Optional drill from column row.

### 5.3 Pipeline linkage
Connect to dataflows/jobs where OMS stores them.

### 5.4 Export
Lineage download for audits (align with OMS lineage downloads).

## 6. User stories
- As an engineer, I see downstream dashboards affected by a column rename.
- As governance, I export lineage for a regulator request.

## 7. Use cases & examples
- Airflow DAG → dbt model → Snowflake table chain visible end-to-end when metadata exists.

## 8. UX & UI notes
LINEAGE button on lists; modal or full page; loading states for large graphs.

## 9. Data model & API considerations
Lineage query by asset id and depth; async job for bulk export if needed.

## 10. Non-functional requirements
Depth limits and timeouts with partial results + warning.

## 11. Acceptance criteria (testable)
- Table-level lineage renders within SLA for N edges.
- RBAC hides unauthorized nodes or shows stub.

## 12. Dependencies
Ingestion from dbt/Airflow/Snowflake as available.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Column lineage coverage targets?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
