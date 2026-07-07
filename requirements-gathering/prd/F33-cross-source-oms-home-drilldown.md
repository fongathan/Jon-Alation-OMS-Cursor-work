# PRD — Feature 33: Cross-Source OMS Home & Asset Drill-Down

## Document control
- **Feature ID:** 33
- **Slug / file:** `F33-cross-source-oms-home-drilldown.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../../business-data-catalog/bdc-requirements-map.html (R-09)`

## 1. Summary
Home experience grouping sources (tables, pipelines, streams) with consistent drill patterns: full page vs drawer per source maturity.

## 2. Problem statement
Users lose context switching between Snowflake-heavy and lighter integrations.

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
### 5.1 Home cards
Counts per category; health indicators.

### 5.2 Snowflake drill
Table list with BDC strip → full-page detail tabs.

### 5.3 Unity / others
List + drawer pattern until parity.

### 5.4 Generic fallback
Short list → detail for immature connectors.

## 6. User stories
- As a user, I land OMS Home and pick Snowflake in two clicks.
- As BDC user, BDC Home tab mirrors card grid inside catalog area.

## 7. Use cases & examples
- Compare asset counts across Snowflake and Unity for migration.

## 8. UX & UI notes
Per R-09 prototype copy in requirements map.

## 9. Data model & API considerations
Aggregated counts endpoint for home.

## 10. Non-functional requirements
Home loads from cache if metadata warehouse slow.

## 11. Acceptance criteria (testable)
- Each datasource tile shows last sync time.
- Drill preserves filter query params where applicable.

## 12. Dependencies
Connectors, F30 navigation decisions.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Parity timeline for drawer vs full page?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
