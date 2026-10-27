# Laminates Customer Portal: screen prototype

A static, clickable prototype of every proposed screen in the four portals (Company Administration, Primary
Distributor, Secondary Dealer, Tertiary Retailer), for stakeholder review and approval.

## Open it

Double-click **`index.html`**. No server, install or build step is needed, and every screen file also opens on its
own by double-click. Share it by zipping the whole folder. All 196 screens are built.

1. `index.html` is the **Screen Directory**: four portal cards (Company Administration, Primary Distributor,
   Secondary Dealer, Tertiary Retailer) and the shared sign-in screens.
2. A portal card opens its directory: roles, screens grouped by menu section, each with ID, full name, role,
   description and a **Preview** button.
3. The **Screen Map** (`screen-map.html`, also reached from the "Screen map" button on the directory pages) shows
   the whole prototype as a tree: Sign In, Portal Selection, the four portals, their roles and menu sections, down
   to every screen. Search, "Built only" and a detail level (Roles, Sections, Screens) narrow it.
4. Every screen has a dark **review bar** on top: **Screen Directory** (back), the screen ID and full name, and
   **Previous** / **Next** for the role. Add `?review=off` to the address to hide the bar for clean screenshots.
5. Inside a portal, use the sidebar, the top bar (search, notifications, profile menu) and the links on each
   screen like a real application. A link that leads to a screen the signed-in role cannot open is greyed out.
6. **Switching roles:** a screen used by several roles opens as the first role that has it. Add `?role=` and the
   role code to the address to see it as another role, for example `order-details.html?role=MGR` (Manager).
   The directory's Preview buttons do this for you. Role codes: OWN (Owner), MGR (Manager), ACC (Accountant),
   SAL (Sales Manager), OPS (Operations Manager), SLS (Sales Executive), PUR (Inventory and Purchasing Executive),
   ADM (Super Admin).

All data on the screens is fictional. It is a prototype of screens only: there is no sign-in, storage or business
logic, and the buttons that would save or send something do nothing.

## Folders

| Path | What |
|---|---|
| `index.html`, `directory/` | Screen Directory pages (drawn from the registry) |
| `screen-map.html` | Screen Map: a tree from Sign In through the portals and roles to every screen, built and planned (drawn from the registry) |
| `screens/<portal>/` | One HTML file per screen |
| `assets/registry.js` | The list of every screen: ID, name, roles, menu section, description |
| `assets/styles.css`, `assets/fonts.css` | Design system; Inter embedded so pages work from disk |
| `assets/shell.js`, `assets/directory.js` | Review bar and directory pages |
| `docs/` | Plan, status, decisions, generated `SCREEN-INVENTORY.md` |
| `assets/app.css`, `assets/chrome.js`, `assets/charts.js` | Application layout, sidebar and top bar, charts |
| `tools/inventory.mjs` | Optional (needs Node): checks the registry against the brief and rewrites the inventory |
| `tools/verify.js` | Optional (needs Playwright): opens every built screen from disk at three sizes and checks it |
| `tools/author/` | Optional (Python): helpers used to generate screen HTML |

Progress and next steps: `docs/STATUS.md`.
