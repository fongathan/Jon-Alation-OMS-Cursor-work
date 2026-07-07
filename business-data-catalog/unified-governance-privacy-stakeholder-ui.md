# Unified Data Governance & Privacy Stakeholder Experience — UI Draft

**Purpose:** Readable companion to the analysis of a single **governance command center** that sits above existing workstream dashboards (privacy compliance, DSAR, tracker remediation, operations, metrics).

**Source context:** Google Slides deck *“Data Navigator — from Alation to new in-house business metadata experience & capabilities”* (`presentation_id` `1OdzAIMxb2gE4n36-8UoYhWXWg-4nzVF4m3i8V9XWYRw`). Slide-level text was not available via the Slides MCP API; pillar names below follow the stakeholder list you provided.

**Related workspace material:** `business-data-catalog/BDC-OMS-integrated-vs-on-top-decision.md`, `business-data-catalog/oms-ui-on-top.html` (Catalog, Glossary, Policies, Requests, Workflows framing).

---

## 1. Problem statement

Each governance and privacy area already has **its own dashboard**. Navigation historically collapsed to **a single entry**, so stakeholders could not see an **overall governance experience**—only deep tools in isolation.

**Goal:** One coherent **mental model** and **shell** that shows posture and workload across pillars, then **hands off** to the right specialist surface with context preserved—not one screen that replaces five products.

---

## 2. Big picture: three layers

Stakeholders should feel these as one product, implemented as layered responsibilities:

| Layer | Role | What it is *not* |
|--------|------|-------------------|
| **Governance & privacy command center** | Answers: *Are we in policy? Where is risk concentrated? What needs a human this week?* Mostly signals, exceptions, SLAs, and deep links. | A duplicate of every chart in every downstream system. |
| **Workstream consoles** | Privacy compliance, DSAR, tracker remediation, operations, metrics—**existing depth** retained. | Hidden behind a generic “Dashboards” list with no story. |
| **Catalog / metadata spine (Data Navigator / OMS / BDC)** | Shared objects: assets, classifications, policies, owners, lineage. Makes the command center **auditable**: exceptions drill to the same records stewards attest. | A separate silo that never links to operational tools. |

**Principle:** *One navigation story* = **Governance home → pick a pillar or an exception → land in the right tool already filtered** (time range, domain, severity), not “one mega-dashboard.”

---

## 3. Information architecture (navigation)

### 3.1 Primary app shell

- **Top bar:** Product name (e.g. **Data Navigator — Governance** or **Privacy & Data Governance Hub**), global search (people, policies, assets, open cases), user or role context (privacy vs enterprise governance if entitlements differ).
- **Left rail (persistent):**
  - **Overview** (default) — unified experience
  - **Privacy compliance**
  - **DSAR**
  - **Tracker remediation**
  - **Operations**
  - **Metrics** (or **Reporting**)
  - **Divider**, then catalog spine shortcuts aligned with the BDC-on-top prototype: **Catalog** · **Glossary** · **Policies** · **Requests** (and **Workflows** / **Admin** where you already separate configuration from consumption).

### 3.2 Why this structure works

Specialists keep **their** dashboards as **second-level destinations** under clear pillar labels. Executives and cross-functional leads get **one map** of the whole program without losing the specialist UIs that teams already trust.

---

## 4. Draft: Overview page (unified governance experience)

**Audience:** Data governance, privacy, compliance, and program leads who need a weekly pulse and triage path.

**Layout option:** One primary scroll, or two top-level tabs: **Pulse** | **Portfolio** (portfolio = longer-horizon KPIs and domain comparisons).

### 4.1 Hero strip — posture at a glance

A row of **five pillar cards** (order matches your workstreams). Each card shows **at most two or three KPIs**, a **trend**, and a **severity** or health state.

| Pillar | Illustrative KPIs (replace with your real measures) |
|--------|--------------------------------------------------------|
| **Privacy compliance** | Policy coverage %, open violations, overdue attestations |
| **DSAR** | Open requests, SLA breach count, median cycle time |
| **Tracker remediation** | Open findings, critical trackers, % remediated on time |
| **Operations** | Incidents or changes affecting privacy metadata, connector or pipeline health |
| **Metrics** | Reporting freshness, executive pack readiness, quality gates on governed assets |

**Interaction:** Card click either **scrolls** to that pillar’s section on the same page or **deep-links** to that pillar’s console with the **same time filter** applied.

### 4.2 Center panel — exceptions and SLAs

A single **queue or table** (backed by a cross-pillar index your platform team maintains or federates):

| Column idea |
|-------------|
| Workstream |
| Item / title |
| Severity |
| Owner |
| Due date |
| Linked asset or policy |
| Action: **Open in tool** |

**Filters:** Domain, region, product, sensitivity class, pillar.

This panel is where the experience **earns** the word *unified*: one triage surface even when resolution stays in the specialist application.

### 4.3 Cross-pillar insight row (optional)

Three **insight tiles** that only work when data is joined—for example:

- DSAR volume rising in domains with **low classification completeness**
- Tracker issues concentrated on **assets missing** a steward owner
- Operations incidents clustered around **metadata change** windows

Each tile links to **Metrics** or a **saved report**, not decorative charts.

### 4.4 Right rail — proof for leadership

- **This week:** three auto-generated bullets from week-over-week deltas across pillars.
- **Audit / evidence pack:** link to export bundle, attestation workflow, or leadership narrative doc.
- **Catalog health:** glossary coverage, CDE or sensitive-field completeness—explicit bridge to **Data Navigator** / OMS work.

---

## 5. Draft: each pillar destination (left-nav item)

Use a **repeatable template** so muscle memory transfers:

1. **Summary strip** — same KPI visual language as Overview, slightly richer.
2. **Primary workspace** — embed, deep link, or native module for the **existing** dashboard.
3. **Metadata spine strip** — related catalog assets, policies, classifications from OMS so actions are never disconnected from inventory and ownership.

---

## 6. Enterprise vs domain scope

- **Overview** defaults **enterprise-wide**; scoped views (DEEPT, business unit, product) ride on **filters** and saved views rather than forking the app.
- **Must-have** for adoption: role-aware defaults (e.g. privacy lead sees global posture; domain steward lands on their domain filter).

---

## 7. Traceability to program decisions

- **BDC-on-top** thinking (`BDC-OMS-integrated-vs-on-top-decision.md`): governance audiences often want a **visible program home** and clearer mandate than “everything inside core OMS chrome.” A **Governance / Privacy hub** can be that named front door while the catalog remains the **system of record** for metadata.
- **Migration narrative** (`Product-Brief-Alation-to-OMS-Migration.md`): extending OMS for governance use cases is stronger when **operational dashboards** and **catalog objects** reference the same identifiers and audit trail.

---

## 8. Gaps and follow-ups

1. **Slide fidelity:** To align wording and diagrams exactly with slide `g3e1ce5672ca_0_18`, export that slide or paste its bullets—the Slides MCP tool used returns **metadata and slide IDs**, not shape text.
2. **Data contract:** Define the **cross-pillar exception index** (schema, owners, refresh SLA, authoritative system per workstream).
3. **Prototype:** Optional next step is a static HTML mock (e.g. Midnight Ops or Editorial Hero theme) in `business-data-catalog/` for stakeholder walkthroughs.

---

*Document generated from working session analysis; refine KPIs and labels with your privacy and governance metric owners.*
