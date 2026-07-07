/**
 * UI Integrated — marked: yellow callouts + info icons (native title tooltips).
 */
(function () {
  document.body.classList.add("marked-page");

  const TIPS = {
    home: "Home catalog: entry point for tables, pipelines, streams, endpoints, and reports — discoverability and scope for governance.",
    bdcStrip: "Business catalog strip on list views: stewardship sync, glossary, export — curated metadata at the datasource.",
    tabs: "Tabs (Overview / Queries / SQL / Lineage): separate narrative metadata, query history, ad-hoc SQL, and lineage.",
    queries: "Previous queries: scoped history for reproducibility and collaboration on this table.",
    sql: "SQL runner: governed execution with connection, audit text, and results grid.",
    sample: "Columns vs Sample Content: Alation-style toggle between structure and sample rows.",
    cols: "Column grid: business title & description with lineage links; edit capture at column level.",
    tableMeta: "Business metadata fields: light red = pending steward / governance review.",
    lineage: "Lineage tab: upstream/downstream visualization for impact and trust."
  };

  function wrap(sel, key) {
    const el = document.querySelector(sel);
    if (!el || el.closest(".bdc-feature-mark")) return;
    const tip = TIPS[key];
    if (!tip) return;
    const wrapEl = document.createElement("div");
    wrapEl.className = "bdc-feature-mark";
    el.parentNode.insertBefore(wrapEl, el);
    wrapEl.appendChild(el);
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "bdc-i";
    btn.title = tip;
    btn.setAttribute("aria-label", "Requirement");
    wrapEl.appendChild(btn);
  }

  function banner() {
    const main = document.querySelector(".oms-main");
    if (!main || document.querySelector(".marked-banner")) return;
    const b = document.createElement("div");
    b.className = "marked-banner";
    b.innerHTML =
      "<strong>UI Integrated — marked</strong> · Yellow regions: Business Data Catalog features. Hover <strong>i</strong> for requirement text.";
    const top = main.querySelector(".oms-topbar");
    if (top && top.nextSibling) main.insertBefore(b, top.nextSibling);
    else main.insertBefore(b, main.firstChild);
  }

  function run() {
    banner();
    wrap("#homeColumns", "home");
    wrap("#view-snowflake-list .bdc-strip", "bdcStrip");
    wrap("#detailTabs", "tabs");
    wrap("#assetPanel-queries", "queries");
    wrap("#assetPanel-sql", "sql");
    wrap("#view-snowflake-detail .sample-toggle", "sample");
    wrap("#view-snowflake-detail #columnsPane .oms-table-wrap", "cols");
    const db = document.querySelector("#detailBusiness");
    if (db && !db.closest(".bdc-feature-mark")) wrap("#detailBusiness", "tableMeta");
    wrap("#assetPanel-lineage", "lineage");
  }

  run();
  setTimeout(run, 500);
  setTimeout(run, 2000);
})();
