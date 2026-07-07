#!/usr/bin/env python3
"""Replace OKR key-result paragraphs with feature-specific text in each matrix-linked PRD.

Uses the same OAuth token as All Google MCP. Safe to re-run: skips docs that already contain the
tailored block for that F-code.

Finds the current block from the line ``Key results (standard for success...)`` through the first
following ``\\n\\n`` (typical end of the OKR subsection), then replaceAllText — works even when the
original generic three KRs were edited or re-flowed, as long as that header and a closing blank line
remain.
"""
from __future__ import annotations

import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from okr_blocks import key_results_body

TOKEN_PATH = Path.home() / "Library/Application Support/All Google MCP/token.json"
SCOPES = ["https://www.googleapis.com/auth/documents"]

# document_id, matrix id, feature title, primary job (title/job unused here but kept aligned with append script)
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

KEY_HEADER = "Key results (standard for success in the first pilot / GA window):\n"


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
        elif "tableOfContents" in el:
            for c in el["tableOfContents"].get("content", []):
                walk(c)

    for el in body.get("content", []):
        walk(el)
    return "".join(parts)


def slice_key_results_block(plain: str) -> str | None:
    """Return the full substring to replace (including trailing \\n\\n when present), or None."""
    start = plain.find(KEY_HEADER)
    if start < 0:
        return None
    rest = plain[start:]
    d = rest.find("\n\n")
    if d == -1:
        return None
    return rest[: d + 2]


def main() -> None:
    if not TOKEN_PATH.exists():
        print("Missing token:", TOKEN_PATH, file=sys.stderr)
        sys.exit(1)
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
    svc = build("docs", "v1", credentials=creds, cache_discovery=False)

    for doc_id, fcode, _title, _job in DOCS:
        new_block = key_results_body(fcode)
        doc = svc.documents().get(documentId=doc_id).execute()
        plain = extract_plain(doc.get("body", {}))
        if new_block in plain:
            print("skip (already has tailored key results):", fcode, doc_id)
            continue
        old_block = slice_key_results_block(plain)
        if not old_block or old_block == new_block:
            print("skip (no OKR key-results block found):", fcode, doc_id)
            continue
        try:
            resp = svc.documents().batchUpdate(
                documentId=doc_id,
                body={
                    "requests": [
                        {
                            "replaceAllText": {
                                "containsText": {"text": old_block, "matchCase": True},
                                "replaceText": new_block,
                            }
                        }
                    ]
                },
            ).execute()
        except Exception as e:
            print("error:", fcode, doc_id, e, file=sys.stderr)
            continue
        n = 0
        for rep in resp.get("replies", []):
            r = rep.get("replaceAllText")
            if r and "occurrencesChanged" in r:
                n = int(r["occurrencesChanged"])
        if n == 0:
            print("warn (replace reported 0 occurrences):", fcode, doc_id)
        else:
            print("tailored KRs:", fcode, doc_id, f"({n} replacement(s))")


if __name__ == "__main__":
    main()
