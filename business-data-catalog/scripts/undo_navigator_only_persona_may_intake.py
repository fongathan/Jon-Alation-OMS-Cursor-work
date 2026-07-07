#!/usr/bin/env python3
"""Revert May intake persona patch on navigator-only.html."""
import re
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "navigator-only.html"
text = PATH.read_text(encoding="utf-8")

# --- JavaScript: remove persona module ---
text = re.sub(
    r"\n  const PERSONA_LENS_META = \{[\s\S]*?\n  function setPersonaLens\(lens, section\) \{[\s\S]*?\n  \}\n",
    "\n",
    text,
    count=1,
)

text = text.replace(
    "  function updateNavLensBanner(_section) {\n    applyPersonaLensUi();\n  }",
    "  function updateNavLensBanner(_section) {\n    /* Lens banner removed from UI; kept as no-op for compatibility. */\n  }",
)

text = text.replace(
    ', personaLens: "consumer",',
    ",",
)

text = re.sub(r"\n      audience: \"(?:consumer|both|internal)\",", "", text)

text = text.replace(
    """      catalogDataSourceOk(a),
      personaLensOk(a)
    ];""",
    """      catalogDataSourceOk(a)
    ];""",
)

text = text.replace(
    """      <a href="#requests" class="btn-primary catalog-request-access js-catalog-request-access" role="button" data-persona-action="steward">Request access</a>
    `;
    mountAlignmentStrip("catalogAlignmentMount", a);""",
    """      <a href="#requests" class="btn-primary catalog-request-access js-catalog-request-access" role="button">Request access</a>
    `;""",
)

text = text.replace(
    """    refreshCatalogCollaborationUI();
    setCatalogPanelActionsEnabled(true);
    mountAlignmentStrip("catalogAlignmentMount", a);
    applyPersonaLensUi();
  }

  function closeCatalogAssetDetail() {""",
    """    refreshCatalogCollaborationUI();
    setCatalogPanelActionsEnabled(true);
  }

  function closeCatalogAssetDetail() {""",
)

text = text.replace(
    """    mountAlignmentStrip("catalogAlignmentMount", null);
    renderTable();
  }

  function openDrawer(id) {""",
    """    renderTable();
  }

  function openDrawer(id) {""",
)

text = text.replace(
    """    renderBdcAssetSocial();
    mountAlignmentStrip("bdcAlignmentMount", ASSETS[1]);
    applyPersonaLensUi();
    document.getElementById("panel-bdc-snowflake-list").classList.add("section-hidden");""",
    """    renderBdcAssetSocial();
    document.getElementById("panel-bdc-snowflake-list").classList.add("section-hidden");""",
)

text = text.replace(
    """      if (state.personaLens === "consumer" || state.personaLens === "compliance") {
        alert("Demo: Access requests are steward/ops — switch to Data steward lens or use Requests when that path is enabled.");
        return;
      }
      showSection("requests");""",
    """      showSection("requests");""",
)

# --- Init wire ---
text = re.sub(
    r"\n\n  document\.getElementById\(\"navPersonaLensSelect\"\)[\s\S]*?applyPersonaLensUi\(\);\n\n  collapseAdminOpsNav\(\);",
    "\n\n  collapseAdminOpsNav();",
    text,
    count=1,
)

# --- HTML / CSS ---
text = text.replace(
    '<div class="oms-main" id="omsMain" data-bdc-area="home" data-persona-lens="consumer">',
    '<div class="oms-main" id="omsMain" data-bdc-area="home">',
)

text = text.replace(
    '["btnCatalogFavorite", "btnCatalogShare", "btnCatalogSuggestEdit", "btnCatalogSeeFullDetails", "btnCatalogOpenInOms", "btnCatalogDetailHide",',
    '["btnCatalogFavorite", "btnCatalogShare", "btnCatalogSuggestEdit", "btnCatalogSeeFullDetails", "btnCatalogDetailHide",',
)

