#!/usr/bin/env python3
"""
Create a native Google Sheet with executive Gantt formatting via Sheets API v4.

Auth (pick one):
  gcloud auth application-default login
  or set GOOGLE_APPLICATION_CREDENTIALS to a service account JSON (Sheets + Drive).

No local gcloud? Generate `ProgramGantt.gs` with export_apps_script_gantt.py and run
createExecutiveGantt() in https://script.google.com (creates the Sheet in your Drive).
"""

from __future__ import annotations

import sys
from datetime import date

from google.auth import default as google_auth_default
from googleapiclient.discovery import build

from generate_executive_gantt import (
    PHASE_STYLES,
    get_program_tasks_and_months,
    month_bounds,
    overlaps,
)

SCOPES = (
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
)

TITLE = "Business Data Catalog — OMS & Alation Migration (Executive Gantt)"
FOLDER_ID = "1m-r_p9q0AClDByNnSb7Ll7p4cFae-5P9"  # Program Drive folder

MILESTONES: list[tuple[str, str, str, str]] = [
    ("Milestone / KPI", "Target / timing", "Owner", "Detail"),
    (
        "Requirements sign-off",
        "May–Jun 2026",
        "Data Governance",
        "Consolidated requirements; gate before build acceleration.",
    ),
    (
        "OMS MVP deployed",
        "Sep–Oct 2026",
        "OMS / Engineering",
        "Glossary, business search, tags/docs, lineage MVP, usage/ownership where scoped.",
    ),
    (
        "Parallel run live",
        "Oct 2026 – Jan 2027",
        "PMO",
        "Alation + OMS; user validation; lower cutover risk.",
    ),
    (
        "Metadata migration validated",
        "Feb 2027",
        "Engineering / Gov",
        "≥95% business metadata preserved; lineage & glossary checks.",
    ),
    (
        "OMS primary (cutover)",
        "Feb–Mar 2027",
        "Steering",
        "OMS system of record; Alation read-only.",
    ),
    (
        "User adoption",
        "Within 4 wks of cutover",
        "Governance",
        "≥80% of former Alation WAU active in OMS (product brief target).",
    ),
    (
        "Alation decommission",
        "Oct 2027 (extended contract)",
        "Eng / Procurement",
        "Full sunset; archive & audit pack.",
    ),
    (
        "Baseline contract date (risk)",
        "1-Oct-2026",
        "Sponsor",
        "Without extension: MVP-only + high risk; negotiate extension per project plan.",
    ),
]


def rgb(hex_color: str) -> dict[str, float]:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return {"red": r / 255.0, "green": g / 255.0, "blue": b / 255.0}


def sheets_serial(d: date) -> int:
    """Google Sheets date serial (epoch Dec 30, 1899)."""
    epoch = date(1899, 12, 30)
    return (d - epoch).days


