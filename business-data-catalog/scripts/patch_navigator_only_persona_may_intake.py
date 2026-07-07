#!/usr/bin/env python3
"""Apply May 2026 intake persona-first UX to navigator-only.html."""
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "navigator-only.html"
text = PATH.read_text(encoding="utf-8")

CSS = """
    /* May intake — persona lens & program boundaries */
    .nav-boundary-lede {
      margin: 0.35rem 0 0;
      font-size: 13px;
      line-height: 1.45;
      color: var(--oms-muted);
      max-width: 78ch;
    }
    .nav-persona-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.5rem 0.75rem;
      margin: 0 0 1rem;
      padding: 0.5rem 0.65rem;
      border-radius: 10px;
      background: rgba(124, 77, 255, 0.06);
      border: 1px solid rgba(124, 77, 255, 0.18);
    }
    .nav-persona-bar label {
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: #5e35b1;
      margin: 0;
    }
    .nav-persona-bar select {
      font-size: 13px;
      padding: 0.35rem 0.6rem;
      border-radius: 8px;
      border: 1px solid var(--oms-border);
      background: #fff;
      min-width: 11rem;
    }
    .nav-lens-banner {
      margin: 0 0 1rem;
      padding: 0.65rem 0.85rem;
      font-size: 12px;
      line-height: 1.45;
      border-radius: 8px;
      background: rgba(124, 77, 255, 0.08);
      border: 1px solid rgba(124, 77, 255, 0.2);
      max-width: 90ch;
    }
    .nav-lens-banner[data-lens="steward"] {
      background: rgba(124, 77, 255, 0.1);
      border-color: rgba(124, 77, 255, 0.28);
    }
    .nav-lens-banner[data-lens="compliance"] {
      background: rgba(225, 29, 72, 0.06);
      border-color: rgba(225, 29, 72, 0.2);
    }
    .nav-persona-entry {
      margin: 0 0 1.25rem;
      padding: 1rem 1.15rem;
      border-radius: 12px;
      border: 1px solid rgba(124, 77, 255, 0.2);
      background: linear-gradient(180deg, rgba(124, 77, 255, 0.06) 0%, #fff 100%);
    }
    .nav-persona-entry h2 {
      margin: 0 0 0.35rem;
      font-size: 1.05rem;
    }
    .nav-persona-entry-lede {
      margin: 0 0 0.85rem;
      font-size: 13px;
      color: var(--oms-muted);
      max-width: 72ch;
    }
    .nav-persona-cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 0.65rem;
    }
    .nav-persona-card {
      text-align: left;
      padding: 0.75rem 0.85rem;
      border-radius: 10px;
      border: 1px solid var(--oms-border);
      background: #fff;
      cursor: pointer;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .nav-persona-card:hover {
      border-color: rgba(124, 77, 255, 0.45);
      box-shadow: 0 4px 14px rgba(124, 77, 255, 0.12);
    }
    .nav-persona-card.is-active {
      border-color: #7c4dff;
      box-shadow: 0 0 0 2px rgba(124, 77, 255, 0.2);
    }
    .nav-persona-card h3 {
      margin: 0 0 0.25rem;
      font-size: 0.9rem;
      color: #4a148c;
    }
    .nav-persona-card p {
      margin: 0;
      font-size: 12px;
      color: var(--oms-muted);
      line-height: 1.35;
    }
    .nav-persona-card .tag {
      display: inline-block;
      margin-top: 0.4rem;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: #5e35b1;
    }
    .nav-alignment-strip {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.5rem;
      margin: 0 0 0.85rem;
    }
    @media (max-width: 720px) {
      .nav-alignment-strip { grid-template-columns: 1fr; }
    }
    .nav-alignment-col {
      padding: 0.65rem 0.75rem;
      border-radius: 8px;
      border: 1px solid var(--oms-border);
      background: #fafafa;
      font-size: 12px;
      line-height: 1.4;
    }
    .nav-alignment-col h4 {
      margin: 0 0 0.35rem;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: #64748b;
    }
    .nav-alignment-col--defined { border-color: rgba(94, 53, 177, 0.25); background: #f8f6ff; }
    .nav-alignment-col--observed { border-color: rgba(14, 116, 144, 0.25); background: #f0fdfa; }
    .nav-alignment-col--gap { border-color: rgba(180, 83, 9, 0.3); background: #fffbeb; }
    .nav-alignment-col--gap.has-gap strong { color: #b45309; }
    .nav-policy-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
      margin-top: 0.5rem;
    }
    .nav-policy-chip {
      font-size: 11px;
      padding: 0.2rem 0.5rem;
      border-radius: 999px;
      background: rgba(225, 29, 72, 0.08);
      border: 1px solid rgba(225, 29, 72, 0.2);
      color: #9f1239;
    }
    #omsMain[data-persona-lens="consumer"] .bdc-subnav-group-ops,
    #omsMain[data-persona-lens="consumer"] .bdc-subnav-divider,
    #omsMain[data-persona-lens="compliance"] .bdc-subnav-group-ops,
    #omsMain[data-persona-lens="compliance"] .bdc-subnav-divider {
      display: none !important;
    }
    #omsMain[data-persona-lens="consumer"] #catalogPulse,
    #omsMain[data-persona-lens="compliance"] #catalogPulse {
      display: none !important;
    }
    #omsMain[data-persona-lens="consumer"] #kpiRequestsCard,
    #omsMain[data-persona-lens="compliance"] #kpiRequestsCard {
      display: none !important;
    }
    #omsMain[data-persona-lens="consumer"] #catalogCommentsBlock,
    #omsMain[data-persona-lens="consumer"] #catalogNotesBlock,
    #omsMain[data-persona-lens="compliance"] #catalogCommentsBlock,
    #omsMain[data-persona-lens="compliance"] #catalogNotesBlock {
      display: none !important;
    }
    #omsMain[data-persona-lens="consumer"] .bdc-asset-social,
    #omsMain[data-persona-lens="compliance"] .bdc-asset-social {
      display: none !important;
    }
    .nav-section-job {
      margin: 0 0 0.75rem;
      font-size: 12px;
      color: #5e35b1;
      font-weight: 600;
    }
"""

