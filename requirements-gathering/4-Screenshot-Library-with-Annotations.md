# Screenshot Library with Annotations
**Alation to OMS Migration — Current Use Documentation**  
**Disney Streaming Services** | **Version:** 1.0 | **Date:** March 19, 2026

---

## Purpose

This library captures screenshots of Alation (and OMS) with annotations to document current usage for migration requirements. Use during stakeholder interviews to ensure nothing is missed. Annotations highlight key UI elements, workflows, and features that must be replicated in OMS.

---

## How to Use This Library

1. **Capture** — Take screenshots of each view listed below.
2. **Annotate** — Add callouts, arrows, or highlights per the annotation instructions.
3. **Store** — Save in `screenshots/` folder with the naming convention: `[Source]_[View]_[Date].png` (e.g., `Alation_Search_2026-03-19.png`).
4. **Reference** — Link or embed in this document for easy access.

---

## Screenshot Index

| # | Screenshot | Source | Priority | Status |
|---|------------|--------|----------|--------|
| 1 | Global Search | Alation | High | ☐ Captured ☐ Annotated |
| 2 | Search Results | Alation | High | ☐ Captured ☐ Annotated |
| 3 | Business Glossary — List View | Alation | High | ☐ Captured ☐ Annotated |
| 4 | Business Glossary — Term Detail | Alation | High | ☐ Captured ☐ Annotated |
| 5 | Catalog Browse / Data Sources | Alation | High | ☐ Captured ☐ Annotated |
| 6 | Table List View (e.g., Snowflake) | Alation | High | ☐ Captured ☐ Annotated |
| 7 | Table Detail — Overview | Alation | High | ☐ Captured ☐ Annotated |
| 8 | Table Detail — Lineage | Alation | High | ☐ Captured ☐ Annotated |
| 9 | Table Detail — Tags & Custom Fields | Alation | High | ☐ Captured ☐ Annotated |
| 10 | Table Detail — Documentation | Alation | High | ☐ Captured ☐ Annotated |
| 11 | Article / Documentation Page | Alation | Medium | ☐ Captured ☐ Annotated |
| 12 | Policy Center (if used) | Alation | Medium | ☐ Captured ☐ Annotated |
| 13 | Usage / Access Metrics | Alation | Medium | ☐ Captured ☐ Annotated |
| 14 | Reports / Export | Alation | Medium | ☐ Captured ☐ Annotated |
| 15 | OMS Dashboard (current) | OMS | High | ☐ Captured ☐ Annotated |
| 16 | OMS Table List | OMS | High | ☐ Captured ☐ Annotated |
| 17 | OMS Table Detail (gap evidence) | OMS | High | ☐ Captured ☐ Annotated |
| 18 | OMS Lineage | OMS | High | ☐ Captured ☐ Annotated |

---

## Annotation Instructions by Screenshot

### 1. Alation — Global Search

**What to capture:** The main search bar and any filters or quick actions visible.

**Annotations to add:**
- [ ] **Arrow/callout:** Search bar — "Primary entry point for discovery"
- [ ] **Arrow/callout:** Any filter options (type, source, etc.)
- [ ] **Arrow/callout:** Recent searches or suggestions (if visible)

**File name:** `Alation_GlobalSearch_YYYY-MM-DD.png`

---

### 2. Alation — Search Results

**What to capture:** Results page after a sample search (e.g., "subscription" or a common term).

**Annotations to add:**
- [ ] **Highlight:** Result types shown (tables, articles, glossary)
- [ ] **Arrow/callout:** Key metadata visible in results (description snippet, owner, tags)
- [ ] **Arrow/callout:** Filter/sort options

**File name:** `Alation_SearchResults_YYYY-MM-DD.png`

---

### 3. Alation — Business Glossary (List View)

**What to capture:** Glossary listing with terms.

**Annotations to add:**
- [ ] **Arrow/callout:** Term name, definition preview
- [ ] **Arrow/callout:** Steward/owner column
- [ ] **Arrow/callout:** Linked assets count (if shown)
- [ ] **Arrow/callout:** Create / Add term button

