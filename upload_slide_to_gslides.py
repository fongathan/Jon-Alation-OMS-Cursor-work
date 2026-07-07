import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN = os.path.expanduser("~/Library/Application Support/All Google MCP/token.json")
SRC = "Alation-to-Data-Navigator-Slide.pptx"
NAME = "Alation to Data Navigator - Slide"

creds = Credentials.from_authorized_user_file(TOKEN)
if not creds.valid and creds.refresh_token:
    creds.refresh(Request())

drive = build("drive", "v3", credentials=creds)

media = MediaFileUpload(
    SRC,
    mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    resumable=True,
)
file = drive.files().create(
    body={"name": NAME, "mimeType": "application/vnd.google-apps.presentation"},
    media_body=media,
    fields="id,name,webViewLink",
    supportsAllDrives=True,
).execute()

print("ID:", file["id"])
print("NAME:", file["name"])
print("LINK:", file["webViewLink"])
