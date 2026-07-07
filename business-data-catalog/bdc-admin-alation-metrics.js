/**
 * Alation-style metrics (midnight dashboard parity) inside BDC admin host.
 * Requires: Chart.js 4.x, window.__BDC_ALATION_ADMIN_HTML__ (from bdc-alation-admin-template.js)
 * or fetchable partials/bdc-alation-admin.html when served over HTTP.
 */
(function () {
  "use strict";

  function $(root, name) {
    return root.querySelector('[data-bdc-ad="' + name + '"]');
  }

  var PALETTE = {
    accent: "#7c4dff",
    teal: "#00acc1",
    green: "#0d8050",
    amber: "#f59e0b",
    blue: "#1a73e8",
    purple: "#9c27b0",
    orange: "#e65100",
    red: "#e53935",
    pink: "#ec407a"
  };
  var GRID_COLOR = "rgba(92, 99, 112, 0.12)";
  var TICK_COLOR = "#5c6370";

  function monthLabels(n) {
    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var labels = [];
    var d = new Date(2026, 2, 1);
    for (var i = n - 1; i >= 0; i--) {
      var dd = new Date(d.getFullYear(), d.getMonth() - i, 1);
      labels.push(months[dd.getMonth()] + " '" + String(dd.getFullYear()).slice(2));
    }
    return labels;
  }

  var SAMPLE = {
    meta: { generated_at: new Date().toISOString(), period_days: 90, source: "Compose-style export (demo)" },
    summary: {
      mau: 1247,
      dau_avg: 412,
      new_users: 183,
      retention_pct: 89,
      searches_total: 38400,
      page_views_total: 94000,
      endorsed_pct: 73,
      description_coverage_pct: 61,
      steward_pct: 84,
      articles_total: 6218,
      terms_total: 2841,
      deprecations: 312,
      total_tables: 93400,
      search_ctr_pct: 67,
      pages_per_session: 4.2,
      policies_active: 1043,
      pii_classified_pct: 97,
      policy_violations_open: 48
    },
    trend_90d: (function () {
      var n = 90;
      var dates = [];
      var i;
      var d = new Date(2026, 2, 12);
      for (i = 0; i < n; i++) {
        var dd = new Date(d);
        dd.setDate(dd.getDate() - n + i + 1);
        dates.push(dd.toISOString().slice(0, 10));
      }
      var searches = dates.map(function (_, i) {
        return Math.round(360 + 80 * Math.sin(i / 7) + i * 1.5 + Math.random() * 60);
      });
      var curations = dates.map(function (_, i) {
        return Math.round(80 + 30 * Math.sin(i / 9 + 1) + i * 0.4 + Math.random() * 20);
      });
      var page_views = dates.map(function (_, i) {
        return Math.round(900 + 200 * Math.sin(i / 6) + i * 2.5 + Math.random() * 100);
      });
      dates.forEach(function (ds, idx) {
        var day = new Date(ds).getDay();
        if (day === 0 || day === 6) searches[idx] = Math.round(searches[idx] * 0.55);
      });
      return { dates: dates, searches: searches, curations: curations, page_views: page_views };
    })(),
    dau_mau_12m: {
      months: monthLabels(12),
      mau: [820, 850, 890, 940, 980, 1020, 1050, 1110, 1150, 1180, 1210, 1247],
      dau: [280, 295, 305, 320, 338, 350, 368, 385, 398, 404, 408, 412]
    },
    top_users: [
      { display_name: "Jenn Yu", email: "jenn.yu@disney.com", endorsements: 84, deprecations: 2, total_flags: 86 },
      { display_name: "Mark Dienger", email: "mark.l.dienger@disney.com", endorsements: 62, deprecations: 1, total_flags: 63 },
      { display_name: "Sam Nasir", email: "sameul.nasir@disney.com", endorsements: 48, deprecations: 0, total_flags: 48 },
      { display_name: "Carolina Manning", email: "carolina.manning@disney.com", endorsements: 41, deprecations: 0, total_flags: 41 },
      { display_name: "Elmer Alpuche", email: "elmer.alpuche.-nd@disney.com", endorsements: 38, deprecations: 4, total_flags: 42 },
      { display_name: "Matt Mittelmann", email: "matthew.j.mittelmann@disney.com", endorsements: 29, deprecations: 0, total_flags: 29 },
      { display_name: "Lucas Wang", email: "lucas.wang2@disney.com", endorsements: 22, deprecations: 0, total_flags: 22 },
      { display_name: "Paul Fischer", email: "paul.fischer@disney.com", endorsements: 18, deprecations: 9, total_flags: 27 }
    ],
    curation_monthly: {
      months: monthLabels(12),
      endorsed: [42, 55, 68, 80, 91, 88, 104, 118, 132, 148, 161, 184],
      deprecated: [12, 18, 22, 28, 31, 25, 34, 40, 52, 58, 61, 68],
      warned: [8, 10, 14, 17, 19, 18, 22, 25, 31, 36, 39, 44]
    },
    catalog_coverage: {
      description_pct: 61,
      steward_pct: 74,
      endorsed_pct: 73,
      term_tagged_pct: 48,
      bi_linked_pct: 55,
      query_titled_pct: 39,
      elt_doc_pct: 32
    },
    amp_terms: [
      { term: "ACCOUNT_ID", tables: 4983 },
      { term: "STREAMING_SERVICE", tables: 985 },
      { term: "USER_ID", tables: 984 },
      { term: "ENTITY_TYPE", tables: 974 },
      { term: "ACCOUNT_HOME_COUNTRY", tables: 754 },
      { term: "SUBSCRIPTION_ID", tables: 649 },
      { term: "BUSINESS_DATE", tables: 412 },
      { term: "PROGRAM_TYPE", tables: 411 }
    ],
    search_daily: null,
    top_searches: [
      { query: "audience watch fact", count: 1847 },
      { query: "subscriber dim", count: 1623 },
      { query: "glimpse pageviews", count: 1412 },
      { query: "payment fact", count: 1198 },
      { query: "identity mapping", count: 1044 },
      { query: "content watch", count: 923 },
      { query: "ad delivery", count: 842 },
      { query: "segment targeting", count: 771 },
      { query: "browse attribution", count: 704 },
      { query: "account management", count: 658 }
    ],
    top_visited: [
      { name: "audience_watch_fact_vw", type: "table", views: 3214 },
      { name: "glimpsev2_pageviews", type: "table", views: 2891 },
      { name: "audience_service_subscriber_dim_vw", type: "table", views: 2647 },
      { name: "payment_event_fact_vw", type: "table", views: 2318 },
      { name: "identity_unified_mapping_dim_vw", type: "table", views: 1872 },
      { name: "Audience Data Guide", type: "article", views: 1649 },
      { name: "glimpsev2_fact_user_journey", type: "table", views: 1503 },
      { name: "browse_playback_attribution_fact_vw", type: "table", views: 1388 }
    ],
    governance_feed: [
      { type: "ENDORSEMENT", user: "Mark Dienger", object: "audience_watch_fact_vw", datasource: "Audience", date: "2026-01-28" },
      { type: "ENDORSEMENT", user: "Jenn Yu", object: "glimpsev2_fact_user_journey", datasource: "Browse", date: "2026-02-05" },
      { type: "DEPRECATION", user: "Peter Yu", object: "dimension_campaign", datasource: "Ad Tech", date: "2025-10-22" },
      { type: "ENDORSEMENT", user: "Elmer Alpuche", object: "conf_disney_gatewaygo_segments_decoded_snapshot", datasource: "Identity", date: "2025-10-24" },
      { type: "WARNING", user: "Rocio Jensen", object: "listenfirst_dss_match", datasource: "Marketing", date: "2025-08-22" },
      { type: "ENDORSEMENT", user: "Carolina Manning", object: "payment_event_fact_vw", datasource: "Commerce", date: "2026-01-26" },
      { type: "ENDORSEMENT", user: "Matt Mittelmann", object: "identity_unified_mapping_dim_vw", datasource: "Identity", date: "2026-02-03" },
      { type: "DEPRECATION", user: "Xingpeng Xiao", object: "registered_user", datasource: "Identity", date: "2026-01-14" }
    ],
    teams_mau: [
      { label: "Data Science & Analytics", pct: 82, val: 342, color: "var(--bdc-adm-accent, #7c4dff)" },
      { label: "Product & Content", pct: 65, val: 271, color: "#0097a7" },
      { label: "Engineering / Data Platform", pct: 55, val: 229, color: "#1a73e8" },
      { label: "Advertising / Ad Sales", pct: 44, val: 184, color: "#9c27b0" },
      { label: "Finance & Strategy", pct: 34, val: 140, color: "#f59e0b" },
      { label: "Marketing & Growth", pct: 27, val: 113, color: "#e65100" }
    ],
    domains_use: [
      { label: "Audience & Subscriber", pct: 90, val: "18.2K", color: "#0097a7" },
      { label: "Browse & Discovery", pct: 78, val: "15.7K", color: "#1a73e8" },
      { label: "Commerce & Payments", pct: 61, val: "12.3K", color: "#0d8050" },
      { label: "Advertising & Targeting", pct: 53, val: "10.6K", color: "#9c27b0" },
      { label: "Content & Playback", pct: 44, val: "8.9K", color: "#f59e0b" },
      { label: "Identity & Segmentation", pct: 36, val: "7.2K", color: "#e65100" }
    ],
    steward_by_domain: [
      { label: "Browse & Discovery", pct: 96 },
      { label: "Audience & Subscriber", pct: 93 },
      { label: "Commerce & Payments", pct: 91 },
      { label: "Identity & Segmentation", pct: 88 },
      { label: "Advertising & Targeting", pct: 79 },
      { label: "Content & Playback", pct: 71 },
      { label: "Marketing & MMM", pct: 64 },
      { label: "Engineering / Infra", pct: 52 }
    ]
  };

  SAMPLE.search_daily = {
    dates: SAMPLE.trend_90d.dates,
    searches: SAMPLE.trend_90d.searches
  };

  var CHARTS = {};
  function destroyChart(id) {
    if (CHARTS[id]) {
      CHARTS[id].destroy();
      delete CHARTS[id];
    }
  }

  function fmt(n) {
    if (n == null || isNaN(n)) return "—";
    n = Number(n);
    if (n >= 1e6) return (n / 1e6).toFixed(1) + "M";
    if (n >= 1e3) return (n / 1e3).toFixed(1) + "K";
    return String(Math.round(n));
  }

  function setTxt(root, name, val) {
    var el = $(root, name);
    if (el) el.textContent = val;
  }

  function hexToRgb(hex) {
    var r = parseInt(hex.slice(1, 3), 16),
      g = parseInt(hex.slice(3, 5), 16),
      b = parseInt(hex.slice(5, 7), 16);
    return "rgb(" + r + "," + g + "," + b + ")";
  }

  function linGradient(ctx, hex, a0, a1) {
    a0 = a0 == null ? 0.22 : a0;
    a1 = a1 == null ? 0 : a1;
    var g = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);
    var base = hexToRgb(hex);
    g.addColorStop(0, base.replace("rgb", "rgba").replace(")", "," + a0 + ")"));
    g.addColorStop(1, base.replace("rgb", "rgba").replace(")", "," + a1 + ")"));
    return g;
  }

  function applyMeta(root, data) {
    var m = data.meta || {};
    if (m.period_days != null) setTxt(root, "meta-period", "Last " + m.period_days + " days");
    if (m.source) setTxt(root, "meta-source", m.source);
    if (m.generated_at) {
      try {
        setTxt(root, "meta-refreshed", new Date(m.generated_at).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" }));
      } catch (e) {
        setTxt(root, "meta-refreshed", String(m.generated_at));
      }
    }
    var badge = $(root, "data-badge");
    if (badge) {
      badge.textContent = "● Sample data (demo)";
      badge.classList.add("bdc-adm-badge--demo");
    }
  }

  function applyKpis(root, data) {
    var s = data.summary || {};
    var c = data.catalog_coverage || {};
    setTxt(root, "kpi-mau", fmt(s.mau));
    setTxt(root, "kpi-searches", fmt(s.searches_total));
    setTxt(root, "kpi-endorsed", (s.endorsed_pct != null ? s.endorsed_pct : 73) + "%");
    setTxt(root, "kpi-coverage", (s.description_coverage_pct != null ? s.description_coverage_pct : 61) + "%");
    setTxt(root, "kpi-articles", fmt(s.articles_total));
    setTxt(root, "kpi-terms", fmt(s.terms_total));
    setTxt(root, "kpi-views", fmt(s.page_views_total));
    setTxt(root, "kpi-deprecations", fmt(s.deprecations));

    setTxt(root, "kpi-a-mau", fmt(s.mau));
    setTxt(root, "kpi-dau", fmt(s.dau_avg));
    setTxt(root, "kpi-new-users", fmt(s.new_users));
    setTxt(root, "kpi-retention", (s.retention_pct != null ? s.retention_pct : 89) + "%");

    var endorsedTables = s.total_tables ? Math.round((s.endorsed_pct / 100) * s.total_tables) : 68200;
    setTxt(root, "kpi-c-endorsed", fmt(endorsedTables));
    setTxt(root, "kpi-c-deprecations", fmt(s.deprecations));
    setTxt(root, "kpi-c-articles", fmt(s.articles_total));
    setTxt(root, "kpi-c-terms", fmt(s.terms_total));

    setTxt(root, "kpi-d-searches", fmt(s.searches_total));
    setTxt(root, "kpi-d-ctr", (s.search_ctr_pct != null ? s.search_ctr_pct : 67) + "%");
    setTxt(root, "kpi-d-views", fmt(s.page_views_total));
    setTxt(root, "kpi-d-pages", String(s.pages_per_session != null ? s.pages_per_session : 4.2));

    setTxt(root, "kpi-g-steward", (s.steward_pct != null ? s.steward_pct : 84) + "%");
    setTxt(root, "kpi-g-policies", fmt(s.policies_active != null ? s.policies_active : 1043));
    setTxt(root, "kpi-g-pii", (s.pii_classified_pct != null ? s.pii_classified_pct : 97) + "%");
    setTxt(root, "kpi-g-violations", fmt(s.policy_violations_open != null ? s.policy_violations_open : 48));
  }

  function renderRankBlock(items, numPrefix) {
    return items
      .map(function (row, i) {
        var num = numPrefix ? '<div class="bdc-adm-rank-num">' + String(i + 1).padStart(2, "0") + "</div>" : "";
        return (
          '<div class="bdc-adm-rank-item">' +
          num +
          '<div class="bdc-adm-rank-bar-wrap"><div class="bdc-adm-rank-lbl">' +
          row.label +
          '</div><div class="bdc-adm-rank-track"><div class="bdc-adm-rank-fill" style="width:' +
          row.pct +
          "%;background:" +
          row.color +
          '"></div></div></div><div class="bdc-adm-rank-val">' +
          row.val +
          "</div></div>"
        );
      })
      .join("");
  }

  function renderRankLists(root, data) {
    var teams = $(root, "rank-teams");
    if (teams && data.teams_mau) {
      teams.innerHTML = renderRankBlock(
        data.teams_mau.map(function (t) {
          return { label: t.label, pct: t.pct, val: String(t.val), color: t.color };
        }),
        true
      );
    }
    var dom = $(root, "rank-domains");
    if (dom && data.domains_use) {
      dom.innerHTML = renderRankBlock(data.domains_use, true);
    }

    var roleBars = $(root, "role-bars");
    if (roleBars) {
      roleBars.innerHTML = renderRankBlock(
        [
          { label: "Data Consumers (search/browse)", pct: 58, val: "726", color: PALETTE.accent },
          { label: "Data Stewards (endorse/curate)", pct: 28, val: "349", color: PALETTE.teal },
          { label: "Catalog Authors (docs/articles)", pct: 14, val: "172", color: PALETTE.purple }
        ],
        false
      );
    }

    var st = $(root, "search-type-bars");
    if (st) {
      st.innerHTML = renderRankBlock(
        [
          { label: "Tables / Views", pct: 72, val: "72%", color: PALETTE.accent },
          { label: "Glossary Terms", pct: 14, val: "14%", color: PALETTE.teal },
          { label: "Articles / Docs", pct: 9, val: "9%", color: PALETTE.purple },
          { label: "Queries / Reports", pct: 5, val: "5%", color: PALETTE.amber }
        ],
        false
      );
    }
  }

  function renderProgressList(el, rows) {
    if (!el) return;
    el.innerHTML = rows
      .map(function (r) {
        return (
          '<div class="bdc-adm-progress-item"><div class="bdc-adm-progress-hd"><span>' +
          r.label +
          '</span><span>' +
          r.pct +
          '%</span></div><div class="bdc-adm-progress-track"><div class="bdc-adm-progress-fill" style="width:' +
          r.pct +
          "%;background:" +
          r.color +
          '"></div></div></div>'
        );
      })
      .join("");
  }

  function renderCoverageAndSteward(root, data) {
    var c = data.catalog_coverage || {};
    renderProgressList($(root, "coverage-list"), [
      { label: "Tables with description", pct: c.description_pct || 61, color: PALETTE.accent },
      { label: "Tables with an owner/steward", pct: c.steward_pct || 74, color: PALETTE.teal },
      { label: "Tables endorsed (trusted)", pct: c.endorsed_pct || 73, color: PALETTE.green },
      { label: "Columns with glossary term tags", pct: c.term_tagged_pct || 48, color: PALETTE.blue },
      { label: "BI Reports linked to sources", pct: c.bi_linked_pct || 55, color: PALETTE.purple },
      { label: "Queries with saved titles", pct: c.query_titled_pct || 39, color: PALETTE.amber },
      { label: "ELT models fully documented", pct: c.elt_doc_pct || 32, color: PALETTE.orange }
    ]);

    var cols = [PALETTE.green, PALETTE.green, PALETTE.teal, PALETTE.teal, PALETTE.accent, PALETTE.blue, PALETTE.amber, PALETTE.orange];
    renderProgressList(
      $(root, "steward-domains"),
      (data.steward_by_domain || []).map(function (d, i) {
        return { label: d.label, pct: d.pct, color: cols[i % cols.length] };
      })
    );
  }

  function renderTables(root, data) {
    var tb = $(root, "tbody-top-users");
    if (tb) {
      tb.innerHTML = (data.top_users || [])
        .slice(0, 10)
        .map(function (u, i) {
          var domain = (u.email || "").split("@")[1] || "—";
          return (
            "<tr><td>" +
            String(i + 1).padStart(2, "0") +
            "</td><td><strong>" +
            (u.display_name || u.email || "—") +
            "</strong></td><td>" +
            domain +
            "</td><td>" +
            (u.endorsements ?? 0) +
            "</td><td>" +
            (u.deprecations ?? 0) +
            '</td><td>—</td><td><span class="bdc-adm-pill">' +
            fmt(u.total_flags) +
            "</span></td></tr>"
          );
        })
        .join("");
    }

    var cur = $(root, "tbody-curators");
    if (cur) {
      cur.innerHTML = (data.top_users || [])
        .slice(0, 8)
        .map(function (u) {
          return (
            "<tr><td><strong>" +
            (u.display_name || u.email) +
            "</strong></td><td>" +
            (u.endorsements ?? 0) +
            "</td><td>" +
            (u.deprecations ?? 0) +
            "</td><td>" +
            (u.total_flags ?? 0) +
            "</td></tr>"
          );
        })
        .join("");
    }

    var ts = $(root, "tbody-searches");
    if (ts) {
      ts.innerHTML = (data.top_searches || [])
        .map(function (s, i) {
          return "<tr><td>" + (i + 1) + "</td><td>" + s.query + "</td><td>" + fmt(s.count) + "</td><td>—</td></tr>";
        })
        .join("");
    }

    var tv = $(root, "tbody-visited");
    if (tv) {
      tv.innerHTML = (data.top_visited || [])
        .map(function (v, i) {
          return (
            "<tr><td>" +
            (i + 1) +
            "</td><td class=\"bdc-adm-mono\">" +
            v.name +
            "</td><td><span class=\"bdc-adm-tag\">" +
            v.type +
            "</span></td><td>" +
            fmt(v.views) +
            "</td></tr>"
          );
        })
        .join("");
    }
  }

  function renderAmpTerms(root, data) {
    var el = $(root, "list-amp-terms");
    if (!el || !data.amp_terms || !data.amp_terms.length) return;
    var max = data.amp_terms[0].tables || 1;
    var colors = [PALETTE.accent, PALETTE.teal, PALETTE.blue, PALETTE.green, PALETTE.purple, PALETTE.amber, PALETTE.orange, PALETTE.pink];
    el.innerHTML = data.amp_terms
      .map(function (t, i) {
        var w = Math.round((t.tables * 100) / max);
        return (
          '<div class="bdc-adm-rank-item"><div class="bdc-adm-rank-bar-wrap"><div class="bdc-adm-rank-lbl bdc-adm-mono">' +
          t.term +
          '</div><div class="bdc-adm-rank-track"><div class="bdc-adm-rank-fill" style="width:' +
          w +
          "%;background:" +
          colors[i % colors.length] +
          '"></div></div></div><div class="bdc-adm-rank-val">' +
          fmt(t.tables) +
          "</div></div>"
        );
      })
      .join("");
  }

  function renderGovernanceFeed(root, data) {
    var el = $(root, "governance-feed");
    if (!el) return;
    var dot = { ENDORSEMENT: PALETTE.green, DEPRECATION: PALETTE.red, WARNING: PALETTE.amber };
    var verb = { ENDORSEMENT: "endorsed", DEPRECATION: "deprecated", WARNING: "flagged with Warning" };
    el.innerHTML = (data.governance_feed || [])
      .map(function (e) {
        return (
          '<div class="bdc-adm-tl-item"><div class="bdc-adm-tl-dot" style="background:' +
          (dot[e.type] || "#94a3b8") +
          '"></div><div class="bdc-adm-tl-body"><div class="bdc-adm-tl-title"><span class="bdc-adm-mono">' +
          e.object +
          "</span> <strong>" +
          (verb[e.type] || e.type) +
          "</strong> by " +
          e.user +
          '</div><div class="bdc-adm-tl-meta">' +
          (e.datasource || "Catalog") +
          " · " +
          e.date +
          "</div></div></div>"
        );
      })
      .join("");
  }

  function buildHeatmap(root) {
    var container = $(root, "activityHeatmap");
    if (!container) return;
    container.innerHTML = "";
    var d, w, cell, intensity, rnd, ageWeeks, isRecent;
    for (d = 0; d < 7; d++) {
      for (w = 0; w < 52; w++) {
        ageWeeks = 51 - w;
        isRecent = ageWeeks < 13;
        rnd = Math.random();
        if (rnd < 0.15) intensity = 0;
        else if (rnd < 0.35) intensity = 1;
        else if (rnd < 0.6) intensity = 2;
        else if (rnd < 0.82) intensity = 3;
        else intensity = 4;
        if (d === 5 || d === 6) intensity = Math.max(0, intensity - 2);
        if (isRecent) intensity = Math.min(4, intensity + 1);
        cell = document.createElement("div");
        cell.className = "bdc-adm-hm-cell hm-" + intensity;
        container.appendChild(cell);
      }
    }
  }

  function renderTrendChart(root, data) {
    destroyChart("trendChart");
    var trend = data.trend_90d || {};
    var raw = trend.dates || [];
    var labels = raw.map(function (d, i) {
      return i % 15 === 0 ? d.slice(5).replace("-", "/") : "";
    });
    var canvas = $(root, "trendChart");
    if (!canvas || !window.Chart) return;
    var ctx = canvas.getContext("2d");
    CHARTS.trendChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Page Views",
            data: trend.page_views || [],
            borderColor: PALETTE.teal,
            backgroundColor: linGradient(ctx, PALETTE.teal, 0.12),
            fill: true,
            tension: 0.4,
            borderWidth: 1.5,
            pointRadius: 0,
            yAxisID: "y2"
          },
          {
            label: "Searches",
            data: trend.searches || [],
            borderColor: PALETTE.accent,
            backgroundColor: linGradient(ctx, PALETTE.accent, 0.18),
            fill: true,
            tension: 0.4,
            borderWidth: 2,
            pointRadius: 0,
            yAxisID: "y"
          },
          {
            label: "Curations",
            data: trend.curations || [],
            borderColor: PALETTE.green,
            backgroundColor: "transparent",
            tension: 0.4,
            borderWidth: 1.5,
            pointRadius: 0,
            borderDash: [4, 3],
            yAxisID: "y"
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: { legend: { display: true, position: "top", labels: { boxWidth: 10, padding: 12 } } },
        scales: {
          x: { grid: { color: GRID_COLOR }, ticks: { color: TICK_COLOR, maxRotation: 0 } },
          y: { position: "left", grid: { color: GRID_COLOR }, ticks: { color: TICK_COLOR, callback: function (v) { return fmt(v); } } },
          y2: { position: "right", grid: { display: false }, ticks: { color: TICK_COLOR, callback: function (v) { return fmt(v); } } }
        }
      }
    });
  }

  function renderDauMauChart(root, data) {
    destroyChart("dauMauChart");
    var dm = data.dau_mau_12m || {};
    var canvas = $(root, "dauMauChart");
    if (!canvas || !window.Chart) return;
    var ctx = canvas.getContext("2d");
    CHARTS.dauMauChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: dm.months || [],
        datasets: [
          {
            label: "MAU",
            data: dm.mau || [],
            borderColor: PALETTE.accent,
            backgroundColor: linGradient(ctx, PALETTE.accent, 0.2),
            fill: true,
            tension: 0.4,
            borderWidth: 2,
            pointRadius: 3,
            pointBackgroundColor: PALETTE.accent
          },
          {
            label: "DAU (avg)",
            data: dm.dau || [],
            borderColor: PALETTE.teal,
            backgroundColor: "transparent",
            tension: 0.4,
            borderWidth: 1.5,
            pointRadius: 3,
            pointBackgroundColor: PALETTE.teal
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: { legend: { display: true, position: "top", labels: { boxWidth: 10, padding: 10 } } },
        scales: {
          x: { grid: { color: GRID_COLOR }, ticks: { color: TICK_COLOR, maxRotation: 30 } },
          y: { grid: { color: GRID_COLOR }, ticks: { color: TICK_COLOR }, min: 0 }
        }
      }
    });
  }

  function renderCurationChart(root, data) {
    destroyChart("curationChart");
    var cm = data.curation_monthly || {};
    var canvas = $(root, "curationChart");
    if (!canvas || !window.Chart) return;
    var ctx = canvas.getContext("2d");
    CHARTS.curationChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: cm.months || [],
        datasets: [
          { label: "Endorsed", data: cm.endorsed || [], backgroundColor: PALETTE.green, borderRadius: 3 },
          { label: "Deprecated", data: cm.deprecated || [], backgroundColor: PALETTE.red, borderRadius: 3 },
          { label: "Warned", data: cm.warned || [], backgroundColor: PALETTE.amber, borderRadius: 3 }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index" },
        plugins: { legend: { display: true, position: "top", labels: { boxWidth: 10, padding: 10 } } },
        scales: {
          x: { grid: { display: false }, ticks: { color: TICK_COLOR, maxRotation: 30 } },
          y: { grid: { color: GRID_COLOR }, ticks: { color: TICK_COLOR } }
        }
      }
    });
  }

  function renderSearchChart(root, data) {
    destroyChart("searchChart");
    var sd = data.search_daily || {};
    var raw = sd.dates || [];
    var labels = raw.map(function (d, i) {
      return i % 15 === 0 ? d.slice(5).replace("-", "/") : "";
    });
    var canvas = $(root, "searchChart");
    if (!canvas || !window.Chart) return;
    var ctx = canvas.getContext("2d");
    CHARTS.searchChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Search Sessions",
            data: sd.searches || [],
            backgroundColor: "rgba(124, 77, 255, 0.35)",
            borderColor: PALETTE.accent,
            borderWidth: 1,
            borderRadius: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { color: TICK_COLOR, maxRotation: 0 } },
          y: { grid: { color: GRID_COLOR }, ticks: { color: TICK_COLOR, callback: function (v) { return fmt(v); } } }
        }
      }
    });
  }

  function initStaticDonutsAndBars(root) {
    if (!window.Chart) return;
    var c;

    c = $(root, "purposeDonut");
    if (c) {
      destroyChart("purposeDonut");
      CHARTS.purposeDonut = new Chart(c.getContext("2d"), {
        type: "doughnut",
        data: {
          labels: ["Data Discovery", "Curation & Quality", "Governance", "Collaboration"],
          datasets: [{ data: [42, 28, 18, 12], backgroundColor: [PALETTE.accent, PALETTE.teal, PALETTE.amber, PALETTE.purple], borderWidth: 0, hoverOffset: 6 }]
        },
        options: { responsive: true, maintainAspectRatio: false, cutout: "70%", plugins: { legend: { position: "right", labels: { boxWidth: 10, padding: 10 } } } }
      });
    }

    c = $(root, "roleChart");
    if (c) {
      destroyChart("roleChart");
      CHARTS.roleChart = new Chart(c.getContext("2d"), {
        type: "doughnut",
        data: {
          labels: ["Consumers", "Stewards", "Authors"],
          datasets: [{ data: [726, 349, 172], backgroundColor: [PALETTE.accent, PALETTE.teal, PALETTE.purple], borderWidth: 0, hoverOffset: 5 }]
        },
        options: { responsive: true, maintainAspectRatio: false, cutout: "65%", plugins: { legend: { position: "right", labels: { boxWidth: 10, padding: 8 } } } }
      });
    }

    c = $(root, "searchTypeChart");
    if (c) {
      destroyChart("searchTypeChart");
      CHARTS.searchTypeChart = new Chart(c.getContext("2d"), {
        type: "doughnut",
        data: {
          labels: ["Tables/Views", "Glossary Terms", "Articles", "Queries/Reports"],
          datasets: [{ data: [72, 14, 9, 5], backgroundColor: [PALETTE.accent, PALETTE.teal, PALETTE.purple, PALETTE.amber], borderWidth: 0, hoverOffset: 5 }]
        },
        options: { responsive: true, maintainAspectRatio: false, cutout: "65%", plugins: { legend: { position: "right", labels: { boxWidth: 10, padding: 8 } } } }
      });
    }

    c = $(root, "trustChart");
    if (c) {
      destroyChart("trustChart");
      CHARTS.trustChart = new Chart(c.getContext("2d"), {
        type: "bar",
        data: {
          labels: ["Audience", "Browse", "Commerce", "Advertising", "Content", "Identity", "Marketing", "Infra"],
          datasets: [
            { label: "Endorsed", data: [94, 91, 88, 62, 71, 80, 58, 43], backgroundColor: PALETTE.green, borderRadius: 4, stack: "a" },
            { label: "Warning", data: [3, 4, 6, 14, 12, 9, 18, 22], backgroundColor: PALETTE.amber, borderRadius: 4, stack: "a" },
            { label: "Deprecated", data: [2, 4, 5, 20, 16, 10, 22, 28], backgroundColor: PALETTE.red, borderRadius: 4, stack: "a" },
            { label: "Uncurated", data: [1, 1, 1, 4, 1, 1, 2, 7], backgroundColor: "rgba(92, 99, 112, 0.35)", borderRadius: 4, stack: "a" }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: "y",
          interaction: { mode: "index" },
          plugins: { legend: { display: true, position: "top", labels: { boxWidth: 10, padding: 8 } } },
          scales: {
            x: { stacked: true, grid: { color: GRID_COLOR }, ticks: { color: TICK_COLOR, callback: function (v) { return v + "%"; } }, max: 100 },
            y: { stacked: true, grid: { display: false }, ticks: { color: TICK_COLOR } }
          }
        }
      });
    }

    c = $(root, "dqChart");
    if (c) {
      destroyChart("dqChart");
      var labels = ["Audience", "Browse", "Commerce", "Advertising", "Content", "Identity"];
      CHARTS.dqChart = new Chart(c.getContext("2d"), {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            { label: "DQ Checks Passing", data: [248, 194, 172, 134, 118, 89], backgroundColor: PALETTE.green, borderRadius: 4 },
            { label: "DQ Checks Failing", data: [12, 8, 16, 22, 18, 14], backgroundColor: PALETTE.red, borderRadius: 4 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: "index" },
          plugins: { legend: { display: true, position: "top", labels: { boxWidth: 10, padding: 8 } } },
          scales: {
            x: { grid: { display: false }, ticks: { color: TICK_COLOR, maxRotation: 30 } },
            y: { grid: { color: GRID_COLOR }, ticks: { color: TICK_COLOR } }
          }
        }
      });
    }
  }

  function renderAllCharts(root, data) {
    renderTrendChart(root, data);
    renderDauMauChart(root, data);
    renderCurationChart(root, data);
    renderSearchChart(root, data);
  }

  function wireNav(root) {
    var titles = {
      summary: "Executive Summary",
      adoption: "User Adoption",
      curation: "Content & Curation",
      discovery: "Search & Discovery",
      governance: "Governance & Compliance"
    };
    root.querySelectorAll("[data-bdc-ad-nav]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var page = btn.getAttribute("data-bdc-ad-nav");
        root.querySelectorAll("[data-bdc-ad-nav]").forEach(function (b) {
          b.classList.toggle("active", b === btn);
        });
        root.querySelectorAll("[data-bdc-ad-page]").forEach(function (sec) {
          var on = sec.getAttribute("data-bdc-ad-page") === page;
          sec.classList.toggle("active", on);
          sec.hidden = !on;
        });
        var tt = $(root, "topbar-title");
        if (tt) tt.textContent = titles[page] || page;
      });
    });
  }

  function wirePeriod(root) {
    root.querySelectorAll("[data-bdc-ad-period]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        root.querySelectorAll("[data-bdc-ad-period]").forEach(function (b) {
          b.classList.toggle("active", b === btn);
        });
      });
    });
  }

  function doInit(root, data) {
    data = data || SAMPLE;
    if (typeof Chart !== "undefined") {
      Chart.defaults.color = TICK_COLOR;
      Chart.defaults.borderColor = GRID_COLOR;
      Chart.defaults.font.family = "'DM Sans', system-ui, sans-serif";
      Chart.defaults.font.size = 11;
    }

    applyMeta(root, data);
    applyKpis(root, data);
    renderRankLists(root, data);
    renderCoverageAndSteward(root, data);
    renderTables(root, data);
    renderAmpTerms(root, data);
    renderGovernanceFeed(root, data);
    buildHeatmap(root);
    wireNav(root);
    wirePeriod(root);

    if (typeof Chart !== "undefined") {
      renderAllCharts(root, data);
      initStaticDonutsAndBars(root);
    }
  }

  function mount(host) {
    if (!host || host.dataset.bdcAlationMounted) return;
    host.dataset.bdcAlationMounted = "1";

    function finish(html) {
      host.innerHTML = html;
      var innerRoot = host.querySelector("[data-bdc-alation-root]") || host;
      doInit(innerRoot, SAMPLE);
      host.querySelector("#btnAdminExport")?.addEventListener("click", function () {
        alert("Demo: export catalog analytics as CSV.");
      });
      requestAnimationFrame(function () {
        Object.keys(CHARTS).forEach(function (k) {
          try {
            CHARTS[k].resize();
          } catch (e) {}
        });
      });
    }

    if (window.__BDC_ALATION_ADMIN_HTML__) {
      finish(window.__BDC_ALATION_ADMIN_HTML__);
      return;
    }

    fetch("partials/bdc-alation-admin.html")
      .then(function (r) {
        return r.ok ? r.text() : Promise.reject();
      })
      .then(finish)
      .catch(function () {
        host.innerHTML =
          '<p class="bdc-adm-err">Could not load analytics layout. Open this page via a local web server (so <code>partials/bdc-alation-admin.html</code> and <code>bdc-alation-admin-template.js</code> load), or include <code>bdc-alation-admin-template.js</code> before <code>bdc-admin-alation-metrics.js</code>.</p>';
      });
  }

  window.BdcAlationAdmin = { mount: mount, SAMPLE: SAMPLE };
})();
