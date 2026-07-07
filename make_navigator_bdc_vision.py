#!/usr/bin/env python3
"""Navigator - Business Data Catalog : Vision deck generator.

A ~10-slide socialization deck for the Navigator Business Data Catalog
(the Alation -> OMS migration slice of Navigator). Clean light "compass"
theme: deep indigo + teal accents on paper. Distinct look from the
dark/gold source deck, but the same kind of vision story:
problem -> solution -> features -> metrics -> roadmap.
"""

import os
import sys

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE

# ---------------------------------------------------------------- palette
INK      = RGBColor(0x10, 0x1A, 0x2E)   # primary text
INK_SOFT = RGBColor(0x33, 0x40, 0x5C)
MUTE     = RGBColor(0x6B, 0x77, 0x8C)   # secondary text
PAPER    = RGBColor(0xFF, 0xFF, 0xFF)
MIST     = RGBColor(0xF4, 0xF7, 0xFB)   # page background
CLOUD    = RGBColor(0xED, 0xF1, 0xF8)   # subtle fill
LINE     = RGBColor(0xDD, 0xE4, 0xF0)   # card borders

INDIGO   = RGBColor(0x1E, 0x2B, 0x52)   # deep brand
INDIGO2  = RGBColor(0x2C, 0x47, 0x8C)
BLUE     = RGBColor(0x2D, 0x6C, 0xE0)   # primary accent
TEAL     = RGBColor(0x10, 0x9A, 0xA6)
VIOLET   = RGBColor(0x6A, 0x57, 0xD6)
AMBER    = RGBColor(0xCF, 0x8A, 0x00)
GREEN    = RGBColor(0x1F, 0x9D, 0x6B)
RED      = RGBColor(0xD2, 0x44, 0x4E)
ROSE     = RGBColor(0xC7, 0x3E, 0x73)

WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
CHIP_BG  = RGBColor(0xEA, 0xF0, 0xFB)

HEAD_FONT = "Helvetica Neue"
BODY_FONT = "Helvetica Neue"

FOOTER = "Navigator  \u00b7  Business Data Catalog  \u00b7  Data Governance  \u00b7  DEEPT \u00b7  2026   |   Confidential"

HERE = os.path.dirname(os.path.abspath(__file__))
DECK_ICONS_DIR = os.path.join(HERE, "assets", "deck-icons")

# Icons extracted from the user-edited deck (slide, filename, left, top, width in inches)
DECK_ICON_PLACEMENTS = [
    (1, "slide01_00_62600921.png", 1.5, 4.74, 1.05),
    (3, "slide03_01_995ecb1d.png", 0.82, 2.79, 0.4),
    (3, "slide03_02_ed98cc58.png", 6.95, 2.77, 0.45),
    (3, "slide03_03_13dd0a54.png", 3.87, 2.74, 0.5),
    (3, "slide03_04_d4d8f454.png", 3.82, 2.74, 0.59),
    (3, "slide03_05_e3f642c1.png", 10.02, 2.76, 0.49),
    (3, "slide03_06_a340f600.png", 10.01, 2.72, 0.6),
    (5, "slide05_07_386cf5cf.png", 0.74, 2.69, 0.61),
    (5, "slide05_08_5d10ce72.png", 3.82, 2.74, 0.6),
    (5, "slide05_09_2c4a374a.png", 6.85, 2.81, 0.63),
    (5, "slide05_10_4905b258.png", 10.01, 2.77, 0.61),
    (7, "slide07_11_4ea9a047.png", 0.74, 4.55, 0.57),
    (7, "slide07_12_6bf96acf.png", 8.99, 4.59, 0.54),
    (7, "slide07_13_3d181086.png", 8.98, 4.58, 0.59),
    (8, "slide08_14_edc3cf61.png", 0.83, 3.9, 0.44),
    (8, "slide08_15_d68b160d.png", 4.97, 3.92, 0.45),
    (8, "slide08_16_2a5bf881.png", 9.0, 3.92, 0.55),
]

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height


# ---------------------------------------------------------------- helpers
def slide():
    return prs.slides.add_slide(prs.slide_layouts[6])


def rect(s, left, top, width, height, fill=None, line=None, line_w=None,
         shape=MSO_SHAPE.RECTANGLE):
    shp = s.shapes.add_shape(shape, left, top, width, height)
    shp.shadow.inherit = False
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = line_w or Pt(1)
    return shp


def gradient(shp, c1, c2, angle=90):
    shp.fill.gradient()
    stops = shp.fill.gradient_stops
    stops[0].position = 0.0
    stops[0].color.rgb = c1
    stops[1].position = 1.0
    stops[1].color.rgb = c2
    try:
        shp.fill.gradient_angle = angle
    except Exception:
        pass
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def text(s, left, top, width, height, runs, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, space_after=Pt(5), line_spacing=1.0):
    box = s.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    first = True
    for item in runs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = item.get("align", align)
        p.space_after = item.get("space_after", space_after)
        p.space_before = item.get("space_before", Pt(0))
        p.line_spacing = item.get("line_spacing", line_spacing)
        parts = item.get("parts")
        if parts is None:
            parts = [(item.get("text", ""), item)]
        for txt, st in parts:
            r = p.add_run()
            r.text = txt
            f = r.font
            f.size = st.get("size", Pt(14))
            f.bold = st.get("bold", False)
            f.italic = st.get("italic", False)
            f.color.rgb = st.get("color", INK)
            f.name = st.get("font", BODY_FONT)
    return box


