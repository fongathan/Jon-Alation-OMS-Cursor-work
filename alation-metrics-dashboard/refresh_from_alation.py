#!/usr/bin/env python3
"""
Alation Metrics Dashboard — Refresh from Alation REST API
==========================================================
Fetches query results from Alation and writes data.json.
Use with cron for automated daily refresh.

Usage:
    python3 refresh_from_alation.py

Requires:
    - 8 saved queries in Alation Compose (against Analytics V2)
    - .env with ALATION_BASE_URL, ALATION_REFRESH_TOKEN, ALATION_USER_ID
    - Each query run at least once (or scheduled) so results exist
"""

import csv
import io
import json
import os
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("ALATION_BASE_URL", "").rstrip("/")
REFRESH_TOKEN = os.getenv("ALATION_REFRESH_TOKEN", "")
USER_ID = int(os.getenv("ALATION_USER_ID", "0") or 0)
API_TOKEN = os.getenv("ALATION_API_TOKEN", "")  # optional; if set, used directly

# Query IDs — fill these in after saving queries in Alation Compose
QUERY_IDS = {
    "01_summary":         int(os.getenv("ALATION_QUERY_01_SUMMARY", "0") or 0),
    "02_top_users":       int(os.getenv("ALATION_QUERY_02_TOP_USERS", "0") or 0),
    "03_curation_monthly": int(os.getenv("ALATION_QUERY_03_CURATION", "0") or 0),
    "04_dau_mau_monthly": int(os.getenv("ALATION_QUERY_04_DAU_MAU", "0") or 0),
    "05_top_searches":    int(os.getenv("ALATION_QUERY_05_SEARCHES", "0") or 0),
    "06_top_visited":     int(os.getenv("ALATION_QUERY_06_VISITED", "0") or 0),
    "07_governance_feed": int(os.getenv("ALATION_QUERY_07_GOVERNANCE", "0") or 0),
    "08_search_daily":    int(os.getenv("ALATION_QUERY_08_SEARCH_DAILY", "0") or 0),
}

OUTPUT = os.path.join(os.path.dirname(__file__), "data.json")