text = text.replace(
    "    .bdc-subnav-group-ops.is-expanded .bdc-subnav-ops-extra {\n      display: inline;\n    }",
    "    .bdc-subnav-group-ops.is-expanded .bdc-subnav-ops-extra {\n      display: inline;\n    }" + CSS,
    1,
)

text = text.replace(
    """        <div class="bdc-hero">
          <h1>Data Navigator</h1>
        </div>

        <nav class="bdc-subnav" aria-label="Catalog and operations" id="bdcSubnav">""",
    """        <div class="bdc-hero">
          <h1>Data Navigator</h1>
          <p class="nav-boundary-lede"><strong>626</strong> improves metadata supply · <strong>OMS</strong> stores and serves it · <strong>Navigator</strong> is governed discovery for business and compliance users (engineers → OMS UI).</p>
        </div>

        <div class="nav-persona-bar" role="region" aria-label="Persona lens">
          <label for="navPersonaLensSelect">Viewing as</label>
          <select id="navPersonaLensSelect" aria-label="Persona lens">
            <option value="consumer" selected>Business &amp; analyst (primary)</option>
            <option value="steward">Data steward</option>
            <option value="compliance">Privacy &amp; compliance (read)</option>
          </select>
        </div>
        <div class="nav-lens-banner" id="navLensBanner" data-lens="consumer" role="status"></div>

        <nav class="bdc-subnav" aria-label="Catalog and operations" id="bdcSubnav">""",
    1,
)

