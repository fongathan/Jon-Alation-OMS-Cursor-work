#!/usr/bin/env python3
"""Append a numbered OKR section to each PRD linked from the Feature Inventory Matrix.

Uses the same OAuth token as All Google MCP. Safe to re-run: skips docs that already
contain a top-level section heading like '5. OKR' (any digit + '. OKR').
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from okr_blocks import okr_body as okr_body_full

TOKEN_PATH = Path.home() / "Library/Application Support/All Google MCP/token.json"
SCOPES = ["https://www.googleapis.com/auth/documents"]

# document_id, matrix id, feature title, primary job-to-be-done (for OKR wording)
DOCS: list[tuple[str, str, str, str]] = [
    ("1hcZz7w1R6myhZYd7C34goN0oeZLNv8o5OI9RMEUbFFA", "F01", "Search & Discovery", "find trusted data assets quickly"),
    ("14D1OyRsWQFawaukLhSp4yKuFUegIUN2ISCDBzrNlSkg", "F02", "Business Glossary", "align the org on canonical definitions and stewardship"),
    ("1PM1CUCKpUMUQPxNsSijmD3NY9kw0kYoiIH4GpD0GH-8", "F03", "Catalog Browse", "explore sources and hierarchies without guesswork"),
    ("1k8zpsEVjaCGsz-seTaxo180qB6ei0tcY5p7BD8PXNCw", "F04", "Table / Asset Detail", "understand asset context before querying or sharing"),
    ("1dts_DdEsa1caLIw46v8_hrPUCptG-zRRtLev3MUNQyU", "F16", "Recommendations", "scale metadata quality with AI-assisted suggestions"),
    ("1PAZq862RS16jzmVHBZAMMZwE9YN7GDCcYwDBRAbrs1o", "F21", "Flags (endorsements, warnings, deprecations, popularity)", "signal trust and risk at the point of discovery"),
    ("176Vuq73A91wOpVnRj-01jRdG8G2XKSn-s2A2YTzd2R4", "F05", "Data Lineage", "run impact analysis and explain data provenance"),
    ("1dv02orjl38L-zrshXG2qnObwlWTXW9MoV0VLVGc8r68", "F25", "Admin Analytics Dashboard", "measure catalog health, adoption, and admin investigations"),
    ("1emf-fhIP4rSPq1NSmrn2NNWgrzRSTWpNTYdYdq9KdAg", "F06", "Tags & Classification", "apply consistent classification and compliance tags"),
    ("1YR9eqTkdVjZABc3HpOl6WwoGKlicCTKRLosdUQro55w", "F30", "Expanded Data Sources", "ingest critical non-default sources with reliable sync"),
    ("1BZnTsn2WU6uh-_m33G68plyizfXaZxZmTTUUplMa1XA", "F33", "Product Pages", "give each product a curated home linked to metrics and stewards"),
    ("1zP9wouUv_jsJXpYP7Ub82H0YdocMLnaAWdjRYDTXzNY", "F11", "Data Sources & Connectors", "keep technical metadata fresh for every in-scope system"),
    ("1b_lWmxPLCsPJg7FOT9q_1NXV5IlEC1FMqnQz81X_LQ4", "F20", "Authentication / SSO", "enforce enterprise identity and catalog RBAC end-to-end"),
    ("1HMFrfIuTlOCvKBc4GuvM3D6RnbVDv2mh1ZMCZ5W-9jw", "F23", "Folders / Source Navigation", "organize articles and navigation the way teams work"),
    ("1htpYdhO4bNB06YxuK_hUAqudBVRLfqPlwMHN-XDVgQU", "F09", "Ownership / Stewardship", "make accountability visible and actionable on every asset"),
    ("1m2nDKqRye31CbW-bnxa7MN0XyUjXUSUPNTUFBTfntmo", "F26", "Mass / Bulk Edit", "apply metadata changes at scale with auditability"),
    ("1CED1OgBgGT3vnRxq7T49W-q72qApDh2CTGFblJXaFaE", "F24", "Dataflows", "document pipelines and jobs alongside catalog objects"),
    ("13Xn16JHfpzUHLRZGd-OyomVyBy_3s1CmfgqVriVYjpM", "F22", "Domains", "scope discovery, policy, and stewardship by business domain"),
    ("12LkYLfrgo_zMFIUq2dqZOsyxUt8y83JLZrce2MF9GcQ", "F19", "Export / Reports", "support audits and leadership reporting from catalog truth"),
    ("1y0GaZr4uegdo6A5aJi_zyjROJdht5shiIG3HEklol2w", "F10", "Usage / Access Metrics", "expose consumption signals without exposing sensitive individual trails"),
    ("1Lz8RyX7mTkVglSxgIB5-vrsu6ACYCtS7zvZepP9ai_U", "F28", "AI Chat Assistant", "answer grounded catalog questions with governance-safe behavior"),
    ("1xUZymJJYS5dKp3rD2U8rh0OFQCCr0etY0_VZN_AeySY", "F27", "Mass Set Rules / Catalog Sets", "automate tagging and ownership from auditable rules"),
    ("1E5KBx25s9Vnu1ZIskHWZmdQkYpCabtGrk2J5ydZKeu8", "F29", "Data Dictionary Download & Uploads", "round-trip bulk metadata edits with validation and logs"),
    ("1kh-n-COtph0DPJuaqEj_xPqka27LEow7CeItA6aFMLU", "F17", "Saved Queries / Favorites", "reduce repeat discovery time for frequent assets"),
    ("1zfNSj-aBgajJCZABoVhZ-zbWzyx3vfG7yuoEK76Ncuc", "F35", "Overview & Social Section", "surface aggregate activity and curated updates without personal surveillance"),
    ("1LiG6PuuCOvYUdb9UtlCbRuKP34l-2MCmBOwunmBPpso", "F07", "Custom Fields", "capture domain-specific metadata consistently"),
    ("1LjsD5dlN7DSRm86kdnFRxbHv7Bodt2EnFfOgeJRJpe4", "F18", "Comments / Q&A", "resolve questions on assets with traceable collaboration"),
    ("1fyPOtEADlMz7RYc1dHXsT8tuOHsxYXOLuYSXEj0jCDk", "F15", "Version Control", "recover from bad edits and prove metadata history"),
    ("1kPBL6aWBCK1Nb_HhEhAabXpNlLm5mmlevHf5BMnCLIw", "F12", "Policy Center", "attach enforceable policies to catalog objects"),
    ("1Xhnh8n6m_wWUd_HDOg7u6CQotnTgIbjaovuY5W0FPaw", "F13", "Compilation / Data Quality", "surface data quality signals where consumers decide"),
    ("1NzZGSQXR_8YbM08bz0mU-xqT13G7JEwKl7lsr_VJOQ4", "F14", "API & Integrations", "automate catalog operations for downstream tools"),
    ("1LmNJ0I6OudrUK4VsC1a1fc0iFJOx-R6_ts7IJxucxAg", "F31", "Details Icon", "explain features and metadata without leaving context"),
    ("1xvNuXHi3KyzfAZdin8lxCGSKVjDgF2RfTsSd_khtJXY", "F32", "Persona View Filtering", "tailor catalog views to role-specific needs"),
    ("10nHMo0xwJf0sr8t_jNTTENtuNKphzqVGyJFia7mezM4", "F34", "AI — How To", "onboard with grounded, policy-safe guidance"),
]


def max_end_index(obj: object, best: int = 1) -> int:
    if isinstance(obj, dict):
        if "endIndex" in obj and isinstance(obj["endIndex"], int):
            best = max(best, obj["endIndex"])
        for v in obj.values():
            best = max_end_index(v, best)
    elif isinstance(obj, list):
        for x in obj:
            best = max_end_index(x, best)
    return best


def extract_plain(body: dict) -> str:
    parts: list[str] = []

    def walk(el: dict) -> None:
        if "paragraph" in el:
            for pe in el["paragraph"].get("elements", []):
                tr = pe.get("textRun")
                if tr:
                    parts.append(tr.get("content", ""))
        elif "table" in el:
            for row in el["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    for c in cell.get("content", []):
                        walk(c)
        elif "sectionBreak" in el:
            return
        elif "tableOfContents" in el:
            for c in el["tableOfContents"].get("content", []):
                walk(c)

    for el in body.get("content", []):
        walk(el)
    return "".join(parts)


def max_numbered_heading(plain: str) -> int:
    best = 0
    for line in plain.splitlines():
        line = line.strip()
        m = re.match(r"^(\d+)\.\s+\S", line)
        if m:
            best = max(best, int(m.group(1)))
    return best


def has_okr_section(plain: str) -> bool:
    return bool(re.search(r"^\d+\.\s*OKR\s*$", plain, re.MULTILINE))


def okr_body(fcode: str, title: str, job: str) -> str:
    return okr_body_full(fcode, title, job)
1

def main() -> None:
    if not TOKEN_PATH.exists():
        print("Missing token:", TOKEN_PATH, file=sys.stderr)
        sys.exit(1)
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
    svc = build("docs", "v1", credentials=creds, cache_discovery=False)

    for doc_id, fcode, title, job in DOCS:
        doc = svc.documents().get(documentId=doc_id).execute()
        plain = extract_plain(doc.get("body", {}))

        pre_requests = []
        if "TEST_INSERT_DELETE" in plain:
            pre_requests.append(
                {
                    "replaceAllText": {
                        "containsText": {"text": "TEST_INSERT_DELETE", "matchCase": True},
                        "replaceText": "",
                    }
                }
            )
        if pre_requests:
            svc.documents().batchUpdate(documentId=doc_id, body={"requests": pre_requests}).execute()
            doc = svc.documents().get(documentId=doc_id).execute()
            plain = extract_plain(doc.get("body", {}))

        if has_okr_section(plain):
            print("skip (already has OKR section):", fcode, doc_id)
            continue

        n = max_numbered_heading(plain) + 1
        text = f"\n\n{n}. OKR\n" + okr_body(fcode, title, job)
        end_idx = max_end_index(doc) - 1
        if end_idx < 1:
            print("skip (bad index):", fcode, doc_id, file=sys.stderr)
            continue

        svc.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": [{"insertText": {"location": {"index": end_idx}, "text": text}}]},
        ).execute()
        print("appended OKR as section", n, ":", fcode, doc_id)


if __name__ == "__main__":
    main()
