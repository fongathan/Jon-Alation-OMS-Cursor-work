#!/usr/bin/env python3
"""Consolidate Navigator FAQs to one bullet per question."""
import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

DOC_ID = "1wP_czgwUmSrE82hKoMIcQDNCpuv99hzyl8pIs-_YY7U"
TOKEN_PATH = Path.home() / "Library/Application Support/All Google MCP/token.json"

QUESTIONS = [
    "What is Navigator?",
    "Who uses this and for what purpose?",
    "How can we make this UI more persona based?",
    "Where does Lineage lie?",
    "Why are we moving off Alation?",
    "What is our goal?",
    "When are we targeting this to be built?",
    "Will our partners using our current Alation instance migrate as well?",
    "Do we want to integrate with other tools?",
]

FAQS = [
    (
        "What is Navigator?",
        [
            "Navigator is the umbrella product for DEEPT data governance — the Data Governance Portal plus programs across Privacy, Platform, Security, and Regulatory (Business Data Catalog, Kronos, OneTrust, DSRs, tracker remediation, classifications, policies, and more). Guided by unified experience and federated execution, 626 supplies metadata, OMS stores and serves it, and Navigator is the governed experience layer for the right persona — not a duplicate metadata store.",
        ],
    ),
    (
        "Who uses this and for what purpose?",
        [
            "DEEPT business and DNA consumers and analysts (find, trust, and use data), stewards (curate and endorse), and privacy, compliance, security, regulatory, and governance leads (attestations, posture, and evidence) are primary users; engineers get technical depth via OMS (Open in OMS) and DRE consumers use API-first access — each persona gets depth where it matters in MVP, not one generic catalog for everyone.",
        ],
    ),
    (
        "How can we make this UI more persona based?",
        [
            "Lock a small persona set (3–5), define one job-to-be-done per persona, and shape IA with role-aware landing pages and by-persona hubs so each surface completes one primary story; MVP goes deep for business discovery, thin for stewards and compliance, with engineers handed off to OMS — then validate navigation with wireframes and A/B tests once greenlit.",
        ],
    ),
    (
        "Where does Lineage lie?",
        [
            "OMS is the system of record for technical lineage (table, column, pipeline); 626 / MCI improves supply at source and Navigator surfaces business-context lineage (provenance, upstream/downstream, impact) on asset pages, with deep graph drill via Open in OMS — one API, two shells: OMS answers how it is built; Navigator answers what it means and whether you can trust it.",
        ],
    ),
    (
        "Why are we moving off Alation?",
        [
            "We can deliver an in-house, business-first metadata experience on OMS with AI-enabled, policy-driven definitions bound to real Disney sources — prioritizing DEEPT jobs over Alation's generic catalog — while avoiding duplicate cost and drift and aligning with the contract exit window.",
        ],
    ),
    (
        "What is our goal?",
        [
            "Serve DEEPT business data users so they can find, learn, navigate, and use the data they need — find, trust, and cite steward-attested metadata on OMS without tribal knowledge — closing the Alation exit with MVP discovery parity on the OMS spine and extending the governance command center in phase 2.",
        ],
    ),
    (
        "When are we targeting this to be built?",
        [
            "May 2027 overall delivery goal, with MVP catalog and discovery targeting Alation exit (~Oct 2026), governance hub in phase 2, and sequencing from persona alignment through ~8–10 months of eng build — dependent on OMS API readiness, 626 supply, and program greenlight.",
        ],
    ),
    (
        "Will our partners using our current Alation instance migrate as well?",
        [
            "Near-term focus is DEEPT data users only; partner teams on the shared Alation instance are out of MVP scope, and any future onboarding would be discussed case by case (federated access, APIs, phased rollout) once DEEPT paths are proven.",
        ],
    ),
    (
        "Do we want to integrate with other tools?",
        [
            "Yes — we are tool-agnostic and integrate via APIs and deep links with OMS as the metadata spine; adjacent tools (OneTrust, Kronos, PULS) stay authoritative for their domains and third-party catalogs can feed or consume via OMS where they add value without duplicating Navigator.",
        ],
    ),
]


def build_body() -> str:
    lines = ["FAQ List", ""]
    for question, answers in FAQS:
        lines.append(question)
        lines.extend(answers)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def paragraph_text(element: dict) -> str:
    return "".join(
        e.get("textRun", {}).get("content", "")
        for e in element.get("paragraph", {}).get("elements", [])
    ).strip()


def main() -> None:
    body = build_body()
    data = json.loads(TOKEN_PATH.read_text())
    creds = Credentials(
        token=data.get("token"),
        refresh_token=data.get("refresh_token"),
        token_uri=data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_secret=data.get("client_secret"),
        client_id=data.get("client_id"),
        scopes=data.get("scopes"),
    )
    service = build("docs", "v1", credentials=creds, cache_discovery=False)

    doc = service.documents().get(documentId=DOC_ID).execute()
    end_index = doc["body"]["content"][-1]["endIndex"]
    requests = [
        {"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end_index - 1}}},
        {"insertText": {"location": {"index": 1}, "text": body}},
    ]
    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()

    doc = service.documents().get(documentId=DOC_ID).execute()
    format_requests = []

    for element in doc["body"]["content"]:
        if "paragraph" not in element:
            continue
        text = paragraph_text(element)
        if not text:
            continue
        start, end = element["startIndex"], element["endIndex"]

        if text == "FAQ List":
            format_requests.append(
                {
                    "updateTextStyle": {
                        "range": {"startIndex": start, "endIndex": end - 1},
                        "textStyle": {"bold": True},
                        "fields": "bold",
                    }
                }
            )
            continue

        if text in QUESTIONS:
            format_requests.extend(
                [
                    {
                        "createParagraphBullets": {
                            "range": {"startIndex": start, "endIndex": end},
                            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                        }
                    },
                    {
                        "updateTextStyle": {
                            "range": {"startIndex": start, "endIndex": end - 1},
                            "textStyle": {"bold": True},
                            "fields": "bold",
                        }
                    },
                ]
            )
            continue

        format_requests.extend(
            [
                {
                    "createParagraphBullets": {
                        "range": {"startIndex": start, "endIndex": end},
                        "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                    }
                },
                {
                    "updateParagraphStyle": {
                        "range": {"startIndex": start, "endIndex": end},
                        "paragraphStyle": {
                            "indentFirstLine": {"magnitude": 54, "unit": "PT"},
                            "indentStart": {"magnitude": 72, "unit": "PT"},
                        },
                        "fields": "indentFirstLine,indentStart",
                    }
                },
            ]
        )

    if format_requests:
        service.documents().batchUpdate(
            documentId=DOC_ID, body={"requests": format_requests}
        ).execute()

    print(f"Updated https://docs.google.com/document/d/{DOC_ID}/edit")


if __name__ == "__main__":
    main()
