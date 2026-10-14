#!/usr/bin/env python3
"""Build styled Excel workbook for Alation / OMS / Data626 capability comparison."""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Alation-OMS-626-Capability-Comparison-Chart.xlsx"

# (num, capability, description, priority, alation_status, alation_notes, oms_status, oms_notes, d626_status, d626_notes)
ROWS = [
    (
        1,
        "Search & discovery",
        "Keyword/semantic search across tables, schemas, columns, articles, glossary; NL / AI-predicted results",
        "MVP",
        "Met",
        "Primary navigation pattern; ideal chat-with-your-data not fully realized",
        "Gap",
        "No global search across catalogs today",
        "Gap",
        "Not a catalog search UX; may feed metadata into search elsewhere",
    ),
    (
        2,
        "Business glossary",
        "Terms, definitions, synonyms, stewardship, links to catalog objects; BU-organized sections",
        "MVP",
        "Met",
        "Thousands of terms; each BU maintains glossaries",
        "Gap",
        "New catalog; migrate Alation data; add/edit; RBAC",
        "Partial",
        "Consumes glossary as governance context for curation AI; does not replace glossary UX",
    ),
    (
        3,
        "Data dictionary",
        "Table/column documentation, stewards, privacy tags, CDEs, bulk CSV/TSV per DDQGC",
        "MVP",
        "Met",
        "Core steward workflow",
        "Partial",
        "Existing OMS feature set + governance intake triggers; business fields incomplete",
        "Met",
        "Core 626 use case: automate required metadata fields from code + governance standards",
    ),
    (
        4,
        "Catalog browse",
        "Hierarchy navigation by datasource / schema / table",
        "MVP",
        "Met",
        "Primary explore pattern",
        "Partial",
        "Hierarchy/browse exists; business-first navigation and parity TBD",
        "Gap",
        "Graph/API for lifecycle paths, not Alation-style catalog browse",
    ),
    (
        5,
        "Table / asset detail & descriptions",
        "Metadata, owner, tags, lineage context on asset pages",
        "MVP",
        "Met",
        "Descriptions, owners, POC, classification most viewed",
        "Partial",
        "Placeholders exist; need population, steward workflow, trust signals",
        "Partial",
        "Generates/curates descriptions and governance fields; publishes to Alation/OMS",
    ),
    (
        6,
        "Asset detail / description automation",
        "AI suggestions for schema/table/column text, POC, classification; human endorsement",
        "MVP",
        "Gap",
        "Manual upkeep; Alation AI beta lacked cross-system context",
        "Gap",
        "AI recommendations on edit fields not built",
        "Met",
        "Primary 626 value: code + repo context for scalable metadata curation",
    ),
    (
        7,
        "Flags",
        "Endorsements, warnings, deprecations, popularity",
        "MVP/High",
        "Partial",
        "Works for admins/stewards; want broader participation",
        "Gap",
        "Trust/endorsement UX not defined",
        "Gap",
        "Not in 626 scope",
    ),
    (
        8,
        "Data lineage",
        "Upstream/downstream at table, column, views, reports, dataflow level",
        "MVP",
        "Partial",
        "Alation has limited lineage (inventory notes)",
        "Met",
        "Lineage exists in OMS (table/column/dataflow)",
        "Met",
        "Core 626 mission: Git-driven lineage, schema evolution, impact graph",
    ),
    (
        9,
        "Data sources & connectors",
        "Snowflake and connected technical metadata ingestion",
        "MVP",
        "Met",
        "Met for connected sources",
        "Partial",
        "OMS datasource list; confirm full Alation source parity",
        "Partial",
        "Ingests Git + pipeline repos, not generic JDBC connectors",
    ),
    (
        10,
        "Authentication / SSO",
        "Single sign-on, RBAC",
        "MVP",
        "Met",
        "In use",
        "Met",
        "Functionality exists in OMS",
        "Gap",
        "Relies on host apps (OMS/Alation) for access",
    ),
    (
        11,
        "Folders / source navigation",
        "Article hierarchy, how-to and project collections",
        "MVP",
        "Met",
        "In use",
        "Partial",
        "Overlaps catalog browse; UI + data structure work",
        "Gap",
        "Not in scope",
    ),
    (
        12,
        "Ownership / stewardship",
        "Assign owners and stewards to assets",
        "MVP",
        "Met",
        "In use",
        "Partial",
        "Part of planned add/edit functionality",
        "Partial",
        "Stewards in curation workflow; publication to catalog",
    ),
    (
        13,
        "Access controls",
        "Feature-based permissions (glossary, metrics, audit)",
        "MVP",
        "Met",
        "In use",
        "Gap",
        "Permission postures for feature categories not built",
        "Gap",
        "Not in scope",
    ),
    (
        14,
        "Admin analytics dashboard",
        "MAU, top searches, usage telemetry, CSV export",
        "High",
        "Met",
        "Typically built-in for admins",
        "Gap",
        "May exist in Datadog; catalog admin UI needed",
        "Gap",
        "Not in scope",
    ),
    (
        15,
        "Workflows",
        "Ad-hoc/recurring governance and legal workflow tracking",
        "Medium",
        "Partial",
        "Medium priority; not full policy engine",
        "Gap",
        "Not built",
        "Gap",
        "Steward checkpoints in curation only, not general workflow product",
    ),
    (
        16,
        "Tags & classification",
        "PII, domain, custom tags; search and filters",
        "High",
        "Partial",
        "Critical tags in use; some readonly from other systems",
        "Partial",
        "Readonly from other systems; tag create/assign/search needs add/edit",
        "Partial",
        "Can populate classification/sensitivity fields in curation model",
    ),
    (
        17,
        "Expanded data sources",
        "Vendor sources outside Snowflake (e.g., HighTouch)",
        "High",
        "Gap",
        "Limited connector coverage for non-Snowflake vendors",
        "Gap",
        "Confirm source list vs Alation",
        "Partial",
        "Code analysis spans ingestion to warehouse to activation paths",
    ),
    (
        18,
        "Product pages (authoring)",
        "Product docs, metrics impacted, contacts, domain, stewards; AI from wiki",
        "High",
        "Gap",
        "Aspirational / not fully realized in Alation today",
        "Gap",
        "Content model, editor, versioning, AI generation",
        "Gap",
        "Focused on dataset/event lifecycle, not product-page CMS",
    ),
    (
        19,
        "Mass / bulk edit",
        "Multi-asset metadata changes; CSV upload with audit",
        "Medium",
        "Met",
        "Alation supports UI + CSV",
        "Partial",
        "Part of planned add/edit (overlap with tags)",
        "Gap",
        "Not in scope",
    ),
    (
        20,
        "Dataflows",
        "ETL jobs, stored procs, dbt, Airflow DAGs as first-class objects",
        "Medium",
        "Met",
        "In use",
        "Met",
        "Pipelines/jobs metadata in OMS",
        "Partial",
        "Inferred from Git/pipeline definitions, not runtime-only",
    ),
    (
        21,
        "Domains",
        "Business area groupings for search, stewards, policies",
        "Medium",
        "Met",
        "In use",
        "Gap",
        "New feature/catalog",
        "Partial",
        "Data domain is a required curation field",
    ),
    (
        22,
        "Export / reports",
        "Catalog, usage, compliance exports",
        "Medium",
        "Met",
        "In use",
        "Gap",
        "Not built",
        "Gap",
        "Not in scope",
    ),
    (
        23,
        "Usage / access metrics",
        "Last access, unique users, query history",
        "Medium",
        "Met",
        "In use",
        "Met",
        "Functionality exists in OMS",
        "Partial",
        "Value score / downstream-use frequency (different metric model)",
    ),
    (
        24,
        "AI chat assistant in app",
        "NL Q&A over catalog, SQL suggestions, glossary links",
        "Medium",
        "Partial",
        "Limited vs desired",
        "Partial",
        "Exists; needs Alation/data enhancements",
        "Partial",
        "AI reasoning layer for why/what-breaks; not full catalog chat",
    ),
    (
        25,
        "Mass set rules / catalog sets",
        "Rule engine for tags, policies, ownership at scale",
        "Medium",
        "Met",
        "In use",
        "Gap",
        "PI fields detectable; rule engine enhancements needed",
        "Gap",
        "Not in scope",
    ),
    (
        26,
        "Data dictionary download & upload",
        "Bulk export/import of metadata",
        "Medium",
        "Met",
        "In use",
        "Partial",
        "Needs enhancements to Alation migration data",
        "Gap",
        "Publishes curated metadata via integration APIs",
    ),
    (
        27,
        "Saved queries / favorites",
        "Bookmark assets and searches",
        "Medium",
        "Met",
        "In use",
        "Gap",
        "Not built",
        "Gap",
        "Not in scope",
    ),
    (
        28,
        "Overview & social section",
        "Catalog home, popular tables/searches, social feed (privacy-safe)",
        "Medium",
        "Gap",
        "Underbuilt / privacy concerns",
        "Gap",
        "Not built",
        "Gap",
        "Not in scope",
    ),
    (
        29,
        "Custom fields",
        "User-defined metadata on assets",
        "Medium",
        "Met",
        "In use",
        "Gap",
        "Not built",
        "Partial",
        "Governed required/optional field set, not arbitrary custom fields",
    ),
    (
        30,
        "Comments on assets / Q&A",
        "Collaboration, questions on assets",
        "Low-Med",
        "Low",
        "Low adoption",
        "Gap",
        "Not built",
        "Gap",
        "Not in scope",
    ),
    (
        31,
        "Version control",
        "Asset versioning, change history",
        "Low-Med",
        "Low",
        "Underutilized",
        "Gap",
        "Not built",
        "Gap",
        "Not in scope",
    ),
    (
        32,
        "Policy center",
        "Policies, risk classification, compliance rules",
        "Low",
        "Low",
        "Low adoption",
        "Gap",
        "Not built",
        "Gap",
        "Privacy links at lifecycle level only",
    ),
    (
        33,
        "Compilation / data quality",
        "DQ rules and monitoring",
        "Low-Med",
        "Low",
        "Low adoption",
        "Gap",
        "Not built",
        "Partial",
        "Fitness function / quality variance warnings in PRD",
    ),
    (
        34,
        "API & integrations",
        "REST for bulk ops, BI integration",
        "Medium",
        "Met",
        "In use",
        "Partial",
        "Enhancement needed for full parity",
        "Partial",
        "Catalog UI/API for synthetic metadata graph",
    ),
    (
        35,
        'Details ("i") icon',
        "In-context help on features",
        "Medium",
        "Gap",
        "UX/documentation gap",
        "Gap",
        "Not built",
        "Gap",
        "Not in scope",
    ),
    (
        36,
        "Persona view filtering",
        "Role-based catalog experience",
        "Low",
        "Gap",
        "Not built in Alation",
        "Gap",
        "Permissions framework needed",
        "Gap",
        "Not in scope",
    ),
    (
        37,
        'AI "How to"',
        "Help center for catalog usage",
        "Low",
        "Gap",
        "Not built",
        "Partial",
        "Extend existing chatbot",
        "Partial",
        "Explain-the-system Q&A, not product help center",
    ),
]

