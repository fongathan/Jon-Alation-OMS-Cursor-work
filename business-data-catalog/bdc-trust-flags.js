/**
 * Demo trust flags: endorse (green) vs deprecated (red), with user + reason.
 * Delegated events on root — safe when tbody is replaced.
 */
(function () {
  const DEFAULT_USER = "you@company.com";

  function syncAttr(card, user) {
    const endorse = card.querySelector(".trust-flag--endorse");
    const deprecate = card.querySelector(".trust-flag--deprecate");
    const reasonEl = card.querySelector(".trust-reason-input");
    const attr = card.querySelector(".trust-attribution");
    if (!attr) return;
    const e = endorse && endorse.getAttribute("aria-pressed") === "true";
    const d = deprecate && deprecate.getAttribute("aria-pressed") === "true";
    const txt = reasonEl && reasonEl.value ? reasonEl.value.trim() : "";
    if (!e && !d && !txt) {
      attr.textContent = "";
      return;
    }
    const kind = e ? "Endorsed" : d ? "Flagged deprecated" : "Note";
    attr.textContent =
      kind + " by " + user + " · " + new Date().toLocaleString() + (txt ? " · “" + txt + "”" : "");
  }

  function resetStrip(strip) {
    if (!strip) return;
    strip.querySelectorAll(".trust-card").forEach((card) => {
      card.querySelectorAll(".trust-flag").forEach((b) => b.setAttribute("aria-pressed", "false"));
      const r = card.querySelector(".trust-reason-input");
      if (r) r.value = "";
      const a = card.querySelector(".trust-attribution");
      if (a) a.textContent = "";
    });
  }

  function wire(root, user) {
    if (!root) return;
    const u = user || DEFAULT_USER;
    if (root.dataset.trustWired) return;
    root.dataset.trustWired = "1";
    root.addEventListener("click", (e) => {
      const btn = e.target.closest(".trust-flag");
      if (!btn || !root.contains(btn)) return;
      const card = btn.closest("[data-trust-scope]");
      if (!card || !root.contains(card)) return;
      const endorse = card.querySelector(".trust-flag--endorse");
      const deprecate = card.querySelector(".trust-flag--deprecate");
      if (!endorse || !deprecate) return;
      if (btn === endorse) {
        const on = endorse.getAttribute("aria-pressed") !== "true";
        endorse.setAttribute("aria-pressed", on ? "true" : "false");
        if (on) deprecate.setAttribute("aria-pressed", "false");
      } else {
        const on = deprecate.getAttribute("aria-pressed") !== "true";
        deprecate.setAttribute("aria-pressed", on ? "true" : "false");
        if (on) endorse.setAttribute("aria-pressed", "false");
      }
      syncAttr(card, u);
    });
    root.addEventListener("input", (e) => {
      const inp = e.target.closest(".trust-reason-input");
      if (!inp || !root.contains(inp)) return;
      const card = inp.closest("[data-trust-scope]");
      if (card) syncAttr(card, u);
    });
  }

  function columnTrustCell(colName) {
    var safe = String(colName)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;");
    return (
      '<td class="trust-col-cell">' +
      '<div class="trust-card trust-card--compact" data-trust-scope="column" data-col-name="' +
      safe +
      '">' +
      '<div class="trust-toggles">' +
      '<button type="button" class="trust-flag trust-flag--endorse trust-mini" aria-pressed="false" aria-label="Endorse column" title="Endorse">✓</button>' +
      '<button type="button" class="trust-flag trust-flag--deprecate trust-mini" aria-pressed="false" aria-label="Mark column deprecated" title="Deprecated">⚑</button>' +
      "</div>" +
      '<input type="text" class="trust-reason-input trust-reason-input--sm" placeholder="Why" aria-label="Reason for column flag" />' +
      '<span class="trust-attribution trust-attribution-sm"></span>' +
      "</div>" +
      "</td>"
    );
  }

  window.BdcTrustFlags = {
    wire: wire,
    resetStrip: resetStrip,
    columnTrustCell: columnTrustCell,
    DEFAULT_USER: DEFAULT_USER
  };
})();
