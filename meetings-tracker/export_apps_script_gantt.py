#!/usr/bin/env python3
"""Emit ProgramGantt.gs for Google Apps Script (run once → native formatted Sheet)."""

import json
from datetime import date
from pathlib import Path

from generate_executive_gantt import PHASE_STYLES, get_program_tasks_and_months, month_range

OUT = Path(__file__).resolve().parent / "ProgramGantt.gs"

TEMPLATE = r"""
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

const PHASE_STYLES = %phase_styles_json%;

const MONTHS = %months_json%;

const TASKS = %tasks_json%;

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

"""


def main() -> None:
    tasks, _months_py = get_program_tasks_and_months()
    timeline_start = date(2026, 3, 1)
    timeline_end = date(2027, 10, 31)
    months_py = month_range(timeline_start, timeline_end)

    months_json = json.dumps([[y, m] for y, m in months_py])
    phase_styles_json = json.dumps({k: list(v) for k, v in PHASE_STYLES.items()})

    ser_tasks = []
    for t in tasks:
        ser_tasks.append(
            {
                "wbs": t["wbs"],
                "phase": t["phase"],
                "ws": t["ws"],
                "task": t["task"],
                "owner": t["owner"],
                "start": t["start"].isoformat(),
                "end": t["end"].isoformat(),
                "pct": t["pct"],
                "status": t["status"],
                "notes": t["notes"],
            }
        )
    tasks_json = json.dumps(ser_tasks)

    body = TEMPLATE.replace("%phase_styles_json%", phase_styles_json)
    body = body.replace("%months_json%", months_json)
    body = body.replace("%tasks_json%", tasks_json)

    OUT.write_text(body, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
