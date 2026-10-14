#!/usr/bin/env python3
"""Rewrite PRD sections 6.3, 7–9, 12–16 from bullets to flowing paragraphs."""
from __future__ import annotations

from pathlib import Path

from docx import Document

SOURCE = Path(__file__).resolve().parent / "PRD-Navigator-Data-Governance-Portal.source.docx"

REPLACEMENTS: dict[str, list[str]] = {
    "6.3 Shared shell elements": [
        "All products in the Navigator umbrella share a common shell so users experience one program rather than disconnected applications. The top bar carries the product breadcrumb, global search, role context, and primary actions such as Evidence export and Auditor view. The left rail supports either a mode switch between major surfaces (v1) or governance-first dimension navigation (v2), depending on the IA option in use.",
        "The main panel hosts Governance Overview, dimension hubs, work queues, or specialist handoffs as the user moves through the program. Deep links tie the story together: a Portal exception can route to a Business Data Catalog asset detail, and from there to Open in OMS when engineers need full technical context on the same object.",
    ],
    "7.1 Governance Overview": [
        "Governance Overview is the default landing for privacy, compliance, and executive personas. It displays the Privacy Compliance Index (PCI) as a hero metric with trend and status badge, alongside Platform, Security, and Regulatory section indices that drill down into their dimension hubs. Open exceptions appear by severity and dimension so leaders can see what needs attention without opening four separate tools. Where live feeds exist, trend charts support time-range selection so posture can be read in context rather than as a single snapshot.",
    ],
    "7.2 Dimension hubs & work queues": [
        "Each dimension exposes an Overview tab with KPI cards and trend charts, and a Work queue tab with actionable items. Queue items carry title, severity, SLA state, assignee or owner, a linked asset or policy reference, and a handoff action into the appropriate downstream system. A unified queue model supports cross-dimension filtering, with dimension-specific views available as presets. Handoffs open MAUI, the consent platform, Access Manager, Navigator Requests, Kronos, or other specialist tools with context preserved where APIs allow. Closed and resolved items remain in the audit trail with timestamps.",
    ],
    "7.3 Privacy dimension": [
        "The Privacy dimension surfaces consent-management posture KPIs and routes exceptions through the work queue. It shows DSR and guest data request volume, SLA compliance, and breach highlighting, and maintains a tracker remediation queue with severity and remediation status. The Portal deep-links to MAUI and other privacy operational tools rather than embedding replacement UIs in Phase 2.",
    ],
    "7.4 Platform dimension": [
        "Platform is the bridge between program operations and catalog stewardship. It reports stewardship coverage and steward assignment gaps, hosts a Classifications Management UI where stewards review, approve, or reject AI-suggested classifications and link outcomes to catalog assets, and provides policies management with control mappings tied to classifications and assets. Stewards enter Business Data Catalog from Platform for discovery and metadata curation. Defined vs observed views sit side by side so policy and classification intent can be compared to OMS-observed state on assets.",
    ],
    "7.5 Security dimension": [
        "The Security dimension makes access and compliance work visible in one place. It shows access review status and overdue attestation queue items, GIS compliance posture with exception routing, and a data-use approval intake queue that hands off to approval workflow systems. Over time, visibility into access and classification alignment will deepen through phased Access Manager integration.",
    ],
    "7.6 Regulatory dimension": [
        "Regulatory covers laws and regulations with applicability and control-mapping summaries, regulatory incident tracking on Overview and in the queue, and audit readiness indicators with audit-cycle queue items. Business inventory is not duplicated here: Regulatory provides a deep link to Kronos (https://dcf.corp.dig.com/vista/kronos/) rather than an embedded inventory UI.",
    ],
    "7.7 Evidence & auditor view": [
        "Evidence export packages posture metrics, open exceptions, and policy mappings for a selected scope and time range. Auditor view offers a read-only Portal mode that hides mutating actions and is optimized for attestation walkthroughs. Export supports PDF and/or structured download (CSV/JSON) per audit program requirements. Phase 3 adds scheduled evidence packages and automated refresh tied to catalog asset IDs.",
    ],
    "7.8 Search & global navigation": [
        "Global search spans governance objects—policies, classifications, queue items—and catalog assets where the user is entitled. Results respect RBAC and route to the appropriate Portal workflow or Business Data Catalog asset detail. Breadcrumbs follow a dimension → function → detail hierarchy so users always know where they are in the program.",
    ],
    "8. User stories": [
        "Privacy officers land on Governance Overview, see PCI and open Privacy queue items, and know what needs action this week. From a DSR SLA breach in the queue they hand off to MAUI with case context preserved. Data stewards review pending classifications in Platform, approve or reject with rationale, and open the linked catalog asset in Business Data Catalog without losing program context.",
        "Governance program leads export an evidence package for an internal audit without assembling spreadsheets from five tools. Executives view Platform, Security, and Regulatory section indices on Overview and drill into exceptions by severity. Access managers see overdue access attestations in the Security queue and route to Access Manager for completion. Auditors use read-only auditor view to walk posture metrics and exception history for a defined scope. Records owners follow Regulatory → Inventory to Kronos for business inventory maintenance.",
    ],
    "9. UI / UX requirements": [
        "The Portal follows enterprise-style patterns with enterprise design review where applicable. Layout is container-first: dimension hub structure and KPI containers should be validated with leadership before final metric definitions are locked. Core flows target WCAG-oriented accessibility (exact tier set by program). The experience is desktop-first for program operators; read-only auditor view is acceptable on tablet.",
        "Empty states should explain when live feeds are not yet connected, distinguishing Phase 1 prototypes from Phase 2 live data. When KPIs are federated from downstream systems, stale data indicators show the last successful sync timestamp. Destructive actions—rejecting a classification, closing an exception—require confirmation and audit logging. Prototype references include data-navigator-governance/index.html (UDGE demo) and navigator-version-2/index.html (v2 shell).",
    ],
    "12. Success criteria": [
        "Success is measured by posture, adoption, and operational follow-through—not feature count alone. PCI and Platform, Security, and Regulatory section indices should trend month over month against target thresholds. Exception SLA performance—percent of work-queue items closed within SLA and breach counts by dimension—shows whether triage is working. Portal adoption among privacy, legal, compliance, and stewardship roles (weekly active users) and handoff completion (percent of Portal-routed items actioned in downstream tools within agreed windows) demonstrate that the Portal is the front door, not another dashboard.",
        "Evidence readiness is the time to produce an audit or regulatory evidence package from Portal export. Navigation coherence means stewards can move Platform → Classifications → Business Data Catalog asset without dead links. Stakeholder satisfaction—privacy council feedback on a single unified experience versus prior dashboard sprawl—closes the loop on whether the program story lands.",
    ],
    "13. Non-functional requirements": [
        "Security relies on SSO via the corporate IdP, RBAC on every read and write, and a read-only auditor role. Classification and policy mutations and queue disposition changes are logged append-only for audit. Performance targets for Governance Overview (P95 load) remain TBD with the program; work queues must paginate for large backlogs. When a downstream KPI feed is unavailable, the UI degrades gracefully—showing stale state with timestamp rather than silent failure. Public views use aggregate KPIs only, not individual user activity in leaderboards. Availability aligns with the enterprise governance program SLA (target TBD with SISU/ops).",
    ],
    "14. Dependencies & risks": [
        "Delivery depends on Gov App backend and PULS schema stability, downstream privacy and access system APIs for KPI feeds, OMS catalog asset IDs for defined vs observed and deep links to Business Data Catalog, and enterprise design review plus privacy/legal sign-off on Overview metrics.",
        "Key risks include launching with demo-grade data (mitigate by labeling beta until live feeds are verified), scope creep that absorbs Business Data Catalog or specialist tools (mitigate with RACI and the architecture diagram), collision with Foundations/OMS UI scope (escalate via metadata working group when Navigator and Foundations overlap), and undefined incident/problem management integration (track with platform partners if Portal proceeds).",
    ],
    "15. Open questions": [
        "Several design and program questions remain open. Architecture must confirm whether OMS reads the governance repository directly from Postgres or exclusively via Gov App API. Phasing needs clarity on which KPI feeds are available for Phase 2 GA versus deferred to Phase 3. The PCI formula and section index weightings require privacy council approval path. Navigation IA must decide v1 two-tab versus v2 governance-first for the combined Business Data Catalog and Portal shell at GA. Incident management integration scope with enterprise problem management is undefined. Entitlement model work is needed to define which queue items are visible to which IdP groups per dimension.",
    ],
    "16. References": [
        ("para", "Supporting artifacts in the program workspace:"),
        ("bullet", "v2 shell prototype: navigator-version-2/index.html"),
        ("bullet", "Original demo wireframes: data-navigator-governance/index.html"),
        ("bullet", "Architecture Q&A memo: requirements-gathering/slides/Data-Gov-Portal-Architecture-QA-Memo.docx"),
        ("bullet", "Value deck: requirements-gathering/slides/data-governance-portal-value-deck-3-slides.html"),
        ("bullet", "Navigator umbrella PRD: requirements-gathering/prd/word/PRD-Navigator-Data-Governance-Umbrella.docx"),
        ("bullet", "Architecture diagram: data-navigator-governance/governance-product-systems-architecture-lucidchart-import.md"),
        ("bullet", "OMS alignment deck: requirements-gathering/slides/navigator-oms-alignment-deck-3-slides.html"),
        ("bullet", "Intake report: requirements-gathering/meetings/data-platforms-intake-2026-05-28-navigator-report.md"),
    ],
}

