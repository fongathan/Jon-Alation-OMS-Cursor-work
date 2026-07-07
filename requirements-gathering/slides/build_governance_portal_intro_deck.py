#!/usr/bin/env python3
"""Build Governance Portal intro decks in two styles: DEET (Alation) and Atlas."""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

SLIDES_DIR = Path(__file__).resolve().parent
OUT_DEET = SLIDES_DIR / "Data-Governance-Portal-Intro-DEET.pptx"
OUT_ATLAS = SLIDES_DIR / "Data-Governance-Portal-Intro-Atlas.pptx"
OUT_DEFAULT = SLIDES_DIR / "Data-Governance-Portal-Intro.pptx"

DEET_TEMPLATE = SLIDES_DIR / "_templates" / "DEET-Disney-Slide-Template.pptx"
ATLAS_TEMPLATE = SLIDES_DIR / "_templates" / "Atlas-Use-Cases-Sequencing-Template.pptx"

# --- Shared slide copy -------------------------------------------------------

TITLE = "Data Governance Portal"
SUBTITLE = (
    "One place to see privacy, security, and compliance posture — "
    "and what needs attention this week"
)

DIMENSIONS = [
    ("Privacy", "Consent · guest data requests · tracker remediation", "PCI & exception volume", RGBColor(0x0D, 0x8D, 0x7E)),
    ("Platform", "Stewards · classifications · policies", "Stewardship coverage", RGBColor(0x4F, 0x81, 0xBD)),
    ("Security", "Access reviews · GIS · data use approvals", "Access & GIS compliance", RGBColor(0xF7, 0x96, 0x46)),
    ("Regulatory", "Laws · incidents · audits", "Evidence readiness", RGBColor(0x80, 0x64, 0xA2)),
]

WHAT_IS = (
    "The Governance Portal is the privacy and data governance command center in the shared OMS shell — "
    "one front door for posture, exceptions, and evidence across guest and consumer data.\n\n"
    "It is not a replacement for specialist tools (consent, DSR, tracker, access, GIS). "
    "Design principle: unified experience, federated execution."
)

WHAT_DOES = [
    "One front door — consent, privacy requests, access, and compliance in one shared experience",
    "Governance Overview — simple scores for Privacy, Platform, Security, and Regulatory posture",
    "Work queues — surface what needs a human and route to the right downstream tool",
    "Defined vs observed — policy intent alongside what OMS actually sees on catalog assets",
    "Evidence export — packages for regulatory and internal audit requests",
    "Reduce dashboard sprawl — one front door instead of five disconnected URLs",
]

WHY = [
    "Each workstream has its own dashboard — hard to see overall risk or prioritize across dimensions",
    "Charts alone don't answer what needs a human this week — the Portal must triage and route",
    "Leadership asked for a single unified experience without rebuilding every backend",
    "As Alation exits, governance needs a stable home linked to OMS-backed catalog assets",
    "Privacy, legal & GIS get one map of consent, requests, and remediation",
    "Executives get posture indices and exportable evidence for council reviews",
]

WHERE = (
    "Phased delivery alongside the Navigator catalog migration:\n\n"
    "Now — Shell & prototypes: four dimension hubs, overview + work-queue tabs, KPI cards validated with privacy and legal.\n\n"
    "Next — Live data & routing: real feeds from consent, DSR, tracker, access, and GIS; role-based landing pages; "
    "handoffs into Navigator and downstream tools.\n\n"
    "Scale — Prove & expand: automated evidence packages, OMS integration for classifications and policies, "
    "enterprise expansion where policy aligns.\n\n"
    "Success measures: posture indices trending up, work-queue SLA closure, weekly adoption among privacy and "
    "stewardship roles, faster audit evidence production."
)

# --- DEET / Alation style ----------------------------------------------------

DEET_NAVY = RGBColor(0x15, 0x23, 0x42)
DEET_BLUE = RGBColor(0x1E, 0x40, 0xAF)
DEET_SLATE = RGBColor(0x33, 0x41, 0x55)
DEET_MUTED = RGBColor(0x47, 0x55, 0x69)
DEET_FOOT_MUTED = RGBColor(0x64, 0x74, 0x8B)
DEET_TOP_BG = RGBColor(0xEE, 0xF2, 0xFF)
DEET_FOOTER_BG = RGBColor(0xF1, 0xF5, 0xF9)
DEET_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DEET_BORDER = RGBColor(0xE2, 0xE8, 0xF0)
DEET_GREEN = RGBColor(0x15, 0x6F, 0x4A)
DEET_TEAL = RGBColor(0x0E, 0x94, 0x9A)
DEET_AMBER = RGBColor(0xB4, 0x53, 0x09)
DEET_SLIDE_W = Inches(13.333333333333334)
DEET_FOOTER = "DEET Data Governance  |  June 2026  |  Data Governance Portal Intro"


