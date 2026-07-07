#!/usr/bin/env python3
"""
Alation Metrics Dashboard — Data Export Script
================================================
Queries the Alation Analytics v2 PostgreSQL database and writes data.json
into the same directory, which the dashboard HTML then reads.

Usage:
    python export.py                          # uses .env in this directory
    PERIOD_DAYS=30 python export.py           # override period

Schedule (cron example – daily at 6 AM):
    0 6 * * * cd /path/to/alation-metrics-dashboard && python export.py

Requirements:
    pip install -r requirements.txt
"""

import os
import json
import logging
from datetime import datetime
from collections import defaultdict

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ─── CONNECTION CONFIG ──────────────────────────────────────────────────────
DB = {
    "host":     os.getenv("ALATION_ANALYTICS_HOST",     "localhost"),
    "port":     int(os.getenv("ALATION_ANALYTICS_PORT", "5432")),
    "dbname":   os.getenv("ALATION_ANALYTICS_DB",       "alation_analytics"),
    "user":     os.getenv("ALATION_ANALYTICS_USER",      "alation_analytics"),
    "password": os.getenv("ALATION_ANALYTICS_PASSWORD",  ""),
    "connect_timeout": 10,
}
PERIOD_DAYS = int(os.getenv("PERIOD_DAYS", "90"))
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data.json")


# ─── DB HELPERS ─────────────────────────────────────────────────────────────
def connect():
    return psycopg2.connect(**DB)


def rows(conn, sql, params=()):
    """Return all rows as a list of plain dicts."""
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, params)
        return [dict(r) for r in cur.fetchall()]


def scalar(conn, sql, params=(), default=0):
    """Return the first column of the first row, or default."""
    rs = rows(conn, sql, params)
    if not rs:
        return default
    v = list(rs[0].values())[0]
    return v if v is not None else default


def safe(name, fn):
    """Run fn(), log any error and return None so one failure doesn't block others."""
    try:
        log.info(f"  → {name}")
        return fn()
    except Exception as exc:
        log.warning(f"  ✗ {name}: {exc}")
        return None


# ─── METRIC QUERIES ─────────────────────────────────────────────────────────

def get_summary(conn, days):
    """Top-line KPIs for the dashboard header cards."""
    period = f"{days} days"

    mau = scalar(conn, """
        SELECT COUNT(DISTINCT user_id)
        FROM   public.visits
        WHERE  ts_created >= NOW() - INTERVAL %s
          AND  user_id IS NOT NULL
    """, (period,))

    dau_avg = scalar(conn, """
        SELECT ROUND(AVG(dau)::numeric, 0)::int
        FROM (
            SELECT DATE_TRUNC('day', ts_created) AS d,
                   COUNT(DISTINCT user_id)        AS dau
            FROM   public.visits
            WHERE  ts_created >= NOW() - INTERVAL %s
              AND  user_id IS NOT NULL
            GROUP BY 1
        ) sub
    """, (period,))

    new_users = scalar(conn, """
        SELECT COUNT(*)
        FROM   public.users
        WHERE  ts_created >= NOW() - INTERVAL %s
          AND  is_active = true
    """, (period,))

    searches = scalar(conn, """
        SELECT COUNT(*)
        FROM   public.search_queries
        WHERE  ts_created >= NOW() - INTERVAL %s
    """, (period,))

    page_views = scalar(conn, """
        SELECT COUNT(*)
        FROM   public.visits
        WHERE  ts_created >= NOW() - INTERVAL %s
    """, (period,))

    deprecations = scalar(conn, """
        SELECT COUNT(*)
        FROM   public.flags
        WHERE  flag_type    = 'DEPRECATION'
          AND  ts_created  >= NOW() - INTERVAL %s
          AND  ts_deleted  IS NULL
    """, (period,))

    articles = scalar(conn, "SELECT COUNT(*) FROM public.article WHERE ts_deleted IS NULL")
    terms    = scalar(conn, "SELECT COUNT(*) FROM public.terms   WHERE ts_deleted IS NULL")

    total_tables = scalar(conn, "SELECT COUNT(*) FROM public.rdbms_tables WHERE ts_deleted IS NULL")

    described = scalar(conn, """
        SELECT COUNT(*) FROM public.rdbms_tables
        WHERE  ts_deleted IS NULL
          AND  description IS NOT NULL AND description <> ''
    """)

    stewarded = scalar(conn, """
        SELECT COUNT(*) FROM public.rdbms_tables
        WHERE  ts_deleted IS NULL
          AND  steward IS NOT NULL AND steward <> ''
    """)

    endorsed = scalar(conn, """
        SELECT COUNT(DISTINCT object_id)
        FROM   public.flags
        WHERE  flag_type   = 'ENDORSEMENT'
          AND  ts_deleted IS NULL
    """)

    def pct(num, den):
        return round(num * 100 / max(den, 1), 1)

    return {
        "mau":                      int(mau),
        "dau_avg":                  int(dau_avg),
        "new_users":                int(new_users),
        "searches_total":           int(searches),
        "page_views_total":         int(page_views),
        "deprecations":             int(deprecations),
        "articles_total":           int(articles),
        "terms_total":              int(terms),
        "endorsed_pct":             pct(endorsed, total_tables),
        "description_coverage_pct": pct(described, total_tables),
        "steward_pct":              pct(stewarded, total_tables),
        "total_tables":             int(total_tables),
    }


