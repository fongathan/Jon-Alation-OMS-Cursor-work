#!/usr/bin/env python3
"""
Generates an executive-style Gantt workbook for the Business Data Catalog (OMS)
and Alation migration program. Upload the .xlsx to Google Drive and open with
Google Sheets for cloud collaboration; formatting transfers well.
"""

from __future__ import annotations

import calendar
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUTPUT = Path(__file__).resolve().parent.parent / "Business-Data-Catalog-Migration-Executive-Gantt.xlsx"

# Phase → header color (dark) and Gantt bar color (light)
PHASE_STYLES = {
    "Program & Governance": ("1B365D", "B8D4F0"),
    "Requirements": ("1D4ED8", "BFDBFE"),
    "Design & Architecture": ("5B21B6", "DDD6FE"),
    "Build — MVP": ("047857", "A7F3D0"),
    "Build — Full parity": ("065F46", "6EE7B7"),
    "Migration": ("B45309", "FDE68A"),
    "Change & Training": ("0E7490", "A5F3FC"),
    "Cutover & Close": ("991B1B", "FECACA"),
    "Risk / Dependency": ("4B5563", "E5E7EB"),
}

THIN = Side(style="thin", color="CBD5E1")


def month_range(start: date, end: date) -> list[tuple[int, int]]:
    """Inclusive list of (year, month) from start through end."""
    out: list[tuple[int, int]] = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        out.append((y, m))
        if m == 12:
            y, m = y + 1, 1
        else:
            m += 1
    return out


def month_bounds(y: int, m: int) -> tuple[date, date]:
    last = calendar.monthrange(y, m)[1]
    return date(y, m, 1), date(y, m, last)


def overlaps(task_start: date, task_end: date, ms: date, me: date) -> bool:
    return not (task_end < ms or task_start > me)


