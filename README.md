# Laminates Customer Portal: screen prototype

A static, clickable prototype of every proposed screen in the four portals (Company Administration, Primary
Distributor, Secondary Dealer, Tertiary Retailer), for stakeholder review and approval.

## Open it

Double-click **`index.html`**. No server, install or build step is needed, and every screen file also opens on its
own by double-click. Share it by zipping the whole folder.

1. `index.html` is the Screen Directory: four portal cards and the shared sign-in screens.
2. A portal card opens its directory: roles, screens grouped by menu section, each with ID, full name, role,
   description and a **Preview** button. Screens not built yet show a greyed Preview.
3. Every screen has a dark review bar on top: **Screen Directory** (back), the screen ID and full name, and
   **Previous** / **Next** for the role. Add `?review=off` to the address to hide the bar for clean screenshots.

All data on the screens is fictional.

## Folders

| Path | What |
|---|---|
| `index.html`, `directory/` | Screen Directory pages (drawn from the registry) |
| `screens/<portal>/` | One HTML file per screen |
| `assets/registry.js` | The list of every screen: ID, name, roles, menu section, description |
| `assets/styles.css`, `assets/fonts.css` | Design system; Inter embedded so pages work from disk |
| `assets/shell.js`, `assets/directory.js` | Review bar and directory pages |
| `docs/` | Plan, status, decisions, generated `SCREEN-INVENTORY.md` |
| `tools/inventory.mjs` | Optional (needs Node): checks the registry against the brief and rewrites the inventory |

Progress and next steps: `docs/STATUS.md`.
