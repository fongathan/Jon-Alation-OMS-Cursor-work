# Data Platforms Intake (Bi-Weekly) — 28 May 2026

**Meeting:** Data Platforms Intake (Bi-Weekly)  
**Your slot:** **Data Navigator** (L3) — migrate Alation catalog experience to in-house OMS UI  
**Sources:** Teams transcript (535 entries) via MC-3PO `teams_get_transcript`; meeting thread via `teams_get_thread`  
**Recap:** [Teams meeting recap](https://teams.microsoft.com/l/meetingrecap?driveId=b%21SAS1GWkLrEGu_WrZNyQP4SEBtIbkH3hEmW_Q7vF6V2cmYPc9929kRo5vYAW5SCqY&driveItemId=01HV7LABC4ZUA2EGWULRC3QSCZRBCDSN4X) · [Meeting chat](https://teams.microsoft.com/l/chat/19:meeting_NGRiMDYyZmMtMWE5ZS00OGQ2LTk1ZDctMzNmNDQ4MTNiOWI4@thread.v2/conversations?context=%7B%22contextType%22%3A%22chat%22%7D)

---

## Executive summary

You presented **Data Navigator** as the **bridge** from today’s Alation catalog (~531 users) to a future in-house stack on **OMS**, while **NCI / Data 66 / MCI** own automated metadata capture—not duplicate scraping in this L3. The room aligned on **enterprise UX** (Dave Hoffman / enterprise design, Sage-style patterns), **early steward and business-user involvement**, and **honest Alation renewal planning** (Aug/Sep 2026 renewal likely; target **Sep 2027** cutover with dev complete ~Mar 2027). **Governance Portal** wireframes were shown as **adjacent / tangential**—not in Navigator scope. **MCP / agentic access** is explicitly **out of Navigator**; Tony was pointed to **MCI + Data 66** for AI-native patterns.

Prior agenda items (non-video WebViews, page-sharing semantic agent) consumed most of the session; your segment ran ~38:30–60:50 UTC.

---

## Intake outcome (your initiative)

| Signal | Detail |
|--------|--------|
| **Placement** | Last agenda item; full presentation + wireframes + governance portal peek |
| **Explicit RICE on call** | **Not completed live** for Navigator (RICE deep-dive was on Trevor’s WebViews item) |
| **Close** | Loni: “did it”; no blocking objections raised at close |
| **Direction** | Continue socializing scope as **MVP UX + migration APIs** on OMS; coordinate via **metadata working group** and DNA/metrics governance threads |

Treat as: **intake socialization advanced; finalize RICE / fleet estimates in Airtable per program norms.**

---

## Top takeaways (what the room cares about)

1. **Navigator ≠ metadata engine** — You are the **surface / home on OMS**; collectors and reconciliation sit in **MCI, Data 66, OMS backend**, and the **metadata working group** (Tony, Sarah).
2. **MVP, then iterate** — Search/discovery, glossary, browse, descriptions/metadata, **APIs to migrate Alation**; persona/filter UX is **TBD** (filters vs access-based vs split technical/business entry)—needs **greenlight to prototype and A/B**, not frozen wireframes.
3. **Design is enterprise-governed** — Charles: leverage **Dave Hoffman’s team + enterprise design** (Makda cited **Sage**). Romit: consider **PM-friendly UI iteration** (AI-assisted) in the plan.
4. **DNA / metrics definitions** — Tony: sequencing **cleanup and definition alignment** with rollout; you: definitions via **MCI**; Brenda: **Metrics Council → GIS handover** with Kyle (link to be shared); consistency work with **Makda, Isobel, Roopa**; **Carmela (DNA)** involved.
5. **Renewal reality** — Suman: contract renewal **~Aug 31 / Sep 1, 2026**; **3–4 month full replacement unrealistic**; procurement (**Samantha Motolo**) engaged; negotiate **flexibility / out clauses**; budget has renewal baked in. Hema: engineering plan targets **Sep 2027** renewal window—**dev by Mar 2027**, migration window before renewal.
6. **Users in the loop** — Romit: don’t build six months then show users; you: prior Alation design reviews + ongoing integration; Suman: **privacy** already reviewed wireframes.
7. **AI exposure elsewhere** — Tony: MCP/agentic patterns for catalog context; you + Suman: **Navigator = traditional UI**; **MCI / Data 66** for AI-native access—Sarah suggested **metadata working group** or a dedicated forum to stitch initiatives.

---

## Instructions & expectations (for you)

- **Do not** present wireframes as final UI; emphasize **discovery + enterprise design + iteration**.
- **Do not** scope scrapers/collectors in Navigator; point to **NCI / Data 66** and OMS as sources of truth for automated definitions.
- **Do** engage **Dave Hoffman / enterprise design** before locking IA.
- **Do** keep **stewards, business users, privacy, DNA** in the design loop (Romit/Suman/Tony pressure).
- **Do** align rollout narrative with **metadata working group** and Brenda’s **metrics governance handover**.
- **Do** support procurement narrative: renewal may be required short-term; build toward **2027 exit** with contract flexibility.
- **Clarify** Governance Portal vs Navigator boundaries when showing demos (Sarah’s question)—portal is **privacy/governance stakeholders**, later/engineering views possible but **not this L3**.

---

## Your action items

| # | Action | Owner | Notes |
|---|--------|-------|-------|
| 1 | **Complete RICE / intake fields in Airtable** for Data Navigator (effort, reach, impact breakdown—not presented live) | Jonathan + Hema/OMS | Follow Trevor/Dorothy pattern; use program calculator |
| 2 | **Engage Dave Hoffman / enterprise design** for Navigator IA and visual system | Jonathan | Charles committed OMS to same path as other enterprise UIs |
| 3 | **Document MVP vs out-of-scope** (UI migration vs MCI/Data 66 vs MCP) in intake artifact | Jonathan | Reduces repeat questions (Tony, Sarah) |
| 4 | **Steward / user design sessions** — expand beyond prior Alation reviews; add **product engineering** voices (Tony asked re Andre’s org) | Jonathan | Suman: business, stewards, privacy, DNA, ME analytics—not prod eng primary |
| 5 | **Share clickable / demo link** in follow-up if not already in chat (Suman asked; you deferred to Romit) | Jonathan | Link to restructured-udge / Navigator demo |
| 6 | **Coordinate with Brenda** on Metrics Council handover link and DNA forum alignment | Jonathan | Brenda to drop process link |
| 7 | **Renewal briefing** with Suman/Hema/procurement context—Navigator timeline vs **Aug 2026** renewal | Jonathan | Support “likely renew + out clauses” story |
| 8 | **Metadata working group** — attend / present how Navigator slots vs MCI, Data 66, classification | Jonathan | Sarah: coordinate cross-initiative picture |
| 9 | **Governance Portal** — note tangential; incidents/problem management integration TBD with Darren/Lance if portal proceeds | Jonathan / Suman | Not Navigator scope; avoid scope creep in this L3 |
| 10 | **Persona / filter UX** — plan A/B or prototype track once greenlit (filters, access-based, dual entry) | Jonathan + UX | Wireframes explicitly exploratory |

---

## Stakeholder quotes / signals (paraphrased)

- **Loni:** Navigator is last item; proceed with presentation.
- **Tony (DNA):** How are we engaging DNA on cleanup/sequencing vs build? → MCI + working group; Navigator surfaces outcomes.
- **Brenda:** Metrics Council handover to GIS with Kyle agreed; link forthcoming.
- **Romit:** Involve stewards during build; renewal date vs achievable date?
- **Hema:** Estimates aligned to **Sep 2027** renewal; dev complete **Mar 2027**; migrate users ~6 months before renewal.
- **Suman:** Renewal **Aug 31**; show governance portal vision briefly; privacy feedback already on wireframes; procurement engaged.
- **Sarah:** Governance dashboard **not** part of Navigator initiative; metadata WG for cross-program alignment.
- **Tony:** MCP/agentic catalog access? → separate tracks (MCI/Data 66).

---

## Meeting chat (28 May)

`teams_get_thread` with `since=2026-05-28` returned **no new messages** for this occurrence (recurring meeting thread has older traffic). **Copilot recap / Facilitator notes** were not available separately in chat pull—rely on transcript + your deck for written follow-up.

---

## Related workspace references

- Prior intake transcript (30 Apr 2026): `requirements-gathering/meetings/data-platforms-intake-2026-04-30-transcript.html`
- Product brief: `Product-Brief-Alation-to-OMS-Migration.md`
- Navigator / UDGE demo context: `data-navigator-governance/`, `business-data-catalog/`

---

*Report generated from MC-3PO Teams MCP session (transcript pull 29 May 2026).*
