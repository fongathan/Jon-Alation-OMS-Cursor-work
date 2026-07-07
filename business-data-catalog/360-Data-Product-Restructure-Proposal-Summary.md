# 360 Data Product Restructure Proposal — Summary

**Source:** Working doc tabs — Current State, Steward Guide, Taxonomy (Potential Master Data Management Taxonomy), Comparison.  
**Purpose:** Capture the proposal’s intent so Navigator persona lenses and 360 filters align with stewardship direction—not a second org model.

---

## What problem it addresses

Today many **360 Data Products** in Alation (25+ named products) create **fragmentation**: discoverability depends on knowing *where* data lives, cross-domain concepts (e.g. subscriber engagement) span multiple 360s, and metadata consistency is manual.

The proposal compares **four structural futures** (Comparison tab):

| | **Current metadata** | **Future scalable metadata curation** |
|---|----------------------|----------------------------------------|
| **Data domain structure** (balanced # of 360s) | Strongest **current-state** governance: clear ownership, domain boundaries, escalation—but weak cross-360 search and self-service | **Likely long-term target:** keep accountability + metadata/lineage/search across 360s, automation, policy at scale |
| **Collapsed 360s** (fewer combined envs) | Fewer names to navigate but **ownership blur**, weak trust without metadata | Viable **only if** metadata excellence compensates for weaker natural boundaries |

**Direction:** Stay **domain-accountable** (not arbitrary collapse), invest in **metadata-driven discoverability** (Navigator/OMS/626 + AI-assisted curation) so users need not memorize 25 folder names.

---

## Current state (governance model today)

- **One 360 per Data Domain** — ownership-aligned containers, not usage-based grouping.
- **Placement rule:** Dataset goes in the 360 owned by its **Data Domain**, regardless of who consumes it.
- **Accountability:** Owners responsible for definition, quality, metadata completeness, compliance.
- **Standardization across all 360s:** Foundation / Conformed / Analytics / Legacy schemas; required metadata (definitions, lineage, business context, sensitivity); Business Glossary alignment; **table-level** Business + Technical stewards on every table.
- **Discoverability intent:** Users should find data via **search, relationships, metadata**—not only by browsing 360 folders (today’s gap).
- **Trade-off:** One business concept may sit in **multiple 360s** (Playback, Session, Engagement, Subscriber, etc.); cross-domain analysis requires multi-360 navigation unless metadata matures.
- **Consolidation of domains:** Not a default fix—only when ownership/stewardship already shared and business functions unified.

---

## Proposed taxonomy (concept-driven restructure)

The **Potential Master Data Management Taxonomy** collapses today’s Alation 360 list into **nine groupings** (eight active + Legacy). Placement is **concept-driven** (what data describes and how it’s used), with steward guide rules for due diligence before new assets or new 360s.

| # | **Proposed 360 bucket** | **What it holds** | **Collapses (examples)** |
|---|-------------------------|-------------------|---------------------------|
| 1 | **People & Accounts** | Who the customer is, identity, subscription, access, payments, value | Subscriber, Subscriber_Hulu (legacy), Identity, Perks, Payments; Fraud (standalone or under Payments) |
| 2 | **Content & Catalog** | Titles, episodes, sports, catalog metadata, what users can watch | Content, Content_Hulu (legacy), Sports_Affinity, ESPN |
| 3 | **Experience & Behavior** | Sessions, journeys, playback, engagement, experiments | Session, Session_Hulu (legacy), Playback, Engagement, Engagement_DGTL, Experiment |
| 4 | **Marketing & Audience** | Acquire, target, campaigns, ads, activation, CRM-style audience | Acquisition, Campaign, Audience, Ads, Activation |
| 5 | **Platform & Operational** | Platform metadata, lineage, observability, cost, runtime ops | Data_Platform, Data_Observe, Cost, DEMO (merge/deprecate) |
| 6 | **Regional & Market** | Territory-specific overlays on global structures | LATAM, INTAL |
| 7 | **Commerce & Merchandising** | Offers, merchandising, commercial products (not account fundamentals) | Merchandising; Perks (dual-anchored—home here or People & Accounts) |
| 8 | **Transitional & Unassigned** | Short-term only: ownership TBD, evaluation | Bridge, ESPN_BET (delete), new 360s until steward finalization |
| 9 | **Legacy (potential)** | Frozen pipelines/regulatory continuity—no new assets | Content_Hulu, Session_Hulu, Subscriber_Hulu, ESPN_BET, DEMO, frozen futures |
| — | **Atlas** | External to this exercise | — |

**Steward guide highlights:** Search existing 360s before classifying; producers virtualize in `PUBLISH`; naming `productacronym.schema.table`; Transitional/Unassigned/Legacy rules with timelines and modern equivalents.

---

## Implications for Navigator

- **Persona picker** = **role lens** (how I work)—not a 360 name and not stewardship.
- **360 filter** = **proposed taxonomy buckets** (7–8 for consumers; Transitional/Legacy backstage).
- **Physical 360 count** may stay domain-aligned for Snowflake/governance; **Navigator UX** exposes the **collapsed conceptual buckets** plus metadata search across them—matching “Data domain structure + future metadata curation” quadrant.

---

## One-line positioning

> **Ownership and stewardship stay at the domain/table level; Navigator and metadata make the restructured conceptual 360 map navigable without 25 tiles.**
