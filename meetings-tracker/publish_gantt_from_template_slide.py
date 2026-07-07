#!/usr/bin/env python3
"""
Build an executive Gantt in Google Slides using the same *layout slide* as:
  Working Copy Mar 2026 - Data Governance Overview
  (roadmap slide with title bar + table region).

Steps:
  1) Drive: copy the template deck
  2) Slides: delete every slide except the template roadmap slide
  3) Slides: remove the sample table, pills, and groups; keep the title shape
  4) Slides: insert a wide table and load rows from the Gantt CSV
  5) Slides: navy header row styling (matches executive Sheet theme)
  6) Drive: move copy into the program folder

Auth: same user credential as All Google MCP:
  ~/Library/Application Support/All Google MCP/token.json
Scopes: presentations + drive (refresh if copy fails).

All-Google MCP only implements slides_get_presentation (read-only); this script
performs the copy/update via Slides API. Use MCP afterward to verify IDs/links.
"""

from __future__ import annotations

import csv
import sys
import uuid
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = Path.home() / "Library/Application Support/All Google MCP/token.json"
SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]

TEMPLATE_PRESENTATION_ID = "19CnHhso_Ts0tVaqtrdGLrtiWlriuffpGfvidMaFa-oU"
TEMPLATE_SLIDE_ID = "g3e63f450cd8_2_512"
TITLE_SHAPE_ID = "g3e63f450cd8_2_513"
FOLDER_ID = "1m-r_p9q0AClDByNnSb7Ll7p4cFae-5P9"

NEW_DECK_TITLE = (
    "Business Data Catalog — OMS & Alation Migration | Executive Gantt (Slide)"
)
TITLE_TEXT = (
    "Business Data Catalog — OMS & Alation Migration | Executive Program Gantt\n"
    "Jan-26 → Oct-27 timeline (see table)"
)

NAVY = {"red": 0.105882, "green": 0.211765, "blue": 0.364706}
WHITE = {"red": 1.0, "green": 1.0, "blue": 1.0}

EMU_PER_PT = 12700


def load_cohort_rows(csv_path: Path) -> tuple[list[list[str]], int]:
    """Return [header] + task rows, each padded to ncol (31)."""
    ncol = 31
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header_idx = 4
    header = list(rows[header_idx])
    if len(header) < ncol:
        header.extend([""] * (ncol - len(header)))
    else:
        header = header[:ncol]
    body: list[list[str]] = []
    for i in range(header_idx + 1, len(rows)):
        row = rows[i]
        if row and row[0].strip().upper().startswith("MILESTONES"):
            break
        if not row or (row[0].strip() == "" and (len(row) < 4 or row[3].strip() == "")):
            continue
        if row[0].strip() == "" and row[3].strip() == "":
            continue
        r = list(row)
        if len(r) < ncol:
            r.extend([""] * (ncol - len(r)))
        else:
            r = r[:ncol]
        body.append(r)
    return [header] + body, ncol


def batch_update(svc, presentation_id: str, requests: list[dict], chunk: int = 80) -> None:
    for i in range(0, len(requests), chunk):
        svc.presentations().batchUpdate(
            presentationId=presentation_id, body={"requests": requests[i : i + chunk]}
        ).execute()


