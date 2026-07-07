# PRD — Feature 20: Authentication / SSO

## Document control
- **Feature ID:** 20
- **Slug / file:** `F20-authentication-sso.md`
- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)
- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)
- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.

## 1. Summary
Enterprise SSO and RBAC aligning catalog roles to groups and datasources.

## 2. Problem statement
Weak access control exposes metadata about sensitive systems.

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
### 5.1 SSO integration
SAML/OIDC with corp IdP.

### 5.2 Roles
Admin, steward, editor, consumer, auditor read-only variants.

### 5.3 ABAC/RBAC hooks
Row-level scope by domain membership optional.

### 5.4 Session security
Idle timeout, MFA per org policy.

## 6. User stories
- As security, I require MFA for admin APIs.
- As a contractor, I see only assigned domains.

## 7. Use cases & examples
- Group membership change revokes access within minutes.

## 8. UX & UI notes
Standard OMS login flows; error pages for unauthorized deep links.

## 9. Data model & API considerations
Token validation middleware on all routes.

## 10. Non-functional requirements
Pen test coverage for token leakage vectors.

## 11. Acceptance criteria (testable)
- Direct URL to forbidden asset returns 404 or 403 per policy.
- Role changes audit logged.

## 12. Dependencies
IdP, group provisioning.

## 13. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |
| Metadata drift from sources | Connector SLAs, visible sync timestamps |
| RBAC gaps exposing sensitive names | Security review on search snippets and exports |

## 14. Open questions
- Just-in-time elevation for stewards?

---
*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*
