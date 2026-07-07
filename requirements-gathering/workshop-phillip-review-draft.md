Navigator Portal & Data Foundations — Complementary Capabilities Workshop
Data Classification, Definitions, Descriptions, Business Catalog, Policy — July 2026 Workshop

Document status: Phillip review draft (v2)
Co-sponsors: Data Governance (Niru Sharma, Jonathan Fong) + Data Foundations Platform (Ryan Malec, Renat Gilfanov)
Original workshop doc: https://docs.google.com/document/d/19K4CBJjKiOku_fWUpMJLCL0WHglasE6eXn10BmdT2wY/edit

═══════════════════════════════════════════════════════════════════════════════
1. EXECUTIVE SUMMARY
═══════════════════════════════════════════════════════════════════════════════

THE ASK

Request approval to hold a 2.5-day cross-team workshop (July 21–23, 2026, Disney Seattle office) with representatives from Data Governance and Data Foundations Platform (DFP). Estimated travel: ~10 attendees from Santa Monica, Glendale, Texas, and San Francisco (travel cost TBD — Finance to confirm).

Deliverables due to Phillip by July 29, 2026:
  • Alignment memo — portal roles, overlap resolution, escalation path
  • RACI by capability area — glossary, dictionary, classification, policy, lineage, stewardship
  • Joint roadmap slice — Q4 FY26 / Q1 FY27 aligned to DFP phased delivery
  • Decision log — open items with owner, deadline, and “needs VP decision” flag

Optional: 30-minute readout to Phillip (week of July 28).

WHY NOW (ORG-LEVEL RISK)

Phillip now leads both Data Governance and Data Foundations. Without explicit alignment, we risk:

  • Duplicate UI and metadata work — OMS UI unification, Navigator/Portal, and DFP unified design system/agent shell may overlap without shared boundaries
  • Competing definitions of governance — DFP Process Repository vs Data Gov policy/classification programs need a single story for stewards and agents
  • Alation exit timeline — migration scope may blur between OMS technical catalog and business glossary/dictionary
  • Agent-first DFP — governance rules must be machine-readable; we must define who owns content vs orchestration

This workshop is not a turf negotiation. It is structured alignment under unified leadership to ship one coherent experience for stewards, privacy leads, and data practitioners.

WHAT PHILLIP GETS BACK

  1. Signed alignment doc (Jul 25 draft → Jul 29 final)
  2. RACI with zero “TBD” ownership at close for in-scope capabilities
  3. Joint roadmap slice tied to DFP PRD phases
  4. Escalation rule for deadlocks (see Section 11)
  5. Optional live readout with decisions flagged for VP ratification

═══════════════════════════════════════════════════════════════════════════════
2. RELATIONSHIP TO DATA FOUNDATIONS PLATFORM (DFP)
═══════════════════════════════════════════════════════════════════════════════

This workshop explicitly supports the DFP vision (agent-orchestrated platform actions with governed processes) by defining what Data Governance owns in content and policy versus what DFP owns in orchestration, UI shell, and platform services.

Reference: DFP PRD — Data Foundations Platform (AI-First Unified Data Platform)
https://docs.google.com/document/d/1NaFTpks3QTp3o2KZWuxfKKthU2hQdn8BabnNyLA2LGQ/edit

Organizing principle: One org, two jobs-to-be-done, one metadata spine.

  • Data Gov Portal — “Are we in policy? What needs a human this week?”
  • Navigator — “Discover and steward data assets”
  • DFP / Platform UIs + Agent — “Operate the platform; execute governed actions”

Shared spine: Governance Metadata Repository (classifications, policies, business metrics) ↔ OMS Semantic Registry (technical metadata, lineage) ↔ Process Repository (machine-readable governed processes for agents).

OVERLAP MAP (WORKSHOP SCOPE ↔ DFP PRD)

