# Navigator: Persona-Opinionated UX and Boundaries vs. 626 / OMS

**Purpose:** Turn stakeholder feedback from Data Platforms Intake (May 2026) into an actionable plan.  
**Audience:** You (product / program lead) and metadata working group collaborators.  
**Origin:** “Point 3” from the intake recap—close the narrative gap on **persona-specific jobs** and **clear boundaries** so Navigator does not read as a generic “do anything” catalog or as a **competing** program to Data 626 / OMS.

---

## 1. What problem you are solving

Stakeholders (notably in intake) reflected that the early Navigator / wireframe direction can feel **under-opinionated**: many capabilities visible at once, without a crisp story for *who* is trying to accomplish *what*.

At the same time, people need clarity on **626 vs OMS vs Navigator**:

- **626 / MCI-style work** is about improving **metadata supply**, curation, scanning, and related mechanics.
- **OMS** is the **operational metadata store** and technical backbone (including APIs for much of what lands there).
- **Navigator** is the **governed experience layer** that composes sources (including OMS) for **business and compliance-oriented discovery and understanding**—not a replacement for every adjacent program.

This document describes **how to make that explicit** in a lightweight, repeatable way.

---

## 2. Minimum viable artifact (if you are time-boxed)

Deliver **one page** containing:

1. **Five user stories each for three prioritized personas** (see templates below).
2. **One boundary table** (626 vs OMS vs Navigator)—Section 5.

That alone usually resolves most “competing project” anxiety without committing to a full UX redesign.

---

## 3. Step-by-step plan

### Step A — Lock a small persona set (3–5 for the next ~90 days)

Do not boil the ocean. Examples aligned to the intake conversation:

| Persona (example) | Why include |
|-------------------|-------------|
| Business / DNA consumer | Primary “find and trust the metric or dataset” user |
| Privacy & compliance reviewer | Needs breadth, audit-friendly narratives, evidence |
| Steward / governance council participant | Curates, reconciles, endorses; needs workflow affordances |
| Engineer (occasional UI use) | Needs lineage, technical truth, engineering-oriented definitions |
| DRE / automation (API-first) | May rarely use UI; needs stable programmatic access |

For **each** persona, write **one sentence**:

> When **[trigger]**, they need **[outcome]** in under **[time / effort bar]**.

That sentence becomes your **north star** for prioritizing navigation and defaults.

### Step B — Run the “five stories per persona” exercise

For **each** persona, write **five** short stories using the same shape every time:

| Field | Prompt |
|-------|--------|
| **Trigger** | What starts the work? (ticket, audit question, planning cycle, incident) |
| **Current pain** | What do they do today? (Alation, spreadsheets, Slack, manual joins) |
| **Desired outcome** | What does “good” look like in one sentence? |
| **Primary object** | Metric? Table? Policy? Classification? Lineage node? |
| **Success signal** | What would they export, screenshot, or cite to prove value? |

**Why five:** Fewer stories hide gaps; more than five invites generic “platform” thinking.

### Step C — Apply the “job test” to every major POC surface

For each major area (home, browse-by-source, asset detail, glossary, classifications / policies, admin / internal):

1. **Which persona story does this screen primarily complete?**  
2. If the answer is “sort of everyone,” either:  
   - **Split** the flow into a **primary** path and **secondary** entry points, or  
   - **Defer** the surface to a later phase with an explicit rationale.

This is how the product becomes **opinionated** without pretending every persona gets equal depth on day one.

### Step D — Maintain a lightweight decision log for boundary debates

When someone says “this feels like 626,” capture a row:

| Capability they mean | Best home (626 / OMS / Navigator / shared API) | User-visible outcome |
|----------------------|-----------------------------------------------|------------------------|
| *Example: automated column descriptions from repo scans* | … | … |

Two or three **written** decisions often end recurring debate faster than another deck-only review.

### Step E — Operationalize in the metadata working group

Ask for **~30 minutes** on a working group agenda:

**Title:** Persona stories + 626 / OMS / Navigator boundary review  
**Goal:** Shared mental model and **prioritized** backlog—not pixel-perfect UX.

---

## 4. One-slide / one-table boundary (copy-ready)

| | **626 / MCI (and adjacent supply-side work)** | **OMS** | **Navigator** |
|---|---------------------------------------------|----------|----------------|
| **Problem it solves** | Improve how metadata is **produced, scanned, curated, and governed at the source** | **Store, connect, and serve** operational and technical metadata; platform APIs | **Compose** trusted metadata into a **governed discovery and understanding experience** for business and compliance users |
| **System of record** | Program artifacts, pipelines, curation outputs—*as defined by those programs* | OMS graph / objects / APIs—*as owned by OMS* | Experience, navigation, persona defaults, policy-surfacing UX—*backed by OMS and other sources* |
| **Primary user** | Engineers, curation teams, metadata program owners | Engineers, platform consumers, integrators | Business consumers, stewards, privacy/compliance reviewers (plus thin engineer paths where needed) |
| **“Done” means** | Higher coverage, better definitions at source, repeatable curation | Reliable technical truth in the store; stable contracts (e.g. APIs) | A user can **answer a real question** (trust, meaning, policy, lineage context) with **low noise** |

**One-line positioning you can reuse in meetings:**

> **626 improves metadata supply; OMS stores and serves it; Navigator is the governed experience that makes the right metadata usable for the right persona.**

---

## 5. Optional: story starters (edit to your org’s real names and systems)

Use these as **stubs**—replace bracketed text.

### Persona: Business / DNA consumer

1. Trigger: planning needs **[metric]** — **Outcome:** find authoritative definition and owner.  
2. Trigger: two dashboards disagree; **Outcome** → see **gold** definition and **known conflicts**.  
3. Trigger: new hire; **Outcome** → browse **approved** datasets for **[domain]**.  
4. Trigger: vendor question; **Outcome** → export a **citation-friendly** definition package.  
5. Trigger: deprecation notice; **Outcome** → understand **replacement** and **downstream impact**.

### Persona: Privacy & compliance reviewer

1. Trigger: audit asks whether **[PII]** exists in **[space]**; **Outcome** → evidence-backed view.  
2. Trigger: legal demo walkthrough; **Outcome** → “**defined vs observed**” narrative without manual screenshots everywhere.  
3. Trigger: DSAR pattern review; **Outcome** → locate **consent / purpose** metadata tied to assets.  
4. Trigger: classification drift; **Outcome** → see **policy ↔ classification** linkage.  
5. Trigger: third-party sharing review; **Outcome** → trace **sensitivity** and **contracts** context.

### Persona: Steward / governance council

1. Trigger: two sources define **[metric]** differently; **Outcome** → reconciliation path visible.  
2. Trigger: council ratifies a definition; **Outcome** → **gold** status and **provenance** clear to consumers.  
3. Trigger: new dataset onboarded; **Outcome** → **endorsement / warning** workflow.  
4. Trigger: policy change; **Outcome** → see **impacted assets** from classifications.  
5. Trigger: quarterly review; **Outcome** → **coverage / exceptions** dashboard slice.

---

## 6. Definition of success for “Point 3”

You can consider this thread **closed** when:

1. **Three personas** have **five stories** each, reviewed with **Sarah** (and **Suman** as needed).  
2. Every **major** POC view maps to **at least one primary story** (or is explicitly deferred).  
3. The **boundary table** has been shown once in **metadata WG** and **decision log** has 2–3 rows filled from real debates.

---

*Generated for internal working use. Refine names (626, MCI, program labels) to match your official program language.*
