/**
 * Cookie consent: persists to both document.cookie and localStorage (key: cookie_prefs).
 * Include this script before your consent UI logic, or call writeStoredPrefs after Accept.
 */
(function () {
  var COOKIE_PREFS_KEY = "cookie_prefs";

  function getCookie(name) {
    var match = document.cookie.match(
      new RegExp("(?:^|; )" + name.replace(/[.+?^${}()|[\]\\]/g, "\\$&") + "=([^;]*)")
    );
    return match ? decodeURIComponent(match[1]) : "";
  }

  function setCookie(name, value, days) {
    var maxAge = days * 24 * 60 * 60;
    var base =
      name +
      "=" +
      encodeURIComponent(value) +
      ";path=/;max-age=" +
      maxAge +
      ";SameSite=Lax";
    if (typeof location !== "undefined" && location.protocol === "https:") {
      base += ";Secure";
    }
    document.cookie = base;
  }

  function readStoredPrefs() {
    var fromCookie = getCookie(COOKIE_PREFS_KEY);
    if (fromCookie) {
      return fromCookie;
    }
    try {
      if (typeof localStorage !== "undefined") {
        var fromLs = localStorage.getItem(COOKIE_PREFS_KEY);
        if (fromLs) {
          return fromLs;
        }
      }
    } catch (err) {}
    return "";
  }

  function writeStoredPrefs(value) {
    setCookie(COOKIE_PREFS_KEY, value, 180);
    try {
      if (typeof localStorage !== "undefined") {
        localStorage.setItem(COOKIE_PREFS_KEY, value);
      }
    } catch (err) {}
  }

  window.MeetingHubStorage = {
    COOKIE_PREFS_KEY: COOKIE_PREFS_KEY,
    readStoredPrefs: readStoredPrefs,
    writeStoredPrefs: writeStoredPrefs,
  };

  /**
   * Wire cookie bar + modal: [data-cookie-bar], [data-cookie-accept], [data-cookie-reject],
   * [data-cookie-open-settings], [data-cookie-modal], [data-cookie-close], [data-cookie-save],
   * toggles [data-cookie-switch="analytics|marketing"].
   */
  function initCookieConsent() {
    var bar = document.querySelector("[data-cookie-bar]");
    if (!bar) {
      return;
    }

    var modal = document.querySelector("[data-cookie-modal]");
    var btnAccept = document.querySelector("[data-cookie-accept]");
    var rejectButtons = document.querySelectorAll("[data-cookie-reject]");
    var btnSettings = document.querySelector("[data-cookie-open-settings]");
    var btnSave = document.querySelector("[data-cookie-save]");
    var btnClose = document.querySelector("[data-cookie-close]");
    var swAnalytics = document.querySelector('[data-cookie-switch="analytics"]');
    var swMarketing = document.querySelector('[data-cookie-switch="marketing"]');

    var stored = readStoredPrefs();
    if (stored) {
      try {
        if (typeof localStorage !== "undefined") {
          localStorage.setItem(COOKIE_PREFS_KEY, stored);
        }
      } catch (err) {}
    }

    if (!stored) {
      bar.removeAttribute("hidden");
    } else {
      try {
        var parsed = JSON.parse(stored);
        if (swAnalytics) {
          swAnalytics.checked = !!parsed.analytics;
        }
        if (swMarketing) {
          swMarketing.checked = !!parsed.marketing;
        }
      } catch (err) {}
    }

    function closeModal() {
      if (!modal) {
        return;
      }
      modal.classList.remove("is-open");
      modal.setAttribute("hidden", "");
      modal.setAttribute("inert", "");
      if (btnSettings) {
        btnSettings.focus();
      }
    }

    function openModal() {
      if (!modal) {
        return;
      }
      modal.removeAttribute("hidden");
      modal.removeAttribute("inert");
      modal.classList.add("is-open");
      requestAnimationFrame(function () {
        var focusTarget = modal.querySelector("button, [href], input");
        if (focusTarget) {
          focusTarget.focus();
        }
      });
    }

    function savePrefs(necessary, analytics, marketing) {
      var payload = {
        necessary: true,
        analytics: analytics,
        marketing: marketing,
      };
      writeStoredPrefs(JSON.stringify(payload));
      bar.setAttribute("hidden", "");
      closeModal();
    }

    if (btnAccept) {
      btnAccept.addEventListener("click", function () {
        if (swAnalytics) {
          swAnalytics.checked = true;
        }
        if (swMarketing) {
          swMarketing.checked = true;
        }
        savePrefs(true, true, true);
      });
    }

    for (var r = 0; r < rejectButtons.length; r++) {
      rejectButtons[r].addEventListener("click", function () {
        if (swAnalytics) {
          swAnalytics.checked = false;
        }
        if (swMarketing) {
          swMarketing.checked = false;
        }
        savePrefs(true, false, false);
      });
    }

    if (btnSettings) {
      btnSettings.addEventListener("click", function () {
        openModal();
      });
    }

    if (btnClose) {
      btnClose.addEventListener("click", function () {
        closeModal();
      });
    }

    if (btnSave) {
      btnSave.addEventListener("click", function () {
        var a = swAnalytics ? swAnalytics.checked : false;
        var m = swMarketing ? swMarketing.checked : false;
        savePrefs(true, a, m);
      });
    }

    if (modal) {
      modal.addEventListener("click", function (e) {
        if (e.target === modal) {
          closeModal();
        }
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCookieConsent);
  } else {
    initCookieConsent();
  }
})();
