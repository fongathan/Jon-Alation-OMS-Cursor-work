#!/usr/bin/env python3
"""Add EVP/SVP org rollup column to Alation catalog activity CSV via Workforce."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE = Path(__file__).resolve().parent
CSV_PATH = BASE / "Users with catalog activity (visits) in the past 6 months.csv"
CACHE_PATH = BASE / "Users with catalog activity (visits) in the past 6 months.workforce_cache.json"
ROLLUP_COLUMN = "evp_svp_org_leader"
WORKERS = 8

TONY_ID = "dbc99bfe-b28e-490f-9106-d740b58fcfdd"
CACHE_LOCK = threading.Lock()


def wf(cmd: list[str]) -> dict:
    result = subprocess.run(
        ["workforce", "--agent", *cmd],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "workforce failed")
    payload = json.loads(result.stdout)
    if payload.get("status") != "success":
        raise RuntimeError(json.dumps(payload)[:500])
    return payload["data"]


def load_cache() -> dict:
    if CACHE_PATH.exists():
        with CACHE_PATH.open(encoding="utf-8") as fh:
            cache = json.load(fh)
    else:
        cache = {}
    for key in ("email_to_uuid", "person", "rollup", "search"):
        cache.setdefault(key, {})
    return cache


def save_cache(cache: dict) -> None:
    with CACHE_PATH.open("w", encoding="utf-8") as fh:
        json.dump(cache, fh, indent=2, sort_keys=False)


def title_of(person: dict) -> str:
    return (person.get("positionTitle") or person.get("title") or "").strip()


def person_name(person: dict) -> str:
    return (person.get("fullName") or person.get("displayName") or "").strip()


def is_evpsvp(title: str) -> bool:
    upper = title.upper()
    return "EVP" in upper or upper.startswith("SVP") or " SVP" in upper


def format_leader_label(person: dict) -> str:
    title = title_of(person)
    name = person_name(person).split("(")[0].strip()
    level = "EVP" if "EVP" in title.upper() else "SVP"
    return f"{level} {name}"


def get_person(uuid: str, cache: dict) -> dict:
    with CACHE_LOCK:
        cached = cache["person"].get(uuid)
        if cached and cached.get("leaderId") is not None:
            return cached
    person = wf(["person", "get", "--uuid", uuid])
    with CACHE_LOCK:
        cache["person"][uuid] = person
    return person


def resolve_uuid(email: str, display_name: str, cache: dict) -> str | None:
    key = email.strip().lower()
    search_key = f"{email}|{display_name}"
    with CACHE_LOCK:
        if key in cache["email_to_uuid"]:
            return cache["email_to_uuid"][key]
        if search_key in cache["search"]:
            uuid = cache["search"][search_key]
            cache["email_to_uuid"][key] = uuid
            return uuid

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
        email_lower = key
        exact = [p for p in candidates if (p.get("email") or "").lower() == email_lower]
        if len(exact) == 1:
            uuid = exact[0]["id"]
        elif len(candidates) == 1:
            uuid = candidates[0]["id"]
        else:
            rostr = email_lower.upper()
            rostr_matches = [
                p for p in candidates if (p.get("rostrEmail") or "").upper() == rostr
            ]
            if len(rostr_matches) == 1:
                uuid = rostr_matches[0]["id"]

    with CACHE_LOCK:
        cache["search"][search_key] = uuid
        cache["email_to_uuid"][key] = uuid
    return uuid


def rollup(uuid: str | None, cache: dict) -> str:
    if not uuid:
        return "Not found in Workforce"
    with CACHE_LOCK:
        if uuid in cache["rollup"]:
            return cache["rollup"][uuid]

    seen: set[str] = set()
    current = uuid
    while current and current not in seen:
        seen.add(current)
        person = get_person(current, cache)
        pid = person.get("id") or current
        pname = person_name(person)
        ptitle = title_of(person)

        if pid == TONY_ID or pname == "Tony Donohoe":
            label = "EVP Tony Donohoe"
            with CACHE_LOCK:
                cache["rollup"][pid] = label
                cache["rollup"][uuid] = label
            return label

        if is_evpsvp(ptitle):
            label = format_leader_label(person)
            with CACHE_LOCK:
                cache["rollup"][pid] = label
                cache["rollup"][uuid] = label
            return label

        leader_id = person.get("leaderId")
        if not leader_id:
            label = f"Unknown leader — {pname or pid}"
            with CACHE_LOCK:
                cache["rollup"][pid] = label
                cache["rollup"][uuid] = label
            return label
        current = leader_id

    label = "Unknown (cycle in org chain)"
    with CACHE_LOCK:
        cache["rollup"][uuid] = label
    return label


def enrich_row(row: dict, cache: dict) -> str:
    email = (row.get("user_email") or "").strip()
    display_name = (row.get("display_name") or "").strip()
    uuid = resolve_uuid(email, display_name, cache)
    return rollup(uuid, cache)


def main() -> int:
    cache = load_cache()

    with CSV_PATH.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if ROLLUP_COLUMN not in fieldnames:
        fieldnames.append(ROLLUP_COLUMN)

    total = len(rows)
    done = 0

    # Pre-resolve emails already in cache sequentially (fast, no API).
    pending: list[dict] = []
    for row in rows:
        email = (row.get("user_email") or "").strip().lower()
        if email in cache["email_to_uuid"]:
            uuid = cache["email_to_uuid"][email]
            row[ROLLUP_COLUMN] = rollup(uuid, cache)
            done += 1
        else:
            pending.append(row)

    print(f"Cache hits: {done}/{total}; remaining lookups: {len(pending)}", flush=True)

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(enrich_row, row, cache): row for row in pending}
        for future in as_completed(futures):
            row = futures[future]
            try:
                row[ROLLUP_COLUMN] = future.result()
            except Exception as exc:  # noqa: BLE001
                row[ROLLUP_COLUMN] = f"Lookup error: {exc.__class__.__name__}"
            done += 1
            if done % 50 == 0 or done == total:
                save_cache(cache)
                print(f"Processed {done}/{total}", flush=True)

    with CSV_PATH.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    save_cache(cache)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row.get(ROLLUP_COLUMN, "")] = counts.get(row.get(ROLLUP_COLUMN, ""), 0) + 1

    print(f"Wrote {CSV_PATH.name} with column {ROLLUP_COLUMN} (column N)")
    print("Top rollup labels:")
    for label, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:20]:
        print(f"  {count:4d}  {label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
