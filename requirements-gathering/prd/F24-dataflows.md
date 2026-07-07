# PRD — Feature 24: Dataflows

## Document control
- **Feature ID:** 24
- **Slug / file:** `F24-dataflows.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../1-Feature-Inventory-Matrix.md row 24 note vs lineage`

## 1. Summary
First-class objects for jobs, DAGs, dbt models, procedures—linked to tables and lineage.

## 2. Problem statement
Lineage alone loses the executable context engineers need.

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
### 5.1 Object types
Airflow DAG, dbt model, stored proc, Spark job, etc.

### 5.2 Metadata
Owner, schedule, repo link, runtime stats if available.

### 5.3 Relationships
Reads/writes edges to datasets.

## 6. User stories
- As an engineer, I open the dbt model from the fact table page.
- As SRE, I jump to Airflow from lineage node.

## 7. Use cases & examples
- sales_transform dbt model shows tests and repo path.

## 8. UX & UI notes
Dataflow detail page; appears as node in lineage graph.

## 9. Data model & API considerations
CRUD/read from OMS ingestion pipelines.

## 10. Non-functional requirements
Dedup same logical job from multiple ingest sources.

## 11. Acceptance criteria (testable)
- From table, list upstream dataflows with schedule.
- Broken repo links flagged.

## 12. Dependencies
Airflow/dbt connectors.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Which orchestrators MVP?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
