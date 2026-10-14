#!/usr/bin/env python3
"""Rebuild BDC L4 grouping Google Doc with formatted epic tables."""

from __future__ import annotations

import json
import time
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

DOC_ID = "1Ieo7MGCoDrU3FLyzPoEdBtm8f3B2ms5mLTWiZyP2jeM"
TOKEN_PATH = Path.home() / "Library/Application Support/All Google MCP/token.json"
JIRA_BASE = "https://deept.atlassian.net/browse/"

L4_SECTIONS = [
    {
        "title": "L4-0 — Navigator Phase 1: Requirements & Discovery (ALREADY RUNNING)",
        "purpose": "Lock scope, PRDs, and epic boundaries before build L4s commit.",
        "why": None,
        "success": [
            "Requirements signed off",
            "MVP vs stretch scope documented",
            "Epics mapped to L4 deliverables",
        ],
        "epics": [
            ("DSDPTGROGU-14322", "Data Navigator Phase 1 Discovery", "In Progress"),
        ],
    },
    {
        "title": "L4-1 — BDC Platform & Integration Foundation",
        "purpose": "OMS-backed platform spine — nothing else ships without this.",
        "why": "Shared infra, ingestion, API contract, and RBAC are one platform commitment — not separate user-facing outcomes.",
        "success": None,
        "epics": [
            ("DSDPTGROGU-14528", "BDC - Architecture & Infrastructure", "Open"),
            ("DSDPTGROGU-14527", "BDC Data Connectors & Ingestion", "Open"),
            ("DSDPTGROGU-14506", "BDC - APIs - expose service APIs & MCP", "Open"),
            ("DSDPTGROGU-14489", "BDC - MVP Role Based Access for Data Stewards, etc.", "Open"),
        ],
    },
    {
        "title": "L4-2 — BDC Discovery & Browse Experience (MVP CORE)",
        "purpose": "Alation-exit consumer journey — find, navigate, and understand assets.",
        "why": "Shell + browse + search + lineage = the primary “I found the data” experience (MVP parity).",
        "success": None,
        "epics": [
            ("DSDPTGROGU-14487", "BDC Initial User Facing UI Implementation", "Open"),
            ("DSDPTGROGU-14493", "BDC - Catalog Browse Data Sources by Hierarchy", "Open"),
            ("DSDPTGROGU-14502", "BDC Search and Discovery", "Open"),
            ("DSDPTGROGU-14505", "BDC - Data Lineage Visualization - enhance what is in OMS", "Open"),
        ],
    },
    {
        "title": "L4-3 — BDC Governance Metadata & Alation Content Migration (MVP CORE)",
        "purpose": "Steward workflows + business metadata parity + Alation content move.",
        "why": "Glossary, dictionary, tags, flags, and AI-assisted descriptions = make data trustworthy and governed. Biggest Alation parity risk if buried in a monolithic L4.",
        "success": None,
        "epics": [
            ("DSDPTGROGU-14490", "BDC Glossary Migration from Alation", "Open"),
            ("DSDPTGROGU-14491", "BDC - Data Dictionary - technical reference document for how data is structured", "Open"),
            ("DSDPTGROGU-14504", "BDC - Flags (Endorsements, Warnings, Deprecations, Popularity)", "Open"),
            ("DSDPTGROGU-14508", "BDC - Data Tagging & Classification", "Open"),
            ("DSDPTGROGU-14488", "BDC - Automated Description Generation", "Open"),
        ],
    },
    {
        "title": "L4-4 — BDC Admin & Adoption Analytics",
        "purpose": "Admin/ops persona + measurable adoption for Alation exit.",
        "why": "Admin dashboard + usage telemetry = prove migration success to leadership. Feeds adoption metrics into L4-6.",
        "success": None,
        "epics": [
            ("DSDPTGROGU-14494", "BDC Admin UI", "Open"),
            ("DSDPTGROGU-14492", "BDC - Usage and system metrics", "Open"),
        ],
    },
    {
        "title": "L4-5 — BDC Advanced Capabilities (STRETCH / PRE–PHASE 2)",
        "purpose": "Valuable but not blocking Alation MVP parity.",
        "why": "Matches “Beyond MVP” scope (AI chat, governance workflows). Keeps L4-2/L4-3 clean for Oct 2026 parity.",
        "success": None,
        "epics": [
            ("DSDPTGROGU-14507", "BDC - Workflows", "Open"),
            ("DSDPTGROGU-14509", "BDC - AI Chat Feature", "Open"),
        ],
    },
    {
        "title": "L4-6 — Phase 2 Adoption, Training & Migration (EXISTING)",
        "purpose": "User adoption, training, and migration to the Internal Solution after Phase 1 build is ready.",
        "why": "Converts Phase 1 delivery into sustained adoption and Alation exit execution. Already tracked as DEEDATA-17108 (cloned from DEEDATA-17107).",
        "success": [
            "Training materials and enablement paths published",
            "Migration runbook executed with stakeholder sign-off",
            "Adoption targets met for Alation exit personas",
        ],
        "epics": [
            (
                "DEEDATA-17108",
                "Phase 2) User adoption training & Migration to the Internal Solution",
                "Open",
            ),
        ],
    },
]