def eyebrow(s, left, top, width, label, color=BLUE):
    # spaced-out uppercase label
    spaced = "   ".join(list(label)) if False else label
    text(s, left, top, width, Inches(0.3),
         [{"text": label, "size": Pt(11), "bold": True, "color": color,
           "font": HEAD_FONT}])


def footer(s):
    rect(s, Inches(0.55), Inches(6.92), Inches(12.23), Pt(1), fill=LINE)
    text(s, Inches(0.55), Inches(7.02), Inches(12.23), Inches(0.3),
         [{"text": FOOTER, "size": Pt(8.5), "color": MUTE, "align": PP_ALIGN.CENTER}],
         align=PP_ALIGN.CENTER)


def title_block(s, kicker, title, kicker_color=BLUE):
    eyebrow(s, Inches(0.6), Inches(0.42), Inches(12), kicker, kicker_color)
    text(s, Inches(0.57), Inches(0.66), Inches(12.2), Inches(0.8),
         [{"text": title, "size": Pt(30), "bold": True, "color": INK, "font": HEAD_FONT}])


def bg(s, color=MIST):
    rect(s, 0, 0, SW, SH, fill=color)


def notes(s, txt):
    s.notes_slide.notes_text_frame.text = txt


def card(s, left, top, width, height, accent, title, body_runs,
         icon=None, title_color=None, fill=PAPER):
    rect(s, left, top, width, height, fill=fill, line=LINE, line_w=Pt(1))
    rect(s, left, top, width, Inches(0.09), fill=accent)  # top accent bar
    tcol = title_color or INK
    ty = top + Inches(0.30)
    if icon:
        text(s, left + Inches(0.28), ty, Inches(0.6), Inches(0.4),
             [{"text": icon, "size": Pt(18), "color": accent}])
        tx = left + Inches(0.78)
    else:
        tx = left + Inches(0.28)
    text(s, tx, ty, width - (tx - left) - Inches(0.2), Inches(0.5),
         [{"text": title, "size": Pt(14.5), "bold": True, "color": tcol, "font": HEAD_FONT}])
    text(s, left + Inches(0.28), top + Inches(0.86), width - Inches(0.56),
         height - Inches(1.0), body_runs, line_spacing=1.05)


def bullets(items, color=INK_SOFT, size=Pt(12.5), gap=Pt(8), marker="\u2014  "):
    runs = []
    for it in items:
        runs.append({"text": marker + it, "size": size, "color": color,
                     "space_after": gap, "line_spacing": 1.06})
    return runs


def place_deck_icons(s, slide_num):
    for sn, fname, left, top, width in DECK_ICON_PLACEMENTS:
        if sn != slide_num:
            continue
        path = os.path.join(DECK_ICONS_DIR, fname)
        if os.path.exists(path):
            s.shapes.add_picture(path, Inches(left), Inches(top), width=Inches(width))


# ============================================================ SLIDE 1 — TITLE
s = slide()
bg(s, PAPER)
# left brand panel with gradient
panel = rect(s, 0, 0, Inches(4.35), SH)
gradient(panel, INDIGO, INDIGO2, angle=120)
rect(s, Inches(4.35), 0, Inches(0.06), SH, fill=TEAL)  # seam accent

# compass mark (drawn ring + N), as kept in the edited deck
rect(s, Inches(1.05), Inches(1.45), Inches(2.05), Inches(2.05),
     fill=None, line=TEAL, line_w=Pt(2.25), shape=MSO_SHAPE.OVAL)
text(s, Inches(1.05), Inches(1.52), Inches(2.05), Inches(1.9),
     [{"text": "N", "size": Pt(78), "bold": True, "color": WHITE, "font": HEAD_FONT,
       "align": PP_ALIGN.CENTER}], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, Inches(0.85), Inches(3.85), Inches(2.6), Inches(0.4),
     [{"text": "N A V I G A T O R", "size": Pt(15), "bold": True, "color": WHITE,
       "font": HEAD_FONT, "align": PP_ALIGN.CENTER}], align=PP_ALIGN.CENTER)
text(s, Inches(0.85), Inches(4.22), Inches(2.6), Inches(0.4),
     [{"text": "Business Data Catalog", "size": Pt(11.5), "color": RGBColor(0xB9, 0xC6, 0xE6),
       "font": HEAD_FONT, "align": PP_ALIGN.CENTER}], align=PP_ALIGN.CENTER)

# right content
RX = Inches(4.95)
text(s, RX, Inches(1.30), Inches(7.9), Inches(0.4),
     [{"text": "ALATION MIGRATION  \u00b7  NEW GOVERNED CATALOG ON INTERNAL SOLUTION", "size": Pt(12),
       "bold": True, "color": TEAL, "font": HEAD_FONT}])
text(s, RX - Inches(0.03), Inches(1.66), Inches(8.0), Inches(1.7),
     [{"text": "The Business Data Catalog", "size": Pt(40), "bold": True, "color": INK,
       "font": HEAD_FONT, "space_after": Pt(0), "line_spacing": 1.0},
      {"text": "for Disney Entertainment ESPN Product & Technology", "size": Pt(40), "bold": True, "color": BLUE,
       "font": HEAD_FONT, "line_spacing": 1.0}])
text(s, RX, Inches(3.18), Inches(7.85), Inches(0.95),
     [{"text": "The in-house, business-first experience built on OMS \u2014 governed discovery, "
               "glossary, lineage, and trust \u2014 replacing Alation while surfacing new automation capabilities.",
       "size": Pt(14.5), "color": INK_SOFT, "italic": True, "line_spacing": 1.12}])

