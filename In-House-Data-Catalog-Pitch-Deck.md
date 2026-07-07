# In-House Data Catalog: Requirements & Migration Pitch

**Audience:** Leadership & partners | **Context:** Alation → OMS (Operational Metadata Store) | **Updated:** March 26, 2026

---

## Slide 1 — The move in one sentence

We are replacing the external **Alation** data catalog with **Disney’s internal OMS** as the system of record for Data Governance—so we keep enterprise alignment, reduce vendor lock-in, and preserve the business metadata and workflows teams rely on today.

**Contract context:** Alation end date **October 1, 2026** — migration must be planned against that constraint (parallel run / extension as needed).

---

## Slide 2 — What we valued in Alation (capability pillars)

These are the **main things we got from Alation** that any in-house solution must cover (parity or agreed substitute):

| Pillar | What Alation delivered |
|--------|-------------------------|
| **Discovery** | Full-catalog search; browse datasources → schema → table → column; filters and relevance |
| **Business context** | Business glossary (terms, synonyms, links to assets); rich articles / documentation |
| **Trust & classification** | Tags, custom fields, domains, flags (endorse/warn/deprecate), stewardship and ownership |
| **Lineage & pipelines** | Table/column/dataflow lineage; visibility into jobs (e.g. Airflow, dbt) where connected |
| **Scale operations** | Bulk edit, catalog sets / rules, data dictionary download/upload, admin analytics |
| **Governance** | Policy center, compliance-oriented workflows; SSO and role-based access |

*Source: Feature inventory and Alation functionality reference — validate “in use” per feature with stakeholders.*

---

## Slide 3 — Requirements: the new in-house catalog must…

**Must-have (MVP / parity):**

1. **Search & discovery** across technical *and* business objects (tables, columns, glossary, docs—not only Snowflake rows).
2. **Business glossary** with terms, definitions, synonyms, and **links to catalog assets**.
3. **Asset detail** that surfaces description, business description, owners/stewards, tags, and lineage in the UI users expect.
4. **Data lineage** at the level teams use today (table at minimum; column/dataflow where required).
5. **Tags, domains, and custom fields** with bulk update paths (UI + import/export).
6. **Documentation / articles** (or equivalent) with sensible information architecture (e.g. folders/collections).
7. **Authentication** (SSO) and **governance-ready** auditability for sensitive metadata operations.

**Phase 2+:** Deeper policy workflows, enhanced analytics, AI-assisted discovery, tighter data quality hooks—**after** critical parity is signed off.

---

## Slide 4 — OMS as the platform: leverage vs build

- **Leverage:** OMS already holds **large-scale technical inventory** (tables, pipelines, streams, reports across Snowflake, Delta, Hive, Harmony, Airflow, etc.) and exposes **lineage entry points** in the UI.
- **Extend / populate:** Business fields (descriptions, glossary, tags, usage metrics, Airflow linkage, ownership) are often **placeholders or empty** today—they need **product + integrations + stewardship**, not only a one-time copy.
- **Net-new where missing:** Glossary, business-context search, bulk/rule-based governance patterns, and policy-style workflows may require **explicit roadmap** items with the OMS team.

*Principle: metadata-first—business context is the hardest to recreate if lost.*

---

## Slide 5 — Migration: Alation → OMS (high level)

| Phase | Focus |
|-------|--------|
| **1. Inventory & extract** | Export glossary, articles, tags, custom fields, lineage references, domains, flags; map to OMS model |
| **2. Transform & load** | Field mapping, validation rules, reconciliation reports |
| **3. Parallel run** | Alation + OMS both available; UAT by stewards and power users |
| **4. Cutover** | Redirect users, freeze writes in Alation, OMS becomes primary |
| **5. Decommission** | Archive, retire Alation; close out contract |

**Dependencies:** Alation API/access for extraction, OMS APIs for load, clear **owners** for data quality at each step.

---

## Slide 6 — Success looks like

| Measure | Target direction |
|---------|------------------|
| **Metadata preservation** | High % of glossary, tags, descriptions, and critical links validated post-migration |
| **Adoption** | Majority of current Alation users active in OMS shortly after cutover |
| **Findability** | Search and browse cover business + technical needs (feedback + usage signals) |
| **Stewardship** | Ongoing updates happen in OMS (not shadow spreadsheets) |
| **Risk** | No undetected loss of **high-priority** governance metadata |

---

## Slide 7 — Risks (and how we manage them)

| Risk | Mitigation |
|------|------------|
| Incomplete requirements | Structured interviews, feature matrix sign-off, screenshot evidence |
| OMS roadmap mismatch | Early partnership with OMS; phased MVP |
| Migration fidelity | Validation checkpoints, parallel run, rollback plan |
| Timeline vs contract | Prioritize MVP; extension for parallel run if needed |
| Change fatigue | Training, champions, clear “where to do X now” guidance |

---

## Slide 8 — Ask

1. **Alignment** on MVP parity scope (what “good enough” is before Oct 2026 vs Phase 2).
2. **Resourcing** for requirements validation, migration tooling, and OMS co-development.
3. **Decision** on contract / parallel-run window so cutover is **data-safe**, not just date-driven.

---

*This deck summarizes themes from the Product Brief, Feature Inventory Matrix, and Alation-to-OMS Migration Project Plan. Use the detailed documents for execution.*
