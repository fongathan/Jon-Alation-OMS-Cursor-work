# Data Navigator — Prioritized Features & Three-Phase Roadmap

**Mickey / Data Governance program** · Companion to Google Slides: [Data Navigator — from Alation to new in-house business metadata experience & capabilities](https://docs.google.com/presentation/d/1OdzAIMxb2gE4n36-8UoYhWXWg-4nzVF4m3i8V9XWYRw/edit) (`presentation_id` `1OdzAIMxb2gE4n36-8UoYhWXWg-4nzVF4m3i8V9XWYRw`)

**Document control**

| Field | Value |
|--------|--------|
| **Purpose** | Single place for **business-oriented feature definitions**, **prioritization**, and a **three-phase roadmap** with **personas per phase**. |
| **How this was built** | The **All Google MCP** `slides_get_presentation` tool returns **titles and slide IDs only**, not on-slide text. This document therefore **aligns to the deck’s stated title and program intent** and is **grounded in workspace artifacts** listed in §0. **Reconcile wording** with the live deck after export or stakeholder review. |
| **Primary inputs** | `requirements-gathering/slides/data-source-navigator-value-deck-3-slides.html`, `In-House-Data-Catalog-Pitch-Deck.md`, `requirements-gathering/1-Feature-Inventory-Matrix.md`, `business-data-catalog/Navigator-persona-and-626-boundary-brief.md`, `business-data-catalog/unified-governance-privacy-stakeholder-ui.md`, `Product-Brief-Alation-to-OMS-Migration.md`. |

---

## 0. Traceability (workspace)

| Topic | Path |
|--------|------|
| Alation → OMS scope & contract pressure | `Product-Brief-Alation-to-OMS-Migration.md` |
| MVP vs later themes (leadership pitch) | `In-House-Data-Catalog-Pitch-Deck.md` |
| Full feature inventory & priority hints | `requirements-gathering/1-Feature-Inventory-Matrix.md` |
| BDC / Navigator definitions & FY27 value narrative | `requirements-gathering/slides/data-source-navigator-value-deck-3-slides.html` |
| 626 vs OMS vs Navigator boundaries & persona stories | `business-data-catalog/Navigator-persona-and-626-boundary-brief.md` |
| Governance “command center” + catalog spine IA | `business-data-catalog/unified-governance-privacy-stakeholder-ui.md` |
| BDC shell / nav (F30) | `requirements-gathering/prd/F30-oms-bdc-navigation-ia.md` |

---

## 1. Product definitions (business language)

| Term | Definition |
|------|------------|
| **Data catalog** | Where teams **discover** assets (tables, pipelines, streams, reports), read **business meaning** (definitions, ownership, classifications, quality signals), and follow **lineage** for impact and compliance. Connects stewardship, policy, and production metadata. |
| **OMS** | **Operational Metadata Store** — Disney’s internal platform that **stores and serves** technical/operational metadata and APIs; backbone for inventory and lineage. |
| **Business Data Catalog (BDC) / Data Navigator** | The **in-house, business-first experience** on top of OMS: governed discovery, glossary, stewardship UX, and policy surfacing — **not** a duplicate metadata store. Positioning: *626 improves metadata supply; OMS stores and serves it; Navigator is the governed experience for the right persona* (`Navigator-persona-and-626-boundary-brief.md`). |
| **AI-readiness (catalog)** | A **defined attribute set** on assets (e.g. quality tier, lineage completeness, access classification, documented limitations) so AI and analytics teams can pick **steward-attested** inputs without tribal knowledge (`data-source-navigator-value-deck-3-slides.html`). |

---

## 2. Personas (reference set)

Use this set consistently when reading the priority table and roadmap.

| Persona | Job-to-be-done (one line) |
|---------|---------------------------|
| **Business / DNA consumer** | Find and **trust** the metric or dataset for a business question, quickly. |
| **Data analyst / BI** | Discover, compare, and use assets with clear definitions and lineage before building. |
| **Data engineer** | Rely on **technical truth**, lineage, and integrations; reduce ad hoc “where is X?” noise. |
| **Data steward / owner** | Curate, endorse, reconcile definitions; run **workloads at scale** (bulk, rules, attestations). |
| **Governance / compliance** | Evidence-friendly views: classification, policy linkage, exports, audit narrative. |
| **Platform / DRE (API-first)** | Stable contracts for automation — bulk load, metadata sync, agents — not only UI. |
| **Leadership / program** | Portfolio posture: coverage, adoption, risk concentration — without losing specialist tools. |

---

## 3. Prioritized feature list (business definitions)

**Priority legend**

| Tier | Meaning |
|------|---------|
| **P0 — Exit / parity** | Required to **replace Alation** for daily work and meet **Oct 1, 2026** contract reality; loss unacceptable without signed substitute. |
| **P1 — FY27 scale** | Needed for **coverage expansion**, **AI-readiness**, and **operating-model** habits; high value shortly after parity. |
| **P2 — Differentiate** | Semantic layer integration, deeper automation, unified governance shell — **after** catalog trust is established. |

| ID | Priority | Feature | Business definition (outcome) | Primary personas | Notes / dependencies |
|----|----------|---------|------------------------------|------------------|----------------------|
| F01 | P0 | **Unified search & discovery** | Users answer “what exists?” across **technical and business objects** (tables, columns, glossary, docs) in one search, with filters that reflect trust and domain. | Consumer, Analyst, Engineer, Steward | Must not be “Snowflake-only technical search”; parity per pitch deck. |
| F02 | P0 | **Hierarchical catalog browse** | Users explore **datasource → schema → table → column** without knowing exact names — matches mental model from Alation. | Analyst, Engineer, Consumer | OMS strength: leverage existing technical inventory. |
| F03 | P0 | **Asset detail (table / column / pipeline)** | One screen shows **description, business description, owners/stewards, tags, lineage entry points** so a consumer can decide “can I use this?” | Consumer, Analyst, Engineer, Steward | “Metadata-first” — business fields must be populated, not hollow placeholders. |
| F04 | P0 | **Business glossary** | Organization shares **one vocabulary**: terms, definitions, synonyms, stewardship — **linked to catalog assets** so language and inventory stay connected. | Steward, Compliance, Consumer | High migration fidelity risk if links break. |
| F05 | P0 | **Data lineage (table +)** | Users see **upstream/downstream** context for impact analysis and compliance traceability; depth as validated (table minimum; column/dataflow where required). | Analyst, Engineer, Compliance | Parity vs actual Alation usage to be validated in interviews. |
| F06 | P0 | **Tags, domains, custom fields** | **Classify and scope** assets for governance, search, and reporting; supports domain operating model. | Steward, Compliance, Engineer | Includes bulk paths (see F14). |
| F07 | P0 | **Trust signals (endorse / warn / deprecate)** | Catalog communicates **intended use** and risk — trusted gold paths vs deprecated assets. | Consumer, Steward, Compliance | Called out in inventory matrix as in use. |
| F08 | P0 | **Ownership & stewardship assignment** | Every critical asset has **accountable owners** visible in UI and reports. | Steward, Compliance, Leadership | Federated stewardship model compatibility. |
| F09 | P0 | **Documentation / articles** | Narrative knowledge (how-to, domain context) is **first-class**, linkable to assets, with sensible IA (folders/collections). | Steward, Analyst, Consumer | Map from Alation articles during migration. |
| F10 | P0 | **SSO & governance-ready access** | **Enterprise authentication** and role-aware access so sensitive metadata operations are controlled and auditable. | All | Non-negotiable baseline. |
| F11 | P0 | **Deep link & handoff to OMS** | BDC/Navigator remains **composable**: users can drop to **full technical / lineage** context in OMS without losing place. | Engineer, Analyst | “One metadata API, two shells” per value deck. |
| F12 | P1 | **Requests / lightweight workflows** | Stewards handle **questions, changes, and attestations** in-system instead of shadow queues (exact scope per OMS/BDC roadmap). | Steward, Analyst, Compliance | Align with `F30` and BDC prototype areas (Requests). |
| F13 | P1 | **Policies surface in catalog** | Users see **policy ↔ classification ↔ asset** linkage for explainable use (privacy, retention, purpose where modeled). | Compliance, Steward, Consumer | Tied to Policy Center–class capabilities from inventory. |
| F14 | P1 | **Bulk edit, catalog sets / rules, dictionary import-export** | Governance runs at **hundreds of assets**: CSV/rule-based updates with **audit trail**. | Steward, Platform | Marked high in feature inventory; operational necessity at scale. |
| F15 | P1 | **Usage / access signals (where available)** | Leaders and compliance prioritize work using **consumption and attention** signals tied to assets. | Leadership, Compliance, Engineer | Medium in matrix — phase after core trust. |
| F16 | P1 | **AI-readiness attributes** | Catalog exposes **quality tier, lineage completeness, access classification, limitations** for AI/analytics intake. | Consumer, AI product, Compliance, Steward | Named Q2 FY27 direction in value deck. |
| F17 | P1 | **Saved searches / favorites** | Power users **bookmark** recurring discovery paths. | Analyst, Steward | Medium priority in matrix. |
| F18 | P2 | **Governance & privacy command center (shell)** | **Unified posture** across pillars (privacy, DSAR, remediation, ops, metrics) with **exceptions queue** and deep links — catalog as **spine**, not silo (`unified-governance-privacy-stakeholder-ui.md`). | Leadership, Compliance, Steward | Experience layer; depends on cross-pillar data contracts. |
| F19 | P2 | **Semantic layer ↔ catalog integration** | **Single governed truth** for metrics shared across BI and data platforms (Q4 FY27 horizon in value deck). | Consumer, Analyst, Steward | Requires semantic layer program alignment. |
| F20 | P2 | **Advanced analytics & recommendations** | Admin telemetry, **AI-suggested** stewardship actions — only after attribution/governance rules clear. | Leadership, Steward | Matrix: lower adoption today; avoid premature parity. |

---

## 4. Roadmap — three phases (personas + features)

Phasing is **outcome-based**: **parity & exit** → **scale & AI-readiness** → **platform differentiation & unified governance**. Dates echo `data-source-navigator-value-deck-3-slides.html` and `Product-Brief-Alation-to-OMS-Migration.md`; adjust to your official program calendar.

### Phase 1 — **Trust & exit** (Alation parity · primary window through **Oct 1, 2026**)

**Theme:** “Users can do their job without Alation.” Migration-safe, interview-validated parity.

| Personas (primary) | Personas (secondary) |
|---------------------|----------------------|
| Data analyst / BI, Data engineer, Data steward | Business consumer, Compliance (read-heavy), Platform |

**Features (target completion):** F01–F11 (full P0 set). **Acceptance posture:** search/browse/detail + glossary + lineage + tags/domains/custom fields + trust flags + stewardship + articles + SSO + OMS handoff; bulk/dictionary paths at least **MVP** where stewards cannot operate otherwise (minimum slice of F14 if validation demands).

**Success signals:** steward UAT sign-off; parallel run metrics; % critical glossary/links validated post-load; reduced “where is X?” escalations.

---

### Phase 2 — **Operate at scale** (roughly **Q2 FY27** horizon for coverage + AI-readiness)

**Theme:** “Catalog is how we **run** governance and AI preparation — not only where we **read** metadata.”

| Personas (primary) | Personas (secondary) |
|---------------------|----------------------|
| Data steward, Governance / compliance, Business consumer | Data engineer, Leadership |

**Features:** F12–F17 — requests/workflows, policy surfacing, **bulk/rules/dictionary** at production strength, usage signals where reliable, **AI-readiness attributes**, saved views. Extend **domain coverage** beyond initial baseline (value deck: priority domains with AI, compliance, or high PII concentration).

**Success signals:** OKR-style measures from value deck — domain coverage %, active stewardship %, self-service rate, AI-readiness adoption %, use-case traceability %.

---

### Phase 3 — **Differentiate & compose** (from **Q4 FY27** onward; continuous)

**Theme:** “One **governed** story from metric definition to production asset — and a coherent **enterprise governance** experience.”

| Personas (primary) | Personas (secondary) |
|---------------------|----------------------|
| Leadership, Compliance / privacy leads, Product / AI | Steward, Analyst |

**Features:** F18–F20 — **governance command center** (unified overview + exceptions + catalog health strip), **semantic layer integration**, deeper **automation** (policy-driven metadata, richer recommendations), expanded **API consumption** by downstream tools and agents.

**Success signals:** % of AI systems/reports consuming steward-approved metadata; audit/evidence packs without manual screenshot culture; semantic conflicts detectable and reconciled in catalog-linked workflows.

---

## 5. One-page roadmap visual (ASCII)

```
Phase 1  TRUST & EXIT          Phase 2  OPERATE AT SCALE        Phase 3  DIFFERENTIATE
(→ Oct 2026)                  (~Q2 FY27+)                    (~Q4 FY27+)
─────────────────────         ─────────────────────          ─────────────────────
Personas: analyst,            Personas: steward,             Personas: leadership,
engineer, steward             compliance, consumer           compliance, AI product

Features: F01–F11             Features: F12–F17              Features: F18–F20
(+ min F14 if required)       + coverage expansion           + semantic layer
                              + AI-readiness attrs           + command center shell
```

---

## 6. Validation checklist (before treating this as “deck-official”)

- [ ] Walk slide-by-slide against exported PDF/PPTX and align **feature names** and **phase boundaries** to speaker notes.
- [ ] Confirm **P0** bulk/rules scope with stewards (F14 minimum bar).
- [ ] Confirm **lineage depth** (F05) vs actual Alation usage by persona.
- [ ] Attach **program IDs / OKRs** to Phase 2 metrics row for executive reporting.

---

*Mickey — document synthesized from workspace program artifacts referencing the same Google Slides deck; slide text not machine-readable via current MCP.*
