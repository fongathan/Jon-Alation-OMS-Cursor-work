# Alation Metrics Dashboard — Automation Setup

Step-by-step guide for **Alation REST API + Python script + cron**.

---

## Step 1: Create a Refresh Token in Alation

1. Log into Alation (e.g. `https://disney-data.alationcloud.com`).
2. Click your **avatar** (top right) → **Account Settings** (or **Profile Settings**).
3. Open the **Authentication** tab.
4. Under **Access Tokens**, click **Create Refresh Token**.
5. Name it (e.g. `Dashboard Cron`).
6. Click **Create Refresh Token**.
7. **Copy the Token Secret Key** immediately — it won’t be shown again.
8. Note your **User ID** (shown in the response or in the URL when viewing your profile).

---

## Step 2: Save the 8 Queries in Alation Compose

1. In Alation, go to **Compose**.
2. Select the **Alation Analytics V2** (or **Private Alation Analytics V2**) data source.
3. For each query below:
   - Open the SQL file from `compose-queries/` (e.g. `01_summary.sql`).
   - Paste the SQL into Compose.
   - Click **Run** to execute it.
   - Click **Save** (or **Save As**).
   - Give it a clear name (e.g. `Dashboard - 01 Summary`).
4. **Run each query at least once** so Alation caches the results (required for the API).

| File | Suggested name |
|------|----------------|
| `01_summary.sql` | Dashboard - 01 Summary |
| `02_top_users.sql` | Dashboard - 02 Top Users |
| `03_curation_monthly.sql` | Dashboard - 03 Curation Monthly |
| `04_dau_mau_monthly.sql` | Dashboard - 04 DAU MAU Monthly |
| `05_top_searches.sql` | Dashboard - 05 Top Searches |
| `06_top_visited.sql` | Dashboard - 06 Top Visited |
| `07_governance_feed.sql` | Dashboard - 07 Governance Feed |
| `08_search_daily.sql` | Dashboard - 08 Search Daily |

---

## Step 3: Get the Query IDs

1. In Compose, open each saved query.
2. Check the URL: `https://disney-data.alationcloud.com/compose/query/123/`
3. The number after `query/` is the **query ID** (e.g. `123`).
4. Write them down:

| Query | ID |
|-------|-----|
| 01 Summary | _____ |
| 02 Top Users | _____ |
| 03 Curation Monthly | _____ |
| 04 DAU MAU Monthly | _____ |
| 05 Top Searches | _____ |
| 06 Top Visited | _____ |
| 07 Governance Feed | _____ |
| 08 Search Daily | _____ |

---

## Step 4: Configure `.env`

1. Copy the example:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set:
   - `ALATION_BASE_URL` — your Alation URL (e.g. `https://disney-data.alationcloud.com`)
   - `ALATION_REFRESH_TOKEN` — the token from Step 1
   - `ALATION_USER_ID` — your user ID
   - `ALATION_QUERY_01_SUMMARY` through `ALATION_QUERY_08_SEARCH_DAILY` — the IDs from Step 3

---

## Step 5: Install Dependencies and Test

```bash
cd "/Users/jonathan.fong/Documents/Jon's Team Docs/alation-metrics-dashboard"
pip3 install -r requirements.txt
python3 refresh_from_alation.py
```

You should see:
```
✓ data.json written to .../alation-metrics-dashboard/data.json
  MAU: 531  |  Searches: 24,858  |  Endorsed: 0.1%
  Top user: ...
```

---

## Step 6: Set Up Cron

1. Open your crontab:
   ```bash
   crontab -e
   ```

2. Add a line (adjust the path if needed):
   ```
   0 6 * * * cd "/Users/jonathan.fong/Documents/Jon's Team Docs/alation-metrics-dashboard" && /usr/bin/python3 refresh_from_alation.py
   ```

3. Save and exit. This runs the script every day at 6:00 AM.

**Note:** Your Mac must be on (or awake) at 6 AM for the job to run. If it’s asleep, the job will not run.

---

## Optional: Schedule Queries in Alation

To keep results fresh before the cron runs:

1. In Compose, open each saved query.
2. Use **Schedule** (if available) to run it daily, e.g. at 5:30 AM.
3. Then the 6 AM cron will pick up the latest results.

If you don’t schedule, the script uses the last cached result from whenever you last ran the query.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `Could not get latest query result ID` | Run the query at least once in Compose. |
| `403 Forbidden` | Check that the refresh token and user ID are correct. |
| `404 Not found` | Verify the query ID and that the query exists. |
| Script runs but data is stale | Schedule the queries in Alation to run before the cron. |