QUICK_REF_ROWS = [
    ("L4-0 Discovery", "DSDPTGROGU-14322"),
    ("L4-1 Platform", "DSDPTGROGU-14528, DSDPTGROGU-14527, DSDPTGROGU-14506, DSDPTGROGU-14489"),
    ("L4-2 Discovery & Browse (MVP)", "DSDPTGROGU-14487, DSDPTGROGU-14493, DSDPTGROGU-14502, DSDPTGROGU-14505"),
    ("L4-3 Governance & Migration (MVP)", "DSDPTGROGU-14490, DSDPTGROGU-14491, DSDPTGROGU-14504, DSDPTGROGU-14508, DSDPTGROGU-14488"),
    ("L4-4 Admin & Analytics", "DSDPTGROGU-14494, DSDPTGROGU-14492"),
    ("L4-5 Advanced", "DSDPTGROGU-14507, DSDPTGROGU-14509"),
    ("L4-6 Phase 2 Adoption & Migration", "DEEDATA-17108"),
]

TITLE_ROWS = [
    ("L4-0", "Phase 1a) Navigator requirements & discovery"),
    ("L4-1", "Phase 1b) BDC platform & OMS integration foundation"),
    ("L4-2", "Phase 1c) BDC discovery & browse experience (MVP)"),
    ("L4-3", "Phase 1d) BDC governance metadata & Alation content migration (MVP)"),
    ("L4-4", "Phase 1e) BDC admin & adoption analytics"),
    ("L4-5", "Phase 1f) BDC advanced capabilities (workflows & AI chat)"),
    ("L4-6", "Phase 2) User adoption, training & migration to the Internal Solution"),
]


def batch_update(service, requests: list[dict], retries: int = 5) -> None:
    if not requests:
        return
    for attempt in range(retries):
        try:
            service.documents().batchUpdate(
                documentId=DOC_ID, body={"requests": requests}
            ).execute()
            return
        except HttpError as exc:
            if exc.resp.status == 429 and attempt < retries - 1:
                time.sleep(65)
                continue
            raise


def get_service():
    data = json.loads(TOKEN_PATH.read_text())
    creds = Credentials(
        token=data.get("token"),
        refresh_token=data.get("refresh_token"),
        token_uri=data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=data.get("client_id"),
        client_secret=data.get("client_secret"),
        scopes=data.get("scopes"),
    )
    return build("docs", "v1", credentials=creds, cache_discovery=False)


def clear_document(service) -> None:
    doc = service.documents().get(documentId=DOC_ID).execute()
    end_index = doc["body"]["content"][-1]["endIndex"]
    if end_index > 2:
        batch_update(
            service,
            [
                {
                    "deleteContentRange": {
                        "range": {"startIndex": 1, "endIndex": end_index - 1}
                    }
                }
            ],
        )


def find_last_table(doc: dict) -> tuple[dict, int]:
    last_table = None
    last_start = 0
    for element in doc["body"]["content"]:
        if "table" in element:
            last_table = element["table"]
            last_start = element["startIndex"]
    if not last_table:
        raise RuntimeError("No table found in document")
    return last_table, last_start


