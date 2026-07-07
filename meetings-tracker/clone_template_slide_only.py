#!/usr/bin/env python3
"""
Duplicate a Google Slides deck, then delete every slide except one — no edits to
that slide (pixel-identical content, theme, shapes, table, etc.).

Uses the same OAuth token as All Google MCP:
  ~/Library/Application Support/All Google MCP/token.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = Path.home() / "Library/Application Support/All Google MCP/token.json"
SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]

DEFAULT_TEMPLATE = "19CnHhso_Ts0tVaqtrdGLrtiWlriuffpGfvidMaFa-oU"
DEFAULT_SLIDE_ID = "g3e63f450cd8_2_512"
DEFAULT_NEW_NAME = "Roadmap slide (exact copy)"
FOLDER_ID = "1m-r_p9q0AClDByNnSb7Ll7p4cFae-5P9"


def batch_update(
    slides, presentation_id: str, requests: list[dict], chunk: int = 100
) -> None:
    for i in range(0, len(requests), chunk):
        slides.presentations().batchUpdate(
            presentationId=presentation_id, body={"requests": requests[i : i + chunk]}
        ).execute()


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--name",
        default=DEFAULT_NEW_NAME,
        help="Title for the new Google Slides file",
    )
    p.add_argument(
        "--template-id",
        default=DEFAULT_TEMPLATE,
        help="Source presentation file ID",
    )
    p.add_argument(
        "--slide-id",
        default=DEFAULT_SLIDE_ID,
        help="Object ID of the slide to keep (all others are removed)",
    )
    p.add_argument(
        "--folder-id",
        default=FOLDER_ID,
        help="Drive folder to move the copy into (may fail for cross-Drive moves)",
    )
    p.add_argument(
        "--skip-move", action="store_true", help="Do not call Drive move"
    )
    args = p.parse_args()

    if not TOKEN_PATH.is_file():
        print("Missing All Google MCP token:", TOKEN_PATH, file=sys.stderr)
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())

    slides = build("slides", "v1", credentials=creds, cache_discovery=False)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    copied = (
        drive.files()
        .copy(
            fileId=args.template_id,
            body={"name": args.name},
            fields="id, webViewLink",
            supportsAllDrives=True,
        )
        .execute()
    )
    new_id = copied["id"]
    link = copied.get("webViewLink") or f"https://docs.google.com/presentation/d/{new_id}/edit"

    pres = slides.presentations().get(presentationId=new_id).execute()
    slide_ids = [s["objectId"] for s in pres.get("slides", [])]
    to_remove = [sid for sid in slide_ids if sid != args.slide_id]
    if not to_remove and slide_ids and slide_ids[0] == args.slide_id:
        pass
    elif not slide_ids or args.slide_id not in slide_ids:
        print(
            f"Slide {args.slide_id!r} not in copy (found {len(slide_ids)} slides).",
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        batch_update(
            slides, new_id, [{"deleteObject": {"objectId": sid}} for sid in to_remove]
        )

    if not args.skip_move and args.folder_id:
        try:
            fmeta = drive.files().get(
                fileId=new_id, fields="parents", supportsAllDrives=True
            ).execute()
            prev = ",".join(fmeta.get("parents", []))
            drive.files().update(
                fileId=new_id,
                addParents=args.folder_id,
                removeParents=prev,
                fields="id, name",
                supportsAllDrives=True,
            ).execute()
            print(f"Moved to folder: {args.folder_id}")
        except Exception as e:
            print(
                f"Note: could not move to folder ({e}). File is in the same place as the copy default.",
                file=sys.stderr,
            )

    print(new_id)
    print(link)


if __name__ == "__main__":
    main()
