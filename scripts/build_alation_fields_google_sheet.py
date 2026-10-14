#!/usr/bin/env python3
"""Build row data for Disney Alation field inventory Google Sheet."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "business-data-catalog" / "oms-ui-on-top.html"
OUT_JSON = ROOT / "business-data-catalog" / "alation-fields-sheet-data.json"

HEADERS = [
    "Category",
    "Field group",
    "Field name",
    "Alation type",
    "Applies to (object types)",
    "Required for governed upload",
    "Description",
    "Format / example",
    "Dictionary upload header",
    "Notes",
]

DATASOURCE_16 = {
    "id": 16,
    "name": "Snowflake - DSS (inferred from workspace examples)",
    "url": "https://disney-data.alationcloud.com/app/data/16/overview",
}


def parse_dictionary_fields() -> list[list[str]]:
    text = HTML.read_text(encoding="utf-8")
    start = text.index('<table class="oms-table catalog-dd-fields">')
    end = text.index("</table>", start)
    chunk = text[start:end]
    rows: list[list[str]] = []
    for tr in re.findall(r"<tr>(.*?)</tr>", chunk, re.S)[1:]:
        cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(cells) != 5:
            continue
        component, header, scope, desc, fmt = [
            re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip() for c in cells
        ]
        if header.lower() == "key":
            continue  # upload key, not an Alation UI field
        alation_type = infer_type(header, fmt)
        required = (
            "Yes"
            if component.lower().startswith("required")
            else "No"
            if component.lower() == "optional"
            else "Privacy / compliance"
        )
        rows.append(
            [
                "Custom field (Disney data dictionary)",
                component,
                header.replace(":groupprofile", " (group)").replace(":user", " (user)"),
                alation_type,
                scope_to_otypes(scope),
                required,
                desc,
                fmt,
                header,
                "From DDQGC Data Dictionary Update Procedure (Confluence 901009939)",
            ]
        )
    return rows


def scope_to_otypes(scope: str) -> str:
    s = scope.lower()
    if s == "both":
        return "table, attribute (column)"
    if s == "table":
        return "table"
    if s == "column":
        return "attribute (column)"
    return scope


def infer_type(header: str, fmt: str) -> str:
    h = header.lower()
    f = fmt.lower()
    if ":groupprofile" in h or ":user" in h:
        return "OBJECT_SET (People set)"
    if h in {"title", "description", "background context", "business formula", "business use cases", "etl job info", "ola"}:
        return "RICH_TEXT or TEXT"
    if ";" in fmt and "yes" in f:
        return "PICKER or MULTI_PICKER"
    if fmt.strip().startswith('["'):
        return "MULTI_PICKER or OBJECT_SET"
    if h == "key":
        return "System identifier (upload key)"
    return "Custom field"


def builtin_rows() -> list[list[str]]:
    """Built-in / platform metadata fields Alation exposes beyond custom field definitions."""
    rows: list[list[str]] = []

    def add(group: str, name: str, otypes: str, desc: str, fmt: str = "", notes: str = ""):
        rows.append(
            [
                "Built-in catalog metadata",
                group,
                name,
                "Platform (not a custom field definition)",
                otypes,
                "",
                desc,
                fmt,
                "",
                notes,
            ]
        )

    ds = "data (data source)"
    for name, desc in [
        ("Title", "Display name of the data source"),
        ("URI / connection", "Connection endpoint or JDBC URI"),
        ("Database type", "Connector type (e.g. Snowflake, PostgreSQL)"),
        ("Description", "Rich-text overview of the source"),
        ("Owner", "Catalog owner for the data source"),
        ("Deployment status", "Deployed vs undeployed"),
        ("Metadata extraction status", "Last MDE / sync timestamps and status"),
        ("Compose enabled", "Whether Compose queries can run against this source"),
        ("Profiling enabled", "Whether column profiling is configured"),
        ("Schema count / object counts", "Summary counts on overview"),
    ]:
        add("Data source overview", name, ds, desc, notes=f"Visible on {DATASOURCE_16['url']}")

    schema = "schema"
    for name, desc in [
        ("Name", "Schema name in the source"),
        ("Title", "Business title"),
        ("Description", "Schema-level definition"),
        ("Steward", "Assigned stewards"),
        ("Tags", "Applied classification tags"),
        ("Domains", "Business domain membership"),
        ("Flags", "Endorse / warn / deprecate"),
        ("Table count", "Number of tables in schema"),
    ]:
        add("Schema", name, schema, desc)

    table = "table"
    for name, desc, fmt in [
        ("Name", "Physical table name", ""),
        ("Title", "Business title", ""),
        ("Description", "Table definition", ""),
        ("Type", "Table vs view", "TABLE, VIEW"),
        ("Steward", "Business / technical stewards", "People sets"),
        ("Tags", "Classification tags", "e.g. Core Table, GDPR Scoped, CCPA Scoped"),
        ("Domains", "Domain membership", ""),
        ("Flags", "Trust signals", "Endorsed, Warning, Deprecated"),
        ("Popularity", "Usage-based ranking", "Query log derived"),
        ("Synonyms", "Alternate search names", ""),
        ("Row count", "Extracted row estimate", ""),
        ("Last updated", "Last metadata change", ""),
        ("Source comments", "DBMS comments from source", ""),
        ("Lineage", "Upstream / downstream graph", "Object graph"),
        ("Queries", "Saved Compose queries referencing object", ""),
        ("Glossary links", "Linked business terms", ""),
        ("Articles", "Linked knowledge articles", ""),
        ("Policies", "Linked business policies", "If enabled"),
    ]:
        add("Table / view", name, table, desc, fmt)

    col = "attribute (column)"
    for name, desc, fmt in [
        ("Name", "Column name", ""),
        ("Title", "Business title", ""),
        ("Description", "Column definition", ""),
        ("Data type", "Physical type from source", "e.g. VARCHAR, NUMBER"),
        ("Steward", "Column stewards", ""),
        ("Tags", "Column-level tags", ""),
        ("Flags", "Trust signals", ""),
        ("Nullable", "Nullability from source", ""),
        ("Primary key", "PK indicator", ""),
        ("Foreign keys", "Relationships", ""),
        ("Sample values", "Profiling samples", "Role-gated"),
        ("Profile statistics", "Distinct count, min/max, etc.", "If profiling enabled"),
        ("Synonyms", "Alternate names", ""),
        ("Lineage", "Column-level lineage", ""),
        ("Glossary links", "Linked terms", ""),
    ]:
        add("Column", name, col, desc, fmt)

    term = "glossary_term, glossary_v3"
    for name, desc in [
        ("Term name", "Canonical business term"),
        ("Description", "Official definition"),
        ("Aliases", "Alternate names / synonyms"),
        ("Related objects", "Linked tables, columns, queries"),
        ("Template / custom fields", "Term-specific custom attributes"),
    ]:
        add("Glossary", name, term, desc, notes="Example term: Paid Subscribers")

    article = "article, custom_glossary"
    for name, desc in [
        ("Title", "Article title"),
        ("Body", "Rich HTML content"),
        ("Folder", "Knowledge base folder hierarchy"),
        ("Author / editors", "Collaboration metadata"),
        ("Linked objects", "Catalog backlinks"),
        ("Custom fields", "Article template fields"),
    ]:
        add("Article / document hub", name, article, desc)

    for name, desc, otypes in [
        ("Tags", "Free-form or controlled vocabulary labels on objects", "All catalog object types"),
        ("Domains", "Business area groupings", "table, schema, glossary, etc."),
        ("Flags — Endorse", "Curator-approved trust signal", "table, schema, attribute, ..."),
        ("Flags — Warning", "Caution signal", "table, schema, attribute, ..."),
        ("Flags — Deprecation", "Planned retirement signal", "table, schema, attribute, ..."),
        ("Conversations", "Threaded comments on objects", "Most catalog objects"),
        ("Stars / favorites", "User bookmarks", "Per-user, not metadata field"),
    ]:
        add("Platform-wide", name, otypes, desc)

    add(
        "Custom field system",
        "Custom field definitions",
        "Admin-defined in Customize Catalog",
        "field_type: TEXT, DATE, PICKER, MULTI_PICKER, RICH_TEXT, OBJECT_SET",
        "",
        "Listed on Custom Fields tab when API access available",
    )

    return rows


def overview_rows() -> list[list[str]]:
    return [
        ["Alation field inventory — Disney Data Catalog"],
        [""],
        ["Data source reference", str(DATASOURCE_16["id"]), DATASOURCE_16["name"]],
        ["Overview URL", DATASOURCE_16["url"]],
        [""],
        [
            "Generated from workspace DDQGC data dictionary field guide + Alation platform field model.",
        ],
        [
            "Live custom field IDs were not pulled: Alation API refresh token expired (2026-08-20).",
        ],
        [
            "To refresh with live API IDs: renew token in alation-mcp-server/.env and re-run export.",
        ],
        [""],
        ["Sheet columns", *HEADERS[1:]],
    ]


def main() -> None:
    all_rows = [HEADERS]
    all_rows.extend(builtin_rows())
    all_rows.extend(parse_dictionary_fields())
    payload = {
        "overview": overview_rows(),
        "all_fields": all_rows,
        "meta": {
            "datasource_id": DATASOURCE_16["id"],
            "datasource_name": DATASOURCE_16["name"],
            "field_count": len(all_rows) - 1,
        },
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_JSON} ({payload['meta']['field_count']} data rows)")


if __name__ == "__main__":
    main()