# capability chips grid
chips = ["Unified Search & Discovery", "Business Glossary", "Lineage & Asset Detail",
         "Trust Signals", "Stewardship & Ownership", "Classification & Bulk Governance",
         "AI-Readiness", "OMS Composability"]
cx0, cy0 = RX, Inches(4.18)
cw, ch, gx, gy = Inches(3.86), Inches(0.46), Inches(0.16), Inches(0.16)
for i, c in enumerate(chips):
    r, col = divmod(i, 2)
    x = cx0 + col * (cw + gx)
    y = cy0 + r * (ch + gy)
    rect(s, x, y, cw, ch, fill=CHIP_BG, line=LINE, line_w=Pt(0.75),
         shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, x + Inches(0.18), y, cw - Inches(0.3), ch,
         [{"text": c, "size": Pt(11.5), "bold": True, "color": INDIGO2, "font": HEAD_FONT}],
         anchor=MSO_ANCHOR.MIDDLE)

text(s, RX, Inches(6.78), Inches(7.85), Inches(0.4),
     [{"text": "20 prioritized features  \u00b7  3 delivery phases  \u00b7  1 governed experience on internal tools",
       "size": Pt(12.5), "bold": True, "color": TEAL, "font": HEAD_FONT}])

place_deck_icons(s, 1)

notes(s, "Navigator is the umbrella product; the Business Data Catalog (BDC) is the slice of "
         "Navigator that serves the Alation migration and the broader business-data-catalog "
         "requirements. This deck socializes what the Alation migration means and why \u2014 the "
         "in-house, governed catalog experience on OMS that replaces Alation with no loss of "
         "functionality. Stack: 626/MCI supplies metadata, OMS stores it, Navigator is the "
         "governed UX. ~531 Alation users; contract reality Oct 1 2026; cutover target Sep 2027.")


# ============================================================ SLIDE 2 — TRANSFORMATION
s = slide()
bg(s)
title_block(s, "WHY WE'RE MOVING", "The Catalog Transformation")
text(s, Inches(0.6), Inches(1.22), Inches(12), Inches(0.4),
     [{"text": "What the catalog looks like on Alation today vs. on Navigator + OMS",
       "size": Pt(13.5), "italic": True, "color": MUTE}])

col_w = Inches(5.95)
col_top = Inches(1.78)
col_h = Inches(4.95)
lx = Inches(0.6)
rx = lx + col_w + Inches(0.33)

# TODAY card
rect(s, lx, col_top, col_w, col_h, fill=PAPER, line=LINE, line_w=Pt(1))
rect(s, lx, col_top, col_w, Inches(0.62), fill=CLOUD)
text(s, lx + Inches(0.3), col_top, col_w - Inches(0.6), Inches(0.62),
     [{"text": "TODAY  \u00b7  ALATION (EXITING)", "size": Pt(13), "bold": True,
       "color": MUTE, "font": HEAD_FONT}], anchor=MSO_ANCHOR.MIDDLE)
today = [
    "External vendor catalog: ~531 users, legacy system for 6 years ",
    "Stale catalog, requiring manual updates & human curation",
    "Unable to integrate directly with Data Sources as 3rd party",
    "Business and technical metadata live in separate worlds",
    "\u201cWhere is X?\u201d fragmented in catalog, chats, and tribal knowledge",
    "Glossary, lineage, and trust flags locked in a tool we're leaving",
    "In need of stronger AI-readiness signals for analytics and AI teams",
    "Vendor lock-in \u2014 limited customization and automation",
]
text(s, lx + Inches(0.32), col_top + Inches(0.85), col_w - Inches(0.64), col_h - Inches(1.0),
     bullets(today, color=INK_SOFT, size=Pt(12.5), gap=Pt(10), marker="\u2022  "))

# WITH NAVIGATOR card
rect(s, rx, col_top, col_w, col_h, fill=PAPER, line=BLUE, line_w=Pt(1.5))
rect(s, rx, col_top, col_w, Inches(0.62), fill=BLUE)
text(s, rx + Inches(0.3), col_top, col_w - Inches(0.6), Inches(0.62),
     [{"text": "WITH NAVIGATOR  \u00b7  ON OMS", "size": Pt(13), "bold": True,
       "color": WHITE, "font": HEAD_FONT}], anchor=MSO_ANCHOR.MIDDLE)
withnav = [
    "In-house, enterprise-owned experience on top of OMS \u2014 no vendor lock-in",
    "Business + technical metadata unified on one spine",
    "Self-service discovery: search, browse, home for reconciled metrics and asset descriptions to surface",
    "Stewardship and trust signals first-class in the UI",
    "Glossary, lineage, and classifications governed and linkable",
    "AI-readiness attributes so teams pick steward-attested data",
    "Fed by 626/MCI supply, stored in OMS, served as governed UX",
]
wr = []
for it in withnav:
    wr.append({"parts": [("\u25B8  ", {"size": Pt(12.5), "bold": True, "color": TEAL}),
                         (it, {"size": Pt(12.5), "color": INK})],
               "space_after": Pt(10), "line_spacing": 1.06})
text(s, rx + Inches(0.32), col_top + Inches(0.85), col_w - Inches(0.64), col_h - Inches(1.0), wr)

footer(s)
notes(s, "The headline: this is not a downgrade. We keep what teams value in Alation and gain an "
         "enterprise-owned, extensible catalog where business and technical metadata finally live "
         "together. 626/MCI improves metadata supply, OMS stores and serves it, Navigator is the "
         "governed experience layer.")


