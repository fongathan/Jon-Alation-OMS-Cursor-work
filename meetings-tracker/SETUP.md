# Connect Meeting Hub to Your Microsoft Teams Calendar

To show your real Teams/Outlook calendar in Meeting Hub, you need to register an app in Microsoft Entra ID (Azure AD) and add your credentials to `config.js`. This is a one-time setup.

## Step 1: Register an app in Azure

1. Go to **[Azure Portal](https://portal.azure.com)** → **Microsoft Entra ID** (or **Azure Active Directory**).
2. Click **App registrations** → **New registration**.
3. Fill in:
   - **Name:** `Meeting Hub` (or any name)
   - **Supported account types:** Choose one:
     - **Accounts in this organizational directory only** — if you only use a work/school account
     - **Accounts in any organizational directory and personal Microsoft accounts** — if you might use a personal Outlook account too
   - **Redirect URI:** Select **Single-page application (SPA)** and enter:
     - `http://localhost:5500` (if using VS Code Live Server on default port)
     - Or `http://localhost:3000`, `http://127.0.0.1:8080`, etc. — **must match exactly** where you open the app
4. Click **Register**.

## Step 2: Add API permissions

1. In your app, go to **API permissions** → **Add a permission**.
2. Choose **Microsoft Graph** → **Delegated permissions**.
3. Add:
   - `User.Read`
   - `Calendars.Read`
4. Click **Add permissions**.

## Step 3: Copy IDs into config.js

1. In your app, go to **Overview**.
2. Copy:
   - **Application (client) ID**
   - **Directory (tenant) ID** (use `common` if you want any Microsoft account to sign in)
3. Open `config.js` in this folder and replace:

```javascript
window.MEETING_HUB_CONFIG = {
  clientId: 'YOUR_CLIENT_ID',           // ← Paste Application (client) ID
  tenantId: 'common',                    // ← Use 'common' or your Directory (tenant) ID
  redirectUri: 'http://localhost:5500',  // ← Must match the redirect URI you set in Azure
};
```

## Step 4: Run a local server

OAuth does not work when opening the file directly (`file://`). You must serve the app over HTTP:

- **VS Code:** Install the "Live Server" extension, right‑click `index.html` → "Open with Live Server" (usually port 5500).
- **Terminal:** From this folder, run:
  ```bash
  npx serve .
  ```
  Then open the URL shown (e.g. `http://localhost:3000`). Update `redirectUri` in `config.js` to match.

## Step 5: Connect in Meeting Hub

1. Open Meeting Hub in your browser (via the local server).
2. Click **Connect Microsoft**.
3. Sign in with your Microsoft account when prompted.
4. Click **Sync calendar** to load your meetings.

Your notes and settings stay in your browser. Each time you want fresh data, click **Sync calendar** again.
