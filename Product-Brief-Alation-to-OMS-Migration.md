# Product Brief: Data Governance Data Catalog Migration — Alation to OMS

**Project:** Data Governance Data Catalog Migration  
**From:** Alation (External Data Catalog)  
**To:** OMS (Operational Metadata Store)  
**Organization:** Disney Streaming Services  
**Document Version:** 1.0  
**Date:** March 19, 2026

---

## 1. Executive Summary

This product brief outlines the plan to migrate our Data Governance data catalog from Alation to OMS (Operational Metadata Store). The migration will consolidate our data catalog capabilities into Disney’s internal OMS platform, reducing vendor dependency while aligning with enterprise metadata and governance standards.

**Key objectives:**
- Preserve critical business metadata and catalog capabilities currently in Alation
- Extend OMS to support Data Governance use cases (glossary, stewardship, discovery, lineage)
- Ensure stakeholder needs are captured and addressed through structured requirements gathering
- Deliver a phased migration with clear success criteria and minimal disruption

---

## 2. Project Scope & Context

### 2.1 Current State
- **Alation** serves as the primary data catalog for Data Governance
- Alation contract end date: **October 1, 2026**
- OMS currently focuses on technical metadata (tables, pipelines, streams, reports)
- Business metadata (glossary, descriptions, tags, ownership) must be extended in OMS

### 2.2 Target State
- **OMS** becomes the system of record for data catalog and Data Governance metadata
- Business metadata parity for critical features (glossary, search, lineage, tags, documentation)
- Governance workflows and stewardship supported in OMS
- Alation decommissioned upon successful cutover

---

## 3. Requirements Gathering

Requirements gathering is the foundation of a successful migration. The following four areas must be completed before design and build phases begin.

---

### 3.1 Documenting Current Use Requirements

**Objective:** Capture how Alation is used today so we do not lose functionality or disrupt user workflows.

**Activities:**

| Activity | Description | Deliverables |
|----------|-------------|--------------|
| **Feature inventory** | Document every Alation feature in use today (search, glossary, lineage, tags, articles, policy center, etc.) | Feature inventory matrix |
| **Usage mapping** | Map each feature to user personas and workflows (e.g., analysts search; stewards tag; governance runs reports) | Persona–feature matrix |
| **Stakeholder interviews** | Interview key users: data stewards, analysts, governance, engineers. Ask: “What do you use Alation for? Walk me through a typical day.” | Interview notes, use-case documentation |
| **Workflow documentation** | Document end-to-end workflows (e.g., “How does a new glossary term get created and approved?”) | Workflow diagrams, process docs |
| **Screenshot documentation** | Capture screenshots for every documented feature and workflow. Include: search UI, glossary view, lineage view, table detail, tags, articles, policy center, reports | Screenshot library with annotations |

**Stakeholder groups to interview:**
- Data stewards
- Data analysts / BI users
- Data engineers
- Governance / compliance
- Leadership (for reporting needs)

**Best practices:**
- Use structured interview guides to ensure consistency
- Record sessions (with permission) for reference
- Validate findings with a second round of “did we miss anything?” sessions
- Organize screenshots by feature and workflow for easy reference in design

---

### 3.2 Documenting Enhancement Requirements

**Objective:** Capture improvements and capabilities that Alation promised but never delivered, or that stakeholders want in the new system.

**Activities:**

| Activity | Description | Deliverables |
|----------|-------------|--------------|
| **Gap document review** | Review the existing Alation gap document (promised vs. delivered). Extract enhancement opportunities | Enhancement backlog |
| **Stakeholder interviews** | Ask: “What did you wish Alation could do that it doesn’t? What would make your job easier?” | Enhancement requirements list |
| **Prioritization** | Prioritize enhancements by impact and feasibility. Separate Phase 1 (parity) from Phase 2 (enhancements) | Prioritized enhancement backlog |
| **Screenshot documentation** | Where applicable, include screenshots of current limitations or mockups of desired enhancements | Screenshot library (gaps, mockups) |

**Typical enhancement areas (from industry patterns):**
- Semantic / AI-powered search
- Column-level lineage
- Automated documentation
- Data quality integration
- Compliance automation
- Workflow automation
- Better reporting and dashboards

