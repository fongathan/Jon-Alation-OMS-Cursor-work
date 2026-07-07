#!/usr/bin/env python3
"""
Remove duplicate PRD sections (same boilerplate on every feature page) from each
Google Doc in a Drive folder.

Deletes these top-level sections (heading "N. " with space after the number,
so 3.1 subsections stay inside section 3):
  2, 3, 4, 8, 9, 10, 11, 12, 13

Deletes from highest section number toward lowest so indices stay valid.
One batchUpdate per section removal; sleep between docs for quota.
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

# Remove in descending order (end of doc first)
SECTIONS_TO_REMOVE = frozenset({13, 12, 11, 10, 9, 8, 4, 3, 2})

# Top-level only: "2. Problem" yes; "3.1 In scope" no
TOP_LEVEL_HEADING = re.compile(r"^(\d+)\.\s+\S")


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


def parse_top_level_sections(body_content: list) -> list[tuple[int, int, int]]:
    """Return list of (section_number, element_start_index, element_end_index).

    Indices are on the structural element (body child), not nested fields — required
    by the Docs API. Headings inside tables are ignored (only top-level sections).
    """
    out: list[tuple[int, int, int]] = []
    for el in body_content:
        if "paragraph" not in el:
            continue
        si = el.get("startIndex")
        ei = el.get("endIndex")
        if si is None or ei is None:
            continue
        raw = paragraph_text(el["paragraph"])
        stripped = raw.strip()
        m = TOP_LEVEL_HEADING.match(stripped)
        if not m:
            continue
        num = int(m.group(1))
        out.append((num, si, ei))
    return out


def document_body_end(doc: dict) -> int:
    """Last structural element endIndex (exclusive end of body)."""
    content = doc.get("body", {}).get("content", [])
    if not content:
        return 1
    return content[-1].get("endIndex", 1)


def find_delete_ranges(sections: list[tuple[int, int, int]], body_end: int) -> list[tuple[int, int]]:
    """
    sections: sorted by start index ascending: (num, para_start, para_end).
    Return list of (start, end_exclusive) for each section to remove, sorted
    by start descending for safe sequential deletion.
    """
    if not sections:
        return []
    by_num: dict[int, tuple[int, int, int]] = {}
    for num, si, ei in sections:
        by_num[num] = (num, si, ei)

    # Sort sections by paragraph start index
    ordered = sorted(sections, key=lambda x: x[1])
    num_to_next_start: dict[int, int] = {}
    for i, (num, si, ei) in enumerate(ordered):
        if i + 1 < len(ordered):
            num_to_next_start[num] = ordered[i + 1][1]
        else:
            num_to_next_start[num] = body_end

    ranges: list[tuple[int, int]] = []
    for num in SECTIONS_TO_REMOVE:
        if num not in by_num:
            continue
        _, si, _ei = by_num[num]
        end_excl = num_to_next_start[num]
        if end_excl > si:
            ranges.append((si, end_excl))
    # Delete from largest start index first
    ranges.sort(key=lambda x: x[0], reverse=True)
    return ranges


def delete_range_with_trim(docs, doc_id: str, start_idx: int, end_idx: int) -> None:
    """Delete [start_idx, end_idx) using Google Docs exclusive endIndex.

    `end_idx` must be the start index of the following section (or body end).
    Do not pre-subtract 1 — that can split tables and triggers 'Invalid deletion range'.
    Only shrink end_idx on specific API errors (trailing newline rules).
    """
    if end_idx <= start_idx:
        return
    trimmed = end_idx
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
            if "429" in err or "RATE_LIMIT" in err:
                time.sleep(4)
                continue
            raise
    raise RuntimeError(f"Could not delete [{start_idx}, {end_idx}) in {doc_id}")


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
        body_end = document_body_end(doc)
        sections = parse_top_level_sections(body)
        ranges = find_delete_ranges(sections, body_end)
        if not ranges:
            print(f"SKIP (no matching sections): {name}")
            continue
        for si, ei in ranges:
            delete_range_with_trim(docs, doc_id, si, ei)
            time.sleep(0.35)
        print(f"OK: {name}  ({len(ranges)} range(s))")
        time.sleep(1.2)

    print("Done.")


if __name__ == "__main__":
    main()