text = text.replace(
    """          <div id="bdcAlignmentMount" class="nav-alignment-mount"></div>
          <p class="bdc-detail-lede" id="bdcDetailLede" style="margin:0 0 0.75rem;font-size:12px;color:var(--oms-muted);max-width:80ch;">Governed business view on OMS — stewardship, definitions, and policy context. SQL and deep technical truth live in OMS UI.</p>

          <div class="asset-detail-tabs" role="tablist" id="bdcDetailTabs">
            <button type="button" role="tab" aria-selected="true" data-bdc-tab="overview">Overview</button>
            <button type="button" role="tab" aria-selected="false" data-bdc-tab="sql" data-persona-tab="steward">SQL</button>
            <button type="button" role="tab" aria-selected="false" data-bdc-tab="lineage" data-persona-tab="steward">Lineage</button>
            <button type="button" class="btn-ghost" id="btnBdcOpenInOms" style="margin-left:auto;font-size:12px;">Open in OMS</button>
          </div>""",
    """          <p style="margin:0 0 0.75rem;font-size:12px;color:var(--oms-muted);max-width:80ch;">BDC-on-top view: operational / storage / profiling technical blocks are hidden. Focus is stewardship, policy, SQL, samples, and business column context.</p>

          <div class="asset-detail-tabs" role="tablist" id="bdcDetailTabs">
            <button type="button" role="tab" aria-selected="true" data-bdc-tab="overview">Overview</button>
            <button type="button" role="tab" aria-selected="false" data-bdc-tab="sql">SQL</button>
            <button type="button" role="tab" aria-selected="false" data-bdc-tab="lineage">Lineage</button>
          </div>""",
)

text = text.replace(
    """                    <button type="button" class="btn-ghost" id="btnCatalogSeeFullDetails" title="Open full-page asset view" aria-label="See full asset details on a dedicated page" disabled>See full details</button>
                    <button type="button" class="btn-ghost" id="btnCatalogOpenInOms" title="Technical lineage, SQL, and operational metadata" disabled>Open in OMS</button>""",
    """                    <button type="button" class="btn-ghost" id="btnCatalogSeeFullDetails" title="Open full-page asset view" aria-label="See full asset details on a dedicated page" disabled>See full details</button>""",
)

text = text.replace(
    """                  <button type="button" role="tab" aria-selected="false" data-tab="technical" data-persona-tab="steward">Technical</button>
                  <button type="button" role="tab" aria-selected="false" data-tab="schema" data-persona-tab="steward">Schema</button>
                  <button type="button" role="tab" aria-selected="false" data-tab="dictionary" data-persona-tab="steward">Dictionary</button>
                  <button type="button" role="tab" aria-selected="false" data-tab="audit" data-persona-tab="steward">Audit</button>""",
    """                  <button type="button" role="tab" aria-selected="false" data-tab="technical">Technical</button>
                  <button type="button" role="tab" aria-selected="false" data-tab="schema">Schema</button>
                  <button type="button" role="tab" aria-selected="false" data-tab="dictionary">Dictionary</button>
                  <button type="button" role="tab" aria-selected="false" data-tab="audit">Audit</button>""",
)

text = text.replace(
    """                <div class="catalog-asset-detail-summary is-placeholder" id="catalogDetailSummary" aria-label="Asset summary"></div>
                <div id="catalogAlignmentMount" class="nav-alignment-mount" hidden></div>
                <div class="drawer-tabs" role="tablist" id="catalogDetailTabs">""",
    """                <div class="catalog-asset-detail-summary is-placeholder" id="catalogDetailSummary" aria-label="Asset summary"></div>
                <div class="drawer-tabs" role="tablist" id="catalogDetailTabs">""",
)

text = text.replace(
    """            <div class="kpi-card" id="kpiRequestsCard">
              <div class="lbl">Open access requests</div>
              <div class="val" id="kpiRequests">3</div>
            </div>""",
    """            <div class="kpi-card">
              <div class="lbl">Open access requests</div>
              <div class="val" id="kpiRequests">3</div>
            </div>""",
)

text = text.replace(
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
)

text = text.replace(
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
    """        <div class="bdc-hero">
          <h1>Data Navigator</h1>
        </div>

        <nav class="bdc-subnav" aria-label="Catalog and operations" id="bdcSubnav">""",
)

css_start = "    /* May intake — persona lens & program boundaries */"
if css_start in text:
    idx = text.index(css_start)
    end_idx = text.index("    .bdc-workflows-lede {", idx)
    text = text[:idx] + text[end_idx:]

# Remove data-persona-lens CSS rules if any left in style block
text = re.sub(
    r"\n    #omsMain\[data-persona-lens[^\]]*\][^\n]*\{[^}]+\}\n",
    "\n",
    text,
)

leftovers = ["navPersonaEntry", "PERSONA_LENS", "personaLens", "nav-alignment", "navPersonaLens", "btnCatalogOpenInOms", "btnBdcOpenInOms", "nav-boundary-lede"]
found = [k for k in leftovers if k in text]
if found:
    raise SystemExit(f"Undo incomplete — still contains: {found}")

PATH.write_text(text, encoding="utf-8")
print("Reverted", PATH)
