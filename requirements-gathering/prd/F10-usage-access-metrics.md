# PRD — Feature 10: Usage / Access Metrics

## Document control
- **Feature ID:** 10
- **Slug / file:** `F10-usage-access-metrics.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
Signals from query logs and catalog telemetry: popularity, last access, top users, for prioritization and risk.

## 2. Problem statement
Stewards guess what matters; unused assets stay over-documented while hot paths lack care.

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
### 5.1 Ingestion
Warehouse access logs, BI tool telemetry where licensed, catalog view events.

### 5.2 Rollups
7/30/90 day windows; PII-safe aggregation.

### 5.3 Presentation
Sparkline or counts on asset; leadership dashboards.

## 6. User stories
- As a steward, I sort domain inventory by last query date.
- As leadership, I see MAU for catalog.

## 7. Use cases & examples
- Deprecation campaign targets tables with zero reads in 12 months.

## 8. UX & UI notes
Column on inventory optional; tooltip definitions for metric source.

## 9. Data model & API considerations
Read-only metrics endpoints; export for analytics team.

## 10. Non-functional requirements
Latency tolerances for batch vs near-real-time clearly documented.

## 11. Acceptance criteria (testable)
- Metrics never expose row-level data.
- Metric definitions versioned and visible to users.

## 12. Dependencies
Data platform agreements for log sharing.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Per-user visibility restricted to admins only?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
