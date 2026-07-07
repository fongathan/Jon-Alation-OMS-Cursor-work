#!/usr/bin/env python3
"""Build Data Navigator overview deck — Editorial Hero theme (distinct from Alation source deck)."""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parents[1] / "Data-Navigator-Overview_06_2026.pptx"

# Editorial Hero palette (violet / cyan / paper — not corporate navy-lavender)
INK = RGBColor(0x0C, 0x0F, 0x1A)
PAPER = RGBColor(0xF8, 0xF9, 0xFF)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
VIOLET = RGBColor(0x7C, 0x3A, 0xED)
CYAN = RGBColor(0x06, 0xB6, 0xD4)
AMBER = RGBColor(0xF5, 0x9E, 0x0B)
LIME = RGBColor(0x84, 0xCC, 0x16)
MAGENTA = RGBColor(0xE1, 0x1D, 0x48)
MUTED = RGBColor(0x64, 0x74, 0x8B)
BORDER = RGBColor(0xE2, 0xE8, 0xF0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
VIOLET_SOFT = RGBColor(0xED, 0xE9, 0xFE)
CYAN_SOFT = RGBColor(0xE0, 0xF7, 0xFA)
AMBER_SOFT = RGBColor(0xFF, 0xF7, 0xED)
HERO_DARK = RGBColor(0x1E, 0x1B, 0x4B)
HERO_MID = RGBColor(0x4C, 0x1D, 0x95)

FONT_DISPLAY = "Georgia"
FONT_BODY = "Calibri"

FOOTER = "Data Navigator · DEET Data Governance · June 2026"

COLORS = [VIOLET, CYAN, AMBER, LIME]
SOFT_BG = [VIOLET_SOFT, CYAN_SOFT, AMBER_SOFT, RGBColor(0xEC, 0xF9, 0xE8)]


def set_para(p, text, size=11, color=INK, bold=False, font=FONT_BODY):
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font


def slide_background(slide, color=PAPER):
    bg = slide.shapes.add_shape(1, 0, 0, Inches(10), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    # send to back
    sp_tree = slide.shapes._spTree  # noqa: SLF001
    sp = bg._element  # noqa: SLF001
    sp_tree.remove(sp)
    sp_tree.insert(2, sp)


def add_left_rail(slide):
    rail = slide.shapes.add_shape(1, 0, 0, Inches(0.14), Inches(7.5))
    rail.fill.solid()
    rail.fill.fore_color.rgb = VIOLET
    rail.line.fill.background()


def add_footer(slide, light=False):
    line = slide.shapes.add_shape(1, Inches(0.55), Inches(7.08), Inches(9.0), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER if not light else RGBColor(0x55, 0x55, 0x88)
    line.line.fill.background()
    tb = slide.shapes.add_textbox(Inches(0.55), Inches(7.15), Inches(9.0), Inches(0.28))
    p = tb.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    set_para(p, FOOTER, size=8, color=MUTED if not light else RGBColor(0xAA, 0xAA, 0xCC))


def slide_title_block(slide, title, subtitle=None, top=Inches(0.42), light=False):
    tb = slide.shapes.add_textbox(Inches(0.55), top, Inches(8.8), Inches(0.65))
    set_para(tb.text_frame.paragraphs[0], title, size=22, color=INK if not light else WHITE, bold=True, font=FONT_DISPLAY)
    if subtitle:
        st = slide.shapes.add_textbox(Inches(0.55), top + Inches(0.58), Inches(8.8), Inches(0.38))
        set_para(st.text_frame.paragraphs[0], subtitle, size=11, color=MUTED if not light else RGBColor(0xCC, 0xCC, 0xEE))


def new_content_slide(prs, title, subtitle=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_background(slide)
    add_left_rail(slide)
    slide_title_block(slide, title, subtitle)
    add_footer(slide)
    return slide


def add_card(slide, left, top, width, height, accent_rgb, heading, body, heading_size=11, body_size=9):
    card = slide.shapes.add_shape(1, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD
    card.line.color.rgb = BORDER
    stripe = slide.shapes.add_shape(1, left, top, Inches(0.06), height)
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = accent_rgb
    stripe.line.fill.background()
    tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.1), width - Inches(0.25), height - Inches(0.14))
    tf = tb.text_frame
    tf.word_wrap = True
    set_para(tf.paragraphs[0], heading, size=heading_size, color=INK, bold=True, font=FONT_DISPLAY)
    set_para(tf.add_paragraph(), body, size=body_size, color=MUTED)


def add_metric_card(slide, left, top, width, accent_rgb, big, label, detail):
    card = slide.shapes.add_shape(1, left, top, width, Inches(1.5))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD
    card.line.color.rgb = BORDER
    tb = slide.shapes.add_textbox(left + Inches(0.12), top + Inches(0.12), width - Inches(0.2), Inches(1.25))
    tf = tb.text_frame
    set_para(tf.paragraphs[0], big, size=26, color=accent_rgb, bold=True, font=FONT_DISPLAY)
    rule = slide.shapes.add_shape(1, left + Inches(0.12), top + Inches(0.72), Inches(0.55), Inches(0.04))
    rule.fill.solid()
    rule.fill.fore_color.rgb = accent_rgb
    rule.line.fill.background()
    set_para(tf.add_paragraph(), label, size=10, color=INK, bold=True)
    set_para(tf.add_paragraph(), detail, size=8, color=MUTED)


def add_callout(slide, top, height, text, bg=VIOLET_SOFT):
    call = slide.shapes.add_shape(1, Inches(0.55), top, Inches(8.85), height)
    call.fill.solid()
    call.fill.fore_color.rgb = bg
    call.line.color.rgb = VIOLET
    tf = call.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.12)
    set_para(tf.paragraphs[0], text, size=10, color=INK, font=FONT_DISPLAY)


def add_summary_bar(slide, top, text):
    bar = slide.shapes.add_shape(1, Inches(0.55), top, Inches(8.85), Inches(0.58))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CYAN_SOFT
    bar.line.color.rgb = CYAN
    tb = slide.shapes.add_textbox(Inches(0.7), top + Inches(0.1), Inches(8.55), Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    set_para(tf.paragraphs[0], text, size=10, color=INK, font=FONT_DISPLAY)


def add_numbered_tile(slide, left, top, w, h, num, title, body):
    tile = slide.shapes.add_shape(1, left, top, w, h)
    tile.fill.solid()
    tile.fill.fore_color.rgb = CARD
    tile.line.color.rgb = VIOLET
    tile.line.width = Pt(1.5)
    nb = slide.shapes.add_textbox(left + Inches(0.1), top + Inches(0.08), Inches(0.35), Inches(0.3))
    set_para(nb.text_frame.paragraphs[0], f"{num:02d}", size=14, color=VIOLET, bold=True, font=FONT_DISPLAY)
    tb = slide.shapes.add_textbox(left + Inches(0.1), top + Inches(0.38), w - Inches(0.18), h - Inches(0.42))
    tf = tb.text_frame
    tf.word_wrap = True
    set_para(tf.paragraphs[0], title, size=10, color=INK, bold=True, font=FONT_DISPLAY)
    set_para(tf.add_paragraph(), body, size=8, color=MUTED)


def add_deep_dive_slide(prs, num, title, subtitle, impacts, challenge, workflow, findings, steps):
    slide = new_content_slide(prs, title, subtitle)
    badge = slide.shapes.add_shape(1, Inches(8.55), Inches(0.38), Inches(1.15), Inches(0.28))
    badge.fill.solid()
    badge.fill.fore_color.rgb = VIOLET
    badge.line.fill.background()
    bt = slide.shapes.add_textbox(Inches(8.6), Inches(0.4), Inches(1.05), Inches(0.24))
    set_para(bt.text_frame.paragraphs[0], f"UC {num}", size=8, color=WHITE, bold=True)

    cw = Inches(2.15)
    y0 = Inches(1.22)
    for i, (big, small) in enumerate(impacts):
        add_metric_card(slide, Inches(0.55) + i * cw, y0, cw - Inches(0.08), COLORS[i % 4], big, small, "")

    add_card(slide, Inches(0.55), Inches(2.05), Inches(4.35), Inches(1.35), MAGENTA, "The challenge", challenge, 10, 9)
    wf_body = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(workflow))
    add_card(slide, Inches(5.05), Inches(2.05), Inches(4.35), Inches(1.35), VIOLET, "AI-assisted workflow", wf_body, 10, 8)

    add_card(slide, Inches(0.55), Inches(3.55), Inches(4.35), Inches(0.78), CYAN, findings[0][0], findings[0][1], 10, 8)
    add_card(slide, Inches(5.05), Inches(3.55), Inches(4.35), Inches(0.78), AMBER, findings[1][0], findings[1][1], 10, 8)

    tb = slide.shapes.add_textbox(Inches(0.55), Inches(4.48), Inches(9), Inches(0.22))
    set_para(tb.text_frame.paragraphs[0], "Reusable template", size=9, color=VIOLET, bold=True, font=FONT_DISPLAY)
    sw = Inches(2.15)
    line = slide.shapes.add_shape(1, Inches(0.55), Inches(4.95), Inches(8.85), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER
    line.line.fill.background()
    for i, (step, desc) in enumerate(steps):
        left = Inches(0.55) + i * sw
        dot = slide.shapes.add_shape(9, left + sw / 2 - Inches(0.08), Inches(4.82), Inches(0.16), Inches(0.16))
        dot.fill.solid()
        dot.fill.fore_color.rgb = COLORS[i % 4]
        dot.line.fill.background()
        ht = slide.shapes.add_textbox(left, Inches(5.05), sw - Inches(0.06), Inches(0.22))
        set_para(ht.text_frame.paragraphs[0], step, size=9, color=COLORS[i % 4], bold=True, font=FONT_DISPLAY)
        bt = slide.shapes.add_textbox(left, Inches(5.32), sw - Inches(0.06), Inches(0.55))
        tf = bt.text_frame
        tf.word_wrap = True
        set_para(tf.paragraphs[0], desc, size=8, color=MUTED)
    return slide


def build():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # --- Slide 1: Title (hero) ---
    s = prs.slides.add_slide(prs.slide_layouts[6])
    slide_background(s, HERO_DARK)
    glow = s.shapes.add_shape(1, Inches(6.5), Inches(-0.5), Inches(4), Inches(3.5))
    glow.fill.solid()
    glow.fill.fore_color.rgb = HERO_MID
    glow.line.fill.background()
    glow2 = s.shapes.add_shape(1, Inches(-0.5), Inches(4.5), Inches(4), Inches(3))
    glow2.fill.solid()
    glow2.fill.fore_color.rgb = RGBColor(0x0E, 0x74, 0x90)
    glow2.line.fill.background()
    badge = s.shapes.add_textbox(Inches(0.65), Inches(1.85), Inches(4), Inches(0.3))
    set_para(badge.text_frame.paragraphs[0], "AD PLATFORMS · DATA GOVERNANCE", size=9, color=CYAN, bold=True)
    tb = s.shapes.add_textbox(Inches(0.6), Inches(2.25), Inches(8.5), Inches(1.0))
    set_para(tb.text_frame.paragraphs[0], "Data Navigator", size=44, color=WHITE, bold=True, font=FONT_DISPLAY)
    sub = s.shapes.add_textbox(Inches(0.6), Inches(3.35), Inches(8), Inches(0.9))
    set_para(sub.text_frame.paragraphs[0], "Governed discovery on OMS · Alation → in-house migration", size=16, color=RGBColor(0xCC, 0xCC, 0xEE))
    add_footer(s, light=True)

    # --- Slide 2: Leadership ---
    s = new_content_slide(
        prs,
        "Why This Program and Data Navigator Matter to Leadership",
    )
    cols = [
        (LIME, "Business outcomes", "High-value business outcomes", "What leadership gains.", [
            "Reduced regulatory and audit risk across GDPR and SOX through governed metadata on OMS.",
            "Faster, defensible decisions backed by gold definitions, lineage context, and ownership.",
            "Operational efficiency — fewer duplicate efforts and shadow spreadsheets after Alation exit.",
            "Scalable foundation for AI and automation — metadata supply via 626/MCI, consumption via OMS APIs.",
            "Improved visibility into PII and user consent signals via Navigator read paths (phase 2 Portal for ops).",
        ]),
        (AMBER, "Why now", "Contract-driven urgency", "Alation end Oct 1, 2026.", [
            "Vendor catalog cannot carry us past renewal without a credible in-house surface.",
            "Passive catalog drift decouples business meaning from production metadata.",
            "2024 EY audit themes still require inspectable lineage, ownership, and documentation at scale.",
            "Competing-program confusion — intake reset to persona-first Navigator on OMS, not “do everything.”",
        ]),
        (VIOLET, "Program impact", "How we deliver the outcomes", "626 + OMS + Navigator.", [
            "OMS as system of record; Navigator as governed discovery UX for business and compliance personas.",
            "Improved visibility into assets, gold/provenance, and ownership across Ads domains.",
            "Stronger stewardship continuity as Alation content migrates via APIs.",
            "Direct alignment with regulatory obligations — read API for evidence workflows.",
            "Lower long-term vendor lock-in; enterprise design–governed UX on internal platform.",
        ]),
    ]
    cw = Inches(3.0)
    for i, (accent, hdr, title, sub, bullets) in enumerate(cols):
        left = Inches(0.45) + i * cw
        add_card(s, left, Inches(1.22), cw - Inches(0.1), Inches(4.95), accent, title, sub, 12, 9)
        tb = s.shapes.add_textbox(left + Inches(0.2), Inches(1.28), cw - Inches(0.25), Inches(0.22))
        set_para(tb.text_frame.paragraphs[0], hdr.upper(), size=8, color=accent, bold=True)
        tb2 = s.shapes.add_textbox(left + Inches(0.2), Inches(1.95), cw - Inches(0.25), Inches(4.0))
        tf = tb2.text_frame
        tf.word_wrap = True
        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(8)
            p.font.color.rgb = INK
            p.font.name = FONT_BODY
            p.space_before = Pt(4)
    add_summary_bar(
        s,
        Inches(6.35),
        "Data governance on OMS, delivered through Data Navigator, is a critical capability for managing risk, "
        "enabling growth, and supporting trusted decision-making — with a clear exit from Alation.",
    )

    # --- Slide 3: What catalog is ---
    s = new_content_slide(
        prs,
        "What Data Navigator Is and How It Supports Data Governance",
        "Two sides of the same story: business pressure for answers, and the governed experience on OMS.",
    )
    left_items = [
        ("System of record (on OMS)", "Technical inventory plus business meaning — objects, definitions, ownership, classifications; Navigator is the UX layer."),
        ("Inspectable lineage", "Lineage and relationships visible for impact narratives; engineers deep-link to OMS for full technical depth."),
        ("Business-to-physical alignment", "Glossary and gold definitions align reporting language to physical fields — corporate metrics federated, not duplicated."),
        ("Reusable via API / MCP", "Same metadata fields power UI, read API, and approved Cursor MCP workflows — not re-pasted into wikis."),
    ]
    right_items = [
        ("1. Defensible answers, fast", "Leaders and DNA consumers find governed definitions and owners in minutes — not multi-day hunts."),
        ("2. Evidence-based conversations", "Privacy and control discussions start from catalog facts — defined vs observed on one asset record."),
        ("3. Risk reduction", "Gold/provenance and classifications reduce wrong-metric and PII interpretation risk."),
        ("4. Stewardship sets the ceiling", "626/MCI supply + steward habits scale the model; thin metadata limits credible governance."),
    ]
    for i, (head, body) in enumerate(left_items):
        add_card(s, Inches(0.55), Inches(1.22) + i * Inches(1.12), Inches(4.25), Inches(1.02), COLORS[i], head, body)
    for i, (head, body) in enumerate(right_items):
        add_card(s, Inches(5.15), Inches(1.22) + i * Inches(1.12), Inches(4.25), Inches(1.02), COLORS[i], head, body)

    # --- Slide 4: Value & footprint ---
    s = new_content_slide(
        prs,
        "Target-State Value & Data Navigator Footprint",
        "What teams will get from governed discovery on OMS — breadth matters when curation and lineage keep pace.",
    )
    values = [
        ("Centralized governed discovery", "Search, browse, glossary, and gold definitions across Ads — less repeat questioning in chat and email."),
        ("Faster impact analysis", "Lineage context and Open in OMS shorten impact analysis for schema and definition changes."),
        ("Routes questions to owners", "Ownership and stewardship visible on asset pages when fields are maintained in OMS."),
        ("Reuse via API / MCP", "OMS read API and approved MCP surfaces for reviews and engineering — Navigator stays traditional UI."),
    ]
    for i, (h, b) in enumerate(values):
        col, row = i % 2, i // 2
        add_card(
            s, Inches(0.55) + col * Inches(4.65), Inches(1.18) + row * Inches(1.12),
            Inches(4.4), Inches(1.0), COLORS[i], h, b,
        )
    metrics = [
        ("OMS", "Technical metadata backbone", "Snowflake, Databricks, pipelines, reports — existing OMS inventory"),
        ("One", "Governed UX shell", "Navigator for business/compliance; OMS UI for engineers"),
        ("531", "Alation users to migrate", "Baseline for adoption targets post-cutover"),
        ("Persona-first", "MVP scope locked", "Consumer primary; steward/compliance thin; engineer handoff"),
    ]
    for i, (big, label, detail) in enumerate(metrics):
        add_metric_card(s, Inches(0.55) + i * Inches(2.3), Inches(3.65), Inches(2.15), COLORS[i], big, label, detail)

    # --- Slide 5: AI use cases ---
    s = new_content_slide(
        prs,
        "AI-Enabled Use Cases with OMS Metadata and Cursor MCP",
        "Accelerate discovery and governance using catalog metadata — MCP reads OMS/Alation; Navigator surfaces trusted outcomes.",
    )
    cases = [
        ("AI-Assisted Data Discovery", "Plain-language search across governed metadata — certified-first results."),
        ("Automated Impact Analysis", "Predict downstream impact of schema and definition changes before release."),
        ("Audit & Compliance Reporting", "Repeatable PII, SOX, and GDPR evidence packs from catalog posture."),
        ("Personal Data / PII Assessments", "Identify classifications and gaps to accelerate audit remediation."),
        ("Field-Class Definition Standardization", "Standardize column classes; inherit definitions source → OMS → BI."),
        ("Metadata Enrichment & Documentation", "AI-drafted descriptions and glossary links — human-approved, applied via 626/OMS."),
    ]
    tw, th = Inches(3.05), Inches(1.45)
    for i, (t, b) in enumerate(cases):
        add_numbered_tile(s, Inches(0.55) + (i % 3) * tw, Inches(1.22) + (i // 3) * th, tw - Inches(0.08), th - Inches(0.08), i + 1, t, b)
    note = s.shapes.add_textbox(Inches(0.55), Inches(6.5), Inches(8.85), Inches(0.35))
    set_para(
        note.text_frame.paragraphs[0],
        "Note: MCP/agentic patterns target OMS read API and catalog metadata — not built inside Navigator MVP. "
        "Separate from vendor MCP; Tony → MCI / Data 626 for AI-native supply.",
        size=8,
        color=MUTED,
    )

    # --- Slide 6: Stack vs outcomes ---
    s = new_content_slide(
        prs,
        "What Data Navigator Provides — and the Ad Platform Governance Outcomes it Supports",
        "Governed experience on OMS, mapped to stewardship accountabilities.",
    )
    stack = [
        ("Metadata search & browse", "Across OMS-connected sources — depth/freshness depend on 626 supply and connectors."),
        ("Glossaries & articles", "Migrated Alation patterns; steward workflows thin in MVP, scale in phase 2."),
        ("Lineage visibility", "Context in Navigator; full technical lineage via Open in OMS."),
        ("Automated access (API / MCP)", "Read API for DRE and assessments; same fields users see in Navigator."),
    ]
    outcomes = [
        ("Privacy & classification", "Inventory and field documentation support tagging and sensitivity review."),
        ("SOX / financial reporting", "Gold metric definitions and lineage narratives for controls-heavy reporting."),
        ("Retention & lifecycle", "Knowing where datasets live aligns policy discussion; enforcement stays platform-specific."),
        ("Ownership & lineage", "Explicit stewards and paths reduce orphaned assets — when maintained."),
    ]
    for i, (h, b) in enumerate(stack):
        add_card(s, Inches(0.55), Inches(1.18) + i * Inches(1.1), Inches(4.25), Inches(0.98), COLORS[i], h, b)
    for i, (h, b) in enumerate(outcomes):
        add_card(s, Inches(5.15), Inches(1.18) + i * Inches(1.1), Inches(4.25), Inches(0.98), COLORS[i], h, b)

    # --- Slide 7: Usage ---
    s = new_content_slide(
        prs,
        "Alation Usage Today & Navigator Adoption Targets",
        "Stewardship metrics show where to invest; engagement baselines the migration.",
    )
    for i, (h, b) in enumerate([
        ("Primary stewardship view", "Alation Curation Metric Report today — track documentation completeness by source."),
        ("Governance use", "Prioritize backlog, justify 626 connector work, show progress to sponsors."),
        ("Navigator target", "Same measures on OMS post-migration — steward UAT and parallel-run adoption."),
    ]):
        add_card(s, Inches(0.55), Inches(1.18) + i * Inches(0.92), Inches(8.85), Inches(0.82), COLORS[i], h, b)
    metrics = [
        ("~411", "Avg monthly users (Alation)", "Baseline for Navigator/OMS adoption"),
        ("~7.2K", "Avg page views / mo", "Discovery and reference behavior to preserve"),
        ("~5.5K", "Avg searches / mo", "Search remains front door — title/description quality"),
        ("~531", "Licensed users", "Migration scope for cutover planning"),
    ]
    for i, (big, label, detail) in enumerate(metrics):
        add_metric_card(s, Inches(0.55) + i * Inches(2.3), Inches(4.25), Inches(2.15), COLORS[i], big, label, detail)
    note = s.shapes.add_textbox(Inches(0.55), Inches(5.95), Inches(5), Inches(0.25))
    p = note.text_frame.paragraphs[0]
    set_para(p, "Indicative Alation averages — refresh before sharing.", size=8, color=MUTED)
    p.font.italic = True

    # --- Slide 8: Tools ---
    s = new_content_slide(
        prs,
        "Data Governance Tools — Transition & Target on OMS / Navigator",
        "AI-enabled tooling on trusted metadata — Alation-era tools migrate to OMS spine; Navigator is consumption layer.",
    )
    tools = [
        ("Data Lineage Finder", "Alation + React · Production", "Surfaces lineage via catalog MCP — target: OMS lineage + Navigator handoff.", "Impact analysis and incident triage."),
        ("Curation Dashboard", "Alation + MSTR · Production", "Schema/column completeness — target: OMS steward metrics + 626 supply signals.", "Metadata curation at scale with human oversight."),
        ("PII Detection Tool", "Alation + LLM · Production", "Flags sensitive fields via MCP — target: compliance read views + pillar tools.", "Audit response and proactive risk reduction."),
        ("Dictionary Transfer", "Alation + API · In development", "Cross-system definitions — target: 626/MCI supply into OMS, surfaced in Navigator.", "Consistent business definitions without manual re-entry."),
    ]
    tw = Inches(2.35)
    for i, (name, tech, does, impact) in enumerate(tools):
        left = Inches(0.5) + i * tw
        add_card(s, left, Inches(1.18), tw - Inches(0.06), Inches(4.85), COLORS[i], name, f"{tech}\n\n{does}\n\nImpact: {impact}", 10, 8)
    add_summary_bar(
        s,
        Inches(6.35),
        "AI-enabled tooling on trusted metadata transforms governance from manual processes into scalable systems — "
        "Navigator surfaces outcomes; 626/MCI and OMS own supply and store.",
    )

    # --- Slide 9: Roadmap ---
    s = new_content_slide(
        prs,
        "Scaling Data Governance: Foundation to Enterprise (FY26–FY28)",
        "From Alation exit through Navigator on OMS to enterprise-scale, AI-enabled governance.",
    )
    phases = [
        (LIME, "Now · FY26", "Navigator MVP & Alation exit planning", "Foundation · Buy vs Build decision", [
            "Persona-first MVP scoped — consumer primary, steward/compliance thin.",
            "OMS + 626/MCI handoffs documented; Alation API migration path defined.",
            "Contract end Oct 1, 2026 — parallel run and renewal narrative.",
            "Five consumer stories + steward/compliance set validated (Sarah/Suman).",
            "Enterprise design alignment on Navigator IA (Sage-style patterns).",
        ]),
        (CYAN, "Current · FY27", "Build Navigator · Migrate Alation", "In progress · Cutover ~Sep 2027", [
            "Deliver search/browse, gold/provenance, glossary, classifications read, read API.",
            "Migrate glossary, articles, endorsements via OMS APIs.",
            "Scale 626/MCI metadata supply into OMS; Navigator consumes — no duplicate scrapers.",
            "Parallel run with steward UAT; dev complete target ~Mar 2027.",
            "Enable OMS read API and approved MCP for Cursor workflows.",
            "Buy vs Build decision: in-house Navigator on OMS vs extend Alation.",
        ]),
        (VIOLET, "Future · FY28", "Enterprise governance on OMS", "Scale & maturity", [
            "Enterprise-scale governance anchored on OMS across Ad Platforms.",
            "Governance Portal phase 2 — privacy/compliance command center adjacent to Navigator.",
            "AI-assisted curation at scale via 626/MCI; Navigator shows steward-approved outputs.",
            "Semantic / corporate metrics federated; coverage and time-to-answer targets met.",
            "Trusted foundation for analytics, AI, and audit readiness.",
        ]),
    ]
    pw = Inches(3.05)
    timeline = s.shapes.add_shape(1, Inches(0.55), Inches(1.38), Inches(8.85), Inches(0.03))
    timeline.fill.solid()
    timeline.fill.fore_color.rgb = BORDER
    timeline.line.fill.background()
    for i, (accent, phase, title, sub, bullets) in enumerate(phases):
        left = Inches(0.45) + i * pw
        dot = s.shapes.add_shape(9, left + pw / 2 - Inches(0.1), Inches(1.28), Inches(0.2), Inches(0.2))
        dot.fill.solid()
        dot.fill.fore_color.rgb = accent
        dot.line.fill.background()
        add_card(s, left, Inches(1.55), pw - Inches(0.08), Inches(5.05), accent, title, sub, 11, 8)
        tb = s.shapes.add_textbox(left + Inches(0.2), Inches(1.6), pw - Inches(0.25), Inches(0.2))
        set_para(tb.text_frame.paragraphs[0], phase.upper(), size=8, color=accent, bold=True)
        tb2 = s.shapes.add_textbox(left + Inches(0.2), Inches(2.15), pw - Inches(0.25), Inches(4.2))
        tf = tb2.text_frame
        tf.word_wrap = True
        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(7)
            p.font.color.rgb = INK
            p.font.name = FONT_BODY
            p.space_before = Pt(3)

    # --- Slide 10: Appendix ---
    s = prs.slides.add_slide(prs.slide_layouts[6])
    slide_background(s, HERO_MID)
    tb = s.shapes.add_textbox(Inches(0.65), Inches(3.0), Inches(5), Inches(0.9))
    set_para(tb.text_frame.paragraphs[0], "Appendix", size=40, color=WHITE, bold=True, font=FONT_DISPLAY)
    sub = s.shapes.add_textbox(Inches(0.65), Inches(3.85), Inches(6), Inches(0.4))
    set_para(sub.text_frame.paragraphs[0], "Use cases · metrics · strategy · socialization", size=12, color=RGBColor(0xDD, 0xDD, 0xFF))
    add_footer(s, light=True)

    # --- Slides 11–16: Deep dives ---
    add_deep_dive_slide(
        prs, 1,
        "Cursor–OMS MCP Use Case — AI-Assisted Data Discovery",
        "Plain-English questions over governed metadata return trusted assets in minutes.",
        [("Days → Mins", "Time to trusted data"), ("All Domains", "Discovery scope"), ("Gold-first", "Results prioritize"), ("New analysts", "Onboarding accelerated")],
        "Analysts lose hours locating the right Snowflake/Databricks table or BI report — tribal knowledge of ad event schemas slows decisions.",
        ["Natural-language query via Cursor MCP.", "MCP queries OMS/Alation glossary, tables, lineage.", "Surface ownership, freshness, certification.", "Hand off curated assets; Open in OMS or Navigator."],
        [("Onboarding accelerated", "New analysts productive in days vs weeks."), ("Highest-trust assets first", "Gold, owned, recently refreshed assets prioritized.")],
        [("Step 1 Ask", "Pose plain-English question via MCP."), ("Step 2 Match", "Query catalog + glossary + lineage."), ("Step 3 Rank", "Trust signals — ownership, gold, freshness."), ("Step 4 Use", "Hand off assets; open in Navigator/OMS.")],
    )
    add_deep_dive_slide(
        prs, 2,
        "Cursor–OMS MCP Use Case — Automated Impact Analysis",
        "Predict downstream impact across pipelines, BI, and 3P consumers before code ships.",
        [("Days → Hrs", "Time to impact brief"), ("100+", "Dependencies traced"), ("Pre-release", "Issues caught earlier"), ("All Domains", "Lineage coverage")],
        "Schema or definition changes can silently break dashboards and feeds — manual impact analysis is slow and partial.",
        ["Define changed asset scope.", "Trace lineage via MCP (OMS/Alation).", "Inventory downstream consumers and stewards.", "Generate stakeholder-ready impact brief."],
        [("Hidden consumers surfaced", "Downstream assets flagged before release."), ("Owners notified pre-deploy", "Stewards identified upfront — less rework.")],
        [("Step 1 Scope", "Identify changed table/column."), ("Step 2 Trace", "Upstream + downstream via MCP."), ("Step 3 Map", "List consumers, owners, jobs."), ("Step 4 Brief", "Change-impact summary + actions.")],
    )
    add_deep_dive_slide(
        prs, 3,
        "Cursor–OMS MCP Use Case — Audit & Compliance Reporting",
        "Repeatable evidence packs for PII, SOX, and GDPR — from catalog metadata.",
        [("Days → Hrs", "Time to evidence pack"), ("100+", "Controls evidenced"), ("PII·SOX·GDPR", "Frameworks"), ("Repeatable", "Every cycle")],
        "Audit cycles force stewards to manually assemble evidence across Snowflake, Databricks, Oracle, ODS, and BI — slow and inconsistent.",
        ["Define audit scope and frameworks.", "MCP pulls classifications, ownership, lineage.", "Map metadata fields to controls.", "Generate repeatable evidence export."],
        [("Audit drift eliminated", "Same shape every cycle — auditor confidence improves."), ("Gaps surface pre-audit", "Missing owners and untagged PII identified early.")],
        [("Step 1 Scope", "Framework + asset universe."), ("Step 2 Pull", "Catalog posture via MCP."), ("Step 3 Map", "Metadata to controls."), ("Step 4 Pack", "Defensible evidence export.")],
    )
    add_deep_dive_slide(
        prs, 4,
        "Cursor–OMS MCP Use Case — Personal Data Assessment (STAQ)",
        "AI-assisted catalog analysis for Legal compliance requests — methodology reusable on OMS.",
        [("~4 hrs", "Manual effort"), ("< 30 min", "With AI assist"), ("1,100+", "Columns audited"), ("3", "Quality issues")],
        "Legal requests assessment of personal data across large schemas — traditionally multi-day steward + Confluence + SME work.",
        ["Automated catalog scan via MCP.", "Cross-reference Confluence/DEEPT docs.", "Business SME validation.", "Remediation plan + Jira tracking."],
        [("Evidence at scale", "Column-level classification scan across schemas."), ("Quality gaps identified", "Vendor lists and tags reconciled with SME input.")],
        [("Step 1 Scan", "Query MCP for columns + PII fields."), ("Step 2 Validate", "Cross-reference Confluence."), ("Step 3 Verify", "SME review."), ("Step 4 Remediate", "OMS/Navigator updates + ticket.")],
    )
    add_deep_dive_slide(
        prs, 5,
        "Cursor–OMS MCP Use Case — Field-Class Definition Standardization",
        "Standardize _id, _cd, _date, _timestamp — inherit from source through OMS to BI.",
        [("1000+", "Columns standardized"), ("Source → BI", "Inheritance path"), ("Consistent", "Across domains"), ("Reusable", "Teams & tools")],
        "Same column classes appear across tens of thousands of columns — defined inconsistently; manual curation cannot scale.",
        ["Field-class scan via MCP.", "AI proposes candidate definitions.", "Propagate through lineage into OMS.", "Steward approval — never AI-only."],
        [("Conflicts resolved", "Steward alignment on class meaning across domains."), ("Curation scales", "Approved definitions flow downstream automatically.")],
        [("Step 1 Scan", "Identify class patterns."), ("Step 2 Propose", "AI drafts per class."), ("Step 3 Inherit", "Lineage propagation to OMS."), ("Step 4 Approve", "Steward review and apply.")],
    )
    add_deep_dive_slide(
        prs, 6,
        "Cursor–OMS MCP Use Case — Metadata Enrichment & Documentation",
        "AI-drafted descriptions and glossary mappings — human-approved, written to OMS.",
        [("1000+", "Assets enriched"), ("Days → Mins", "Per asset effort"), ("AI-Assisted", "Human-approved"), ("Scalable", "Ad domains")],
        "Thousands of assets lack descriptions or glossary links — limiting search, AI quality, and audit readiness.",
        ["Coverage gap scan via MCP.", "AI draft enrichment proposals.", "Steward review queue.", "Push approved changes to OMS via API."],
        [("Sporadic → consistent", "Priority domains near-full documentation."), ("Humans in control", "Every enrichment reviewed and traceable.")],
        [("Step 1 Scan", "Undocumented assets in priority domains."), ("Step 2 Draft", "AI proposes descriptions + links."), ("Step 3 Review", "Steward approval queue."), ("Step 4 Apply", "Write to OMS; surface in Navigator.")],
    )

    # --- Slide 17: Metrics dashboard ---
    s = new_content_slide(
        prs,
        "Navigator & OMS — Metrics Dashboard (Target)",
        "Stewardship and adoption telemetry on OMS — Alation Compose exports inform migration baselines.",
    )
    tb = s.shapes.add_textbox(Inches(0.55), Inches(1.22), Inches(5.5), Inches(5.5))
    tf = tb.text_frame
    tf.word_wrap = True
    kpis = [
        "MONTHLY ACTIVE USERS — target ≥ Alation baseline (~411+) post-cutover",
        "SEARCH SESSIONS — discovery front door; title/description quality drives success",
        "TABLES ENDORSED / GOLD — trust signals visible in Navigator",
        "CATALOG COVERAGE (DESCRIBED) — 626/MCI supply + steward SLAs",
        "GLOSSARY TERMS — migrated + net-new on OMS",
        "PAGE VIEWS — engagement parity through parallel run",
    ]
    set_para(tf.paragraphs[0], "Executive Summary · Data Navigator on OMS", size=14, color=INK, bold=True, font=FONT_DISPLAY)
    set_para(tf.add_paragraph(), "Workspace prototype: alation-metrics-dashboard / OMS steward views", size=10, color=MUTED)
    for k in kpis:
        p = tf.add_paragraph()
        set_para(p, f"• {k}", size=11, color=INK)
        p.space_before = Pt(8)
    add_callout(
        s, Inches(1.18), Inches(2.8),
        "During migration: Alation Compose CSV baselines (e.g. 534 MAU, 27.9K searches/90d) — "
        "post-cutover measures shift to OMS/Navigator telemetry.",
        bg=AMBER_SOFT,
    )

    # --- Slide 18: Buy vs Build ---
    s = new_content_slide(
        prs,
        "Data Catalog Strategy: Buy vs Build",
        "Deep dive from Scaling Data Governance roadmap.",
    )
    for col, (hdr, sub, pros, cons) in enumerate([
        (
            "Buy (Continue Alation)",
            "Extend the established vendor catalog through renewal window.",
            ["Mature catalog; existing Ads footprint and connectors.", "Faster near-term value; known stewardship workflows.", "Vendor SLAs, certifications, and support.", "Broad connector library and peer patterns."],
            ["Recurring license cost; roadmap not fully controlled.", "Customization bounded by product model.", "Vendor lock-in deepens with adoption.", "Gaps for Disney-specific governance workflows."],
        ),
        (
            "Build (Navigator on OMS)",
            "In-house governed discovery — 626 supply, OMS store, Navigator UX.",
            ["Full control of Ads terminology, controls, and persona-first UX.", "Direct roadmap with OMS and 626/MCI programs.", "Tighter coupling with Cursor MCP on OMS read API.", "Lower marginal cost at scale; exit Oct 2026 contract."],
            ["Engineering investment for parity and migration.", "Multi-year delivery risk; business fields need population.", "Platform/SRE/security burden internal.", "MVP scope discipline required — no MCP/scraper creep in Navigator."],
        ),
    ]):
        left = Inches(0.55) + col * Inches(4.75)
        panel = s.shapes.add_shape(1, left, Inches(1.18), Inches(4.55), Inches(5.55))
        panel.fill.solid()
        panel.fill.fore_color.rgb = SOFT_BG[col]
        panel.line.color.rgb = COLORS[col]
        tb = s.shapes.add_textbox(left + Inches(0.15), Inches(1.28), Inches(4.25), Inches(5.3))
        tf = tb.text_frame
        tf.word_wrap = True
        set_para(tf.paragraphs[0], hdr, size=14, color=INK, bold=True, font=FONT_DISPLAY)
        set_para(tf.add_paragraph(), sub, size=10, color=MUTED)
        set_para(tf.add_paragraph(), "Pros", size=10, color=LIME, bold=True)
        for p in pros:
            bp = tf.add_paragraph()
            bp.text = f"• {p}"
            bp.font.size = Pt(9)
            bp.font.color.rgb = INK
            bp.font.name = FONT_BODY
        set_para(tf.add_paragraph(), "Cons", size=10, color=MAGENTA, bold=True)
        for c in cons:
            bp = tf.add_paragraph()
            bp.text = f"• {c}"
            bp.font.size = Pt(9)
            bp.font.color.rgb = INK
            bp.font.name = FONT_BODY

    # --- Slide 19: Socialization ---
    s = new_content_slide(
        prs,
        "Data Navigator Socialization Plan",
        "Phased approach to drive alignment, awareness, and adoption across Ad Platforms.",
    )
    phases = [
        ("COMPLETED – 5/18", "Ad Platforms Data Governance", "Ad Platforms DG Team", ["Initial team review", "Aligned on persona-first messaging"]),
        ("COMPLETED – 6/1", "DEE Tech Data Governance", "Disney Enterprise DG", ["Align with enterprise catalog strategy", "Connect to OMS migration initiatives"]),
        ("TARGET – FY26 Q3", "Engineering Alignment", "OMS / platform partners", ["Validate Navigator vs OMS UI handoffs", "Share with engineering leadership"]),
        ("TARGET – FY26 Q3", "Product Alignment", "Domain product leads", ["Align data domains and MVP stories", "Confirm business use cases for Navigator"]),
        ("TARGET – FY26 Q4", "Fleets & Squads", "Stewards & domain teams", ["Tailor messaging for stewards", "Drive adoption as Alation parallel run begins"]),
    ]
    pw = Inches(1.85)
    for i, (status, title, lead, bullets) in enumerate(phases):
        left = Inches(0.45) + i * pw
        add_card(s, left, Inches(1.18), pw - Inches(0.05), Inches(5.35), COLORS[i % 4], title, lead, 9, 8)
        st = s.shapes.add_textbox(left + Inches(0.2), Inches(1.24), pw - Inches(0.15), Inches(0.2))
        sc = LIME if "COMPLETED" in status else VIOLET
        set_para(st.text_frame.paragraphs[0], status, size=7, color=sc, bold=True)
        num = s.shapes.add_textbox(left + Inches(0.2), Inches(1.75), Inches(0.25), Inches(0.25))
        set_para(num.text_frame.paragraphs[0], str(i + 1), size=12, color=VIOLET, bold=True, font=FONT_DISPLAY)
        tb2 = s.shapes.add_textbox(left + Inches(0.2), Inches(2.05), pw - Inches(0.15), Inches(4.2))
        tf = tb2.text_frame
        tf.word_wrap = True
        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(7)
            p.font.color.rgb = INK
            p.font.name = FONT_BODY

    prs.save(OUT)
    print(f"Wrote {OUT} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    build()
