#!/usr/bin/env python3
"""Generate PRD markdown files from structured metadata. Re-run after matrix changes."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FEATURES: list[dict] = [
    {
        "num": 1,
        "slug": "search-discovery",
        "title": "Search & Discovery",
        "summary": "Unified discovery across technical and business metadata so users can find tables, columns, articles, glossary terms, and related assets quickly.",
        "problem": "Users waste time hunting across sources, wikis, and chat without a single query surface aligned to how DSS names and organizes data.",
        "components": [
            {"name": "Global search entry", "detail": "Prominent search in shell/header; keyboard shortcut optional; scope indicator (all sources vs current datasource)."},
            {"name": "Index & ranking", "detail": "Keyword match on names, descriptions, tags, stewards, glossary terms; optional semantic/vector tier later; de-duplicate logical entities."},
            {"name": "Scoped filters", "detail": "Post-search facets: domain, environment, sensitivity, owner, object type, trust flag."},
            {"name": "Result cards / rows", "detail": "Title, type badge, 1-line description, steward, key tags, datasource; click opens asset context."},
            {"name": "Zero-result & disambiguation", "detail": "Suggestions, synonym expansion from glossary, clear empty state."},
        ],
        "stories": [
            "As an analyst, I search for a business concept and land on the canonical table and glossary definition.",
            "As a steward, I search within my domain to find undescribed assets to prioritize.",
            "As an engineer, I search by pipeline or dataset name and open lineage in one step.",
        ],
        "use_cases": [
            "New hire looks up 'subscriber revenue' and finds the approved metric table plus policy notes.",
            "Compliance officer searches for PII-tagged assets under a program code.",
        ],
        "ui": "Header search + full-width results page; facet panel; saved scope presets (phase 2).",
        "api": "Search API returning typed hits with snippets and facet counts; rate limits for automation.",
        "nfr": "P95 search under agreed SLA; audit log for sensitive scopes if required by policy.",
        "acceptance": ["Given indexed assets, when user types a known table name then the asset appears in top 5 results.", "When user applies domain facet, only in-domain assets show.", "Search respects RBAC: user never sees forbidden object titles/snippets."],
        "deps": "Ingestion completeness, RBAC model, glossary synonym graph.",
        "open": ["Semantic search in MVP or phase 2?", "Cross-tool search (Confluence) in scope?"],
        "related": ["../1-Feature-Inventory-Matrix.md", "../../business-data-catalog/bdc-requirements-map.html (R-01)"],
    },
    {
        "num": 2,
        "slug": "business-glossary",
        "title": "Business Glossary",
        "summary": "Controlled vocabulary of business terms with definitions, synonyms, stewardship, and links to physical data elements.",
        "problem": "Teams use inconsistent labels for the same concept; policies and reports reference terms that are not tied to actual columns.",
        "components": [
            {"name": "Term CRUD", "detail": "Create/edit/retire terms; status (draft/published/deprecated); rich-text definition."},
            {"name": "Synonyms & abbreviations", "detail": "Alternate labels for search and documentation."},
            {"name": "Stewardship", "detail": "Primary owner, backup, domain linkage, review cadence."},
            {"name": "Mappings", "detail": "Link terms to tables/columns/metrics; cardinality and confidence optional."},
            {"name": "Consumption surfaces", "detail": "Term appears on asset detail, search snippets, policy references."},
        ],
        "stories": [
            "As a steward, I publish a term and map it to the authoritative columns.",
            "As an analyst, I hover a column and see the glossary definition.",
        ],
        "use_cases": ["Finance publishes 'ARPU' with formula narrative and maps to three warehouse columns across envs."],
        "ui": "Glossary list + term detail; mapping UI with picker for catalog objects; change history.",
        "api": "REST for term lifecycle and bulk mapping import.",
        "nfr": "Published terms immutable without new version or audit reason.",
        "acceptance": ["Published term visible on all mapped assets.", "Search finds term by synonym.", "Deprecation blocks new mappings and surfaces banner on assets."],
        "deps": "Domain model, RBAC for publishers vs consumers.",
        "open": ["Workflow for approving new terms?", "Integration with external glossary?"],
        "related": ["../2-Persona-Feature-Matrix.md"],
    },
    {
        "num": 3,
        "slug": "catalog-browse",
        "title": "Catalog Browse",
        "summary": "Hierarchical and faceted browsing of datasources, schemas, databases, and tables consistent with OMS mental models.",
        "problem": "Users who do not know exact names need safe exploration without running queries.",
        "components": [
            {"name": "Datasource catalog", "detail": "Cards or list of registered sources with health/counts."},
            {"name": "Drill hierarchy", "detail": "Datasource → database/schema → table (source-specific shapes abstracted)."},
            {"name": "Column preview", "detail": "Optional expand for column list with types and business fields."},
            {"name": "Contextual BDC strip", "detail": "Business chips when browsing within a technical context (integrated pattern)."},
        ],
        "stories": ["As an engineer, I browse Unity vs Snowflake namespaces side by side in OMS.", "As an analyst, I browse only prod assets in my domain."],
        "use_cases": ["User navigates Snowflake ANALYTICS → MART → FACT_SUBSCRIPTION."],
        "ui": "Breadcrumbs, left tree optional, paginated tables, LINEAGE action per row where applicable.",
        "api": "Child listing endpoints with cursor pagination.",
        "nfr": "Large schemas remain responsive via pagination and lazy load.",
        "acceptance": ["Breadcrumb matches user location.", "Pagination stable under sort/filter."],
        "deps": "Connector metadata freshness.",
        "open": ["Favorite paths / pinned hierarchies?"],
        "related": ["../../business-data-catalog/bdc-requirements-map.html (R-09)"],
    },
    {
        "num": 4,
        "slug": "table-asset-detail",
        "title": "Table / Asset Detail",
        "summary": "Authoritative asset page combining technical metadata, business metadata, lineage entry points, and stewardship.",
        "problem": "Fragmented views force users to open many tools before trusting data.",
        "components": [
            {"name": "Overview", "detail": "Name, type, description, owners, tags, trust flags, key stats."},
            {"name": "Technical metadata", "detail": "Row counts, partitioning, retention hints, operational fields as available from OMS."},
            {"name": "Business metadata", "detail": "Sensitivity, policies, glossary links, custom fields."},
            {"name": "Schema / columns", "detail": "Grid with technical + business columns; inline or drawer edit."},
            {"name": "Tabs / drawers", "detail": "Lineage, queries, samples per program decision (integrated vs on-top)."},
        ],
        "stories": ["As a steward, I edit description and owner with pending-change UX.", "As an analyst, I read trust flag and deprecation reason before querying."],
        "use_cases": ["Deprecated table shows red banner, successor link, and read-only technical stats."],
        "ui": "Integrated: full technical + business. On-top: business-first with deep link to full OMS technical page.",
        "api": "GET asset; PATCH business fields with ETag.",
        "nfr": "Field-level audit trail for business edits.",
        "acceptance": ["All mandatory business fields visible per policy.", "Unauthorized user cannot PATCH.", "Lineage button opens same modal/page as browse."],
        "deps": "Trust flags feature, glossary mappings.",
        "open": ["Which tabs ship MVP vs later?"],
        "related": ["../../business-data-catalog/BDC-OMS-integrated-vs-on-top-decision.md"],
    },
    {
        "num": 5,
        "slug": "data-lineage",
        "title": "Data Lineage",
        "summary": "Upstream/downstream relationships at table, column, and pipeline granularity for impact analysis and onboarding.",
        "problem": "Schema changes break unknown downstream consumers; root-cause analysis is slow.",
        "components": [
            {"name": "Graph / list hybrid", "detail": "Visual graph where supported; tabular upstream/downstream fallback."},
            {"name": "Column lineage", "detail": "Optional drill from column row."},
            {"name": "Pipeline linkage", "detail": "Connect to dataflows/jobs where OMS stores them."},
            {"name": "Export", "detail": "Lineage download for audits (align with OMS lineage downloads)."},
        ],
        "stories": ["As an engineer, I see downstream dashboards affected by a column rename.", "As governance, I export lineage for a regulator request."],
        "use_cases": ["Airflow DAG → dbt model → Snowflake table chain visible end-to-end when metadata exists."],
        "ui": "LINEAGE button on lists; modal or full page; loading states for large graphs.",
        "api": "Lineage query by asset id and depth; async job for bulk export if needed.",
        "nfr": "Depth limits and timeouts with partial results + warning.",
        "acceptance": ["Table-level lineage renders within SLA for N edges.", "RBAC hides unauthorized nodes or shows stub."],
        "deps": "Ingestion from dbt/Airflow/Snowflake as available.",
        "open": ["Column lineage coverage targets?"],
        "related": ["../../business-data-catalog/bdc-requirements-map.html (R-04)"],
    },
    {
        "num": 6,
        "slug": "tags-classification",
        "title": "Tags & Classification",
        "summary": "Controlled and extensible tags for sensitivity, domain, lifecycle, and custom programs.",
        "problem": "Manual email-driven classification does not scale; filters for compliance are unreliable.",
        "components": [
            {"name": "Tag dictionary", "detail": "Admin-defined tags with categories, colors, descriptions."},
            {"name": "Application UI", "detail": "Multi-select on asset, column-level tags optional."},
            {"name": "Bulk tag", "detail": "Ties to mass edit and rules engine."},
            {"name": "Reporting", "detail": "Filter catalog and exports by tag combinations."},
        ],
        "stories": ["As governance, I require 'PII' tag before prod promotion.", "As a steward, I bulk-remove obsolete program tags."],
        "use_cases": ["Tag 'GDPR-Relevant' applied to 400 tables via CSV import with audit."],
        "ui": "Pills on detail; filter row on tables; import tags action in integrated toolbar.",
        "api": "Tag CRUD; bulk apply endpoint.",
        "nfr": "Tag changes audited with actor and timestamp.",
        "acceptance": ["Cannot apply retired tag.", "Facet counts match authoritative index within refresh window."],
        "deps": "RBAC for who can create vs apply tags.",
        "open": ["Hierarchical tags?"],
        "related": ["../1-Feature-Inventory-Matrix.md Appendix Tags"],
    },
    {
        "num": 7,
        "slug": "custom-fields",
        "title": "Custom Fields",
        "summary": "Configurable metadata fields per object type to capture domain-specific attributes beyond core schema.",
        "problem": "One-size metadata misses retention category, cost center, data product IDs, etc.",
        "components": [
            {"name": "Field definitions", "detail": "Types: text, number, date, enum, URL; required/optional per type or domain."},
            {"name": "Rendering", "detail": "Dynamic form sections on asset detail and exports."},
            {"name": "Validation", "detail": "Regex, max length, enum enforcement."},
            {"name": "Dictionary round-trip", "detail": "Include in download/upload templates."},
        ],
        "stories": ["As a domain admin, I add 'Data Product ID' to all tables in my domain.", "As an analyst, I filter by that field."],
        "use_cases": ["DEET adds enum for 'Consumer jurisdiction' on sensitive marts."],
        "ui": "Collapsible 'Custom attributes' card; empty vs filled states.",
        "api": "Schema registry for custom fields; PATCH validates against schema.",
        "nfr": "Schema migrations backward compatible or versioned.",
        "acceptance": ["Invalid enum rejected with clear error.", "Field appears in CSV export column set."],
        "deps": "Tag and domain scoping rules.",
        "open": ["Who can define fields globally vs per domain?"],
        "related": ["../1-Feature-Inventory-Matrix.md Appendix Custom Fields"],
    },
    {
        "num": 8,
        "slug": "documentation-articles",
        "title": "Documentation / Articles",
        "summary": "Rich-text knowledge attached to catalog objects or organized in folders for how-tos and data product docs.",
        "problem": "Tribal knowledge lives outside the catalog; onboarding is slow.",
        "components": [
            {"name": "Editor", "detail": "Markdown or WYSIWYG; attachments; internal links to assets."},
            {"name": "Linking model", "detail": "Many-to-many articles ↔ assets; primary article flag optional."},
            {"name": "Folders / spaces", "detail": "See Folders feature for hierarchy."},
            {"name": "Permissions", "detail": "Author vs reader; draft/publish workflow optional."},
        ],
        "stories": ["As a steward, I attach a getting-started article to a complex dataset.", "As an analyst, I read the article from asset detail."],
        "use_cases": ["How-to for quarterly close checks linked to finance marts."],
        "ui": "Articles tab on asset; print-friendly view.",
        "api": "CRUD articles; link endpoints.",
        "nfr": "Full-text search included in global search index.",
        "acceptance": ["Broken internal links detected on publish (optional).", "Unpublished drafts invisible to readers."],
        "deps": "SSO groups for authoring.",
        "open": ["Confluence coexistence / embed?"],
        "related": [],
    },
    {
        "num": 9,
        "slug": "ownership-stewardship",
        "title": "Ownership / Stewardship",
        "summary": "Clear accountability: data owner, technical owner, stewards, escalation paths on assets and domains.",
        "problem": "No single accountable party when quality or access issues arise.",
        "components": [
            {"name": "Role assignments", "detail": "Owner, steward, delegate; inherit from domain with override."},
            {"name": "Directory integration", "detail": "Resolve people from corporate directory; show contact."},
            {"name": "Coverage metrics", "detail": "Dashboard widgets: % assets with owner in domain."},
            {"name": "Escalation", "detail": "Link to request workflow for ownership disputes."},
        ],
        "stories": ["As leadership, I see owner coverage by domain.", "As a user, I request access from the listed steward."],
        "use_cases": ["Domain reorg: bulk reassign stewards via CSV."],
        "ui": "People chips with avatar; empty state prompts assignment for stewards.",
        "api": "PATCH owners; bulk assign.",
        "nfr": "Invalid user ids rejected at API boundary.",
        "acceptance": ["Inherited owner visible with source badge.", "Removing last steward blocked if policy requires one."],
        "deps": "HR/directory API, domain model.",
        "open": ["Co-owner vs single owner policy?"],
        "related": [],
    },
    {
        "num": 10,
        "slug": "usage-access-metrics",
        "title": "Usage / Access Metrics",
        "summary": "Signals from query logs and catalog telemetry: popularity, last access, top users, for prioritization and risk.",
        "problem": "Stewards guess what matters; unused assets stay over-documented while hot paths lack care.",
        "components": [
            {"name": "Ingestion", "detail": "Warehouse access logs, BI tool telemetry where licensed, catalog view events."},
            {"name": "Rollups", "detail": "7/30/90 day windows; PII-safe aggregation."},
            {"name": "Presentation", "detail": "Sparkline or counts on asset; leadership dashboards."},
        ],
        "stories": ["As a steward, I sort domain inventory by last query date.", "As leadership, I see MAU for catalog."],
        "use_cases": ["Deprecation campaign targets tables with zero reads in 12 months."],
        "ui": "Column on inventory optional; tooltip definitions for metric source.",
        "api": "Read-only metrics endpoints; export for analytics team.",
        "nfr": "Latency tolerances for batch vs near-real-time clearly documented.",
        "acceptance": ["Metrics never expose row-level data.", "Metric definitions versioned and visible to users."],
        "deps": "Data platform agreements for log sharing.",
        "open": ["Per-user visibility restricted to admins only?"],
        "related": [],
    },
    {
        "num": 11,
        "slug": "data-sources-connectors",
        "title": "Data Sources & Connectors",
        "summary": "Registration, credentialing, scheduling, and health of metadata connectors into OMS/BDC.",
        "problem": "Stale or missing sources undermine trust in the entire catalog.",
        "components": [
            {"name": "Connector catalog", "detail": "Snowflake, Unity, Tableau, Airflow, etc. per OMS roadmap."},
            {"name": "Sync jobs", "detail": "Schedule, manual run, last success, error surfacing."},
            {"name": "Scope controls", "detail": "Include/exclude databases, schemas, projects."},
            {"name": "Secrets management", "detail": "Vault integration; no secrets in UI."},
        ],
        "stories": ["As platform admin, I add a new Snowflake account with scoped schemas.", "As governance, I see connector lag SLAs."],
        "use_cases": ["Connector fails; UI shows actionable error and ticket link."],
        "ui": "Admin tab pattern in on-top BDC; or OMS native admin surface.",
        "api": "Connector CRUD and trigger sync (admin scoped).",
        "nfr": "Incremental sync where supported; full refresh windows communicated.",
        "acceptance": ["New table appears within agreed lag after warehouse DDL.", "Failed sync visible on datasource home."],
        "deps": "Network, IAM roles, warehouse admin cooperation.",
        "open": ["BYO connector SDK in scope?"],
        "related": ["../../business-data-catalog/bdc-requirements-map.html (R-12 partial)"],
    },
    {
        "num": 12,
        "slug": "policy-center",
        "title": "Policy Center",
        "summary": "Map organizational policies to catalog objects: retention, classification, handling instructions.",
        "problem": "Policies live in PDFs; engineers cannot see actionable rules next to data.",
        "components": [
            {"name": "Policy definitions", "detail": "Title, version, applicability rules (tags, domains, sensitivity)."},
            {"name": "Attachments", "detail": "Link policies to assets; display summary + deep link to GRC system optional."},
            {"name": "Compliance views", "detail": "Reports of coverage and exceptions."},
        ],
        "stories": ["As compliance, I attach retention policy to all customer PII datasets.", "As an engineer, I read handling rules on the asset page."],
        "use_cases": ["Policy pack v3 rolls out; catalog shows banner until assets re-attested."],
        "ui": "Policies tab/section in on-top pattern; chips on integrated strip.",
        "api": "Policy association CRUD; read filters for catalog export.",
        "nfr": "Policy changes audited.",
        "acceptance": ["Removing policy requires permission.", "Conflicting policies flagged to admin."],
        "deps": "Glossary and tags for applicability.",
        "open": ["Authoritative system of record: OMS vs external GRC?"],
        "related": ["../../business-data-catalog/bdc-requirements-map.html (R-03, R-05)"],
    },
    {
        "num": 13,
        "slug": "compilation-data-quality",
        "title": "Compilation / Data Quality",
        "summary": "Profiling, rules, and compilation signals surfaced where OMS already captures them; optional expansion for BDC.",
        "problem": "Consumers discover broken data only after shipping reports.",
        "components": [
            {"name": "Profiles", "detail": "Null rates, cardinality, min/max where supported."},
            {"name": "Rules & alerts", "detail": "Pass/warn/fail with schedule; link to incident workflow optional."},
            {"name": "Compilation", "detail": "dbt/test or platform-specific compile errors if integrated."},
        ],
        "stories": ["As an engineer, I see last profile timestamp on column.", "As governance, I see failing assets in a domain report."],
        "use_cases": ["Freshness SLA breach highlights asset in steward inbox (phase 2)."],
        "ui": "Quality tab or subsection; avoid duplicating full observability product—link out when needed.",
        "api": "Read profile snapshots; optional webhook on rule failure.",
        "nfr": "Profiling cost controls (sample size, schedule).",
        "acceptance": ["If no profile exists, UI states 'not run' not silent empty.", "PII columns masked in profile views for restricted roles."],
        "deps": "Compute for profiling, warehouse permissions.",
        "open": ["MVP depth: profile only vs full rules engine?"],
        "related": [],
    },
    {
        "num": 14,
        "slug": "api-integrations",
        "title": "API & Integrations",
        "summary": "REST/GraphQL-style APIs and tokens for automation, CI/CD metadata updates, and BI embedding.",
        "problem": "Manual catalog updates lag code changes; integrators need stable contracts.",
        "components": [
            {"name": "Public contract", "detail": "Versioned OpenAPI; deprecation policy."},
            {"name": "Auth", "detail": "SSO for humans; service principals / PAT for automation with scopes."},
            {"name": "Bulk endpoints", "detail": "Batch PATCH, async job for large uploads."},
            {"name": "Webhooks", "detail": "Optional events: asset updated, tag applied."},
        ],
        "stories": ["As a DE, I update descriptions from CI when dbt model changes.", "As a tool vendor, I embed catalog iframe with SSO."],
        "use_cases": ["Nightly job reconciles owners from internal CMDB."],
        "ui": "Developer portal page: keys, examples, rate limit status.",
        "api": "Core of feature—documented limits and error codes.",
        "nfr": "Idempotency keys for bulk writes; SLO for read APIs.",
        "acceptance": ["429 with Retry-After when throttled.", "Invalid payload returns field-level errors."],
        "deps": "API gateway, audit store.",
        "open": ["GraphQL vs REST only?"],
        "related": ["../../business-data-catalog/bdc-requirements-map.html (R-08)"],
    },
    {
        "num": 15,
        "slug": "version-control",
        "title": "Version Control",
        "summary": "History of business metadata changes with optional compare and restore.",
        "problem": "Regulators and incident reviews need to know who changed what and when.",
        "components": [
            {"name": "Audit log UI", "detail": "Per-asset timeline of field changes."},
            {"name": "Diff view", "detail": "Before/after for text fields."},
            {"name": "Restore", "detail": "Admin/steward restore prior value with new audit entry."},
        ],
        "stories": ["As compliance, I export change history for an asset for 2 years.", "As a steward, I undo a mistaken bulk description."],
        "use_cases": ["Incident: prove deprecation notice was added before outage."],
        "ui": "History tab; filters by field and actor.",
        "api": "GET history; POST restore with reason.",
        "nfr": "Immutable append-only audit store.",
        "acceptance": ["No silent overwrites without version bump in audit.", "Restore requires reason string."],
        "deps": "Identity service for stable actor ids.",
        "open": ["Retention of audit events?"],
        "related": [],
    },
    {
        "num": 16,
        "slug": "recommendations",
        "title": "Recommendations / Suggestions",
        "summary": "Lightweight suggestions for descriptions, tags, stewards based on heuristics or ML (distinct from full chat assistant).",
        "problem": "Metadata debt grows faster than steward capacity.",
        "components": [
            {"name": "Suggestion engine", "detail": "Rules: copy from similar asset name patterns; optional ML."},
            {"name": "Inbox UX", "detail": "Accept/dismiss per suggestion; batch accept."},
            {"name": "Feedback loop", "detail": "Dismissal trains suppression (phase 2)."},
        ],
        "stories": ["As a steward, I accept 10 tag suggestions generated from column names.", "As governance, I tune which rules run per domain."],
        "use_cases": ["Suggest 'email' PII tag when column names match regex."],
        "ui": "Badge on asset; queue in steward dashboard.",
        "api": "Generate suggestions job; POST accept/dismiss.",
        "nfr": "Suggestions never auto-apply without policy flag.",
        "acceptance": ["User sees confidence or rule name for each suggestion.", "Dismiss is audited."],
        "deps": "Feature 6 tags, profiling optional.",
        "open": ["ML vs rules-only MVP?"],
        "related": [],
    },
    {
        "num": 17,
        "slug": "saved-queries-favorites",
        "title": "Saved Queries / Favorites",
        "summary": "Bookmark assets, saved searches, and optional shared lists for teams.",
        "problem": "Repeat navigation for recurring analysis work.",
        "components": [
            {"name": "Favorites", "detail": "Star asset; list in home sidebar."},
            {"name": "Saved search", "detail": "Persist filter + query string; optional alert on new matches."},
            {"name": "Collections", "detail": "Curated lists for onboarding packs (phase 2)."},
        ],
        "stories": ["As an analyst, I star my five weekly KPI tables.", "As a lead, I share a saved search for 'unowned marts'."],
        "use_cases": ["New team member clones starter collection from lead."],
        "ui": "Star icon on rows; Favorites page; save search dialog.",
        "api": "CRUD favorites and saved searches per user.",
        "nfr": "Privacy: shared lists respect RBAC on contained assets.",
        "acceptance": ["Cannot favorite asset user cannot read.", "Deleting asset removes from favorites gracefully."],
        "deps": "User identity.",
        "open": ["Org-wide curated lists ownership model?"],
        "related": [],
    },
    {
        "num": 18,
        "slug": "comments-discussions",
        "title": "Comments / Discussions",
        "summary": "Threaded discussion on assets for Q&A and change coordination.",
        "problem": "Questions repeat in Slack without durable record on the asset.",
        "components": [
            {"name": "Threads", "detail": "Top-level comment, replies, @mentions optional."},
            {"name": "Moderation", "detail": "Steward can lock or hide abusive content."},
            {"name": "Notifications", "detail": "Email or in-app on reply."},
        ],
        "stories": ["As an analyst, I ask if a column is still populated.", "As a steward, I pin official answer."],
        "use_cases": ["Schema migration discussion attached to table for audit."],
        "ui": "Comments tab; markdown lite; sort by newest.",
        "api": "CRUD comments; pagination.",
        "nfr": "Retention and export for legal hold.",
        "acceptance": ["Deleted user shows as 'Former user' without PII leak.", "Pinning limited to stewards."],
        "deps": "Notification service.",
        "open": ["Integration with Slack threads?"],
        "related": [],
    },
    {
        "num": 19,
        "slug": "export-reports",
        "title": "Export / Reports",
        "summary": "CSV/Excel exports and scheduled reports for catalog state, usage, and compliance.",
        "problem": "Execs and auditors need snapshots outside the UI.",
        "components": [
            {"name": "Ad hoc export", "detail": "From any filtered inventory view."},
            {"name": "Templates", "detail": "Standard compliance column packs."},
            {"name": "Scheduling", "detail": "Email delivery or S3 drop (phase 2)."},
        ],
        "stories": ["As governance, I export all PII-tagged tables monthly.", "As PM, I export backlog of missing descriptions."],
        "use_cases": ["Audit workbook with owner, domain, last access, policies."],
        "ui": "Export button with column picker; progress for large exports.",
        "api": "Async export job with download URL.",
        "nfr": "Exports watermarked or access-logged if sensitive.",
        "acceptance": ["Export respects current filters and RBAC.", "Large export emails link with expiry."],
        "deps": "Object storage for temp files.",
        "open": ["Max rows per export?"],
        "related": [],
    },
    {
        "num": 20,
        "slug": "authentication-sso",
        "title": "Authentication / SSO",
        "summary": "Enterprise SSO and RBAC aligning catalog roles to groups and datasources.",
        "problem": "Weak access control exposes metadata about sensitive systems.",
        "components": [
            {"name": "SSO integration", "detail": "SAML/OIDC with corp IdP."},
            {"name": "Roles", "detail": "Admin, steward, editor, consumer, auditor read-only variants."},
            {"name": "ABAC/RBAC hooks", "detail": "Row-level scope by domain membership optional."},
            {"name": "Session security", "detail": "Idle timeout, MFA per org policy."},
        ],
        "stories": ["As security, I require MFA for admin APIs.", "As a contractor, I see only assigned domains."],
        "use_cases": ["Group membership change revokes access within minutes."],
        "ui": "Standard OMS login flows; error pages for unauthorized deep links.",
        "api": "Token validation middleware on all routes.",
        "nfr": "Pen test coverage for token leakage vectors.",
        "acceptance": ["Direct URL to forbidden asset returns 404 or 403 per policy.", "Role changes audit logged."],
        "deps": "IdP, group provisioning.",
        "open": ["Just-in-time elevation for stewards?"],
        "related": [],
    },
    {
        "num": 21,
        "slug": "flags-endorsements-deprecations",
        "title": "Flags (Endorsements, Warnings, Deprecations)",
        "summary": "Trust signals: endorsed, experimental, deprecated—with reasons, dates, and attribution.",
        "problem": "Analysts cannot tell curated vs legacy junk without tribal knowledge.",
        "components": [
            {"name": "Flag types", "detail": "Trusted/endorsed, warning, deprecated; optional custom."},
            {"name": "Scope", "detail": "Schema, table, column level per program."},
            {"name": "Attribution", "detail": "Who set flag, when, reason text, optional successor link."},
            {"name": "UX enforcement", "detail": "Query tools may warn on deprecated (integration point optional)."},
        ],
        "stories": ["As a steward, I deprecate a table with successor URL.", "As an analyst, I see red banner before running SQL."],
        "use_cases": ["Migration: bulk mark legacy Alation-endorsed assets in OMS."],
        "ui": "Trust strip under title; column-level toggles in schema grid (see prototype).",
        "api": "PATCH trust state with validation transitions.",
        "nfr": "High visibility changes notify subscribers.",
        "acceptance": ["Deprecation requires reason if policy enabled.", "Column flag visible in inventory export."],
        "deps": "Notification optional, stewardship roles.",
        "open": ["Endorsement governance: who can endorse?"],
        "related": ["../../business-data-catalog/bdc-requirements-map.html (R-11)", "../../business-data-catalog/bdc-trust-flags.js"],
    },
    {
        "num": 22,
        "slug": "domains",
        "title": "Domains",
        "summary": "Business grouping for search scope, stewardship defaults, and policy application (e.g., DEEPT, Ad Platforms).",
        "problem": "Enterprise catalog is too large without domain boundaries.",
        "components": [
            {"name": "Domain registry", "detail": "Name, charter, leads, member groups."},
            {"name": "Asset membership", "detail": "Manual, inherited from path rules, or hybrid."},
            {"name": "Scoped experiences", "detail": "Default filters, dashboards, steward queues per domain."},
        ],
        "stories": ["As a domain lead, I see only my assets in default view.", "As enterprise governance, I compare coverage across domains."],
        "use_cases": ["DEEPT domain auto-includes tables under approved database prefixes."],
        "ui": "Domain switcher; badges on assets; domain admin settings.",
        "api": "Domain CRUD; membership rules engine.",
        "nfr": "Membership recomputation jobs observable.",
        "acceptance": ["User in two domains can switch context without re-login.", "Asset cannot be orphaned if policy requires domain."],
        "deps": "IdP groups for membership.",
        "open": ["Overlap / multi-domain assets?"],
        "related": ["../../AGENTS.md (DEEPT context)"],
    },
    {
        "num": 23,
        "slug": "folders",
        "title": "Folders",
        "summary": "Hierarchical organization for articles and documentation separate from technical hierarchy.",
        "problem": "Flat article lists become unnavigable at scale.",
        "components": [
            {"name": "Folder tree", "detail": "Nested folders; permissions inherit with override."},
            {"name": "Move / copy", "detail": "Articles relocate with audit."},
            {"name": "Navigation", "detail": "Breadcrumb in knowledge section."},
        ],
        "stories": ["As a steward, I group onboarding articles under 'Q1 2027'.", "As a reader, I browse folder structure like a mini wiki."],
        "use_cases": ["How-to folder vs project-specific collections per matrix notes."],
        "ui": "Left tree + content pane; drag-drop optional phase 2.",
        "api": "Folder CRUD; list children.",
        "nfr": "Max depth / count limits to prevent abuse.",
        "acceptance": ["Circular moves prevented.", "Unauthorized folder hidden from search."],
        "deps": "Articles feature, RBAC.",
        "open": ["Shared with Confluence hierarchy?"],
        "related": [],
    },
    {
        "num": 24,
        "slug": "dataflows",
        "title": "Dataflows",
        "summary": "First-class objects for jobs, DAGs, dbt models, procedures—linked to tables and lineage.",
        "problem": "Lineage alone loses the executable context engineers need.",
        "components": [
            {"name": "Object types", "detail": "Airflow DAG, dbt model, stored proc, Spark job, etc."},
            {"name": "Metadata", "detail": "Owner, schedule, repo link, runtime stats if available."},
            {"name": "Relationships", "detail": "Reads/writes edges to datasets."},
        ],
        "stories": ["As an engineer, I open the dbt model from the fact table page.", "As SRE, I jump to Airflow from lineage node."],
        "use_cases": ["sales_transform dbt model shows tests and repo path."],
        "ui": "Dataflow detail page; appears as node in lineage graph.",
        "api": "CRUD/read from OMS ingestion pipelines.",
        "nfr": "Dedup same logical job from multiple ingest sources.",
        "acceptance": ["From table, list upstream dataflows with schedule.", "Broken repo links flagged."],
        "deps": "Airflow/dbt connectors.",
        "open": ["Which orchestrators MVP?"],
        "related": ["../1-Feature-Inventory-Matrix.md row 24 note vs lineage"],
    },
    {
        "num": 25,
        "slug": "admin-analytics-dashboard",
        "title": "Admin Analytics Dashboard",
        "summary": "Pre-built and exploratory analytics for catalog adoption, curation, search, and governance—admin role.",
        "problem": "Program sponsors cannot prove value; stewards lack backlog signals.",
        "components": [
            {"name": "Dashboards", "detail": "Executive summary, adoption, curation progress, search quality."},
            {"name": "Ad hoc query", "detail": "SQL or guided query over telemetry warehouse."},
            {"name": "Filters", "detail": "Time, team, asset type, domain."},
            {"name": "Export", "detail": "CSV from widgets."},
        ],
        "stories": ["As admin, I view MAU and top searches.", "As governance, I find domains with declining description coverage."],
        "use_cases": ["Quarterly business review slide data exported from dashboard."],
        "ui": "Dedicated admin section; Chart.js or embedded BI per platform choice.",
        "api": "Read-only analytics API or reuse warehouse connection.",
        "nfr": "PII minimization in telemetry; retention policy published.",
        "acceptance": ["Only admin role sees user-level detail if exposed.", "Dashboards load within agreed time with cache."],
        "deps": "Telemetry pipeline into warehouse.",
        "open": ["Overlap with feature 12 R-12 prototype consolidation?"],
        "related": ["../../business-data-catalog/partials/bdc-alation-admin.html"],
    },
    {
        "num": 26,
        "slug": "mass-bulk-edit",
        "title": "Mass / Bulk Edit",
        "summary": "Select many assets and apply metadata changes once; CSV upload with validation and audit.",
        "problem": "One-by-one edits block migration and domain-wide policy updates.",
        "components": [
            {"name": "Selection UI", "detail": "Checkboxes, select all in page, select all matching filter with warning."},
            {"name": "Bulk form", "detail": "Apply tags, owners, descriptions pattern, clear fields."},
            {"name": "CSV pipeline", "detail": "Template download, upload, dry-run, error report, commit."},
            {"name": "Job tracking", "detail": "Async for large jobs; email on completion."},
        ],
        "stories": ["As a steward, I assign owner to 200 tables.", "As governance, I dry-run CSV before apply."],
        "use_cases": ["Reorg: mapping file table FQN → new steward imported."],
        "ui": "Bulk action bar; progress modal; downloadable error CSV.",
        "api": "Bulk PATCH job creation; status polling.",
        "nfr": "Idempotent retries; partial failure semantics documented.",
        "acceptance": ["Dry-run shows row-level errors without writes.", "Every committed row has audit actor=batch job+user."],
        "deps": "RBAC bulk permission, dictionary upload F29.",
        "open": ["Max assets per job?"],
        "related": [],
    },
    {
        "num": 27,
        "slug": "mass-set-rules-catalog-sets",
        "title": "Mass Set Rules / Catalog Sets",
        "summary": "Rule-defined dynamic sets of assets for tagging, ownership, and policy application at scale.",
        "problem": "Static lists rot; governance needs 'all tables matching X' continuously.",
        "components": [
            {"name": "Rule builder", "detail": "Conditions on name patterns, tags, sensitivity, domain, column names."},
            {"name": "Catalog sets", "detail": "Saved dynamic membership; preview count."},
            {"name": "Actions", "detail": "Apply tag, assign steward, attach policy, enqueue review."},
            {"name": "Scheduling", "detail": "Nightly re-eval or on-change triggers."},
        ],
        "stories": ["As governance, I auto-tag tables with PII columns.", "As a steward, I preview set before applying policy."],
        "use_cases": ["All tables with 'ssn' in column name → retention policy + compliance tag."],
        "ui": "Rule wizard; preview table; execution history.",
        "api": "Rule CRUD; evaluate endpoint; execution logs.",
        "nfr": "Evaluation cost caps; circuit breaker if count explodes.",
        "acceptance": ["Preview count matches bulk job affected rows within tolerance.", "Rule cannot escalate privileges."],
        "deps": "Tags, policies, profiling optional.",
        "open": ["Human approval gate for destructive actions?"],
        "related": [],
    },
    {
        "num": 28,
        "slug": "ai-chat-assistant",
        "title": "AI Chat Assistant in App",
        "summary": "LLM conversational assistant grounded in catalog metadata for discovery and SQL hints.",
        "problem": "Keyword search fails for vague questions; new users need guided answers.",
        "components": [
            {"name": "Grounding", "detail": "Retrieve relevant assets/terms; cite sources in answers."},
            {"name": "Safety", "detail": "PII redaction, prompt injection defenses, no training on customer data without approval."},
            {"name": "Actions", "detail": "Deep links to assets; optional 'copy SQL' with watermark."},
            {"name": "Governance", "detail": "Feature flags per domain; audit transcripts admin-only."},
        ],
        "stories": ["As an analyst, I ask where revenue is defined and get cited assets.", "As security, I disable assistant for restricted domains."],
        "use_cases": ["Natural language: 'datasets for churn model in DEET'."],
        "ui": "Side panel or dedicated tab; feedback thumbs up/down.",
        "api": "Chat completion endpoint with catalog context injection.",
        "nfr": "Latency targets; fallback when LLM unavailable.",
        "acceptance": ["Assistant refuses uncitable claims.", "RBAC: never cites forbidden assets."],
        "deps": "Search index, LLM vendor contract, legal review.",
        "open": ["On-prem model vs SaaS?", "MVP vs phase 2?"],
        "related": [],
    },
    {
        "num": 29,
        "slug": "data-dictionary-download-upload",
        "title": "Data Dictionary Download & Uploads",
        "summary": "Spreadsheet round-trip for titles, descriptions, custom fields across many assets for stewards and audits.",
        "problem": "Stewards work faster in Excel; audits need frozen extracts.",
        "components": [
            {"name": "Export", "detail": "Scoped export by datasource/domain; column chooser."},
            {"name": "Template stability", "detail": "Versioned headers; FQN stable keys."},
            {"name": "Import validation", "detail": "Type checks, unknown rows, permission checks per row."},
            {"name": "Diff report", "detail": "What would change before commit."},
        ],
        "stories": ["As a steward, I edit 500 descriptions offline and upload.", "As audit, I download dictionary quarterly."],
        "use_cases": ["Acquisition: merge two catalogs via spreadsheet mapping."],
        "ui": "Export/import wizard under toolbar actions.",
        "api": "Same as bulk job with file upload multipart.",
        "nfr": "File size limits; virus scan on upload.",
        "acceptance": ["Round-trip: export → unchanged re-import is no-op.", "Row-level errors downloadable."],
        "deps": "F7 custom fields schema, F26 bulk permissions.",
        "open": ["Excel macro support or CSV only MVP?"],
        "related": [],
    },
    # Features 30–35: OMS/BDC program capabilities (see matrix note); align names to your Google Doc if they differ.
    {
        "num": 30,
        "slug": "oms-bdc-navigation-ia",
        "title": "OMS / BDC Navigation & Information Architecture",
        "summary": "How users enter catalog experiences: integrated contextual catalog vs dedicated Business Data Catalog shell, breadcrumbs, and deep links.",
        "problem": "Two valid mental models—engineers live in OMS; stewards need a named BDC—must coexist without duplicate backends.",
        "components": [
            {"name": "Integrated path", "detail": "BDC chips/strips on existing datasource pages; no new top-level nav item required."},
            {"name": "On-top path", "detail": "Business Data Catalog under Main Pages with sub-nav: Overview, Catalog, Lineage, Glossary, Policies, Requests, Admin."},
            {"name": "Breadcrumbs & back", "detail": "Snowflake drill hides subnav; back returns to BDC home without losing context."},
            {"name": "Deep links", "detail": "URL scheme opens specific asset, tab, and filter state; shareable."},
            {"name": "Hybrid contract", "detail": "Open full technical OMS view from BDC in one click and reverse."},
        ],
        "stories": ["As a steward, I start from BDC Overview KPIs.", "As an engineer, I never leave OMS home but still edit business fields."],
        "use_cases": ["Exec demo: bookmark goes straight to BDC Policies tab filtered to domain."],
        "ui": "See BDC-OMS-integrated-vs-on-top-decision.md evaluation table.",
        "api": "Stable asset URLs across shells.",
        "nfr": "Accessibility: landmarks for nav regions; keyboard order consistent.",
        "acceptance": ["Deep link survives SSO redirect.", "Integrated and on-top show same asset id in URL or resolve equivalently."],
        "deps": "Program decision on primary pattern; single metadata API.",
        "open": ["Default landing for hybrid users?"],
        "related": ["../../business-data-catalog/BDC-OMS-integrated-vs-on-top-decision.md", "../../business-data-catalog/bdc-requirements-map.html (R-06)"],
    },
    {
        "num": 31,
        "slug": "metadata-quality-completeness",
        "title": "Metadata Quality & Completeness Scoring",
        "summary": "Signals for description presence, stewardship coverage, and composite quality score on inventory and dashboards.",
        "problem": "Programs need measurable curation progress beyond subjective reviews.",
        "components": [
            {"name": "Field-level signals", "detail": "Empty description chip; missing owner; missing glossary link for key columns."},
            {"name": "Quality score", "detail": "Weighted formula configurable by governance; color-coded column."},
            {"name": "Rollups", "detail": "Domain and datasource averages on Overview KPIs."},
            {"name": "Facets", "detail": "Filter catalog to low-quality assets for sprint planning."},
        ],
        "stories": ["As a steward lead, I sort by lowest quality in my domain.", "As PMO, I track average score weekly."],
        "use_cases": ["OKR: raise average quality score from 42 to 70 by Q4."],
        "ui": "Quality column on tables; optional sparkline on Overview.",
        "api": "GET score breakdown per asset for transparency.",
        "nfr": "Recompute incremental on metadata change.",
        "acceptance": ["Score formula versioned and displayed in UI help.", "Changing weight recalculates within SLA."],
        "deps": "Custom fields, owners, glossary mappings.",
        "open": ["Who configures formula globally?"],
        "related": ["../../business-data-catalog/bdc-requirements-map.html (R-07)"],
    },
    {
        "num": 32,
        "slug": "catalog-metadata-rest-apis",
        "title": "Catalog & Metadata REST APIs (Developer Surface)",
        "summary": "Documented REST shape for assets, search, export hooks, and PATCH semantics used by UI and automation.",
        "problem": "Undocumented stubs block parallel UI/engineering work.",
        "components": [
            {"name": "Resource model", "detail": "Assets, domains, tags, terms, policies with stable ids."},
            {"name": "PATCH semantics", "detail": "Partial updates, ETags, optimistic concurrency."},
            {"name": "Error contract", "detail": "Problem+json or consistent error envelope."},
            {"name": "Developer docs", "detail": "Examples for curl, Postman collection, changelog."},
        ],
        "stories": ["As a frontend dev, I mock against published OpenAPI.", "As integrator, I rotate PAT without downtime."],
        "use_cases": ["UI drawer calls PATCH /catalog/assets/{id} for inline edit."],
        "ui": "N/A server-side; optional API explorer page.",
        "api": "Core deliverable—mirror prototype references in requirements map.",
        "nfr": "Backward compatible minor versions.",
        "acceptance": ["OpenAPI published in CI artifact.", "Breaking changes require major version bump."],
        "deps": "Auth gateway, audit middleware.",
        "open": ["GraphQL read layer?"],
        "related": ["../../business-data-catalog/bdc-requirements-map.html (R-08)"],
    },
    {
        "num": 33,
        "slug": "cross-source-oms-home-drilldown",
        "title": "Cross-Source OMS Home & Asset Drill-Down",
        "summary": "Home experience grouping sources (tables, pipelines, streams) with consistent drill patterns: full page vs drawer per source maturity.",
        "problem": "Users lose context switching between Snowflake-heavy and lighter integrations.",
        "components": [
            {"name": "Home cards", "detail": "Counts per category; health indicators."},
            {"name": "Snowflake drill", "detail": "Table list with BDC strip → full-page detail tabs."},
            {"name": "Unity / others", "detail": "List + drawer pattern until parity."},
            {"name": "Generic fallback", "detail": "Short list → detail for immature connectors."},
        ],
        "stories": ["As a user, I land OMS Home and pick Snowflake in two clicks.", "As BDC user, BDC Home tab mirrors card grid inside catalog area."],
        "use_cases": ["Compare asset counts across Snowflake and Unity for migration."],
        "ui": "Per R-09 prototype copy in requirements map.",
        "api": "Aggregated counts endpoint for home.",
        "nfr": "Home loads from cache if metadata warehouse slow.",
        "acceptance": ["Each datasource tile shows last sync time.", "Drill preserves filter query params where applicable."],
        "deps": "Connectors, F30 navigation decisions.",
        "open": ["Parity timeline for drawer vs full page?"],
        "related": ["../../business-data-catalog/bdc-requirements-map.html (R-09)"],
    },
    {
        "num": 34,
        "slug": "in-catalog-sql-query-sample",
        "title": "In-Catalog SQL Exploration, Query History & Sample Content",
        "summary": "Optional SQL workspace on asset: editor, run history, column vs sample toggle, pending-change highlighting for business fields.",
        "problem": "Users jump to warehouse consoles losing catalog context.",
        "components": [
            {"name": "SQL editor", "detail": "Syntax highlight; limits on rows/cost; role-checked warehouse creds."},
            {"name": "Query history", "detail": "Previous runs on this asset with timestamp and user."},
            {"name": "Columns & sample", "detail": "Toggle between schema grid and masked sample rows."},
            {"name": "Change highlighting", "detail": "Pending business edits in light red until saved."},
            {"name": "Provenance", "detail": "Show where sample data came from (env, policy)."},
        ],
        "stories": ["As an analyst, I validate a column without leaving catalog.", "As governance, I enforce masked samples only."],
        "use_cases": ["Analyst runs SELECT COUNT(*) FROM mart before requesting access."],
        "ui": "Queries tab + SQL tab per integrated prototype; on-top may deep link to OMS for full SQL.",
        "api": "Proxy query execution service; audit all runs.",
        "nfr": "Cost guardrails; query timeout; no PII in logs.",
        "acceptance": ["Unauthorized warehouse role cannot run.", "Sample respects row-level security if enabled."],
        "deps": "Warehouse compute, SSO to warehouse, F20 RBAC.",
        "open": ["MVP: read-only vs full run?", "On-top: always deep link vs embed?"],
        "related": ["../../business-data-catalog/bdc-requirements-map.html (R-10)"],
    },
    {
        "num": 35,
        "slug": "stewardship-requests-admin",
        "title": "Stewardship Requests, Approvals & Admin Operations",
        "summary": "Queues for access and metadata change requests; admin for connectors, sync, roles, import/export catalog actions.",
        "problem": "Email-based access and stewardship approvals do not scale; admins need one place for catalog ops.",
        "components": [
            {"name": "Requests queue", "detail": "Intake, assignee, SLA, approve/deny with reason, link to asset."},
            {"name": "Access vs metadata requests", "detail": "Separate templates and approver pools if needed."},
            {"name": "Admin tab", "detail": "Connectors, sync triggers, role assignment, feature flags."},
            {"name": "Toolbar actions", "detail": "Import tags, export catalog CSV in integrated pattern."},
        ],
        "stories": ["As a user, I request description update from asset page.", "As domain admin, I approve batch tag change requests."],
        "use_cases": ["Access request routes to table owner and data platform if external share."],
        "ui": "Requests tab in on-top BDC; notifications on state change.",
        "api": "Ticket CRUD; webhook to ITSM optional.",
        "nfr": "SLA metrics for time-to-first-response.",
        "acceptance": ["Request always references asset version at submission.", "Denial requires reason visible to requester."],
        "deps": "Identity, email/Slack notify, F9 ownership.",
        "open": ["Integrate with ServiceNow / Jira?"],
        "related": ["../../business-data-catalog/bdc-requirements-map.html (R-05)"],
    },
]


def render_feature(f: dict) -> str:
    num = f["num"]
    slug = f["slug"]
    title = f["title"]
    lines: list[str] = []
    lines.append(f"# PRD — Feature {num}: {title}")
    lines.append("")
    lines.append("## Document control")
    lines.append(f"- **Feature ID:** {num}")
    lines.append(f"- **Slug / file:** `F{num:02d}-{slug}.md`")
    lines.append("- **Source matrix (workspace):** [Feature Inventory Matrix](../1-Feature-Inventory-Matrix.md)")
    lines.append("- **Google Doc matrix (authoritative if different):** [Feature matrix (requires access)](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit)")
    lines.append("- **Note:** Features 30–35 in the workspace matrix are OMS/BDC-specific capabilities derived from `business-data-catalog/bdc-requirements-map.html`. **Rename or split rows** to match your Google Doc if numbering diverges.")
    lines.append("")
    if f.get("related"):
        lines.append("## Related workspace artifacts")
        for r in f["related"]:
            lines.append(f"- `{r}`")
        lines.append("")
    lines.append("## 1. Summary")
    lines.append(f"{f['summary']}")
    lines.append("")
    lines.append("## 2. Problem statement")
    lines.append(f"{f['problem']}")
    lines.append("")
    lines.append("## 3. Goals & non-goals")
    lines.append("### Goals")
    lines.append("- Deliver the outcomes described in user stories and acceptance criteria below.")
    lines.append("- Stay compatible with OMS as system of record for technical metadata unless explicitly scoped otherwise.")
    lines.append("")
    lines.append("### Non-goals (unless pulled into scope by program)")
    lines.append("- Re-implement full warehouse observability or BI server admin outside catalog boundaries.")
    lines.append("")
    lines.append("## 4. Users & primary personas")
    lines.append("| Persona | Why they care |")
    lines.append("|---------|----------------|")
    lines.append("| Data Steward / Owner | Maintain accurate metadata and policies.")
    lines.append("| Data Analyst / BI | Find and trust data for reporting.")
    lines.append("| Data Engineer | Lineage, technical context, automation hooks.")
    lines.append("| Governance / Compliance | Risk reduction, attestations, exports.")
    lines.append("| Platform Admin | Connectors, access, operational health.")
    lines.append("")
    lines.append("## 5. Functional requirements (decomposed)")
    for i, c in enumerate(f["components"], 1):
        lines.append(f"### 5.{i} {c['name']}")
        lines.append(c["detail"])
        lines.append("")
    lines.append("## 6. User stories")
    for s in f["stories"]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append("## 7. Use cases & examples")
    for u in f["use_cases"]:
        lines.append(f"- {u}")
    lines.append("")
    lines.append("## 8. UX & UI notes")
    lines.append(f["ui"])
    lines.append("")
    lines.append("## 9. Data model & API considerations")
    lines.append(f["api"])
    lines.append("")
    lines.append("## 10. Non-functional requirements")
    lines.append(f["nfr"])
    lines.append("")
    lines.append("## 11. Acceptance criteria (testable)")
    for a in f["acceptance"]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append("## 12. Dependencies")
    lines.append(f["deps"])
    lines.append("")
    lines.append("## 13. Risks & mitigations")
    lines.append("| Risk | Mitigation |")
    lines.append("|------|------------|")
    lines.append("| Scope creep across integrated vs on-top shells | Time-box MVP per persona; shared API contract |")
    lines.append("| Metadata drift from sources | Connector SLAs, visible sync timestamps |")
    lines.append("| RBAC gaps exposing sensitive names | Security review on search snippets and exports |")
    lines.append("")
    lines.append("## 14. Open questions")
    for o in f["open"]:
        lines.append(f"- {o}")
    lines.append("")
    lines.append("---")
    lines.append("*Generated structure — edit in place for program specifics. Regenerator: `python3 generate_prds.py`*")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    index_rows: list[tuple[int, str, str, str]] = []
    for f in FEATURES:
        body = render_feature(f)
        out = ROOT / f"F{f['num']:02d}-{f['slug']}.md"
        out.write_text(body, encoding="utf-8")
        index_rows.append((f["num"], f["title"], f"F{f['num']:02d}-{f['slug']}.md", f["slug"]))
    manifest = {"features": [{"num": n, "title": t, "file": fn, "slug": s} for n, t, fn, s in index_rows]}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {len(FEATURES)} PRDs to {ROOT}")


if __name__ == "__main__":
    main()
