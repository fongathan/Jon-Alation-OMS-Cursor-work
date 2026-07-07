#!/usr/bin/env python3
"""Build Data Navigator intake deck (PowerPoint) — persona-first narrative."""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parents[1] / "Data-Navigator-Intake-May2026.pptx"

NAVY = RGBColor(0x0F, 0x27, 0x44)
BLUE = RGBColor(0x1E, 0x5A, 0x96)
ACCENT = RGBColor(0x15, 0x65, 0xC0)
MUTED = RGBColor(0x5C, 0x65, 0x70)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN_BG = RGBColor(0xE8, 0xF5, 0xE9)
AMBER_BG = RGBColor(0xFF, 0xF8, 0xE8)
GREY_BG = RGBColor(0xF4, 0xF6, 0xFA)


def set_title(shape, text, size=32, color=NAVY, bold=True):
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = PP_ALIGN.LEFT


def add_bullets(shape, items, size=16, color=NAVY):
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(6)


def add_slide_title(prs, title, subtitle=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bar = slide.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(1.15))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.22), Inches(9), Inches(0.7))
    set_title(tb, title, size=26, color=WHITE)
    if subtitle:
        st = slide.shapes.add_textbox(Inches(0.5), Inches(1.35), Inches(9), Inches(0.45))
        set_title(st, subtitle, size=14, color=MUTED, bold=False)
    return slide


def add_body_box(slide, top, height, bullets, size=15):
    box = slide.shapes.add_textbox(Inches(0.55), top, Inches(8.9), height)
    add_bullets(box, bullets, size=size)
    return box


def style_table_header(table, headers, bg=NAVY):
    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg
        for p in cell.text_frame.paragraphs:
            p.font.color.rgb = WHITE
            p.font.size = Pt(10)
            p.font.bold = True


