---
name: html-theme-editorial-hero
description: >-
  Styles HTML pages with the Editorial Hero theme: light paper background,
  indigo gradient hero, Outfit + Source Serif 4, cards, timelines, program
  plans. Use for narrative pages, executive briefs, stakeholder one-pagers,
  migration/program plans, or when the user asks for Editorial Hero, light
  editorial layout, or theme-editorial-hero.css.
---

# Editorial Hero HTML theme

## Canonical theme files (source of truth)

On this machine the CSS lives here (copy from here into any other project):

- **Directory:** `/Users/jonathan.fong/Documents/Jon Alation OMS Cursor work/data-catalog-expansion/themes/`
- **CSS:** `theme-editorial-hero.css`
- **Reference:** `USAGE.txt`
- **Example page:** `/Users/jonathan.fong/Documents/Jon Alation OMS Cursor work/data-catalog-expansion/program-plan.html`

In the **Jon Alation OMS Cursor work** repo, relative paths from `data-catalog-expansion/` HTML files are:

- `themes/theme-editorial-hero.css`

**Global skill copy:** `~/.cursor/skills/html-theme-editorial-hero/SKILL.md` (same instructions in any workspace).

## When to use

Long-form narrative, program plans, executive summaries, feature briefs. Typical structure:

- `header.hero` with `.hero-inner`, `.badge-row`, `.badge`, `h1`, `.hero-lead`, `.hero-cta`, `.btn` / `.btn-primary` / `.btn-ghost`
- `main.wrap` (or equivalent) for body sections
- Optional: `.callout`, `.grid-2`, `.card`, `.tag`, `.timeline`, semantic `table`, `footer`

## Setup

1. Add **fonts** from the comment block at the **top** of `theme-editorial-hero.css` (Outfit + Source Serif 4).
2. Link the stylesheet (adjust `href` to file location):

   ```html
   <link rel="stylesheet" href="themes/theme-editorial-hero.css">
   ```

## Other projects (global use)

When building HTML **outside** this workspace: **copy** `theme-editorial-hero.css` (and optionally `USAGE.txt`) into the new project’s `themes/` folder, then link with `href="themes/theme-editorial-hero.css"`. Do not rely on absolute `file://` links for shipping pages.

## Conflicts

Do **not** load `theme-midnight-ops.css` on the same page (both set global `body` styles). For dashboards use the Midnight Ops skill instead.

## Agent behavior

Prefer linking the shared CSS file over pasting large inline `<style>` blocks.
