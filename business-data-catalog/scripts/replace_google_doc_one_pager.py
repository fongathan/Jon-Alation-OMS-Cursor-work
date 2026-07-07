#!/usr/bin/env python3
"""Replace Google Doc body with condensed one-page plan."""
import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

DOC_ID = "1OwYe7m2IQP2yW-ohV9QMeHlq9Gxhpj5LzrTKIBYl0Hc"
TOKEN_PATH = Path.home() / "Library/Application Support/All Google MCP/token.json"

BODY = """DATA NAVIGATOR — APPROACH (ONE PAGE) · May 2026
Jonathan Fong · Data Governance · Data Platforms Intake

RESET AFTER MAY INTAKE
Intake supported Alation → OMS direction but not one UI that looked like 626 + OMS + DSAR/tracker/consent + discovery combined. We reset to: (1) persona-first scope, (2) clear layers — 626 = supply, OMS = store/APIs, Navigator = experience only, (3) governance command center = phase 2, not MVP.

NORTH STAR · Oct 1, 2026 (Alation exit)
Business & compliance users find, trust, and cite governed metadata on OMS via a named Navigator experience — fed by 626/MCI supply, stored in OMS.
Stack: 626 → supply · OMS → store · Navigator → governed UX for the right persona.

WHO WE SERVE (MVP ORDER)
• PRIMARY — Business/DNA consumer & analyst/BI: find & trust metrics/datasets → full discovery (search, browse, gold + provenance, glossary, classifications read).
• SECONDARY — Steward: endorse/reconcile (thin). Privacy/compliance: evidence & policy context (read, role-filtered).
• HANDOFF — Engineer → OMS UI (“Open in OMS”). DRE → API read (MVP requirement).
• PHASE 2 — DRE/DPM remediation + governance hub (DSAR, tracker, consent, ops) — deep links, not rebuilt in Navigator MVP.

WHAT WE OWN vs NOT
OWN: Persona stories, acceptance, business-first UX on OMS APIs, gold presentation & provenance badges, deep links/API needs.
NOT: 626 scanning, OMS platform/technical UI, corporate metric definition (federated), pillar operational consoles, fixing ~18–20% coverage without 626.
OMS UI = “How is it built?” · Navigator = “What does it mean — can I trust it?” · One API, two shells.

TWO TRACKS · ONE STORY
A — Navigator MVP now (persona-led discovery, Alation parity path). B — Governance hub phase 2 (posture, exceptions, pillar links, same OMS spine).

NEXT ~3 WEEKS
Week: 5 consumer stories + steward/compliance thin set (Sarah/Suman). Strip POC to MVP paths only.
Intake: Persona-first deck — scope alignment. WG: 626→OMS→Navigator RACI. Capacity plan offline (Loni).

MVP IN / OUT
IN: Search/browse, gold+provenance, glossary, classifications (read), thin steward signals, read API, Open in OMS.
OUT: DSAR/tracker consoles, DRE remediation UI, governance overview queue, SQL/social/admin playground.

INTAKE ASKS
(1) Endorse persona-first MVP. (2) Navigator = program UI on OMS — not competing platform. (3) WG time on stories + handoffs.

TIMELINE
Intake alignment → next session · Alation Oct 1, 2026 · MVP ~8–10 mo (eng Q3) · Governance hub phase 2 after MVP paths proven.
"""


def main():
    data = json.loads(TOKEN_PATH.read_text())
    creds = Credentials(
        token=data.get("token"),
        refresh_token=data.get("refresh_token"),
        token_uri=data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=data.get("client_id"),
        client_secret=data.get("client_secret"),
        scopes=data.get("scopes"),
    )
    service = build("docs", "v1", credentials=creds, cache_discovery=False)
    doc = service.documents().get(documentId=DOC_ID).execute()
    end_index = doc["body"]["content"][-1]["endIndex"]
    requests = [
        {"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end_index - 1}}},
        {"insertText": {"location": {"index": 1}, "text": BODY}},
    ]
    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()
    print(f"Updated https://docs.google.com/document/d/{DOC_ID}/edit")


if __name__ == "__main__":
    main()
