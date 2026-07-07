# Meeting Hub — Teams Meeting Tracker

A lightweight, local-first tool to track your Microsoft Teams meetings, add notes, and get smart notifications for important or large meetings.

## Features

- **Meeting list** — See upcoming meetings in a clean timeline
- **Notes per meeting** — Add short notes to any meeting (stored locally)
- **Smart notifications** — Get browser notifications for meetings that match your criteria
- **Configurable settings** — Define important people, size thresholds, and notification timing
- **Live calendar sync** — Connect to your Microsoft account to pull real Teams/Outlook meetings

## Quick start

1. Open `index.html` in your browser (double-click or `open index.html`).
2. Click **Import** → **Load sample data** to try it with demo meetings.

## Connect to your real Teams calendar

See **[SETUP.md](SETUP.md)** for step-by-step instructions. You’ll need to:

1. Register an app in Microsoft Entra ID (Azure)
2. Add your Client ID and redirect URI to `config.js`
3. Run a local server (`npm start` or VS Code Live Server)
4. Click **Connect Microsoft** and sign in, then **Sync calendar**
3. Open **Settings** to configure:
   - **Important people** — Emails (one per line). Meetings with these people are flagged and can trigger notifications.
   - **Notify when meeting size ≥** — Minimum attendee count for “large meeting” notifications.
   - **Notify X minutes before** — How far in advance to send a reminder.
   - **Notify for VIP / large meetings** — Toggle each notification type on or off.

## Import from Teams

To use real Teams data:

1. In **Cursor**, open Chat and ask: *"Get my Teams meetings for the next 7 days using the Teams MCP."*
2. Copy the JSON output from the response.
3. In Meeting Hub, click **Import from Teams** and paste the JSON.
4. Click **Import JSON**.

The app expects an array of meeting objects. Each meeting should have:

- `subject` — Meeting title
- `startTime` — ISO 8601 (e.g. `"2026-03-18T09:00:00.000Z"`)
- `endTime` — ISO 8601
- `organizer` — `{ name, email }`
- `attendees` — Array of `{ name, email }` (optional)
- `joinUrl` — Teams meeting link (optional)

## Notifications

Meeting Hub uses the browser’s **Notification API**. When you first use it, you may be asked to allow notifications. Notifications are sent for meetings that match your settings (VIP and/or large) within the configured time window.

## Data storage

All data is stored in your browser:

- **Notes** — `localStorage` (key: `meetinghub_notes`)
- **Settings** — `localStorage` (key: `meetinghub_settings`)
- **Meetings** — `localStorage` (key: `meetinghub_meetings`)

No data is sent to any server. Everything stays on your device.