def get_program_tasks_and_months() -> tuple[list[dict], list[tuple[int, int]]]:
    timeline_start = date(2026, 3, 1)
    timeline_end = date(2027, 10, 31)
    months = month_range(timeline_start, timeline_end)

    tasks: list[dict] = [
        # Program & Governance
        {
            "wbs": "1.0",
            "phase": "Program & Governance",
            "ws": "Steering",
            "task": "Program kickoff, charter, steering committee cadence",
            "owner": "Sponsor / PMO",
            "start": date(2026, 3, 1),
            "end": date(2026, 3, 21),
            "pct": 0,
            "status": "Not started",
            "deps": "—",
            "notes": "Exec sponsor; cross-functional steering (Eng, Gov, Analytics)",
        },
        {
            "wbs": "1.1",
            "phase": "Program & Governance",
            "ws": "Governance",
            "task": "RACI, governance charter — OMS as system of record",
            "owner": "Data Governance",
            "start": date(2026, 3, 10),
            "end": date(2026, 4, 4),
            "pct": 0,
            "status": "Not started",
            "deps": "1.0",
            "notes": "Phase-gate sign-off model",
        },
        {
            "wbs": "1.2",
            "phase": "Risk / Dependency",
            "ws": "Vendor",
            "task": "Alation contract extension negotiation (target 1yr to Oct 2027)",
            "owner": "Procurement / Sponsor",
            "start": date(2026, 3, 1),
            "end": date(2026, 5, 15),
            "pct": 0,
            "status": "Not started",
            "deps": "—",
            "notes": "Fallback: 6-mo extension; wind-down / read-only pricing",
        },
        {
            "wbs": "1.3",
            "phase": "Program & Governance",
            "ws": "Comms",
            "task": "Stakeholder comms plan & leadership reporting",
            "owner": "PMO",
            "start": date(2026, 3, 15),
            "end": date(2027, 3, 31),
            "pct": 0,
            "status": "Not started",
            "deps": "1.0",
            "notes": "Timeline visibility; change management",
        },
        # Requirements (from Product Brief 3.1–3.4 + Project Plan gap process)
        {
            "wbs": "2.0",
            "phase": "Requirements",
            "ws": "Current state",
            "task": "Feature inventory matrix & Alation metadata export",
            "owner": "BA / Gov",
            "start": date(2026, 3, 15),
            "end": date(2026, 4, 18),
            "pct": 0,
            "status": "Not started",
            "deps": "—",
            "notes": "API/MCP export; glossary, articles, tags, lineage, custom fields",
        },
        {
            "wbs": "2.1",
            "phase": "Requirements",
            "ws": "Current state",
            "task": "Persona–feature matrix, stakeholder interviews, workflow docs",
            "owner": "BA / Gov",
            "start": date(2026, 3, 22),
            "end": date(2026, 4, 25),
            "pct": 0,
            "status": "Not started",
            "deps": "2.0",
            "notes": "Stewards, analysts, engineers, compliance, leadership",
        },
        {
            "wbs": "2.2",
            "phase": "Requirements",
            "ws": "Evidence",
            "task": "Screenshot library (Alation + OMS) with annotations",
            "owner": "BA / Gov",
            "start": date(2026, 4, 1),
            "end": date(2026, 5, 2),
            "pct": 0,
            "status": "Not started",
            "deps": "2.0",
            "notes": "Side-by-side gap evidence for executives",
        },
        {
            "wbs": "2.3",
            "phase": "Requirements",
            "ws": "Enhancements",
            "task": "Enhancement backlog — 'promised never delivered' + wishes",
            "owner": "BA / Gov",
            "start": date(2026, 4, 8),
            "end": date(2026, 5, 9),
            "pct": 0,
            "status": "Not started",
            "deps": "2.1",
            "notes": "Separate from MVP parity; Phase 2/3",
        },
        {
            "wbs": "2.4",
            "phase": "Requirements",
            "ws": "OMS leverage",
            "task": "OMS capability matrix & requirements→OMS mapping",
            "owner": "BA / OMS liaison",
            "start": date(2026, 4, 15),
            "end": date(2026, 5, 16),
            "pct": 0,
            "status": "Not started",
            "deps": "2.2",
            "notes": "Align to Disney OMS roadmap",
        },
        {
            "wbs": "2.5",
            "phase": "Requirements",
            "ws": "Gaps",
            "task": "Prioritized gap matrix & build scope (H/M/L criticality)",
            "owner": "BA / Gov",
            "start": date(2026, 4, 22),
            "end": date(2026, 5, 23),
            "pct": 0,
            "status": "Not started",
            "deps": "2.4",
            "notes": "MVP = critical business metadata parity",
        },
        {
            "wbs": "2.6",
            "phase": "Requirements",
            "ws": "Sign-off",
            "task": "Consolidated requirements package & governance sign-off",
            "owner": "Data Governance",
            "start": date(2026, 5, 10),
            "end": date(2026, 5, 30),
            "pct": 0,
            "status": "Not started",
            "deps": "2.5",
            "notes": "Gate before detailed design",
        },
        # Design
        {
            "wbs": "3.0",
            "phase": "Design & Architecture",
            "ws": "Architecture",
            "task": "Target data model — glossary, tags, custom fields, stewardship",
            "owner": "Architect / OMS",
            "start": date(2026, 6, 1),
            "end": date(2026, 6, 28),
            "pct": 0,
            "status": "Not started",
            "deps": "2.6",
            "notes": "Business metadata in OMS",
        },
        {
            "wbs": "3.1",
            "phase": "Design & Architecture",
            "ws": "Integration",
            "task": "Integration design — ingestion, lineage, APIs, Airflow links",
            "owner": "Eng / OMS",
            "start": date(2026, 6, 8),
            "end": date(2026, 7, 12),
            "pct": 0,
            "status": "Not started",
            "deps": "3.0",
            "notes": "Population of 'Not Available' fields where applicable",
        },
        {
            "wbs": "3.2",
            "phase": "Design & Architecture",
            "ws": "UX",
            "task": "UI/UX design (OMS design system) — search, glossary, detail pages",
            "owner": "UX / OMS",
            "start": date(2026, 6, 15),
            "end": date(2026, 7, 19),
            "pct": 0,
            "status": "Not started",
            "deps": "3.0",
            "notes": "Discovery & stewardship flows",
        },
        {
            "wbs": "3.3",
            "phase": "Design & Architecture",
            "ws": "Migration",
            "task": "Migration design — ETL mapping Alation→OMS, validation approach",
            "owner": "Eng",
            "start": date(2026, 6, 22),
            "end": date(2026, 7, 26),
            "pct": 0,
            "status": "Not started",
            "deps": "3.0",
            "notes": "Metadata-first; ≥95% preservation target",
        },
        {
            "wbs": "3.4",
            "phase": "Design & Architecture",
            "ws": "Sign-off",
            "task": "Architecture & design review — approved for build",
            "owner": "Steering",
            "start": date(2026, 7, 20),
            "end": date(2026, 7, 31),
            "pct": 0,
            "status": "Not started",
            "deps": "3.1,3.2,3.3",
            "notes": "Formal gate",
        },
        # Build MVP
        {
            "wbs": "4.0",
            "phase": "Build — MVP",
            "ws": "Core",
            "task": "OMS MVP: glossary & business metadata model (implement)",
            "owner": "OMS / DSS Eng",
            "start": date(2026, 6, 15),
            "end": date(2026, 8, 30),
            "pct": 0,
            "status": "Not started",
            "deps": "3.4",
            "notes": "Terms, definitions, stewardship",
        },
        {
            "wbs": "4.1",
            "phase": "Build — MVP",
            "ws": "Discovery",
            "task": "OMS MVP: business-context search & discovery",
            "owner": "OMS / DSS Eng",
            "start": date(2026, 7, 1),
            "end": date(2026, 9, 13),
            "pct": 0,
            "status": "Not started",
            "deps": "4.0",
            "notes": "Glossary, articles, catalog objects",
        },
        {
            "wbs": "4.2",
            "phase": "Build — MVP",
            "ws": "Metadata",
            "task": "OMS MVP: documentation, business description, tags on assets",
            "owner": "OMS / DSS Eng",
            "start": date(2026, 7, 15),
            "end": date(2026, 9, 27),
            "pct": 0,
            "status": "Not started",
            "deps": "4.0",
            "notes": "Populate placeholders",
        },
        {
            "wbs": "4.3",
            "phase": "Build — MVP",
            "ws": "Lineage",
            "task": "OMS MVP: lineage depth + Airflow DAG/task link population",
            "owner": "OMS / DSS Eng",
            "start": date(2026, 8, 1),
            "end": date(2026, 10, 4),
            "pct": 0,
            "status": "Not started",
            "deps": "3.1",
            "notes": "Table/column per roadmap",
        },
        {
            "wbs": "4.4",
            "phase": "Build — MVP",
            "ws": "Usage",
            "task": "OMS MVP: usage metrics (last access, top users) where supported",
            "owner": "OMS / DSS Eng",
            "start": date(2026, 8, 15),
            "end": date(2026, 10, 11),
            "pct": 0,
            "status": "Not started",
            "deps": "4.2",
            "notes": "Ownership / created-by fields",
        },
        {
            "wbs": "4.5",
            "phase": "Build — MVP",
            "ws": "QA",
            "task": "MVP UAT, hardening, performance — governance acceptance",
            "owner": "Gov / QA",
            "start": date(2026, 9, 15),
            "end": date(2026, 10, 18),
            "pct": 0,
            "status": "Not started",
            "deps": "4.1,4.2,4.3",
            "notes": "Success metrics baseline",
        },
        # Full parity (Phase 2) — overlaps post-MVP per plan
        {
            "wbs": "5.0",
            "phase": "Build — Full parity",
            "ws": "Workflows",
            "task": "Full parity: custom fields, governance workflows, policy/compliance UI",
            "owner": "OMS / DSS Eng",
            "start": date(2026, 10, 15),
            "end": date(2027, 1, 15),
            "pct": 0,
            "status": "Not started",
            "deps": "4.5",
            "notes": "Policy center analog; integrations",
        },
        # Migration
        {
            "wbs": "6.0",
            "phase": "Migration",
            "ws": "Planning",
            "task": "Migration runbook, environments, rollback, validation checkpoints",
            "owner": "Eng / PMO",
            "start": date(2026, 7, 1),
            "end": date(2026, 8, 15),
            "pct": 0,
            "status": "Not started",
            "deps": "3.3",
            "notes": "Industry: 3–6 mo execution window",
        },
        {
            "wbs": "6.1",
            "phase": "Migration",
            "ws": "Extract",
            "task": "Build/run extraction — Alation (glossary, articles, tags, lineage, CF)",
            "owner": "Eng",
            "start": date(2026, 8, 1),
            "end": date(2026, 9, 30),
            "pct": 0,
            "status": "Not started",
            "deps": "6.0",
            "notes": "Secure export before contract risk",
        },
        {
            "wbs": "6.2",
            "phase": "Migration",
            "ws": "Transform",
            "task": "Transform & map to OMS schema; reconciliation tooling",
            "owner": "Eng",
            "start": date(2026, 9, 1),
            "end": date(2026, 11, 15),
            "pct": 0,
            "status": "Not started",
            "deps": "6.1,4.0",
            "notes": "Data fidelity > speed",
        },
        {
            "wbs": "6.3",
            "phase": "Migration",
            "ws": "Parallel run",
            "task": "Parallel run — Alation + OMS (user validation)",
            "owner": "PMO / Gov",
            "start": date(2026, 10, 1),
            "end": date(2027, 1, 15),
            "pct": 0,
            "status": "Not started",
            "deps": "4.5",
            "notes": "Reduces incident risk vs big-bang",
        },
        {
            "wbs": "6.4",
            "phase": "Migration",
            "ws": "Load",
            "task": "Phased load to OMS, validation reports, lineage checks",
            "owner": "Eng / Gov",
            "start": date(2026, 11, 1),
            "end": date(2027, 2, 15),
            "pct": 0,
            "status": "Not started",
            "deps": "6.2",
            "notes": "≥95% business metadata preserved",
        },
        # Change & training
        {
            "wbs": "7.0",
            "phase": "Change & Training",
            "ws": "Materials",
            "task": "Training curriculum, quick guides, videos, FAQs (vs Alation)",
            "owner": "Gov / BA",
            "start": date(2026, 12, 1),
            "end": date(2027, 1, 31),
            "pct": 0,
            "status": "Not started",
            "deps": "4.5",
            "notes": "Role-based: stewards, analysts, gov, engineers",
        },
        {
            "wbs": "7.1",
            "phase": "Change & Training",
            "ws": "Delivery",
            "task": "Workshops, champions program, office hours (2–4 wk post cutover)",
            "owner": "Gov",
            "start": date(2027, 1, 15),
            "end": date(2027, 3, 15),
            "pct": 0,
            "status": "Not started",
            "deps": "7.0",
            "notes": "Adoption metrics; survey loop",
        },
        # Cutover
        {
            "wbs": "8.0",
            "phase": "Cutover & Close",
            "ws": "Cutover",
            "task": "Production cutover — OMS primary; Alation read-only",
            "owner": "Steering / Eng",
            "start": date(2027, 2, 15),
            "end": date(2027, 3, 15),
            "pct": 0,
            "status": "Not started",
            "deps": "6.4,7.1",
            "notes": "Rollback plan documented",
        },
        {
            "wbs": "8.1",
            "phase": "Cutover & Close",
            "ws": "Milestone",
            "task": "MILESTONE: Alation baseline contract end (if no extension)",
            "owner": "—",
            "start": date(2026, 10, 1),
            "end": date(2026, 10, 1),
            "pct": 0,
            "status": "Milestone",
            "deps": "—",
            "notes": "Oct 1, 2026 — extension strongly recommended per program plan",
        },
        {
            "wbs": "8.2",
            "phase": "Cutover & Close",
            "ws": "Decommission",
            "task": "Alation decommission, archive, final audit evidence",
            "owner": "Eng / Gov",
            "start": date(2027, 9, 1),
            "end": date(2027, 10, 1),
            "pct": 0,
            "status": "Not started",
            "deps": "8.0",
            "notes": "Align to extended contract Oct 2027",
        },
        {
            "wbs": "9.0",
            "phase": "Program & Governance",
            "ws": "Metrics",
            "task": "Success metrics dashboard — WAU, glossary coverage, search success",
            "owner": "Gov / PMO",
            "start": date(2026, 6, 1),
            "end": date(2027, 4, 30),
            "pct": 0,
            "status": "Not started",
            "deps": "1.1",
            "notes": "Steward activity; migration validation summary",
        },
    ]

    return tasks, months


