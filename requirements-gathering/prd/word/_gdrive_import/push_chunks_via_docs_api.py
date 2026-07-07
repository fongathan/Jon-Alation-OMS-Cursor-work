#!/usr/bin/env python3
"""Insert PRD chunks into Google Docs using token from All Google MCP (requires docs scope)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = Path.home() / "Library/Application Support/All Google MCP/token.json"
SCOPES = ["https://www.googleapis.com/auth/documents"]

INSERT_OPS = Path(__file__).resolve().parent / "insert_ops"


def main() -> None:
    if not TOKEN_PATH.exists():
        print("Missing token:", TOKEN_PATH, file=sys.stderr)
        sys.exit(1)
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds.valid and creds.refresh_token:
        from google.auth.transport.requests import Request

        creds.refresh(Request())
    svc = build("docs", "v1", credentials=creds, cache_discovery=False)

    for path in sorted(INSERT_OPS.glob("[0-9][0-9][0-9].json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        doc_id = payload["document_id"]
        text = payload["text"]
        body = {"requests": [{"insertText": {"location": {"index": 1}, "text": text}}]}
        svc.documents().batchUpdate(documentId=doc_id, body=body).execute()
        print(path.name, doc_id, "inserted", len(text), "chars")
    print("Done:", len(list(INSERT_OPS.glob('[0-9][0-9][0-9].json'))), "inserts")


if __name__ == "__main__":
    main()