SECTION_7_INTRO = (
    "Functional requirements describe what the Portal must do across Overview, dimension hubs, "
    "queues, evidence, and navigation. Each subsection below maps to a major surface in the "
    "UDGE demo and Phase 2 delivery scope."
)


def heading_level(paragraph) -> int:
    name = paragraph.style.name if paragraph.style else ""
    if name == "Heading 1":
        return 1
    if name == "Heading 2":
        return 2
    if name == "Heading 3":
        return 3
    return 0


def is_bullet(paragraph) -> bool:
    name = paragraph.style.name if paragraph.style else ""
    return name in {"List Bullet", "List Number"}


def apply(doc: Document) -> None:
    for heading_text in reversed(list(REPLACEMENTS.keys())):
        start_idx = end_idx = None
        paras = doc.paragraphs
        for i, p in enumerate(paras):
            if p.text.strip() != heading_text:
                continue
            start_idx = i
            start_lvl = heading_level(p)
            end_idx = len(paras)
            for j in range(i + 1, len(paras)):
                lvl = heading_level(paras[j])
                if lvl and lvl <= start_lvl:
                    end_idx = j
                    break
            break
        if start_idx is None:
            continue

        paras = doc.paragraphs
        for i in range(end_idx - 1, start_idx, -1):
            p = paras[i]
            if is_bullet(p) or not p.text.strip():
                p._element.getparent().remove(p._element)

        anchor = next(p for p in doc.paragraphs if p.text.strip() == heading_text)
        insert_after = anchor._element
        items = REPLACEMENTS[heading_text]
        for item in items:
            if isinstance(item, tuple):
                kind, text = item
            else:
                kind, text = "para", item
            if kind == "bullet":
                new_p = doc.add_paragraph(text, style="List Bullet")
            else:
                new_p = doc.add_paragraph(text)
                new_p.style = doc.styles["Normal"]
            insert_after.addnext(new_p._element)
            insert_after = new_p._element

    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() != "7. Functional requirements":
            continue
        nxt = doc.paragraphs[i + 1] if i + 1 < len(doc.paragraphs) else None
        if nxt and heading_level(nxt) == 2:
            intro = doc.add_paragraph(SECTION_7_INTRO)
            intro.style = doc.styles["Normal"]
            p._element.addnext(intro._element)
        break


def main() -> None:
    doc = Document(SOURCE)
    apply(doc)
    doc.save(SOURCE)
    print(f"Updated paragraph style in {SOURCE}")


if __name__ == "__main__":
    main()
