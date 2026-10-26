# Status

_Last updated: 2026-10-26. Update at the end of every task and phase._

## Where we are

**Phase 2 (Primary Owner, part 1) is built and waiting for the user's design approval. Do not start Phase 3 until
the user has approved the look** (or sent changes; record them in DECISIONS.md first). Next after approval:
Phase 3, Primary Owner part 2 (PLAN.md section 5).

20 of 196 screens are built: the 9 sign-in screens and the 11 Primary Owner screens: Dashboard, Company Profile,
Product Catalogue, Product Details, Place Order, Order Builder, Order Confirmation, Order History, Order Details,
Inventory Overview, Inventory Item Details. All open by double-click from disk.

## What exists

- `assets/registry.js`: all 196 screens (ID, name, roles, menu section, kind, parent, description, built flag), plus
  each portal's organisation, portal name and each role's person. A screen is built when its ID is in `BUILT`.
- `assets/shell.js`: review bar; link helper `P.setLink` (a link is live only if the target is built and, within the
  portal, available to the signed-in role; otherwise it is inert, muted, with a reason). Use `data-link="PRI-ORD-02"`,
  `data-signin`, `data-directory`.
- `assets/chrome.js`: sidebar (menu sections from the registry, unbuilt items muted), top bar (breadcrumbs from the
  parent chain, search, notification bell, profile menu), mobile drawer, `<i data-icon="plus"></i>` icons.
- `assets/charts.js`: bars, line, donut from data attributes (month names written in full).
- `assets/app.css`: application layout and components (cards, KPI tiles, tables, filters, tabs, steps, track, swatches,
  product cards, quantity stepper, forms, alert, feed). `assets/styles.css`: tokens, buttons, chips, forms, review
  bar, directory, authentication.
- `docs/DATA.md`: products, prices, stock, people, number series, the order flow and formats. **Read before building.**
- `tools/author/`: Python helpers used to generate screen HTML (`data.py` shared data, `phase2a/b/c.py`). Not needed to
  run the prototype. `tools/inventory.mjs`: registry check and `docs/SCREEN-INVENTORY.md`. `tools/verify.js`: browser
  check over `file://` (needs Playwright).
- To add a screen: write it (copy a generated file), add its ID to `BUILT`, run `node tools/inventory.mjs` and
  `node tools/verify.js <folder> <ID prefix>`.

## Verified in Phase 2

`node tools/verify.js` passes for all 11 screens (and the Manager role versions of the shared ones) over `file://` at
1440, 1366 × 768 and 390 px. All 11 were looked at in screenshots at 1440; the dashboard, Place Order and Order
Builder were also looked at at 1366 and 390. Not yet checked in Firefox or Safari.

## Open items for the user (also at the design checkpoint)

1. **Manager ordering dead end.** Place Order is shared by Owner and Manager but Order Builder, Order Confirmation
   and Inventory Item Details are Owner only, so for the Manager those links are inert. Same shape as My Profile:
   tag the Manager onto them (no new screens)? Secondary Manager has the same gap.
2. Whether the look is approved (sidebar, cards, colours, swatches, charts). Record changes in DECISIONS.md.
3. In Order History every row opens Order Details for ORD-2026-10447 (documented in DATA.md).

## Next

Phase 3 after approval: Dealer Network, Dealer Details, Add Dealer Request, Secondary Sales Overview/Entry/History,
Invoices and Payments (4), Schemes (2), Sales Reports, Inventory Reports, Return Requests (2), Support (3), User
Management (3), My Profile, Notifications. Call the advisor before starting and after committing.