# ============================================================ SLIDE 3 — SEARCH & DISCOVERY
s = slide()
bg(s)
title_block(s, "FEATURE 01  \u00b7  ONE SEARCH ACROSS BUSINESS + TECHNICAL  \u00b7  SELF-SERVICE",
            "Unified Search & Discovery", BLUE)

# lead banner
lead_top = Inches(1.45)
rect(s, Inches(0.6), lead_top, Inches(12.18), Inches(0.82), fill=CHIP_BG,
     line=BLUE, line_w=Pt(1))
rect(s, Inches(0.6), lead_top, Inches(0.14), Inches(0.82), fill=BLUE)
text(s, Inches(0.95), lead_top, Inches(11.6), Inches(0.82),
     [{"parts": [("Answer \u201cwhat exists?\u201d in one place. ", {"size": Pt(14.5), "bold": True, "color": INK}),
                 ("Tables, columns, glossary terms, and docs in a single ranked result \u2014 "
                  "with filters that reflect trust, domain, and context, not a data source-only technical search.",
                  {"size": Pt(14.5), "color": INK_SOFT})], "line_spacing": 1.08}],
     anchor=MSO_ANCHOR.MIDDLE)

cards = [
    (BLUE, "\U0001F50D", "Search business + technical",
     "One query spans tables, columns, business terms, and articles \u2014 ranked by relevance and usage. Replaces the daily Alation search teams rely on."),
    (TEAL, "\U0001F5C2", "Hierarchical browse",
     "Explore data source \u2192 schema \u2192 table \u2192 column without knowing exact names \u2014 leverages the mental model people already have."),
    (VIOLET, "\U0001F4C4", "Asset detail answers \u201ccan I use this?\u201d",
     "Business description, owners/stewards, tags, and lineage entry points on one screen \u2014 metadata-first, not hollow placeholders."),
    (GREEN, "\U0001F510", "Access-aware by design",
     "SSO and role-aware results. Users see only what they're permitted to \u2014 discovery never bypasses governance."),
]
cw = Inches(2.92)
gap = Inches(0.16)
cx = Inches(0.6)
cy = Inches(2.55)
chh = Inches(3.95)
for i, (acc, ic, t, b) in enumerate(cards):
    x = cx + i * (cw + gap)
    card(s, x, cy, cw, chh, acc, t,
         [{"text": b, "size": Pt(12.5), "color": INK_SOFT, "line_spacing": 1.1}], icon=ic)

place_deck_icons(s, 3)

footer(s)
notes(s, "F01-F03. Parity for the #1 thing people do in Alation: find data and decide whether to "
         "use it. Search must cover business + technical objects together; browse mirrors the "
         "Alation hierarchy; asset detail surfaces ownership, tags, and lineage; all access-gated.")


# ============================================================ SLIDE 4 — BUSINESS GLOSSARY
s = slide()
bg(s)
title_block(s, "FEATURE 02  \u00b7  ONE SHARED VOCABULARY  \u00b7  LINKED TO ASSETS",
            "Business Glossary", TEAL)

# left narrative column
lx = Inches(0.6)
lw = Inches(5.55)
top = Inches(1.6)

rect(s, lx, top, lw, Inches(2.05), fill=PAPER, line=LINE, line_w=Pt(1))
rect(s, lx, top, lw, Inches(0.09), fill=AMBER)
text(s, lx + Inches(0.3), top + Inches(0.26), lw - Inches(0.6), Inches(0.4),
     [{"text": "The problem today", "size": Pt(14), "bold": True, "color": INK, "font": HEAD_FONT}])
text(s, lx + Inches(0.3), top + Inches(0.78), lw - Inches(0.6), Inches(1.2),
     [{"text": "\u201cPaid subscriber,\u201d \u201cactive subscriber,\u201d \u201ccustomer\u201d mean different "
               "things across Disney+, Hulu, and ESPN. Established definitions must live in the catalog \u2014 "
               "so every cross-segment effort does not start with a vocabulary negotiation.",
       "size": Pt(12.5), "color": INK_SOFT, "line_spacing": 1.12}])

top2 = top + Inches(2.25)
rect(s, lx, top2, lw, Inches(2.5), fill=PAPER, line=TEAL, line_w=Pt(1.5))
rect(s, lx, top2, lw, Inches(0.09), fill=TEAL)
text(s, lx + Inches(0.3), top2 + Inches(0.26), lw - Inches(0.6), Inches(0.4),
     [{"text": "With Navigator - business data catalog", "size": Pt(14), "bold": True, "color": TEAL, "font": HEAD_FONT}])
text(s, lx + Inches(0.3), top2 + Inches(0.78), lw - Inches(0.6), Inches(1.6),
     [{"text": "One vocabulary for the organization \u2014 terms, definitions, synonyms, business "
               "formula, and stewardship \u2014 linked to the actual catalog assets that implement "
               "them, so language and inventory stay connected. Alation terms migrate with high "
               "fidelity and their asset links are preserved, until updated when AI automated capabilities are ready. ",
       "size": Pt(12.5), "color": INK, "line_spacing": 1.14}])

