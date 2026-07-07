#!/usr/bin/env python3
"""Build Framing slide — Data Navigator on OMS (single-slide PPTX)."""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parents[1] / "Data-Navigator-Framing-Slide.pptx"

NAVY = RGBColor(0x0F, 0x27, 0x44)
BLUE = RGBColor(0x1E, 0x5A, 0x96)
LIGHT_BLUE = RGBColor(0x4A, 0x7F, 0xC4)
ACCENT = RGBColor(0x6B, 0x9F, 0xF0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MUTED = RGBColor(0xB8, 0xC8, 0xDC)
BODY = RGBColor(0xE8, 0xEE, 0xF5)
GOLD_BG = RGBColor(0x2A, 0x4A, 0x7A)
GREEN = RGBColor(0x7C, 0xE0, 0xA8)


def add_textbox(slide, left, top, width, height, text, size=12, bold=False, color=BODY, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    return box


def add_bullets(slide, left, top, width, height, items, size=11, color=BODY):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(4)
    return box


def stack_box(slide, left, top, width, height, label, sub, highlight=False):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    if highlight:
        shape.fill.fore_color.rgb = ACCENT
        shape.line.color.rgb = WHITE
        shape.line.width = Pt(2)
    else:
        shape.fill.fore_color.rgb = RGBColor(0x1A, 0x3A, 0x5C)
        shape.line.color.rgb = LIGHT_BLUE
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = label
    p.font.size = Pt(11 if not highlight else 12)
    p.font.bold = highlight
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    if sub:
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(8)
        p2.font.color.rgb = MUTED
        p2.alignment = PP_ALIGN.CENTER
    return shape


def build():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Background gradient band
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background()

    accent_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.05))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = BLUE
    accent_bar.line.fill.background()

    # Title block
    add_textbox(
        slide, Inches(0.45), Inches(0.18), Inches(7.5), Inches(0.45),
        "Framing: From Alation catalog to Data Navigator",
        size=24, bold=True, color=WHITE,
    )
    add_textbox(
        slide, Inches(0.45), Inches(0.62), Inches(9), Inches(0.35),
        "A persona-led discovery experience on OMS — not a second metadata platform",
        size=12, color=MUTED,
    )

    # --- LEFT: The shift ---
    add_textbox(slide, Inches(0.45), Inches(1.15), Inches(2.9), Inches(0.3), "THE SHIFT", size=10, bold=True, color=ACCENT)

    table = slide.shapes.add_table(4, 2, Inches(0.4), Inches(1.42), Inches(3.0), Inches(1.85)).table
    headers = ("Was (Alation)", "Is (Navigator)")
    rows = [
        ("Passive wiki, manual curation", "Governed discovery — find, trust, cite"),
        ("Often stale vs production", "Gold definitions + provenance on OMS"),
        ("One UI for many jobs", "Opinionated by role — consumers first"),
    ]
    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0x1A, 0x3A, 0x5C)
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(8)
            p.font.bold = True
            p.font.color.rgb = WHITE
    for r, row in enumerate(rows, 1):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(8)
                p.font.color.rgb = BODY

    add_textbox(slide, Inches(0.45), Inches(3.35), Inches(2.9), Inches(0.25), "Alation contract end: Oct 1, 2026", size=9, color=MUTED)

    # --- CENTER: Stack ---
    add_textbox(slide, Inches(3.55), Inches(1.15), Inches(3.2), Inches(0.3), "HOW IT FITS", size=10, bold=True, color=ACCENT)

    y = Inches(1.48)
    w = Inches(0.72)
    h = Inches(0.62)
    gap = Inches(0.08)
    xs = [Inches(3.5), Inches(4.3), Inches(5.1), Inches(5.9)]
    labels = [
        ("Sources", ""),
        ("626 / MCI", "supply"),
        ("OMS", "store + APIs"),
        ("Navigator", "experience"),
    ]
    for x, (lab, sub), hi in zip(xs, labels, [False, False, False, True]):
        stack_box(slide, x, y, w, h, lab, sub, highlight=hi)

    for x in [Inches(4.22), Inches(5.02), Inches(5.82)]:
        arr = slide.shapes.add_textbox(x, Inches(1.68), Inches(0.2), Inches(0.25))
        arr.text_frame.text = "→"
        arr.text_frame.paragraphs[0].font.size = Pt(14)
        arr.text_frame.paragraphs[0].font.color.rgb = MUTED

    callout = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.45), Inches(2.25), Inches(3.25), Inches(0.55))
    callout.fill.solid()
    callout.fill.fore_color.rgb = GOLD_BG
    callout.line.color.rgb = ACCENT
    tf = callout.text_frame
    tf.text = "We build Navigator (UI layer). 626 & OMS are partner programs."
    tf.paragraphs[0].font.size = Pt(10)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = WHITE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    add_textbox(
        slide, Inches(3.45), Inches(2.88), Inches(3.25), Inches(0.4),
        "626 → supply · OMS → store · Navigator → usable for the right persona",
        size=8, color=MUTED, align=PP_ALIGN.CENTER,
    )

    # --- RIGHT: Goal + MVP ---
    add_textbox(slide, Inches(6.95), Inches(1.15), Inches(2.85), Inches(0.3), "GOAL", size=10, bold=True, color=ACCENT)
    add_textbox(
        slide, Inches(6.95), Inches(1.42), Inches(2.9), Inches(1.05),
        "Help business & compliance users answer: What is this data? Can I trust it? Who owns it?",
        size=11, color=BODY,
    )

    add_textbox(slide, Inches(6.95), Inches(2.55), Inches(2.85), Inches(0.25), "MVP serves first", size=9, bold=True, color=GREEN)
    add_bullets(
        slide, Inches(6.95), Inches(2.78), Inches(2.9), Inches(1.1),
        [
            "Business / DNA consumer",
            "Data analyst / BI",
            "Steward (thin paths)",
            "Privacy / compliance (read)",
        ],
        size=10,
    )

    add_textbox(slide, Inches(6.95), Inches(3.95), Inches(2.85), Inches(0.25), "Phase 2 — not this MVP", size=9, bold=True, color=MUTED)
    add_bullets(
        slide, Inches(6.95), Inches(4.15), Inches(2.9), Inches(0.9),
        [
            "DSAR / tracker consoles",
            "DRE remediation hub",
            "Governance command center",
        ],
        size=9,
        color=MUTED,
    )

    # Footer tagline
    footer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(6.75), prs.slide_width, Inches(0.75))
    footer.fill.solid()
    footer.fill.fore_color.rgb = RGBColor(0x0A, 0x1C, 0x32)
    footer.line.fill.background()
    add_textbox(
        slide, Inches(0.45), Inches(6.88), Inches(9.1), Inches(0.45),
        "The governed place to find, trust, and use your data.",
        size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
    )

    prs.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