def deet_rgb(hex6: str) -> RGBColor:
    return RGBColor(int(hex6[0:2], 16), int(hex6[2:4], 16), int(hex6[4:6], 16))


def deet_para(p, text, size=11, color=DEET_SLATE, bold=False, font="Calibri", align=None):
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font
    if align is not None:
        p.alignment = align


def deet_send_back(slide, shape):
    sp_tree = slide.shapes._spTree  # noqa: SLF001
    el = shape._element  # noqa: SLF001
    sp_tree.remove(el)
    sp_tree.insert(2, el)


def deet_rect(slide, left, top, width, height, fill, line=None, radius=False):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line if line else fill
    if not line:
        shape.line.fill.background()
    return shape


def deet_footer(slide):
    deet_rect(slide, Inches(0), Inches(7.0), DEET_SLIDE_W, Inches(0.5), DEET_FOOTER_BG)
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(7.08), Inches(12.33), Inches(0.34))
    deet_para(tb.text_frame.paragraphs[0], DEET_FOOTER, size=9, color=DEET_FOOT_MUTED)


def deet_title_slide(prs, title, subtitle):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    top = deet_rect(slide, Inches(0), Inches(0), DEET_SLIDE_W, Inches(2.4), DEET_TOP_BG)
    deet_send_back(slide, top)
    bar = deet_rect(slide, Inches(0), Inches(2.4), DEET_SLIDE_W, Inches(0.06), DEET_NAVY)
    deet_send_back(slide, bar)
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(2.9), Inches(11.9), Inches(1.4))
    deet_para(tb.text_frame.paragraphs[0], title, size=40, color=DEET_NAVY, font="Calibri Light")
    st = slide.shapes.add_textbox(Inches(0.7), Inches(4.05), Inches(11.9), Inches(0.48))
    deet_para(st.text_frame.paragraphs[0], subtitle, size=18, color=DEET_MUTED)
    deet_footer(slide)
    return slide


def deet_content_slide(prs, title, subtitle=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header = deet_rect(slide, Inches(0), Inches(0), DEET_SLIDE_W, Inches(0.55), DEET_TOP_BG)
    deet_send_back(slide, header)
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.88), Inches(12.5), Inches(0.44))
    deet_para(tb.text_frame.paragraphs[0], title, size=24, color=DEET_NAVY, font="Calibri Light")
    top = Inches(1.36)
    if subtitle:
        st = slide.shapes.add_textbox(Inches(0.5), top, Inches(12.33), Inches(0.3))
        deet_para(st.text_frame.paragraphs[0], subtitle, size=12, color=DEET_MUTED)
        top = Inches(1.72)
    deet_footer(slide)
    return slide, top


def deet_bullets(slide, left, top, width, height, items, size=11):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {item}"
        p.font.size = Pt(size)
        p.font.color.rgb = DEET_SLATE
        p.font.name = "Calibri"
        p.space_before = Pt(5)


def deet_callout(slide, top, text):
    deet_rect(slide, Inches(0.5), top, Inches(12.33), Inches(0.58), deet_rgb("E0E7FF"), line=DEET_BLUE, radius=True)
    tb = slide.shapes.add_textbox(Inches(0.65), top + Inches(0.1), Inches(12.0), Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    deet_para(tf.paragraphs[0], text, size=13, color=DEET_NAVY, bold=True, font="Calibri Light")


def deet_feature_card(slide, left, top, width, height, num, heading, body, accent):
    deet_rect(slide, left, top, width, height, DEET_WHITE, line=DEET_BORDER, radius=True)
    oval = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.2), top + Inches(0.2), Inches(0.42), Inches(0.42))
    oval.fill.solid()
    oval.fill.fore_color.rgb = accent
    oval.line.fill.background()
    deet_para(oval.text_frame.paragraphs[0], str(num), size=16, color=DEET_WHITE, bold=True, align=PP_ALIGN.CENTER)
    tb = slide.shapes.add_textbox(left + Inches(0.78), top + Inches(0.12), width - Inches(0.95), Inches(0.55))
    tf = tb.text_frame
    tf.word_wrap = True
    deet_para(tf.paragraphs[0], heading, size=16, color=DEET_NAVY, font="Calibri Light")
    deet_para(tf.add_paragraph(), body, size=11, color=DEET_SLATE)


