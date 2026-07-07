#!/usr/bin/env python3
"""Add restructure-aligned role + 360 bucket filter to navigator-only.html."""
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "navigator-only.html"
text = PATH.read_text(encoding="utf-8")

CSS = """
    /* Navigator lens — role + restructured 360 taxonomy (demo) */
    .nav-lens-panel {
      margin: 0 0 1rem;
      padding: 0.85rem 1rem;
      border-radius: 12px;
      border: 1px solid rgba(124, 77, 255, 0.22);
      background: linear-gradient(180deg, rgba(124, 77, 255, 0.05) 0%, #fff 100%);
    }
    .nav-lens-panel.is-concept {
      border-style: dashed;
    }
    .nav-lens-hd {
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      justify-content: space-between;
      gap: 0.35rem 0.75rem;
      margin-bottom: 0.65rem;
    }
    .nav-lens-hd h2 {
      margin: 0;
      font-size: 0.82rem;
      font-weight: 700;
      color: #4a148c;
    }
    .nav-lens-concept-tag {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #64748b;
    }
    .nav-lens-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.5rem 0.65rem;
      margin-bottom: 0.55rem;
    }
    .nav-lens-row:last-child { margin-bottom: 0; }
    .nav-lens-row label {
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: var(--oms-muted);
      min-width: 4.5rem;
    }
    .nav-lens-role-select {
      font-size: 13px;
      padding: 0.4rem 0.55rem;
      border-radius: 8px;
      border: 1px solid var(--oms-border);
      background: #fff;
      min-width: 14rem;
    }
    .nav-lens-buckets {
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
      flex: 1;
    }
    .nav-lens-bucket {
      font-family: inherit;
      font-size: 11px;
      font-weight: 600;
      padding: 0.28rem 0.55rem;
      border-radius: 999px;
      border: 1px solid var(--oms-border);
      background: #fff;
      color: var(--oms-text);
      cursor: pointer;
    }
    .nav-lens-bucket:hover {
      border-color: rgba(6, 182, 212, 0.5);
    }
    .nav-lens-bucket.is-on {
      border-color: #0891b2;
      background: rgba(6, 182, 212, 0.12);
      color: #0e7490;
    }
    .nav-lens-bucket[hidden] { display: none; }
    .nav-lens-banner {
      font-size: 12px;
      line-height: 1.45;
      color: var(--oms-muted);
      margin: 0.5rem 0 0;
      padding-top: 0.5rem;
      border-top: 1px dashed rgba(124, 77, 255, 0.2);
    }
    .nav-lens-banner strong { color: #5e35b1; }
    .nav-lens-reset {
      font-size: 11px;
      margin-left: auto;
    }
"""

HTML = """
        <div class="nav-lens-panel is-concept" id="navLensPanel" role="region" aria-label="Role and 360 taxonomy lens">
          <div class="nav-lens-hd">
            <h2>Discovery lens</h2>
            <span class="nav-lens-concept-tag">Concept · restructured 360 taxonomy</span>
          </div>
          <div class="nav-lens-row">
            <label for="navRoleSelect">I work as</label>
            <select id="navRoleSelect" class="nav-lens-role-select" aria-describedby="navLensBanner">
              <option value="analytics" selected>Business &amp; analytics</option>
              <option value="marketing">Marketing &amp; growth</option>
              <option value="product">Product &amp; experimentation</option>
              <option value="finance">Finance &amp; commercial ops</option>
              <option value="data-science">Data science &amp; ML</option>
              <option value="privacy">Privacy &amp; legal (read)</option>
            </select>
            <button type="button" class="btn-ghost nav-lens-reset" id="btnNavLensReset">Reset filters</button>
          </div>
          <div class="nav-lens-row">
            <label>360 bucket</label>
            <div class="nav-lens-buckets" id="navBucketChips" role="group" aria-label="Optional 360 taxonomy buckets"></div>
          </div>
          <p class="nav-lens-banner" id="navLensBanner" role="status"></p>
        </div>
"""