def get_trend(conn, days):
    """Daily search sessions, curations, and page views for the trend chart."""
    period = f"{days} days"

    search_rows = rows(conn, """
        SELECT DATE_TRUNC('day', ts_created)::date AS day,
               COUNT(*)                             AS n
        FROM   public.search_queries
        WHERE  ts_created >= NOW() - INTERVAL %s
        GROUP BY 1 ORDER BY 1
    """, (period,))

    view_rows = rows(conn, """
        SELECT DATE_TRUNC('day', ts_created)::date AS day,
               COUNT(*)                             AS n
        FROM   public.visits
        WHERE  ts_created >= NOW() - INTERVAL %s
        GROUP BY 1 ORDER BY 1
    """, (period,))

    curation_rows = rows(conn, """
        SELECT DATE_TRUNC('day', ts_created)::date AS day,
               COUNT(*)                             AS n
        FROM   public.flags
        WHERE  ts_created  >= NOW() - INTERVAL %s
          AND  ts_deleted  IS NULL
        GROUP BY 1 ORDER BY 1
    """, (period,))

    s_map = {str(r["day"]): int(r["n"]) for r in search_rows}
    v_map = {str(r["day"]): int(r["n"]) for r in view_rows}
    c_map = {str(r["day"]): int(r["n"]) for r in curation_rows}
    all_dates = sorted(set(list(s_map) + list(v_map) + list(c_map)))

    return {
        "dates":      all_dates,
        "searches":   [s_map.get(d, 0) for d in all_dates],
        "page_views": [v_map.get(d, 0) for d in all_dates],
        "curations":  [c_map.get(d, 0) for d in all_dates],
    }


def get_dau_mau_12m(conn):
    """Monthly MAU and average DAU for the 12-month trend chart."""
    mau_rows = rows(conn, """
        SELECT DATE_TRUNC('month', ts_created)::date AS month,
               COUNT(DISTINCT user_id)               AS mau
        FROM   public.visits
        WHERE  ts_created >= NOW() - INTERVAL '12 months'
          AND  user_id IS NOT NULL
        GROUP BY 1 ORDER BY 1
    """)

    dau_rows = rows(conn, """
        SELECT month, ROUND(AVG(dau)::numeric, 0)::int AS dau_avg
        FROM (
            SELECT DATE_TRUNC('month', ts_created)::date AS month,
                   DATE_TRUNC('day',   ts_created)::date AS day,
                   COUNT(DISTINCT user_id)               AS dau
            FROM   public.visits
            WHERE  ts_created >= NOW() - INTERVAL '12 months'
              AND  user_id IS NOT NULL
            GROUP BY 1, 2
        ) sub
        GROUP BY 1 ORDER BY 1
    """)

    mau_map = {str(r["month"]): int(r["mau"])     for r in mau_rows}
    dau_map = {str(r["month"]): int(r["dau_avg"]) for r in dau_rows}
    months  = sorted(set(list(mau_map) + list(dau_map)))

    def fmt(m):
        return datetime.strptime(m, "%Y-%m-%d").strftime("%b '%y")

    return {
        "months": [fmt(m) for m in months],
        "mau":    [mau_map.get(m, 0) for m in months],
        "dau":    [dau_map.get(m, 0) for m in months],
    }


