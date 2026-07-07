"""
Load Kronos inventory data from Disney Streaming Excel files.
Outputs JSON suitable for embedding in index.html or for the Apps Script integration.

Usage:
  python load_from_excel.py                    # writes data/kronos_from_excel.json
  python load_from_excel.py --embed            # prints JS to replace DATA in index.html
"""

import json
import re
import sys
from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).parent / "data"
TRACKERS_FILE = DATA_DIR / "Disney Streaming - Digital Tracker Inventory 2024-07-12.xlsx"
SYSTEMS_FILE = DATA_DIR / "Disney Streaming - Systems Inventory 2024-07-12.xlsx"
USE_CASES_FILE = DATA_DIR / "Disney Streaming - Business Use Case Inventory 2024-07-12.xlsx"


def _str(v):
    if pd.isna(v) or v is None:
        return None
    s = str(v).strip()
    return s if s else None


def _slug(name):
    if not name:
        return "unknown"
    return re.sub(r"[^a-z0-9]+", "-", str(name).lower())[:20]


def load_trackers():
    df = pd.read_excel(TRACKERS_FILE, sheet_name="Digital Tracker Inventory", header=None)
    headers = df.iloc[4].astype(str).tolist()
    col = {h: i for i, h in enumerate(headers) if _str(h) and h != "nan"}

    trackers = []
    vendor_set = set()
    for i in range(6, len(df)):  # skip title, headers, helper row
        row = df.iloc[i]
        num = _str(row.get(col.get("#", 3)))
        if not num or num == "-" or num.lower() == "example":
            continue
        vendor = _str(row.get(col.get("Vendor", 4)))
        name = _str(row.get(col.get("Tracker Name", 5)))
        if not name and not vendor:
            continue
        uid = _str(row.get(col.get("Unique Identifier", 6)))
        owner = _str(row.get(col.get("Tracker Owner / Contact", 7)))
        desc = _str(row.get(col.get("Description", 9)))
        first_third = _str(row.get(col.get("First vs Third Party Tracker", 10)))
        tracker_type = _str(row.get(col.get("Tracker Type", 11)))
        purpose = _str(row.get(col.get("Purpose Categorization", 16))) or _str(row.get(col.get("Purpose Description Detail", 17)))
        pii = _str(row.get(col.get("PI or PII Processing", 18)))
        in_scope_brands = _str(row.get(col.get("In-Scope Brand(s)", 12)))
        in_scope_platforms = _str(row.get(col.get("In-Scope Platform(s)", 14)))

        if vendor:
            vendor_set.add(vendor)
        asset_id = f"TRK-{uid[:8]}" if uid else f"TRK-{i:04d}"
        asset_id = re.sub(r"[^A-Za-z0-9\-]", "-", asset_id)[:32]

        trackers.append({
            "asset_id": asset_id,
            "name": name or f"{vendor} Tracker" if vendor else f"Tracker {i}",
            "tracker_type": tracker_type,
            "purpose": purpose,
            "domain_or_platform": in_scope_platforms,
            "data_collected": None,
            "placement": "app" if "mobile" in str(in_scope_platforms or "").lower() or "sdk" in str(tracker_type or "").lower() else "website",
            "consent_required": "Y" in str(pii or "").upper() or "Yes" in str(pii or ""),
            "owner": owner,
            "vendor_id": f"VND-{_slug(vendor)}" if vendor else None,
            "region": "Global",
            "status": "active",
            "description": desc,
        })
    return trackers, vendor_set


def load_vendors(tracker_vendor_set):
    df = pd.read_excel(TRACKERS_FILE, sheet_name="Vendor Classification (COPY)", header=0)
    vendors = []
    seen = set()
    for _, row in df.iterrows():
        name = _str(row.get("VendorProduct"))
        if not name or name in seen:
            continue
        seen.add(name)
        alias = _str(row.get("Alias"))
        owner = _str(row.get("TWDCOwner"))
        aid = f"VND-{_slug(name)}"
        vendors.append({
            "asset_id": aid,
            "name": name,
            "vendor_type": "SaaS",
            "vendor_category": "analytics",
            "description": None,
            "owner": owner,
            "risk_rating": "medium",
            "dpa_in_place": None,
            "contract_expiry": None,
            "region": "Global",
            "status": "active",
        })
    for v in tracker_vendor_set:
        if v not in seen:
            seen.add(v)
            vendors.append({
                "asset_id": f"VND-{_slug(v)}",
                "name": v,
                "vendor_type": "SaaS",
                "vendor_category": "analytics",
                "description": None,
                "owner": None,
                "risk_rating": "medium",
                "dpa_in_place": None,
                "contract_expiry": None,
                "region": "Global",
                "status": "active",
            })
    return vendors