ASSET_TAGS = {
    '"id": "1",': '"id": "1",\n      navigatorRoles: ["analytics", "marketing"],\n      taxonomy360: ["marketing-audience", "platform-operational"],',
    '"id": "2",': '"id": "2",\n      navigatorRoles: ["analytics", "marketing"],\n      taxonomy360: ["marketing-audience"],',
    '"id": "3",': '"id": "3",\n      navigatorRoles: ["analytics", "finance", "privacy"],\n      taxonomy360: ["people-accounts"],',
    '"id": "4",': '"id": "4",\n      navigatorRoles: ["analytics", "product", "data-science"],\n      taxonomy360: ["experience-behavior", "content-catalog"],',
    '"id": "5",': '"id": "5",\n      navigatorRoles: ["marketing"],\n      taxonomy360: ["marketing-audience"],',
    '"id": "6",': '"id": "6",\n      navigatorRoles: ["finance", "analytics"],\n      taxonomy360: ["people-accounts", "commerce-merchandising"],',
    '"id": "7",': '"id": "7",\n      navigatorRoles: ["analytics", "product", "data-science"],\n      taxonomy360: ["experience-behavior"],',
    '"id": "8",': '"id": "8",\n      navigatorRoles: ["product", "analytics", "data-science"],\n      taxonomy360: ["experience-behavior"],',
}

JS = r'''
  const NAV_ROLES = {
    analytics: {
      label: "Business & analytics",
      banner: "Primary MVP lens — People, Content, and Experience buckets boosted; metadata search across all 360s.",
      search: "Find official metrics and governed tables…",
      buckets: ["people-accounts", "content-catalog", "experience-behavior", "marketing-audience", "commerce-merchandising", "regional-market"]
    },
    marketing: {
      label: "Marketing & growth",
      banner: "Marketing & Audience 360 — campaigns, acquisition, activation, ads.",
      search: "Find campaign, audience, and activation datasets…",
      buckets: ["marketing-audience", "commerce-merchandising", "regional-market"]
    },
    product: {
      label: "Product & experimentation",
      banner: "Experience & Behavior 360 — sessions, playback, experiments.",
      search: "Find session, playback, and experiment assets…",
      buckets: ["experience-behavior", "content-catalog", "people-accounts"]
    },
    finance: {
      label: "Finance & commercial ops",
      banner: "People & Accounts and Commerce buckets — payments, subscriber, revenue.",
      search: "Find subscriber, payments, and revenue assets…",
      buckets: ["people-accounts", "commerce-merchandising", "regional-market"]
    },
    "data-science": {
      label: "Data science & ML",
      banner: "Experience & Content buckets — model-ready tables and sports/content features.",
      search: "Find model-ready tables and features…",
      buckets: ["experience-behavior", "content-catalog", "people-accounts"]
    },
    privacy: {
      label: "Privacy & legal (read)",
      banner: "People & Accounts — classification and policy context on assets (not DSAR/tracker consoles).",
      search: "Audit identity and sensitivity on assets…",
      buckets: ["people-accounts", "regional-market"]
    }
  };

  const NAV_TAXONOMY_BUCKETS = [
    { id: "people-accounts", label: "People & Accounts", roles: ["analytics", "finance", "privacy", "product", "data-science"] },
    { id: "content-catalog", label: "Content & Catalog", roles: ["analytics", "product", "data-science"] },
    { id: "experience-behavior", label: "Experience & Behavior", roles: ["analytics", "product", "data-science"] },
    { id: "marketing-audience", label: "Marketing & Audience", roles: ["analytics", "marketing"] },
    { id: "commerce-merchandising", label: "Commerce & Merch", roles: ["analytics", "finance", "marketing"] },
    { id: "regional-market", label: "Regional & Market", roles: ["analytics", "marketing", "finance", "privacy"] },
    { id: "platform-operational", label: "Platform & Ops", roles: ["analytics", "finance"], omsHint: true }
  ];

  function navLensBucketLabels(ids) {
    return ids.map((id) => NAV_TAXONOMY_BUCKETS.find((b) => b.id === id)?.label || id).join(", ");
  }

  function personaFilterOk(a) {
    const role = state.navRole || "analytics";
    const roles = a.navigatorRoles || ["analytics"];
    if (!roles.includes(role)) return false;
    const selected = state.navBuckets || [];
    if (!selected.length) return true;
    const tax = a.taxonomy360 || [];
    return selected.some((b) => tax.includes(b));
  }

  function renderNavBucketChips() {
    const host = document.getElementById("navBucketChips");
    if (!host) return;
    const role = state.navRole || "analytics";
    host.innerHTML = "";
    NAV_TAXONOMY_BUCKETS.forEach((b) => {
      const show = b.roles.includes(role);
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "nav-lens-bucket" + (state.navBuckets.includes(b.id) ? " is-on" : "");
      btn.textContent = b.label;
      btn.dataset.bucket = b.id;
      btn.hidden = !show;
      btn.setAttribute("aria-pressed", state.navBuckets.includes(b.id) ? "true" : "false");
      btn.addEventListener("click", () => {
        const idx = state.navBuckets.indexOf(b.id);
        if (idx >= 0) state.navBuckets.splice(idx, 1);
        else state.navBuckets.push(b.id);
        applyNavLensUi();
      });
      host.appendChild(btn);
    });
  }

  function applyNavLensUi() {
    const role = state.navRole || "analytics";
    const meta = NAV_ROLES[role] || NAV_ROLES.analytics;
    const omsMain = document.getElementById("omsMain");
    if (omsMain) omsMain.setAttribute("data-nav-role", role);
    const sel = document.getElementById("navRoleSelect");
    if (sel && sel.value !== role) sel.value = role;
    const search = document.getElementById("globalSearch");
    if (search) search.placeholder = meta.search;
    const banner = document.getElementById("navLensBanner");
    if (banner) {
      let text = meta.banner;
      if (state.navBuckets.length) {
        text += " Filtering: " + navLensBucketLabels(state.navBuckets) + ".";
      }
      const platformOn = state.navBuckets.includes("platform-operational");
      if (platformOn || role === "finance") {
        text += " Platform & cost depth → OMS UI (demo).";
      }
      banner.innerHTML = "<strong>" + escapeHtml(meta.label) + ".</strong> " + escapeHtml(text);
    }
    renderNavBucketChips();
    state.page = 1;
    if (state.section === "catalog" || document.getElementById("tbody")) renderTable();
    if (state.section === "overview") {
      renderKpis();
      if (typeof renderPopularTables === "function") renderPopularTables();
    }
  }

  function setNavRole(role) {
    if (!NAV_ROLES[role]) role = "analytics";
    state.navRole = role;
    state.navBuckets = [];
    applyNavLensUi();
  }

  function resetNavLens() {
    setNavRole("analytics");
  }

'''