def populate_table(service, table_start_index: int, headers: list[str], rows: list[list[str]]) -> None:
    data = [headers] + rows
    batch_update(
        service,
        [
            {
                "insertTable": {
                    "rows": len(data),
                    "columns": len(headers),
                    "location": {"index": table_start_index},
                }
            }
        ],
    )

    doc = service.documents().get(documentId=DOC_ID).execute()
    table, _table_start = find_last_table(doc)

    text_requests = []
    for r, row in enumerate(data):
        for c, value in enumerate(row):
            cell = table["tableRows"][r]["tableCells"][c]
            cell_start = cell["content"][0]["startIndex"]
            text_requests.append(
                {"insertText": {"location": {"index": cell_start}, "text": value}}
            )
    batch_update(service, list(reversed(text_requests)))

    doc = service.documents().get(documentId=DOC_ID).execute()
    table, _table_start = find_last_table(doc)

    style_requests = []
    header_row = table["tableRows"][0]
    for cell in header_row["tableCells"]:
        start = cell["content"][0]["startIndex"]
        end = cell["content"][0]["endIndex"]
        style_requests.append(
            {
                "updateTextStyle": {
                    "range": {"startIndex": start, "endIndex": max(start, end - 1)},
                    "textStyle": {"bold": True},
                    "fields": "bold",
                }
            }
        )

    if len(headers) >= 1:
        for r in range(1, len(data)):
            cell = table["tableRows"][r]["tableCells"][0]
            start = cell["content"][0]["startIndex"]
            key = data[r][0]
            if key.startswith("DSDPTGROGU-") or key.startswith("DEEDATA-"):
                style_requests.append(
                    {
                        "updateTextStyle": {
                            "range": {"startIndex": start, "endIndex": start + len(key)},
                            "textStyle": {
                                "link": {"url": f"{JIRA_BASE}{key}"},
                                "foregroundColor": {
                                    "color": {
                                        "rgbColor": {
                                            "red": 0.09,
                                            "green": 0.33,
                                            "blue": 0.85,
                                        }
                                    }
                                },
                                "underline": True,
                            },
                            "fields": "link,foregroundColor,underline",
                        }
                    }
                )

    batch_update(service, style_requests)


def insert_text(service, index: int, text: str) -> int:
    batch_update(
        service,
        [{"insertText": {"location": {"index": index}, "text": text}}],
    )
    return index + len(text)


def apply_heading(service, start: int, end: int, level: str = "HEADING_2") -> None:
    batch_update(
        service,
        [
            {
                "updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": {"namedStyleType": level},
                    "fields": "namedStyleType",
                }
            }
        ],
    )


