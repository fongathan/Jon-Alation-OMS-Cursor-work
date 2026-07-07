#!/usr/bin/env python3
"""
Remove section "14. References" from every Google Doc in a Drive folder.

One batchUpdate per document (single deleteContentRange) to stay under Docs API
write quota (~60/min). Trims endIndex if Google rejects newline-at-segment-end.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

TOKEN_PATH = Path.home() / "Library/Application Support/All Google MCP/token.json"
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive.readonly",
]
FOLDER_ID = "1NY805KZKDSkvwQ0XnN4z450E642nbQGy"

ref_heading = re.compile(r"^14\.\s*References\b", re.I)
feature_inv = re.compile(r"^Feature\s+Inventory\s+Matrix", re.I)
workspace_line = re.compile(r"^Workspace\s*:", re.I)
bdc_line = re.compile(r"^BDC\s*/\s*OMS\s+UX", re.I)


def creds() -> Credentials:
    c = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not c.valid and c.refresh_token:
        c.refresh(Request())
    return c


def paragraph_text(para: dict) -> str:
    parts: list[str] = []
    for elem in para.get("elements", []) or []:
        tr = elem.get("textRun")
        if tr:
            parts.append(tr.get("content", "") or "")
    return "".join(parts)


def collect_section_14_paragraph_ranges(body_content: list) -> list[tuple[int, int]]:
    paras: list[tuple[int, int, str]] = []
    for el in body_content:
        if "paragraph" not in el:
            continue
        si = el.get("startIndex")
        ei = el.get("endIndex")
        if si is None or ei is None:
            continue
        t = paragraph_text(el["paragraph"]).strip()
        paras.append((si, ei, t))

    for idx, (si, ei, t) in enumerate(paras):
        if not ref_heading.match(t):
            continue
        out: list[tuple[int, int]] = [(si, ei)]
        j = idx + 1
        while j < len(paras):
            si2, ei2, t2 = paras[j]
            if t2 == "":
                out.append((si2, ei2))
                j += 1
                continue
            if feature_inv.match(t2) or workspace_line.match(t2):
                out.append((si2, ei2))
                j += 1
                continue
            if bdc_line.match(t2):
                out.append((si2, ei2))
                return out
            break
        return out
    return []


def delete_merged_range(docs, doc_id: str, start_idx: int, end_idx: int) -> None:
    """Delete [start_idx, end_idx) with end trimming and short retry on API errors."""
    if end_idx <= start_idx:
        return
    trimmed = end_idx - 1
    while trimmed > start_idx:
        try:
            docs.documents().batchUpdate(
                documentId=doc_id,
                body={
                    "requests": [
                        {"deleteContentRange": {"range": {"startIndex": start_idx, "endIndex": trimmed}}}
                    ]
                },
            ).execute()
            return
        except HttpError as e:
            err = str(e)
            if "newline character at the end of the segment" in err and trimmed > start_idx + 1:
                trimmed -= 1
                continue
            if "RATE_LIMIT" in err or "429" in err:
                time.sleep(3)
                continue
            raise
    raise RuntimeError(f"Could not delete range [{start_idx}, {end_idx}) in {doc_id}")


def main() -> None:
    c = creds()
    drive = build("drive", "v3", credentials=c, cache_discovery=False)
    docs = build("docs", "v1", credentials=c, cache_discovery=False)

    q = f"'{FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.document' and trashed = false"
    resp = (
        drive.files()
        .list(q=q, fields="files(id,name)", pageSize=100, supportsAllDrives=True, includeItemsFromAllDrives=True)
        .execute()
    )
    files = resp.get("files", [])
    if not files:
        print("No Google Docs in folder.", file=sys.stderr)
        sys.exit(1)

    for f in sorted(files, key=lambda x: x.get("name", "")):
        doc_id = f["id"]
        name = f.get("name", doc_id)
        doc = docs.documents().get(documentId=doc_id).execute()
        body = doc.get("body", {}).get("content", [])
        ranges = collect_section_14_paragraph_ranges(body)
        if not ranges:
            print(f"SKIP (no section 14): {name}")
            continue
        start_idx = ranges[0][0]
        end_idx = ranges[-1][1]
        delete_merged_range(docs, doc_id, start_idx, end_idx)
        print(f"OK: {name}")
        time.sleep(1.1)  # stay under ~60 writes/min with get+update per file

    print("Done.")


if __name__ == "__main__":
    main()
