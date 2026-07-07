/**
 * UI On-Top — marked: highlights BDC-only features; notes hidden technical metadata.
 */
(function () {
  document.body.classList.add("marked-page");

  const TIPS = {
    nav: "Business Data Catalog left-nav: dedicated workspace for stewardship without replacing core OMS.",
    home: "BDC Home: same grouped sources as OMS landing — drill-in preserves catalog mental model.",
    noTech: "Technical metrics & system sections are intentionally omitted here — business metadata, SQL, and samples only.",
    tabs: "Same tab pattern (Overview / Queries / SQL / Lineage) inside the BDC drill view.",
    queries: "Previous queries: reproducibility and team history for this asset.",
    sql: "SQL runner: governed queries with logging — meets self-serve and audit requirements.",
    sample: "Sample Content: governed preview rows separate from column definitions.",
    cols: "Columns list: business title/description first; technical types behind toggle.",
    business: "Business metadata card: policies, stewards, glossary — no storage/bytes/profiling blocks.",
    lineage: "Lineage summary oriented to business impact."
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
      "<strong>UI On-Top — marked</strong> · BDC tab experience. Technical metadata sections are <em>removed</em> from table detail. Hover <strong>i</strong> icons for requirements.";
    const top = main.querySelector(".oms-topbar");
    if (top && top.nextSibling) main.insertBefore(b, top.nextSibling);
    else main.insertBefore(b, main.firstChild);
  }

  function run() {
    banner();
    wrap("#homeColumnsBdc", "home");
    const note = document.querySelector("#panel-bdc-snowflake-detail > p");
    if (note && !note.closest(".bdc-feature-mark")) {
      const w = document.createElement("div");
      w.className = "bdc-feature-mark";
      note.parentNode.insertBefore(w, note);
      w.appendChild(note);
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "bdc-i";
      btn.title = TIPS.noTech;
      w.appendChild(btn);
    }
    wrap("#bdcDetailTabs", "tabs");
    wrap("#bdcPanel-queries", "queries");
    wrap("#bdcPanel-sql", "sql");
    wrap("#panel-bdc-snowflake-detail .sample-toggle", "sample");
    wrap("#bdcColumnsPane .oms-table-wrap", "cols");
    wrap("#bdcBusiness", "business");
    wrap("#bdcPanel-lineage", "lineage");
  }

  run();
  setTimeout(run, 500);
  setTimeout(run, 2000);
})();