def load_systems():
    df = pd.read_excel(SYSTEMS_FILE, sheet_name="System Inventory - Master", header=None)
    headers = df.iloc[3].astype(str).tolist()
    col = {h: i for i, h in enumerate(headers) if _str(h) and h != "nan"}

    systems = []
    for i in range(5, len(df)):
        row = df.iloc[i]
        num = _str(row.get(col.get("#", 0)))
        if not num or num == "-" or str(num).lower() == "example":
            continue
        name = _str(row.get(col.get("Systems", 1)))
        desc = _str(row.get(col.get("Description", 2)))
        owner = _str(row.get(col.get("System Owner", 6)))
        tech_type = _str(row.get(col.get("Technology Type ", 4)))
        data_class = _str(row.get(col.get("Global Information Security Data Classif", 8)))

        if not name:
            continue
        asset_id = f"SYS-{_slug(name)[:20]}-{i}"
        asset_id = re.sub(r"[^A-Za-z0-9\-]", "-", asset_id)[:32]

        systems.append({
            "asset_id": asset_id,
            "name": name.strip(),
            "system_type": tech_type or "application",
            "description": desc,
            "business_unit": None,
            "data_classification": data_class or "internal",
            "hosting": "cloud",
            "pii_processed": "sensitive" in str(data_class or "").lower() or "confidential" in str(data_class or "").lower(),
            "owner": owner,
            "vendor_id": None,
            "region": "Global",
            "status": "active",
        })
    return systems


def load_use_cases(trackers, tracker_by_name):
    df = pd.read_excel(USE_CASES_FILE, sheet_name="Business Use Case Inventory", header=None)
    headers = df.iloc[4].astype(str).tolist()
    col = {h: i for i, h in enumerate(headers) if _str(h) and h != "nan"}

    use_cases = []
    for i in range(6, len(df)):
        row = df.iloc[i]
        num = _str(row.get(col.get("#", 3)))
        if not num or num == "-" or str(num).lower() == "example":
            continue
        category = _str(row.get(col.get("Use Case Category", 4)))
        subcategory = _str(row.get(col.get("Use Case Sub-Category", 5)))
        objective = _str(row.get(col.get("Business Objective", 6)))
        consent = _str(row.get(col.get("Consent Capture", 13)))
        first_party = _str(row.get(col.get("First Party Trackers / SDKs", 27)))
        third_party = _str(row.get(col.get("Third Party Trackers / SDKs", 28)));
        third_party_share = _str(row.get(col.get("Third Party Data Sharing", 22)))

        if not category and not subcategory:
            continue
        name = f"{category} - {subcategory}" if category and subcategory else (category or subcategory or f"Use Case {i}")
        asset_id = f"UC-{_slug(category)[:10]}-{i}"
        asset_id = re.sub(r"[^A-Za-z0-9\-]", "-", asset_id)[:32]

        tracker_ids = []
        for raw in [first_party, third_party]:
            if not raw:
                continue
            for part in re.split(r"[,;]|\band\b", raw):
                t = part.strip()
                if not t or t.lower() in ("n/a", "none", "unsure"):
                    continue
                for trk in trackers:
                    if t.lower() in (trk["name"] or "").lower() or t.lower() in (trk.get("vendor_id") or "").lower():
                        tracker_ids.append(trk["asset_id"])
                        break
                else:
                    for trk in trackers:
                        if trk["name"] and t[:15] in (trk["name"] or ""):
                            tracker_ids.append(trk["asset_id"])
                            break
        tracker_ids = list(dict.fromkeys(tracker_ids))

        use_cases.append({
            "asset_id": asset_id,
            "name": name,
            "category": category,
            "subcategory": subcategory,
            "description": objective,
            "legal_basis": "consent" if consent and "y" in str(consent).lower() else "legitimate interest",
            "owner": None,
            "region": "Global",
            "status": "active",
            "cross_border": False,
            "vendors": [],
            "trackers": tracker_ids,
            "systems": [],
        })
    return use_cases


def main():
    print("Loading from Excel...")
    trackers, vendor_set = load_trackers()
    vendors = load_vendors(vendor_set)
    systems = load_systems()
    use_cases = load_use_cases(trackers, {})

    blob = {
        "vendors": vendors,
        "trackers": trackers,
        "systems": systems,
        "use_cases": use_cases,
        "legal_exceptions": [],  # not in Excel
        "prior_audits": [],     # not in Excel
        "change_log": [],
    }

    out_path = DATA_DIR / "kronos_from_excel.json"
    with open(out_path, "w") as f:
        json.dump(blob, f, indent=2)

    print(f"Wrote {len(vendors)} vendors, {len(trackers)} trackers, {len(systems)} systems, {len(use_cases)} use cases to {out_path}")

    if "--embed" in sys.argv:
        _embed_into_index(blob)


def _embed_into_index(blob):
    index_path = Path(__file__).parent / "index.html"
    with open(index_path, "r") as f:
        html = f.read()
    js = json.dumps(blob, indent=2)
    new_data = "const DATA = " + js + ";"
    import re
    pattern = r"const DATA = \{[^}]*(?:\{[^}]*\}[^}]*)*\};"
    # Simpler: match from "const DATA = {" to the closing "};" before "// === APP LOGIC"
    start = html.find("const DATA = {")
    if start == -1:
        print("Could not find DATA in index.html")
        return
    end_marker = "\n// =====================================================================\n// APP LOGIC"
    end = html.find(end_marker, start)
    if end == -1:
        end = html.find("// APP LOGIC", start)
    if end == -1:
        # Find matching }; - walk from start
        depth = 0
        i = start + len("const DATA = ")
        while i < len(html):
            c = html[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = i + 2  # include };
                    break
            i += 1
    else:
        end = html.rfind("};", start, end) + 2
    before = html[:start]
    after = html[end:]
    new_html = before + new_data + after
    with open(index_path, "w") as f:
        f.write(new_html)
    print(f"Embedded data into {index_path}")


if __name__ == "__main__":
    main()