text = text.replace(
    """        <section id="panel-home" class="section-panel">
          <div class="oms-welcome">
            <div class="oms-welcome-icon" aria-hidden="true">◇</div>
            <div>
              <h1 style="margin:0;font-size:1.25rem;">Data sources</h1>
              <p style="margin:0.35rem 0 0;font-size:13px;color:var(--oms-muted);">Choose a table platform to open the catalog experience (filters, grid, asset detail) scoped to assets indexed under that source in this demo.</p>
            </div>
          </div>
          <div class="home-columns" id="homeColumnsBdc"></div>
        </section>""",
    """        <section id="panel-home" class="section-panel">
          <div class="nav-persona-entry" id="navPersonaEntry">
            <h2>What do you need?</h2>
            <p class="nav-persona-entry-lede">Persona-first entry (May intake): one catalog spine, different defaults per role — not one UI for 626, OMS, DSAR, tracker, and discovery combined.</p>
            <div class="nav-persona-cards" role="list">
              <button type="button" class="nav-persona-card is-active" data-persona-lens="consumer" data-persona-section="catalog">
                <h3>Find &amp; trust data</h3>
                <p>Official metrics, approved datasets, gold definitions — low noise.</p>
                <span class="tag">Primary · MVP</span>
              </button>
              <button type="button" class="nav-persona-card" data-persona-lens="steward" data-persona-section="catalog">
                <h3>Curate &amp; endorse</h3>
                <p>Reconcile definitions, coverage gaps, endorsement workflows.</p>
                <span class="tag">Secondary · thin</span>
              </button>
              <button type="button" class="nav-persona-card" data-persona-lens="compliance" data-persona-section="catalog">
                <h3>Review evidence</h3>
                <p>Defined vs observed on assets; policy &amp; classification read — not DSAR/tracker consoles.</p>
                <span class="tag">Secondary · read</span>
              </button>
            </div>
          </div>
          <p class="nav-section-job" id="navSectionJob" hidden></p>
          <div class="oms-welcome">
            <div class="oms-welcome-icon" aria-hidden="true">◇</div>
            <div>
              <h2 style="margin:0;font-size:1.1rem;">Browse by platform</h2>
              <p style="margin:0.35rem 0 0;font-size:13px;color:var(--oms-muted);">Optional: open the catalog scoped to a table platform. Consumer lens hides dev-only and internal-only assets in the grid.</p>
            </div>
          </div>
          <div class="home-columns" id="homeColumnsBdc"></div>
        </section>""",
    1,
)

text = text.replace(
    """            <div class="kpi-card">
              <div class="lbl">Open access requests</div>
              <div class="val" id="kpiRequests">3</div>
            </div>""",
    """            <div class="kpi-card" id="kpiRequestsCard">
              <div class="lbl">Open access requests</div>
              <div class="val" id="kpiRequests">3</div>
            </div>""",
    1,
)

text = text.replace(
    """                <div class="catalog-asset-detail-summary is-placeholder" id="catalogDetailSummary" aria-label="Asset summary"></div>
                <div class="drawer-tabs" role="tablist" id="catalogDetailTabs">""",
    """                <div class="catalog-asset-detail-summary is-placeholder" id="catalogDetailSummary" aria-label="Asset summary"></div>
                <div id="catalogAlignmentMount" class="nav-alignment-mount" hidden></div>
                <div class="drawer-tabs" role="tablist" id="catalogDetailTabs">""",
    1,
)

text = text.replace(
    """                  <button type="button" role="tab" aria-selected="false" data-tab="technical">Technical</button>
                  <button type="button" role="tab" aria-selected="false" data-tab="schema">Schema</button>
                  <button type="button" role="tab" aria-selected="false" data-tab="dictionary">Dictionary</button>
                  <button type="button" role="tab" aria-selected="false" data-tab="audit">Audit</button>""",
    """                  <button type="button" role="tab" aria-selected="false" data-tab="technical" data-persona-tab="steward">Technical</button>
                  <button type="button" role="tab" aria-selected="false" data-tab="schema" data-persona-tab="steward">Schema</button>
                  <button type="button" role="tab" aria-selected="false" data-tab="dictionary" data-persona-tab="steward">Dictionary</button>
                  <button type="button" role="tab" aria-selected="false" data-tab="audit" data-persona-tab="steward">Audit</button>""",
    1,
)

text = text.replace(
    """                    <button type="button" class="btn-ghost" id="btnCatalogSeeFullDetails" title="Open full-page asset view" aria-label="See full asset details on a dedicated page" disabled>See full details</button>""",
    """                    <button type="button" class="btn-ghost" id="btnCatalogSeeFullDetails" title="Open full-page asset view" aria-label="See full asset details on a dedicated page" disabled>See full details</button>
                    <button type="button" class="btn-ghost" id="btnCatalogOpenInOms" title="Technical lineage, SQL, and operational metadata" disabled>Open in OMS</button>""",
    1,
)

