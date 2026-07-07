#!/usr/bin/env python3
"""
Build index-sample.html with sample data from kronos_data.json.
Run: python3 build_sample_html.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
INDEX = ROOT / "index.html"
SAMPLE_JSON = ROOT / "kronos_data.json"
OUT = ROOT / "index-sample.html"


def main():
    with open(INDEX) as f:
        html = f.read()
    with open(SAMPLE_JSON) as f:
        data = json.load(f)
    new_data = "const DATA = " + json.dumps(data, indent=2) + ";"
    start = html.find("const DATA = {")
    if start == -1:
        print("Could not find DATA in index.html")
        return
    end_marker = "// APP LOGIC"
    end = html.find(end_marker, start)
    if end == -1:
        end = html.find("// APP LOGIC", start)
    if end != -1:
        end = html.rfind("};", start, end) + 2
    else:
        depth, i = 0, start + len("const DATA = ")
        while i < len(html):
            c = html[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = i + 2
                    break
            i += 1
    out_html = html[:start] + new_data + html[end:]
    with open(OUT, "w") as f:
        f.write(out_html)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
