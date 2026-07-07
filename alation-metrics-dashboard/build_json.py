#!/usr/bin/env python3
"""
Alation Metrics Dashboard — CSV → data.json Builder
=====================================================
Run this after downloading all 8 CSVs from Alation Compose.

Usage:
    python3 build_json.py

Reads CSVs from:  ./compose-exports/01_summary.csv  (etc.)
Writes:           ./data.json
"""

import csv
import json
import os
from datetime import datetime

EXPORTS = os.path.join(os.path.dirname(__file__), "compose-exports")
OUTPUT  = os.path.join(os.path.dirname(__file__), "data.json")


def read_csv(filename):
    path = os.path.join(EXPORTS, filename)
    if not os.path.exists(path):
        print(f"  ⚠  Missing: {filename} — skipping")
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def safe_int(val, default=0):
    try:
        return int(float(str(val).replace(",", "").strip()))
    except (ValueError, TypeError):
        return default


def safe_float(val, default=0.0):
    try:
        return round(float(str(val).replace(",", "").strip()), 1)
    except (ValueError, TypeError):
        return default


def pct(num, den):
    return round(safe_int(num) * 100 / max(safe_int(den), 1), 1)


# ─── 01  Summary KPIs ─────────────────────────────────────────────────────────
def build_summary():
    rows = read_csv("01_summary.csv")
    if not rows:
        return None
    r = rows[0]

    total_tables   = safe_int(r.get("tables_total"))
    tables_desc    = safe_int(r.get("tables_described"))
    tables_stew    = safe_int(r.get("tables_stewarded"))
    tables_end     = safe_int(r.get("tables_endorsed"))

    return {
        "mau":                      safe_int(r.get("mau")),
        "dau_avg":                  safe_int(r.get("avg_daily_views")),
        "new_users":                safe_int(r.get("new_users_90d")),
        "searches_total":           safe_int(r.get("searches_90d")),
        "page_views_total":         safe_int(r.get("page_views_90d")),
        "deprecations":             safe_int(r.get("deprecations_90d")),
        "articles_total":           safe_int(r.get("articles_total")),
        "terms_total":              safe_int(r.get("terms_total")),
        "total_tables":             total_tables,
        "endorsed_pct":             pct(tables_end,  total_tables),
        "description_coverage_pct": pct(tables_desc,  total_tables),
        "steward_pct":              pct(tables_stew,  total_tables),
    }


# ─── 02  Top Users ────────────────────────────────────────────────────────────
def build_top_users():
    rows = read_csv("02_top_users.csv")
    return [
        {
            "display_name": r.get("display_name", ""),
            "email":        r.get("email", ""),
            "endorsements": safe_int(r.get("endorsements")),
            "deprecations": safe_int(r.get("deprecations")),
            "total_flags":  safe_int(r.get("total_flags")),
        }
        for r in rows
    ]


# ─── 03  Curation Monthly ─────────────────────────────────────────────────────
def build_curation_monthly():
    rows = read_csv("03_curation_monthly.csv")
    if not rows:
        return None
    return {
        "months":     [r.get("month", "") for r in rows],
        "endorsed":   [safe_int(r.get("endorsed"))   for r in rows],
        "deprecated": [safe_int(r.get("deprecated")) for r in rows],
        "warned":     [safe_int(r.get("warned"))      for r in rows],
    }


# ─── 04  DAU / MAU Monthly ────────────────────────────────────────────────────
def build_dau_mau():
    rows = read_csv("04_dau_mau_monthly.csv")
    if not rows:
        return None
    return {
        "months": [r.get("month", "") for r in rows],
        "mau":    [safe_int(r.get("mau"))            for r in rows],
        "dau":    [safe_int(r.get("avg_daily_views")) for r in rows],
    }


# ─── 05  Top Searches ─────────────────────────────────────────────────────────
def build_top_searches():
    rows = read_csv("05_top_searches.csv")
    return [
        {"query": r.get("query_text", ""), "count": safe_int(r.get("search_count"))}
        for r in rows
    ]


# ─── 06  Top Visited ──────────────────────────────────────────────────────────
def build_top_visited():
    rows = read_csv("06_top_visited.csv")
    return [
        {
            "name":  r.get("object_name", ""),
            "type":  r.get("object_type", "other"),
            "views": safe_int(r.get("views")),
        }
        for r in rows
    ]


# ─── 07  Governance Feed ──────────────────────────────────────────────────────
def build_governance_feed():
    rows = read_csv("07_governance_feed.csv")
    return [
        {
            "type":       r.get("flag_type", ""),
            "user":       r.get("curator", ""),
            "object":     r.get("object_name", ""),
            "datasource": r.get("datasource", ""),
            "date":       r.get("event_date", ""),
        }
        for r in rows
    ]


# ─── 08  Search Daily ─────────────────────────────────────────────────────────
def build_search_daily():
    rows = read_csv("08_search_daily.csv")
    if not rows:
        return None
    return {
        "dates":   [r.get("day", "") for r in rows],
        "searches": [safe_int(r.get("searches")) for r in rows],
    }


# ─── ASSEMBLE ─────────────────────────────────────────────────────────────────
def main():
    print("Building data.json from compose-exports/ …\n")

    summary = build_summary()
    if summary:
        # catalog_coverage mirrors summary pct fields for the coverage bars
        catalog_coverage = {
            "description_pct": summary["description_coverage_pct"],
            "steward_pct":      summary["steward_pct"],
            "endorsed_pct":     summary["endorsed_pct"],
        }
    else:
        catalog_coverage = None

    top_users = build_top_users()

    data = {
        "meta": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "period_days":  90,
            "source":       "Alation Compose CSV exports",
        },
        "summary":          summary,
        "dau_mau_12m":      build_dau_mau(),
        "top_users":        top_users,
        "curation_monthly": build_curation_monthly(),
        "catalog_coverage": catalog_coverage,
        "top_curators":     top_users,   # same data, shown on curation page
        "search_daily":     build_search_daily(),
        "top_searches":     build_top_searches(),
        "top_visited":      build_top_visited(),
        "governance_feed":  build_governance_feed(),
        # trend_90d and amp_terms need a separate query; fall back to sample
        "trend_90d":        None,
        "amp_terms":        None,
    }

    # Remove None values so the dashboard falls back to sample for those keys
    data = {k: v for k, v in data.items() if v is not None}

    with open(OUTPUT, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✓  data.json written to {OUTPUT}")

    # Print a quick summary
    if summary:
        print(f"\n  MAU:              {summary['mau']:,}")
        print(f"  Searches (90d):   {summary['searches_total']:,}")
        print(f"  Page views (90d): {summary['page_views_total']:,}")
        print(f"  Endorsed %:       {summary['endorsed_pct']}%")
        print(f"  Description cov:  {summary['description_coverage_pct']}%")
    print(f"\n  Top user:         {top_users[0]['display_name'] if top_users else '—'}")
    print(f"\nOpen index.html in your browser and refresh — it will now show live data.")


if __name__ == "__main__":
    main()