STATUS_FILL = {
    "Met": PatternFill("solid", fgColor="C6EFCE"),
    "Partial": PatternFill("solid", fgColor="FFEB9C"),
    "Gap": PatternFill("solid", fgColor="FFC7CE"),
    "Low": PatternFill("solid", fgColor="E7E6E6"),
}

STATUS_FONT = {
    "Met": Font(color="006100", bold=True),
    "Partial": Font(color="9C6500", bold=True),
    "Gap": Font(color="9C0006", bold=True),
    "Low": Font(color="595959", bold=True),
}

THIN = Side(style="thin", color="D9D9D9")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def style_header(cell, fill: str, font_color: str = "FFFFFF") -> None:
    cell.fill = PatternFill("solid", fgColor=fill)
    cell.font = Font(bold=True, color=font_color, size=11)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = BORDER


def write_comparison_sheet(wb: Workbook) -> None:
    ws = wb.active
    ws.title = "Capability Comparison"

    ws.merge_cells("A1:J1")
    title = ws["A1"]
    title.value = "Alation → OMS → Data626 Capability Comparison"
    title.font = Font(bold=True, size=16, color="1F2937")
    title.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:J2")
    subtitle = ws["A2"]
    subtitle.value = (
        "DEEPT Data Governance  |  Navigator Feature Inventory Matrix v1.0 (Mar 2026)  |  "
        "Column 2 inferred pending SharePoint gap doc validation"
    )
    subtitle.font = Font(italic=True, size=10, color="6B7280")
    subtitle.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[2].height = 18

    group_row = 4
    ws.merge_cells("A4:A5")
    ws["A4"].value = "#"
    style_header(ws["A4"], "374151")

    ws.merge_cells("B4:D4")
    ws["B4"].value = "Alation Capabilities (used or wanted)"
    style_header(ws["B4"], "4338CA")

    ws.merge_cells("E4:F4")
    ws["E4"].value = "Used / Need (Alation)"
    style_header(ws["E4"], "6366F1")

    ws.merge_cells("G4:H4")
    ws["G4"].value = "OMS"
    style_header(ws["G4"], "0F766E")

    ws.merge_cells("I4:J4")
    ws["I4"].value = "Data626"
    style_header(ws["I4"], "7C3AED")

    subheader_row = 5
    subheaders = ["Capability", "Description", "Priority", "Status", "Notes", "Status", "Notes", "Status", "Notes"]
    for idx, label in enumerate(subheaders, start=2):
        cell = ws.cell(row=subheader_row, column=idx, value=label)
        style_header(cell, "111827")

    start_row = 6
    for i, row in enumerate(ROWS):
        r = start_row + i
        num, cap, desc, priority, a_stat, a_note, o_stat, o_note, d_stat, d_note = row
        values = [num, cap, desc, priority, a_stat, a_note, o_stat, o_note, d_stat, d_note]
        for col_idx, value in enumerate(values, start=1):
            cell = ws.cell(row=r, column=col_idx, value=value)
            cell.border = BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if col_idx in (5, 7, 9):
                status = str(value)
                cell.fill = STATUS_FILL.get(status, PatternFill())
                cell.font = STATUS_FONT.get(status, Font(bold=True))
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            elif col_idx == 1:
                cell.alignment = Alignment(horizontal="center", vertical="top")
                cell.font = Font(bold=True)
            elif col_idx == 4:
                cell.alignment = Alignment(horizontal="center", vertical="top")
                if priority in ("MVP", "MVP/High", "High"):
                    cell.fill = PatternFill("solid", fgColor="EEF2FF")
                    cell.font = Font(bold=True, color="3730A3")

        if priority in ("MVP", "MVP/High", "High"):
            for col_idx in range(1, 11):
                ws.cell(row=r, column=col_idx).fill = PatternFill("solid", fgColor="F5F3FF")

        for col_idx in (5, 7, 9):
            ws.cell(row=r, column=col_idx).fill = STATUS_FILL.get(
                str(ws.cell(row=r, column=col_idx).value), PatternFill()
            )

    last_row = start_row + len(ROWS) - 1
    ws.freeze_panes = "B6"
    ws.auto_filter.ref = f"A5:J{last_row}"

    widths = {"A": 5, "B": 28, "C": 42, "D": 10, "E": 10, "F": 36, "G": 10, "H": 36, "I": 10, "J": 36}
    for col, width in widths.items():
        ws.column_dimensions[col].width = width

    for row_num in range(start_row, last_row + 1):
        ws.row_dimensions[row_num].height = 52


