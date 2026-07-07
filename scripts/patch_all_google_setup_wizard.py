#!/usr/bin/env python3
"""Patch All Google MCP setup_overlay.html for team install flow."""

from pathlib import Path

path = Path("/Users/jonathan.fong/Documents/AI Tools/all-google-mcp/all_google_mcp/setup_overlay.html")
text = path.read_text(encoding="utf-8")

start_marker = '    <div id="cursorGlobalBanner"'
end_marker = '    <footer class="nav-foot">'
start = text.index(start_marker)
end = text.index(end_marker)

new_body = r'''    <motion.div class="intro-callout">
      <strong>Google Cloud is already set up for you.</strong> You do not need console.cloud.google.com unless you are building your own OAuth app (see Advanced at the bottom).
    </div>

    <div id="cursorGlobalBanner" class="cursor-banner success" style="display:none" role="status" aria-live="polite"></div>
    <div id="cursorInstallErr" class="cursor-banner err" style="display:none" role="alert"></div>

    <div class="panel" id="panelStep1">
      <span class="step-badge">Step 1</span>
      <h2>Install the app</h2>
      <ol class="spaced compact">
        <li>Unzip <strong>All Google MCP.zip</strong> if you have not already.</li>
        <li>Drag <strong>All Google MCP.app</strong> into <strong>Applications</strong> (recommended).</li>
        <li>Open <strong>All Google MCP</strong> from Applications. This setup page opens in your browser.</li>
      </ol>
      <p class="step-note">You can also run the app from the unzipped folder; using Applications keeps paths stable for Cursor.</p>
    </div>

    <div class="panel" id="panelStep2">
      <span class="step-badge">Step 2</span>
      <h2>Sign in with Google</h2>
      <ol class="spaced compact">
        <li>Click <strong>Sign in with Google</strong> below.</li>
        <li>Choose the Google account you want Cursor to use (work or personal).</li>
        <li>Click <strong>Allow</strong> for all requested permissions (Drive, Docs, Sheets, Slides, Gmail).</li>
      </ol>
      <p class="step-note" id="credNote">Your personal session is saved as <strong>token.json</strong> on this Mac only — never share that file.</p>
      <div class="row">
        <button type="button" class="btn btn-primary" id="btnOAuth">Sign in with Google</button>
        <button type="button" class="btn btn-danger" id="btnRevokeToken">Sign out on this Mac</button>
      </div>
      <motion.div class="callout-revoke">
        <strong>Sign out on this Mac</strong> deletes <code>token.json</code> here. Use <strong>Sign in with Google</strong> again to reconnect.
      </div>
      <p id="oauthErr"></p>
    </div>

    <div class="panel" id="panelStep3">
      <span class="step-badge">Step 3</span>
      <h2>Connect Cursor</h2>
      <ol class="spaced compact">
        <li>After you are signed in, click <strong>Add to Cursor</strong> below (updates <code>~/.cursor/mcp.json</code>).</li>
        <li><strong>Quit Cursor completely</strong> (<kbd>⌘Q</kbd>) — not just close the window.</li>
        <li>Reopen Cursor. In <strong>Settings → MCP</strong>, confirm <strong>all-google-mcp</strong> is enabled.</li>
        <li>Start a new Agent chat and try a Google task (e.g. list a Drive file or read a Doc).</li>
      </ol>
      <p class="step-note" id="stdioNote"></p>
      <div class="row">
        <button type="button" class="btn btn-primary" id="btnInstallCursor">Add to Cursor</button>
        <button type="button" class="btn btn-ghost" id="btnCopyMcpSnippet">Copy MCP JSON snippet</button>
      </div>
    </div>

    <details class="advanced">
      <summary>Advanced — use your own Google Cloud project</summary>
      <div class="advanced-body">
        <div class="panel" style="margin-bottom:0.75rem">
          <h2>Enable APIs (your project)</h2>
          <p>In <a href="https://console.cloud.google.com/" target="_blank" rel="noopener">Google Cloud Console</a>, enable each API, then mark done (local checklist only).</p>
          <div class="api-list" id="apiList">
            <motion.div class="api-row" data-api="drive">
              <button type="button" class="btn btn-ghost open-btn" data-open="drive">Open Drive API</button>
              <div class="toggle-line">
                <label>
                  <input type="checkbox" class="api-toggle" data-api="drive" aria-label="Drive API enabled"/>
                  <span class="switch-pill"></span>
                  <span>I enabled it</span>
                </label>
                <span class="flag-on" title="Marked enabled">✓</span>
              </div>
            </div>
            <div class="api-row" data-api="sheets">
              <button type="button" class="btn btn-ghost open-btn" data-open="sheets">Open Sheets API</button>
              <div class="toggle-line">
                <label>
                  <input type="checkbox" class="api-toggle" data-api="sheets" aria-label="Sheets API enabled"/>
                  <span class="switch-pill"></span>
                  <span>I enabled it</span>
                </label>
                <span class="flag-on">✓</span>
              </div>
            </div>
            <div class="api-row" data-api="docs">
              <button type="button" class="btn btn-ghost open-btn" data-open="docs">Open Docs API</button>
              <div class="toggle-line">
                <label>
                  <input type="checkbox" class="api-toggle" data-api="docs" aria-label="Docs API enabled"/>
                  <span class="switch-pill"></span>
                  <span>I enabled it</span>
                </label>
                <span class="flag-on">✓</span>
              </div>
            </div>
            <div class="api-row" data-api="slides">
              <button type="button" class="btn btn-ghost open-btn" data-open="slides">Open Slides API</button>
              <div class="toggle-line">
                <label>
                  <input type="checkbox" class="api-toggle" data-api="slides" aria-label="Slides API enabled"/>
                  <span class="switch-pill"></span>
                  <span>I enabled it</span>
                </label>
                <span class="flag-on">✓</span>
              </div>
            </div>
            <div class="api-row" data-api="gmail">
              <button type="button" class="btn btn-ghost open-btn" data-open="gmail">Open Gmail API</button>
              <div class="toggle-line">
                <label>
                  <input type="checkbox" class="api-toggle" data-api="gmail" aria-label="Gmail API enabled"/>
                  <span class="switch-pill"></span>
                  <span>I enabled it</span>
                </label>
                <span class="flag-on">✓</span>
              </div>
            </div>
          </div>
        </div>
        <div class="panel" style="margin-bottom:0">
          <h2>OAuth consent &amp; Desktop client</h2>
          <ol class="spaced compact">
            <li><strong>OAuth consent screen</strong> — name the app, add developer contact email, save.</li>
            <li><strong>Credentials</strong> → <strong>Create credentials</strong> → <strong>OAuth client ID</strong> → <strong>Desktop app</strong> → download JSON.</li>
            <li>Save as <strong>credentials.json</strong> at:
              <div class="pathbox js-cred-path"></div>
            </li>
          </ol>
          <div class="row">
            <button type="button" class="btn btn-ghost" id="btnConsent">Open OAuth consent</button>
            <button type="button" class="btn btn-ghost" id="btnCreds">Open Credentials</button>
            <button type="button" class="btn btn-ghost" id="btnOpenFolder">Reveal support folder</button>
            <button type="button" class="btn btn-ghost" id="btnCopyCredPath">Copy credentials path</button>
          </div>
        </div>
      </div>
    </details>

'''

