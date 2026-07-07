# Business Data Catalog on OMS: Integrated vs On-Top

> **Purpose:** Compare two **UX patterns** for BDC on the Operational Metadata Store (OMS) and recommend which fits this program.  
> **Read this first:** Use **Section 1** for the evaluation framework, **Section 2** for how it applies to our prototypes, **Section 3** for the recommendation and decision flow.

**Google Doc (formatted):** [Open in Google Docs](https://docs.google.com/document/d/12bpg2TPeUCBHQY_AGrh9l16addgB4GF3DTfWckshK8I/edit)

**HTML slide deck (13 slides, keyboard + swipe):** same sections as this doc—open `bdc-integrated-vs-ontop-deck.html` in a browser from the `business-data-catalog` folder.

---

## Pattern overview (at a glance)

| **Pattern** | **What it is** | **Prototype** |
| :--- | :--- | :--- |
| **Integrated into OMS** | BDC woven into **existing** OMS home, nav, and journeys (Snowflake list → full detail with **technical + business** metadata; Unity list + drawer). | `oms-ui-integrated.html` |
| **Layer on top of OMS** | **Dedicated** BDC entry + drills **above** OMS: clearer **catalog / stewardship** work; **business-first** views (technical blocks de-emphasized). | `oms-ui-on-top.html` |

---

## 1) How to evaluate which version is better

Score each pattern **Low / Medium / High** (or 1–5) per criterion—**no single criterion wins alone**; weight by org priorities.

### A. User jobs and mental model

- **Question:** Is “metadata work” part of **daily OMS** use, or a **separate stewardship** job?
- **Integrated wins when:** Same people browse **lineage + tables** and own **descriptions, policies, quality**—they want **one surface**.
- **On-top wins when:** Stewards need a **purpose-built** catalog space (tasks, approvals, **trust flags**, glossary) without **operational chrome**.

### B. Discoverability and adoption

- **Question:** Will users **find** BDC without training?
- **Integrated wins when:** OMS is already the **habit**; BDC next to technical metadata drives **passive adoption**.
- **On-top wins when:** You need a **named product** (“Business Data Catalog”) on the home page for **execs + stewards**.

### C. Information density vs. clarity

- **Question:** Is the risk **too busy on one screen** vs. **too many places to look**?
- **Integrated wins when:** **Technical + business** together reduces clicks for **engineers** who need both.
- **On-top wins when:** Mixed audiences get lost in **storage / profiling / ops** fields; **business-first** reduces noise for **stewards**.

### D. Implementation and ownership

- **Question:** **One OMS team** or a **BDC product** team ships UI?
- **Integrated wins when:** **One** delivery train, shared components—**if** scope does not creep forever.
- **On-top wins when:** BDC needs **faster iteration**, different cadence, or a clear **bounded context** vs. core OMS.

### E. Governance and policy story

- **Question:** Do audits need obvious separation: **“catalog actions”** vs. **“platform browsing”**?
- **On-top:** Easier story for **who did what** in the catalog (endorsements, deprecation, steward edits).
- **Integrated:** Same features possible; narrative is **“OMS does it all.”**

### F. Time-to-value and migration

- **Question:** **Enhance** existing OMS or launch a **net-new** catalog program?
- **Integrated:** Often **faster** if users already live in OMS—add strips, tabs, fields.
- **On-top:** Often **faster pilot** without retouching **every** OMS view—**tradeoff:** two “doors” into similar data.

### G. Stakeholder alignment

- **Platform / engineering:** Often prefers **integrated** (**one portal**, fewer duplicates).
- **Data governance / enterprise data:** Often prefers **on-top** (**visible program**, dedicated home, clearer mandate).

---

## 2) Apply the evaluation to this case (BDC + OMS prototypes)

Context: **Integrated** = full Alation-style asset page **with** technical blocks. **On-top** = BDC drill **with** technical sections reduced/hidden + **dedicated BDC home** path.

| **Criterion** | **Integrated** | **On-top** | **Notes (this program)** |
| :--- | :--- | :--- | :--- |
| **User jobs** | **High** for engineers/operators in OMS daily | **High** for stewards / **program**-framed catalog work | **Both** personas exist—tension is real |
| **Discoverability** | **High** if everyone starts from **OMS Home** | **Medium–High** if buyers only know **“BDC”** by name | **Named BDC** helps **sponsorship + training** |
| **Information density** | **One-stop** tech+biz; risk **busy UI** | **Clearer** for stewards; engineers may need **full technical** path | On-top prototype = **business-first** Snowflake detail |
| **Implementation** | **High** when **one** team owns all surfaces | **High** when BDC ships **independently** or needs **boundary** | Depends on **team topology** |
| **Governance story** | **Medium** signaling vs. dedicated app | **High** as **stewardship system of record** | **Trust flags** fit either; **on-top** = cleaner **narrative** |
| **Time-to-value** | **Often faster** add-on to existing flows | **Often faster pilot** if duplicate nav **short-term** OK | |

**Synthesis:** Prototypes target **different primary users**—**throughput + single surface** (integrated) vs. **program visibility + lower cognitive load** (on-top).

---

## 3) Recommendation

**Primary recommendation:** Lead with the **“layer on top of OMS”** pattern for the **Business Data Catalog program**, while **reusing OMS APIs** and **deep-linking** to **integrated-style** asset detail when **full technical** context is needed.

**Why (evaluation-linked):**

1. **Named product & adoption:** Dedicated BDC home/drill fits **funding, comms, training**—especially for people who are **not** “OMS-first.”
2. **Business-first clarity:** On-top Snowflake drill matches **stewardship** (descriptions, policies, samples, **trust/deprecation**) without fighting **ops metadata**.
3. **Bounded product:** Clear **ownership + roadmap + audit** story for **catalog actions**; OMS stays **operational** source of truth **underneath**.
4. **Integrated stays the engineering path:** Same data; richer **SQL / history / lineage** via **Open in OMS** or shared components—**avoid two backends**.

**When to prefer integrated-first instead:**

- OMS is **mandated** for **all** platform users—**no** second front door.
- Success = **time-on-task in OMS**, not a standalone catalog program.
- Team **cannot** maintain two navigation shells.

**Practical hybrid (common end state):**

- **On-top:** BDC home, search/facets, stewardship drills, **governance** (trust, deprecation, reasons).
- **Integrated:** Embedded strips/tabs where OMS users already work—**same services + deep links**, not duplicate logic.

### Decision flow (text diagram)

```
                    ┌──────────────────────────────────┐
                    │  Who is the primary audience   │
                    │  for “success” in year one?    │
                    └─────────────────┬────────────────┘
                                      │
            ┌─────────────────────────┼─────────────────────────┐
            ▼                         ▼                         ▼
   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
   │ Engineers /     │    │ Stewards /      │    │ Leadership /    │
   │ platform users  │    │ owners /        │    │ governance      │
   │ (OMS-heavy)     │    │ catalog program │    │ (named BDC)     │
   └────────┬────────┘    └────────┬────────┘    └────────┬────────┘
            │                      │                      │
            │         Favor: deep links + shared API      │
            │         ┌────────────┴────────────┐          │
            │         ▼                         ▼          │
            │  ┌──────────────┐        ┌──────────────┐   │
            └─►│  Integrated  │        │  On-top BDC  │◄──┘
               │  (full tech) │        │  (lead UX)   │
               └──────┬───────┘        └──────┬───────┘
                      │                       │
                      └───────────┬───────────┘
                                  ▼
                    ┌─────────────────────────────┐
                    │   One metadata API /        │
                    │   two shells (UX only)      │
                    └─────────────────────────────┘
```

---

## 4) Suggested next steps

- **Metrics:** Confirm **year-one** success (e.g. steward tasks, **described assets**, **policy coverage**—not only page views).
- **Research:** **~5 users per persona:** engineer (OMS-heavy), steward, analyst, owner, platform admin.
- **Deep links:** Contract **BDC on-top → OMS integrated** for “full technical / SQL” in **one click**.
- **Architecture:** **One** metadata API; duplicate navigation is a **UX** choice, not a **data** fork.

---

*Last updated: March 31, 2026. For **table header shading** or **accent colors** in Google Docs, use the doc’s **Table options** or **Styles** after import—the MCP applies structured headings and bold; cell fill colors are best finalized in the editor.*