**File name:** `Alation_Glossary_List_YYYY-MM-DD.png`

---

### 4. Alation — Business Glossary (Term Detail)

**What to capture:** Full view of a single glossary term.

**Annotations to add:**
- [ ] **Arrow/callout:** Definition, synonyms, examples
- [ ] **Arrow/callout:** Linked tables/columns
- [ ] **Arrow/callout:** Steward, approval status
- [ ] **Arrow/callout:** Edit / history (if visible)

**File name:** `Alation_Glossary_TermDetail_YYYY-MM-DD.png`

---

### 5. Alation — Catalog Browse / Data Sources

**What to capture:** Hierarchy view of datasources (e.g., Snowflake > Database > Schema > Table).

**Annotations to add:**
- [ ] **Arrow/callout:** Data source list
- [ ] **Arrow/callout:** Schema/table hierarchy
- [ ] **Arrow/callout:** Metadata preview on hover/click (if any)

**File name:** `Alation_CatalogBrowse_YYYY-MM-DD.png`

---

### 6. Alation — Table List View

**What to capture:** List of tables (e.g., Snowflake schema) with columns visible.

**Annotations to add:**
- [ ] **Highlight:** Columns shown (name, description, owner, tags, etc.)
- [ ] **Arrow/callout:** Filter controls
- [ ] **Arrow/callout:** Sort options
- [ ] **Arrow/callout:** Bulk actions (if any)

**File name:** `Alation_TableList_YYYY-MM-DD.png`

---

### 7. Alation — Table Detail (Overview)

**What to capture:** Main overview of a table (description, key metadata).

**Annotations to add:**
- [ ] **Arrow/callout:** Description / Business description
- [ ] **Arrow/callout:** Owner, steward
- [ ] **Arrow/callout:** Key technical metadata (rows, size, etc.)
- [ ] **Arrow/callout:** Last updated, created

**File name:** `Alation_TableDetail_Overview_YYYY-MM-DD.png`

---

### 8. Alation — Table Detail (Lineage)

**What to capture:** Lineage diagram for a table.

**Annotations to add:**
- [ ] **Arrow/callout:** Upstream sources
- [ ] **Arrow/callout:** Downstream consumers (tables, reports)
- [ ] **Arrow/callout:** Column-level vs. table-level toggle (if available)
- [ ] **Arrow/callout:** Expand/collapse, zoom controls

**File name:** `Alation_TableDetail_Lineage_YYYY-MM-DD.png`

---

### 9. Alation — Table Detail (Tags & Custom Fields)

**What to capture:** Tags and custom metadata fields on a table.

**Annotations to add:**
- [ ] **Highlight:** Tags applied (PII, domain, etc.)
- [ ] **Arrow/callout:** Custom fields and values
- [ ] **Arrow/callout:** Add/edit tag controls

**File name:** `Alation_TableDetail_Tags_YYYY-MM-DD.png`

---

### 10. Alation — Table Detail (Documentation)

**What to capture:** Documentation section linked to the table.

**Annotations to add:**
- [ ] **Arrow/callout:** Linked articles
- [ ] **Arrow/callout:** Inline description vs. linked docs
- [ ] **Arrow/callout:** Add documentation button

**File name:** `Alation_TableDetail_Documentation_YYYY-MM-DD.png`

---

### 11. Alation — Article / Documentation Page

**What to capture:** A sample article (how-to, data dictionary entry).

**Annotations to add:**
- [ ] **Arrow/callout:** Rich text, formatting
- [ ] **Arrow/callout:** Links to catalog objects
- [ ] **Arrow/callout:** Author, last updated

**File name:** `Alation_Article_YYYY-MM-DD.png`

---

### 12. Alation — Policy Center (if used)

**What to capture:** Policy Center or compliance view.

**Annotations to add:**
- [ ] **Arrow/callout:** Policies listed
- [ ] **Arrow/callout:** Asset coverage / compliance status
- [ ] **Arrow/callout:** Report or export options

**File name:** `Alation_PolicyCenter_YYYY-MM-DD.png`

---

### 13. Alation — Usage / Access Metrics