# right 2x2 cards
rcards = [
    (BLUE, "Authoritative definitions", "Term, business formula, data domain, and both business + technical steward in one place."),
    (TEAL, "Linked to assets", "Each term connects to the tables and columns that implement it \u2014 no orphan definitions."),
    (VIOLET, "Metric conflict resolution", "Automated metric definition & conflict resolution capabilities surface here."),
    (GREEN, "See who owns each term", "Steward name and contact surfaced with every definition \u2014 questions route themselves."),
]
rx = lx + lw + Inches(0.33)
rw = Inches(2.97)
rh = Inches(2.30)
rgap = Inches(0.16)
for i, (acc, t, b) in enumerate(rcards):
    r, c = divmod(i, 2)
    x = rx + c * (rw + rgap)
    y = Inches(1.6) + r * (rh + rgap)
    card(s, x, y, rw, rh, acc, t, [{"text": b, "size": Pt(12), "color": INK_SOFT, "line_spacing": 1.1}])

footer(s)
notes(s, "F04. The glossary is the highest-fidelity migration risk and the biggest day-to-day "
         "governance win. One shared, stewarded vocabulary linked to real assets; Alation terms "
         "preserved with their links intact.")


# ============================================================ SLIDE 5 — LINEAGE & ASSET DETAIL
s = slide()
bg(s)
title_block(s, "FEATURE 03  \u00b7  UPSTREAM / DOWNSTREAM  \u00b7  IMPACT & COMPLIANCE",
            "Data Lineage & Provenance", VIOLET)

lead_top = Inches(1.45)
rect(s, Inches(0.6), lead_top, Inches(12.18), Inches(0.82), fill=CHIP_BG,
     line=VIOLET, line_w=Pt(1))
rect(s, Inches(0.6), lead_top, Inches(0.14), Inches(0.82), fill=VIOLET)
text(s, Inches(0.95), lead_top, Inches(11.6), Inches(0.82),
     [{"parts": [("Where did this data come from, and what breaks if it changes? ", {"size": Pt(14.5), "bold": True, "color": INK}),
                 ("See upstream and downstream context for impact analysis and compliance "
                  "traceability \u2014 table-level at minimum, column/dataflow where validated.",
                  {"size": Pt(14.5), "color": INK_SOFT})], "line_spacing": 1.08}],
     anchor=MSO_ANCHOR.MIDDLE)

cards = [
    (VIOLET, "\U0001F500", "Impact analysis",
     "Trace what feeds a table and what consumes it before you change or deprecate it \u2014 fewer surprises, safer decommissions."),
    (BLUE, "\U0001F517", "Provenance for trust",
     "Where did it come from, what transformed it, who certified it? Provenance makes cross-segment activation defensible."),
    (TEAL, None, "Composable handoff onto OMS",
     "Drop from the business view into full technical / lineage context in OMS without losing your place \u2014 one spine, two shells."),
    (GREEN, "\U0001F6E1", "Compliance traceability",
     "Lineage supports audit and privacy narratives \u2014 evidence-friendly views instead of manual screenshots."),
]
cw = Inches(2.92)
gap = Inches(0.16)
cx = Inches(0.6)
cy = Inches(2.55)
chh = Inches(3.95)
for i, (acc, ic, t, b) in enumerate(cards):
    x = cx + i * (cw + gap)
    card(s, x, cy, cw, chh, acc, t,
         [{"text": b, "size": Pt(12.5), "color": INK_SOFT, "line_spacing": 1.1}], icon=ic)

place_deck_icons(s, 5)

footer(s)
notes(s, "F05 + F11. Lineage depth is validated against actual Alation usage by persona; table-level "
         "minimum with column/dataflow where teams need it. The composability point matters: "
         "Navigator is the business shell, OMS is the technical shell, both on one metadata spine.")


# ============================================================ SLIDE 6 — TRUST & STEWARDSHIP
s = slide()
bg(s)
title_block(s, "FEATURE 04  \u00b7  ENDORSE / WARN / DEPRECATE  \u00b7  ACCOUNTABLE OWNERS",
            "Trust Signals & Stewardship", GREEN)

# left: trust dashboard
lx = Inches(0.6)
lw = Inches(5.95)
top = Inches(1.62)
dh = Inches(5.05)
rect(s, lx, top, lw, dh, fill=PAPER, line=LINE, line_w=Pt(1))
text(s, lx + Inches(0.3), top + Inches(0.22), lw - Inches(0.6), Inches(0.4),
     [{"text": "Live trust view (illustrative)", "size": Pt(13), "bold": True,
       "color": INK, "font": HEAD_FONT}])

rows = [
    ("DIM_DISNEY_CUSTOMER_ENGAGEMENT", "Endorsed", GREEN),
    ("VIEW_DIM_CUSTOMER  (Hulu)", "Endorsed", GREEN),
    ("DIM_CUSTOMER_TYPES  (Subs)", "Warning", AMBER),
    ("Paid Subscribers  (metric)", "Endorsed", GREEN),
    ("GDPR Scoped tables", "Endorsed", GREEN),
    ("LEGACY_SUBS_ROLLUP_V1", "Deprecated", RED),
    ("CCPA Scoped views", "Warning", AMBER),
]
ry = top + Inches(0.72)
rhh = Inches(0.55)
for name, status, col in rows:
    rect(s, lx + Inches(0.3), ry + Inches(0.14), Inches(0.16), Inches(0.16),
         fill=col, shape=MSO_SHAPE.OVAL)
    text(s, lx + Inches(0.62), ry, Inches(3.55), rhh,
         [{"text": name, "size": Pt(11.5), "color": INK, "font": BODY_FONT}],
         anchor=MSO_ANCHOR.MIDDLE)
    pill = rect(s, lx + lw - Inches(1.55), ry + Inches(0.08), Inches(1.25), Inches(0.38),
                fill=None, line=col, line_w=Pt(1.25), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, lx + lw - Inches(1.55), ry + Inches(0.08), Inches(1.25), Inches(0.38),
         [{"text": status, "size": Pt(10.5), "bold": True, "color": col,
           "align": PP_ALIGN.CENTER, "font": HEAD_FONT}], anchor=MSO_ANCHOR.MIDDLE)
    ry += rhh + Inches(0.085)