def write_legend_sheet(wb: Workbook) -> None:
    ws = wb.create_sheet("Legend & Sources")
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 70

    ws["A1"] = "Legend"
    ws["A1"].font = Font(bold=True, size=14)

    legend = [
        ("Met", "In use today; platform meets the need (may still need migration or UX polish)"),
        ("Partial", "Works with known limitations, manual burden, or extensions required"),
        ("Gap", "Needed but not reliably delivered or not in scope"),
        ("Low", "Low adoption or Phase 2+ priority"),
    ]
    row = 3
    for status, meaning in legend:
        ws.cell(row=row, column=1, value=status).fill = STATUS_FILL[status]
        ws.cell(row=row, column=1).font = STATUS_FONT[status]
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="center")
        ws.cell(row=row, column=2, value=meaning).alignment = Alignment(wrap_text=True)
        row += 1

    row += 2
    ws.cell(row=row, column=1, value="Sources").font = Font(bold=True, size=14)
    row += 1
    sources = [
        "Navigator Feature Inventory Matrix (Google Doc) — Alation inventory + OMS assessment, Mar 2026",
        "Alation Capabilities and Gap Evaluation (SharePoint, Tim Liu) — NOT retrieved; column 2 inferred",
        "Metadata Curation Automation memo — Data626 curation scope, Alation AI limits",
        "Data626: Data Lifecycle Management PRD — lineage, graph, explicit non-replacement of Alation/OMS",
    ]
    for source in sources:
        ws.cell(row=row, column=1, value="•")
        ws.cell(row=row, column=2, value=source).alignment = Alignment(wrap_text=True)
        row += 1

    row += 2
    ws.cell(row=row, column=1, value="Positioning").font = Font(bold=True, size=14)
    row += 1
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
    ws.cell(row=row, column=1, value=(
        "626 improves metadata supply; OMS stores and serves it; "
        "Navigator/BDC is the governed experience for business and compliance users."
    )).alignment = Alignment(wrap_text=True)