def get_access_token():
    """Get API access token from refresh token (or use ALATION_API_TOKEN if set)."""
    if API_TOKEN:
        return API_TOKEN
    if not REFRESH_TOKEN or not USER_ID:
        print("Error: Set ALATION_REFRESH_TOKEN and ALATION_USER_ID in .env (or ALATION_API_TOKEN)")
        sys.exit(1)
    r = requests.post(
        f"{BASE_URL}/integration/v1/createAPIAccessToken/",
        json={"refresh_token": REFRESH_TOKEN, "user_id": USER_ID},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    return data.get("api_access_token", "")


def fetch_query_csv(token, query_id):
    """Get latest result for a query and return CSV rows as list of dicts."""
    headers = {"Token": token}
    # 1. Get latest execution result ID
    r = requests.get(
        f"{BASE_URL}/integration/v1/query/{query_id}/result/latest/",
        headers=headers,
        timeout=30,
    )
    if r.status_code == 404:
        return []
    r.raise_for_status()
    latest = r.json()
    result_id = latest.get("id")
    if not result_id:
        return []
    # 2. Get CSV content
    r2 = requests.get(
        f"{BASE_URL}/integration/v1/result/{result_id}/csv/",
        headers=headers,
        timeout=60,
    )
    r2.raise_for_status()
    text = r2.content.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def safe_int(val, default=0):
    try:
        return int(float(str(val).replace(",", "").strip()))
    except (ValueError, TypeError):
        return default


def pct(num, den):
    return round(safe_int(num) * 100 / max(safe_int(den), 1), 1)


def build_from_rows(name, rows, builder_fn):
    """Run builder on rows, using expected CSV column mapping per query."""
    if not rows:
        return None
    # API returns same columns as manual CSV export
    return builder_fn(rows)


def main():
    if not BASE_URL:
        print("Error: Set ALATION_BASE_URL in .env (e.g. https://disney-data.alationcloud.com)")
        sys.exit(1)

    token = get_access_token()
    if not token:
        print("Error: Could not obtain API access token")
        sys.exit(1)

    # Map query names to CSV filenames / expected structure
    csv_data = {}
    for key, qid in QUERY_IDS.items():
        if qid <= 0:
            continue
        try:
            rows = fetch_query_csv(token, qid)
            csv_data[key] = rows
        except Exception as e:
            print(f"  ⚠  Query {key} (id={qid}): {e}")

    # Build data structure (same logic as build_json.py)
    def _summary(rows):
        if not rows:
            return None
        r = rows[0]
        total_tables = safe_int(r.get("tables_total"))
        tables_desc = safe_int(r.get("tables_described"))
        tables_stew = safe_int(r.get("tables_stewarded"))
        tables_end = safe_int(r.get("tables_endorsed"))
        return {
            "mau": safe_int(r.get("mau")),
            "dau_avg": safe_int(r.get("avg_daily_views")),
            "new_users": safe_int(r.get("new_users_90d")),
            "searches_total": safe_int(r.get("searches_90d")),
            "page_views_total": safe_int(r.get("page_views_90d")),
            "deprecations": safe_int(r.get("deprecations_90d")),
            "articles_total": safe_int(r.get("articles_total")),
            "terms_total": safe_int(r.get("terms_total")),
            "total_tables": total_tables,
            "endorsed_pct": pct(tables_end, total_tables),
            "description_coverage_pct": pct(tables_desc, total_tables),
            "steward_pct": pct(tables_stew, total_tables),
        }

    def _top_users(rows):
        return [
            {
                "display_name": r.get("display_name", ""),
                "email": r.get("email", ""),
                "endorsements": safe_int(r.get("endorsements")),
                "deprecations": safe_int(r.get("deprecations")),
                "total_flags": safe_int(r.get("total_flags")),
            }
            for r in rows
        ]

    def _curation_monthly(rows):
        if not rows:
            return None
        return {
            "months": [r.get("month", "") for r in rows],
            "endorsed": [safe_int(r.get("endorsed")) for r in rows],
            "deprecated": [safe_int(r.get("deprecated")) for r in rows],
            "warned": [safe_int(r.get("warned")) for r in rows],
        }

    def _dau_mau(rows):
        if not rows:
            return None
        return {
            "months": [r.get("month", "") for r in rows],
            "mau": [safe_int(r.get("mau")) for r in rows],
            "dau": [safe_int(r.get("avg_daily_views")) for r in rows],
        }

    def _top_searches(rows):
        return [{"query": r.get("query_text", ""), "count": safe_int(r.get("search_count"))} for r in rows]

    def _top_visited(rows):
        return [
            {"name": r.get("object_name", ""), "type": r.get("object_type", "other"), "views": safe_int(r.get("views"))}
            for r in rows
        ]

    def _governance_feed(rows):
        return [
            {
                "type": r.get("flag_type", ""),
                "user": r.get("curator", ""),
                "object": r.get("object_name", ""),
                "datasource": r.get("datasource", ""),
                "date": r.get("event_date", ""),
            }
            for r in rows
        ]

    def _search_daily(rows):
        if not rows:
            return None
        return {
            "dates": [r.get("day", "") for r in rows],
            "searches": [safe_int(r.get("searches")) for r in rows],
        }

    summary = build_from_rows("01_summary", csv_data.get("01_summary", []), lambda r: _summary(r))
    top_users = build_from_rows("02_top_users", csv_data.get("02_top_users", []), lambda r: _top_users(r)) or []
    curation = build_from_rows("03_curation_monthly", csv_data.get("03_curation_monthly", []), lambda r: _curation_monthly(r))
    dau_mau = build_from_rows("04_dau_mau_monthly", csv_data.get("04_dau_mau_monthly", []), lambda r: _dau_mau(r))
    top_searches = build_from_rows("05_top_searches", csv_data.get("05_top_searches", []), lambda r: _top_searches(r)) or []
    top_visited = build_from_rows("06_top_visited", csv_data.get("06_top_visited", []), lambda r: _top_visited(r)) or []
    governance = build_from_rows("07_governance_feed", csv_data.get("07_governance_feed", []), lambda r: _governance_feed(r)) or []
    search_daily = build_from_rows("08_search_daily", csv_data.get("08_search_daily", []), lambda r: _search_daily(r))

    catalog_coverage = None
    if summary:
        catalog_coverage = {
            "description_pct": summary["description_coverage_pct"],
            "steward_pct": summary["steward_pct"],
            "endorsed_pct": summary["endorsed_pct"],
        }

    data = {
        "meta": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "period_days": 90,
            "source": f"Alation API ({BASE_URL})",
        },
        "summary": summary,
        "dau_mau_12m": dau_mau,
        "top_users": top_users,
        "curation_monthly": curation,
        "catalog_coverage": catalog_coverage,
        "top_curators": top_users,
        "search_daily": search_daily,
        "top_searches": top_searches,
        "top_visited": top_visited,
        "governance_feed": governance,
    }
    data = {k: v for k, v in data.items() if v is not None}

    with open(OUTPUT, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✓ data.json written to {OUTPUT}")
    if summary:
        print(f"  MAU: {summary['mau']:,}  |  Searches: {summary['searches_total']:,}  |  Endorsed: {summary['endorsed_pct']}%")
    print(f"  Top user: {top_users[0]['display_name'] if top_users else '—'}")


if __name__ == "__main__":
    main()
