# Alation Functionality Reference

A comprehensive list of Alation's core functionalities with documentation links, brief explanations, and examples from your Disney Data Alation instance.

---

## 1. Search / Catalog Search

**How it works:** Full-text search across the catalog by keyword. You can filter by object type (table, article, schema, column, datasource) and optionally require all keywords to match. Results are ranked by relevance and usage statistics.

**Documentation:** [Full Page Search](https://docs.alation.com/en/latest/welcome/CatalogBasics/FullPageSearch.html)

**Example (search for "customer"):**
- **DIM_DISNEY_CUSTOMER_ENGAGEMENT** (table) — Snowflake - DSS → CONFORMED schema  
- **VIEW_DIM_CUSTOMER** (table) — Snowflake - Hulu → SUBSCRIPTIONS schema  
- **DIM_CUSTOMER_TYPES** (table) — Snowflake - Hulu → SUBS schema  

**Direct link:** [Search results for "customer"](https://disney-data.alationcloud.com/full_search/?q=customer&limit=5)

---

## 2. Data Sources

**How it works:** Data sources are the top-level connections to databases (Snowflake, PostgreSQL, etc.). Each source has schemas, tables, and columns. Alation extracts metadata, supports profiling, and can run Compose queries against them.

**Documentation:** [Adding Data Sources](https://docs.alation.com/en/latest/datasources/AddDataSources/index.html)

**Example:** Your instance includes sources such as:
- **(Private) Alation Analytics V2 - PostgreSQL DB** — For analyzing user behavior and catalog content
- **Snowflake - DSS**
- **Snowflake - Hulu**
- **Snowflake - DTCI - UP**

---

## 3. Schemas, Tables, and Columns

**How it works:** Hierarchical metadata: Data Source → Schema → Table → Column. Each level has descriptions, stewards, custom fields, and can be tagged. Tables and columns support synonyms and popularity metrics.

**Documentation:** [Working with Catalog Data](https://docs.alation.com/en/latest/sources/WorkwithCatalogData/index.html)

**Examples:**
- **Schema:** CONFORMED (Snowflake - DSS), SUBSCRIPTIONS (Snowflake - Hulu)
- **Table:** DIM_CUSTOMER, VIEW_DIM_CUSTOMER, DIM_CUSTOMER_TYPES
- **Column:** Filter by table_id or datasource_id to list columns with descriptions and data types

---

## 4. Articles (Knowledge Base)

**How it works:** Rich-text documentation pages stored in the catalog. Articles can be nested in folders, linked to data objects, and edited collaboratively. Used for data stewardship frameworks, onboarding, and process documentation.

**Documentation:** [Document Hubs](https://docs.alation.com/en/latest/welcome/DocumentHubs/index.html)

**Example:** 
- **(Ignore) Data Stewardship Framework** — Describes Data Stewardship Operating Model, governing groups (DSComm, DSC, DWG), and stewardship responsibilities
- **Welcome to Alation** — D.E.E.T.'s Data Catalog Tool with resources for catalog users and stewards

**Direct link:** [Article example](https://disneystreaming.alationcloud.com/article/3/)

---

## 5. Business Glossary

**How it works:** Centralized definitions of business terms and metrics. Terms can have descriptions, aliases, custom fields (e.g., Business Formula, Query, Data Domain, Stewards), and links to related queries or tables.

**Documentation:** [Alation Glossary](https://docs.alation.com/en/latest/welcome/Glossary/index.html)

**Example:**
- **Paid Subscribers (Subscribers)** — Definition of paid subscribers, dimensional cuts (Unactivated Paid, Paid Pending Cancel), business formulas, and links to Compose queries
- **Total Time Streamed per Entitled Account (HPS)** — Formula: [Total playback time] / [Total entitled accounts], with SQL query and background context

**Direct link:** [D.E.E.T. Unified Glossary](https://disneystreaming-dev.alationcloud.com/docs/glossary/1/)

---

## 6. Data Lineage

**How it works:** Visualizes upstream and downstream data flow for tables, columns, and dataflows. Lineage is auto-generated from query logs, metadata extraction, and Compose. Supports column-level and cross-source lineage.

**Documentation:** [Discover Lineage](https://docs.alation.com/en/latest/analyst/Lineage/index.html) | [Lineage Glossary](https://docs.alation.com/en/latest/sources/Lineage/LineageGlossary.html)

**Example:** For a table like **VIEW_DIM_CUSTOMER** (id: 364837), lineage shows:
- Upstream: source tables feeding into this view
- Downstream: tables, reports, or queries that consume this data

**Direct link:** [Table lineage example](https://disney-data.alationcloud.com/table/364837/) — open the Lineage tab

---

## 7. Compose (Saved Queries)

**How it works:** Alation Compose is an SQL editor integrated with the catalog. Users write, save, and share queries. Saved queries appear in the catalog, contribute to lineage, and can be scheduled or exported.

**Documentation:** [Alation Compose](https://www.alation.com/glossary/alation-compose/) | [Share and Access Queries](https://docs.alation.com/en/latest/analyst/ShareAndAccessQueries/ShareAndAccessQueries2023_1/index.html)

**Example:** Glossary terms like "Paid Subscribers" link to Compose queries (e.g., Metric table version, Metric build version) that implement the business logic.

**Direct link:** [Compose queries](https://disney-data.alationcloud.com/compose/)

---

## 8. Dataflows

**How it works:** Dataflow objects represent ETL/ELT jobs, stored procedures, or transformation pipelines. They appear in lineage and can be documented like tables.

**Documentation:** [Lineage Glossary — Dataflow](https://docs.alation.com/en/latest/sources/Lineage/LineageGlossary.html)

**Example:** List dataflows filtered by datasource_id to see ETL jobs for a given Snowflake or other source.

---

## 9. Tags

**How it works:** Labels applied to catalog objects (tables, columns, articles, etc.) for classification, compliance, or discovery. Tags can have descriptions and show how many objects use them.

**Documentation:** [Working with Catalog Data](https://docs.alation.com/en/latest/sources/WorkwithCatalogData/index.html)

**Examples from your instance:**
- **Core Table** — 28 objects
- **GDPR Scoped** — General Data Protection Regulation (8 objects)
- **CCPA Scoped** — California Consumer Privacy Act (15 objects)
- **Content360**, **Session360**, **Adobe** — Domain/project tags

**Direct link:** [Tags](https://disney-data.alationcloud.com/tags/)

---

## 10. Tagged Objects

**How it works:** Given a tag ID, returns all catalog objects (tables, columns, articles, etc.) that have that tag applied. Useful for compliance reporting or finding all "GDPR Scoped" tables.

**Example:** `get_tagged_objects(tag_id=15)` returns all objects tagged "GDPR Scoped".

---

## 11. Flags (Endorsements, Warnings, Deprecations)

**How it works:** Data quality signals on catalog objects:
- **ENDORSEMENT** — Marks trusted, production-ready data
- **WARNING** — Indicates known issues or caveats
- **DEPRECATION** — Marks objects as deprecated or being phased out

**Documentation:** [Working with Catalog Data — Data Quality Actions](https://docs.alation.com/en/latest/sources/WorkwithCatalogData/index.html)

**Example:** Schemas endorsed by LEAUNDRA Lewis (e.g., schema ids 79, 43, 144, 69, 165) indicate trusted data sources.

---

## 12. Domains

**How it works:** Logical groupings of catalog objects by business area. Domains help organize data by department, product, or use case. Objects can be filtered and searched by domain.

**Documentation:** [Domains Overview](https://docs.alation.com/en/latest/welcome/Domains/DomainsOverview.html)

**Examples from your instance:**
- **Ad Platforms Domain** — All objects belonging to Ad Platforms
- **DEET Data Domain** — DEET Data organization
- **Atlas Domain** — Atlas / CIM Team

**Direct link:** [Domains](https://disney-data.alationcloud.com/domains/)

---

## 13. Custom Fields

**How it works:** Admin-defined attributes (e.g., Business Steward, Data Domain, Business Formula) that can be added to glossary terms, tables, columns, and other objects. Supports text, users, groups, and multi-select values.

**Documentation:** [Custom Fields and Templates](https://docs.alation.com/en/latest/steward/TemplatesAndCustomFields/index.html)

**Example:** Glossary term "Paid Subscribers" has custom fields: Background Context, Data Domain (Subscriber), Aliases, Business Data Steward, Technical Data Steward, Business Segment (Star+, Hotstar, Hulu, Disney+, ESPN).

---

## 14. Folders

**How it works:** Organizational structure for articles and other content. Folders can contain subfolders and articles for a clear knowledge base hierarchy.

**Example:** Articles like "Data Stewardship Framework" and "Welcome to Alation" can be organized in folders such as "Data Governance" or "Onboarding".

---

## 15. Query Results & SQL

**How it works:** For saved Compose queries, you can retrieve the query metadata, SQL text, and (where permitted) query results. Supports sharing and exporting.

**Documentation:** [Work with Query Results](https://docs.alation.com/en/latest/analyst/WorkwithQueryResults/index.html)

**Example:** `get_query(query_id=1489)` returns details for the "Paid Subscribers" metric table version query.

---

## 16. Create/Update Articles

**How it works:** Create new knowledge base articles or update existing ones via API. Supports rich HTML content, attachments, and custom fields.

**Documentation:** [Document Hubs](https://docs.alation.com/en/latest/steward/Documentation/DocumentHubs/index.html)

---

## 17. Update Custom Field Values

**How it works:** Programmatically set or update custom field values on catalog objects (e.g., assign a steward, update a description field).

---

## 18. Get Current User

**How it works:** Returns the authenticated user's profile (used for API context and permissions).

---

## Summary Table

| Functionality      | Purpose                                      | Example / Link                                                                 |
|--------------------|----------------------------------------------|---------------------------------------------------------------------------------|
| Search Catalog     | Find tables, articles, columns by keyword    | [Search "customer"](https://disney-data.alationcloud.com/full_search/?q=customer) |
| Data Sources       | Database connections                         | Snowflake - DSS, Snowflake - Hulu, Alation Analytics V2                         |
| Tables & Columns   | Metadata hierarchy                           | DIM_CUSTOMER, VIEW_DIM_CUSTOMER                                                 |
| Articles           | Knowledge base documentation                 | Data Stewardship Framework, Welcome to Alation                                  |
| Glossary           | Business term definitions                    | Paid Subscribers, Total Time Streamed per Entitled Account                      |
| Lineage            | Data flow visualization                      | Table/column upstream & downstream                                            |
| Compose / Queries  | Saved SQL queries                            | Metric table version, Metric build version                                     |
| Dataflows          | ETL/transformation jobs                      | Filter by datasource                                                            |
| Tags               | Classification labels                        | Core Table, GDPR Scoped, CCPA Scoped                                           |
| Flags              | Endorsement, Warning, Deprecation             | Endorsed schemas                                                                |
| Domains            | Business area groupings                      | Ad Platforms, DEET Data, Atlas                                                 |
| Custom Fields      | Extended metadata                            | Stewards, Data Domain, Business Formula                                         |
| Folders            | Content organization                         | Article hierarchy                                                               |

---

## Official Documentation Links (with screenshots)

- [Alation User Guide (main)](https://docs.alation.com/en/latest/index.html)
- [New User Experience](https://docs.alation.com/en/latest/welcome/CatalogPages/NewUserExperience.html)
- [Full Page Search](https://docs.alation.com/en/latest/welcome/CatalogBasics/FullPageSearch.html)
- [Discover Lineage](https://docs.alation.com/en/latest/analyst/Lineage/index.html)
- [Alation Glossary](https://docs.alation.com/en/latest/welcome/Glossary/index.html)
- [Working with Catalog Data](https://docs.alation.com/en/latest/sources/WorkwithCatalogData/index.html)
- [Domains Overview](https://docs.alation.com/en/latest/welcome/Domains/DomainsOverview.html)
- [Custom Fields and Templates](https://docs.alation.com/en/latest/steward/TemplatesAndCustomFields/index.html)
- [Policy Center](https://docs.alation.com/en/latest/steward/PolicyCenter/index.html)
- [Data Dictionaries](https://docs.alation.com/en/latest/steward/DataDictionaries/index.html)

---

*Generated from Alation MCP tools and live Disney Data Alation instance. Documentation links may include screenshots in the official Alation docs.*