Capability area          | Data Gov workshop scope                    | DFP PRD touchpoint                          | Intended workshop outcome
-------------------------|--------------------------------------------|---------------------------------------------|--------------------------------------------------
Business glossary/metrics| Glossary, Git SoR, conflict detection      | OMS Semantic Registry (Phase 1)               | Gov owns business definitions; OMS stores technical semantics; define sync model
Data dictionary          | Table/column metadata, steward workflows   | OMS UI unification (Phase 0.1), OMS MCP       | Define steward UX ownership vs metadata API ownership
Classification           | Algorithms, tag propagation, dictionary    | OMS PI identification; Process Repository R6.5| Define classification SoR; enforcement handoff to DFP router
Policy                   | Authoring, storage, enforcement evidence   | Process Repository (R6 — Gov + DX joint)      | Gov owns policy content; DFP owns orchestration/enforcement plumbing
Portal vs platform UI    | Privacy/Gov Portal vs Data Foundation UI   | Unified Design System (R4), embedded agents   | Shared shell, distinct jobs-to-be-done, deep links
Lineage                  | OMS + beyond, steward validation           | OMS MCP, lineage system tables              | Read via OMS; Gov adds stewardship validation overlay
Stewardship              | Roles, domain groupings, gap management    | Org Data Mart, Access Manager, OMS ownership  | Define steward assignment SoR and alert workflows

CONTENT VS PLATFORM OWNERSHIP (PROPOSED FRAMEWORK)

Layer                              | Data Governance              | Data Foundations
-----------------------------------|------------------------------|----------------------------------
Policy/classification definitions  | Own                          | Consume via Process Repository
Process authoring (human-readable) | Own                          | Host (Process Repository)
Process orchestration (agent runs) | Inform / approve             | Own (Router, NOMS, MCPs)
Business glossary / metrics        | Own (Git as SoR)             | Sync to OMS registry
Technical metadata / lineage       | Validate & enrich            | Own (OMS)
Unified UI shell / embedded agents | Participate (Portal/Nav IA)  | Own (DX design system)

═══════════════════════════════════════════════════════════════════════════════
3. WORKSHOP OVERVIEW
═══════════════════════════════════════════════════════════════════════════════

Date:        July 21–23, 2026 (Tuesday–Thursday)
Location:    Disney Seattle office
Duration:    2.5 days

A cross-team workshop to establish an aligned and complementary approach across Data Governance and Data Foundations initiatives in support of Governance, Privacy, Security, and Compliance requirements.

The session will define product goals, use cases, scope, and ownership; identify overlaps; and establish RACI for areas where Governance and DFP needs intersect and require either a complementary or unified approach.

The workshop will prioritize clarity on product goals and ownership over decisions about where and how a solution will be implemented. Implementation and platform considerations are important and will be addressed, but discussion begins with business requirements, governance needs, and stakeholder expectations to ensure future solutions are aligned, actionable, and clearly owned.

Recommended pattern: Dual product, single spine
  • Logically separate experiences for different personas
  • Physically one product family — shared design language, global search, deep links, same asset IDs
  • Not a second metadata store — one spine: supplies → OMS stores → governance repo defines business meaning

═══════════════════════════════════════════════════════════════════════════════
4. GOALS & SUCCESS CRITERIA
═══════════════════════════════════════════════════════════════════════════════

GOALS

  1. Define the desired outcome for each workstream, including recommended path forward for leadership review and buy-in
  2. Clarify intersection between Governance and DFP needs — complementary vs single approach per capability
  3. Articulate purpose, goals, and distinct roles of Gov Portal, Navigator, and DFP platform experiences — and why all are needed
  4. Define scope, ownership, and RACI across initiatives and capability areas
  5. Identify open questions, dependencies, and unresolved decisions — including which engineering team builds and supports each capability

WORKSHOP SUCCESS CRITERIA (EXIT CONDITIONS)

  • Every in-scope capability has named Responsible (R) and Accountable (A) in RACI
  • Zero capabilities with “TBD” ownership at workshop close
  • Alignment doc reviewed by Romit Mehta, Charles Chao, and Ryan Malec before Phillip readout
  • Explicit list of intentional shared areas (design system, OMS APIs, Process Repository) vs must-not-duplicate areas
  • Decision log with ≤5 items escalated to Phillip for ratification

═══════════════════════════════════════════════════════════════════════════════
5. ARCHITECTURE FRAMING
═══════════════════════════════════════════════════════════════════════════════

(See architecture diagram — to be embedded from Navigator/OMS alignment deck)

Personas → Experiences → Shared spine → Infrastructure

  Stewards & Privacy  →  Gov Portal (govern & prove)     →  Governance Metadata Repository
  Stewards & Analysts →  Navigator (discover & steward)  →  OMS Semantic Registry
  Data Engineers      →  DFP Agent + Platform UIs        →  Process Repository + OMS + platform services
  Leadership          →  Gov Portal + compliance views   →  Aggregated posture feeds