def col_letter(n: int) -> str:
    """1-based column index to A1 letter(s)."""
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def main() -> None:
    creds, _ = google_auth_default(scopes=SCOPES)
    sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    tasks, months = get_program_tasks_and_months()
    n_meta = 11
    n_months = len(months)
    ncols = n_meta + n_months

    header_row_1based = 5
    data_start_1based = header_row_1based + 1
    nrows = header_row_1based + len(tasks)

    # --- Create spreadsheet with 3 tabs ---
    create_body = {
        "properties": {"title": TITLE},
        "sheets": [
            {
                "properties": {
                    "title": "Executive Gantt",
                    "gridProperties": {
                        "frozenRowCount": header_row_1based,
                        "frozenColumnCount": n_meta,
                    },
                }
            },
            {"properties": {"title": "Milestones & KPIs"}},
            {"properties": {"title": "Notes"}},
        ],
    }
    ss = sheets.spreadsheets().create(body=create_body).execute()
    spreadsheet_id = ss["spreadsheetId"]
    sheet_id = ss["sheets"][0]["properties"]["sheetId"]
    ms_sheet_id = ss["sheets"][1]["properties"]["sheetId"]
    notes_sheet_id = ss["sheets"][2]["properties"]["sheetId"]

    last_col = col_letter(ncols)
    title_text = (
        "Business Data Catalog — In-House (OMS) & Alation Migration  |  "
        "Disney Streaming Services  |  Executive Program Gantt"
    )
    subtitle_text = (
        "Sources: Product Brief & Migration Project Plan (Mar 2026)  •  "
        "Baseline Alation contract end: 1-Oct-2026  •  "
        "Recommended: extension + cutover Feb–Mar 2027  •  Decommission Oct 2027"
    )

    # Build value grid (1-based rows for clarity when appending)
    values_rows: list[list[object]] = []
    row1 = [title_text] + [""] * (ncols - 1)
    values_rows.append(row1)
    row2 = [subtitle_text] + [""] * (ncols - 1)
    values_rows.append(row2)
    leg = ["Phase legend (timeline bar colors):"] + [""] * (ncols - 1)
    values_rows.append(leg)
    values_rows.append([""] * ncols)
    headers = [
        "WBS",
        "Phase",
        "Workstream",
        "Task / Deliverable",
        "Owner",
        "Start",
        "End",
        "Duration (wks)",
        "% Complete",
        "Status",
        "Dependencies / Notes",
    ] + [date(y, m, 1).strftime("%b-%y") for y, m in months]
    values_rows.append(headers)

    for t in tasks:
        dur = max(0, (t["end"] - t["start"]).days) // 7
        if (t["end"] - t["start"]).days > 0 and dur == 0:
            dur = 1
        timeline: list[object] = []
        for y, m in months:
            ms, me = month_bounds(y, m)
            if overlaps(t["start"], t["end"], ms, me):
                if str(t.get("task", "")).startswith("MILESTONE"):
                    timeline.append("◆")
                else:
                    timeline.append("■")
            else:
                timeline.append("")
        values_rows.append(
            [
                t["wbs"],
                t["phase"],
                t["ws"],
                t["task"],
                t["owner"],
                sheets_serial(t["start"]),
                sheets_serial(t["end"]),
                dur,
                t["pct"] / 100.0,
                t["status"],
                t["notes"],
            ]
            + timeline
        )

    sheets.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'Executive Gantt'!A1:{last_col}{nrows}",
        valueInputOption="RAW",
        body={"values": values_rows},
    ).execute()

    # --- Formatting batch ---
    requests: list[dict] = []

    # Title & subtitle merges
    requests.append(
        {
            "mergeCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": ncols,
                },
                "mergeType": "MERGE_ALL",
            }
        }
    )
    requests.append(
        {
            "mergeCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 0,
                    "endColumnIndex": ncols,
                },
                "mergeType": "MERGE_ALL",
            }
        }
    )

    # Row heights
    for ri, h in [(0, 40), (1, 34), (2, 24), (3, 8), (4, 44)]:
        requests.append(
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "ROWS",
                        "startIndex": ri,
                        "endIndex": ri + 1,
                    },
                    "properties": {"pixelSize": h},
                    "fields": "pixelSize",
                }
            }
        )

    # Column widths (pixels)
    meta_widths = [56, 160, 112, 420, 150, 110, 110, 88, 88, 120, 340]
    for i, w in enumerate(meta_widths):
        requests.append(
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": i,
                        "endIndex": i + 1,
                    },
                    "properties": {"pixelSize": w},
                    "fields": "pixelSize",
                }
            }
        )
    for j in range(n_months):
        requests.append(
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": n_meta + j,
                        "endIndex": n_meta + j + 1,
                    },
                    "properties": {"pixelSize": 34},
                    "fields": "pixelSize",
                }
            }
        )

    # Title row format
    requests.append(
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": ncols,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": rgb("1B365D"),
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE",
                        "wrapStrategy": "WRAP",
                        "textFormat": {
                            "foregroundColor": rgb("FFFFFF"),
                            "fontSize": 15,
                            "bold": True,
                            "fontFamily": "Roboto",
                        },
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)",
            }
        }
    )
    requests.append(
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 0,
                    "endColumnIndex": ncols,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": rgb("334155"),
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE",
                        "wrapStrategy": "WRAP",
                        "textFormat": {
                            "foregroundColor": rgb("E2E8F0"),
                            "fontSize": 11,
                            "italic": True,
                            "fontFamily": "Roboto",
                        },
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)",
            }
        }
    )
    requests.append(
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 2,
                    "endRowIndex": 3,
                    "startColumnIndex": 0,
                    "endColumnIndex": ncols,
                },
                "cell": {
                    "userEnteredFormat": {
                        "verticalAlignment": "MIDDLE",
                        "textFormat": {"bold": True, "fontSize": 10, "fontFamily": "Roboto"},
                    }
                },
                "fields": "userEnteredFormat(verticalAlignment,textFormat)",
            }
        }
    )

    # Header row (row index 4)
    requests.append(
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 4,
                    "endRowIndex": 5,
                    "startColumnIndex": 0,
                    "endColumnIndex": ncols,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": rgb("0F172A"),
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE",
                        "wrapStrategy": "WRAP",
                        "textFormat": {
                            "foregroundColor": rgb("FFFFFF"),
                            "bold": True,
                            "fontSize": 10,
                            "fontFamily": "Roboto",
                        },
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)",
            }
        }
    )
    # Month header sub-style (slate)
    requests.append(
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 4,
                    "endRowIndex": 5,
                    "startColumnIndex": n_meta,
                    "endColumnIndex": ncols,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": rgb("475569"),
                        "textFormat": {
                            "foregroundColor": rgb("FFFFFF"),
                            "bold": True,
                            "fontSize": 9,
                            "fontFamily": "Roboto",
                        },
                        "textRotation": {"angle": 45},
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,textRotation)",
            }
        }
    )

    # Data rows: zebra meta columns + borders + date/percent formats
    data_start_idx = 5  # 0-based
    for i, _t in enumerate(tasks):
        r = data_start_idx + i
        alt = i % 2 == 1
        # Meta columns background
        bg = rgb("F8FAFC") if alt else rgb("FFFFFF")
        requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": r,
                        "endRowIndex": r + 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": n_meta,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "WRAP",
                            "backgroundColor": bg,
                            "borders": {
                                "top": {"style": "SOLID", "color": rgb("CBD5E1")},
                                "bottom": {"style": "SOLID", "color": rgb("CBD5E1")},
                                "left": {"style": "SOLID", "color": rgb("CBD5E1")},
                                "right": {"style": "SOLID", "color": rgb("CBD5E1")},
                            },
                        }
                    },
                    "fields": "userEnteredFormat(verticalAlignment,wrapStrategy,backgroundColor,borders)",
                }
            }
        )
        # WBS bold
        requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": r,
                        "endRowIndex": r + 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": 1,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "textFormat": {"bold": True, "fontFamily": "Roboto"},
                        }
                    },
                    "fields": "userEnteredFormat.textFormat",
                }
            }
        )
        # Dates F,G (indices 5,6)
        requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": r,
                        "endRowIndex": r + 1,
                        "startColumnIndex": 5,
                        "endColumnIndex": 7,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "numberFormat": {"type": "DATE", "pattern": "mmm d, yyyy"},
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat",
                }
            }
        )
        # % column (index 8)
        requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": r,
                        "endRowIndex": r + 1,
                        "startColumnIndex": 8,
                        "endColumnIndex": 9,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "numberFormat": {"type": "PERCENT", "pattern": "0%"},
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat",
                }
            }
        )

    # Timeline column backgrounds + borders
    for i, t in enumerate(tasks):
        r = data_start_idx + i
        phase = t["phase"]
        _, light = PHASE_STYLES.get(phase, ("64748B", "F1F5F9"))
        is_mile = str(t.get("task", "")).startswith("MILESTONE")
        for j, (y, m) in enumerate(months):
            ms, me = month_bounds(y, m)
            if not overlaps(t["start"], t["end"], ms, me):
                continue
            bar_color = "F59E0B" if is_mile else light
            requests.append(
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": r,
                            "endRowIndex": r + 1,
                            "startColumnIndex": n_meta + j,
                            "endColumnIndex": n_meta + j + 1,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": rgb(bar_color),
                                "horizontalAlignment": "CENTER",
                                "verticalAlignment": "MIDDLE",
                                "borders": {
                                    "top": {"style": "SOLID", "color": rgb("94A3B8")},
                                    "bottom": {"style": "SOLID", "color": rgb("94A3B8")},
                                    "left": {"style": "SOLID", "color": rgb("94A3B8")},
                                    "right": {"style": "SOLID", "color": rgb("94A3B8")},
                                },
                                "textFormat": {
                                    "foregroundColor": rgb("1E293B"),
                                    "bold": is_mile,
                                    "fontSize": 9,
                                },
                            }
                        },
                        "fields": "userEnteredFormat",
                    }
                }
            )

    # Status column data validation (column J = index 9)
    requests.append(
        {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": data_start_idx,
                    "endRowIndex": data_start_idx + len(tasks),
                    "startColumnIndex": 9,
                    "endColumnIndex": 10,
                },
                "rule": {
                    "condition": {
                        "type": "ONE_OF_LIST",
                        "values": [
                            {"userEnteredValue": "Not started"},
                            {"userEnteredValue": "In progress"},
                            {"userEnteredValue": "At risk"},
                            {"userEnteredValue": "Blocked"},
                            {"userEnteredValue": "Complete"},
                            {"userEnteredValue": "Milestone"},
                        ],
                    },
                    "strict": False,
                    "showCustomUi": True,
                },
            }
        }
    )

    # Apply in chunks (API request size)
    def batch(reqs: list[dict]) -> None:
        if not reqs:
            return
        sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body={"requests": reqs}
        ).execute()

    chunk_size = 450
    for i in range(0, len(requests), chunk_size):
        batch(requests[i : i + chunk_size])

    # --- Milestones sheet (row 1: title, row 2: column headers, then data) ---
    ms_rows = [
        ["Key milestones & success criteria (from program documents)", "", "", ""],
        list(MILESTONES[0]),
    ]
    ms_rows.extend(list(r) for r in MILESTONES[1:])
    n_ms_rows = len(ms_rows)
    sheets.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'Milestones & KPIs'!A1:D{n_ms_rows}",
        valueInputOption="USER_ENTERED",
        body={"values": ms_rows},
    ).execute()

    ms_req: list[dict] = [
        {
            "mergeCells": {
                "range": {
                    "sheetId": ms_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 4,
                },
                "mergeType": "MERGE_ALL",
            }
        },
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": ms_sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 1,
                },
                "properties": {"pixelSize": 220},
                "fields": "pixelSize",
            }
        },
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": ms_sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 1,
                    "endIndex": 2,
                },
                "properties": {"pixelSize": 160},
                "fields": "pixelSize",
            }
        },
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": ms_sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 2,
                    "endIndex": 3,
                },
                "properties": {"pixelSize": 150},
                "fields": "pixelSize",
            }
        },
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": ms_sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 3,
                    "endIndex": 4,
                },
                "properties": {"pixelSize": 520},
                "fields": "pixelSize",
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": ms_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 4,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": rgb("1B365D"),
                        "horizontalAlignment": "CENTER",
                        "textFormat": {"foregroundColor": rgb("FFFFFF"), "bold": True, "fontSize": 13},
                    }
                },
                "fields": "userEnteredFormat",
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": ms_sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 0,
                    "endColumnIndex": 4,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": rgb("334155"),
                        "textFormat": {"foregroundColor": rgb("FFFFFF"), "bold": True},
                        "wrapStrategy": "WRAP",
                    }
                },
                "fields": "userEnteredFormat",
            }
        },
    ]
    for ri in range(2, n_ms_rows):
        alt = ri % 2 == 0
        ms_req.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": ms_sheet_id,
                        "startRowIndex": ri,
                        "endRowIndex": ri + 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": 4,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": rgb("F8FAFC") if alt else rgb("FFFFFF"),
                            "wrapStrategy": "WRAP",
                            "verticalAlignment": "TOP",
                        }
                    },
                    "fields": "userEnteredFormat",
                }
            }
        )
    sheets.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body={"requests": ms_req}
    ).execute()

    # --- Notes tab ---
    notes = [
        ["This sheet was generated by publish_google_gantt.py (native Google Sheets)."],
        [""],
        ["Refresh credentials if needed:  gcloud auth application-default login"],
        ["Regenerate:  python3 meetings-tracker/publish_google_gantt.py"],
    ]
    sheets.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="'Notes'!A1:A4",
        valueInputOption="RAW",
        body={"values": notes},
    ).execute()
    sheets.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "requests": [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": notes_sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": 4,
                            "startColumnIndex": 0,
                            "endColumnIndex": 6,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {"fontSize": 10, "foregroundColor": rgb("475569")}
                            }
                        },
                        "fields": "userEnteredFormat.textFormat",
                    }
                }
            ]
        },
    ).execute()

    # Move to Drive folder
    fmeta = drive.files().get(fileId=spreadsheet_id, fields="parents").execute()
    prev = ",".join(fmeta.get("parents", []))
    drive.files().update(
        fileId=spreadsheet_id,
        addParents=FOLDER_ID,
        removeParents=prev,
        fields="id, webViewLink, name",
        supportsAllDrives=True,
    ).execute()

    link = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
    print("Created Google Sheet:")
    print(link)
    print(f"(Also placed in Drive folder {FOLDER_ID})")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Failed:", e, file=sys.stderr)
        print(
            "\nEnsure Application Default Credentials are set, e.g.\n"
            "  gcloud auth application-default login\n"
            "and that the account can create Sheets and write to the target folder.",
            file=sys.stderr,
        )
        sys.exit(1)