def deet_metric_tile(slide, left, top, width, big, detail, accent):
    deet_rect(slide, left, top, width, Inches(1.05), DEET_WHITE, line=DEET_BORDER, radius=True)
    tb = slide.shapes.add_textbox(left + Inches(0.12), top + Inches(0.1), width - Inches(0.2), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    deet_para(tf.paragraphs[0], big, size=22, color=accent, bold=True, font="Calibri Light")
    deet_para(tf.add_paragraph(), detail, size=8, color=DEET_MUTED)


def clear_slides(prs: Presentation) -> None:
    while len(prs.slides) > 0:
        r_id = prs.slides._sldIdLst[0].rId  # noqa: SLF001
        prs.part.drop_rel(r_id)
        del prs.slides._sldIdLst[0]


def build_deet() -> Path:
    template = DEET_TEMPLATE
    if not template.exists():
        template = Path.home() / "Downloads" / "Alation_Data_Catalog_Overview_05_2026_v2.pptx"
    if not template.exists():
        raise FileNotFoundError(f"DEET template not found: {DEET_TEMPLATE}")

    prs = Presentation(str(template))
    clear_slides(prs)

    deet_title_slide(prs, TITLE, SUBTITLE)

    slide, top = deet_content_slide(
        prs,
        "What is the Governance Portal?",
        "A command center for privacy and data governance — not a replacement for the tools you already use.",
    )
    cards = [
        (1, "One front door", "Consent, privacy requests, access reviews, and compliance each have their own dashboard today. The Portal brings the big picture together.", DEET_BLUE),
        (2, "See posture at a glance", "Governance Overview with simple scores for Privacy, Platform, Security, and Regulatory areas.", DEET_TEAL),
        (3, "Know what needs action", "Work queues surface overdue items and route you to the right tool.", DEET_AMBER),
        (4, "Prove it for audits", "Evidence packages tied to real catalog assets for legal and audit requests.", DEET_GREEN),
    ]
    cw, ch = Inches(6.04), Inches(2.05)
    for (left, y), (num, heading, body, accent) in zip(
        [(Inches(0.5), top), (Inches(6.8), top), (Inches(0.5), top + Inches(2.25)), (Inches(6.8), top + Inches(2.25))],
        cards,
    ):
        deet_feature_card(slide, left, y, cw, ch, num, heading, body, accent)
    deet_callout(slide, Inches(6.35), "Unified experience, federated execution — one portal for the story; specialist systems stay authoritative for deep work.")

    slide, top = deet_content_slide(prs, "Organized around four areas of work", "Grouped by what you need to do — not by org chart names.")
    tw, th = Inches(6.04), Inches(1.35)
    for i, (name, examples, _, accent) in enumerate(DIMENSIONS):
        col, row = i % 2, i // 2
        left = Inches(0.5) + col * Inches(6.3)
        y = top + row * Inches(1.5)
        deet_rect(slide, left, y, tw, th, DEET_WHITE, line=accent, radius=True)
        tb = slide.shapes.add_textbox(left + Inches(0.18), y + Inches(0.12), tw - Inches(0.3), th - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        deet_para(tf.paragraphs[0], name, size=16, color=DEET_NAVY, bold=True, font="Calibri Light")
        deet_para(tf.add_paragraph(), examples, size=10, color=DEET_MUTED)
    deet_callout(slide, top + Inches(3.15), "Portal = govern & prove  ·  Business Data Navigator = discover & steward")
    note = slide.shapes.add_textbox(Inches(0.5), top + Inches(3.85), Inches(12.33), Inches(0.3))
    deet_para(note.text_frame.paragraphs[0], "Same OMS metadata underneath — two modes in one shell, one source of truth.", size=10, color=DEET_MUTED, font="Calibri Light")

    slide, top = deet_content_slide(prs, "Why we're building it", "Dashboard sprawl makes it hard to see overall risk or know what needs a human this week.")
    col_w = Inches(4.05)
    columns = [
        ("THE PROBLEM", "Too many disconnected views", WHAT_DOES[:3], DEET_AMBER),
        ("WHO BENEFITS", "One map for many roles", WHY[4:6], DEET_BLUE),
        ("BEFORE → AFTER", "From sprawl to clarity", ["5+ URLs → one Overview", "Hunt for SLA breaches → unified queues", "Manual audit assembly → Portal export"], DEET_GREEN),
    ]
    for i, (label, heading, bullets, accent) in enumerate(columns):
        left = Inches(0.5) + i * col_w
        deet_rect(slide, left, top, col_w - Inches(0.12), Inches(4.95), DEET_WHITE, line=DEET_BORDER, radius=True)
        lb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.12), col_w - Inches(0.3), Inches(0.22))
        deet_para(lb.text_frame.paragraphs[0], label, size=10, color=accent, bold=True)
        hd = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.38), col_w - Inches(0.3), Inches(0.45))
        deet_para(hd.text_frame.paragraphs[0], heading, size=18, color=DEET_NAVY, font="Calibri Light")
        deet_bullets(slide, left + Inches(0.18), top + Inches(1.0), col_w - Inches(0.3), Inches(3.7), bullets)

    slide, top = deet_content_slide(prs, "Where we're headed", "Phased delivery alongside the Navigator catalog migration.")
    phases = [
        ("NOW", "Shell & prototypes", ["Dimension hubs + work queues", "KPI cards with privacy & legal", "Clear Portal vs Navigator split"], DEET_BLUE),
        ("NEXT", "Live data & routing", ["Real feeds from downstream systems", "Role-based landing pages", "Navigator handoffs"], DEET_TEAL),
        ("SCALE", "Prove & expand", ["Evidence automation", "OMS integration", "Enterprise expansion"], DEET_GREEN),
    ]
    pw = Inches(4.05)
    for i, (phase, ptitle, bullets, accent) in enumerate(phases):
        left = Inches(0.5) + i * pw
        deet_rect(slide, left, top, pw - Inches(0.12), Inches(3.35), DEET_WHITE, line=DEET_BORDER, radius=True)
        tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.12), pw - Inches(0.25), Inches(3.1))
        tf = tb.text_frame
        tf.word_wrap = True
        deet_para(tf.paragraphs[0], phase, size=9, color=accent, bold=True)
        deet_para(tf.add_paragraph(), ptitle, size=16, color=DEET_NAVY, font="Calibri Light")
        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(10)
            p.font.color.rgb = DEET_SLATE
            p.space_before = Pt(4)
    hdr = slide.shapes.add_textbox(Inches(0.5), Inches(5.05), Inches(12.0), Inches(0.25))
    deet_para(hdr.text_frame.paragraphs[0], "How we'll know it's working", size=11, color=DEET_BLUE, bold=True)
    metrics = [
        ("Posture scores", "Privacy & section indices trend up", DEET_BLUE),
        ("SLA closure", "Queue items closed on time", DEET_TEAL),
        ("Adoption", "Weekly use by privacy & stewardship", DEET_AMBER),
        ("Evidence speed", "Audit packages produced faster", DEET_GREEN),
    ]
    mw = Inches(3.05)
    for i, (label, detail, accent) in enumerate(metrics):
        deet_metric_tile(slide, Inches(0.5) + i * mw, Inches(5.35), mw - Inches(0.08), label, detail, accent)

    prs.save(OUT_DEET)
    prs.save(OUT_DEFAULT)
    return OUT_DEET


