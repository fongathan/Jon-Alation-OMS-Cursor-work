"""Shared OKR wording: generic block (for replace) and feature-specific key results by F-code."""

from __future__ import annotations

# Exact text appended by append_okr_sections.py (must match live Docs for replace).
GENERIC_KR_BLOCK = (
    "Key results (standard for success in the first pilot / GA window):\n"
    "1. Outcome: Meets the acceptance criteria in this PRD with documented UAT sign-off from "
    "Data Governance and at least one pilot domain (DEEPT-aligned).\n"
    "2. Adoption: ≥70% of invited pilot users report the feature as valuable for weekly catalog work "
    "(short survey), and volume of support requests attributable to this area stays within the agreed SLO vs. pre-launch baseline.\n"
    "3. Trust & operations: Telemetry, audit trails, and access controls behave as specified; "
    "no open Sev-1 / launch-blocking defects at the migration gate.\n"
)


def key_results_body(fcode: str) -> str:
    """Return the 'Key results:' header plus three numbered KRs tailored to the feature."""
    krs = _KEY_RESULTS_BY_FCODE[fcode]
    return (
        "Key results (standard for success in the first pilot / GA window):\n"
        f"1. Outcome: {krs[0]}\n"
        f"2. Adoption: {krs[1]}\n"
        f"3. Trust & operations: {krs[2]}\n"
    )


def okr_body(fcode: str, title: str, job: str) -> str:
    """Full OKR section body (objective + tailored key results)."""
    return (
        f"Objective: Deliver {title} as a production-ready capability that clearly advances "
        f"the Alation-to-OMS migration so teams can {job}.\n\n"
        + key_results_body(fcode)
    )


