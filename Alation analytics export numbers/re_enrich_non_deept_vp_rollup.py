#!/usr/bin/env python3
"""Re-enrich Non-DEEPT rows with VP-or-higher Workforce rollup."""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import openpyxl

BASE = Path(__file__).resolve().parent
XLSX_PATH = BASE / "Active users with catalog activity (visits) in the past 6 months.xlsx"
CSV_PATH = BASE / "Active users with catalog activity (visits) in the past 6 months.csv"
CACHE_PATH = BASE / "active_users.workforce_cache.json"
ROLLUP_COLUMN = "deept_evp_svp_rollup"
SHEET_ID = "1u2tcqSq8cuQSK_KQi356XmG3yaI1BqFLpU6FYyUCzuM"


def wf(cmd: list[str], timeout: int = 45) -> dict:
    result = subprocess.run(
        ["workforce", "--agent", *cmd],
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "workforce failed")
    payload = json.loads(result.stdout)
    if payload.get("status") != "success":
        raise RuntimeError(json.dumps(payload)[:500])
    return payload["data"]


def load_cache() -> dict:
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    for key in ("email_to_uuid", "person", "rollup_vp", "search"):
        cache.setdefault(key, {})
    return cache


def save_cache(cache: dict) -> None:
    fd, tmp = tempfile.mkstemp(suffix=".json", dir=CACHE_PATH.parent)
    try:
        with open(fd, "w", encoding="utf-8") as fh:
            json.dump(cache, fh, indent=2)
        Path(tmp).replace(CACHE_PATH)
    finally:
        if Path(tmp).exists():
            Path(tmp).unlink(missing_ok=True)


def title_of(person: dict) -> str:
    return (person.get("positionTitle") or person.get("title") or "").strip()


def person_name(person: dict) -> str:
    return (person.get("fullName") or person.get("displayName") or "").split("(")[0].strip()


def leader_level(title: str) -> str | None:
    upper = title.upper()
    if "EVP" in upper:
        return "EVP"
    if upper.startswith("SVP") or " SVP" in upper or ", SVP" in upper:
        return "SVP"
    if "VICE PRESIDENT" in upper or re.search(r"(^|[ ,/])VP[ ,/]", upper):
        return "VP"
    if "CO-PRESIDENT" in upper or "CO PRESIDENT" in upper:
        return "Co-President"
    if "PRESIDENT" in upper and "VICE PRESIDENT" not in upper and "VP" not in upper.split("PRESIDENT")[0][-3:]:
        return "President"
    if upper.startswith("HEAD OF") or " HEAD OF " in f" {upper} ":
        return "Head of"
    return None


def format_leader_label(person: dict) -> str:
    level = leader_level(title_of(person)) or "Leader"
    return f"{level} {person_name(person)}"


def get_person(uuid: str, cache: dict) -> dict:
    cached = cache["person"].get(uuid)
    if cached and cached.get("leaderId") is not None:
        return cached
    person = wf(["person", "get", "--uuid", uuid])
    cache["person"][uuid] = person
    return person


def resolve_uuid(email: str, display_name: str, cache: dict) -> str | None:
    key = email.strip().lower()
    if key in cache["email_to_uuid"]:
        return cache["email_to_uuid"][key]

    candidates: list[dict] = []
    for query in (email, display_name):
        if not query:
            continue
        data = wf(["search", "query", "--query", query])
        persons = data.get("persons") or []
        if persons:
            candidates = persons
            break

    uuid = None
    if candidates:
        exact = [p for p in candidates if (p.get("email") or "").lower() == key]
        if len(exact) == 1:
            uuid = exact[0]["id"]
        elif len(candidates) == 1:
            uuid = candidates[0]["id"]
        else:
            rostr = key.upper()
            rostr_matches = [p for p in candidates if (p.get("rostrEmail") or "").upper() == rostr]
            if len(rostr_matches) == 1:
                uuid = rostr_matches[0]["id"]

    cache["email_to_uuid"][key] = uuid
    return uuid


def rollup_vp_or_higher(uuid: str | None, cache: dict) -> str | None:
    if not uuid:
        return None
    if uuid in cache["rollup_vp"]:
        return cache["rollup_vp"][uuid]

    seen: set[str] = set()
    current = uuid
    label: str | None = None

    while current and current not in seen:
        seen.add(current)
        person = get_person(current, cache)
        if label is None and leader_level(title_of(person)):
            label = format_leader_label(person)
            break
        current = person.get("leaderId")

    cache["rollup_vp"][uuid] = label
    return label


def read_rows_from_xlsx() -> list[dict]:
    ws = openpyxl.load_workbook(XLSX_PATH).active
    headers = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
    rows = []
    for r in range(2, ws.max_row + 1):
        row = {headers[c - 1]: ws.cell(r, c).value for c in range(1, ws.max_column + 1)}
        rows.append(row)
    return rows