**What to capture:** Usage stats for a table or global usage view.

**Annotations to add:**
- [ ] **Arrow/callout:** Last access, unique users
- [ ] **Arrow/callout:** Top users
- [ ] **Arrow/callout:** Query history (if visible)

**File name:** `Alation_UsageMetrics_YYYY-MM-DD.png`

---

### 14. Alation — Reports / Export

**What to capture:** Report or export interface.

**Annotations to add:**
- [ ] **Arrow/callout:** Report types available
- [ ] **Arrow/callout:** Export format (CSV, etc.)
- [ ] **Arrow/callout:** Filters applied

**File name:** `Alation_Reports_YYYY-MM-DD.png`

---

### 15. OMS — Dashboard (Current State)

**What to capture:** OMS home/dashboard as of capture date.

**Annotations to add:**
- [ ] **Arrow/callout:** Inventory summary (tables, pipelines, etc.)
- [ ] **Arrow/callout:** Navigation structure
- [ ] **Arrow/callout:** What's present vs. missing vs. Alation

**File name:** `OMS_Dashboard_YYYY-MM-DD.png`

---

### 16. OMS — Table List

**What to capture:** OMS table list (e.g., Snowflake datasource).

**Annotations to add:**
- [ ] **Arrow/callout:** Columns shown
- [ ] **Highlight:** Gaps (no glossary, no tags, no owner in list)
- [ ] **Arrow/callout:** Lineage button

**File name:** `OMS_TableList_YYYY-MM-DD.png`

---

### 17. OMS — Table Detail (Gap Evidence)

**What to capture:** OMS table detail with "Not Available" fields visible.

**Annotations to add:**
- [ ] **Highlight:** Fields showing "Not Available" (Documentation, Business Description, Created by, etc.)
- [ ] **Arrow/callout:** What is populated (technical metadata)
- [ ] **Arrow/callout:** Side-by-side comparison note to Alation

**File name:** `OMS_TableDetail_Gaps_YYYY-MM-DD.png`

---

### 18. OMS — Lineage

**What to capture:** OMS lineage view for a table.

**Annotations to add:**
- [ ] **Arrow/callout:** What lineage shows (upstream/downstream)
- [ ] **Arrow/callout:** Gaps (e.g., Airflow links "Not Available")
- [ ] **Arrow/callout:** Comparison to Alation lineage

**File name:** `OMS_Lineage_YYYY-MM-DD.png`

---

## Side-by-Side Comparison (Optional)

Create a side-by-side comparison document with:

| Feature | Alation Screenshot | OMS Screenshot | Gap Summary |
|--------|-------------------|----------------|-------------|
| Search | [Link] | [Link] | OMS has technical search only; no glossary/article search |
| Table Detail | [Link] | [Link] | OMS missing description, tags, ownership |
| Lineage | [Link] | [Link] | OMS has lineage; Airflow links not populated |
| _Add rows_ | | | |

---

## Annotation Tools

Suggested tools for adding annotations:
- **macOS:** Preview (Markup), Skitch
- **Windows:** Snipping Tool + Paint, Greenshot
- **Cross-platform:** Monosnap, Awesome Screenshot, Figma (for detailed annotations)

---

## Folder Structure

```
requirements-gathering/
├── screenshots/
│   ├── alation/
│   │   ├── Alation_GlobalSearch_2026-03-19.png
│   │   ├── Alation_Glossary_List_2026-03-19.png
│   │   └── ...
│   └── oms/
│       ├── OMS_Dashboard_2026-03-19.png
│       └── ...
├── 1-Feature-Inventory-Matrix.md
├── 2-Persona-Feature-Matrix.md
├── 3-Workflow-Diagrams-and-Process-Docs.md
└── 4-Screenshot-Library-with-Annotations.md
```

---

## Validation Checklist

- [ ] All high-priority screenshots captured
- [ ] Annotations added per instructions
- [ ] Files named consistently
- [ ] Screenshots linked or embedded in this document
- [ ] Side-by-side comparison completed for gap analysis

---

*Document owner: Data Governance | Update as screenshots are captured*