text = text.replace(
    """          <p style="margin:0 0 0.75rem;font-size:12px;color:var(--oms-muted);max-width:80ch;">BDC-on-top view: operational / storage / profiling technical blocks are hidden. Focus is stewardship, policy, SQL, samples, and business column context.</p>

          <div class="asset-detail-tabs" role="tablist" id="bdcDetailTabs">
            <button type="button" role="tab" aria-selected="true" data-bdc-tab="overview">Overview</button>
            <button type="button" role="tab" aria-selected="false" data-bdc-tab="sql">SQL</button>
            <button type="button" role="tab" aria-selected="false" data-bdc-tab="lineage">Lineage</button>
          </div>""",
    """          <div id="bdcAlignmentMount" class="nav-alignment-mount"></div>
          <p class="bdc-detail-lede" id="bdcDetailLede" style="margin:0 0 0.75rem;font-size:12px;color:var(--oms-muted);max-width:80ch;">Governed business view on OMS — stewardship, definitions, and policy context. SQL and deep technical truth live in OMS UI.</p>

          <div class="asset-detail-tabs" role="tablist" id="bdcDetailTabs">
            <button type="button" role="tab" aria-selected="true" data-bdc-tab="overview">Overview</button>
            <button type="button" role="tab" aria-selected="false" data-bdc-tab="sql" data-persona-tab="steward">SQL</button>
            <button type="button" role="tab" aria-selected="false" data-bdc-tab="lineage" data-persona-tab="steward">Lineage</button>
            <button type="button" class="btn-ghost" id="btnBdcOpenInOms" style="margin-left:auto;font-size:12px;">Open in OMS</button>
          </div>""",
    1,
)

# ASSETS audience
audience_map = {
    '"id": "1",': '"id": "1",\n      audience: "consumer",',
    '"id": "2",': '"id": "2",\n      audience: "both",',
    '"id": "3",': '"id": "3",\n      audience: "consumer",',
    '"id": "4",': '"id": "4",\n      audience: "consumer",',
    '"id": "5",': '"id": "5",\n      audience: "internal",',
    '"id": "6",': '"id": "6",\n      audience: "consumer",',
    '"id": "7",': '"id": "7",\n      audience: "consumer",',
    '"id": "8",': '"id": "8",\n      audience: "internal",',
}
for old, new in audience_map.items():
    text = text.replace(old, new, 1)

text = text.replace(
    '  const state = { page: 1, pageSize: 10, filters: {}, current: null, selectedCatalogAssetId: null, catalogQualitySort: null, section: "home", adminOpsExpanded: false,',
    '  const state = { page: 1, pageSize: 10, filters: {}, current: null, selectedCatalogAssetId: null, catalogQualitySort: null, section: "home", personaLens: "consumer", adminOpsExpanded: false,',
    1,
)