def build_document(service) -> None:
    index = 1

    title_start = index
    index = insert_text(
        service,
        index,
        "BDC Phase 1 — L4 Deliverable Grouping\n"
        "Source: DEEDATA-17107 (Phase 1) under L3 DEEDATA-17106 (Data Navigator)\n"
        "Prepared: September 18, 2026\n\n",
    )
    apply_heading(service, title_start, title_start + len("BDC Phase 1 — L4 Deliverable Grouping"), "HEADING_1")

    overview_start = index
    index = insert_text(
        service,
        index,
        "Overview\n\n"
        "DEEDATA-17107 is currently a single L4 Delivery carrying 18 Grogu epics. "
        "This document splits it into L4-0 through L4-5 (Phase 1 build) plus L4-6 (Phase 2 adoption & migration).\n\n"
        "Alignment:\n"
        "• 626 supplies metadata · OMS stores/serves · BDC is the governed business experience\n"
        "• MVP vs Beyond MVP Alation parity scope\n"
        "• Consumer vs steward vs admin personas\n\n",
    )
    apply_heading(service, overview_start, overview_start + len("Overview"), "HEADING_2")

    rec_start = index
    index = insert_text(service, index, "Recommended L4 Structure\n\n")
    apply_heading(service, rec_start, rec_start + len("Recommended L4 Structure"), "HEADING_2")

    for section in L4_SECTIONS:
        heading_start = index
        index = insert_text(service, index, f"{section['title']}\n")
        apply_heading(service, heading_start, heading_start + len(section["title"]), "HEADING_3")

        index = insert_text(service, index, f"Purpose: {section['purpose']}\n\n")

        table_start = index
        rows = [[key, summary, status] for key, summary, status in section["epics"]]
        populate_table(service, table_start, ["Epic", "Summary", "Status"], rows)

        doc = service.documents().get(documentId=DOC_ID).execute()
        index = doc["body"]["content"][-1]["endIndex"] - 1
        index = insert_text(service, index, "\n")

        if section.get("why"):
            index = insert_text(service, index, f"Why together: {section['why']}\n\n")

        if section.get("success"):
            index = insert_text(service, index, "Success criteria:\n")
            for item in section["success"]:
                index = insert_text(service, index, f"• {item}\n")
            index = insert_text(service, index, "\n")

    hierarchy_start = index
    index = insert_text(
        service,
        index,
        "Hierarchy Map\n\n"
        "L3  DEEDATA-17106  Data Navigator\n"
        "├── L4-0  Discovery & requirements          (DSDPTGROGU-14322)     ← in progress\n"
        "├── L4-1  Platform & integration foundation (4 epics)\n"
        "├── L4-2  Discovery & browse experience     (4 epics)               ← MVP\n"
        "├── L4-3  Governance metadata & migration   (5 epics)               ← MVP\n"
        "├── L4-4  Admin & adoption analytics        (2 epics)\n"
        "├── L4-5  Advanced capabilities             (2 epics)               ← stretch\n"
        "└── L4-6  DEEDATA-17108  Phase 2 adoption, training & migration   ← already exists\n\n"
        "Note: Retire or repurpose DEEDATA-17107 as the umbrella on DEEDATA-17106, "
        "or convert it into L4-0 (Discovery).\n\n",
    )
    apply_heading(service, hierarchy_start, hierarchy_start + len("Hierarchy Map"), "HEADING_2")

    alt_start = index
    index = insert_text(
        service,
        index,
        "Simpler 4-L4 Option\n\n"
        "Merge L4-4 + L4-5 into one deliverable: "
        "“BDC Operations, Analytics & Enhancement” — Admin UI, usage metrics, workflows, AI chat (4 epics).\n"
        "Keep L4-1, L4-2, L4-3 as-is. L4-6 (DEEDATA-17108) stays separate as Phase 2. "
        "Discovery stays separate or folds into L3 planning.\n\n",
    )
    apply_heading(service, alt_start, alt_start + len("Simpler 4-L4 Option"), "HEADING_2")

    titles_start = index
    index = insert_text(service, index, "Suggested L4 Titles\n\n")
    apply_heading(service, titles_start, titles_start + len("Suggested L4 Titles"), "HEADING_2")
    table_start = index
    populate_table(
        service,
        table_start,
        ["L4", "Proposed title"],
        [[l4, title] for l4, title in TITLE_ROWS],
    )
    doc = service.documents().get(documentId=DOC_ID).execute()
    index = doc["body"]["content"][-1]["endIndex"] - 1
    index = insert_text(service, index, "\n")

    dep_start = index
    index = insert_text(
        service,
        index,
        "Dependency Order\n\n"
        "1. L4-0 (Discovery) → gates scope on all others\n"
        "2. L4-1 (Platform) → blocks L4-2, L4-3, L4-4\n"
        "3. L4-2 + L4-3 in parallel (consumer vs steward tracks)\n"
        "4. L4-4 after L4-1 (needs data flowing)\n"
        "5. L4-5 last — or fold into Phase 2 if capacity is tight\n"
        "6. L4-6 (DEEDATA-17108) after Phase 1 MVP paths are ready — adoption, training & migration\n\n",
    )
    apply_heading(service, dep_start, dep_start + len("Dependency Order"), "HEADING_2")

    jira_start = index
    index = insert_text(
        service,
        index,
        "Jira Mechanics\n\n"
        "For each new L4 Delivery under DEEDATA-17106:\n"
        "1. Create Delivery issue (same type as DEEDATA-17107)\n"
        "2. Issue split link from L4 → its Grogu epics\n"
        "3. Remove those epics from DEEDATA-17107 split links\n"
        "4. Tag epics: l4-platform, l4-discovery, l4-governance, l4-admin, l4-advanced\n"
        "5. L4-6 already exists as DEEDATA-17108 — no new Delivery ticket needed\n\n",
    )
    apply_heading(service, jira_start, jira_start + len("Jira Mechanics"), "HEADING_2")

    ref_start = index
    index = insert_text(service, index, "Epic-to-L4 Quick Reference\n\n")
    apply_heading(service, ref_start, ref_start + len("Epic-to-L4 Quick Reference"), "HEADING_2")
    table_start = index
    populate_table(
        service,
        table_start,
        ["L4 Deliverable", "Epics"],
        [[l4, epics] for l4, epics in QUICK_REF_ROWS],
    )
    doc = service.documents().get(documentId=DOC_ID).execute()
    index = doc["body"]["content"][-1]["endIndex"] - 1
    index = insert_text(
        service,
        index,
        "\nLinks\n"
        "• L3 Initiative: https://deept.atlassian.net/browse/DEEDATA-17106\n"
        "• Current L4 (to split): https://deept.atlassian.net/browse/DEEDATA-17107\n"
        "• L4-6 Phase 2 (existing): https://deept.atlassian.net/browse/DEEDATA-17108\n",
    )


def main() -> None:
    service = get_service()
    clear_document(service)
    build_document(service)
    print(f"Updated https://docs.google.com/document/d/{DOC_ID}/edit")


if __name__ == "__main__":
    main()
