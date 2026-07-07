# Google Docs — PRD F26–F35 (from Word sources)

Created in Drive folder: [Open folder](https://drive.google.com/drive/folders/1NY805KZKDSkvwQ0XnN4z450E642nbQGy)

Each row matches your Finder `.docx` files. Content is **plain text extracted** from Word (tables become pipe-separated lines), then inserted into a native Google Doc—not a binary `.docx` upload.

| # | Word source | Google Doc |
|---|-------------|------------|
| 26 | `PRD-F26-mass-bulk-edit.docx` | [PRD-F26 Mass bulk edit](https://docs.google.com/document/d/1CarbNEtFwtYwIDfp6mSGcfCQrtyWbFIn4Qg691qA9AM/edit?usp=drivesdk) |
| 27 | `PRD-F27-mass-set-rules-catalog-sets.docx` | [PRD-F27 Mass set rules catalog sets](https://docs.google.com/document/d/1sO8MTTk9Rif7ka5VFWilXcpgE8-byQmRriUGFrsLiP0/edit?usp=drivesdk) |
| 28 | `PRD-F28-ai-chat-assistant-in-app.docx` | [PRD-F28 AI chat assistant in app](https://docs.google.com/document/d/1Jy4_tDn69WZuNbpqQuGC5uFK7mZsc4tP0c4-yIvB340/edit?usp=drivesdk) |
| 29 | `PRD-F29-data-dictionary-download-uploads.docx` | [PRD-F29 Data dictionary download uploads](https://docs.google.com/document/d/1VO9TmhZ8ZQrW2F-6D2HbLHvt5XbiHbKuc4LPZa4Qy9Q/edit?usp=drivesdk) |
| 30 | `PRD-F30-expanded-data-sources.docx` | [PRD-F30 Expanded data sources](https://docs.google.com/document/d/1xLJObGagmZt7R4VqQRb8v54MkQSkEPNqjx0irPtY77M/edit?usp=drivesdk) |
| 31 | `PRD-F31-details-icon.docx` | [PRD-F31 Details icon](https://docs.google.com/document/d/1tKFIdOrDcDWjY0XdSsK4cC_jyHwRreyJETNnTIygYGQ/edit?usp=drivesdk) |
| 32 | `PRD-F32-persona-view-filtering.docx` | [PRD-F32 Persona view filtering](https://docs.google.com/document/d/1an30CYZyOxyrdRO0-tNclknxZax8SY2jrMIgj9pnGPg/edit?usp=drivesdk) |
| 33 | `PRD-F33-product-pages.docx` | [PRD-F33 Product pages](https://docs.google.com/document/d/15J_1PM-Z-6iRvy4_2fjCActeUB1lsT0twAsUpiXzhyg/edit?usp=drivesdk) |
| 34 | `PRD-F34-ai-how-to.docx` | [PRD-F34 AI How to](https://docs.google.com/document/d/1pc9GL4eukHrb35S43fqAWinuGw6f4-Ov2IhSfFxEvJA/edit?usp=drivesdk) |
| 35 | `PRD-F35-overview-section.docx` | [PRD-F35 Overview section](https://docs.google.com/document/d/19ijwHUSc9g55Dgp_GdZn8-uGWh0Ui3RuY3rp80rczKI/edit?usp=drivesdk) |

## Regenerate body from Word

```bash
cd requirements-gathering/prd/word
python3 build_word_prds.py   # refresh .docx if needed
python3 _gdrive_import/push_chunks_via_docs_api.py   # after rebuilding insert_ops/*.json
```

The push script uses `~/Library/Application Support/All Google MCP/token.json` (same OAuth as All Google MCP).