JS_BLOCK = r'''
  const PERSONA_LENS_META = {
    consumer: {
      banner: "Low-noise discovery — approved, business-relevant assets (Renat: not every non–customer-facing or internal-only dataset).",
      search: "Find official metrics and approved tables…",
      job: "Primary story: find and trust the right metric or dataset.",
      filterConsumer: true
    },
    steward: {
      banner: "Thin stewardship path — endorse, reconcile, and see coverage on the same catalog records consumers use.",
      search: "Search assets, stewards, and endorsement state…",
      job: "Secondary story: curate definitions and trust signals at scale.",
      filterConsumer: false
    },
    compliance: {
      banner: "Read policy and classification on assets — defined vs observed on one record. DSAR, tracker, and consent operations stay in pillar tools (phase 2 hub links only).",
      search: "Audit assets — sensitivity, policy linkage, evidence…",
      job: "Secondary story: evidence-friendly review without operational consoles in Navigator.",
      filterConsumer: false
    }
  };

  function personaLensOk(a) {
    const meta = PERSONA_LENS_META[state.personaLens] || PERSONA_LENS_META.consumer;
    if (!meta.filterConsumer) return true;
    return (a.audience || "both") !== "internal";
  }

  function renderAlignmentStripHtml(a) {
    const defined = escapeHtml((a.displayTitle || a.name) + " — " + (a.description || "No steward definition published.").slice(0, 140));
    const colCount = a.columns ? a.columns.length : 0;
    const observed = escapeHtml(
      "OMS index: " + colCount + " column(s) · env " + (a.env || "—") + " · " + (a.sensitivity || "—") +
      (catalogEndorsed.has(a.id) ? " · endorsed" : "")
    );
    const driftCol = a.columns && a.columns.find((c) => c.governanceFlag);
    const hasGap = !!(driftCol || (a.quality != null && a.quality < 72));
    const gapText = driftCol
      ? "Column " + driftCol.key + ": business description needs governance sign-off vs production usage (demo)."
      : (a.quality < 72 ? "Description or coverage thin vs observed usage — steward review recommended (demo)." : "No material gaps in last automated check (demo).");
    const policyHtml = state.personaLens === "compliance"
      ? `<div class="nav-policy-chips"><span class="nav-policy-chip">${escapeHtml(a.sensitivity)}</span><span class="nav-policy-chip">Classification read</span><span class="nav-policy-chip">Policy link (demo)</span></div>`
      : "";
    return `<div class="nav-alignment-strip" role="region" aria-label="Defined vs observed">
      <div class="nav-alignment-col nav-alignment-col--defined"><h4>Defined</h4><p>${defined}</p></div>
      <div class="nav-alignment-col nav-alignment-col--observed"><h4>Observed</h4><p>${observed}</p></div>
      <div class="nav-alignment-col nav-alignment-col--gap${hasGap ? " has-gap" : ""}"><h4>Gap</h4><p><strong>${hasGap ? "Review" : "OK"}:</strong> ${escapeHtml(gapText)}</p></div>
    </div>${policyHtml}`;
  }

  function mountAlignmentStrip(mountId, a) {
    const el = document.getElementById(mountId);
    if (!el) return;
    if (!a) { el.hidden = true; el.innerHTML = ""; return; }
    el.hidden = false;
    el.innerHTML = renderAlignmentStripHtml(a);
  }

  function applyPersonaLensUi() {
    const lens = state.personaLens || "consumer";
    const meta = PERSONA_LENS_META[lens] || PERSONA_LENS_META.consumer;
    const omsMain = document.getElementById("omsMain");
    if (omsMain) omsMain.setAttribute("data-persona-lens", lens);
    const sel = document.getElementById("navPersonaLensSelect");
    if (sel && sel.value !== lens) sel.value = lens;
    document.querySelectorAll(".nav-persona-card").forEach((card) => {
      card.classList.toggle("is-active", card.getAttribute("data-persona-lens") === lens);
    });
    const banner = document.getElementById("navLensBanner");
    if (banner) {
      banner.dataset.lens = lens;
      banner.textContent = meta.banner;
    }
    const search = document.getElementById("globalSearch");
    if (search) search.placeholder = meta.search;
    const job = document.getElementById("navSectionJob");
    if (job) {
      job.hidden = false;
      job.textContent = meta.job;
    }
    document.querySelectorAll("#catalogDetailTabs [role=tab][data-persona-tab]").forEach((tab) => {
      const hide = lens !== "steward";
      tab.hidden = hide;
      tab.style.display = hide ? "none" : "";
    });
    document.querySelectorAll("#bdcDetailTabs [data-persona-tab]").forEach((tab) => {
      const hide = lens !== "steward";
      tab.hidden = hide;
      tab.style.display = hide ? "none" : "";
    });
    if (lens !== "steward") {
      const sqlTab = document.querySelector('#bdcDetailTabs [data-bdc-tab="sql"]');
      if (sqlTab && sqlTab.getAttribute("aria-selected") === "true") setBdcTab("overview");
    }
    state.page = 1;
    renderTable();
    if (state.section === "overview") {
      renderKpis();
      if (typeof renderPopularTables === "function") renderPopularTables();
    }
    if (state.current) {
      mountAlignmentStrip("catalogAlignmentMount", state.current);
      syncCatalogDetailTabBody();
    }
  }

  function setPersonaLens(lens, section) {
    if (!PERSONA_LENS_META[lens]) lens = "consumer";
    state.personaLens = lens;
    applyPersonaLensUi();
    if (section) showSection(section);
  }

'''

text = text.replace(
    "  function updateNavLensBanner(_section) {\n    /* Lens banner removed from UI; kept as no-op for compatibility. */\n  }",
    JS_BLOCK + "\n  function updateNavLensBanner(_section) {\n    applyPersonaLensUi();\n  }",
    1,
)

