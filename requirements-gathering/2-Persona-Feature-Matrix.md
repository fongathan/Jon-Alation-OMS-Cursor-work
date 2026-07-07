# Persona–Feature Matrix
**Alation to OMS Migration — Current Use Documentation**  
**Disney Streaming Services** | **Version:** 1.0 | **Date:** March 19, 2026

---

## Purpose

This matrix maps which Alation features each user persona uses. Use it to prioritize OMS build, plan training, and ensure no persona loses critical functionality. Validate with stakeholders during interviews.

---

## Persona Definitions

| Persona | Description | Example Roles |
|---------|-------------|---------------|
| **Data Steward** | Owns and maintains metadata quality for a domain; creates glossary terms, tags, descriptions | Domain stewards, data owners |
| **Data Analyst / BI User** | Consumes data for reporting and analysis; discovers and evaluates data assets | Analysts, BI developers, report builders |
| **Data Engineer** | Builds and maintains pipelines; needs lineage, technical metadata, impact analysis | DEs, platform engineers |
| **Governance / Compliance** | Ensures policies are followed; runs compliance reports; manages risk | Governance leads, compliance officers |
| **Leadership** | Consumes high-level reports; needs adoption and usage visibility | Directors, VPs |

---

## Persona–Feature Matrix

**Legend:**  
● Primary user (uses daily/weekly) | ○ Secondary user (uses occasionally) | — Not used

| Feature | Data Steward | Data Analyst / BI | Data Engineer | Governance / Compliance | Leadership |
|---------|:------------:|:-----------------:|:-------------:|:-----------------------:|:----------:|
| Search & Discovery | ● | ● | ● | ○ | — |
| Business Glossary | ● | ○ | ○ | ● | — |
| Catalog Browse | ○ | ● | ● | ○ | — |
| Table / Asset Detail | ● | ● | ● | ○ | — |
| Data Lineage | ○ | ● | ● | ● | — |
| Tags & Classification | ● | ○ | ○ | ● | — |
| Custom Fields | ● | — | ○ | ○ | — |
| Documentation / Articles | ● | ● | ○ | ○ | — |
| Ownership / Stewardship | ● | — | ○ | ● | — |
| Usage / Access Metrics | ○ | ○ | ○ | ● | ● |
| Data Sources & Connectors | ○ | ● | ● | — | — |
| Policy Center | ○ | — | — | ● | ○ |
| Compilation / Data Quality | ○ | ○ | ○ | ● | — |
| API & Integrations | ○ | ○ | ● | ○ | — |
| Version Control | ● | — | ○ | ● | — |
| Recommendations | ● | ○ | — | — | — |
| Saved Queries / Favorites | ○ | ● | ● | ○ | — |
| Comments / Discussions | ● | ● | ○ | ○ | — |
| Export / Reports | ○ | ○ | ○ | ● | ● |
| Authentication / SSO | ● | ● | ● | ● | ● |

---

## Persona-Specific Summary

### Data Steward — Critical Features
| Feature | Why Critical |
|---------|--------------|
| Business Glossary | Create and maintain terms; link to assets |
| Tags & Classification | Apply and manage tags for domain |
| Documentation / Articles | Write and update descriptions |
| Ownership / Stewardship | Assign and track ownership |
| Search & Discovery | Find assets to steward |
| Table / Asset Detail | View and edit metadata |

### Data Analyst / BI User — Critical Features
| Feature | Why Critical |
|---------|--------------|
| Search & Discovery | Find relevant data for analysis |
| Catalog Browse | Explore by source/schema |
| Table / Asset Detail | Evaluate data before use |
| Data Lineage | Understand data flow and freshness |
| Documentation / Articles | Learn how to use data |
| Saved Queries / Favorites | Quick access to frequent assets |

### Data Engineer — Critical Features
| Feature | Why Critical |
|---------|--------------|
| Data Lineage | Impact analysis, dependency mapping |
| Catalog Browse | Navigate technical structure |
| Table / Asset Detail | Technical metadata, schema |
| Data Sources & Connectors | Source connectivity |
| API & Integrations | Automation, CI/CD |
| Saved Queries / Favorites | Frequently used assets |

### Governance / Compliance — Critical Features
| Feature | Why Critical |
|---------|--------------|
| Business Glossary | Standardized terminology for policies |
| Tags & Classification | PII, sensitivity classification |
| Policy Center | Policy definition and enforcement |
| Usage / Access Metrics | Audit, usage reporting |
| Ownership / Stewardship | Accountability |
| Export / Reports | Compliance reporting |

### Leadership — Critical Features
| Feature | Why Critical |
|---------|--------------|
| Usage / Access Metrics | Adoption, ROI visibility |
| Export / Reports | Executive dashboards |

---

## Training Implications

| Persona | Training Focus |
|---------|----------------|
| Data Steward | Glossary, tags, documentation, stewardship workflows in OMS |
| Data Analyst / BI | Search, discovery, lineage, how to find and evaluate data |
| Data Engineer | Lineage, technical metadata, APIs |
| Governance / Compliance | Policy center equivalent, reporting, compliance workflows |
| Leadership | Reporting and dashboards in OMS |

---

## Validation Checklist

- [ ] Matrix validated with at least one representative per persona
- [ ] "Primary" vs. "Secondary" usage confirmed
- [ ] Any persona-specific features not in main list documented
- [ ] Training implications reviewed with L&D or change management

---

*Document owner: Data Governance | Update after stakeholder interviews*