def write_outputs(rows: list[dict]) -> Counter:
    counts: Counter = Counter()
    email_to_rollup = {}

    for row in rows:
        email = (row.get("user_email") or "").strip()
        rollup = row.get(ROLLUP_COLUMN) or "Non-DEEPT"
        email_to_rollup[email.lower()] = rollup
        counts[rollup] += 1

    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb.active
    header_col = None
    for c in range(1, ws.max_column + 2):
        if ws.cell(1, c).value == ROLLUP_COLUMN:
            header_col = c
            break
    if header_col is None:
        header_col = ws.max_column + 1
        ws.cell(1, header_col, ROLLUP_COLUMN)
    for r in range(2, ws.max_row + 1):
        email = (ws.cell(r, 3).value or "").strip().lower()
        ws.cell(r, header_col, email_to_rollup.get(email, "Non-DEEPT"))
    wb.save(XLSX_PATH)

    with CSV_PATH.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        data = list(reader)
    if ROLLUP_COLUMN not in fieldnames:
        fieldnames.append(ROLLUP_COLUMN)
    for row in data:
        row[ROLLUP_COLUMN] = email_to_rollup.get((row.get("user_email") or "").lower(), "Non-DEEPT")
    with CSV_PATH.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)

    return counts


def build_sheet_values(counts: Counter) -> list[list]:
    major = {
        "EVP Tony Donohoe",
        "Non-DEEPT",
        "SVP Chas Murphy",
        "EVP Andre Rohe",
        "SVP Devika Chawla",
    }
    other = [(label, count) for label, count in counts.items() if label not in major]
    other.sort(key=lambda x: (-x[1], x[0]))
    other_total = sum(c for _, c in other)

    rows: list[list] = [
        ["Active Alation Users with Catalog Activity (Past 6 Months)", "", "", ""],
        ["Source: Active users export enriched with Workforce org rollup (VP or higher)", "", "", ""],
        ["Total active catalog users", sum(counts.values()), "", ""],
        ["Non-DEEPT re-enriched: VP+ rollup applied where Workforce match exists", "", "", ""],
        ["", "", "", ""],
        ["Org Leader Rollup", "Level", "Active Users", "Notes"],
    ]

    ordered_major = [
        ("EVP Tony Donohoe", "EVP", "DEEPT — Tony org"),
        ("Non-DEEPT", "Non-DEEPT", "Not found in Workforce"),
        ("SVP Chas Murphy", "SVP", ""),
        ("EVP Andre Rohe", "EVP", "Nearest rollup; 78 users roll to SVP Devika below Andre"),
        ("SVP Devika Chawla", "SVP", "Rolls up to Andre Rohe"),
    ]
    for label, level, note in ordered_major:
        if label in counts:
            rows.append([label, level, counts[label], note])

    rows.append(["", "", "", ""])
    rows.append([f"Other leaders ({other_total} users total)", "", other_total, "VP or higher nearest rollup"])
    for label, count in other:
        level = label.split(" ", 1)[0] if " " in label else ""
        rows.append([label, level, count, ""])
    return rows


def update_google_sheet(rows: list[list]) -> None:
    values_json = json.dumps(rows)
    script = f'''
import json, subprocess
payload = {{
    "spreadsheet_id": "{SHEET_ID}",
    "range_a1": "Sheet1!A1:D{len(rows)}",
    "values_json": {json.dumps(json.dumps(rows))},
}}
# use workforce-style shell via python google api not available; call MCP substitute below
'''
    # Write temp json and use subprocess curl to sheets via gdrive if needed - use openpyxl alternative: shell out to a small inline python with google auth from MCP isn't available in subprocess.
    # Instead save rows to temp file for manual MCP call from main after write.
    Path(BASE / "_sheet_update_payload.json").write_text(json.dumps(rows), encoding="utf-8")


def main() -> int:
    cache = load_cache()
    rows = read_rows_from_xlsx()
    non_deept = [r for r in rows if (r.get(ROLLUP_COLUMN) or "") == "Non-DEEPT"]
    print(f"Re-enriching {len(non_deept)} Non-DEEPT rows with VP+ rollup...", flush=True)

    updated = 0
    for idx, row in enumerate(non_deept, start=1):
        email = (row.get("user_email") or "").strip()
        display_name = (row.get("display_name") or "").strip()
        try:
            uuid = resolve_uuid(email, display_name, cache)
            label = rollup_vp_or_higher(uuid, cache)
            if label:
                row[ROLLUP_COLUMN] = label
                updated += 1
        except Exception as exc:  # noqa: BLE001
            print(f"  skip {email}: {exc}", flush=True)
        if idx % 25 == 0 or idx == len(non_deept):
            save_cache(cache)
            print(f"  processed {idx}/{len(non_deept)} ({updated} resolved)", flush=True)

    counts = write_outputs(rows)
    save_cache(cache)
    sheet_rows = build_sheet_values(counts)
    Path(BASE / "_sheet_update_payload.json").write_text(json.dumps(sheet_rows), encoding="utf-8")

    print(f"\nUpdated {updated} Non-DEEPT rows with VP+ rollup")
    print(f"Remaining Non-DEEPT: {counts.get('Non-DEEPT', 0)}")
    print("\nTop counts:")
    for label, count in counts.most_common(15):
        print(f"  {count:4d}  {label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
