#!/usr/bin/env python3
"""Apply nested bullet styling to Mickey FAQ inserts."""
import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from insert_navigator_faqs_mickey import INSERTIONS

DOC_ID = "1wP_czgwUmSrE82hKoMIcQDNCpuv99hzyl8pIs-_YY7U"
TOKEN_PATH = Path.home() / "Library/Application Support/All Google MCP/token.json"

MICKEY_LINES = {b for _, bullets in INSERTIONS for b in bullets}


def main() -> None:
    data = json.loads(TOKEN_PATH.read_text())
    creds = Credentials(
        token=data.get("token"),
        refresh_token=data.get("refresh_token"),
        token_uri=data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_secret=data.get("client_secret"),
        client_id=data.get("client_id"),
        scopes=data.get("scopes"),
    )
    service = build("docs", "v1", credentials=creds, cache_discovery=False)
    doc = service.documents().get(documentId=DOC_ID).execute()

    requests = []
    for element in doc["body"]["content"]:
        if "paragraph" not in element:
            continue
        if "bullet" in element["paragraph"]:
            continue
        text = "".join(
            e.get("textRun", {}).get("content", "")
            for e in element["paragraph"].get("elements", [])
        ).strip()
        if text not in MICKEY_LINES:
            continue
        requests.append(
            {
                "createParagraphBullets": {
                    "range": {
                        "startIndex": element["startIndex"],
                        "endIndex": element["endIndex"],
                    },
                    "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                }
            }
        )
        requests.append(
            {
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": element["startIndex"],
                        "endIndex": element["endIndex"],
                    },
                    "paragraphStyle": {
                        "indentFirstLine": {"magnitude": 54, "unit": "PT"},
                        "indentStart": {"magnitude": 72, "unit": "PT"},
                    },
                    "fields": "indentFirstLine,indentStart",
                }
            }
        )

    if requests:
        service.documents().batchUpdate(
            documentId=DOC_ID, body={"requests": requests}
        ).execute()
    print(f"Styled https://docs.google.com/document/d/{DOC_ID}/edit")


if __name__ == "__main__":
    main()