# right: stewardship cards
rx = lx + lw + Inches(0.33)
rw = Inches(5.9)
rcards = [
    (GREEN, "Credible paths, clearly marked", "Endorse / warn / deprecate communicate intended use and risk \u2014 trusted paths vs. assets being phased out."),
    (BLUE, "Every critical asset has an owner", "Accountable business and technical stewards visible in the UI and in reports \u2014 a federated stewardship model, not a spreadsheet."),
    (AMBER, "Gap alerts", "Assets without a steward are surfaced automatically \u2014 no manual auditing to find governance gaps."),
    (VIOLET, "Stewardship at scale", "Curate, endorse, and reconcile definitions across hundreds of assets \u2014 with the bulk paths on the next slide."),
]
ry2 = Inches(1.62)
rhh2 = Inches(1.16)
for acc, t, b in rcards:
    card(s, rx, ry2, rw, rhh2, acc, t,
         [{"text": b, "size": Pt(12), "color": INK_SOFT, "line_spacing": 1.08}])
    ry2 += rhh2 + Inches(0.14)

footer(s)
notes(s, "F07 + F08. Trust flags (endorse/warn/deprecate) are in use in Alation today and must "
         "carry over. Ownership is visible in UI and reports; gap alerts find unstewarded assets. "
         "Example asset names are illustrative, drawn from the Alation functionality reference.")


# ============================================================ SLIDE 7 — CLASSIFICATION & BULK
s = slide()
bg(s)
title_block(s, "FEATURE 05  \u00b7  TAGS \u00b7 DOMAINS \u00b7 POLICY  \u00b7  GOVERNANCE AT SCALE",
            "Classification & Bulk Governance", AMBER)

# stat row
stats = [("100s", "of assets updated per bulk action", AMBER),
         ("GDPR \u00b7 CCPA", "compliance tags scoped to the right assets", BLUE),
         ("Audit trail", "on every classification and bulk change", GREEN)]
sx = Inches(0.6)
sw = Inches(3.92)
sgap = Inches(0.21)
sy = Inches(1.55)
shh = Inches(1.5)
for i, (big, sub, col) in enumerate(stats):
    x = sx + i * (sw + sgap)
    rect(s, x, sy, sw, shh, fill=PAPER, line=LINE, line_w=Pt(1))
    rect(s, x, sy, Inches(0.12), shh, fill=col)
    text(s, x + Inches(0.35), sy + Inches(0.2), sw - Inches(0.55), Inches(0.6),
         [{"text": big, "size": Pt(26), "bold": True, "color": col, "font": HEAD_FONT}])
    text(s, x + Inches(0.35), sy + Inches(0.86), sw - Inches(0.55), Inches(0.55),
         [{"text": sub, "size": Pt(12), "color": INK_SOFT, "line_spacing": 1.05}])

# principle banner
pb = Inches(3.32)
rect(s, Inches(0.6), pb, Inches(12.18), Inches(0.78), fill=CHIP_BG, line=AMBER, line_w=Pt(1))
rect(s, Inches(0.6), pb, Inches(0.14), Inches(0.78), fill=AMBER)
text(s, Inches(0.95), pb, Inches(11.6), Inches(0.78),
     [{"parts": [("Govern once, apply everywhere.  ", {"size": Pt(14), "bold": True, "color": INK}),
                 ("Classify and scope assets for governance, search, and reporting \u2014 then "
                  "operate at scale with rules and imports instead of one asset at a time.",
                  {"size": Pt(14), "color": INK_SOFT})], "line_spacing": 1.06}],
     anchor=MSO_ANCHOR.MIDDLE)

cards = [
    (AMBER, "\U0001F3F7", "Tags, domains & custom fields",
     "Classify and scope assets by compliance, domain, and project (GDPR Scoped, CCPA Scoped, Core Table) for search and reporting."),
    (BLUE, "\u21BB", "Bulk edit, sets & rules",
     "CSV and rule-based updates across hundreds of assets, plus data-dictionary import/export \u2014 an operational necessity at scale."),
    (GREEN, "\U0001F512", "Policy surfaced in the catalog",
     "Users see policy \uf0df\uf0e0 classification \uf0df\uf0e0 asset linkage for explainable use \u2014 privacy, retention, and purpose where modeled."),
]
cw = Inches(3.92)
cy = Inches(4.42)
chh = Inches(2.3)
for i, (acc, ic, t, b) in enumerate(cards):
    x = sx + i * (cw + sgap)
    card(s, x, cy, cw, chh, acc, t,
         [{"text": b, "size": Pt(12), "color": INK_SOFT, "line_spacing": 1.08}], icon=ic)

place_deck_icons(s, 7)

footer(s)
notes(s, "F06 + F13 + F14. Classification (tags/domains/custom fields) plus bulk operations are "
         "marked high in the feature inventory \u2014 stewards cannot run governance one asset at a "
         "time. Policy surfacing links classification to assets for explainable, defensible use.")


# ============================================================ SLIDE 8 — AI-READINESS / SPINE
s = slide()
bg(s)
title_block(s, "FEATURE 06  \u00b7  AI-READY METADATA  \u00b7  ONE SPINE, COMPOSABLE",
            "AI-Readiness & OMS Composability", TEAL)