def write_summary_sheet(wb: Workbook) -> None:
    ws = wb.create_sheet("Summary (MVP+High)")

    ws["A1"] = "Roll-up: MVP + High priority capabilities (rows 1–18)"
    ws["A1"].font = Font(bold=True, size=14)

    headers = ["Platform", "Met", "Partial", "Gap"]
    for col, h in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=col, value=h)
        style_header(cell, "374151")

    summary = [
        ("Alation (today)", 12, 8, 5),
        ("OMS", 4, 9, 12),
        ("Data626", 3, 8, 14),
    ]
    for r_idx, (platform, met, partial, gap) in enumerate(summary, start=4):
        ws.cell(row=r_idx, column=1, value=platform).font = Font(bold=True)
        ws.cell(row=r_idx, column=2, value=met).fill = STATUS_FILL["Met"]
        ws.cell(row=r_idx, column=3, value=partial).fill = STATUS_FILL["Partial"]
        ws.cell(row=r_idx, column=4, value=gap).fill = STATUS_FILL["Gap"]
        for c in range(1, 5):
            ws.cell(row=r_idx, column=c).border = BORDER
            ws.cell(row=r_idx, column=c).alignment = Alignment(horizontal="center" if c > 1 else "left")

    ws.column_dimensions["A"].width = 22
    for col in ("B", "C", "D"):
        ws.column_dimensions[col].width = 12

    ws["A8"] = "Cross-cutting Alation gaps driving migration"
    ws["A8"].font = Font(bold=True, size=12)
    themes = [
        "Manual metadata burden — descriptions, classifications, stewardship fields decay without automation",
        "Limited lineage depth — insufficient for impact analysis; 626 + OMS intended to exceed Alation",
        "AI without system context — Alation AI cannot interpret cross-platform pipelines",
        "Business experience gaps — global search, glossary UX, trust flags, product pages, persona filtering",
        "Connector / source sprawl — non-Snowflake and activation tools poorly covered",
    ]
    row = 9
    for theme in themes:
        ws.cell(row=row, column=1, value=f"{row - 8}.")
        ws.cell(row=row, column=2, value=theme)
        row += 1
    ws.column_dimensions["B"].width = 90


def main() -> None:
    wb = Workbook()
    write_comparison_sheet(wb)
    write_legend_sheet(wb)
    write_summary_sheet(wb)
    wb.save(OUTPUT)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