# --- Atlas style --------------------------------------------------------------

ATLAS_GRAY = RGBColor(0xCC, 0xCC, 0xCC)
ATLAS_DARK = RGBColor(0x36, 0x36, 0x36)
ATLAS_BLACK = RGBColor(0x00, 0x00, 0x00)
ATLAS_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ATLAS_FOOTER = "CONFIDENTIAL   |   THE WALT DISNEY COMPANY"
ATLAS_LAYOUT_TITLE_BODY = 1
ATLAS_LAYOUT_BLANK = 6  # fallback if needed


def atlas_para(p, text, size=11, color=ATLAS_DARK, bold=False, font="Calibri", align=None):
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font
    if align is not None:
        p.alignment = align


def atlas_set_ph(slide, idx: int, text: str) -> None:
    for shape in slide.shapes:
        if shape.is_placeholder and shape.placeholder_format.idx == idx:
            shape.text = text
            return


def atlas_footer(slide) -> None:
    tb = slide.shapes.add_textbox(Inches(0.45), Inches(6.95), Inches(8.0), Inches(0.35))
    atlas_para(tb.text_frame.paragraphs[0], ATLAS_FOOTER, size=9, color=ATLAS_DARK)


def atlas_box(slide, left, top, width, height, text, fill=ATLAS_GRAY, font_size=10, bold=False):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = ATLAS_GRAY
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.06)
    tf.margin_top = Inches(0.04)
    atlas_para(tf.paragraphs[0], text, size=font_size, color=ATLAS_DARK, bold=bold)
    return shape