**Best practices:**
- Keep enhancement backlog separate from parity requirements
- Include screenshots of current pain points where possible
- Validate enhancements with governance and engineering for feasibility

---

### 3.3 Examining OMS for Current Features to Leverage

**Objective:** Identify OMS capabilities that already meet or can be extended to meet our requirements.

**Activities:**

| Activity | Description | Deliverables |
|----------|-------------|--------------|
| **OMS capability inventory** | Document OMS’s current features: search, lineage, metadata fields, APIs, integrations | OMS capability matrix |
| **Feature mapping** | Map each Alation requirement to OMS: “OMS has it” / “OMS can extend” / “OMS lacks” | Requirements–OMS mapping |
| **Leverage opportunities** | Identify where we can use OMS as-is (e.g., technical metadata, lineage button, datasource UI) | Leverage list with screenshots |
| **Screenshot documentation** | Capture OMS screenshots for each capability. Annotate what works and what needs extension | OMS screenshot library |

**OMS areas to examine:**
- Search and discovery
- Lineage (table, column, dataflow)
- Metadata fields (description, ownership, tags)
- Data source connectors
- API and integration options
- Governance and policy features

**Best practices:**
- Work closely with the OMS product/engineering team
- Validate OMS roadmap for planned features
- Document evidence (screenshots, API docs) for each capability

---

### 3.4 Examining OMS for Gaps

**Objective:** Identify where OMS cannot meet our requirements with current features and where net-new build is needed.

**Activities:**

| Activity | Description | Deliverables |
|----------|-------------|--------------|
| **Gap analysis** | For each requirement, document: OMS has / OMS lacks / Build required | Gap matrix |
| **Prioritization** | Prioritize gaps by criticality (High/Medium/Low) and migration impact | Prioritized gap list |
| **Build scope** | Define what OMS team (or DSS) must build: glossary, tags, business search, etc. | Build scope document |
| **Screenshot documentation** | Screenshots of OMS showing “Not Available” or missing fields. Compare to Alation screenshots | Gap evidence (screenshots) |

**Known gap areas (from current OMS assessment):**
- Business glossary
- Business-context search (glossary, articles)
- Documentation / Business Description (placeholders exist; need population)
- Tags and custom fields
- Usage / access metrics (last access, top users)
- Ownership / Created By
- Version control
- Airflow integration (fields exist; need population)
- Policy center / compliance workflows

**Best practices:**
- Use side-by-side Alation vs. OMS screenshots for stakeholder communication
- Engage OMS team early to validate gaps and build estimates
- Document workarounds where they exist

---

### 3.5 Requirements Gathering Summary

| Phase | Duration (Est.) | Key Outputs |
|-------|-----------------|-------------|
| Current use documentation | 2–3 weeks | Feature inventory, workflow docs, screenshot library |
| Enhancement documentation | 1–2 weeks | Enhancement backlog, prioritization |
| OMS leverage analysis | 1–2 weeks | OMS capability matrix, requirements mapping |
| OMS gap analysis | 1–2 weeks | Gap matrix, build scope |
| **Total** | **5–9 weeks** | Consolidated requirements document, sign-off |

---

## 4. Design & Architecture

**Objective:** Translate requirements into technical design and architecture.

**Activities:**
- Data model design for business metadata (glossary, tags, custom fields)
- Integration design (metadata ingestion, lineage, APIs)
- UI/UX design for new OMS features (aligned with OMS design system)
- Migration design (extract from Alation, transform, load to OMS)

**Deliverables:** Architecture document, data model, integration specs, UI wireframes

---

## 5. Build & Development

**Objective:** Implement OMS extensions and migration tooling.

**Phases:**
- **MVP (Phase 1):** Critical Alation parity — glossary, search, basic lineage, tags, documentation
- **Full parity (Phase 2):** Custom fields, governance workflows, integrations
- **Enhancements (Phase 3):** AI search, automation, compliance features (from enhancement backlog)

**Deliverables:** Deployed OMS features, migration scripts, API integrations

---

## 6. Migration Execution

**Objective:** Move metadata and users from Alation to OMS with minimal data loss.

