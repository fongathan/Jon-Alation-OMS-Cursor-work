#!/usr/bin/env python3
"""Emit CSV for gsheets_create (MCP). Writes UTF-8 CSV to path or stdout."""

import csv
import io
import sys
from datetime import date

from generate_executive_gantt import (
    PHASE_STYLES,
    get_program_tasks_and_months,
    month_bounds,
    month_range,
    overlaps,
)

TIMELINE_START = date(2026, 3, 1)
TIMELINE_END = date(2027, 10, 31)


def main() -> None:
    tasks, _ = get_program_tasks_and_months()
    months = month_range(TIMELINE_START, TIMELINE_END)
    n_meta = 11

    out: io.StringIO = io.StringIO()
    w = csv.writer(out, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")

    title = (
        "Business Data Catalog — In-House (OMS) & Alation Migration | "
        "Disney Streaming Services | Executive Program Gantt"
    )
    sub = (
        "Sources: Product Brief & Migration Project Plan (Mar 2026) • "
        "Baseline Alation contract end: 1-Oct-2026 • "
        "Recommended: extension + cutover Feb–Mar 2027 • Decommission Oct 2027"
    )
    w.writerow([title] + [""] * (n_meta + len(months) - 1))
    w.writerow([sub] + [""] * (n_meta + len(months) - 1))
    w.writerow(["Phase legend: Program | Requirements | Design | Build MVP | Build parity | Migration | Change | Cutover | Risk"] + [""] * (n_meta + len(months) - 1))
    w.writerow([""] * (n_meta + len(months)))

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
    w.writerow(headers)

    for t in tasks:
        dur = max(0, (t["end"] - t["start"]).days) // 7
        if (t["end"] - t["start"]).days > 0 and dur == 0:
            dur = 1
        timeline = []
        for y, m in months:
            ms, me = month_bounds(y, m)
            if overlaps(t["start"], t["end"], ms, me):
                timeline.append("◆" if str(t["task"]).startswith("MILESTONE") else "■")
            else:
                timeline.append("")
        w.writerow(
            [
                t["wbs"],
                t["phase"],
                t["ws"],
                t["task"],
                t["owner"],
                t["start"].isoformat(),
                t["end"].isoformat(),
                dur,
                f"{t['pct']}%",
                t["status"],
                t["notes"],
            ]
            + timeline
        )

    w.writerow([""] * (n_meta + len(months)))
    w.writerow(["MILESTONES & KPIs", "", "", "", "", "", "", "", "", "", ""] + [""] * len(months))
    milestones = [
        ("Milestone / KPI", "Target / timing", "Owner", "Detail"),
        ("Requirements sign-off", "May–Jun 2026", "Data Governance", "Consolidated requirements; gate before build."),
        ("OMS MVP deployed", "Sep–Oct 2026", "OMS / Engineering", "Glossary, search, tags/docs, lineage MVP."),
        ("Parallel run live", "Oct 2026 – Jan 2027", "PMO", "Alation + OMS validation."),
        ("Metadata migration validated", "Feb 2027", "Engineering / Gov", "≥95% business metadata preserved."),
        ("OMS primary (cutover)", "Feb–Mar 2027", "Steering", "OMS system of record."),
        ("User adoption", "Within 4 wks of cutover", "Governance", "≥80% former Alation WAU in OMS."),
        ("Alation decommission", "Oct 2027 (extended)", "Eng / Procurement", "Sunset; archive & audit."),
        ("Baseline contract (risk)", "1-Oct-2026", "Sponsor", "Without extension: high risk."),
    ]
    for row in milestones:
        pad = list(row) + [""] * (n_meta + len(months) - len(row))
        w.writerow(pad[: n_meta + len(months)])

    w.writerow([""] * (n_meta + len(months)))
    w.writerow(
        [
            "Tip: Select row 1–2 → bold, fill #1B365D (navy), font white. Freeze rows 5 and columns A–K. Status column: Data validation list.",
        ]
        + [""] * (n_meta + len(months) - 1)
    )

    data = out.getvalue()
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if path:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(data)
        print(path)
    else:
        sys.stdout.write(data)


if __name__ == "__main__":
    main()