def get_top_users(conn, days, limit=10):
    """Power users ranked by total curation activity."""
    period = f"{days} days"
    rs = rows(conn, """
        SELECT u.display_name,
               u.email,
               COUNT(CASE WHEN f.flag_type = 'ENDORSEMENT' THEN 1 END) AS endorsements,
               COUNT(CASE WHEN f.flag_type = 'DEPRECATION' THEN 1 END) AS deprecations,
               COUNT(*)                                                  AS total_flags
        FROM   public.flags f
        JOIN   public.users u ON u.id = f.user_id
        WHERE  f.ts_created  >= NOW() - INTERVAL %s
          AND  f.ts_deleted  IS NULL
          AND  u.is_active    = true
        GROUP BY u.id, u.display_name, u.email
        ORDER BY total_flags DESC
        LIMIT %s
    """, (period, limit))
    return [
        {
            "display_name": r["display_name"],
            "email":        r["email"] or "",
            "endorsements": int(r["endorsements"]),
            "deprecations": int(r["deprecations"]),
            "total_flags":  int(r["total_flags"]),
        }
        for r in rs
    ]


def get_curation_monthly(conn):
    """Monthly breakdown of endorsements, deprecations, and warnings."""
    rs = rows(conn, """
        SELECT DATE_TRUNC('month', ts_created)::date AS month,
               flag_type,
               COUNT(*)                              AS cnt
        FROM   public.flags
        WHERE  ts_created  >= NOW() - INTERVAL '12 months'
          AND  ts_deleted  IS NULL
        GROUP BY 1, 2 ORDER BY 1, 2
    """)

    months = sorted({str(r["month"]) for r in rs})
    by_type: dict = defaultdict(lambda: defaultdict(int))
    for r in rs:
        by_type[r["flag_type"]][str(r["month"])] = int(r["cnt"])

    def fmt(m):
        return datetime.strptime(m, "%Y-%m-%d").strftime("%b '%y")

    return {
        "months":     [fmt(m) for m in months],
        "endorsed":   [by_type["ENDORSEMENT"].get(m, 0) for m in months],
        "deprecated": [by_type["DEPRECATION"].get(m, 0) for m in months],
        "warned":     [by_type["WARNING"].get(m, 0)     for m in months],
    }


def get_catalog_coverage(conn):
    """Coverage percentages for various catalog quality dimensions."""
    total = scalar(conn, "SELECT COUNT(*) FROM public.rdbms_tables WHERE ts_deleted IS NULL")
    if total == 0:
        return {}

    def pct(num):
        return round(int(num) * 100 / max(int(total), 1), 1)

    described = scalar(conn, """
        SELECT COUNT(*) FROM public.rdbms_tables
        WHERE ts_deleted IS NULL AND description IS NOT NULL AND description <> ''
    """)
    stewarded = scalar(conn, """
        SELECT COUNT(*) FROM public.rdbms_tables
        WHERE ts_deleted IS NULL AND steward IS NOT NULL AND steward <> ''
    """)
    endorsed = scalar(conn, """
        SELECT COUNT(DISTINCT object_id) FROM public.flags
        WHERE flag_type = 'ENDORSEMENT' AND ts_deleted IS NULL
    """)

    total_queries  = scalar(conn, "SELECT COUNT(*) FROM public.query WHERE ts_deleted IS NULL")
    titled_queries = scalar(conn, """
        SELECT COUNT(*) FROM public.query
        WHERE ts_deleted IS NULL AND title IS NOT NULL AND title <> ''
    """)

    # Columns with any customfield value set (proxy for "term tagged")
    total_cols  = scalar(conn, "SELECT COUNT(*) FROM public.rdbms_columns WHERE ts_deleted IS NULL")
    tagged_cols = scalar(conn, """
        SELECT COUNT(DISTINCT cfv.object_id)
        FROM   public.customfieldvalue cfv
        JOIN   public.rdbms_columns rc ON rc.id = cfv.object_id
        WHERE  cfv.ts_deleted IS NULL AND rc.ts_deleted IS NULL
    """, default=0)

    return {
        "description_pct":  pct(described),
        "steward_pct":       pct(stewarded),
        "endorsed_pct":      pct(endorsed),
        "term_tagged_pct":   round(int(tagged_cols) * 100 / max(int(total_cols), 1), 1) if total_cols else 0,
        "query_titled_pct":  round(int(titled_queries) * 100 / max(int(total_queries), 1), 1) if total_queries else 0,
    }


