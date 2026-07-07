#!/usr/bin/env python3
"""Build Navigator umbrella overview PowerPoint deck."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parent / "Navigator-Data-Governance-Overview.pptx"

# Brand palette (aligned with navigator-oms-alignment-deck)
NAVY = RGBColor(0x0F, 0x27, 0x44)
HEADER_BLUE = RGBColor(0x1E, 0x5A, 0x96)
ACCENT = RGBColor(0x15, 0x65, 0xC0)
LIGHT_BLUE = RGBColor(0xE4, 0xEE, 0xF8)
PAGE_BG = RGBColor(0xF4, 0xF6, 0xF9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x5C, 0x65, 0x70)
FOOTER = RGBColor(0x3D, 0x51, 0x66)
SOFT_BORDER = RGBColor(0xD0, 0xD8, 0xE2)


def rgb(hex_str: str) -> RGBColor:
    h = hex_str.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def set_fill(shape, color: RGBColor) -> None:
    shape.fill.solid()
    shape.fill.fore_color.rgb = color


def set_line(shape, color: RGBColor, width_pt: float = 0.75) -> None:
    line = shape.line
    line.color.rgb = color
    line.width = Pt(width_pt)


def add_textbox(
    slide,
    left,
    top,
    width,
    height,
    text: str,
    *,
    size: int = 14,
    bold: bool = False,
    color: RGBColor = TEXT,
    align=PP_ALIGN.LEFT,
    font_name: str = "Calibri",
    valign=MSO_ANCHOR.TOP,
    spacing: float = 1.15,
):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.line_spacing = spacing
    run = p.runs[0]
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = font_name
    run.font.color.rgb = color
    return box


def add_bullets(slide, left, top, width, height, items: list[str], *, size: int = 13, color: RGBColor = TEXT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.line_spacing = 1.2
        p.space_after = Pt(6)
        run = p.runs[0]
        run.font.size = Pt(size)
        run.font.name = "Calibri"
        run.font.color.rgb = color
    return box


def add_header_bar(slide, title: str, slide_num: int | None = None) -> None:
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.72))
    set_fill(bar, HEADER_BLUE)
    bar.line.fill.background()
    add_textbox(
        slide,
        Inches(0.55),
        Inches(0.14),
        Inches(10.5),
        Inches(0.5),
        title,
        size=22,
        bold=True,
        color=WHITE,
    )
    if slide_num is not None:
        add_textbox(
            slide,
            Inches(11.6),
            Inches(0.22),
            Inches(1.4),
            Inches(0.35),
            f"{slide_num:02d}",
            size=11,
            bold=True,
            color=WHITE,
            align=PP_ALIGN.RIGHT,
        )


def add_footer(slide, note: str = "DEEPT · Data Governance · Navigator") -> None:
    foot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.05), Inches(13.333), Inches(0.45))
    set_fill(foot, FOOTER)
    foot.line.fill.background()
    add_textbox(slide, Inches(0.55), Inches(7.12), Inches(8), Inches(0.3), note, size=9, color=WHITE)
    add_textbox(
        slide,
        Inches(10.5),
        Inches(7.12),
        Inches(2.3),
        Inches(0.3),
        date.today().strftime("%B %Y"),
        size=9,
        color=WHITE,
        align=PP_ALIGN.RIGHT,
    )


def blank_slide(prs: Presentation):
    layout = prs.slide_layouts[6]  # blank
    slide = prs.slides.add_slide(layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    set_fill(bg, PAGE_BG)
    bg.line.fill.background()
    # send to back by re-adding isn't trivial; keep as first shape — fine for blank layout
    return slide


def add_card(slide, left, top, width, height, title: str, body: str, accent: RGBColor = ACCENT):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    set_fill(card, WHITE)
    set_line(card, SOFT_BORDER, 1)
    accent_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.08), height)
    set_fill(accent_bar, accent)
    accent_bar.line.fill.background()
    add_textbox(slide, left + Inches(0.22), top + Inches(0.12), width - Inches(0.3), Inches(0.35), title, size=13, bold=True, color=NAVY)
    add_textbox(slide, left + Inches(0.22), top + Inches(0.48), width - Inches(0.3), height - Inches(0.55), body, size=11, color=TEXT)


def slide_title(prs: Presentation) -> None:
    slide = blank_slide(prs)
    hero = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(4.35))
    set_fill(hero, NAVY)
    hero.line.fill.background()
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(4.35), Inches(13.333), Inches(0.12))
    set_fill(stripe, ACCENT)
    stripe.line.fill.background()

    add_textbox(slide, Inches(0.9), Inches(1.35), Inches(11), Inches(1.2), "Navigator", size=54, bold=True, color=WHITE)
    add_textbox(
        slide,
        Inches(0.92),
        Inches(2.55),
        Inches(10.5),
        Inches(0.9),
        "The collective data governance product family for DEEPT",
        size=24,
        color=RGBColor(0xC5, 0xD4, 0xE3),
    )
    add_textbox(
        slide,
        Inches(0.92),
        Inches(3.35),
        Inches(10),
        Inches(0.6),
        "Programs · Catalog · Policy · Inventory · Operations",
        size=14,
        color=RGBColor(0xA8, 0xBC, 0xD4),
    )

    panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(4.75), Inches(11.5), Inches(1.85))
    set_fill(panel, WHITE)
    set_line(panel, SOFT_BORDER, 1)
    add_textbox(
        slide,
        Inches(1.15),
        Inches(4.95),
        Inches(11),
        Inches(1.5),
        "One umbrella story connecting the governance portal, Business Data Catalog on OMS, "
        "the Policy Drive Governance Framework, and Kronos business inventory—without "
        "duplicating platform stores or blurring build ownership.",
        size=15,
        color=TEXT,
    )
    add_footer(slide, "Disney Entertainment & ESPN Technology · Data Governance")


def slide_why(prs: Presentation) -> None:
    slide = blank_slide(prs)
    add_header_bar(slide, "Why Navigator", 2)
    add_textbox(
        slide,
        Inches(0.65),
        Inches(0.95),
        Inches(12),
        Inches(0.55),
        "Alation exit and OMS maturation require a coherent governance product—not another disconnected toolset.",
        size=16,
        color=NAVY,
        bold=True,
    )
    cols = [
        (
            "Continuity",
            "Stewards and analysts need search, glossary, ownership, and tags on OMS—not a return to spreadsheets and Slack threads when Alation sunsets.",
            ACCENT,
        ),
        (
            "Coherence",
            "Privacy, security, regulatory, and catalog work already span PULS, Access Manager, Kronos, and program queues. Navigator orients users across them.",
            HEADER_BLUE,
        ),
        (
            "Clarity",
            "OMS Foundations owns the store and APIs. Data Governance owns business-facing shells. Navigator makes that boundary explicit and defensible.",
            NAVY,
        ),
    ]
    x0 = Inches(0.65)
    w = Inches(3.95)
    gap = Inches(0.25)
    for i, (title, body, accent) in enumerate(cols):
        add_card(slide, x0 + i * (w + gap), Inches(1.75), w, Inches(2.35), title, body, accent)

    callout = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), Inches(4.35), Inches(12.05), Inches(1.05))
    set_fill(callout, LIGHT_BLUE)
    set_line(callout, ACCENT, 1.5)
    add_textbox(
        slide,
        Inches(0.9),
        Inches(4.55),
        Inches(11.6),
        Inches(0.75),
        "Navigator answers two questions for every user:  Where is my program work?   and   Where is the governed data?",
        size=14,
        bold=True,
        color=NAVY,
        align=PP_ALIGN.CENTER,
    )
    add_footer(slide)


def slide_umbrella(prs: Presentation) -> None:
    slide = blank_slide(prs)
    add_header_bar(slide, "One product family, four named parts", 3)

    center = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5.15), Inches(2.55), Inches(3.0), Inches(1.55))
    set_fill(center, NAVY)
    center.line.fill.background()
    add_textbox(slide, Inches(5.35), Inches(3.0), Inches(2.6), Inches(0.7), "Navigator\n(umbrella)", size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    parts = [
        (Inches(0.65), Inches(1.35), "Navigator Portal", "Governance home & program operations\nPrivacy · Platform · Security · Regulatory"),
        (Inches(9.15), Inches(1.35), "Business Data Catalog", "Business-first UI on OMS APIs\nDiscovery · Glossary · Stewardship"),
        (Inches(0.65), Inches(4.55), "Policy Drive Framework", "PULS · Access Manager · Gov App backend\nClassifications · Policies · Metrics"),
        (Inches(9.15), Inches(4.55), "Kronos", "Business inventory (SISU Postgres)\nRegulatory · Inventory deep link"),
    ]
    for left, top, title, body in parts:
        add_card(slide, left, top, Inches(3.55), Inches(1.55), title, body)

    # connector lines (simple rectangles as arrows)
    for left, top, width, height in [
        (Inches(4.2), Inches(2.1), Inches(0.95), Inches(0.04)),
        (Inches(8.15), Inches(2.1), Inches(0.95), Inches(0.04)),
        (Inches(4.2), Inches(5.3), Inches(0.95), Inches(0.04)),
        (Inches(8.15), Inches(5.3), Inches(0.95), Inches(0.04)),
    ]:
        ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        set_fill(ln, ACCENT)
        ln.line.fill.background()

    add_footer(slide)


def slide_portal(prs: Presentation) -> None:
    slide = blank_slide(prs)
    add_header_bar(slide, "Navigator portal — program command center", 4)
    add_textbox(
        slide,
        Inches(0.65),
        Inches(0.95),
        Inches(12),
        Inches(0.5),
        "Formerly Governance Portal. Orients governance operators; does not replace Kronos or PULS.",
        size=14,
        color=MUTED,
    )
    dims = [
        ("Privacy", "Consent · DSRs · Tracker remediation", RGBColor(0x6A, 0x1B, 0x9A)),
        ("Platform", "Stewards → BDC · Classifications · Policies", ACCENT),
        ("Security", "Access · GIS · Data use", HEADER_BLUE),
        ("Regulatory", "Laws & regulations · Incidents · Inventory → Kronos", NAVY),
    ]
    for i, (title, items, accent) in enumerate(dims):
        row, col = divmod(i, 2)
        left = Inches(0.65 + col * 6.2)
        top = Inches(1.65 + row * 2.05)
        add_card(slide, left, top, Inches(5.95), Inches(1.75), title, items, accent)

    add_bullets(
        slide,
        Inches(0.65),
        Inches(5.85),
        Inches(12),
        Inches(0.9),
        [
            "Governance Overview aggregates posture metrics for leadership reporting.",
            "Workflow UIs connect to Gov App backend; evidence export supports audit cycles.",
        ],
        size=12,
        color=TEXT,
    )
    add_footer(slide)


def slide_bdc(prs: Presentation) -> None:
    slide = blank_slide(prs)
    add_header_bar(slide, "Business Data Catalog — governed metadata on OMS", 5)
    add_textbox(
        slide,
        Inches(0.65),
        Inches(0.95),
        Inches(7.5),
        Inches(0.9),
        "The daily workspace for stewards, analysts, and engineers. Consumes OMS—it does not re-implement ingestion or the graph store.",
        size=14,
        color=TEXT,
    )
    add_bullets(
        slide,
        Inches(0.65),
        Inches(1.95),
        Inches(6.2),
        Inches(2.8),
        [
            "Data Sources, Catalog browse, Glossary, asset detail",
            "Ownership, tags/classifications, lineage (where OMS graph supports)",
            "Opened from left nav or Navigator Platform → Stewards",
            "MVP: high-value Alation workflow parity for in-scope domains",
        ],
        size=13,
    )
    panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.35), Inches(5.5), Inches(4.2))
    set_fill(panel, WHITE)
    set_line(panel, SOFT_BORDER, 1)
    add_textbox(slide, Inches(7.45), Inches(1.55), Inches(5), Inches(0.35), "Build ownership", size=12, bold=True, color=NAVY)
    rows = [
        ("Data Governance", "BDC product, UX, stewardship flows"),
        ("OMS Foundations", "Store, connectors, APIs, graph"),
        ("Not in scope", "Duplicate ingestion or second catalog store"),
    ]
    y = Inches(2.0)
    for who, what in rows:
        add_textbox(slide, Inches(7.45), y, Inches(2.1), Inches(0.35), who, size=11, bold=True, color=ACCENT)
        add_textbox(slide, Inches(9.55), y, Inches(3.0), Inches(0.55), what, size=11, color=TEXT)
        y += Inches(0.75)
    add_textbox(
        slide,
        Inches(7.45),
        Inches(4.35),
        Inches(5),
        Inches(0.9),
        "OMS is the engine. BDC is how the governance program experiences catalog value.",
        size=11,
        bold=True,
        color=NAVY,
    )
    add_footer(slide)


def slide_puls(prs: Presentation) -> None:
    slide = blank_slide(prs)
    add_header_bar(slide, "Policy Drive Governance Framework", 6)
    add_textbox(
        slide,
        Inches(0.65),
        Inches(0.95),
        Inches(12),
        Inches(0.5),
        "Authoritative policy and control metadata behind Navigator workflows.",
        size=14,
        color=MUTED,
    )
    stack = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), Inches(1.55), Inches(5.8), Inches(4.35))
    set_fill(stack, WHITE)
    set_line(stack, ACCENT, 1.25)
    add_textbox(slide, Inches(0.9), Inches(1.75), Inches(5.3), Inches(0.35), "PULS Postgres (system of record)", size=13, bold=True, color=NAVY)
    domains = [
        "Classifications & tag definitions — sensitivity, domain, control labels",
        "Policies — obligations and control mappings to asset populations",
        "Metrics — governance KPIs feeding Governance Overview",
    ]
    add_bullets(slide, Inches(0.95), Inches(2.2), Inches(5.2), Inches(2.2), domains, size=12)

    add_card(
        slide,
        Inches(6.85),
        Inches(1.55),
        Inches(5.85),
        Inches(1.35),
        "Access Manager",
        "Bidirectional read/update with PULS classifications. Where governance meets access enforcement.",
        HEADER_BLUE,
    )
    add_card(
        slide,
        Inches(6.85),
        Inches(3.1),
        Inches(5.85),
        Inches(1.35),
        "Gov App backend",
        "API layer for Navigator workflow UIs. Read/update policies and metrics with audit logging.",
        ACCENT,
    )
    add_card(
        slide,
        Inches(6.85),
        Inches(4.65),
        Inches(5.85),
        Inches(1.25),
        "Open design question",
        "OMS → PULS read path (direct vs. via Gov App API) — affects BDC classification display.",
        NAVY,
    )
    add_footer(slide)


def slide_kronos(prs: Presentation) -> None:
    slide = blank_slide(prs)
    add_header_bar(slide, "Kronos — business inventory", 7)
    add_textbox(
        slide,
        Inches(0.65),
        Inches(0.95),
        Inches(12),
        Inches(0.55),
        "Business context lives here—not in OMS technical metadata. Navigator links out; it does not fork inventory.",
        size=14,
        color=TEXT,
    )
    left_panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), Inches(1.7), Inches(5.9), Inches(3.9))
    set_fill(left_panel, LIGHT_BLUE)
    set_line(left_panel, HEADER_BLUE, 1)
    add_textbox(slide, Inches(0.95), Inches(1.95), Inches(5.3), Inches(0.35), "What Kronos holds", size=13, bold=True, color=NAVY)
    add_bullets(
        slide,
        Inches(0.95),
        Inches(2.4),
        Inches(5.2),
        Inches(2.8),
        [
            "Authoritative business inventory on SISU Postgres",
            "Business purpose, obligations, and inventory completeness",
            "Complements OMS tables, columns, and lineage",
            "Regulatory-facing; edited in Kronos, not duplicated in Navigator",
        ],
        size=12,
    )
    add_card(
        slide,
        Inches(7.0),
        Inches(1.7),
        Inches(5.7),
        Inches(1.6),
        "Navigator entry point",
        "Regulatory dimension → Inventory opens Kronos (dcf.corp.dig.com/vista/kronos/).",
        ACCENT,
    )
    add_card(
        slide,
        Inches(7.0),
        Inches(3.55),
        Inches(5.7),
        Inches(1.6),
        "Future posture",
        "Inventory completeness metrics may appear on Governance Overview; curation stays in Kronos.",
        NAVY,
    )
    add_footer(slide)


def slide_architecture(prs: Presentation) -> None:
    slide = blank_slide(prs)
    add_header_bar(slide, "Architecture — three platform zones", 8)

    zones = [
        (Inches(0.55), "SISU / Kronos", "Business inventory\n(Postgres)", RGBColor(0x2E, 0x7D, 0x32)),
        (Inches(4.65), "Governance stack", "PULS · Access Mgr · Gov App\nClassifications · Policies · Metrics", HEADER_BLUE),
        (Inches(8.75), "OMS", "Technical metadata hub\nAPIs · Graph · Warehouses", ACCENT),
    ]
    for left, title, body, accent in zones:
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.55), Inches(3.85), Inches(2.45))
        set_fill(box, WHITE)
        set_line(box, accent, 1.5)
        add_textbox(slide, left + Inches(0.2), Inches(1.75), Inches(3.45), Inches(0.4), title, size=14, bold=True, color=NAVY)
        add_textbox(slide, left + Inches(0.2), Inches(2.25), Inches(3.45), Inches(1.2), body, size=12, color=TEXT, align=PP_ALIGN.CENTER)

    # BDC + Navigator UI under OMS
    bdc = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), Inches(4.35), Inches(2.2), Inches(0.75))
    set_fill(bdc, LIGHT_BLUE)
    set_line(bdc, ACCENT, 1)
    add_textbox(slide, Inches(8.1), Inches(4.5), Inches(2.0), Inches(0.5), "Business Data\nCatalog UI", size=10, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

    nav_ui = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.35), Inches(4.35), Inches(2.4), Inches(0.75))
    set_fill(nav_ui, LIGHT_BLUE)
    set_line(nav_ui, HEADER_BLUE, 1)
    add_textbox(slide, Inches(4.45), Inches(4.5), Inches(2.2), Inches(0.5), "Navigator\nportal UIs", size=10, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

    kronos_ui = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(4.35), Inches(1.8), Inches(0.75))
    set_fill(kronos_ui, LIGHT_BLUE)
    set_line(kronos_ui, RGBColor(0x2E, 0x7D, 0x32), 1)
    add_textbox(slide, Inches(1.05), Inches(4.55), Inches(1.6), Inches(0.4), "Kronos UI", size=10, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

    add_textbox(
        slide,
        Inches(0.65),
        Inches(5.35),
        Inches(12),
        Inches(0.55),
        "UI layers read from their authoritative stores. Navigator orchestrates; it does not collapse three platforms into one database.",
        size=12,
        color=MUTED,
        align=PP_ALIGN.CENTER,
    )
    add_footer(slide)


def slide_ownership(prs: Presentation) -> None:
    slide = blank_slide(prs)
    add_header_bar(slide, "Who builds what", 9)
    headers = ["Component", "Product / program owner", "Platform owner"]
    rows = [
        ("Navigator portal & workflows", "Data Governance", "Gov App backend with SISU"),
        ("Business Data Catalog", "Data Governance", "OMS APIs (OMS Foundations)"),
        ("PULS / classifications / policies", "Data Governance program", "SISU relational stack"),
        ("Kronos inventory", "Inventory program operators", "SISU Postgres"),
        ("OMS store & ingestion", "—", "OMS Foundations"),
    ]
    table_shape = slide.shapes.add_table(len(rows) + 1, 3, Inches(0.65), Inches(1.45), Inches(12.05), Inches(3.35))
    table = table_shape.table
    col_widths = (Inches(3.6), Inches(4.0), Inches(4.45))
    for idx, w in enumerate(col_widths):
        table.columns[idx].width = w

    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = h
        for p in cell.text_frame.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(11)
                r.font.color.rgb = WHITE
        set_fill(cell, NAVY)

    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(11)
                    run.font.color.rgb = TEXT
            if r % 2 == 0:
                set_fill(cell, RGBColor(0xF8, 0xFA, 0xFC))

    add_textbox(
        slide,
        Inches(0.65),
        Inches(5.05),
        Inches(12),
        Inches(0.7),
        "Clear ownership prevents “another OMS” scope creep and keeps migration delivery credible.",
        size=13,
        bold=True,
        color=NAVY,
        align=PP_ALIGN.CENTER,
    )
    add_footer(slide)


def slide_phasing(prs: Presentation) -> None:
    slide = blank_slide(prs)
    add_header_bar(slide, "Phased delivery", 10)
    phases = [
        ("Phase 1 — Now", "BDC MVP on OMS APIs · Navigator IA & wireframes · Kronos inventory link", ACCENT),
        ("Phase 2 — Next", "Gov App backend + PULS paths · Classifications & policy workflows in Navigator", HEADER_BLUE),
        ("Phase 3 — Mature", "Metrics governance UI · OMS↔PULS read model · executive reporting automation", NAVY),
    ]
    for i, (phase, detail, accent) in enumerate(phases):
        top = Inches(1.35 + i * 1.55)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), top, Inches(0.18), Inches(1.15))
        set_fill(bar, accent)
        bar.line.fill.background()
        add_textbox(slide, Inches(0.95), top, Inches(2.2), Inches(0.4), phase, size=14, bold=True, color=NAVY)
        add_textbox(slide, Inches(0.95), top + Inches(0.42), Inches(11.5), Inches(0.65), detail, size=13, color=TEXT)

    add_bullets(
        slide,
        Inches(0.65),
        Inches(5.35),
        Inches(12),
        Inches(1.0),
        [
            "Front-load catalog continuity to de-risk Alation exit.",
            "Sequence PULS integration without blocking BDC on OMS.",
            "Defer low-adoption features until migration must-haves are proven.",
        ],
        size=12,
        color=MUTED,
    )
    add_footer(slide)


def slide_close(prs: Presentation) -> None:
    slide = blank_slide(prs)
    hero = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    set_fill(hero, NAVY)
    hero.line.fill.background()
    add_textbox(slide, Inches(0.9), Inches(2.0), Inches(11), Inches(1.0), "Navigator", size=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(
        slide,
        Inches(1.2),
        Inches(3.15),
        Inches(10.9),
        Inches(0.8),
        "One governance program. Clear platform boundaries. Coordinated delivery.",
        size=20,
        color=RGBColor(0xC5, 0xD4, 0xE3),
        align=PP_ALIGN.CENTER,
    )
    add_textbox(
        slide,
        Inches(1.2),
        Inches(4.2),
        Inches(10.9),
        Inches(0.6),
        "Wireframes · PRD · Architecture diagram available in program workspace",
        size=13,
        color=RGBColor(0xA8, 0xBC, 0xD4),
        align=PP_ALIGN.CENTER,
    )
    add_textbox(slide, Inches(1.2), Inches(5.5), Inches(10.9), Inches(0.5), "Questions & discussion", size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


def build() -> Path:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    slide_title(prs)
    slide_why(prs)
    slide_umbrella(prs)
    slide_portal(prs)
    slide_bdc(prs)
    slide_puls(prs)
    slide_kronos(prs)
    slide_architecture(prs)
    slide_ownership(prs)
    slide_phasing(prs)
    slide_close(prs)

    prs.save(OUT)
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")
