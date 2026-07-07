# Demo Outline — PMs Using Cursor
**Total time: 5–7 minutes**

---

## Practical Tips to Highlight During the Demo

Weave these into your narrative — they show you know how to use AI effectively:

| # | Tip | When to mention it |
|---|-----|--------------------|
| 1 | **Use screenshots and pictures** | When showing the Migration Plan — "I pasted OMS screenshots into Cursor so it could understand the current UI for the gap analysis." |
| 2 | **Talk in simplest terms possible** | When showing a prompt — "I kept it simple: 'sidebar with 4 stat cards' instead of technical jargon." |
| 3 | **Add context when possible** | When showing Cursor — "I used @ to reference our data.json so Cursor knew the exact data shape." |
| 4 | **Reverse engineer requirements when needed** | When showing Kronos — "I had an existing OMS in mind; I described what I saw and asked Cursor to build something similar." |
| 5 | **Use expensive tokens on planning, cheaper ones on execution** | In the slide deck or Q&A — "I use a stronger model for the initial spec and architecture; faster models for small edits and formatting." |

---

## Pre-Demo Setup (do this before the meeting)

1. **Open these in separate tabs/windows:**
   - `alation-metrics-dashboard/index.html` (in browser)
   - `kronos-ui/index.html` (in browser)
   - `Alation-to-OMS-Migration-Project-Plan.html` (in browser, or use the .md in Cursor)
   - Cursor with the workspace open (for the live prompt demo)

2. **Verify Kronos has data:**  
   If `kronos-ui/kronos_data.json` exists and has content, the Kronos UI will show real-ish data. If not, it may fall back to sample data or show zeros — that's fine for a wireframe demo.

3. **Verify Alation dashboard:**  
   If `alation-metrics-dashboard/data.json` exists, the dashboard will show charts. If it's empty or missing, the layout still demonstrates the concept.

---

## Demo Flow

### Part 1: Alation Metrics Dashboard (1.5–2 min)

**Say:**  
"First, the Alation Metrics Dashboard. This is a report-style POC — I wanted to surface Alation usage metrics for leadership without waiting for a BI team."

**Do:**
1. Open `alation-metrics-dashboard/index.html` in the browser.
2. Point out: sidebar, summary stats (MAU, searches, endorsement rate), charts.
3. Mention: "A Python script pulls from the Alation REST API and writes to `data.json`. I set up a cron job so it refreshes daily. The HTML reads that JSON and renders the charts."
4. Optional: Show `SETUP.md` — "I had Cursor generate this setup doc so anyone could replicate it."
5. **Tip to mention:** "I used @ to reference our data.json so Cursor knew the exact structure — adding context improves output."

**Key message:** PM-defined requirements + Cursor-generated code = working internal dashboard.

---

### Part 2: Kronos UI (2–2.5 min)

**Say:**  
"Second, Kronos — a wireframe and POC for an OMS-style inventory tool. I needed to show stakeholders what 'sustainable inventory management' could look like before we committed engineering."

**Do:**
1. Open `kronos-ui/index.html` in the browser.
2. **Dashboard:** Point out stat cards (Vendors, Trackers, Systems, Use Cases), governance stats (Legal Exceptions, Audits, Relationships).
3. **Navigation:** Click "Vendors" (or Digital Trackers) — show the inventory table with status badges, search.
4. **Search:** Use the header search — show it filters.
5. **Register / Reports / Legal Exceptions:** Quick click through to show the breadth of the wireframe.
6. Mention: "This is a single HTML file with Tailwind and Alpine.js. No backend — it loads from a JSON file. Perfect for stakeholder demos."
7. **Tip to mention:** "I described the UI in simple terms — 'sidebar with Dashboard, Vendors, Trackers' — no jargon. I also reverse-engineered from OMS: I looked at what exists and asked Cursor to build something similar."

**Key message:** Full wireframe with multiple views, generated from a spec. Iterated on prompts to get the layout and data model right.

---

### Part 3: Migration Plan Report (1 min)

**Say:**  
"Third, the Alation-to-OMS Migration Plan. This is a report — executive summary, gap analysis, OMS screenshots, timeline."

**Do:**
1. Open `Alation-to-OMS-Migration-Project-Plan.html` (or the .md in Cursor).
2. Scroll through: Executive Summary, Current OMS Capabilities, gap tables.
3. Mention: "Cursor helped structure this from my notes and screenshots. I provided the content; it helped with formatting and consistency."
4. **Tip to mention:** "Screenshots were key — I pasted OMS screenshots so Cursor could understand the current UI and help with the gap analysis. Pictures beat long descriptions."

**Key message:** Reports and documentation are low-friction use cases — paste in notes, get structured output.

---

### Part 4: Live Prompt (Optional, 1–2 min)

**Say:**  
"If we have time, I'll show how a prompt turns into code."

**Do:**
1. Open Cursor Chat in the workspace.
2. Paste a prompt like:  
   *"Add a new 'Data Quality' stat card to the Kronos dashboard, next to the Legal Exceptions card. Use an icon like fa-check-double and the color amber."*
3. Let Cursor generate the change.
4. Apply it and refresh the Kronos UI to show the new card.

**Key message:** Iteration is fast. PM specifies; Cursor implements. You can tweak and refine in real time.

---

## Backup / If Something Breaks

- **Charts don't load:** Say "The data file might be empty — but the layout and structure are what I'm showing. The Python script would populate this from Alation."
- **Kronos shows zeros:** Say "This is a wireframe — the data is sample/placeholder. The point is the UI structure and flows."
- **Live prompt fails:** Skip it. Say "I can share the prompts I used in the deck — the process is the same."

---

## Closing Line

"These three examples — dashboard, wireframe, report — are all PM-led. I didn't write the code from scratch; I wrote the spec and iterated on prompts. The five tips we covered — screenshots, simple language, context, reverse engineering, and smart token use — make a real difference. The goal isn't to replace engineering; it's to validate and communicate faster so when we do commit engineering time, we're building the right thing."
