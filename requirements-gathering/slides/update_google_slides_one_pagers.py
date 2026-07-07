#!/usr/bin/env python3
"""Update Google Slides one-pager deck: slide 1 (Navigator), 2 (Kronos), 3 (DGP)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

PRESENTATION_ID = "1dNApXdE49ad8SKi2YckP2eSV0FmyxW7QBOpaLGBDEps"
TOKEN_PATH = Path.home() / "Library/Application Support/All Google MCP/token.json"

# Slide 1 — Data Navigator
NAVIGATOR = {
    "sidebar": "g3dbc968f750_0_1",
    "title": "g3dbc968f750_0_3",
    "okrs_body": "g3dbc968f750_0_4",
    "footer_links": "g3dbc968f750_0_6",
    "timing_body": "g3dbc968f750_0_8",
    "team_line": "g3dbc968f750_0_19",
}

# Slide 2 — Kronos (object ids from presentation)
KRONOS = {
    "sidebar": "g3e570df2494_0_9",
    "title": "g3e570df2494_0_10",
    "okrs_body": "g3e570df2494_0_11",
    "footer_links": "g3e570df2494_0_13",
    "timing_body": "g3e570df2494_0_15",
    "team_line": "g3e570df2494_0_18",
}

# Slide 3 — Data Governance Portal
DGP = {
    "sidebar": "g3e570df2494_0_23",
    "title": "g3e570df2494_0_24",
    "okrs_body": "g3e570df2494_0_25",
    "footer_links": "g3e570df2494_0_27",
    "timing_body": "g3e570df2494_0_29",
    "team_line": "g3e570df2494_0_32",
}

VT = "\u000b"

NAVIGATOR_SIDEBAR = (
    "What\n"
    "Data Navigator is the governed discovery experience on OMS—the new home for business metadata, "
    "glossary, and metric definitions where ~531 Alation users search, browse, and trust assets after migration. "
    "Navigator is the UX layer, not the metadata engine: automated capture and AI-enriched definitions are "
    "produced by Data 626 / MCI and OMS; Navigator is where that work surfaces.\n"
    f"Why{VT}"
    "Alation is a passive catalog that drifts from production and cannot carry us past contract renewal. "
    "We need an in-house surface on OMS that preserves discovery workflows, migrates Alation content, and "
    "composes trusted metadata for the right personas—without duplicating scrapers in this L3.\n"
    "Stakeholders: "
    "Business & DNA consumers and analysts (primary); stewards and privacy/compliance (secondary); OMS; "
    "Data 626 / MCI (metadata supply); DNA / Metrics Council; enterprise design; metadata working group."
    f"{VT}{VT}"
    "Top Things to Know\n"
    "Boundary: Navigator ≠ scrapers, collectors, or MCP/agentic access—those sit in MCI, Data 626, OMS backend.\n"
    "MVP: Search/discovery, glossary, browse, descriptions/metadata, APIs to migrate Alation.\n"
    "Adjacent: Governance Portal is phase 2 / tangential—not in this L3 scope.\n"
    "Renewal: Alation renewal likely Aug/Sep 2026; target Sep 2027 cutover (dev ~Mar 2027).\n"
    "\n\n"
)

NAVIGATOR_OKRS = (
    "Ship MVP UX on OMS — search, browse, glossary, gold/provenance, classifications read, migration APIs."
    f"{VT}\n"
    "Persona-first validation — business/DNA consumer stories with stewards, privacy, and DNA."
    f"{VT}\n"
    "Enterprise design engagement — IA with Dave Hoffman / enterprise design before locking UI."
    f"{VT}\n"
    "Migration readiness — gap matrix vs. Alation; plan supporting Aug 2026 renewal and Sep 2027 cutover."
    f"{VT}\n"
    "Adoption: active users / time-to-answer vs. Alation baseline (~531 users).\n"
    "\n\n"
)

NAVIGATOR_TIMING = (
    "[2026] Intake, requirements, exploratory wireframes, metadata working group; Alation renewal planning."
    f"{VT}\n"
    "[Mar 2027] Dev complete target; begin user migration window."
    f"{VT}\n"
    "[Sep 2027] Target cutover aligned to renewal window."
    f"{VT}\n"
    "Phase 2: Governance Portal hub; MCP/agentic via MCI / Data 626—not Navigator MVP.\n"
    "\n\n"
)

NAVIGATOR_TEAM = (
    "Program Lead: Jon Fong\n"
    "Intake: Data Platforms Intake (Bi-weekly)\n"
    "Key Partners: OMS, Data 626 / MCI, data governance, DNA / Metrics Council\n"
)

KRONOS_SIDEBAR = (
    "What\n"
    "Kronos is the program to establish a single system of record for data-related assets—"
    "vendors, digital trackers, internal systems, and business use cases—with lifecycle discipline "
    "(register, attest, review, deboard). The UI POC demonstrates discovery, relationships, exports, "
    "and legal-exception tracking on a governed inventory store.\n"
    f"Why{VT}"
    "Tracker and vendor sprawl outpaces spreadsheet inventories. Privacy, DSAR, remediation, and RIM "
    "programs all need the same asset register. Without it, teams cannot answer "
    "“what collects guest data and who owns it?” until after an incident or audit fire drill.\n"
    "Stakeholders: "
    "Privacy & legal; marketing & product (trackers/SDKs); security & GIS (vendor risk); "
    "engineering & platform (systems registry); records management; data governance stewards; "
    "leadership sponsors for inventory coverage and remediation prioritization."
    f"{VT}{VT}"
    "Top Things to Know\n"
    "Today: Disney Streaming inventories live in Excel and tribal knowledge; Kronos UI POC uses "
    "imported baseline data (vendors, trackers, systems, use cases).\n"
    "Scope: Supply-side inventory—not a catalog replacement; feeds tracker remediation, vendor DPAs, "
    "and Governance Portal RIM views.\n"
    "Registration: Net-new assets via JIRA / intake until self-service registration is production-ready.\n"
    "\n\n"
)

KRONOS_OKRS = (
    "Inventory coverage — % of in-scope vendors, trackers, and systems with owner, risk tier, "
    "and lifecycle status."
    f"{VT}\n"
    "Attestation freshness — % of assets reviewed within the agreed cadence; overdue count trending down."
    f"{VT}\n"
    "Remediation linkage — % of open tracker findings mapped to a registered inventory asset."
    f"{VT}\n"
    "Deboarding discipline — Time from deprecation decision to inventory update and tool removal."
    f"{VT}\n"
    "Self-service discovery — Reduction in ad hoc “what trackers/vendors do we use?” requests to "
    "governance teams.\n"
    "\n\n"
)

KRONOS_TIMING = (
    "[Now] Baseline import from legacy Excel; Kronos UI POC validation with privacy & stewards."
    f"{VT}\n"
    "[Near-term] Governed store (PostgreSQL / Snowflake); registration intake workflow; "
    "legal exceptions module."
    f"{VT}\n"
    "[Scale] Connectors (tag manager, contracts, CMDB); attestation cadences; API for downstream tools."
    f"{VT}\n"
    "[Enterprise] Expand taxonomy and federated ownership beyond initial segment; integrate with "
    "Governance Portal queues.\n"
    "\n\n"
)

KRONOS_TEAM = (
    "Program: Sustainable Inventory Management\n"
    "Program Lead: Jon Fong\n"
    "Key Partners: Privacy, Legal, GIS, Marketing ops, Records (RIM), Data Governance\n"
)

DGP_SIDEBAR = (
    "What\n"
    "The Governance Portal is the privacy and data governance command center in the shared OMS shell—"
    "one front door for posture, exceptions, and evidence across guest and consumer data. "
    "One portal for privacy, platform, security, and regulatory posture, organized by four dimensions: "
    "Privacy, Platform, Security, and Regulatory.\n"
    f"Why{VT}"
    "Each workstream already has its own dashboard; stakeholders cannot see overall posture or prioritize "
    "across dimensions. Leadership asked for a single unified experience (Abacus-inspired) without "
    "rebuilding every backend—unified experience, federated execution.\n"
    "Stakeholders: "
    "Privacy, legal, compliance, and GIS teams; data stewards and DPMs; executives and program leads; "
    "internal audit; business and analytics consumers (indirect—faster resolution of governance blockers "
    "on datasets they use)."
    f"{VT}{VT}"
    "Top Things to Know\n"
    "Portal vs Navigator: Portal = posture, triage, evidence; Navigator = catalog discovery and steward "
    "execution (Data Sources, Catalog, Requests, Workflows).\n"
    "Dimension IA: Privacy (Consent, DSRs, Tracker) · Platform (Stewards → Navigator, Classifications, "
    "Policies) · Security (Access, GIS, Data Use) · Regulatory (Laws, Incidents, Audits).\n"
    "Phase: Governance hub is phase 2 alongside Navigator MVP for catalog migration (Alation exit Oct 1, 2026).\n"
    "Not in scope: Replacing DSR, consent, tracker, or downstream RIM consoles—deep links and per-function "
    "work queues instead.\n"
    "\n\n"
)

DGP_OKRS = (
    "Privacy Compliance Index — Top-line PCI plus Platform, Security, and Regulatory section indices "
    "trended with target thresholds."
    f"{VT}\n"
    "Exception SLA — % of work-queue items closed within SLA; breaches by dimension "
    "(Privacy, Platform, Security, Regulatory)."
    f"{VT}\n"
    "Portal adoption — Weekly active users among privacy, legal, compliance, and stewardship roles."
    f"{VT}\n"
    "Handoff completion — % of Portal-routed items actioned in Navigator or downstream tools on time."
    f"{VT}\n"
    "Evidence readiness — Time to produce audit / regulatory evidence package from Portal export.\n"
    "\n\n"
)

DGP_TIMING = (
    "[Now] UDGE demo: Privacy / Platform / Security / Regulatory IA, Governance Overview "
    "(PCI + section indices), work queues, auditor view & evidence export."
    f"{VT}\n"
    "[Phase 2 start] Stakeholder sign-off on containers/format; live KPI feeds from dimension workstreams."
    f"{VT}\n"
    "[With catalog migration] Defined-vs-observed on OMS assets; Navigator Requests handoffs wired."
    f"{VT}\n"
    "[Scale] Evidence automation, role-based defaults, enterprise segment expansion.\n"
    "\n\n"
)

DGP_TEAM = (
    "Program: Unified Data Governance Experience (UDGE)\n"
    "Program Lead: Jon Fong\n"
    "Key Partners: Privacy, Legal, GIS, Compliance, OMS, Business Data Navigator, Kronos RIM\n"
)


def load_credentials() -> Credentials:
    data = json.loads(TOKEN_PATH.read_text())
    creds = Credentials(
        token=data.get("token"),
        refresh_token=data.get("refresh_token"),
        token_uri=data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=data.get("client_id"),
        client_secret=data.get("client_secret"),
        scopes=data.get("scopes"),
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        data["token"] = creds.token
        if creds.expiry:
            data["expiry"] = creds.expiry.isoformat() + "Z"
        TOKEN_PATH.write_text(json.dumps(data, indent=2))
    return creds


def replace_shape_text(object_id: str, new_text: str) -> list[dict]:
    return [
        {
            "deleteText": {
                "objectId": object_id,
                "textRange": {"type": "ALL"},
            }
        },
        {
            "insertText": {
                "objectId": object_id,
                "insertionIndex": 0,
                "text": new_text,
            }
        },
    ]


def bold_range(object_id: str, start: int, end: int) -> dict:
    return {
        "updateTextStyle": {
            "objectId": object_id,
            "textRange": {"type": "FIXED_RANGE", "startIndex": start, "endIndex": end},
            "style": {"bold": True},
            "fields": "bold",
        }
    }


def apply_sidebar_bold(object_id: str, text: str) -> list[dict]:
    """Match Navigator slide: bold section labels."""
    reqs: list[dict] = []
    labels = ["What", "Why", "Stakeholders: ", "Top Things to Know"]
    for label in labels:
        idx = text.find(label)
        if idx >= 0:
            reqs.append(bold_range(object_id, idx, idx + len(label)))
    # Bold list lead-ins after Top Things
    for lead in ("Today:", "Scope:", "Registration:", "Portal vs Navigator:", "Dimension IA:", "Phase:", "Not in scope:", "Boundary:", "MVP:", "Adjacent:", "Renewal:"):
        idx = text.find(lead)
        if idx >= 0:
            reqs.append(bold_range(object_id, idx, idx + len(lead)))
    return reqs


def main() -> int:
    creds = load_credentials()
    service = build("slides", "v1", credentials=creds)
    requests: list[dict] = []

    # --- Slide 1: Data Navigator ---
    requests.extend(replace_shape_text(NAVIGATOR["title"], "Data Navigator \n"))
    requests.extend(replace_shape_text(NAVIGATOR["sidebar"], NAVIGATOR_SIDEBAR))
    requests.extend(apply_sidebar_bold(NAVIGATOR["sidebar"], NAVIGATOR_SIDEBAR))
    requests.extend(replace_shape_text(NAVIGATOR["okrs_body"], NAVIGATOR_OKRS))
    requests.extend(replace_shape_text(NAVIGATOR["timing_body"], NAVIGATOR_TIMING))
    requests.extend(replace_shape_text(NAVIGATOR["footer_links"], "Product brief | 28 May intake report\n"))
    requests.extend(replace_shape_text(NAVIGATOR["team_line"], NAVIGATOR_TEAM))

    # --- Slide 2: Kronos ---
    requests.extend(replace_shape_text(KRONOS["title"], "Kronos \n"))
    requests.extend(replace_shape_text(KRONOS["sidebar"], KRONOS_SIDEBAR))
    requests.extend(apply_sidebar_bold(KRONOS["sidebar"], KRONOS_SIDEBAR))
    requests.extend(replace_shape_text(KRONOS["okrs_body"], KRONOS_OKRS))
    requests.extend(replace_shape_text(KRONOS["timing_body"], KRONOS_TIMING))
    requests.extend(replace_shape_text(KRONOS["footer_links"], "Value deck | Kronos UI POC\n"))
    requests.extend(replace_shape_text(KRONOS["team_line"], KRONOS_TEAM))

    # --- Slide 3: Data Governance Portal ---
    requests.extend(replace_shape_text(DGP["title"], "Data Governance Portal \n"))
    requests.extend(replace_shape_text(DGP["sidebar"], DGP_SIDEBAR))
    requests.extend(apply_sidebar_bold(DGP["sidebar"], DGP_SIDEBAR))
    requests.extend(replace_shape_text(DGP["okrs_body"], DGP_OKRS))
    requests.extend(replace_shape_text(DGP["timing_body"], DGP_TIMING))
    requests.extend(replace_shape_text(DGP["footer_links"], "Value deck | Portal demo\n"))
    requests.extend(replace_shape_text(DGP["team_line"], DGP_TEAM))

    service.presentations().batchUpdate(
        presentationId=PRESENTATION_ID,
        body={"requests": requests},
    ).execute()

    print("Updated slides 1 (Navigator), 2 (Kronos), and 3 (Data Governance Portal).")
    print(f"https://docs.google.com/presentation/d/{PRESENTATION_ID}/edit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
