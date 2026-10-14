#!/usr/bin/env python3
"""Create/populate Google Sheet template for Data626/MCI vs OMS Gen AI metadata evaluation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SHEET_TITLE = "Gen AI Metadata Evaluation — Data626 vs OMS"
MCP_DIR = Path.home() / "Library/Application Support/All Google MCP"

REQUIRED_FIELDS = [
    "Description",
    "Background Context",
    "Business Use Cases",
    "Data Domain",
    "Business Segments",
    "Business Sensitivity",
    "Child Data",
    "Data Classification",
    "Data Sensitivity",
    "Is Aggregated",
    "Is D2C Compliant",
    "Stewards",
    "Technical Data Stewards",
]

OPTIONAL_FIELDS = [
    "Business Unit Stakeholders",
    "ETL Job Info",
    "OLA",
    "External Business Partners",
    "Regions",
    "Sub Regions",
    "Insertion Date for Retention",
]

STRATA = [
    "Git-backed pipeline (dbt/Airflow/repo-defined)",
    "Warehouse-native only (view/table, thin Git trail)",
    "Cross-system journey (ingest → transform → activation)",
    "Well-documented baseline (Alation reference)",
    "Intentionally sparse / known-bad metadata",
]

SOLUTIONS = ["Data626 / MCI", "OMS Gen AI"]

TABS = [
    "Read Me",
    "Test Corpus",
    "Required Fields",
    "Scoring Rubric",
    "Blind Scores",
    "Steward Efficiency",
    "Coverage",
    "Platform Fit",
    "Summary",
    "Decision",
]


def sheets_service():
    token_path = MCP_DIR / "token.json"
    if not token_path.exists():
        raise RuntimeError(f"Google MCP token not found at {token_path}")
    creds = Credentials.from_authorized_user_file(str(token_path))
    return build("sheets", "v4", credentials=creds)


def create_spreadsheet(service) -> str:
    body = {"properties": {"title": SHEET_TITLE}}
    resp = service.spreadsheets().create(body=body).execute()
    return resp["spreadsheetId"]


def setup_tabs(service, spreadsheet_id: str) -> None:
    requests = [
        {"updateSheetProperties": {"properties": {"sheetId": 0, "title": TABS[0]}, "fields": "title"}},
    ]
    for title in TABS[1:]:
        requests.append({"addSheet": {"properties": {"title": title}}})
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body={"requests": requests}
    ).execute()


def write_tab(service, spreadsheet_id: str, tab: str, rows: list[list]) -> None:
    if not rows:
        return
    width = max(len(r) for r in rows)
    padded = [r + [""] * (width - len(r)) for r in rows]
    end_col = chr(ord("A") + width - 1) if width <= 26 else "Z"
    range_a1 = f"'{tab}'!A1:{end_col}{len(padded)}"
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_a1,
        valueInputOption="USER_ENTERED",
        body={"values": padded},
    ).execute()


def read_me_rows() -> list[list]:
    return [
        ["Gen AI Metadata Evaluation Template"],
        ["Compare Data626/MCI vs OMS Gen AI for table descriptions and governance metadata"],
        [],
        ["Purpose"],
        [
            "Structured bake-off to evaluate which solution (or combination) should generate "
            "governed metadata fields — not which team wins."
        ],
        [],
        ["Program context"],
        ["626 / MCI", "Metadata supply — Git + governance context → curated fields → publish to OMS"],
        ["OMS Gen AI", "Metadata store + serve — suggestions from OMS graph, lineage, usage"],
        ["Navigator / BDC", "Surfaces steward-approved outputs; does not generate metadata"],
        [],
        ["Phases"],
        ["1. Setup (Week 1)", "Lock corpus (Test Corpus tab), assign blind labels, confirm field list"],
        ["2. Generate (Weeks 2-3)", "Both solutions run on same assets; paste blind codes in Blind Scores"],
        ["3. Score (Weeks 3-4)", "Stewards score blind (do not reveal solution until scoring complete)"],
        ["4. Decide (Weeks 5-6)", "Review Summary + Decision tabs; metadata working group readout"],
        [],
        ["Scoring weights (default)"],
        ["Dimension", "Weight"],
        ["Accuracy & trust", "40%"],
        ["Steward efficiency", "25%"],
        ["Coverage & completeness", "20%"],
        ["Consumer usefulness", "10%"],
        ["Explainability", "5%"],
        [],
        ["Success thresholds (suggested)"],
        ["Metric", "Target"],
        ["Required field coverage", ">= 95%"],
        ["Steward accept without major rewrite", ">= 70% of fields"],
        ["Material hallucination rate (red-team set)", "< 5%"],
        ["Median steward time per asset (full required set)", "<= 10 min"],
        ["Cross-system narrative accuracy", ">= 80% steward agreement"],
        [],
        ["How to use each tab"],
        ["Test Corpus", "Register 40-60 assets across strata; assign Asset IDs"],
        ["Required Fields", "Governance field checklist from DGSMM / Metadata Curation Automation memo"],
        ["Scoring Rubric", "Reference 1-3-5 scales for blind scoring"],
        ["Blind Scores", "One row per asset × field × blind solution; score 1-5 per criterion"],
        ["Steward Efficiency", "Time, edit distance, investigation burden per asset"],
        ["Coverage", "Count populated required/optional fields per solution"],
        ["Platform Fit", "Operational/integration criteria scored 1-5"],
        ["Summary", "Formulas roll up scores by solution (reveal after blind phase)"],
        ["Decision", "Record primary/supplement/split-by-asset-type outcome"],
        [],
        ["Owners"],
        ["DGSMM / stewards", "Rubric, blind scoring, workflow"],
        ["626/MCI team", "Corpus run, confidence scores, publish API"],
        ["OMS team", "Gen AI run, write path, context disclosure"],
        ["Metadata working group", "Adjudicate overlap and precedence"],
    ]


def test_corpus_rows() -> list[list]:
    header = [
        "Asset ID",
        "Asset Name",
        "Fully Qualified Name",
        "Platform",
        "Stratum",
        "Domain / Pilot",
        "Has Git Repo?",
        "Repo URL (if any)",
        "Alation Doc Quality",
        "Red Team?",
        "Notes",
        "Include in POC?",
    ]
    rows = [header]
    samples = [
        ("A001", "Example dbt mart", "DSS.PROD.FCT_SUBSCRIBER", "Snowflake", STRATA[0], "Playback", "Y", "", "Low", "N", "Replace with real asset", "Y"),
        ("A002", "Example view", "DSS.PROD.VW_REVENUE", "Snowflake", STRATA[1], "DNA", "N", "", "Medium", "N", "", "Y"),
        ("A003", "Cross-system table", "DSS.PROD.ACTIVATION_OUT", "Snowflake", STRATA[2], "MCI", "Y", "", "Low", "Y", "Test pipeline narrative", "Y"),
        ("A004", "Baseline table", "DSS.PROD.DIM_PRODUCT", "Snowflake", STRATA[3], "Enterprise", "Y", "", "High", "N", "Regression check", "Y"),
        ("A005", "Sparse metadata", "DSS.PROD.RAW_EVENTS", "Snowflake", STRATA[4], "Playback", "Y", "", "None", "Y", "", "Y"),
    ]
    for s in samples:
        rows.append(list(s))
    for i in range(6, 41):
        rows.append([f"A{i:03d}", "", "", "Snowflake", "", "", "", "", "", "N", "", ""])
    return rows


def required_fields_rows() -> list[list]:
    rows = [
        ["Field Name", "Tier", "Confidence Required?", "626 Expected?", "OMS Expected?", "Steward Checkpoint?", "Notes"],
    ]
    for f in REQUIRED_FIELDS:
        conf = "Y" if f not in ("Stewards", "Technical Data Stewards") else "Exception"
        rows.append([f, "Required", conf, "Y", "Y", "Y", ""])
    for f in OPTIONAL_FIELDS:
        rows.append([f, "Optional", "N", "If context exists", "If context exists", "N", ""])
    return rows


def scoring_rubric_rows() -> list[list]:
    return [
        ["Criterion", "Weight group", "Score 1 (Fail)", "Score 3 (Acceptable)", "Score 5 (Excellent)"],
        [
            "Factual correctness",
            "Accuracy & trust (40%)",
            "Contradicts schema, lineage, or glossary",
            "Mostly correct; minor gaps",
            "Accurate; aligns with code/lineage/glossary",
        ],
        [
            "Cross-system fidelity",
            "Accuracy & trust",
            "Warehouse-only; misses upstream logic",
            "Partial pipeline context",
            "Correctly explains production/transformation path",
        ],
        [
            "Glossary alignment",
            "Accuracy & trust",
            "Invents terms or conflicts with glossary",
            "Mostly aligned",
            "Uses authoritative enterprise terms",
        ],
        [
            "Hallucination rate",
            "Accuracy & trust",
            "Invented owners, policies, or use cases",
            "Rare, catchable errors",
            "No material fabrications",
        ],
        [
            "Confidence calibration",
            "Accuracy & trust",
            "High confidence on wrong answers",
            "Mixed",
            "Low confidence when uncertain; flags gaps",
        ],
        [
            "Time to approve (minutes)",
            "Steward efficiency (25%)",
            "> 20 min per field set",
            "10-20 min",
            "<= 10 min",
        ],
        [
            "Edit distance (% text kept)",
            "Steward efficiency",
            "< 30% kept",
            "30-70% kept",
            "> 70% kept without rewrite",
        ],
        [
            "Investigation burden",
            "Steward efficiency",
            "Must leave tool (Git, Slack, warehouse)",
            "Some external validation",
            "Validates entirely in scoring UI",
        ],
        [
            "Required field coverage (%)",
            "Coverage (20%)",
            "< 60%",
            "60-94%",
            ">= 95%",
        ],
        [
            "Confidence threshold met (%)",
            "Coverage",
            "< 70%",
            "70-99%",
            "100% on required (626 target)",
        ],
        [
            "Consumer can use dataset?",
            "Consumer usefulness (10%)",
            "No — still ambiguous",
            "Partial — needs follow-up",
            "Yes — clear meaning, owner, restrictions",
        ],
        [
            "Explainability",
            "Explainability (5%)",
            "No rationale shown",
            "Partial (rule name or generic)",
            "Shows code snippet, lineage path, glossary link",
        ],
        [],
        ["Red-team cases (must pass)"],
        ["Case", "What to test"],
        ["Compliance-filtered fields", "Is Aggregated, D2C, classification under-filter scenarios"],
        ["Derived metrics", "Multiple valid definitions — does output acknowledge nuance?"],
        ["Similar names", "Tables with similar names but different semantics"],
        ["Missing Git trail", "Warehouse-native assets — compare 626 vs OMS fairly"],
    ]


def blind_scores_rows() -> list[list]:
    header = [
        "Score Row ID",
        "Asset ID",
        "Field Name",
        "Blind Code (A/B)",
        "Actual Solution (reveal after scoring)",
        "Factual correctness (1-5)",
        "Cross-system fidelity (1-5)",
        "Glossary alignment (1-5)",
        "Hallucination (1-5, 5=none)",
        "Confidence calibration (1-5)",
        "Explainability (1-5)",
        "Reviewer",
        "Notes",
    ]
    rows = [header]
    for i in range(1, 101):
        rows.append(
            [
                f"S{i:03d}",
                "",
                "",
                "A" if i % 2 else "B",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ]
        )
    return rows


def steward_efficiency_rows() -> list[list]:
    header = [
        "Asset ID",
        "Blind Code (A/B)",
        "Actual Solution (reveal after)",
        "Minutes to review all required fields",
        "Fields accepted as-is (#)",
        "Fields lightly edited (#)",
        "Fields rejected/rewritten (#)",
        "Left tool to investigate? (Y/N)",
        "Reviewer",
        "Notes",
    ]
    rows = [header]
    for i in range(1, 41):
        rows.append([f"A{i:03d}", "A" if i % 2 else "B", "", "", "", "", "", "", "", ""])
    return rows


def coverage_rows() -> list[list]:
    header = [
        "Asset ID",
        "Solution",
        "Required fields populated (#/13)",
        "Required coverage (%)",
        "Optional fields populated (#/7)",
        "Meets 95% target? (Y/N)",
        "Meets 100% confidence on required? (Y/N)",
        "Notes",
    ]
    rows = [header]
    for aid in [f"A{i:03d}" for i in range(1, 21)]:
        for sol in SOLUTIONS:
            rows.append([aid, sol, "", "", "", "", "", ""])
    return rows


def platform_fit_rows() -> list[list]:
    criteria = [
        ("Context sources", "What feeds the model? (Git, lineage, query logs, glossary)"),
        ("Freshness / re-generation", "Event-driven on schema/code change?"),
        ("Write path to OMS", "API, field mapping, idempotency, versioning"),
        ("Steward workflow", "Inbox, accept/dismiss, bulk approve, audit trail"),
        ("Governance & safety", "PII in prompts, model hosting, retention"),
        ("Scale economics", "Cost per 1,000 assets at steady state"),
        ("Overlap / duplication risk", "Competing writes to same fields?"),
        ("Explainability to stewards", "Why was this value suggested?"),
    ]
    rows = [
        ["Criterion", "Question", "Data626 / MCI (1-5)", "OMS Gen AI (1-5)", "Notes", "Evidence / link"],
    ]
    for c, q in criteria:
        rows.append([c, q, "", "", "", ""])
    return rows


def summary_rows() -> list[list]:
    return [
        ["Summary — reveal solutions after blind scoring complete"],
        [],
        ["Dimension", "Weight", "Data626 / MCI avg", "OMS Gen AI avg", "Winner"],
        ["Accuracy & trust", "40%", "", "", ""],
        ["Steward efficiency", "25%", "", "", ""],
        ["Coverage & completeness", "20%", "", "", ""],
        ["Consumer usefulness", "10%", "", "", ""],
        ["Explainability", "5%", "", "", ""],
        ["TOTAL (weighted)", "100%", "", "", ""],
        [],
        ["Coverage roll-up"],
        ["Solution", "Assets evaluated", "Avg required field coverage %", "Assets meeting 95% target", "Red-team pass rate"],
        ["Data626 / MCI", "", "", "", ""],
        ["OMS Gen AI", "", "", "", ""],
        [],
        ["Steward efficiency roll-up"],
        ["Solution", "Median minutes per asset", "Avg % text kept", "Investigation rate (%)"],
        ["Data626 / MCI", "", "", ""],
        ["OMS Gen AI", "", "", ""],
        [],
        ["Instructions"],
        ["1", "After blind scoring, map Blind Code A/B to actual solution in Blind Scores tab"],
        ["2", "Enter averages from Blind Scores / Coverage / Steward Efficiency tabs"],
        ["3", "Use Decision tab to record outcome pattern and field-level precedence"],
    ]


def decision_rows() -> list[list]:
    patterns = [
        "626 primary, OMS assist",
        "OMS primary, 626 for lineage-heavy gaps",
        "Split by asset type",
        "Layered (different fields per solution)",
        "Need more data / extend POC",
    ]
    when = [
        "626 wins accuracy/cross-system; OMS adds inline UX",
        "OMS wins warehouse-native; 626 fills pipeline why",
        "Clear stratification in bake-off results",
        "626: description+lineage; OMS: tag/steward suggestions",
        "Results inconclusive or corpus too small",
    ]
    rows = [
        ["Decision matrix"],
        [],
        ["Pattern", "When to choose", "Selected? (Y/N)", "Rationale"],
    ]
    for p, w in zip(patterns, when):
        rows.append([p, w, "", ""])
    rows.extend(
        [
            [],
            ["Field-level precedence (avoid dual-write)"],
            [
                "Field Name",
                "Primary generator",
                "Supplement",
                "Steward checkpoint required?",
                "Publish target (OMS field)",
                "Notes",
            ],
        ]
    )
    for f in REQUIRED_FIELDS:
        rows.append([f, "", "", "Y", "", ""])
    rows.extend(
        [
            [],
            ["Asset-class routing"],
            ["Stratum", "Primary generator", "Notes"],
        ]
    )
    for s in STRATA:
        rows.append([s, "", ""])
    rows.extend(
        [
            [],
            ["Decision owners & date"],
            ["Decision owner", ""],
            ["Metadata working group date", ""],
            ["Follow-up actions", ""],
        ]
    )
    return rows


def populate(service, spreadsheet_id: str) -> None:
    tab_data = {
        "Read Me": read_me_rows(),
        "Test Corpus": test_corpus_rows(),
        "Required Fields": required_fields_rows(),
        "Scoring Rubric": scoring_rubric_rows(),
        "Blind Scores": blind_scores_rows(),
        "Steward Efficiency": steward_efficiency_rows(),
        "Coverage": coverage_rows(),
        "Platform Fit": platform_fit_rows(),
        "Summary": summary_rows(),
        "Decision": decision_rows(),
    }
    for tab, rows in tab_data.items():
        write_tab(service, spreadsheet_id, tab, rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--spreadsheet-id",
        help="Existing spreadsheet ID to populate (omit to create new)",
    )
    args = parser.parse_args()

    service = sheets_service()
    sheet_id = args.spreadsheet_id or create_spreadsheet(service)
    if not args.spreadsheet_id:
        setup_tabs(service, sheet_id)
    else:
        setup_tabs(service, sheet_id)
    populate(service, sheet_id)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    print(json.dumps({"id": sheet_id, "url": url, "title": SHEET_TITLE}, indent=2))


if __name__ == "__main__":
    main()