Integration commitments (to be confirmed in workshop):

  Data Governance will:
    • Project governance definitions to OMS (not maintain a parallel technical catalog)
    • Express policies in Process Repository–compatible format for DFP agents
    • Deep-link Portal to OMS asset pages and DFP platform actions
    • Co-own persona research and shared UI patterns with DFP

  Data Foundations will:
    • Expose governance-aware queries via OMS MCP (classification, owner, policy flags)
    • Include Gov-authored process templates in Process Repository by Phase 1
    • Accommodate Gov Portal / Navigator navigation in unified UI without absorbing Gov program roadmap

═══════════════════════════════════════════════════════════════════════════════
6. ATTENDEES & CO-SPONSORS
═══════════════════════════════════════════════════════════════════════════════

CO-SPONSORS (joint ownership of workshop outcomes)
  • Niru Sharma — Product Lead, Data Governance (SEA)
  • Jonathan Fong — Product Lead, Data Governance (Santa Monica)
  • Ryan Malec — Product Manager, Data Foundations Platform (Santa Monica)
  • Renat Gilfanov — DP Product Lead (SEA)

CORE ATTENDEES

Name              | Role                         | Team            | Location     | Travel
------------------|------------------------------|-----------------|--------------|--------
Suman Pal         | Director Product             | Data Governance | SEA          | No
Niru Sharma       | Product Lead                 | Data Governance | SEA          | No
Brenda Villasenor | Product Lead                 | Data Governance | SEA          | No
Richard Lu        | Product Lead                 | Data Governance | SEA          | No
Jonathan Fong     | Product Lead                 | Data Governance | Santa Monica | Yes
Parshant Jain     | Product                      | Data Governance | Santa Monica | Yes
Norman [TBD]      | Product / Privacy Lead         | Data Governance | TBD          | TBD
Roopa Prabhu      | DP Architect                 | DFP             | SEA          | No
Manish Vyas       | [Role TBD — confirm]         | DFP             | TBD          | TBD
Chris Shields     | Director Engineering         | Ad Platforms    | Glendale     | Yes
Romit Mehta       | Executive Director Product   | DFP             | SFO          | Yes
Renat Gilfanov    | DP Product Lead              | DFP             | SEA          | No
Ryan Malec        | Product Manager              | DFP             | Santa Monica | Yes
Charles Chao      | Executive Director Engineering| DFP / Gov bridge| Santa Monica | Yes
Samuel Heaney     | Engineering Manager          | Privacy Services| TX           | Yes
Matthew Marple    | Engineering (AI / NOMS)      | Data Experience | Santa Monica | Yes
Richard Lopez     | TPM                          | DFP             | SEA          | No
Wilson Chaves     | TPM                          | DFP             | Santa Monica | Yes

Note: Confirm Manish Vyas attendance and role. Add Norman’s full name and travel. Fill any remaining gaps by July 7.

LEADERSHIP TOUCHPOINTS
  • Pre-brief to Phillip (optional, 15 min) — week of July 14: overlap map + guardrails
  • Post-workshop readout to Phillip (optional, 30 min) — week of July 28: decisions for ratification

═══════════════════════════════════════════════════════════════════════════════
7. PRE-WORK (DUE JULY 14)
═══════════════════════════════════════════════════════════════════════════════

  1. Read DFP PRD (link above) — focus on Process Repository (R6), OMS Semantic Registry, Unified Design System (R4)
  2. Read Gov Portal architecture summary (internal: Navigator/OMS alignment deck)
  3. Complete pre-workshop survey: “Top 3 overlaps you want resolved”
  4. Review pre-populated RACI draft ( circulated separately ) — come prepared with R/A recommendations per capability

═══════════════════════════════════════════════════════════════════════════════
8. AGENDA
═══════════════════════════════════════════════════════════════════════════════

This agenda is designed to produce aligned scope, RACI, and a joint roadmap for capabilities where Data Governance and Data Foundations intersect. Joint sessions are co-led unless noted as parallel tracks.

DAY 1 — TUESDAY, JULY 21 — FRAMING & PERSONAS

Time        | Topic                                              | Leads              | Duration | Audience
------------|----------------------------------------------------|--------------------|----------|----------
9:00 AM     | Welcome, objectives, and success criteria          | Niru, Jon, Ryan    | 15 min   | All — Discuss
9:15 AM     | Portal roles: Gov Portal vs DFP Platform UI        | Niru & Jon + Ryan  | 60 min   | All — Discuss
            | (Dual product, single spine; shared shell)         | & Renat            |          |
