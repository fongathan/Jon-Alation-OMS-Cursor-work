/**
 * Microsoft Graph / Entra ID configuration
 *
 * Full instructions: see SETUP.md
 *
 * 1. Register an app at https://portal.azure.com → Microsoft Entra ID → App registrations → New registration
 * 2. Set redirect URI: Single-page application → http://localhost:5500 (must match your dev server)
 * 3. Add API permissions: Microsoft Graph → Delegated → Calendars.Read, User.Read
 * 4. Copy Application (client) ID and Directory (tenant) ID here
 */
window.MEETING_HUB_CONFIG = {
  clientId: 'ca1c1554-aab8-410c-b058-711ead4a3df2',            // Application (client) ID from Azure
  tenantId: '56b731a8-a2ac-4c32-bf6b-616810e913c6',                     // 'common' = any org/personal, or your tenant ID for single-tenant
  redirectUri: 'http://localhost:5500',    // Must match exactly what you set in Azure (run: npm start)
};
