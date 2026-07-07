
/**
 * Business Data Catalog — OMS & Alation Migration — Executive Gantt
 * Generated — do not edit by hand; regenerate from export_apps_script_gantt.py
 *
 * HOW TO USE:
 * 1. https://script.google.com → New project
 * 2. Paste this entire file over Code.gs
 * 3. Save. Run createExecutiveGantt (Authorize when prompted)
 * 4. Open the created spreadsheet from the dialog or Drive root, then move to your folder.
 */

const PHASE_STYLES = {"Program & Governance": ["1B365D", "B8D4F0"], "Requirements": ["1D4ED8", "BFDBFE"], "Design & Architecture": ["5B21B6", "DDD6FE"], "Build \u2014 MVP": ["047857", "A7F3D0"], "Build \u2014 Full parity": ["065F46", "6EE7B7"], "Migration": ["B45309", "FDE68A"], "Change & Training": ["0E7490", "A5F3FC"], "Cutover & Close": ["991B1B", "FECACA"], "Risk / Dependency": ["4B5563", "E5E7EB"]};

const MONTHS = [[2026, 3], [2026, 4], [2026, 5], [2026, 6], [2026, 7], [2026, 8], [2026, 9], [2026, 10], [2026, 11], [2026, 12], [2027, 1], [2027, 2], [2027, 3], [2027, 4], [2027, 5], [2027, 6], [2027, 7], [2027, 8], [2027, 9], [2027, 10]];