10:15 AM    | UI patterns / Personas (steward, privacy, engineer)| Niru & Jon + Ryan  | 60 min   | All — Discuss
11:15 AM    | Architectural considerations & metadata spine      | Roopa + Jon        | 45 min   | All — Discuss
11:45 AM    | Stewardship assignment                             | Brenda + Ryan      | 30 min   | All — Discuss
12:15 PM    | Lunch                                              |                    |          |
1:00 PM     | PARALLEL TRACK A: Business Glossary                | Brenda             | 60 min   | Gov-led; DFP observers welcome
1:00 PM     | PARALLEL TRACK B: OMS MCP & semantic registry      | Renat / Matthew    | 60 min   | DFP-led; Gov observers welcome
2:00 PM     | Share-out: Glossary + OMS registry                 | Brenda + Renat     | 15 min   | All
2:15 PM     | Table / column descriptions — MVP vs future state  | Jon + Ryan         | 60 min   | All — Discuss
3:15 PM     | Data lineage integrations (OMS + beyond)           | Brenda + Roopa     | 45 min   | All — Discuss
4:00 PM     | Unity Catalog & Governance: complementary roles    | Jon + Roopa        | 30 min   | All — Discuss
            | (integration points, not either/or)                |                    |          |
4:30 PM     | Day 1 recap: RACI draft + boundaries               | Niru & Jon + Ryan  | 30 min   | All

DAY 2 — WEDNESDAY, JULY 22 — CAPABILITY DEEP DIVES & OVERLAP RESOLUTION

Time        | Topic                                              | Leads              | Duration | Audience
------------|----------------------------------------------------|--------------------|----------|----------
9:00 AM     | PARALLEL TRACK A: Data Dictionary                  | Brenda             | 45 min   | Gov-led; DFP observers welcome
9:00 AM     | PARALLEL TRACK B: Process Repository & Gov processes| Ryan / Matthew    | 45 min   | DFP-led; Gov observers welcome
9:45 AM     | Share-out: Dictionary + Process Repository         | Brenda + Ryan      | 15 min   | All
10:00 AM    | Glossary ↔ Data Dictionary integration             | Brenda + Renat     | 30 min   | All — Discuss
10:30 AM    | Break                                              |                    | 15 min   |
10:45 AM    | CLASSIFICATION (joint block)                       | Richard + Ryan     | 2 hr     | All — Discuss
            | • Identification: algorithms, integration          |                    |          |
            | • UI and workflow; tag propagation                 |                    |          |
            | • Classification definitions — ownership           |                    |          |
            | • Classification dictionary — UI & integrations    |                    |          |
12:45 PM    | Lunch                                              |                    |          |
1:45 PM     | POLICY (joint block)                               | Richard + Ryan     | 2 hr     | All — Discuss
            | • Authoring and storage; use case gathering        |                    |          |
            | • Policy authoring UI and workflow                 |                    |          |
            | • Policy storage; Process Repository alignment     |                    |          |
            | • Enforcement evidence collection                  |                    |          |
            | Ref: Policy memo (Mike O)                          |                    |          |
3:45 PM     | Optional: Onboarding / Access / RIM / DSR /        | Richard, Norman,   | 60 min   | Time permitting
            | Retention / Inventory                              | Ryan               |          |
4:45 PM     | Day 2 recap: RACI & scope                          | Niru, Jon, Ryan    | 30 min   | All

DAY 3 — THURSDAY, JULY 23 — PRIVACY WORKFLOWS & CLOSE

Time        | Topic                                              | Leads              | Duration | Audience
------------|----------------------------------------------------|--------------------|----------|----------
9:00 AM     | Privacy, Security, Legal, and RIM review triggers  | Norman + Ryan      | 60 min   | All — Discuss
10:00 AM    | RIM, data retention, deletion, DSR use cases       | Norman, Niru       | 60 min   | All — Discuss
11:00 AM    | Spillover items and open decision review           | Niru, Jon, Ryan    | 60 min   | All
12:00 PM    | Conclusion: outputs, owners, Phillip readout plan  | Niru, Jon, Ryan    | 30 min   | All

═══════════════════════════════════════════════════════════════════════════════
9. PROPOSED SCOPE
═══════════════════════════════════════════════════════════════════════════════

1. BUSINESS GLOSSARY
   • Target look & feel (search, usability)
   • Integration with Git as system of record
   • Metric conflict detection (surfacing conflicts, resolution workflow)
   • Automated metric consistency scoring
   • Workflow for suggesting updates and steward approvals

2. DATA DICTIONARY
   • Dataset / table / column-level metadata experience
   • Workflow for suggesting updates and steward approvals
   • Differentiation of governed vs non-governed assets (e.g., filtering for Conformed layers)

