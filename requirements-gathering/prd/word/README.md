# Feature PRDs (Word)

This folder contains **35 Microsoft Word** (`.docx`) product requirement documents—**one per row** in the DEEPT **Feature Inventory Matrix** Google Doc (features 1–35).

## Navigator product PRDs

| File | Description |
|------|-------------|
| `PRD-Navigator-Data-Governance-Portal.docx` | **Data Governance Portal** — posture, queues, evidence, four dimensions (Privacy / Platform / Security / Regulatory) |
| `PRD-Navigator-Data-Governance-Umbrella.docx` | **Navigator product family** — umbrella story (Portal, BDC, PULS, Kronos) |

Regenerate:

```bash
python3 build_navigator_data_governance_portal_prd.py
python3 build_navigator_umbrella_prd.py
```

## Files

| Pattern | Meaning |
|--------|---------|
| `PRD-F01-….docx` … `PRD-F35-….docx` | One PRD per matrix feature # |

Each document includes: summary, problem/outcomes, scope, persona table, **component-by-component** breakdown, user stories, use cases, UI notes, data/API, NFRs, sample acceptance criteria, dependencies, open questions, and references.

## Regenerate

From this directory:

```bash
python3 build_word_prds.py
```

Requires **python-docx** (`pip install python-docx`).

## Linking from the Google matrix (“PRD page link” column)

The All Google MCP cannot upload arbitrary `.docx` binaries to Drive from this agent, so **you attach the links** after upload:

1. Upload the whole `word/` folder (or its `.docx` files) to **Google Drive** (shared drive or My Drive).
2. For each file `PRD-Fnn-….docx`, use **Share → Anyone with the link (Viewer)** or keep **restricted** to DEEPT as policy requires.
3. Open your **Feature Inventory Matrix** Google Doc.
4. In the **PRD page link** column for row *n*, insert a **hyperlink** to the matching Drive file (right-click → Link → paste URL).

Use **`PRD-LINKS-TEMPLATE.csv`** in this folder as a checklist: it lists every feature #, name, and filename so you can paste the Drive URL in the last column, then work down the matrix rows.

## Source of truth

- Matrix text and priorities: [Feature Inventory Matrix](https://docs.google.com/document/d/1747SyGfelCmz-T8frBXup-UDCZ1HYi7kwONwXXsrjxg/edit) (Google Doc).
- PRD body text is generated from that matrix plus program-wide defaults (OMS/BDC, DEEPT); edit the `.docx` or adjust `build_word_prds.py` and re-run.