# Each tuple: (outcome KR, adoption KR, trust/ops KR) — written for that feature.
_KEY_RESULTS_BY_FCODE: dict[str, tuple[str, str, str]] = {
    "F01": (
        "Search relevance, ranking, and filters meet this PRD’s acceptance tests—including "
        "synonyms, faceted filters, and permission-aware results—with UAT sign-off from Data Governance "
        "and at least one pilot domain.",
        "Pilot users achieve target time-to-trusted-asset (median vs. baseline) on scripted discovery tasks; "
        "≥70% rate search as valuable weekly, and search-related support tickets stay within the agreed SLO.",
        "Query/click telemetry, retention, and RBAC on indexed metadata match the spec; no Sev-1 defects "
        "on performance, leakage of unauthorized assets, or logging of sensitive query text.",
    ),
    "F02": (
        "Glossary term CRUD, approval workflows, and published definitions meet PRD criteria with "
        "steward UAT and Data Governance sign-off (including conflict handling and deprecation).",
        "Pilot domains adopt canonical terms for agreed subject areas; ≥70% of glossary editors report "
        "weekly value, and glossary-related clarification requests trend down vs. baseline.",
        "Change history, ownership, and export/report hooks behave as specified; audit evidence is available "
        "for definition changes; no launch-blocking defects on access or lineage links from terms.",
    ),
    "F03": (
        "Hierarchy browse, breadcrumbs, and empty/stale states meet acceptance criteria with UAT from "
        "Data Governance and a pilot domain representing complex source trees.",
        "Target completion rate for “browse to a known folder/source” tasks improves vs. baseline; "
        "≥70% of pilot users use browse weekly and rate it valuable; browse-related support within SLO.",
        "Navigation state respects permissions; sync/staleness indicators accurate; no Sev-1 issues on "
        "incorrect exposure of restricted nodes or broken deep links.",
    ),
    "F04": (
        "Asset detail surfaces required fields, lineage previews, policies, and stewardship actions per "
        "this PRD, with UAT sign-off from Data Governance and a pilot domain on representative assets.",
        "Consumers complete “understand before query” checks (sample scenarios) without escalations; "
        "≥70% rate detail pages valuable weekly; detail-page confusion tickets stay within SLO.",
        "Field-level permissions, PII handling, and audit views for edits/comments meet spec; no Sev-1 "
        "defects on wrong metadata, broken policy badges, or missing stewardship attribution.",
    ),
    "F05": (
        "Column/table/job-level lineage accuracy and impact summaries meet PRD thresholds with UAT on "
        "golden-path assets and sign-off from Data Governance + a pilot data engineering team.",
        "Impact-analysis tasks (e.g., upstream change blast radius) complete within target time; "
        "≥70% of pilot engineers rate lineage valuable weekly; lineage-correctness disputes within SLO.",
        "Lineage ingestion jobs, freshness SLAs, and access rules for sensitive jobs match spec; "
        "no Sev-1 issues on false dependencies, missing critical hops, or unauthorized pipeline detail.",
    ),
    "F06": (
        "Tag application, controlled vocabularies, and bulk tagging flows meet acceptance tests with "
        "UAT from Data Governance (taxonomy) and a pilot domain (compliance tagging scenarios).",
        "Tag coverage on in-scope assets reaches agreed targets; ≥70% of stewards rate tagging workflows "
        "valuable weekly; mis-triage or “wrong tag” support volume stays within SLO.",
        "Tag policies, inheritance rules, and audit trails for tag changes behave as specified; "
        "no Sev-1 defects on policy bypass, silent removals, or inconsistent classification in exports/APIs.",
    ),
    "F07": (
        "Custom field types, validation, and display on assets meet PRD criteria with UAT covering "
        "required/optional fields and steward workflows; Data Governance + pilot domain sign-off.",
        "Agreed pilot domains publish domain-specific fields within validation error budgets defined in this PRD; "
        "≥70% of metadata editors report weekly value; custom-field support tickets within SLO.",
        "Field-level RBAC, change history, and API exposure of custom fields match spec; no Sev-1 on "
        "data loss, unauthorized edits, or schema drift vs. documented contracts.",
    ),
    "F09": (
        "Ownership models, steward badges, escalation paths, and RACI displays meet acceptance criteria "
        "with UAT from Data Governance and pilot domain stewards on contested assets.",
        "Time-to-owner for new in-scope assets meets target; ≥70% of consumers find ownership trustworthy; "
        "“who owns this?” tickets trend down and stay within SLO.",
        "Delegation, succession, and audit logs for ownership changes behave as specified; no Sev-1 on "
        "orphaned accountability, incorrect stewards on regulated assets, or missing approval trails.",
    ),
    "F10": (
        "Aggregated usage and access signals (no inappropriate individual surveillance) meet PRD thresholds "
        "with privacy/security UAT and Data Governance sign-off on definitions and rollups.",
        "Dashboards answer agreed operational questions for pilot leadership; ≥70% of pilot analytics users "
        "rate signals valuable weekly; misuse or misinterpretation support stays within SLO.",
        "Aggregation windows, suppression rules, and retention for metrics match spec; no Sev-1 on "
        "re-identification risk, wrong aggregates on governed assets, or broken export controls.",
    ),
    "F11": (
        "Connector coverage, sync schedules, error surfacing, and metadata depth meet PRD acceptance for "
        "in-scope systems, with UAT from platform owners and Data Governance on sync contracts.",
        "Freshness and completeness KPIs hit targets for pilot sources; ≥70% of admins rate connectors "
        "reliable weekly; connector/sync failure tickets within agreed SLO.",
        "Credentials vaulting, least-privilege scopes, and job logs behave as specified; no Sev-1 on "
        "credential leaks, silent sync skips, or over-broad extraction from sources.",
    ),
    "F12": (
        "Policy attachment, inheritance, enforcement points in catalog UX, and exception workflows meet "
        "PRD tests with legal/compliance + Data Governance UAT on representative policies.",
        "Pilot domains can demonstrate policy coverage on in-scope assets; ≥70% of stewards rate Policy "
        "Center valuable weekly; policy misapplication support within SLO.",
        "Evidence packs (what policy, where enforced, who changed it) and RBAC on policy admin match "
        "spec; no Sev-1 on false “compliant” signals or policies hidden from authorized reviewers.",
    ),
    "F13": (
        "Compilation jobs, rule packs, and quality signals on assets meet PRD accuracy/latency targets "
        "with UAT from Data Governance and pilot stewards on agreed quality dimensions.",
        "Consumers act on quality badges in discovery tasks with fewer false positives vs. baseline; "
        "≥70% of pilot users rate signals trustworthy weekly; quality-rule support within SLO.",
        "Job telemetry, rule versioning, and access to underlying checks match spec; no Sev-1 on "
        "misleading green badges, missing failures, or unauthorized visibility into sensitive checks.",
    ),
    "F14": (
        "Public/catalog APIs and integration patterns meet versioning, rate limits, and functional "
        "acceptance in this PRD, with UAT from a pilot downstream team and Data Governance on scopes.",
        "Successful integrations complete onboarding scenarios without escalations; ≥70% of API consumers "
        "rate stability/docs valuable weekly; integration break-fix tickets within SLO.",
        "AuthN/Z for tokens, audit logs of mutating calls, and deprecation policy behave as specified; "
        "no Sev-1 on broken auth, silent data corruption via API, or undocumented breaking changes in-window.",
    ),
    "F15": (
        "Version history, diff/compare, and restore flows meet PRD criteria with UAT from Data Governance "
        "and pilot stewards, including conflict resolution and who-can-restore rules.",
        "Restore drills succeed on agreed scenarios within target time; ≥70% of editors rate versioning "
        "valuable weekly; “wrong restore” or lost-history incidents stay within SLO (ideally zero Sev-1).",
        "Immutability guarantees, retention, and audit trails for versions match spec; no Sev-1 on "
        "history gaps, unauthorized restores, or tampering with prior snapshots.",
    ),
    "F16": (
        "Recommendation types (e.g., similar assets, missing fields, stewards) meet precision/recall "
        "targets in this PRD with UAT from Data Governance and pilot stewards on golden sets.",
        "Stewards accept/reject recommendations at expected rates with net metadata quality lift; "
        "≥70% rate suggestions valuable weekly; bad-recommendation noise tickets within SLO.",
        "Model/feature flags, logging, and guardrails (no unsafe automation) behave as specified; "
        "no Sev-1 on mass incorrect writes, policy-violating suggestions, or opaque automation.",
    ),
    "F17": (
        "Saved query/favorite CRUD, sharing, and permission models meet acceptance tests with UAT from "
        "Data Governance and pilot analysts on shared vs. private lists.",
        "Repeat discovery tasks show reduced time vs. baseline using favorites; ≥70% of frequent users "
        "report weekly value; broken-link or permission-denied favorites support within SLO.",
        "Access inheritance, rename/delete audit, and export of saved definitions match spec; "
        "no Sev-1 on leaking private lists, stale results without warning, or orphaned shares.",
    ),
    "F18": (
        "Threaded comments, @mentions, resolution states, and notifications meet PRD criteria with UAT "
        "from Data Governance and pilot collaboration on regulated assets.",
        "Time-to-resolution for open questions improves vs. baseline; ≥70% of active collaborators rate "
        "Q&A valuable weekly; duplicate-thread or notification-fatigue tickets within SLO.",
        "Moderation, retention, PII handling in comments, and audit exports behave as specified; "
        "no Sev-1 on hidden edits, unauthorized deletion of audit trail, or spam/PII leakage paths.",
    ),
    "F19": (
        "Export formats, filters, schedules, and row-level security in reports meet PRD acceptance with "
        "UAT from audit stakeholders and Data Governance on sensitive catalogs.",
        "Scheduled exports run reliably for pilot jobs; ≥70% of report consumers rate outputs trustworthy "
        "weekly; export failure or “wrong extract” tickets within SLO.",
        "Encryption, signed URLs or equivalent, lineage of exported fields, and access logs match spec; "
        "no Sev-1 on over-broad extracts, missing redactions, or broken entitlement checks.",
    ),
    "F20": (
        "SSO flows, session handling, group/role mapping, and catalog RBAC alignment meet PRD security "
        "tests with InfoSec + Data Governance UAT on joiner/mover/leaver scenarios.",
        "Access-denied/incorrect-access incidents meet zero Sev-1 and trend toward SLO for pilot; "
        "≥70% of admins rate identity integration reliable weekly.",
        "Token lifetimes, MFA compatibility (if required), forced logout, and audit of privilege changes "
        "behave as specified; no Sev-1 on privilege escalation, stale group grants, or broken SCIM edges.",
    ),
    "F21": (
        "Flag types (endorsement, warning, deprecation, popularity) render consistently in discovery "
        "and detail contexts per PRD, with UAT from Data Governance and pilot stewards on edge cases.",
        "Consumers correctly interpret trust signals in test scenarios; ≥70% rate flags valuable weekly; "
        "confusion or “ignored warning” incidents tracked and within SLO.",
        "Attribution, expiry, revocation, and audit for flags match spec; no Sev-1 on forged endorsements, "
        "missing critical warnings on regulated assets, or popularity metrics that re-identify users.",
    ),
    "F22": (
        "Domain scoping for discovery, policies, and stewardship meets PRD acceptance with UAT from "
        "multiple pilot domains and Data Governance on cross-domain edge cases.",
        "Cross-domain leakage tests pass; ≥70% of domain leads rate scoping valuable weekly; "
        "mis-scoped asset tickets within SLO.",
        "Domain admin roles, inheritance, and migration of assets between domains behave as specified; "
        "no Sev-1 on policy bypass via domain switches or incorrect default domain assignment.",
    ),
    "F23": (
        "Folder trees, drag/drop or equivalent ordering, permissions on folders, and deep links meet "
        "PRD criteria with UAT from pilot teams with large navigational taxonomies.",
        "Navigation efficiency targets met on scripted tasks; ≥70% of pilot users rate foldering valuable "
        "weekly; broken-navigation or lost-asset support within SLO.",
        "Permission propagation, recycle/restore, and audit of structural changes match spec; "
        "no Sev-1 on exposure through mis-inherited folder ACLs or silent moves breaking lineage.",
    ),
    "F24": (
        "Dataflow/job documentation, linking to tables/pipelines, and freshness of job metadata meet "
        "PRD acceptance with UAT from pilot data engineering and Data Governance.",
        "Impact questions (“what breaks if this job fails?”) answerable within target time; "
        "≥70% of engineers rate dataflows valuable weekly; job-metadata correction tickets within SLO.",
        "Secrets handling in job metadata, access to logs, and scheduler integration behave as specified; "
        "no Sev-1 on missing critical jobs, incorrect lineage to production tables, or credential exposure.",
    ),
    "F25": (
        "Admin dashboards for health, adoption, and investigations meet metric definitions in this PRD "
        "with UAT from platform admins and Data Governance on official KPIs.",
        "Admins complete top investigation workflows within target time; ≥70% rate dashboards valuable "
        "weekly; dashboard wrong-number or trust disputes within SLO.",
        "Role-based access to admin metrics, drill-down limits, and data retention for admin views match "
        "spec; no Sev-1 on exposing PII, cross-tenant leakage, or tamperable metrics.",
    ),
    "F26": (
        "Bulk selection, preview/diff, validation, and job progress for mass edits meet PRD acceptance "
        "with UAT from Data Governance and pilot stewards on large-change scenarios.",
        "Bulk edit jobs complete within performance targets with rollback success on failure; "
        "≥70% of stewards rate bulk edit valuable weekly; mass-edit incident tickets within SLO.",
        "Atomicity guarantees, per-record audit, and entitlement checks on bulk operations match spec; "
        "no Sev-1 on partial writes without notice, unauthorized bulk scope, or audit gaps.",
    ),
    "F27": (
        "Catalog Sets / rules engine (conditions, actions, dry-run, scheduling) meets acceptance tests "
        "with UAT from Data Governance and pilot stewards on representative rules.",
        "Automated tagging/ownership updates reduce manual work vs. baseline with agreed error rates; "
        "≥70% of rule authors rate the engine valuable weekly; rule-debug support within SLO.",
        "Rule versioning, simulation vs. production, and kill switches behave as specified; "
        "no Sev-1 on runaway rules, cross-domain side effects, or unaudited mass changes.",
    ),
    "F28": (
        "Assistant answers are grounded in approved catalog sources, refuse out-of-scope how-tos, and "
        "meet safety/accuracy bars in this PRD with UAT from Data Governance + pilot users.",
        "Task success on scripted catalog Q&A improves vs. baseline; ≥70% rate the assistant valuable "
        "weekly; unsafe or hallucinated-answer reports within SLO with agreed triage.",
        "Prompt/response logging, redaction, rate limits, and RBAC on retrieved context match spec; "
        "no Sev-1 on policy violations, leakage of restricted metadata, or missing citations where required.",
    ),
    "F29": (
        "Template download, bulk upload validation, error reports, and partial-apply behavior meet PRD "
        "acceptance with UAT from Data Governance and pilot stewards on large dictionaries.",
        "Round-trip edits succeed on golden files within blocking-error budgets defined in this PRD; ≥70% of bulk "
        "editors rate the flow valuable weekly; upload-parse support tickets within SLO.",
        "Checksums, row-level error logs, and who-ran-which-upload audit behave as specified; "
        "no Sev-1 on silent data loss, applying changes to wrong assets, or bypassing validation.",
    ),
    "F30": (
        "New/expanded source types ingest per connector PRD with schema coverage and sync SLAs; UAT with "
        "owning platform teams and Data Governance on data contracts.",
        "Pilot sources hit freshness/completeness KPIs; ≥70% of source owners rate expanded coverage "
        "valuable weekly; new-source break-fix volume within SLO.",
        "Credential isolation, network egress controls, and per-source RBAC match spec; "
        "no Sev-1 on pulling unauthorized schemas, PII overspill, or connector privilege escalation.",
    ),
    "F31": (
        "Details icon / contextual help surfaces correct copy and links for the surface in focus, per "
        "PRD, with UAT from UX + Data Governance on accuracy of governance messaging.",
        "Help interactions reduce “how do I…?” tickets for targeted flows vs. baseline; ≥70% of pilot "
        "users rate in-context help valuable weekly; wrong-help reports within SLO.",
        "Content versioning, locale/access rules, and telemetry (no sensitive content in logs) match "
        "spec; no Sev-1 on misleading guidance on regulated actions or broken escalation links.",
    ),
    "F32": (
        "Persona-based default filters, saved persona views, and admin management of personas meet PRD "
        "acceptance with UAT from pilot roles (analyst, engineer, steward) and Data Governance.",
        "Role-appropriate landing experiences improve task success vs. one-size baseline; "
        "≥70% of pilot users rate persona filtering valuable weekly; “wrong persona” confusion within SLO.",
        "Persona entitlements cannot escalate access; audit of persona changes and impersonation rules "
        "(if any) match spec; no Sev-1 on seeing assets outside effective RBAC via persona bugs.",
    ),
    "F33": (
        "Product pages aggregate metrics, stewards, linked assets, and curated narrative per PRD with "
        "UAT from product owners and Data Governance on canonical product definitions.",
        "Business stakeholders find product truth in one place for pilot products; ≥70% rate product "
        "pages valuable weekly; conflicting-product-metadata tickets trend down within SLO.",
        "Page permissions, embedded metrics freshness, and audit of curated content match spec; "
        "no Sev-1 on stale KPIs presented as current, or unauthorized edits to executive-facing pages.",
    ),
    "F34": (
        "AI “How to” content is grounded in approved corpora, refuses unsafe instructions, and passes "
        "accuracy checks in this PRD with UAT from Data Governance and pilot onboarding cohorts.",
        "New-user onboarding task completion improves vs. baseline; ≥70% rate How-To AI valuable weekly; "
        "unsafe or off-policy guidance reports within SLO with triage to content owners.",
        "Logging, retention, and linkage to Feature 31 entry points behave as specified; "
        "no Sev-1 on training-data leakage paths, PII in transcripts, or bypass of refusal rules.",
    ),
    "F35": (
        "Overview/social surfaces show only aggregate/curated activity (no personal surveillance) per "
        "PRD, with privacy UAT and Data Governance sign-off on definitions and sampling.",
        "Engagement with curated highlights meets pilot targets without spikes in privacy complaints; "
        "≥70% of users rate the section valuable weekly; moderation tickets within SLO.",
        "Suppression, blocking, retention, and abuse-reporting flows match spec; "
        "no Sev-1 on exposing individual behavioral trails, doxxing vectors, or broken opt-outs.",
    ),
}