def get_top_curators(conn, days, limit=10):
    """Top curators (same shape as top_users but labelled for the curation page)."""
    return get_top_users(conn, days, limit)


def get_amp_terms(conn, limit=15):
    """
    AMP glossary terms ranked by how many tables reference them.
    Tries catalog_set_membership (if terms are stored as catalog sets),
    then falls back to returning terms ordered by creation date.
    """
    try:
        rs = rows(conn, """
            SELECT t.title                          AS term,
                   COUNT(DISTINCT csm.object_id)   AS tables_tagged
            FROM   public.terms t
            JOIN   public.catalog_set_membership csm ON csm.catalog_set_id = t.id
            WHERE  t.ts_deleted IS NULL
            GROUP BY t.id, t.title
            ORDER BY tables_tagged DESC
            LIMIT %s
        """, (limit,))
        if rs:
            return [{"term": r["term"], "tables": int(r["tables_tagged"])} for r in rs]
    except Exception:
        pass

    # Fallback: just list terms
    rs = rows(conn, """
        SELECT title AS term FROM public.terms
        WHERE  ts_deleted IS NULL
        ORDER BY ts_created DESC LIMIT %s
    """, (limit,))
    return [{"term": r["term"], "tables": 0} for r in rs]


def get_search_daily(conn, days):
    """Daily search session counts for the bar chart."""
    period = f"{days} days"
    rs = rows(conn, """
        SELECT DATE_TRUNC('day', ts_created)::date AS day,
               COUNT(*)                             AS n
        FROM   public.search_queries
        WHERE  ts_created >= NOW() - INTERVAL %s
        GROUP BY 1 ORDER BY 1
    """, (period,))
    return {
        "dates":   [str(r["day"]) for r in rs],
        "searches": [int(r["n"])  for r in rs],
    }


def get_search_types(conn, days):
    """
    Object type distribution of search result clicks (table, article, term, etc.).
    Falls back gracefully if otype column doesn't exist in this Alation version.
    """
    period = f"{days} days"
    try:
        rs = rows(conn, """
            SELECT COALESCE(otype, 'unknown') AS otype,
                   COUNT(*)                   AS cnt
            FROM   public.search_clicks
            WHERE  ts_created >= NOW() - INTERVAL %s
            GROUP BY 1 ORDER BY 2 DESC
        """, (period,))
        total = sum(int(r["cnt"]) for r in rs) or 1
        return {r["otype"]: round(int(r["cnt"]) * 100 / total, 1) for r in rs}
    except Exception:
        return {}


def get_top_searches(conn, days, limit=15):
    """Most-searched terms/queries."""
    period = f"{days} days"
    rs = rows(conn, """
        SELECT name    AS query_text,
               COUNT(*) AS cnt
        FROM   public.search_queries
        WHERE  ts_created >= NOW() - INTERVAL %s
          AND  name IS NOT NULL AND name <> ''
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT %s
    """, (period, limit))
    return [{"query": r["query_text"], "count": int(r["cnt"])} for r in rs]


