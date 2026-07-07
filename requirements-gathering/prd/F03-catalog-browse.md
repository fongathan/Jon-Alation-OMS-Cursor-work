# PRD — Feature 3: Catalog Browse

## Document control
- **Feature ID:** 3
- **Slug / file:** `F03-catalog-browse.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/bdc-requirements-map.html (R-09)`

## 1. Summary
Hierarchical and faceted browsing of datasources, schemas, databases, and tables consistent with OMS mental models.

## 2. Problem statement
Users who do not know exact names need safe exploration without running queries.

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
### 5.1 Datasource catalog
Cards or list of registered sources with health/counts.

### 5.2 Drill hierarchy
Datasource → database/schema → table (source-specific shapes abstracted).

### 5.3 Column preview
Optional expand for column list with types and business fields.

### 5.4 Contextual BDC strip
Business chips when browsing within a technical context (integrated pattern).

## 6. User stories
- As an engineer, I browse Unity vs Snowflake namespaces side by side in OMS.
- As an analyst, I browse only prod assets in my domain.

## 7. Use cases & examples
- User navigates Snowflake ANALYTICS → MART → FACT_SUBSCRIPTION.

## 8. UX & UI notes
Breadcrumbs, left tree optional, paginated tables, LINEAGE action per row where applicable.

## 9. Data model & API considerations
Child listing endpoints with cursor pagination.

## 10. Non-functional requirements
Large schemas remain responsive via pagination and lazy load.

## 11. Acceptance criteria (testable)
- Breadcrumb matches user location.
- Pagination stable under sort/filter.

## 12. Dependencies
Connector metadata freshness.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Favorite paths / pinned hierarchies?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