def build_excel_workbook(tasks: list[dict], months: list[tuple[int, int]]) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Executive Gantt"

    n_meta_cols = 11
    last_col = n_meta_cols + len(months)

    # --- Title block ---
    title = (
        "Business Data Catalog — In-House (OMS) & Alation Migration  |  "
        "Disney Streaming Services  |  Executive Program Gantt"
    )
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=last_col)
    c1 = ws.cell(1, 1, title)
    c1.font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    c1.fill = PatternFill("solid", fgColor="1B365D")
    c1.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 36

    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=last_col)
    sub = (
        "Sources: Product Brief & Migration Project Plan (Mar 2026)  •  "
        "Baseline Alation contract end: 1-Oct-2026  •  "
        "Recommended: extension + cutover Feb–Mar 2027  •  Decommission Oct 2027"
    )
    c2 = ws.cell(2, 1, sub)
    c2.font = Font(name="Calibri", size=11, italic=True, color="E2E8F0")
    c2.fill = PatternFill("solid", fgColor="334155")
    c2.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[2].height = 30

    # Legend row 3
    ws.row_dimensions[3].height = 22
    ws.cell(3, 1, "Phase legend (timeline bar colors):").font = Font(bold=True, size=10)
    col_leg = 2
    for phase, (dark, light) in PHASE_STYLES.items():
        if col_leg > last_col - 2:
            break
        cell = ws.cell(3, col_leg, phase[:22] + ("…" if len(phase) > 22 else ""))
        cell.fill = PatternFill("solid", fgColor=light)
        cell.font = Font(size=9, bold=True, color="1E293B")
        cell.border = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
        col_leg += 3

    # Header row 5
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
    ]
    header_row = 5
    for col, h in enumerate(headers, 1):
        cell = ws.cell(header_row, col, h)
        cell.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="0F172A")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

    for i, (y, m) in enumerate(months):
        col = n_meta_cols + 1 + i
        label = date(y, m, 1).strftime("%b-%y")
        cell = ws.cell(header_row, col, label)
        cell.font = Font(size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="475569")
        cell.alignment = Alignment(horizontal="center", vertical="center", text_rotation=45)
        cell.border = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

    ws.row_dimensions[header_row].height = 44

    # Data rows
    data_start = header_row + 1
    for i, t in enumerate(tasks):
        r = data_start + i
        dur = max(0, (t["end"] - t["start"]).days) // 7
        if (t["end"] - t["start"]).days > 0 and dur == 0:
            dur = 1

        row_vals = [
            t["wbs"],
            t["phase"],
            t["ws"],
            t["task"],
            t["owner"],
            t["start"],
            t["end"],
            dur,
            t["pct"] / 100.0,
            t["status"],
            t["notes"],
        ]
        phase = t["phase"]
        _, light = PHASE_STYLES.get(phase, ("64748B", "F1F5F9"))

        for c_idx, val in enumerate(row_vals, 1):
            cell = ws.cell(r, c_idx, val)
            cell.border = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            if c_idx in (6, 7):
                cell.number_format = "mmm d, yyyy"
            if c_idx == 9:
                cell.number_format = "0%"
            if c_idx <= 4:
                cell.font = Font(bold=(c_idx == 1))
            if c_idx == 4 and t.get("task", "").startswith("MILESTONE"):
                cell.font = Font(bold=True, color="B45309")

        for j, (y, m) in enumerate(months):
            col = n_meta_cols + 1 + j
            ms, me = month_bounds(y, m)
            cell = ws.cell(r, col)
            cell.border = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
            if overlaps(t["start"], t["end"], ms, me):
                cell.fill = PatternFill("solid", fgColor=light)
                if t.get("task", "").startswith("MILESTONE"):
                    cell.fill = PatternFill("solid", fgColor="F59E0B")
                    cell.value = "◆"
                    cell.font = Font(bold=True, color="78350F")
                    cell.alignment = Alignment(horizontal="center", vertical="center")

        if i % 2 == 1:
            for c_idx in range(1, n_meta_cols + 1):
                ws.cell(r, c_idx).fill = PatternFill("solid", fgColor="F8FAFC")

    # Column widths
    widths = [6, 22, 14, 52, 18, 12, 12, 10, 10, 14, 38]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for j in range(len(months)):
        ws.column_dimensions[get_column_letter(n_meta_cols + 1 + j)].width = 3.2

    ws.freeze_panes = ws.cell(data_start, n_meta_cols + 1)

    # Status dropdown
    dv = DataValidation(
        type="list",
        formula1='"Not started,In progress,At risk,Blocked,Complete,Milestone"',
        allow_blank=True,
    )
    dv.add(f"{get_column_letter(10)}{data_start}:{get_column_letter(10)}{data_start + len(tasks) - 1}")
    ws.add_data_validation(dv)

    # --- Sheet 2: Milestones ---
    mws = wb.create_sheet("Milestones & KPIs", 1)
    mws.merge_cells("A1:D1")
    t1 = mws.cell(1, 1, "Key milestones & success criteria (from program documents)")
    t1.font = Font(size=14, bold=True, color="FFFFFF")
    t1.fill = PatternFill("solid", fgColor="1B365D")
    t1.alignment = Alignment(horizontal="center")

    milestones = [
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
    for ri, row in enumerate(milestones, 2):
        for ci, val in enumerate(row, 1):
            c = mws.cell(ri, ci, val)
            c.border = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            if ri == 2:
                c.font = Font(bold=True, color="FFFFFF")
                c.fill = PatternFill("solid", fgColor="334155")
            elif ri % 2 == 0:
                c.fill = PatternFill("solid", fgColor="F8FAFC")

    mws.column_dimensions["A"].width = 28
    mws.column_dimensions["B"].width = 22
    mws.column_dimensions["C"].width = 20
    mws.column_dimensions["D"].width = 70

    # --- Sheet 3: How to open in Google Sheets ---
    iws = wb.create_sheet("Open in Google Sheets", 2)
    iws.merge_cells("A1:B1")
    h = iws.cell(1, 1, "Using this file in Google Drive / Google Sheets")
    h.font = Font(size=14, bold=True, color="FFFFFF")
    h.fill = PatternFill("solid", fgColor="1B365D")
    h.alignment = Alignment(horizontal="left", indent=1, vertical="center")
    iws.row_dimensions[1].height = 28

    steps = [
        (
            "1. Upload",
            "In Google Drive (your program folder), click New → File upload and select this .xlsx, "
            "or drag the file into the folder.",
        ),
        (
            "2. Open as Sheet",
            "Right-click the file → Open with → Google Sheets. Sheets will convert formatting; "
            "review column widths and frozen panes (View → Freeze).",
        ),
        (
            "3. Executive view",
            "Hide the month columns you do not need yet, or create a Filter view for leadership "
            "with only WBS, Phase, Task, Status, and End date visible.",
        ),
        (
            "4. Maintain",
            "Update % Complete and Status weekly; adjust Start/End if dependencies slip. "
            "Regenerate from generate_executive_gantt.py if you need a full task reset.",
        ),
        (
            "5. Source docs",
            "Aligned to your Product Brief, Migration Project Plan, and appendix timeline "
            "(extension scenario to Oct 2027). Milestone 1-Oct-2026 is the baseline contract date.",
        ),
    ]
    for ri, (title, body) in enumerate(steps, 3):
        iws.cell(ri, 1, title).font = Font(bold=True, size=11)
        iws.cell(ri, 1).alignment = Alignment(wrap_text=True, vertical="top")
        iws.cell(ri, 2, body).alignment = Alignment(wrap_text=True, vertical="top")
        iws.row_dimensions[ri].height = max(36, len(body) // 80 * 14 + 24)
    iws.column_dimensions["A"].width = 16
    iws.column_dimensions["B"].width = 88

    wb.save(OUTPUT)
    print(f"Wrote {OUTPUT}")


def main() -> None:
    tasks, months = get_program_tasks_and_months()
    build_excel_workbook(tasks, months)


if __name__ == "__main__":
    main()
