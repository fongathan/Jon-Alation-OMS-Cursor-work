---
name: html-theme-midnight-ops
description: >-
  Styles HTML dashboards with the Midnight Ops theme: dark blue shell, grid +
  glow background, Plus Jakarta Sans, KPI cards, panels, tables, pills. Use
  for admin UIs, metrics dashboards, status boards, charts, or when the user
  asks for Midnight Ops, dark dashboard styling, or theme-midnight-ops.css.
---

# Midnight Ops HTML theme

## Canonical theme files (source of truth)

On this machine the CSS lives here (copy from here into any other project):

- **Directory:** `/Users/jonathan.fong/Documents/Jon Alation OMS Cursor work/data-catalog-expansion/themes/`
- **CSS:** `theme-midnight-ops.css`
- **Reference:** `USAGE.txt`
- **Example page:** `/Users/jonathan.fong/Documents/Jon Alation OMS Cursor work/data-catalog-expansion/admin-dashboard.html`

In the **Jon Alation OMS Cursor work** repo, relative paths from `data-catalog-expansion/` HTML files are:

- `themes/theme-midnight-ops.css`

**Global skill copy:** `~/.cursor/skills/html-theme-midnight-ops/SKILL.md` (same instructions in any workspace).

## When to use

Internal tools, KPIs, charts (e.g. Chart.js), filters, data tables. Typical structure:

- Optional fixed layers (before main): `.bg-grid`, `.glow.a`, `.glow.b`
- `.shell` wrapping content with `z-index` above glows
- `.title-block`, `.header-actions`, `.btn` / `.btn-primary` / `.btn-ghost`
- `.kpis` with `.kpi.c1` … `.c4`, `.grid-main`, `.panel`, `.chart-wrap`, `select.filter`
- Tables: `table.vendor-table`, `.pill` (`.warehouse`, `.activation`, `.cdp`, `.engage`), `.progress-mini`
- `footer.nav-foot` for footer links

## Setup

1. Add **font** from the comment block at the **top** of `theme-midnight-ops.css` (Plus Jakarta Sans).
2. Link the stylesheet (adjust `href` to file location):

   ```html
   <link rel="stylesheet" href="themes/theme-midnight-ops.css">
   ```

## Other projects (global use)

When building HTML **outside** this workspace: **copy** `theme-midnight-ops.css` (and optionally `USAGE.txt`) into the new project’s `themes/` folder, then link with `href="themes/theme-midnight-ops.css"`. Do not rely on absolute `file://` links for shipping pages.

## Conflicts

Do **not** load `theme-editorial-hero.css` on the same page. For narrative/program pages use the Editorial Hero skill instead.

## Agent behavior

Prefer linking the shared CSS file over duplicating dashboard CSS. Chart libraries load separately (CDN or bundle).
