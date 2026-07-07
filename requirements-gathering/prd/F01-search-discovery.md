# PRD — Feature 1: Search & Discovery

## Document control
- **Feature ID:** 1
- **Slug / file:** `F01-search-discovery.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## Related workspace artifacts
- `../1-Feature-Inventory-Matrix.md`
- `../../business-data-catalog/bdc-requirements-map.html (R-01)`

## 1. Summary
Unified discovery across technical and business metadata so users can find tables, columns, articles, glossary terms, and related assets quickly.

## 2. Problem statement
Users waste time hunting across sources, wikis, and chat without a single query surface aligned to how DSS names and organizes data.

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
### 5.1 Global search entry
Prominent search in shell/header; keyboard shortcut optional; scope indicator (all sources vs current datasource).

### 5.2 Index & ranking
Keyword match on names, descriptions, tags, stewards, glossary terms; optional semantic/vector tier later; de-duplicate logical entities.

### 5.3 Scoped filters
Post-search facets: domain, environment, sensitivity, owner, object type, trust flag.

### 5.4 Result cards / rows
Title, type badge, 1-line description, steward, key tags, datasource; click opens asset context.

### 5.5 Zero-result & disambiguation
Suggestions, synonym expansion from glossary, clear empty state.

## 6. User stories
- As an analyst, I search for a business concept and land on the canonical table and glossary definition.
- As a steward, I search within my domain to find undescribed assets to prioritize.
- As an engineer, I search by pipeline or dataset name and open lineage in one step.

## 7. Use cases & examples
- New hire looks up 'subscriber revenue' and finds the approved metric table plus policy notes.
- Compliance officer searches for PII-tagged assets under a program code.

## 8. UX & UI notes
Header search + full-width results page; facet panel; saved scope presets (phase 2).

## 9. Data model & API considerations
Search API returning typed hits with snippets and facet counts; rate limits for automation.

## 10. Non-functional requirements
P95 search under agreed SLA; audit log for sensitive scopes if required by policy.

## 11. Acceptance criteria (testable)
- Given indexed assets, when user types a known table name then the asset appears in top 5 results.
- When user applies domain facet, only in-domain assets show.
- Search respects RBAC: user never sees forbidden object titles/snippets.

## 12. Dependencies
Ingestion completeness, RBAC model, glossary synonym graph.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Semantic search in MVP or phase 2?
- Cross-tool search (Confluence) in scope?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