3. STEWARDSHIP ASSIGNMENT
   • Steward roles (business vs technical) and responsibilities
   • Domain-based steward groupings
   • Gap management: alerts when stewards leave / inactive; replacement workflows; ownership coverage tracking

4. GLOSSARY ↔ DATA DICTIONARY INTEGRATION
   • Linking business terms / metrics to physical data assets

5. DATA LINEAGE INTEGRATION (OMS + BEYOND)
   • Connecting to OMS lineage for end-to-end visibility
   • Steward workflows for validating lineage accuracy

6. CLASSIFICATION & POLICY (joint with DFP)
   • Classification SoR, UI, propagation, and Process Repository conditionals
   • Policy authoring, storage, enforcement evidence, and agent orchestration handoff

OUT OF SCOPE FOR THIS WORKSHOP (explicit)
   • Business question-answering (Glyph / Cortex / Pixie — owned by Performance Data)
   • CW provisioning mechanics (DFP Journey 2 — reference only)
   • Final implementation technology choices (defer to engineering spikes post-alignment)

═══════════════════════════════════════════════════════════════════════════════
10. EXPECTED OUTPUTS & TIMELINE
═══════════════════════════════════════════════════════════════════════════════

Output                              | Owner              | Due date
------------------------------------|--------------------|-----------
Alignment memo (draft)              | Niru + Jon + Ryan  | Jul 25, 2026
RACI by capability (final)          | Niru + Ryan        | Jul 25, 2026
Joint roadmap slice (Q4/Q1)           | Jon + Ryan         | Aug 1, 2026
Decision log                          | Richard Lopez      | Jul 25, 2026
Engineering alignment & plan          | Charles + Roopa    | Aug 8, 2026
Action items tracker (living)         | Richard Lopez      | Ongoing
Phillip readout (optional)          | Niru + Ryan        | Week of Jul 28

═══════════════════════════════════════════════════════════════════════════════
11. DECISIONS FOR VP RATIFICATION
═══════════════════════════════════════════════════════════════════════════════

The workshop is designed to produce recommendations on the following. Items marked ★ may require Phillip’s explicit ratification if teams do not reach consensus.

  1. Portal IA: two products in one shared shell vs merged experience ★
  2. System of record: business metrics/definitions (Gov) vs technical semantics (OMS) — sync model ★
  3. Classification: build vs integrate for UI; SoR for classification dictionary
  4. Process Repository: Gov authors policies/processes; DFP hosts and orchestrates (aligns with DFP PRD R6)
  5. Engineering ownership: which squad builds and supports each in-scope capability ★
  6. Escalation rule for deadlocks ★

DEFAULT ESCALATION RULE (PROPOSED)

  • User outcome and system-of-record for business meaning → Data Governance
  • Platform orchestration, UI shell, and technical metadata APIs → Data Foundations
  • Joint architecture changes → Roopa + Charles, then Phillip within 5 business days if unresolved

═══════════════════════════════════════════════════════════════════════════════
12. ACTION ITEMS TRACKER
═══════════════════════════════════════════════════════════════════════════════

Action item                                      | Owner        | Due date   | Status
-------------------------------------------------|--------------|------------|--------
Confirm attendee list (Manish, Norman, travel)   | Niru         | Jul 7      | Open
Circulate pre-work pack (DFP PRD + RACI draft)   | Jon          | Jul 10     | Open
Pre-align executive summary with Ryan + Renat    | Jon + Ryan   | Jul 10     | Open
Schedule optional Phillip pre-brief (15 min)     | Niru         | Jul 14     | Open
Embed architecture diagram in this doc           | Jon          | Jul 14     | Open
Confirm travel budget with Finance               | Richard Lopez| Jul 14     | Open
Send calendar holds to all attendees               | Richard Lopez| Jul 7      | Open
Schedule Phillip post-readout (30 min)           | Niru + Ryan  | Jul 23     | Open

═══════════════════════════════════════════════════════════════════════════════
APPENDIX: STRATEGIC POSITION (INTERNAL — REMOVE OR MOVE BEFORE WIDE DISTRIBUTION)
═══════════════════════════════════════════════════════════════════════════════

Lead with user outcomes, not org charts. Embrace DFP as the platform layer; define the Gov slice inside it. Pre-align with DFP co-sponsors before Phillip submission. Avoid defensive framing (e.g., “why we can’t use Unity Catalog”) — use integration design language instead.