def get_top_visited(conn, days, limit=15):
    """Most-viewed catalog objects, with names resolved via outer joins."""
    period = f"{days} days"
    rs = rows(conn, """
        SELECT v.object_id,
               COALESCE(rt.name, art.title, q.title, t.title, 'Unknown') AS name,
               CASE
                   WHEN rt.id   IS NOT NULL THEN 'table'
                   WHEN art.id  IS NOT NULL THEN 'article'
                   WHEN q.id    IS NOT NULL THEN 'query'
                   WHEN t.id    IS NOT NULL THEN 'term'
                   ELSE 'other'
               END AS type,
               COUNT(*) AS views
        FROM   public.visits v
        LEFT JOIN public.rdbms_tables rt  ON rt.id  = v.object_id AND rt.ts_deleted  IS NULL
        LEFT JOIN public.article      art ON art.id = v.object_id AND art.ts_deleted IS NULL
        LEFT JOIN public.query        q   ON q.id   = v.object_id AND q.ts_deleted   IS NULL
        LEFT JOIN public.terms        t   ON t.id   = v.object_id AND t.ts_deleted   IS NULL
        WHERE  v.ts_created >= NOW() - INTERVAL %s
          AND  v.object_id  IS NOT NULL
        GROUP BY 1, 2, 3
        ORDER BY 4 DESC
        LIMIT %s
    """, (period, limit))
    return [{"name": r["name"], "type": r["type"], "views": int(r["views"])} for r in rs]


def get_governance_feed(conn, limit=12):
    """Recent curation events for the governance activity feed."""
    rs = rows(conn, """
        SELECT f.flag_type,
               u.display_name,
               COALESCE(rt.name, 'Unknown object') AS object_name,
               COALESCE(ds.name, '')               AS datasource,
               f.ts_created
        FROM   public.flags f
        JOIN   public.users u ON u.id = f.user_id
        LEFT JOIN public.rdbms_tables rt ON rt.id = f.object_id
        LEFT JOIN public.rdbms_datasources ds ON ds.id = rt.ds_id
        WHERE  f.ts_deleted IS NULL
        ORDER BY f.ts_created DESC
        LIMIT %s
    """, (limit,))
    return [
        {
            "type":       r["flag_type"],
            "user":       r["display_name"] or "Unknown",
            "object":     r["object_name"],
            "datasource": r["datasource"],
            "date":       r["ts_created"].strftime("%Y-%m-%d") if r["ts_created"] else "",
        }
        for r in rs
    ]


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    log.info(f"Connecting to Alation Analytics at {DB['host']}:{DB['port']} / {DB['dbname']} …")
    conn = connect()
    log.info(f"Connected. Exporting metrics for last {PERIOD_DAYS} days …")

    data = {
        "meta": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "period_days":  PERIOD_DAYS,
            "source":       f"{DB['host']}:{DB['port']}/{DB['dbname']}",
        }
    }

    steps = [
        ("summary",          lambda: get_summary(conn, PERIOD_DAYS)),
        ("trend_90d",        lambda: get_trend(conn, PERIOD_DAYS)),
        ("dau_mau_12m",      lambda: get_dau_mau_12m(conn)),
        ("top_users",        lambda: get_top_users(conn, PERIOD_DAYS)),
        ("curation_monthly", lambda: get_curation_monthly(conn)),
        ("catalog_coverage", lambda: get_catalog_coverage(conn)),
        ("top_curators",     lambda: get_top_curators(conn, PERIOD_DAYS)),
        ("amp_terms",        lambda: get_amp_terms(conn)),
        ("search_daily",     lambda: get_search_daily(conn, PERIOD_DAYS)),
        ("search_types",     lambda: get_search_types(conn, PERIOD_DAYS)),
        ("top_searches",     lambda: get_top_searches(conn, PERIOD_DAYS)),
        ("top_visited",      lambda: get_top_visited(conn, PERIOD_DAYS)),
        ("governance_feed",  lambda: get_governance_feed(conn)),
    ]

    for key, fn in steps:
        data[key] = safe(key, fn)

    conn.close()

    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2, default=str)

    log.info(f"✓ data.json written to {OUTPUT_PATH}")
    log.info(f"  MAU: {(data.get('summary') or {}).get('mau', '?')}  |  "
             f"Searches: {(data.get('summary') or {}).get('searches_total', '?')}  |  "
             f"Endorsed: {(data.get('summary') or {}).get('endorsed_pct', '?')}%")


if __name__ == "__main__":
    main()