def build():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # 1 Title — persona-led
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background()
    t = s.shapes.add_textbox(Inches(0.6), Inches(2.0), Inches(8.8), Inches(1.0))
    set_title(t, "Data Navigator", size=40, color=WHITE)
    sub = s.shapes.add_textbox(Inches(0.6), Inches(3.1), Inches(8.8), Inches(2.0))
    add_bullets(
        sub,
        [
            "Who we serve first — and what each persona needs from us",
            "Data Platforms Intake · May 2026",
            "Alation exit · governed discovery on OMS (experience layer only)",
        ],
        size=17,
        color=RGBColor(0xD0, 0xD8, 0xE8),
    )

    # 2 Persona landscape
    s = add_slide_title(
        prs,
        "Who we serve",
        "Opinionated by role — not one generic catalog for everyone",
    )
    table = s.shapes.add_table(6, 4, Inches(0.4), Inches(1.42), Inches(9.2), Inches(5.0)).table
    style_table_header(table, ["Persona", "Job-to-be-done", "Navigator MVP", "Channel"])
    rows = [
        (
            "Business / DNA consumer",
            "Find & trust the right metric or dataset fast",
            "PRIMARY — full discovery UX",
            "Navigator",
        ),
        (
            "Data analyst / BI",
            "Evaluate assets before building reports",
            "PRIMARY (shared path with consumer)",
            "Navigator",
        ),
        (
            "Data steward / owner",
            "Endorse, reconcile, attest definitions",
            "SECONDARY — thin stewardship",
            "Navigator",
        ),
        (
            "Privacy & compliance reviewer",
            "Evidence: classification, policy, defined vs observed",
            "SECONDARY — read + drill to asset",
            "Navigator",
        ),
        (
            "Data engineer",
            "Technical truth, lineage, SQL context",
            "Deep link only",
            "OMS UI",
        ),
    ]
    for r, row in enumerate(rows, 1):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                p.font.color.rgb = NAVY
            if c == 2 and "PRIMARY" in val:
                cell.fill.solid()
                cell.fill.fore_color.rgb = GREEN_BG
    note = s.shapes.add_textbox(Inches(0.55), Inches(6.55), Inches(8.9), Inches(0.55))
    note.text_frame.text = (
        "Phase 2 (separate surface): DRE / DPM remediation · Governance hub (DSAR, tracker, consent, ops pillars)"
    )
    note.text_frame.paragraphs[0].font.size = Pt(11)
    note.text_frame.paragraphs[0].font.italic = True
    note.text_frame.paragraphs[0].font.color.rgb = MUTED

    # 3 Primary persona — Business / DNA consumer
    s = add_slide_title(
        prs,
        "MVP focus: Business & analytics consumers",
        "When planning or reporting, they need an authoritative answer — not a wiki hunt",
    )
    add_body_box(
        s,
        Inches(1.48),
        Inches(1.35),
        [
            "North star: When I have a business question, I find the governed definition and owner in minutes — with confidence it matches production.",
        ],
        size=15,
    )
    add_body_box(
        s,
        Inches(2.35),
        Inches(3.8),
        [
            "“Which metric is official?” → Gold definition + provenance (corporate vs DEEPT domain)",
            "“Two dashboards disagree” → See gold standard and known conflicts",
            "“I’m new to the domain” → Browse approved datasets with owner, classification, quality tier",
            "“Vendor or exec asks what X means” → Citation-friendly definition package",
            "“Something is being deprecated” → Replacement asset and downstream context",
        ],
        size=14,
    )
    call = s.shapes.add_shape(1, Inches(0.55), Inches(5.35), Inches(8.9), Inches(0.75))
    call.fill.solid()
    call.fill.fore_color.rgb = GREEN_BG
    call.line.color.rgb = ACCENT
    tf = call.text_frame
    tf.text = "MVP screens serve these stories: search · browse · asset detail (gold) · glossary — not admin, social, or SQL playground."
    tf.paragraphs[0].font.size = Pt(12)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = NAVY

    # 4 Steward + Compliance
    s = add_slide_title(
        prs,
        "Also in MVP (secondary): Stewards & compliance reviewers",
        "Thin, purposeful paths — not full operational consoles",
    )
    # two columns via text boxes
    left = s.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.35), Inches(4.8))
    tf = left.text_frame
    tf.text = "Data steward / owner"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(14)
    tf.paragraphs[0].font.color.rgb = NAVY
    for item in [
        "Reconcile conflicting definitions → visible path to gold",
        "Council ratifies → gold status + provenance for consumers",
        "Onboard dataset → endorsement / warning signals",
        "Policy change → see impacted assets (via classifications)",
    ]:
        p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(12)
        p.level = 0
        p.space_before = Pt(6)

    right = s.shapes.add_textbox(Inches(5.0), Inches(1.5), Inches(4.45), Inches(4.8))
    tf = right.text_frame
    tf.text = "Privacy & compliance reviewer"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(14)
    tf.paragraphs[0].font.color.rgb = NAVY
    for item in [
        "Audit / legal demo → defined vs observed on same asset record",
        "PII / sensitivity question → classification + policy linkage",
        "DSAR pattern → locate consent / purpose metadata on assets",
        "Breadth without noise → filters; not every non–customer-facing asset for consumers",
    ]:
        p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(12)
        p.level = 0
        p.space_before = Pt(6)

    foot = s.shapes.add_textbox(Inches(0.55), Inches(6.2), Inches(8.9), Inches(0.6))
    foot.text_frame.text = "Rebecka’s reminder: legal often wants tools to self-serve — we enable review, not replace their process."
    foot.text_frame.paragraphs[0].font.size = Pt(11)
    foot.text_frame.paragraphs[0].font.italic = True
    foot.text_frame.paragraphs[0].font.color.rgb = MUTED

    # 5 Who we defer (and where they go)
    s = add_slide_title(prs, "Who we do not serve in Navigator MVP", "Clear handoffs — avoids “do everything” confusion")
    table = s.shapes.add_table(5, 3, Inches(0.45), Inches(1.45), Inches(9.1), Inches(4.5)).table
    style_table_header(table, ["Persona / need", "Why not Navigator MVP", "Where they go"])
    rows = [
        (
            "Data engineer (daily ops)",
            "Needs technical density & SQL",
            "OMS UI — Open in OMS from Navigator",
        ),
        (
            "DRE / automation",
            "Incident enrichment, programmatic workflows",
            "OMS / platform APIs (MVP: read API)",
        ),
        (
            "DSAR / tracker / consent operators",
            "Deep operational workflows exist today",
            "Existing pillar tools · Phase 2 governance hub shell",
        ),
        (
            "Metadata supply / scanning",
            "Not a UI problem",
            "Data 626 / MCI → OMS",
        ),
    ]
    for r, row in enumerate(rows, 1):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.font.color.rgb = NAVY

    # 6 One product, different views (Renat)
    s = add_slide_title(
        prs,
        "One catalog spine — different views per persona",
        "Same OMS objects; role-aware defaults and filters",
    )
    add_body_box(
        s,
        Inches(1.48),
        Inches(4.5),
        [
            "Consumers see approved, business-relevant assets — low noise (Renat: not every non–customer-facing dataset).",
            "Stewards see curation queues, conflicts, endorsement workflows on the same records.",
            "Compliance sees breadth, classifications, policy context, audit-friendly exports.",
            "Engineers jump to OMS for lineage depth, SQL, and operational metadata — same asset ID.",
            "We are not building five products — we are building persona-first entry points on one spine.",
        ],
        size=14,
    )

    # 7 How we enable personas (light architecture)
    s = add_slide_title(
        prs,
        "How we deliver for these personas",
        "We own the experience — 626 and OMS own supply and store",
    )
    add_body_box(
        s,
        Inches(1.45),
        Inches(2.5),
        [
            "626 / MCI improves definitions & coverage at source (incl. DEEPT domain metrics).",
            "OMS stores technical + business metadata and exposes APIs.",
            "Navigator is UI only: the place stewards and consumers go for governed discovery.",
            "Corporate / enterprise metrics (e.g. Kyle program): federated badges — not owned in Navigator.",
        ],
        size=14,
    )
    call = s.shapes.add_shape(1, Inches(0.55), Inches(4.2), Inches(8.9), Inches(0.9))
    call.fill.solid()
    call.fill.fore_color.rgb = RGBColor(0xE8, 0xEB, 0xFA)
    call.line.color.rgb = ACCENT
    tf = call.text_frame
    tf.text = (
        "Navigator vs OMS UI: OMS answers “how is it built?” · Navigator answers "
        "“what does it mean and can I trust it?” — complementary shells, one API."
    )
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = NAVY

    # 8 Asks
    s = add_slide_title(prs, "Timeline & asks", "Alation exit Oct 2026 · MVP ~8–10 months · capacity plan offline")
    add_body_box(
        s,
        Inches(1.45),
        Inches(2.0),
        [
            "MVP delivers primary consumer + thin steward/compliance paths first.",
            "626 prototypes in parallel; Navigator consumes via OMS.",
            "Governance command center (DSAR, tracker, ops pillars): phase 2 — same story, separate delivery.",
        ],
        size=14,
    )
    ask = s.shapes.add_textbox(Inches(0.55), Inches(4.0), Inches(8.9), Inches(2.2))
    add_bullets(
        ask,
        [
            "ASK 1: Endorse persona-first MVP (consumer primary; steward/compliance secondary).",
            "ASK 2: Confirm engineers use OMS UI; Navigator is not a second platform UI for them.",
            "ASK 3: Metadata WG — validate persona stories and 626 → OMS → Navigator handoffs.",
        ],
        size=15,
        color=ACCENT,
    )

    prs.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
