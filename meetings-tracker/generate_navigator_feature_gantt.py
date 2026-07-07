#!/usr/bin/env python3
"""
Generate an executive weekly Gantt for Business Data Catalog
feature build — Kronos-style layout with Business-Data-Catalog-Migration-Executive-Gantt
phase colors.

Timeline: Roadmap slide (Jun 2026 kickoff → May 2027 launch).
Features: Business Data Catalog Feature Inventory Matrix (Google Doc) + intake deck P1/P2 scope.

Run:
  python3 meetings-tracker/generate_navigator_feature_gantt.py
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUTPUT = (
    Path(__file__).resolve().parent.parent
    / "Business-Data-Catalog-Feature-Build-Executive-Gantt.xlsx"
)

# Title bands — Kronos / Sisu executive pattern
TITLE_BAND_1 = PatternFill("solid", fgColor="1B365D")
TITLE_BAND_2 = PatternFill("solid", fgColor="334155")
TITLE_BAND_3 = PatternFill("solid", fgColor="E2E8F0")
HEADER_FILL = PatternFill("solid", fgColor="1B365D")
HEADER_FONT = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
TITLE_FONT = Font(name="Calibri", size=22, bold=True, color="FFFFFF")
SUBTITLE_ON_BAND = Font(name="Calibri", size=11, color="E2E8F0")
META_ON_BAND_LIGHT = Font(name="Calibri", size=10, italic=True, color="334155")
BODY_FONT = Font(name="Calibri", size=10, color="1F2937")
META_FONT = Font(name="Calibri", size=9, italic=True, color="64748B")
SECTION_FONT = Font(name="Calibri", size=10, bold=True, color="1B365D")
THIN = Side(style="thin", color="CBD5E1")
GRID_BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

ZEBRA: tuple[PatternFill, PatternFill] = (
    PatternFill("solid", fgColor="F8FAFC"),
    PatternFill("solid", fgColor="F1F5F9"),
)

# Bar colors — light tints from Business-Data-Catalog-Migration-Executive-Gantt PHASE_STYLES
PHASE_BAR: dict[str, str] = {
    "Program & Governance": "B8D4F0",
    "Requirements": "BFDBFE",
    "Design & Architecture": "DDD6FE",
    "Build — MVP (P1)": "A7F3D0",
    "Build — MVP (P2)": "6EE7B7",
    "Build — OMS leverage": "E5E7EB",
    "Testing & QA": "A5F3FC",
    "Migration": "FDE68A",
    "Cutover & Close": "FECACA",
}

# --- Roadmap dates (deck + screenshot: kickoff Jun 1 2026, launch May 1 2027) ---
KICKOFF = date(2026, 6, 1)
LAUNCH = date(2027, 5, 1)

PHASE_REQ_START = date(2026, 6, 1)
PHASE_REQ_END = date(2026, 7, 26)  # 8 weeks

PHASE_DESIGN_START = date(2026, 8, 3)
PHASE_DESIGN_END = date(2026, 10, 11)  # 10 weeks (Aug–Oct)

PHASE_BUILD_START = date(2026, 10, 12)
PHASE_BUILD_END = date(2027, 1, 10)  # 13 weeks (Oct–Jan)

PHASE_TEST_START = date(2027, 1, 11)
PHASE_TEST_END = date(2027, 2, 7)  # 4 weeks

PHASE_MIG_START = date(2027, 3, 1)
PHASE_MIG_END = date(2027, 4, 11)  # 6 weeks (Mar–Apr)


def monday_on_or_before(d: date) -> date:
    return d - timedelta(days=d.weekday())


def week_end(week_start: date) -> date:
    return week_start + timedelta(days=6)


def overlaps(ts: date, te: date, ws: date, we: date) -> bool:
    return not (te < ws or ts > we)


def get_tasks() -> list[dict]:
    """Program phases + per-feature design / build / test / migration rows."""
    return [
        # --- Program spine ---
        {
            "id": "—",
            "phase": "Program & Governance",
            "priority": "—",
            "feature": "▸ PROGRAM PHASE: Requirements gathering (8 wks · Q2–Q3 FY26)",
            "prd": "—",
            "start": PHASE_REQ_START,
            "end": PHASE_REQ_END,
            "bucket": "Program & Governance",
            "section": True,
        },
        {
            "id": "R1",
            "phase": "Requirements",
            "priority": "All",
            "feature": "Feature inventory validation & stakeholder interviews (matrix sign-off)",
            "prd": "Doc",
            "start": date(2026, 6, 1),
            "end": date(2026, 6, 28),
            "bucket": "Requirements",
        },
        {
            "id": "R2",
            "phase": "Requirements",
            "priority": "All",
            "feature": "Persona stories & acceptance criteria (consumer, steward, compliance)",
            "prd": "Intake",
            "start": date(2026, 6, 8),
            "end": date(2026, 7, 12),
            "bucket": "Requirements",
        },
        {
            "id": "R3",
            "phase": "Requirements",
            "priority": "All",
            "feature": "OMS capability mapping, gap analysis & migration field mapping",
            "prd": "Brief",
            "start": date(2026, 6, 15),
            "end": date(2026, 7, 19),
            "bucket": "Requirements",
        },
        {
            "id": "R4",
            "phase": "Requirements",
            "priority": "All",
            "feature": "Consolidated requirements package & governance gate",
            "prd": "—",
            "start": date(2026, 7, 13),
            "end": PHASE_REQ_END,
            "bucket": "Requirements",
        },
        {
            "id": "—",
            "phase": "Program & Governance",
            "priority": "—",
            "feature": "▸ PROGRAM PHASE: Solution design — backend + frontend (10 wks · Q3 FY26)",
            "prd": "—",
            "start": PHASE_DESIGN_START,
            "end": PHASE_DESIGN_END,
            "bucket": "Program & Governance",
            "section": True,
        },
        {
            "id": "D0",
            "phase": "Design & Architecture",
            "priority": "All",
            "feature": "Business Data Catalog shell, IA & OMS handoff patterns (Open in OMS, role-aware nav)",
            "prd": "F30",
            "start": PHASE_DESIGN_START,
            "end": date(2026, 9, 6),
            "bucket": "Design & Architecture",
        },
        {
            "id": "—",
            "phase": "Program & Governance",
            "priority": "—",
            "feature": "▸ PROGRAM PHASE: MVP development (13 wks · Q3–Q4 FY26 → Q1 FY27)",
            "prd": "—",
            "start": PHASE_BUILD_START,
            "end": PHASE_BUILD_END,
            "bucket": "Program & Governance",
            "section": True,
        },
        # --- P1 features (deck) ---
        {
            "id": "F01",
            "phase": "Design & Architecture",
            "priority": "P1",
            "feature": "Search & Discovery — UX, filters, semantic/keyword search API contract",
            "prd": "F01",
            "start": date(2026, 8, 10),
            "end": date(2026, 9, 20),
            "bucket": "Design & Architecture",
        },
        {
            "id": "F01",
            "phase": "Build — MVP (P1)",
            "priority": "P1",
            "feature": "Search & Discovery — global search, AI-assisted results, natural language",
            "prd": "F01",
            "start": date(2026, 10, 12),
            "end": date(2026, 11, 15),
            "bucket": "Build — MVP (P1)",
        },
        {
            "id": "F02",
            "phase": "Design & Architecture",
            "priority": "P1",
            "feature": "Business Glossary — term model, BU folders, synonym & stewardship UX",
            "prd": "F02",
            "start": date(2026, 8, 17),
            "end": date(2026, 9, 27),
            "bucket": "Design & Architecture",
        },
        {
            "id": "F02",
            "phase": "Build — MVP (P1)",
            "priority": "P1",
            "feature": "Business Glossary — browse, search terms, link to catalog assets, RBAC",
            "prd": "F02",
            "start": date(2026, 10, 19),
            "end": date(2026, 12, 6),
            "bucket": "Build — MVP (P1)",
        },
        {
            "id": "F03",
            "phase": "Design & Architecture",
            "priority": "P1",
            "feature": "Catalog Browse — datasource → schema → table hierarchy & navigation",
            "prd": "F03",
            "start": date(2026, 8, 24),
            "end": date(2026, 10, 4),
            "bucket": "Design & Architecture",
        },
        {
            "id": "F03",
            "phase": "Build — MVP (P1)",
            "priority": "P1",
            "feature": "Catalog Browse — hierarchical explore, asset-type filters",
            "prd": "F03",
            "start": date(2026, 10, 12),
            "end": date(2026, 11, 22),
            "bucket": "Build — MVP (P1)",
        },
        {
            "id": "F04",
            "phase": "Design & Architecture",
            "priority": "P1",
            "feature": "Asset Detail / Descriptions — table & column detail, owners, classifications",
            "prd": "F04",
            "start": date(2026, 9, 1),
            "end": date(2026, 10, 11),
            "bucket": "Design & Architecture",
        },
        {
            "id": "F04",
            "phase": "Build — MVP (P1)",
            "priority": "P1",
            "feature": "Asset Detail / Descriptions — business + technical fields, provenance badges",
            "prd": "F04",
            "start": date(2026, 11, 3),
            "end": date(2026, 12, 20),
            "bucket": "Build — MVP (P1)",
        },
        {
            "id": "F14",
            "phase": "Design & Architecture",
            "priority": "P1",
            "feature": "API & integrations — read API, migration bulk ops, BI tool hooks",
            "prd": "F14",
            "start": date(2026, 9, 8),
            "end": date(2026, 10, 11),
            "bucket": "Design & Architecture",
        },
        {
            "id": "F14",
            "phase": "Build — MVP (P1)",
            "priority": "P1",
            "feature": "API integrations for migration — Alation extract, OMS load, validation jobs",
            "prd": "F14",
            "start": date(2026, 11, 17),
            "end": date(2027, 1, 10),
            "bucket": "Build — MVP (P1)",
        },
        # --- P2 features (deck) ---
        {
            "id": "F09",
            "phase": "Design & Architecture",
            "priority": "P2",
            "feature": "Ownership / Stewardship — assign owners, stewards, escalation paths",
            "prd": "F09",
            "start": date(2026, 9, 15),
            "end": date(2026, 10, 11),
            "bucket": "Design & Architecture",
        },
        {
            "id": "F09",
            "phase": "Build — MVP (P2)",
            "priority": "P2",
            "feature": "Ownership / Stewardship — thin endorse/reconcile in Business Data Catalog",
            "prd": "F09",
            "start": date(2026, 12, 1),
            "end": date(2027, 1, 3),
            "bucket": "Build — MVP (P2)",
        },
        {
            "id": "AC",
            "phase": "Design & Architecture",
            "priority": "P2",
            "feature": "Access Controls — feature-based permission postures (glossary, metrics, audit)",
            "prd": "RBAC",
            "start": date(2026, 9, 22),
            "end": date(2026, 10, 11),
            "bucket": "Design & Architecture",
        },
        {
            "id": "AC",
            "phase": "Build — MVP (P2)",
            "priority": "P2",
            "feature": "Access Controls — role-aware views & admin policy configuration",
            "prd": "RBAC",
            "start": date(2026, 12, 8),
            "end": date(2027, 1, 10),
            "bucket": "Build — MVP (P2)",
        },
        {
            "id": "F21",
            "phase": "Design & Architecture",
            "priority": "P2",
            "feature": "Flags — endorsements, warnings, deprecations, popularity signals",
            "prd": "F21",
            "start": date(2026, 9, 29),
            "end": date(2026, 10, 11),
            "bucket": "Design & Architecture",
        },
        {
            "id": "F21",
            "phase": "Build — MVP (P2)",
            "priority": "P2",
            "feature": "Flags — trusted / deprecated / warning badges on asset surfaces",
            "prd": "F21",
            "start": date(2026, 12, 15),
            "end": date(2027, 1, 10),
            "bucket": "Build — MVP (P2)",
        },
        # --- Additional MVP from feature matrix (parallel / OMS leverage) ---
        {
            "id": "F16",
            "phase": "Build — MVP (P1)",
            "priority": "MVP",
            "feature": "Asset detail automation — AI description suggestions (human endorsement gate)",
            "prd": "F16",
            "start": date(2026, 12, 1),
            "end": date(2027, 1, 10),
            "bucket": "Build — MVP (P1)",
        },
        {
            "id": "F06",
            "phase": "Build — MVP (P2)",
            "priority": "High",
            "feature": "Tags & Classification — read filters; tag assignment where OMS supports edit",
            "prd": "F06",
            "start": date(2026, 11, 24),
            "end": date(2027, 1, 10),
            "bucket": "Build — MVP (P2)",
        },
        {
            "id": "F23",
            "phase": "Build — MVP (P1)",
            "priority": "MVP",
            "feature": "Folders / source navigation — article hierarchy & content organization",
            "prd": "F23",
            "start": date(2026, 11, 10),
            "end": date(2026, 12, 27),
            "bucket": "Build — MVP (P1)",
        },
        {
            "id": "F05",
            "phase": "Build — OMS leverage",
            "priority": "MVP",
            "feature": "Data Lineage — deep link & embed from OMS (table / column level)",
            "prd": "F05",
            "start": date(2026, 10, 26),
            "end": date(2026, 12, 6),
            "bucket": "Build — OMS leverage",
        },
        {
            "id": "F20",
            "phase": "Build — OMS leverage",
            "priority": "MVP",
            "feature": "Authentication / SSO — enterprise SSO & role integration (OMS baseline)",
            "prd": "F20",
            "start": date(2026, 10, 12),
            "end": date(2026, 11, 1),
            "bucket": "Build — OMS leverage",
        },
        {
            "id": "F11",
            "phase": "Build — OMS leverage",
            "priority": "MVP",
            "feature": "Data Sources & Connectors — critical datasource coverage via OMS / 626",
            "prd": "F11",
            "start": date(2026, 10, 19),
            "end": date(2026, 12, 13),
            "bucket": "Build — OMS leverage",
        },
        {
            "id": "DD",
            "phase": "Build — MVP (P1)",
            "priority": "MVP",
            "feature": "Data Dictionary — steward workflows, privacy tags, CDE surfacing",
            "prd": "DD",
            "start": date(2026, 11, 17),
            "end": date(2027, 1, 10),
            "bucket": "Build — MVP (P1)",
        },
        # --- Test / migrate / launch ---
        {
            "id": "—",
            "phase": "Program & Governance",
            "priority": "—",
            "feature": "▸ PROGRAM PHASE: Testing (4 wks · Q1 FY27)",
            "prd": "—",
            "start": PHASE_TEST_START,
            "end": PHASE_TEST_END,
            "bucket": "Program & Governance",
            "section": True,
        },
        {
            "id": "T1",
            "phase": "Testing & QA",
            "priority": "All",
            "feature": "Feature QA — P1 discovery flows (search, browse, glossary, detail)",
            "prd": "P1",
            "start": PHASE_TEST_START,
            "end": date(2027, 1, 24),
            "bucket": "Testing & QA",
        },
        {
            "id": "T2",
            "phase": "Testing & QA",
            "priority": "All",
            "feature": "Feature QA — P2 governance signals (stewardship, flags, access)",
            "prd": "P2",
            "start": date(2027, 1, 18),
            "end": PHASE_TEST_END,
            "bucket": "Testing & QA",
        },
        {
            "id": "T3",
            "phase": "Testing & QA",
            "priority": "All",
            "feature": "Regression, migration validation & performance testing",
            "prd": "—",
            "start": date(2027, 1, 25),
            "end": PHASE_TEST_END,
            "bucket": "Testing & QA",
        },
        {
            "id": "—",
            "phase": "Program & Governance",
            "priority": "—",
            "feature": "▸ PROGRAM PHASE: Migration + UAT + stabilization (6 wks · Q1–Q2 FY27)",
            "prd": "—",
            "start": PHASE_MIG_START,
            "end": PHASE_MIG_END,
            "bucket": "Program & Governance",
            "section": True,
        },
        {
            "id": "M1",
            "phase": "Migration",
            "priority": "All",
            "feature": "Alation → OMS metadata load — glossary, articles, endorsements, tags",
            "prd": "F14",
            "start": PHASE_MIG_START,
            "end": date(2027, 3, 21),
            "bucket": "Migration",
        },
        {
            "id": "M2",
            "phase": "Migration",
            "priority": "All",
            "feature": "Parallel run & steward UAT — link integrity, search parity checks",
            "prd": "—",
            "start": date(2027, 3, 15),
            "end": date(2027, 4, 4),
            "bucket": "Migration",
        },
        {
            "id": "M3",
            "phase": "Migration",
            "priority": "All",
            "feature": "Stabilization, defect burn-down & cutover readiness",
            "prd": "—",
            "start": date(2027, 3, 29),
            "end": PHASE_MIG_END,
            "bucket": "Migration",
        },
        {
            "id": "—",
            "phase": "Program & Governance",
            "priority": "—",
            "feature": "▸ LAUNCH — Business Data Catalog go-live",
            "prd": "—",
            "start": LAUNCH,
            "end": LAUNCH,
            "bucket": "Cutover & Close",
            "section": True,
        },
    ]


def build_workbook(tasks: list[dict]) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Feature Build Gantt"

    grid_start = monday_on_or_before(min(t["start"] for t in tasks))
    grid_end = max(t["end"] for t in tasks)
    grid_end_monday = monday_on_or_before(grid_end) + timedelta(weeks=2)

    week_starts: list[date] = []
    cur = grid_start
    while cur <= grid_end_monday:
        week_starts.append(cur)
        cur += timedelta(weeks=1)

    labels = ["ID", "Phase", "Priority", "Feature / deliverable", "PRD", "Start", "End"]
    first_week_col = len(labels) + 1
    ncols = len(labels) + len(week_starts)
    last_letter = get_column_letter(ncols)

    # Title block
    ws.merge_cells(f"A1:{last_letter}1")
    c1 = ws["A1"]
    c1.value = "Business Data Catalog — Feature Build Gantt"
    c1.font = TITLE_FONT
    c1.fill = TITLE_BAND_1
    c1.alignment = Alignment(horizontal="left", vertical="center", indent=1, wrap_text=True)
    ws.row_dimensions[1].height = 44

    ws.merge_cells(f"A2:{last_letter}2")
    c2 = ws["A2"]
    c2.value = (
        "Roadmap: 2027  |  "
        "Kickoff Jun 1, 2026  ·  Launch May 1, 2027  ·  "
        "41 weeks program  |  Team: OMS (Madhuri + 4) + BDC (4 eng)"
    )
    c2.font = SUBTITLE_ON_BAND
    c2.fill = TITLE_BAND_2
    c2.alignment = Alignment(horizontal="left", vertical="center", indent=1, wrap_text=True)
    ws.row_dimensions[2].height = 24

    ws.merge_cells(f"A3:{last_letter}3")
    c3 = ws["A3"]
    c3.value = (
        "Sources: Data Catalog deck (1OdzAIMxb2gE4n36-8UoYhWXWg-4nzVF4m3i8V9XWYRw)  ·  "
        "Business Data Catalog Feature Inventory Matrix (Mar 2026)  ·  "
        "P1: Search, Glossary, Browse, Detail, API/migration  ·  "
        "P2: Stewardship, Access, Flags"
    )
    c3.font = META_ON_BAND_LIGHT
    c3.fill = TITLE_BAND_3
    c3.alignment = Alignment(horizontal="left", vertical="center", indent=1, wrap_text=True)
    ws.row_dimensions[3].height = 22

    header_row = 5
    for col, label in enumerate(labels, start=1):
        cell = ws.cell(row=header_row, column=col, value=label)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = GRID_BORDER

    for i, wk in enumerate(week_starts):
        col = first_week_col + i
        cell = ws.cell(row=header_row, column=col, value=wk)
        cell.number_format = "mmm d"
        cell.font = Font(name="Calibri", size=8, bold=True, color="FFFFFF")
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", text_rotation=45)
        cell.border = GRID_BORDER
    ws.row_dimensions[header_row].height = 54

    data_start = header_row + 1
    for idx, task in enumerate(tasks):
        r = data_start + idx
        is_section = task.get("section", False)
        base_fill = PatternFill("solid", fgColor="E2E8F0") if is_section else ZEBRA[idx % 2]
        row_font = SECTION_FONT if is_section else BODY_FONT

        values = [
            task["id"],
            task["phase"],
            task["priority"],
            task["feature"],
            task["prd"],
            task["start"],
            task["end"],
        ]
        for col_idx, val in enumerate(values, start=1):
            cell = ws.cell(row=r, column=col_idx, value=val)
            cell.font = row_font
            cell.fill = base_fill
            cell.border = GRID_BORDER
            if col_idx in (6, 7) and isinstance(val, date):
                cell.number_format = "mmm d, yyyy"
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif col_idx == 4:
                cell.alignment = Alignment(vertical="top", wrap_text=True)
            else:
                cell.alignment = Alignment(vertical="top", wrap_text=True)

        bar_color = PHASE_BAR.get(task["bucket"], "BFDBFE")
        bar_fill = PatternFill("solid", fgColor=bar_color)
        ts, te = task["start"], task["end"]
        for wi, wk in enumerate(week_starts):
            col = first_week_col + wi
            cell = ws.cell(row=r, column=col, value="")
            cell.border = GRID_BORDER
            if overlaps(ts, te, wk, week_end(wk)):
                cell.fill = bar_fill
            else:
                cell.fill = base_fill

        ws.row_dimensions[r].height = 30 if is_section else 36

    ws.column_dimensions["A"].width = 8
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 9
    ws.column_dimensions["D"].width = 62
    ws.column_dimensions["E"].width = 8
    ws.column_dimensions["F"].width = 14
    ws.column_dimensions["G"].width = 14
    week_w = max(3.0, min(5.0, 320 / max(len(week_starts), 1)))
    for i in range(len(week_starts)):
        ws.column_dimensions[get_column_letter(first_week_col + i)].width = week_w

    ws.freeze_panes = ws.cell(row=data_start, column=first_week_col)
    ws.sheet_properties.tabColor = "1B365D"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0

    # Legend
    leg_row = data_start + len(tasks) + 2
    ws.merge_cells(start_row=leg_row, start_column=1, end_row=leg_row, end_column=first_week_col - 1)
    leg = ws.cell(leg_row, 1)
    leg.value = (
        "Legend: weekly columns (Mon–Sun). Bar colors match Business-Data-Catalog-Migration-Executive-Gantt phases. "
        "Design rows precede build rows per feature. Regenerate: python3 meetings-tracker/generate_navigator_feature_gantt.py"
    )
    leg.font = META_FONT
    leg.alignment = Alignment(wrap_text=True)

    key_row = leg_row + 2
    ws.cell(key_row, 1, "Phase color key").font = Font(bold=True, size=10, color="1B365D")
    kr = key_row + 1
    for label, color in PHASE_BAR.items():
        sw = ws.cell(kr, 1, "")
        sw.fill = PatternFill("solid", fgColor=color)
        sw.border = GRID_BORDER
        ws.cell(kr, 2, label).font = META_FONT
        ws.row_dimensions[kr].height = 16
        kr += 1

    # Milestones sheet
    _add_milestones_sheet(wb)
    _add_feature_matrix_sheet(wb)

    wb.save(OUTPUT)
    print(f"Wrote {OUTPUT}")


def _add_milestones_sheet(wb: Workbook) -> None:
    ms = wb.create_sheet("Milestones")
    ms.sheet_properties.tabColor = "1D4ED8"
    ms.merge_cells("A1:C1")
    t = ms["A1"]
    t.value = "Business Data Catalog — program milestones"
    t.font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    t.fill = TITLE_BAND_1
    t.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ms.row_dimensions[1].height = 28

    milestones = [
        ("Kickoff", KICKOFF, "Program start · Jun 1, 2026"),
        ("Requirements complete", PHASE_REQ_END, "8 weeks · Q2–Q3 FY26"),
        ("Solution design complete", PHASE_DESIGN_END, "10 weeks · Q3 FY26 (backend + frontend)"),
        ("MVP development complete", PHASE_BUILD_END, "13 weeks · Oct 2026 – Jan 2027"),
        ("Testing complete", PHASE_TEST_END, "4 weeks · Jan–Feb 2027"),
        ("Migration + UAT complete", PHASE_MIG_END, "6 weeks · Mar–Apr 2027"),
        ("Launch — Business Data Catalog", LAUNCH, "May 1, 2027"),
    ]
    hr = 3
    for col, h in enumerate(["Milestone", "Date", "Notes"], 1):
        c = ms.cell(hr, col, h)
        c.font = HEADER_FONT
        c.fill = HEADER_FILL
        c.border = GRID_BORDER
    for i, (name, dt, note) in enumerate(milestones, start=hr + 1):
        ms.cell(i, 1, name).font = BODY_FONT
        ms.cell(i, 2, dt).number_format = "mmm d, yyyy"
        ms.cell(i, 2).font = BODY_FONT
        ms.cell(i, 3, note).font = BODY_FONT
        z = ZEBRA[(i - hr) % 2]
        for c in range(1, 4):
            cell = ms.cell(i, c)
            cell.fill = z
            cell.border = GRID_BORDER
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    ms.column_dimensions["A"].width = 32
    ms.column_dimensions["B"].width = 16
    ms.column_dimensions["C"].width = 48


def _add_feature_matrix_sheet(wb: Workbook) -> None:
    feat = wb.create_sheet("Feature scope")
    feat.sheet_properties.tabColor = "047857"
    feat.merge_cells("A1:F1")
    ft = feat["A1"]
    ft.value = "Business Data Catalog Feature Inventory — scope snapshot"
    ft.font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    ft.fill = TITLE_BAND_1
    ft.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    rows = [
        ("P1", "F01", "Search & Discovery", "MVP", "Find data assets across catalog", "Deck + matrix #1"),
        ("P1", "F02", "Business Glossary", "MVP", "Terms, definitions, BU organization", "Deck + matrix #2"),
        ("P1", "F03", "Catalog Browse", "MVP", "Datasource → schema → table hierarchy", "Deck + matrix #4"),
        ("P1", "F04", "Asset Detail / Descriptions", "MVP", "Table & column context, owners, tags", "Deck + matrix #5"),
        ("P1", "F14", "API & migration integrations", "MVP", "Bulk ops, Alation→OMS load", "Deck P1"),
        ("P2", "F09", "Ownership / Stewardship", "MVP", "Assign owners & stewards", "Deck + matrix #12"),
        ("P2", "—", "Access Controls", "MVP", "Feature-based permission postures", "Deck P2 + matrix #13"),
        ("P2", "F21", "Flags", "MVP/High", "Endorse, warn, deprecate, popularity", "Deck + matrix #7"),
        ("—", "F16", "Asset detail automation", "MVP", "AI suggestions, human endorsement", "Matrix #6"),
        ("—", "F06", "Tags & Classification", "High", "PII/domain tags, filters", "Matrix #16"),
        ("—", "F05", "Data Lineage", "MVP", "OMS leverage — deep link", "Matrix #8"),
        ("—", "F20", "Authentication / SSO", "MVP", "OMS baseline", "Matrix #10"),
        ("—", "F11", "Data Sources & Connectors", "MVP", "Critical datasource coverage", "Matrix #9"),
        ("—", "F23", "Folders / source navigation", "MVP", "Article & content hierarchy", "Matrix #11"),
        ("—", "DD", "Data Dictionary", "MVP", "Steward workflows, CDEs", "Matrix #3"),
        ("Phase 2", "F25", "Admin analytics dashboard", "High", "Usage telemetry & reporting", "Matrix #14"),
        ("Phase 2", "F30", "Expanded data sources", "High", "626 connectors beyond Snowflake", "Matrix #17"),
        ("Phase 2", "F33", "Product pages (authoring)", "High", "Product home, metrics links", "Matrix #18"),
    ]
    hr = 3
    hdr = ["Wave", "PRD", "Feature", "Priority", "Primary use", "Source"]
    for col, h in enumerate(hdr, 1):
        c = feat.cell(hr, col, h)
        c.font = HEADER_FONT
        c.fill = HEADER_FILL
        c.border = GRID_BORDER
    for ri, row in enumerate(rows, start=hr + 1):
        for ci, val in enumerate(row, 1):
            c = feat.cell(ri, ci, val)
            c.font = BODY_FONT
            c.border = GRID_BORDER
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.fill = ZEBRA[(ri - hr) % 2]
    feat.column_dimensions["A"].width = 8
    feat.column_dimensions["B"].width = 8
    feat.column_dimensions["C"].width = 30
    feat.column_dimensions["D"].width = 10
    feat.column_dimensions["E"].width = 36
    feat.column_dimensions["F"].width = 18


def main() -> None:
    tasks = get_tasks()
    build_workbook(tasks)


if __name__ == "__main__":
    main()