**Activities:**
- Metadata extraction from Alation (glossary, articles, tags, lineage, custom fields)
- Transformation and mapping to OMS schema
- Load and validation
- Parallel run (Alation + OMS) for user validation
- Cutover and Alation decommission

**Deliverables:** Migration runbook, validation report, cutover plan

---

## 7. Change Management & Training

**Objective:** Ensure users adopt OMS and can perform their roles effectively.

**Activities:**
- Training materials (quick guides, videos, FAQs)
- Role-based training (stewards, analysts, governance, engineers)
- Champions program
- Office hours post-launch
- Communication plan (timeline, what’s changing, where to get help)

**Deliverables:** Training curriculum, materials, champions roster, communication calendar

---

## 8. Governance & Ownership

**Objective:** Ensure clear ownership and governance of the data catalog in OMS.

**Recommendations:**
- **Data Governance team** owns: catalog features, requirements, acceptance criteria, adoption, steward community
- **Engineering/OMS team** owns: technical implementation, integrations, performance
- RACI matrix for each capability
- Governance sign-off at phase gates
- Success metrics (glossary coverage, steward activity, search success)

---

## 9. Success Criteria & Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Business metadata preservation | ≥95% | Glossary terms, tags, descriptions migrated and validated |
| User adoption | ≥80% of current Alation users active in OMS within 4 weeks of cutover | Weekly active users |
| Search success | Users find assets in OMS | Search-to-click rate, user feedback |
| Steward engagement | Stewards actively maintaining metadata | Steward activity logs |
| Zero critical data loss | No loss of high-priority metadata | Migration validation report |

---

## 10. Timeline & Milestones

| Phase | Duration | Key Milestones |
|-------|----------|----------------|
| Requirements gathering | 5–9 weeks | Requirements doc signed off |
| Design & architecture | 4–6 weeks | Architecture approved |
| Build (MVP) | 3–4 months | OMS MVP deployed |
| Migration planning | 4–6 weeks | Migration runbook approved |
| Parallel run | 2–4 months | Alation + OMS both available |
| Migration execution | 6–12 weeks | Metadata migrated, validated |
| Training | 2–4 weeks | Materials delivered, workshops complete |
| Cutover | 2–4 weeks | OMS primary; Alation read-only |
| Alation decommission | By contract end | Full OMS |

**Note:** Timeline assumes Alation contract extension to enable adequate parallel run and validation. See existing Migration Project Plan for extension recommendation.

---

## 11. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Incomplete requirements | Structured interviews, screenshot documentation, validation rounds |
| OMS roadmap misalignment | Early engagement with OMS team; align requirements to roadmap |
| Migration data loss | Metadata-first approach; validation checkpoints; parallel run |
| User resistance | Change management, champions, training, clear communication |
| Timeline pressure | Prioritize MVP; negotiate Alation extension |

---

## 12. Dependencies & Assumptions

**Dependencies:**
- OMS team capacity and roadmap alignment
- Alation API access for metadata extraction
- Stakeholder availability for interviews
- Budget and resource allocation

**Assumptions:**
- OMS can be extended to support business metadata
- Alation contract can be extended (or cutover is achievable by Oct 1, 2026)
- Data Governance team has capacity for requirements, UAT, and adoption
- Disney-wide OMS service can accommodate DSS-specific needs

---

## 13. Appendix

### A. Requirements Gathering Interview Guide (Sample Questions)

**Current use:**
- What Alation features do you use most often?
- Walk me through a typical task in Alation.
- What would break if we lost [specific feature]?

**Enhancements:**
- What did you wish Alation could do that it doesn’t?
- What would make your job easier in a new catalog?

### B. Screenshot Checklist

- [ ] Alation search UI
- [ ] Alation glossary view
- [ ] Alation table/asset detail
- [ ] Alation lineage view
- [ ] Alation tags and custom fields
- [ ] Alation articles/documentation
- [ ] Alation policy center (if used)
- [ ] Alation reports (if used)
- [ ] OMS current dashboard
- [ ] OMS table list and detail
- [ ] OMS lineage
- [ ] OMS “Not Available” fields (gap evidence)

### C. Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | March 19, 2026 | — | Initial product brief |

---

*This product brief should be reviewed and updated as requirements gathering progresses and scope is refined.*