const TASKS = [{"wbs": "1.0", "phase": "Program & Governance", "ws": "Steering", "task": "Program kickoff, charter, steering committee cadence", "owner": "Sponsor / PMO", "start": "2026-03-01", "end": "2026-03-21", "pct": 0, "status": "Not started", "notes": "Exec sponsor; cross-functional steering (Eng, Gov, Analytics)"}, {"wbs": "1.1", "phase": "Program & Governance", "ws": "Governance", "task": "RACI, governance charter \u2014 OMS as system of record", "owner": "Data Governance", "start": "2026-03-10", "end": "2026-04-04", "pct": 0, "status": "Not started", "notes": "Phase-gate sign-off model"}, {"wbs": "1.2", "phase": "Risk / Dependency", "ws": "Vendor", "task": "Alation contract extension negotiation (target 1yr to Oct 2027)", "owner": "Procurement / Sponsor", "start": "2026-03-01", "end": "2026-05-15", "pct": 0, "status": "Not started", "notes": "Fallback: 6-mo extension; wind-down / read-only pricing"}, {"wbs": "1.3", "phase": "Program & Governance", "ws": "Comms", "task": "Stakeholder comms plan & leadership reporting", "owner": "PMO", "start": "2026-03-15", "end": "2027-03-31", "pct": 0, "status": "Not started", "notes": "Timeline visibility; change management"}, {"wbs": "2.0", "phase": "Requirements", "ws": "Current state", "task": "Feature inventory matrix & Alation metadata export", "owner": "BA / Gov", "start": "2026-03-15", "end": "2026-04-18", "pct": 0, "status": "Not started", "notes": "API/MCP export; glossary, articles, tags, lineage, custom fields"}, {"wbs": "2.1", "phase": "Requirements", "ws": "Current state", "task": "Persona\u2013feature matrix, stakeholder interviews, workflow docs", "owner": "BA / Gov", "start": "2026-03-22", "end": "2026-04-25", "pct": 0, "status": "Not started", "notes": "Stewards, analysts, engineers, compliance, leadership"}, {"wbs": "2.2", "phase": "Requirements", "ws": "Evidence", "task": "Screenshot library (Alation + OMS) with annotations", "owner": "BA / Gov", "start": "2026-04-01", "end": "2026-05-02", "pct": 0, "status": "Not started", "notes": "Side-by-side gap evidence for executives"}, {"wbs": "2.3", "phase": "Requirements", "ws": "Enhancements", "task": "Enhancement backlog \u2014 'promised never delivered' + wishes", "owner": "BA / Gov", "start": "2026-04-08", "end": "2026-05-09", "pct": 0, "status": "Not started", "notes": "Separate from MVP parity; Phase 2/3"}, {"wbs": "2.4", "phase": "Requirements", "ws": "OMS leverage", "task": "OMS capability matrix & requirements\u2192OMS mapping", "owner": "BA / OMS liaison", "start": "2026-04-15", "end": "2026-05-16", "pct": 0, "status": "Not started", "notes": "Align to Disney OMS roadmap"}, {"wbs": "2.5", "phase": "Requirements", "ws": "Gaps", "task": "Prioritized gap matrix & build scope (H/M/L criticality)", "owner": "BA / Gov", "start": "2026-04-22", "end": "2026-05-23", "pct": 0, "status": "Not started", "notes": "MVP = critical business metadata parity"}, {"wbs": "2.6", "phase": "Requirements", "ws": "Sign-off", "task": "Consolidated requirements package & governance sign-off", "owner": "Data Governance", "start": "2026-05-10", "end": "2026-05-30", "pct": 0, "status": "Not started", "notes": "Gate before detailed design"}, {"wbs": "3.0", "phase": "Design & Architecture", "ws": "Architecture", "task": "Target data model \u2014 glossary, tags, custom fields, stewardship", "owner": "Architect / OMS", "start": "2026-06-01", "end": "2026-06-28", "pct": 0, "status": "Not started", "notes": "Business metadata in OMS"}, {"wbs": "3.1", "phase": "Design & Architecture", "ws": "Integration", "task": "Integration design \u2014 ingestion, lineage, APIs, Airflow links", "owner": "Eng / OMS", "start": "2026-06-08", "end": "2026-07-12", "pct": 0, "status": "Not started", "notes": "Population of 'Not Available' fields where applicable"}, {"wbs": "3.2", "phase": "Design & Architecture", "ws": "UX", "task": "UI/UX design (OMS design system) \u2014 search, glossary, detail pages", "owner": "UX / OMS", "start": "2026-06-15", "end": "2026-07-19", "pct": 0, "status": "Not started", "notes": "Discovery & stewardship flows"}, {"wbs": "3.3", "phase": "Design & Architecture", "ws": "Migration", "task": "Migration design \u2014 ETL mapping Alation\u2192OMS, validation approach", "owner": "Eng", "start": "2026-06-22", "end": "2026-07-26", "pct": 0, "status": "Not started", "notes": "Metadata-first; \u226595% preservation target"}, {"wbs": "3.4", "phase": "Design & Architecture", "ws": "Sign-off", "task": "Architecture & design review \u2014 approved for build", "owner": "Steering", "start": "2026-07-20", "end": "2026-07-31", "pct": 0, "status": "Not started", "notes": "Formal gate"}, {"wbs": "4.0", "phase": "Build \u2014 MVP", "ws": "Core", "task": "OMS MVP: glossary & business metadata model (implement)", "owner": "OMS / DSS Eng", "start": "2026-06-15", "end": "2026-08-30", "pct": 0, "status": "Not started", "notes": "Terms, definitions, stewardship"}, {"wbs": "4.1", "phase": "Build \u2014 MVP", "ws": "Discovery", "task": "OMS MVP: business-context search & discovery", "owner": "OMS / DSS Eng", "start": "2026-07-01", "end": "2026-09-13", "pct": 0, "status": "Not started", "notes": "Glossary, articles, catalog objects"}, {"wbs": "4.2", "phase": "Build \u2014 MVP", "ws": "Metadata", "task": "OMS MVP: documentation, business description, tags on assets", "owner": "OMS / DSS Eng", "start": "2026-07-15", "end": "2026-09-27", "pct": 0, "status": "Not started", "notes": "Populate placeholders"}, {"wbs": "4.3", "phase": "Build \u2014 MVP", "ws": "Lineage", "task": "OMS MVP: lineage depth + Airflow DAG/task link population", "owner": "OMS / DSS Eng", "start": "2026-08-01", "end": "2026-10-04", "pct": 0, "status": "Not started", "notes": "Table/column per roadmap"}, {"wbs": "4.4", "phase": "Build \u2014 MVP", "ws": "Usage", "task": "OMS MVP: usage metrics (last access, top users) where supported", "owner": "OMS / DSS Eng", "start": "2026-08-15", "end": "2026-10-11", "pct": 0, "status": "Not started", "notes": "Ownership / created-by fields"}, {"wbs": "4.5", "phase": "Build \u2014 MVP", "ws": "QA", "task": "MVP UAT, hardening, performance \u2014 governance acceptance", "owner": "Gov / QA", "start": "2026-09-15", "end": "2026-10-18", "pct": 0, "status": "Not started", "notes": "Success metrics baseline"}, {"wbs": "5.0", "phase": "Build \u2014 Full parity", "ws": "Workflows", "task": "Full parity: custom fields, governance workflows, policy/compliance UI", "owner": "OMS / DSS Eng", "start": "2026-10-15", "end": "2027-01-15", "pct": 0, "status": "Not started", "notes": "Policy center analog; integrations"}, {"wbs": "6.0", "phase": "Migration", "ws": "Planning", "task": "Migration runbook, environments, rollback, validation checkpoints", "owner": "Eng / PMO", "start": "2026-07-01", "end": "2026-08-15", "pct": 0, "status": "Not started", "notes": "Industry: 3\u20136 mo execution window"}, {"wbs": "6.1", "phase": "Migration", "ws": "Extract", "task": "Build/run extraction \u2014 Alation (glossary, articles, tags, lineage, CF)", "owner": "Eng", "start": "2026-08-01", "end": "2026-09-30", "pct": 0, "status": "Not started", "notes": "Secure export before contract risk"}, {"wbs": "6.2", "phase": "Migration", "ws": "Transform", "task": "Transform & map to OMS schema; reconciliation tooling", "owner": "Eng", "start": "2026-09-01", "end": "2026-11-15", "pct": 0, "status": "Not started", "notes": "Data fidelity > speed"}, {"wbs": "6.3", "phase": "Migration", "ws": "Parallel run", "task": "Parallel run \u2014 Alation + OMS (user validation)", "owner": "PMO / Gov", "start": "2026-10-01", "end": "2027-01-15", "pct": 0, "status": "Not started", "notes": "Reduces incident risk vs big-bang"}, {"wbs": "6.4", "phase": "Migration", "ws": "Load", "task": "Phased load to OMS, validation reports, lineage checks", "owner": "Eng / Gov", "start": "2026-11-01", "end": "2027-02-15", "pct": 0, "status": "Not started", "notes": "\u226595% business metadata preserved"}, {"wbs": "7.0", "phase": "Change & Training", "ws": "Materials", "task": "Training curriculum, quick guides, videos, FAQs (vs Alation)", "owner": "Gov / BA", "start": "2026-12-01", "end": "2027-01-31", "pct": 0, "status": "Not started", "notes": "Role-based: stewards, analysts, gov, engineers"}, {"wbs": "7.1", "phase": "Change & Training", "ws": "Delivery", "task": "Workshops, champions program, office hours (2\u20134 wk post cutover)", "owner": "Gov", "start": "2027-01-15", "end": "2027-03-15", "pct": 0, "status": "Not started", "notes": "Adoption metrics; survey loop"}, {"wbs": "8.0", "phase": "Cutover & Close", "ws": "Cutover", "task": "Production cutover \u2014 OMS primary; Alation read-only", "owner": "Steering / Eng", "start": "2027-02-15", "end": "2027-03-15", "pct": 0, "status": "Not started", "notes": "Rollback plan documented"}, {"wbs": "8.1", "phase": "Cutover & Close", "ws": "Milestone", "task": "MILESTONE: Alation baseline contract end (if no extension)", "owner": "\u2014", "start": "2026-10-01", "end": "2026-10-01", "pct": 0, "status": "Milestone", "notes": "Oct 1, 2026 \u2014 extension strongly recommended per program plan"}, {"wbs": "8.2", "phase": "Cutover & Close", "ws": "Decommission", "task": "Alation decommission, archive, final audit evidence", "owner": "Eng / Gov", "start": "2027-09-01", "end": "2027-10-01", "pct": 0, "status": "Not started", "notes": "Align to extended contract Oct 2027"}, {"wbs": "9.0", "phase": "Program & Governance", "ws": "Metrics", "task": "Success metrics dashboard \u2014 WAU, glossary coverage, search success", "owner": "Gov / PMO", "start": "2026-06-01", "end": "2027-04-30", "pct": 0, "status": "Not started", "notes": "Steward activity; migration validation summary"}];

