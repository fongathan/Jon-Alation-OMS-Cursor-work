# Feature Inventory Matrix
**Alation to OMS Migration — Current Use Documentation**  
**Disney Streaming Services** | **Version:** 1.0 | **Date:** March 19, 2026

---

## Purpose

This matrix documents every Alation feature in use today at DSS. Use it to ensure no functionality is lost during migration to OMS. Validate each row with stakeholders and update the "In Use" and "Usage Notes" columns during interviews.

---

## Feature Inventory

| # | Feature | Description | In Use? | Usage Frequency | Primary Use Case | Priority for OMS | Notes |
|---|---------|-------------|---------|-----------------|------------------|------------------|------|
| 1 | **Search & Discovery** | Keyword and semantic search across tables, schemas, columns, articles, glossary terms | ☐ Yes ☐ No | Daily / Weekly / Monthly | Find data assets, understand what exists | High | _Validate: What do users search for most?_ |
| 2 | **Business Glossary** | Terms, definitions, synonyms, stewardship, linked to catalog objects | ☐ Yes ☐ No | Daily / Weekly / Monthly | Standardize terminology, link terms to tables/columns | High | _Validate: How many terms? Who maintains?_ |
| 3 | **Catalog Browse** | Browse datasources, schemas, tables by hierarchy | ☐ Yes ☐ No | Daily / Weekly / Monthly | Explore data by source/schema | High | _Validate: Primary navigation pattern?_ |
| 4 | **Table / Asset Detail** | View metadata for tables, columns: description, owner, tags, lineage | ☐ Yes ☐ No | Daily / Weekly / Monthly | Understand asset context before use | High | _Validate: Which fields are most viewed?_ |
| 5 | **Data Lineage** | Upstream/downstream lineage (table, column, dataflow level) | ☐ Yes ☐ No | Daily / Weekly / Monthly | Impact analysis, data flow understanding | High | _Validate: Table-level vs. column-level usage?_ |
| 6 | **Tags & Classification** | Apply tags (PII, domain, custom) to assets | ☐ Yes ☐ No | Daily / Weekly / Monthly | Classification, filtering, compliance | High | _Validate: Which tags are critical?_ |
| 7 | **Custom Fields** | User-defined metadata fields on assets | ☐ Yes ☐ No | Daily / Weekly / Monthly | Domain-specific metadata | Medium | _Validate: List custom fields in use_ |
| 8 | **Documentation / Articles** | Rich-text documentation linked to catalog objects | ☐ Yes ☐ No | Daily / Weekly / Monthly | How-to guides, data dictionaries | High | _Validate: Article count, structure_ |
| 9 | **Ownership / Stewardship** | Assign owners, stewards to assets | ☐ Yes ☐ No | Daily / Weekly / Monthly | Accountability, escalation | High | _Validate: Steward assignment coverage_ |
| 10 | **Usage / Access Metrics** | Last access, unique users, top users, query history | ☐ Yes ☐ No | Daily / Weekly / Monthly | Usage reporting, prioritization | Medium | _Validate: Who consumes these reports?_ |
| 11 | **Data Sources & Connectors** | Connected datasources (Snowflake, etc.) | ☐ Yes ☐ No | Daily / Weekly / Monthly | Technical metadata ingestion | High | _Validate: Which sources are critical?_ |
| 12 | **Policy Center** | Policies, risk classification, compliance rules | ☐ Yes ☐ No | Daily / Weekly / Monthly | Governance, compliance reporting | Medium | _Validate: Policies in use_ |
| 13 | **Compilation / Data Quality** | Data quality rules, profiling | ☐ Yes ☐ No | Daily / Weekly / Monthly | Quality monitoring | Low–Medium | _Validate: Extent of use_ |
| 14 | **API & Integrations** | REST API for bulk ops, custom metadata, BI tool integration | ☐ Yes ☐ No | Daily / Weekly / Monthly | Automation, tool integration | Medium | _Validate: Which integrations?_ |
| 15 | **Version Control** | Asset versioning, change history | ☐ Yes ☐ No | Daily / Weekly / Monthly | Audit trail, rollback | Low–Medium | _Validate: How often used?_ |
| 16 | **Recommendations / Suggestions** | AI-suggested metadata, stewardship actions | ☐ Yes ☐ No | Daily / Weekly / Monthly | Metadata improvement | Low | _Validate: Adoption level_ |
| 17 | **Saved Queries / Favorites** | Save searches, bookmark assets | ☐ Yes ☐ No | Daily / Weekly / Monthly | Quick access to frequent assets | Medium | _Validate: Usage patterns_ |
| 18 | **Comments / Discussions** | Comments on assets, Q&A | ☐ Yes ☐ No | Daily / Weekly / Monthly | Collaboration, questions | Low–Medium | _Validate: Active use?_ |
| 19 | **Export / Reports** | Export catalog, usage reports, compliance reports | ☐ Yes ☐ No | Daily / Weekly / Monthly | Leadership reporting, audits | Medium | _Validate: Report types_ |
| 20 | **Authentication / SSO** | Single sign-on, role-based access | ☐ Yes ☐ No | N/A (infra) | Access control | High | _Validate: SSO provider_ |
| 21 | **Flags (Endorsements, Warnings, Deprecations)** | Data quality signals on catalog objects (trusted, deprecated, etc.) | ☑ Yes ☐ No | Daily / Weekly / Monthly | Data quality signals | High | Examples: trusted endorsement, deprecated warning |
| 22 | **Domains** | Business area groupings (e.g., Ad Platforms, DEET Data, Atlas) | ☑ Yes ☐ No | Daily / Weekly / Monthly | Business area groupings | High | Used to scope search, assign stewards, and apply domain policies |
| 23 | **Folders** | Article/content hierarchy and organization | ☑ Yes ☐ No | Daily / Weekly / Monthly | Content hierarchy | High | Examples: How-to folder, project-specific article collections |
| 24 | **Dataflows** | ETL/transformation jobs, stored procedures, dbt models, Airflow DAGs | ☑ Yes ☐ No | Daily / Weekly / Monthly | ETL / pipelines | High | Examples: dbt model 'sales_transform', Airflow DAG 'daily_load'. Distinct from lineage: these are the pipeline definitions/executables |
| 25 | **Admin Analytics Dashboard** | Collects telemetry and metadata (searches, views, queries, top assets, user activity); exposes pre-built dashboards and ad-hoc query interface; filters by time, asset type, user, team | ☑ Yes ☐ No | Weekly / Monthly | Usage reporting, analytics | Medium | Admin views MAU, top-searched datasets, runs queries for declining usage; exports CSV. Typically built-in; requires admin role |
| 26 | **Mass/Bulk Edit** | Select multiple assets (checkboxes or saved set) and apply metadata changes (owners, tags, descriptions) in a single operation; supports CSV upload to update many records with audit logging | ☑ Yes ☐ No | Weekly / Monthly | Bulk metadata updates | High | Update owner and add compliance tag to 200 tables at once; import CSV mapping table → owner. Alation supports bulk updates (UI and CSV); requires permission checks and audit trail |
| 27 | **Mass Set Rules / Catalog Sets** | Define rules (pattern, metadata condition) and apply to a set of assets or dynamically create catalog sets; rule engine matches assets and applies tags/policies or assigns ownership at scale | ☑ Yes ☐ No | Weekly / Monthly | Governance automation | High | Create catalog set for all tables with "pii" in column names and auto-apply retention policy and steward. Catalog sets and rule engines available for policy enforcement |
| 28 | **AI Chat Assistant in App** | LLM-backed conversational interface using catalog metadata to answer questions, locate datasets, suggest SQL, and summarize definitions; may use internal knowledge index for sensitive data | ☐ Yes ☐ No | Daily / Weekly | Natural language search, discovery | Medium | User asks "Where is the revenue metric defined?" Assistant returns dataset, column, sample query, glossary links. May be native or add-on depending on version/licence; check privacy/PII and governance settings |
| 29 | **Data Dictionary Download & Uploads** | Download catalog metadata (titles, descriptions, custom fields) for data sources and child objects; upload CSV/Excel to bulk-update field values across many assets | ☑ Yes ☐ No | Weekly / Monthly | Bulk metadata export/import, documentation | High | Download dictionary for analysis or audits; upload to apply steward assignments, descriptions, or custom fields at scale. Supports data dictionary update procedures |

---

## Priority Legend

| Priority | Definition |
|----------|------------|
| **High** | Critical for day-to-day work; must have in OMS MVP |
| **Medium** | Important; include in MVP or Phase 2 |
| **Low** | Nice to have; Phase 2 or later |

---

## Validation Checklist

- [ ] All rows reviewed with at least one stakeholder per persona
- [ ] "In Use" and "Usage Notes" columns completed for each feature
- [ ] Priority confirmed with Data Governance lead
- [ ] Custom fields and tags documented in separate appendix (if many)
- [ ] Integrations and API usage documented

---

## Appendix: Custom Fields in Use (if applicable)

| Field Name | Object Type | Purpose | In Use? |
|------------|-------------|---------|---------|
| _Add rows as discovered_ | | | |

---

## Appendix: Tags in Use (if applicable)

| Tag Name | Category | Purpose | Asset Count (approx.) |
|----------|----------|---------|------------------------|
| _Add rows as discovered_ | | | |

---

*Document owner: Data Governance | Update after stakeholder interviews*
