#!/usr/bin/env python3
"""Insert Mickey FAQ answers into Navigator FAQs Google Doc."""
import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

DOC_ID = "1wP_czgwUmSrE82hKoMIcQDNCpuv99hzyl8pIs-_YY7U"
TOKEN_PATH = Path.home() / "Library/Application Support/All Google MCP/token.json"

# (insert_index, list of answer bullets) — insert bottom-up so indices stay valid
INSERTIONS = [
    (
        1563,
        [
            "OMS remains the metadata spine for technical inventory and lineage; adjacent tools stay authoritative for their domains (consent in OneTrust, inventory in Kronos, policies in PULS/Gov backend).",
            "Third-party catalog or observability tools can feed or consume metadata via OMS APIs where it adds value without duplicating the governed Navigator experience.",
            "Requirements drive tooling choices — we integrate what DEEPT programs and personas actually need, regardless of vendor.",
        ],
    ),
    (
        1352,
        [
            "Partner teams on the shared Alation instance are out of MVP scope — we are not committing to a big-bang migration for all current Alation consumers.",
            "If partners need catalog capabilities later, we can discuss federated access, API integration, or phased onboarding once DEEPT MVP paths are proven.",
            "Decision factors for any future partner migration: feature parity, persona fit, OMS coverage of their sources, and stakeholder demand.",
        ],
    ),
    (
        1128,
        [
            "Phased delivery: MVP catalog/discovery paths target Alation exit (~Oct 2026); governance hub and deeper pillar workflows follow in phase 2.",
            "Sequencing: persona stories & intake alignment → eng build (~8–10 months for MVP scope) → iterative rollout with stakeholder validation.",
            "Dependencies: OMS API readiness, 626 metadata supply improvements, and program greenlight/capacity.",
        ],
    ),
    (
        1064,
        [
            "North star: users can find, trust, and cite steward-attested, governed metadata on OMS through Navigator.",
            "Reduce tribal knowledge — definitions, ownership, classifications, and lineage context should be discoverable without Slack archaeology.",
            "Close the Alation exit with MVP discovery parity (search, browse, glossary, gold/provenance, classifications read) on the OMS spine.",
            "Phase 2 extends into the full governance command center (pillar deep links, remediation queues) without blocking MVP catalog value.",
        ],
    ),
    (
        921,
        [
            "OMS already exists as the operational metadata backbone — paying for a parallel catalog duplicates cost and creates drift.",
            "Persona-opinionated UX: Alation served many users generically; Navigator can prioritize DEEPT jobs (find/trust for business users, evidence for compliance).",
            "Contract and migration window make this the right time to consolidate on OMS + Navigator rather than extend a tool we are exiting.",
        ],
    ),
    (
        538,
        [
            "OMS is the system of record for technical lineage (table, column, pipeline granularity) — stored, served via APIs, and owned by the OMS platform.",
            "626 / MCI improves lineage supply (scanning, curation at source); Navigator does not rebuild or duplicate the lineage store.",
            "Navigator surfaces business-context lineage on asset pages — upstream/downstream summaries, provenance badges, impact context for trust and compliance questions.",
            "Deep technical lineage (full graph, column drill, pipeline linkage) → “Open in OMS” for engineers and power users.",
            "One API, two shells: OMS UI answers “how is it built?”; Navigator answers “what does it mean — can I trust it?” — both read from the same OMS spine.",
        ],
    ),
    (
        514,
        [
            "Lock a small persona set (3–5) for the next phase and write one “when X, they need Y in under Z” sentence per persona — that drives navigation defaults.",
            "Persona-first IA: each major surface should primarily complete one persona story; if it serves “everyone,” split into a primary path and secondary entry points or defer to a later phase.",
            "Role-aware landing & filters: e.g. Privacy sees consent/DSR/tracker paths first; Business sees catalog discovery; Technical gets a clear handoff to OMS.",
            "“By persona” hubs on the governance portal (Privacy & Compliance, Business, Technical) with curated deep links — not a flat list of every capability.",
            "Thin vs. deep by persona in MVP: full discovery for business consumers; thin steward endorse/reconcile; read-only, role-filtered for compliance; engineer remediation stays in OMS.",
            "Validate with users once greenlit: wireframe tests and A/B experiments on IA and defaults — but persona stories and boundary tables come first.",
        ],
    ),
    (
        469,
        [
            "Business / DNA consumers & analysts — find, trust, and use the right metric or dataset for a business question (search, browse, glossary, classifications).",
            "Data stewards / owners — curate, endorse, and reconcile definitions; run governance workloads at scale.",
            "Privacy & compliance reviewers — read policy/classification context, run attestations, export audit-friendly evidence.",
            "Security & access reviewers — understand data use posture, access, and GIS compliance signals.",
            "Regulatory program managers — track laws/regulations, incidents, and inventory posture (via Kronos and linked workflows).",
            "Data engineers — rely on technical truth and lineage; primary deep-dive UI hands off to OMS (“Open in OMS”).",
            "DRE / automation consumers — API-first read access to governed metadata without living in the UI.",
            "Governance leads & auditors — executive posture, exception queues, and packaged control narratives.",
        ],
    ),
    (
        433,
        [
            "Navigator is the umbrella name for DEEPT’s data governance products, programs, catalog experience, and operations — one coherent story instead of disconnected tools.",
            "Design principle: Unified experience, federated execution — one portal for orientation and posture; authoritative systems (OMS, PULS, OneTrust, Kronos, etc.) stay authoritative.",
            "Stack: 626 improves metadata supply → OMS stores and serves technical/operational metadata → Navigator is the governed experience layer for the right persona (not a duplicate metadata store).",
            "Reframes prior initiatives: Governance Portal → Navigator (program command center); Business Data Navigator → Business Data Catalog (catalog on OMS); PULS + Gov backend → policy-driven governance framework; Kronos → linked business inventory.",
        ],
    ),
]


def text_from_bullets(bullets: list[str]) -> str:
    return "".join(f"{b}\n" for b in bullets)


def main() -> None:
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

    requests = []
    bullet_ranges: list[tuple[int, int]] = []
    for insert_index, bullets in INSERTIONS:
        text = text_from_bullets(bullets)
        bullet_ranges.append((insert_index, insert_index + len(text)))
        requests.append(
            {"insertText": {"location": {"index": insert_index}, "text": text}}
        )

    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()

    doc = service.documents().get(documentId=DOC_ID).execute()
    list_id = next(iter(doc.get("lists", {})), None)

    bullet_requests = []
    for start, end in bullet_ranges:
        bullet_requests.append(
            {
                "createParagraphBullets": {
                    "range": {"startIndex": start, "endIndex": end},
                    "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                }
            }
        )
        if list_id:
            bullet_requests.append(
                {
                    "updateParagraphStyle": {
                        "range": {"startIndex": start, "endIndex": end},
                        "paragraphStyle": {
                            "indentFirstLine": {"magnitude": 54, "unit": "PT"},
                            "indentStart": {"magnitude": 72, "unit": "PT"},
                            "bullet": {"listId": list_id, "nestingLevel": 1},
                        },
                        "fields": "indentFirstLine,indentStart,bullet",
                    }
                }
            )

    if bullet_requests:
        service.documents().batchUpdate(
            documentId=DOC_ID, body={"requests": bullet_requests}
        ).execute()

    print(f"Updated https://docs.google.com/document/d/{DOC_ID}/edit")


if __name__ == "__main__":
    main()