# Fix accidental motion.div typos in template
new_body = new_body.replace("<motion.div", "<div").replace("</motion.div>", "</div>")

new_js = r'''    function applyStepPanels(s) {
      const p1 = document.getElementById('panelStep1');
      const p2 = document.getElementById('panelStep2');
      const p3 = document.getElementById('panelStep3');
      if (p1) p1.classList.add('panel-done');
      if (p2) p2.classList.toggle('panel-done', !!s.tokenPresent);
      if (p3) p3.classList.toggle('panel-done', !!s.cursorMcpConfigured);
      const btnCursor = document.getElementById('btnInstallCursor');
      if (btnCursor) btnCursor.disabled = !s.tokenPresent;
      const note = document.getElementById('credNote');
      if (note && s.credentialsAutoInstalled) {
        note.textContent = 'App credentials were installed automatically. Your sign-in is saved as token.json on this Mac only.';
      }
      const stdio = document.getElementById('stdioNote');
      if (stdio && s.bundledStdioPath) {
        stdio.textContent = 'Cursor will use: ' + s.bundledStdioPath;
      }
    }
'''

# Replace body section
text = text[:start] + new_body + text[end:]

# Patch renderStatus to call applyStepPanels and improve pills
old_render_end = "      applyApiFlags(s.apiEnabledFlags);\n      const oe = document.getElementById('oauthErr');"
new_render_mid = """      applyApiFlags(s.apiEnabledFlags);
      applyStepPanels(s);
      if (s.cursorMcpConfigured) {
        const cur = document.createElement('span');
        cur.className = 'pill';
        cur.textContent = 'Cursor connected';
        el.appendChild(cur);
      }
      const oe = document.getElementById('oauthErr');"""
text = text.replace(old_render_end, new_render_mid, 1)

# Insert applyStepPanels before renderStatus
text = text.replace("    function renderStatus(s) {", new_js + "\n    function renderStatus(s) {", 1)

# Update status pills for bundled creds
text = text.replace(
      "c.textContent = s.credentialsPresent ? 'credentials.json found' : 'credentials.json missing';",
      "c.textContent = s.credentialsPresent\n        ? (s.credentialsBundledInApp ? 'app ready' : 'credentials.json found')\n        : 'app not configured — contact the person who shared this zip';",
      1,
)

# Add btn handlers before refresh();
insert_before = "    document.getElementById('btnConsent').onclick"
handlers = """    document.getElementById('btnInstallCursor').onclick = async () => {
      const btn = document.getElementById('btnInstallCursor');
      btn.disabled = true;
      await runCursorMcpInstall();
      await refresh();
      btn.disabled = !(await fetchJson('/api/status')).tokenPresent;
    };
    document.getElementById('btnCopyMcpSnippet').onclick = async () => {
      const s = await fetchJson('/api/status');
      await navigator.clipboard.writeText(s.mcpSnippet || '');
    };
    """
if "btnInstallCursor" not in text.split("document.getElementById('btnConsent')")[0]:
    text = text.replace(insert_before, handlers + insert_before, 1)

path.write_text(text, encoding="utf-8")
print("Patched", path)

PYEOF