function monthBounds(y, m) {
  const last = new Date(y, m, 0).getDate();
  return { start: new Date(y, m - 1, 1), end: new Date(y, m - 1, last) };
}

function overlaps(taskStart, taskEnd, ms, me) {
  return !(taskEnd < ms || taskStart > me);
}

function createExecutiveGantt() {
  const nMeta = 11;
  const nMonths = MONTHS.length;
  const ncols = nMeta + nMonths;
  const tasks = TASKS;
  const headerRow = 5;
  const dataStart = headerRow + 1;
  const nrows = headerRow + tasks.length;

  const ss = SpreadsheetApp.create(
    'Business Data Catalog — OMS & Alation Migration (Executive Gantt)'
  );
  const sheet = ss.getSheets()[0];
  sheet.setName('Executive Gantt');

  const title =
    'Business Data Catalog — In-House (OMS) & Alation Migration  |  ' +
    'Disney Streaming Services  |  Executive Program Gantt';
  const subtitle =
    'Sources: Product Brief & Migration Project Plan (Mar 2026)  •  ' +
    'Baseline Alation contract end: 1-Oct-2026  •  ' +
    'Recommended: extension + cutover Feb–Mar 2027  •  Decommission Oct 2027';

  sheet.getRange(1, 1, 1, ncols).merge();
  sheet.getRange(1, 1).setValue(title);
  sheet.getRange(1, 1, 1, ncols).setBackground('#1B365D');
  sheet.getRange(1, 1, 1, ncols).setFontColor('#ffffff');
  sheet.getRange(1, 1, 1, ncols).setFontWeight('bold');
  sheet.getRange(1, 1, 1, ncols).setFontSize(15);
  sheet.getRange(1, 1, 1, ncols).setHorizontalAlignment('center');
  sheet.getRange(1, 1, 1, ncols).setVerticalAlignment('middle');
  sheet.setRowHeight(1, 40);

  sheet.getRange(2, 1, 2, ncols).merge();
  sheet.getRange(2, 1).setValue(subtitle);
  sheet.getRange(2, 1, 2, ncols).setBackground('#334155');
  sheet.getRange(2, 1, 2, ncols).setFontColor('#E2E8F0');
  sheet.getRange(2, 1, 2, ncols).setFontStyle('italic');
  sheet.getRange(2, 1, 2, ncols).setHorizontalAlignment('center');
  sheet.setRowHeight(2, 34);

  sheet.getRange(3, 1).setValue('Phase legend (timeline bar colors):');
  sheet.getRange(3, 1).setFontWeight('bold');
  sheet.setRowHeight(3, 24);
  sheet.setRowHeight(4, 8);

  const headers = [
    'WBS',
    'Phase',
    'Workstream',
    'Task / Deliverable',
    'Owner',
    'Start',
    'End',
    'Duration (wks)',
    '% Complete',
    'Status',
    'Dependencies / Notes',
  ].concat(MONTHS.map(function (ym) {
    const d = new Date(ym[0], ym[1] - 1, 1);
    return Utilities.formatDate(d, Session.getScriptTimeZone(), 'MMM-yy');
  }));

  sheet.getRange(headerRow, 1, headerRow, ncols).setValues([headers]);
  sheet.getRange(headerRow, 1, headerRow, ncols).setBackground('#0F172A');
  sheet.getRange(headerRow, 1, headerRow, ncols).setFontColor('#ffffff');
  sheet.getRange(headerRow, 1, headerRow, ncols).setFontWeight('bold');
  sheet.getRange(headerRow, 1, headerRow, ncols).setHorizontalAlignment('center');
  sheet.getRange(headerRow, nMeta + 1, headerRow, ncols).setBackground('#475569');
  sheet.getRange(headerRow, nMeta + 1, headerRow, ncols).setFontSize(9);
  sheet.setRowHeight(headerRow, 44);

  const data = [];
  for (let i = 0; i < tasks.length; i++) {
    const t = tasks[i];
    const ts = new Date(t.start);
    const te = new Date(t.end);
    const dur = Math.max(0, Math.floor((te - ts) / (7 * 24 * 3600 * 1000)));
    const row = [
      t.wbs,
      t.phase,
      t.ws,
      t.task,
      t.owner,
      ts,
      te,
      dur || ((te - ts) > 0 ? 1 : 0),
      t.pct / 100,
      t.status,
      t.notes,
    ];
    const timeline = [];
    for (let j = 0; j < MONTHS.length; j++) {
      const ym = MONTHS[j];
      const mb = monthBounds(ym[0], ym[1]);
      if (overlaps(ts, te, mb.start, mb.end)) {
        timeline.push(String(t.task).indexOf('MILESTONE') === 0 ? '◆' : '■');
      } else {
        timeline.push('');
      }
    }
    data.push(row.concat(timeline));
  }
  sheet.getRange(dataStart, 1, nrows, ncols).setValues(data);

  const metaWidths = [60, 200, 120, 400, 150, 110, 110, 80, 80, 120, 340];
  for (let c = 0; c < metaWidths.length; c++) {
    sheet.setColumnWidth(c + 1, metaWidths[c]);
  }
  for (let c = 0; c < nMonths; c++) {
    sheet.setColumnWidth(nMeta + c + 1, 34);
  }

  for (let i = 0; i < tasks.length; i++) {
    const r = dataStart + i;
    const t = tasks[i];
    const alt = i % 2 === 1;
    const bg = alt ? '#F8FAFC' : '#FFFFFF';
    sheet.getRange(r, 1, r, nMeta).setBackground(bg);
    sheet.getRange(r, 1).setFontWeight('bold');
    sheet.getRange(r, 6, r, 7).setNumberFormat('mmm d, yyyy');
    sheet.getRange(r, 9).setNumberFormat('0%');
    if (String(t.task).indexOf('MILESTONE') === 0) {
      sheet.getRange(r, 4).setFontColor('#B45309');
      sheet.getRange(r, 4).setFontWeight('bold');
    }
  }

  for (let i = 0; i < tasks.length; i++) {
    const r = dataStart + i;
    const t = tasks[i];
    const st = PHASE_STYLES[t.phase] || ['64748B', 'F1F5F9'];
    const light = '#' + st[1];
    const isMile = String(t.task).indexOf('MILESTONE') === 0;
    const ts = new Date(t.start);
    const te = new Date(t.end);
    for (let j = 0; j < MONTHS.length; j++) {
      const ym = MONTHS[j];
      const mb = monthBounds(ym[0], ym[1]);
      if (!overlaps(ts, te, mb.start, mb.end)) continue;
      const col = nMeta + j + 1;
      const bar = isMile ? '#F59E0B' : light;
      sheet.getRange(r, col).setBackground(bar);
      sheet.getRange(r, col).setHorizontalAlignment('center');
      sheet.getRange(r, col).setFontWeight(isMile ? 'bold' : 'normal');
    }
  }

  const statusRange = sheet.getRange(dataStart, 10, nrows, 10);
  const rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(
      ['Not started', 'In progress', 'At risk', 'Blocked', 'Complete', 'Milestone'],
      true
    )
    .setAllowInvalid(true)
    .build();
  statusRange.setDataValidation(rule);

  sheet.setFrozenRows(headerRow);
  sheet.setFrozenColumns(nMeta);

  SpreadsheetApp.flush();
  console.log('Created spreadsheet: ' + ss.getUrl());
}