if ".nav-lens-panel" in text:
    print("Already patched")
    raise SystemExit(0)

if CSS.strip() not in text:
    text = text.replace("    .bdc-workflows-lede {", CSS + "\n    .bdc-workflows-lede {", 1)

if 'id="navLensPanel"' not in text:
    text = text.replace(
        """        <div class="bdc-hero">
          <h1>Data Navigator</h1>
        </div>

        <nav class="bdc-subnav" """,
        """        <div class="bdc-hero">
          <h1>Data Navigator</h1>
        </div>
""" + HTML + """
        <nav class="bdc-subnav" """,
        1,
    )

for needle, repl in ASSET_TAGS.items():
    if needle in text and "navigatorRoles" not in text[text.index(needle) : text.index(needle) + 120]:
        text = text.replace(needle, repl, 1)

text = text.replace(
    'const state = { page: 1, pageSize: 10, filters: {}, current: null',
    'const state = { page: 1, pageSize: 10, filters: {}, navRole: "analytics", navBuckets: [], current: null',
    1,
)

text = text.replace(
    """      catalogDataSourceOk(a)
    ];""",
    """      catalogDataSourceOk(a),
      personaFilterOk(a)
    ];""",
    1,
)

text = text.replace(
    """  function updateNavLensBanner(_section) {
    /* Lens banner removed from UI; kept as no-op for compatibility. */
  }""",
    """  function updateNavLensBanner(_section) {
    applyNavLensUi();
  }""" + JS,
    1,
)

INIT = """
  document.getElementById("navRoleSelect")?.addEventListener("change", (e) => setNavRole(e.target.value));
  document.getElementById("btnNavLensReset")?.addEventListener("click", resetNavLens);
  applyNavLensUi();

  collapseAdminOpsNav();"""

text = text.replace(
    "\n\n  collapseAdminOpsNav();\n  renderHomeBdc();",
    INIT + "\n  renderHomeBdc();",
    1,
)

PATH.write_text(text, encoding="utf-8")
print("Patched", PATH)
