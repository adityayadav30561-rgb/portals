# Status

_Last updated: 2026-10-26. Update at the end of every task and phase._

## Where we are

**Phase 1 (Foundations) is done. Next: Phase 2, Primary Owner part 1** (PLAN.md section 5): the application
sidebar and top bar, then Owner Dashboard, Company Profile, Product Catalogue, Product Details, Place Order, Order
Builder, Order Confirmation, Order History, Order Details, Inventory Overview, Inventory Item Details. **The user
approves the look after this phase**, before the rest is built.

9 of 194 screens are built (the shared sign-in screens). Everything opens by double-click from disk.

## What exists

- `assets/registry.js`: all 194 screens (ID, full name parts, roles, menu section, kind, parent, description,
  built flag). A screen is marked built by adding its ID to `BUILT` at the bottom of the file.
- `assets/shell.js`: the review bar, plus link helpers any screen can use: `data-link="PRI-ORD-02"`,
  `data-signin="primary"` (role dashboard once built, else the portal directory), `data-directory="index"`,
  `data-toggle-password="<input id>"`. Role comes from `?role=MGR`, default the screen's first role.
- `assets/directory.js`, `index.html`, `directory/*.html`: Screen Directory with search and a built-only filter.
- `assets/styles.css`: tokens, buttons, chips, forms, cards, tables, review bar, directory, authentication. The
  application chrome (sidebar, top bar, page header, KPI cards, charts) is **not** written yet: Phase 2.
- `assets/fonts.css`: Inter embedded as base64 (Firefox blocks fonts from a parent folder over `file://`).
- `tools/inventory.mjs`: `node tools/inventory.mjs` checks the registry against the brief's 11 role lists (with the
  approved merges and additions), pinned IDs, unique IDs and files, banned abbreviations and browser storage in
  built screens, and rewrites `docs/SCREEN-INVENTORY.md`. Run it at the end of every phase.
- Screen files live in `screens/<portal id>/<slug>.html` (portal ids: company, primary, secondary, tertiary,
  authentication). A screen needs `<body data-screen="PRI-ORD-02">`, the stylesheet links and the two scripts
  (copy `screens/authentication/company-login.html` for the pattern).

## Verified in Phase 1

Opened over `file://` in Chromium at 1440, 1366 × 768 and 390 px: no console errors, no horizontal scroll, Inter
loaded, directory search, built-only filter, Preview, Previous and Next, back link and `?review=off` working.
Not yet checked in Firefox or Safari.

## Open questions for the user (DECISIONS.md)

1. Company roles have no My Profile screen (the top bar has a profile menu): add one (+1 screen)?
2. Tertiary Payments Overview has nothing to open: add Payment Details (Tertiary 40, total 195)?
3. Screen names: three-part ("Primary Customer — Owner — Order Details", used now) or the brief's two-part
   examples ("Primary Customer — Product Catalogue")? One-line change in `registry.js`.

## Next

Phase 2: write the application chrome (sidebar from the registry grouped by menu section, top bar with
breadcrumbs, search, notifications bell, user and role, profile menu; page header; KPI cards; table patterns; a
real laminate swatch component for product images), build the 11 Primary Owner screens, then ask the user to
approve the design. Call the advisor before starting and after committing.