text = text.replace(
    """      catalogDataSourceOk(a)
    ];""",
    """      catalogDataSourceOk(a),
      personaLensOk(a)
    ];""",
    1,
)

text = text.replace(
    """    sum.innerHTML = `
      ${descSection}
      ${stewHtml}
      <a href="#requests" class="btn-primary catalog-request-access js-catalog-request-access" role="button">Request access</a>
    `;""",
    """    sum.innerHTML = `
      ${descSection}
      ${stewHtml}
      <a href="#requests" class="btn-primary catalog-request-access js-catalog-request-access" role="button" data-persona-action="steward">Request access</a>
    `;
    mountAlignmentStrip("catalogAlignmentMount", a);""",
    1,
)

text = text.replace(
    """    refreshCatalogCollaborationUI();
    setCatalogPanelActionsEnabled(true);
  }""",
    """    refreshCatalogCollaborationUI();
    setCatalogPanelActionsEnabled(true);
    mountAlignmentStrip("catalogAlignmentMount", a);
    applyPersonaLensUi();
  }""",
    1,
)

text = text.replace(
    """    if (panel) panel.hidden = true;
      panel.classList.remove("is-expanded");
    }
    document.querySelector("#catalogAssetDetail .catalog-asset-detail-inner")?.classList.remove("has-catalog-asset");
    renderTable();
  }""",
    """    if (panel) panel.hidden = true;
      panel.classList.remove("is-expanded");
    }
    document.querySelector("#catalogAssetDetail .catalog-asset-detail-inner")?.classList.remove("has-catalog-asset");
    mountAlignmentStrip("catalogAlignmentMount", null);
    renderTable();
  }""",
    1,
)

text = text.replace(
    """    renderBdcAssetSocial();
    document.getElementById("panel-bdc-snowflake-list").classList.add("section-hidden");
    document.getElementById("panel-bdc-snowflake-detail").classList.remove("section-hidden");
  }""",
    """    renderBdcAssetSocial();
    mountAlignmentStrip("bdcAlignmentMount", ASSETS[1]);
    applyPersonaLensUi();
    document.getElementById("panel-bdc-snowflake-list").classList.add("section-hidden");
    document.getElementById("panel-bdc-snowflake-detail").classList.remove("section-hidden");
  }""",
    1,
)

INIT_WIRE = """
  document.getElementById("navPersonaLensSelect")?.addEventListener("change", (e) => {
    setPersonaLens(e.target.value, state.section);
  });
  document.querySelectorAll(".nav-persona-card").forEach((card) => {
    card.addEventListener("click", () => {
      setPersonaLens(card.getAttribute("data-persona-lens"), card.getAttribute("data-persona-section") || "catalog");
    });
  });
  document.getElementById("btnCatalogOpenInOms")?.addEventListener("click", () => {
    alert("Demo: Open in OMS UI for technical lineage, SQL, and pipeline metadata (May intake — engineers do not use Navigator as a second platform).");
  });
  document.getElementById("btnBdcOpenInOms")?.addEventListener("click", () => {
    alert("Demo: Open in OMS UI for technical lineage, SQL, and pipeline metadata.");
  });
  applyPersonaLensUi();
"""

text = text.replace(
    """  document.getElementById("catalogAssetDetail").addEventListener("click", (e) => {
    if (e.target.closest(".js-catalog-request-access")) {
      e.preventDefault();
      showSection("requests");
      return;
    }""",
    """  document.getElementById("catalogAssetDetail").addEventListener("click", (e) => {
    if (e.target.closest(".js-catalog-request-access")) {
      e.preventDefault();
      if (state.personaLens === "consumer" || state.personaLens === "compliance") {
        alert("Demo: Access requests are steward/ops — switch to Data steward lens or use Requests when that path is enabled.");
        return;
      }
      showSection("requests");
      return;
    }""",
    1,
)

text = text.replace(
    "  collapseAdminOpsNav();\n  renderHomeBdc();",
    INIT_WIRE + "\n  collapseAdminOpsNav();\n  renderHomeBdc();",
    1,
)

text = text.replace(
    '<div class="oms-main" id="omsMain" data-bdc-area="home">',
    '<div class="oms-main" id="omsMain" data-bdc-area="home" data-persona-lens="consumer">',
    1,
)

PATH.write_text(text, encoding="utf-8")
print("Patched", PATH)