def main() -> None:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "_gantt_mcp_upload.csv"
    if not csv_path.is_file():
        print("CSV not found:", csv_path, file=sys.stderr)
        sys.exit(1)
    if not TOKEN_PATH.is_file():
        print("Missing All Google MCP token:", TOKEN_PATH, file=sys.stderr)
        sys.exit(1)

    grid, ncol = load_cohort_rows(csv_path)
    nrows = len(grid)
    if ncol != 31:
        print("Expected 31 columns, got", ncol, file=sys.stderr)
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())

    slides = build("slides", "v1", credentials=creds, cache_discovery=False)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    copied = (
        drive.files()
        .copy(
            fileId=TEMPLATE_PRESENTATION_ID,
            body={"name": NEW_DECK_TITLE},
            fields="id, webViewLink",
            supportsAllDrives=True,
        )
        .execute()
    )
    new_id = copied["id"]
    link = copied.get("webViewLink") or f"https://docs.google.com/presentation/d/{new_id}/edit"

    pres = slides.presentations().get(presentationId=new_id).execute()
    slide_ids = [s["objectId"] for s in pres.get("slides", [])]
    del_slides = [sid for sid in slide_ids if sid != TEMPLATE_SLIDE_ID]
    # Slides API removes slides via deleteObject (slideId), not removeSlide/deleteSlide.
    batch_update(slides, new_id, [{"deleteObject": {"objectId": sid}} for sid in del_slides])

    pres = slides.presentations().get(presentationId=new_id).execute()
    slide = pres["slides"][0]
    assert slide["objectId"] == TEMPLATE_SLIDE_ID
    keep = {TITLE_SHAPE_ID}
    del_elems = [el["objectId"] for el in slide.get("pageElements", []) if el["objectId"] not in keep]
    batch_update(slides, new_id, [{"deleteObject": {"objectId": oid}} for oid in del_elems])

    reqs: list[dict] = [
        {
            "deleteText": {
                "objectId": TITLE_SHAPE_ID,
                "textRange": {"type": "ALL"},
            }
        },
        {
            "insertText": {
                "objectId": TITLE_SHAPE_ID,
                "insertionIndex": 0,
                "text": TITLE_TEXT,
            }
        },
    ]
    batch_update(slides, new_id, reqs)

    table_id = "GanttTbl" + uuid.uuid4().hex[:8]
    reqs = [
        {
            "createTable": {
                "objectId": table_id,
                "elementProperties": {
                    "pageObjectId": TEMPLATE_SLIDE_ID,
                    "size": {
                        "width": {"magnitude": 920, "unit": "PT"},
                        "height": {"magnitude": min(480, max(120, nrows * 11)), "unit": "PT"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": int(12 * EMU_PER_PT),
                        "translateY": int(48 * EMU_PER_PT),
                        "unit": "EMU",
                    },
                },
                "rows": nrows,
                "columns": ncol,
            }
        }
    ]
    batch_update(slides, new_id, reqs)

    def trunc(val: str, col: int) -> str:
        v = (val or "").replace("\r", " ").strip()
        limits = (6, 14, 12, 42, 16, 11, 11, 4, 5, 11, 36) + tuple(3 for _ in range(20))
        lim = limits[col] if col < len(limits) else 8
        if len(v) > lim:
            return v[: lim - 1] + "…"
        return v

    cell_reqs: list[dict] = []
    for r, row in enumerate(grid):
        for c, raw in enumerate(row):
            text = trunc(raw, c)
            if not text:
                continue
            # New table cells can be length-0; deleteText with ALL fails (endIndex 0).
            cell_reqs.append(
                {
                    "insertText": {
                        "objectId": table_id,
                        "cellLocation": {"rowIndex": r, "columnIndex": c},
                        "insertionIndex": 0,
                        "text": text,
                    }
                }
            )
    batch_update(slides, new_id, cell_reqs, chunk=60)

    style_reqs: list[dict] = []
    for c in range(ncol):
        style_reqs.append(
            {
                "updateTableCellProperties": {
                    "objectId": table_id,
                    "tableRange": {
                        "location": {
                            "rowIndex": 0,
                            "columnIndex": c,
                        },
                        "rowSpan": 1,
                        "columnSpan": 1,
                    },
                    "tableCellProperties": {
                        "tableCellBackgroundFill": {
                            "solidFill": {"color": {"rgbColor": NAVY}, "alpha": 1}
                        }
                    },
                    "fields": "tableCellBackgroundFill",
                }
            }
        )
        style_reqs.append(
            {
                "updateTextStyle": {
                    "objectId": table_id,
                    "cellLocation": {"rowIndex": 0, "columnIndex": c},
                    "style": {
                        "foregroundColor": {"opaqueColor": {"rgbColor": WHITE}},
                        "bold": True,
                        "fontSize": {"magnitude": 5.5, "unit": "PT"},
                    },
                    "textRange": {"type": "ALL"},
                    "fields": "foregroundColor,bold,fontSize",
                }
            }
        )
    batch_update(slides, new_id, style_reqs, chunk=40)

    try:
        fmeta = drive.files().get(
            fileId=new_id, fields="parents", supportsAllDrives=True
        ).execute()
        prev = ",".join(fmeta.get("parents", []))
        drive.files().update(
            fileId=new_id,
            addParents=FOLDER_ID,
            removeParents=prev,
            fields="id, webViewLink, name",
            supportsAllDrives=True,
        ).execute()
        print(f"(Moved to folder {FOLDER_ID})")
    except Exception as exc:
        print(
            f"(Could not move to folder {FOLDER_ID}: {exc}; deck stays in My Drive)",
            file=sys.stderr,
        )

    print(new_id)
    print(link)
    print(f"Rows × cols: {nrows} × {ncol}")


if __name__ == "__main__":
    main()
