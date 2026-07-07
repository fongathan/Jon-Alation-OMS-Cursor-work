# PRD — Feature 28: AI Chat Assistant in App

## Document control
- **Feature ID:** 28
- **Slug / file:** `F28-ai-chat-assistant.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
LLM conversational assistant grounded in catalog metadata for discovery and SQL hints.

## 2. Problem statement
Keyword search fails for vague questions; new users need guided answers.

## 3. Goals & non-goals
### Goals
- Deliver the outcomes described in user stories and acceptance criteria below.
- Stay compatible with OMS as system of record for technical metadata unless explicitly scoped otherwise.

### Non-goals (unless pulled into scope by program)
- Re-implement full warehouse observability or BI server admin outside catalog boundaries.

## 4. Users & primary personas
| Persona | Why they care |
|---------|----------------|
| Data Steward / Owner | Maintain accurate metadata and policies.
| Data Analyst / BI | Find and trust data for reporting.
| Data Engineer | Lineage, technical context, automation hooks.
| Governance / Compliance | Risk reduction, attestations, exports.
| Platform Admin | Connectors, access, operational health.

## 5. Functional requirements (decomposed)
### 5.1 Grounding
Retrieve relevant assets/terms; cite sources in answers.

### 5.2 Safety
PII redaction, prompt injection defenses, no training on customer data without approval.

### 5.3 Actions
Deep links to assets; optional 'copy SQL' with watermark.

### 5.4 Governance
Feature flags per domain; audit transcripts admin-only.

## 6. User stories
- As an analyst, I ask where revenue is defined and get cited assets.
- As security, I disable assistant for restricted domains.

## 7. Use cases & examples
- Natural language: 'datasets for churn model in DEET'.

## 8. UX & UI notes
Side panel or dedicated tab; feedback thumbs up/down.

## 9. Data model & API considerations
Chat completion endpoint with catalog context injection.

## 10. Non-functional requirements
Latency targets; fallback when LLM unavailable.

## 11. Acceptance criteria (testable)
- Assistant refuses uncitable claims.
- RBAC: never cites forbidden assets.

## 12. Dependencies
Search index, LLM vendor contract, legal review.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- On-prem model vs SaaS?
- MVP vs phase 2?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
