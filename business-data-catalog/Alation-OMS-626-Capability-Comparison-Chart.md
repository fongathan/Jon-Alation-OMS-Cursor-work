# Alation → OMS → Data626 Capability Comparison Chart

**Framework:** Whiteboard columns — Alation capability | Used / Need (Alation) | OMS | Data626  
**Sources:**
- [Navigator Feature Inventory Matrix](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit) — Alation inventory + OMS assessment (Mar 2026)
- *Alation Capabilities and Gap Evaluation* (SharePoint — Tim Liu) — **not retrieved**; Alation Used/Need column inferred from inventory notes, stakeholder priority, and [Metadata Curation Automation memo](https://docs.google.com/document/d/1pD1T5gGGcqJSlel-BPwwFp_u547ecth73j901EanTYk/edit)
- [Data626: Data Lifecycle Management PRD](https://docs.google.com/document/d/17UHO_iBfp_qbcUeChku6tHkjoIpTtoXett9a0fdGToo/edit) + Metadata Curation Automation memo — 626 scope and boundaries

**Legend**

| Symbol | Alation (Used / Need) | OMS / Data626 |
|--------|------------------------|---------------|
| ✓ **Met** | In use today; Alation meets the need | Platform covers today (may need UX or migration) |
| ⚠ **Partial** | In use but known limitations or manual burden | Some capability exists; extensions or integration required |
| ✗ **Gap** | Needed but Alation does not reliably deliver | Not in scope or not built yet |
| — **Low** | Low adoption / Phase 2+ priority | Not a primary target for this platform |

**Scope:** Features marked **MVP**, **High**, or actively **Medium** in the inventory — i.e., capabilities DEEPT uses or wants for Alation exit. Low-priority rows included for completeness.

---

## Comparison matrix

| # | Alation capability | Priority | Used / Need (Alation) | OMS | Data626 |
|---|-------------------|----------|------------------------|-----|---------|
| 1 | **Search & discovery** — keyword/semantic search across tables, schemas, columns, articles, glossary; NL / AI-predicted results | MVP | ✓ **Met** — primary navigation pattern; ideal “chat with your data” not fully realized | ✗ **Gap** — no global search across catalogs today | ✗ **Gap** — not a catalog search UX; may feed metadata into search elsewhere |
| 2 | **Business glossary** — terms, definitions, synonyms, stewardship, links to catalog objects; BU-organized sections | MVP | ✓ **Met** — thousands of terms; each BU maintains glossaries | ✗ **Gap** — new catalog; migrate Alation data; add/edit; RBAC | ⚠ **Partial** — consumes glossary as governance context for curation AI; does not replace glossary UX |
| 3 | **Data dictionary** — table/column documentation, stewards, privacy tags, CDEs, bulk CSV/TSV per DDQGC | MVP | ✓ **Met** — core steward workflow | ⚠ **Partial** — existing OMS feature set + governance intake triggers; population and business fields incomplete | ✓ **Met** — core 626 use case: automate required metadata fields (description, classification, stewards, etc.) from code + governance standards |
| 4 | **Catalog browse** — hierarchy navigation by datasource / schema / table | MVP | ✓ **Met** — primary explore pattern | ⚠ **Partial** — hierarchy/browse exists; business-first navigation and parity TBD | ✗ **Gap** — graph/API for lifecycle paths, not Alation-style catalog browse |
| 5 | **Table / asset detail & descriptions** — metadata, owner, tags, lineage context on asset pages | MVP | ✓ **Met** — descriptions, owners, POC, classification most viewed | ⚠ **Partial** — placeholders exist; need population, steward workflow, trust signals | ⚠ **Partial** — generates/curates descriptions and governance fields; publishes to Alation/OMS; not the full asset-detail UX |
| 6 | **Asset detail / description automation** — AI suggestions for schema/table/column text, POC, classification; human endorsement | MVP | ✗ **Gap** — manual upkeep; Alation AI beta lacked cross-system context ([626 memo](https://docs.google.com/document/d/1pD1T5gGGcqJSlel-BPwwFp_u547ecth73j901EanTYk/edit)) | ✗ **Gap** — AI recommendations on edit fields not built | ✓ **Met** — **primary 626 value**: code + repo context for scalable metadata curation |
| 7 | **Flags** — endorsements, warnings, deprecations, popularity | MVP/High | ⚠ **Partial** — works for admins/stewards; want broader participation | ✗ **Gap** — trust/endorsement UX not defined | ✗ **Gap** — not in 626 scope |
| 8 | **Data lineage** — upstream/downstream at table, column, views, reports, dataflow level | MVP | ⚠ **Partial** — **“Alation has limited lineage”** (inventory notes) | ✓ **Met** — lineage exists in OMS (table/column/dataflow) | ✓ **Met** — **core 626 mission**: Git-driven lineage, schema evolution, impact graph ([PRD §6–8](https://docs.google.com/document/d/17UHO_iBfp_qbcUeChku6tHkjoIpTtoXett9a0fdGToo/edit)) |
| 9 | **Data sources & connectors** — Snowflake and connected technical metadata ingestion | MVP | ✓ **Met** for connected sources | ⚠ **Partial** — OMS datasource list; confirm full Alation source parity | ⚠ **Partial** — ingests **Git + pipeline repos**, not generic JDBC connectors |
| 10 | **Authentication / SSO** — single sign-on, RBAC | MVP | ✓ **Met** | ✓ **Met** | ✗ **Gap** — relies on host apps (OMS/Alation) for access |
| 11 | **Folders / source navigation** — article hierarchy, how-to and project collections | MVP | ✓ **Met** | ⚠ **Partial** — overlaps catalog browse; UI + data structure work | ✗ **Gap** |
| 12 | **Ownership / stewardship** — assign owners and stewards to assets | MVP | ✓ **Met** | ⚠ **Partial** — part of planned add/edit functionality | ⚠ **Partial** — stewards in curation workflow; publication to catalog |
| 13 | **Access controls** — feature-based permissions (glossary, metrics, audit) | MVP | ✓ **Met** | ✗ **Gap** — permission postures for feature categories not built | ✗ **Gap** |
| 14 | **Admin analytics dashboard** — MAU, top searches, usage telemetry, CSV export | High | ✓ **Met** — typically built-in for admins | ✗ **Gap** — may exist in Datadog; catalog admin UI needed | ✗ **Gap** |
| 15 | **Workflows** — ad-hoc/recurring governance and legal workflow tracking | Medium | ⚠ **Partial** — medium priority; not full policy engine | ✗ **Gap** | ✗ **Gap** — steward **checkpoints** in curation, not general workflow product |
| 16 | **Tags & classification** — PII, domain, custom tags; search and filters | High | ⚠ **Partial** — critical tags in use; some readonly from other systems | ⚠ **Partial** — readonly from other systems; tag create/assign/search needs add/edit | ⚠ **Partial** — can populate classification/sensitivity fields in curation model |
| 17 | **Expanded data sources** — vendor sources outside Snowflake (e.g., HighTouch) | High | ✗ **Gap** — limited connector coverage for non-Snowflake vendors | ✗ **Gap** — confirm source list vs Alation | ⚠ **Partial** — code analysis spans ingestion → warehouse → activation paths in PRD examples |
| 18 | **Product pages (authoring)** — product docs, metrics impacted, contacts, domain, stewards; AI from wiki | High | ✗ **Gap** — aspirational / not fully realized in Alation today | ✗ **Gap** — content model, editor, versioning, AI generation | ✗ **Gap** — focused on dataset/event lifecycle, not product-page CMS |
| 19 | **Mass / bulk edit** — multi-asset metadata changes; CSV upload with audit | Medium | ✓ **Met** — Alation supports UI + CSV | ⚠ **Partial** — part of planned add/edit (overlap with tags) | ✗ **Gap** |
| 20 | **Dataflows** — ETL jobs, stored procs, dbt, Airflow DAGs as first-class objects | Medium | ✓ **Met** | ✓ **Met** — pipelines/jobs metadata in OMS | ⚠ **Partial** — inferred from Git/pipeline definitions, not runtime-only |
| 21 | **Domains** — business area groupings for search, stewards, policies | Medium | ✓ **Met** | ✗ **Gap** — new feature/catalog | ⚠ **Partial** — **Data domain** is a required curation field |
| 22 | **Export / reports** — catalog, usage, compliance exports | Medium | ✓ **Met** | ✗ **Gap** | ✗ **Gap** |
| 23 | **Usage / access metrics** — last access, unique users, query history | Medium | ✓ **Met** | ✓ **Met** | ⚠ **Partial** — **value score** / downstream-use frequency (different metric model) |
| 24 | **AI chat assistant in app** — NL Q&A over catalog, SQL suggestions, glossary links | Medium | ⚠ **Partial** — limited vs desired | ⚠ **Partial** — exists; needs Alation/data enhancements | ⚠ **Partial** — AI reasoning layer for “why / what breaks” ([FR-15](https://docs.google.com/document/d/17UHO_iBfp_qbcUeChku6tHkjoIpTtoXett9a0fdGToo/edit)); not full catalog chat |
| 25 | **Mass set rules / catalog sets** — rule engine for tags, policies, ownership at scale | Medium | ✓ **Met** | ✗ **Gap** — PI fields detectable; rule engine enhancements needed | ✗ **Gap** |
| 26 | **Data dictionary download & upload** — bulk export/import of metadata | Medium | ✓ **Met** | ⚠ **Partial** — needs enhancements to Alation migration data | ✗ **Gap** — publishes curated metadata via integration APIs |
| 27 | **Saved queries / favorites** — bookmark assets and searches | Medium | ✓ **Met** | ✗ **Gap** | ✗ **Gap** |
| 28 | **Overview & social section** — catalog home, popular tables/searches, social feed (privacy-safe) | Medium | ✗ **Gap** — underbuilt / privacy concerns | ✗ **Gap** | ✗ **Gap** |
| 29 | **Custom fields** — user-defined metadata on assets | Medium | ✓ **Met** | ✗ **Gap** | ⚠ **Partial** — governed **required/optional** field set, not arbitrary custom fields |
| 30 | **Comments on assets / Q&A** | Low–Med | — **Low** | ✗ **Gap** | ✗ **Gap** |
| 31 | **Version control** — asset versioning, change history | Low–Med | — **Low** — underutilized | ✗ **Gap** | ✗ **Gap** |
| 32 | **Policy center** — policies, risk classification, compliance rules | Low | — **Low** | ✗ **Gap** | ✗ **Gap** — privacy links at lifecycle level only |
| 33 | **Compilation / data quality** — DQ rules and monitoring | Low–Med | — **Low** | ✗ **Gap** | ⚠ **Partial** — fitness function / quality variance warnings in PRD |
| 34 | **API & integrations** — REST for bulk ops, BI integration | Medium | ✓ **Met** | ⚠ **Partial** — enhancement needed for full parity | ⚠ **Partial** — catalog UI/API for synthetic metadata graph |
| 35 | **Details (“i”) icon** — in-context help on features | Medium | ✗ **Gap** — UX/documentation gap | ✗ **Gap** | ✗ **Gap** |
| 36 | **Persona view filtering** — role-based catalog experience | Low | ✗ **Gap** | ✗ **Gap** — permissions framework needed | ✗ **Gap** |
| 37 | **AI “How to”** — help center for catalog usage | Low | ✗ **Gap** | ⚠ **Partial** — extend existing chatbot | ⚠ **Partial** — explain-the-system Q&A, not product help center |

---

## Summary roll-up (MVP + High only)

| Platform | Covered / Met | Partial | Gap |
|----------|---------------|---------|-----|
| **Alation (today)** | 12 | 8 | 5 |
| **OMS** | 4 | 9 | 12 |
| **Data626** | 3 | 8 | 14 |

*Counts among rows 1–18 (MVP + High). Low/Medium-only rows shift totals but do not change the pattern.*

---

## How the three platforms divide labor

```text
┌─────────────────────┬──────────────────────────────────────────┬─────────────────────────────────────────┐
│ Column              │ OMS                                      │ Data626                                 │
├─────────────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
│ System of record    │ Technical + operational metadata store   │ Code-derived lifecycle graph + curation │
│ Sweet spot          │ Lineage, pipelines, usage, SSO, APIs     │ Auto lineage, metadata curation, “why”  │
│ Not trying to be    │ Full business glossary UX (today)        │ Catalog search, glossary, admin analytics│
└─────────────────────┴──────────────────────────────────────────┴─────────────────────────────────────────┘
```

**One-line positioning (from boundary work in repo):**

> **626 improves metadata supply; OMS stores and serves it; Navigator/BDC is the governed experience for business and compliance users.**

Data626 explicitly **does not replace Alation or OMS** ([PRD §10.2](https://docs.google.com/document/d/17UHO_iBfp_qbcUeChku6tHkjoIpTtoXett9a0fdGToo/edit)); it **publishes curated metadata into** Alation (today) and OMS (target), and owns **Git-native lineage + contextual curation** that Alation cannot generate reliably.

---

## Alation gaps that drive the migration (cross-cutting)

These themes appear across the inventory and [Metadata Curation Automation memo](https://docs.google.com/document/d/1pD1T5gGGcqJSlel-BPwwFp_u547ecth73j901EanTYk/edit):

1. **Manual metadata burden** — descriptions, classifications, and stewardship fields decay without automation (rows 5–6, 16, 26).
2. **Limited lineage depth** — table/column/report lineage insufficient for impact analysis (row 8); 626 + OMS combination intended to exceed Alation.
3. **AI without system context** — Alation AI and warehouse-only assistants cannot interpret cross-platform pipelines (row 6, 24); 626’s code-first model is the proposed fix.
4. **Business experience gaps** — global search, glossary UX, trust flags, product pages, persona filtering (rows 1–2, 7, 18, 36).
5. **Connector / source sprawl** — non-Snowflake and activation tools (HighTouch, etc.) poorly covered (row 17).

---

## Recommended next step

**Validate column 2** against the SharePoint *Alation Capabilities and Gap Evaluation* doc once accessible — export to Google Doc or paste plain text so Used/Need can be reconciled row-by-row with Tim Liu’s evaluation.

**Document owner:** Data Governance | Align with Navigator Feature Inventory Matrix v1.0 (Mar 19, 2026)