# spine diagram band
band_top = Inches(1.5)
bh = Inches(1.35)
seg_w = Inches(3.62)
seg_gap = Inches(0.55)
segs = [("626 / MCI", "Metadata supply \u2014 scanners, enrichment, suggested mappings", INDIGO2),
        ("OMS", "Stores & serves technical + business metadata, APIs", BLUE),
        ("NAVIGATOR \u2013 BUSINESS DATA CATALOG", "The governed, business-first experience layer", TEAL)]
bx = Inches(0.6)
for i, (t, sub, col) in enumerate(segs):
    x = bx + i * (seg_w + seg_gap)
    seg = rect(s, x, band_top, seg_w, bh, fill=col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, x + Inches(0.25), band_top + Inches(0.2), seg_w - Inches(0.5), Inches(0.45),
         [{"text": t, "size": Pt(17), "bold": True, "color": WHITE, "font": HEAD_FONT}])
    text(s, x + Inches(0.25), band_top + Inches(0.68), seg_w - Inches(0.5), Inches(0.6),
         [{"text": sub, "size": Pt(11), "color": RGBColor(0xE6, 0xEE, 0xFA), "line_spacing": 1.05}])
    if i < 2:
        text(s, x + seg_w, band_top, seg_gap, bh,
             [{"text": "\u2192", "size": Pt(24), "bold": True, "color": MUTE,
               "align": PP_ALIGN.CENTER}], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

text(s, Inches(0.6), band_top + bh + Inches(0.1), Inches(12.18), Inches(0.34),
     [{"text": "One metadata spine \u2014 Navigator surfaces upstream AI and automation work; it does not rebuild the engines.",
       "size": Pt(12), "italic": True, "color": MUTE}])

cards = [
    (TEAL, "\u2728", "AI-readiness attributes",
     "Quality tier, lineage completeness, access classification, and documented limitations on assets \u2014 so AI and analytics teams pick steward-attested inputs without tribal knowledge."),
    (BLUE, "\U0001F50C", "Read API for DRE & agents",
     "Stable contracts for automation \u2014 bulk read, metadata sync, and agentic access \u2014 not only a UI. The catalog is consumable by downstream tools."),
    (VIOLET, None, "Surfaces upstream AI work",
     "When MCI / Data 626 produce enriched descriptions, lineage, or suggested mappings, Navigator is where stewards and consumers see and act on that work."),
]
cw = Inches(3.92)
cy = Inches(3.7)
chh = Inches(2.95)
for i, (acc, ic, t, b) in enumerate(cards):
    x = Inches(0.6) + i * (cw + Inches(0.21))
    card(s, x, cy, cw, chh, acc, t,
         [{"text": b, "size": Pt(12.5), "color": INK_SOFT, "line_spacing": 1.12}], icon=ic)

place_deck_icons(s, 8)

footer(s)
notes(s, "F16 + F11 + F19. AI-readiness is the FY27 differentiator: a defined attribute set so AI "
         "intake is steward-attested. Composability is the architecture principle \u2014 one spine "
         "(626 supply, OMS store, Navigator UX), with a read API for DRE and agents.")


# ============================================================ SLIDE 9 — BY THE NUMBERS
s = slide()
bg(s)
title_block(s, "WHY IT MATTERS", "By the Numbers", BLUE)

bigs = [("~531", "Alation users to migrate \u2014 with zero functionality lost", BLUE),
        ("20", "prioritized features: 11 parity \u00b7 6 scale \u00b7 3 differentiate", TEAL),
        ("1", "governed spine \u2014 626 supply \u00b7 OMS store \u00b7 Navigator UX", VIOLET),
        ("Sep 2027", "full Alation cutover target (dev complete ~Mar 2027)", GREEN)]
bx = Inches(0.6)
bw = Inches(2.92)
bgap = Inches(0.16)
by = Inches(1.7)
bhh = Inches(2.3)
for i, (big, sub, col) in enumerate(bigs):
    x = bx + i * (bw + bgap)
    rect(s, x, by, bw, bhh, fill=PAPER, line=LINE, line_w=Pt(1))
    rect(s, x, by, bw, Inches(0.09), fill=col)
    text(s, x + Inches(0.25), by + Inches(0.5), bw - Inches(0.5), Inches(0.9),
         [{"text": big, "size": Pt(38), "bold": True, "color": col, "font": HEAD_FONT,
           "align": PP_ALIGN.CENTER}], align=PP_ALIGN.CENTER)
    text(s, x + Inches(0.25), by + Inches(1.5), bw - Inches(0.5), Inches(0.7),
         [{"text": sub, "size": Pt(12), "color": INK_SOFT, "align": PP_ALIGN.CENTER,
           "line_spacing": 1.08}], align=PP_ALIGN.CENTER)

# success-signal banner
sb = Inches(4.35)
rect(s, Inches(0.6), sb, Inches(12.18), Inches(2.2), fill=PAPER, line=LINE, line_w=Pt(1))
rect(s, Inches(0.6), sb, Inches(0.14), Inches(2.2), fill=BLUE)
text(s, Inches(0.95), sb + Inches(0.22), Inches(11.6), Inches(0.4),
     [{"text": "HOW WE'LL KNOW IT'S WORKING", "size": Pt(12), "bold": True, "color": BLUE,
       "font": HEAD_FONT}])
sig = [
    "Adoption \u2014 weekly active users vs. the ~531 Alation baseline after cutover",
    "Definition coverage \u2014 priority domains with glossary / metric definitions reachable in Navigator",
    "Time-to-answer \u2014 faster on supported consumer and analyst journeys; fewer \u201cwhere is X?\u201d escalations",
    "Metadata preservation \u2014 high % of glossary, tags, descriptions, and links validated post-migration",
    "AI-readiness adoption \u2014 % of AI / analytics intake using steward-attested assets",
]
sigr = []
for it in sig:
    sigr.append({"parts": [("\u25B8  ", {"size": Pt(12.5), "bold": True, "color": TEAL}),
                           (it, {"size": Pt(12.5), "color": INK_SOFT})],
                 "space_after": Pt(6), "line_spacing": 1.05})
text(s, Inches(0.95), sb + Inches(0.66), Inches(11.6), Inches(1.45), sigr)

footer(s)
notes(s, "Contract reality: Alation ends Oct 1, 2026 with a likely Aug/Sep 2026 renewal while we "
         "build toward a Sep 2027 cutover (dev complete ~Mar 2027). Feature count: F01-F11 parity "
         "(11), F12-F17 scale (6), F18-F20 differentiate (3). Success signals come from the value "
         "deck OKRs.")


# ============================================================ SLIDE 10 — ROADMAP
s = slide()
bg(s)
title_block(s, "3 PHASES  \u00b7  PARITY \u2192 SCALE \u2192 DIFFERENTIATE",
            "The Roadmap to Full Migration", BLUE)

phases = [
    (BLUE, "Phase 1", "Trust & Exit", "Alation mvp \u00b7 build toward dev-complete ~Mar 2027",
     ["Unified search, browse & asset detail", "Business glossary, linked to assets",
      "Lineage & provenance (table +)", "Trust flags & stewardship",
      "Tags, domains & SSO access", "API for migration onto OMS"],
     "Users can do their job without Alation \u2014 migration-safe, interview-validated parity (features F01\u2013F11)."),
    (TEAL, "Phase 2", "Operate at Scale", "Coverage + AI-readiness \u00b7 ~Q2 FY27+",
     ["Requests & lightweight workflows", "Policy surfaced in the catalog",
      "Bulk / rules / dictionary at strength", "Usage & access signals",
      "AI-readiness attributes", "Saved searches & favorites"],
     "The catalog is how we run governance and AI prep \u2014 not only where we read metadata (F12\u2013F17)."),
    (VIOLET, "Phase 3", "Differentiate & Compose", "Governance Portal \u00b7 ~Q4 FY27+",
     ["Governance & privacy command center", "Semantic layer \u2194 catalog integration",
      "Policy-driven metadata automation", "Richer recommendations",
      "Expanded API consumption by agents", "Cross-pillar governance posture"],
     "One governed story from metric definition to production asset, on a coherent enterprise shell (F18\u2013F20)."),
]
px = Inches(0.6)
pw = Inches(3.92)
pgap = Inches(0.21)
ptop = Inches(1.62)
ph = Inches(5.05)
for i, (col, ph_lbl, ph_name, when, feats, foot) in enumerate(phases):
    x = px + i * (pw + pgap)
    rect(s, x, ptop, pw, ph, fill=PAPER, line=LINE, line_w=Pt(1))
    head = rect(s, x, ptop, pw, Inches(1.0), fill=col)
    text(s, x + Inches(0.28), ptop + Inches(0.14), pw - Inches(0.5), Inches(0.4),
         [{"text": ph_lbl, "size": Pt(13), "bold": True, "color": RGBColor(0xDD,0xE8,0xFB), "font": HEAD_FONT}])
    text(s, x + Inches(0.28), ptop + Inches(0.44), pw - Inches(0.5), Inches(0.4),
         [{"text": ph_name, "size": Pt(17), "bold": True, "color": WHITE, "font": HEAD_FONT}])
    text(s, x + Inches(0.28), ptop + Inches(1.12), pw - Inches(0.5), Inches(0.4),
         [{"text": when, "size": Pt(10.5), "italic": True, "color": MUTE}])
    fr = []
    for fe in feats:
        fr.append({"parts": [("\u25B8  ", {"size": Pt(11.5), "bold": True, "color": col}),
                             (fe, {"size": Pt(11.5), "color": INK})],
                   "space_after": Pt(7), "line_spacing": 1.04})
    text(s, x + Inches(0.28), ptop + Inches(1.55), pw - Inches(0.56), Inches(2.5), fr)
    # footer strip
    fb = ptop + ph - Inches(1.18)
    rect(s, x + Inches(0.2), fb, pw - Inches(0.4), Inches(1.0), fill=MIST, line=LINE, line_w=Pt(0.75))
    text(s, x + Inches(0.36), fb + Inches(0.12), pw - Inches(0.7), Inches(0.8),
         [{"text": foot, "size": Pt(10.5), "italic": True, "color": INK_SOFT, "line_spacing": 1.06}])

footer(s)
notes(s, "Outcome-based phasing: parity & exit, then scale & AI-readiness, then differentiation + "
         "unified governance (the Navigator Governance Portal). Dates echo the value deck and "
         "product brief; adjust to the official program calendar. Phase 1 is the heart of the "
         "Alation migration narrative.")


# ---------------------------------------------------------------- save
OUT = sys.argv[1] if len(sys.argv) > 1 else "Navigator-Business-Data-Catalog-Vision.pptx"
prs.save(OUT)
print("saved", OUT, "-", len(prs.slides._sldIdLst), "slides")