def atlas_pill(slide, left, top, width, text, color: RGBColor):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.32))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.color.rgb = color
    tf = shape.text_frame
    tf.word_wrap = True
    atlas_para(tf.paragraphs[0], text, size=9, color=ATLAS_WHITE if color != ATLAS_GRAY else ATLAS_DARK, bold=True, align=PP_ALIGN.CENTER)
    return shape


def atlas_matrix_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[ATLAS_LAYOUT_TITLE_BODY])
    # Clear default placeholders visually by repurposing title
    atlas_set_ph(slide, 0, "Data Governance Portal — Four Dimensions Overview")
    for shape in slide.shapes:
        if shape.is_placeholder and shape.placeholder_format.idx == 1:
            shape.text = ""

    # Row / swimlane labels (Atlas slide 1 pattern)
    for y, label in [(Inches(1.37), "DIMENSION"), (Inches(2.47), "Scope"), (Inches(4.4), "What we are trying to achieve"), (Inches(6.35), "Key signal")]:
        tb = slide.shapes.add_textbox(Inches(0.15), y, Inches(1.2), Inches(0.3))
        atlas_para(tb.text_frame.paragraphs[0], label, size=9, color=ATLAS_DARK, bold=True)

    lane = slide.shapes.add_textbox(Inches(1.45), Inches(1.37), Inches(11.0), Inches(0.32))
    atlas_para(lane.text_frame.paragraphs[0], "PRIVACY  ·  PLATFORM  ·  SECURITY  ·  REGULATORY POSTURE", size=10, color=ATLAS_DARK, bold=True)

    col_w = Inches(2.85)
    gap = Inches(0.18)
    start_x = Inches(1.45)
    for i, (name, scope, kpi, color) in enumerate(DIMENSIONS):
        left = start_x + i * (col_w + gap)
        atlas_pill(slide, left, Inches(1.78), col_w, name.upper(), color)
        atlas_box(slide, left, Inches(2.22), col_w, Inches(0.72), name, font_size=11, bold=True)
        atlas_box(slide, left, Inches(3.12), col_w, Inches(2.87), scope, font_size=10)
        atlas_box(slide, left, Inches(6.11), col_w, Inches(0.72), kpi, font_size=10, bold=True)

    atlas_footer(slide)
    return slide


def atlas_detail_slide(prs, title: str, body: str):
    slide = prs.slides.add_slide(prs.slide_layouts[ATLAS_LAYOUT_TITLE_BODY])
    atlas_set_ph(slide, 0, title)
    atlas_set_ph(slide, 1, f"Description: {body}")
    atlas_footer(slide)
    return slide


def build_atlas() -> Path:
    if not ATLAS_TEMPLATE.exists():
        raise FileNotFoundError(f"Atlas template not found: {ATLAS_TEMPLATE}")

    prs = Presentation(str(ATLAS_TEMPLATE))
    clear_slides(prs)

    atlas_matrix_slide(prs)
    atlas_detail_slide(prs, "What is the Governance Portal?", WHAT_IS)
    atlas_detail_slide(prs, "What it does for the organization", "\n\n".join(f"• {b}" for b in WHAT_DOES))
    atlas_detail_slide(prs, "Why we're building it", "\n\n".join(f"• {b}" for b in WHY))
    atlas_detail_slide(prs, "Where we're headed", WHERE)

    prs.save(OUT_ATLAS)
    return OUT_ATLAS


def build():
    deet = build_deet()
    atlas = build_atlas()
    print(f"Wrote {deet} (DEET / Alation style, {len(Presentation(str(deet)).slides)} slides)")
    print(f"Wrote {atlas} (Atlas style, {len(Presentation(str(atlas)).slides)} slides)")
    print(f"Wrote {OUT_DEFAULT} (default copy = DEET)")


if __name__ == "__main__":
    build()
