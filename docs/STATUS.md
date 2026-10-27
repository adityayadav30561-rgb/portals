# Status

_Last updated: 2026-10-27. Update at the end of every task and phase._

## Where we are

**Phase 13 (Company Sales Manager and Operations Manager) is built and verified: 18 screens, plus the Sales Manager's tag on the Customer Approval Queue. All 196 screens are built** (9 sign-in, Primary 52, Secondary 45, Tertiary 40, Company 50). Open item 11 was answered "do whats recommended by you" (2026-10-27) and is applied: the Sales Manager sees the Customer Approval Queue (`ADM SAL` in the registry, in its original place; `chrome.js` orders the Sales Manager's menu groups; `tools/inventory.mjs` lists it as an approved extra role tag), and Sales Order Overview has a Confirm Order card for ORD-2026-10482 (DECISIONS.md, "Answered 2026-10-27"). The Phase 12 review was taken as approval.
**What remains is Phase 14, review and hand-over** (PLAN.md section 5): links between related screens (the shared-screen gaps listed below), a full responsive pass, README, screen inventory and counts, optional hosting for stakeholders.

Phase 13 screens (generators `tools/author/phase13a.py` and `13b`; folder `screens/company/`): Sales Manager: Dashboard (`sales-manager-dashboard.html`), Distributor, Dealer and Retailer Performance, Sales Targets, Regional Sales Analysis, Product Sales Analysis, Customer Sales History (Dealer Bravo), Sales Order Overview, Promotional Campaigns. Operations Manager: Dashboard (`operations-manager-dashboard.html`), Order Processing Queue, Delayed Orders, Dispatch Details (DSP-2026-5521), Stock Movement History, Return Requests, Delivery Issues, Operational Reports. Links on each role's screens go only to screens that role can open (Sales Manager: his own, Customer Approval Queue, My Profile, Notifications; Operations Manager: his own plus Order Details, Dispatch Management, Inventory Overview, Support Ticket Management and Details). Vikram Chopra's and Neha Kulkarni's Phase 12 notifications now open their own screens.
Data: DATA.md "Phase 13 data" and `data.py` section "Phase 13" (asserts). **Decisions I made (recommended, change if you disagree):** targets for the 17 other retailers (total ₹28,20,000); quarterly targets (Q2 82 lakh, Q3 96 lakh, Q4 1 crore); Fast and Slow Mover thresholds (250 and 120 sheets); six placeholder retailer orders in progress with numbers `TSL-2026-<dealer>-nnnn`; the five Promotional Campaigns (PRM-2026-02 to 06) and their budgets; promised dispatch dates (ORD-2026-10398 one day late, reason "Batch Quality Check"); production receipts, transfers and opening stock of Crestline's October stock movements (STN got no production, which is why it is low); the stock count variance of 19/10. Earlier generators re-run: only `registry.js`, the chrome and the company screens changed.
Other changes: `chrome.js` now orders the Operations Manager's sidebar as Orders, Dispatch and Delivery, Stock and Returns, Reports and Support (with Overview first), and gives Delivery Issues, Delayed Orders, Return Requests, Operational Reports and Stock Movement History their own icons.
Verified: `node tools/verify.js <folder>` over every built screen and role at 1440, 1366 × 768 and 390 px over `file://`: ALL OK (196 screens, all roles); looked at in a 1440 screenshot: Sales Manager Dashboard, Retailer Performance, Sales Targets, Regional Sales Analysis, Product Sales Analysis, Sales Order Overview, Promotional Campaigns, Customer Approval Queue as Sales Manager, Operations Manager Dashboard, Order Processing Queue, Delayed Orders, Dispatch Details, Stock Movement History, Return Requests, Operational Reports. Not looked at (automated checks only): Distributor Performance, Dealer Performance, Customer Sales History, Delivery Issues, and Dispatch Details after its activity card was added. Not yet checked in Firefox or Safari.

**Review gaps, stated plainly:** Phases 4 and 5 had no post-commit advisor review; Phase 12 had no advisor review before building. Shared screens do not yet link the newest screens in every place (Bravo's Manager screens do not link Low Stock Overview or Incoming Stock; Charlie's PUR notification and My Inventory's Incoming Shipments card open Order Details, not Incoming Deliveries). Known earlier inconsistencies not changed: Alpha's Order History tab counts (In Transit 2, Awaiting Confirmation 2, Confirmed 3) are above what its list shows; DSP-2026-5521 (24/10) sits between Alpha's 5519 (22/10) and 5522 (23/10).

## What exists

- **Screen Map** (`screen-map.html`, `assets/map.js`, `assets/map.css`; added after Phase 6 at the user's request): a tree from Sign In through Portal
  Selection, the four login screens, the portals, their roles and menu sections to every screen, with the screens opened from another hanging
  under it (Place Order, Order Builder, Order Confirmation). Built screens are links (with `?role=` where needed), planned ones are greyed out; each
  portal, role and section shows "built of total". Search, "Built only" and a detail level (Roles, Sections, Screens) prune the tree. Built from the
  registry, so it never drifts; linked from the "Screen map" button on the Screen Directory pages; checked by `tools/verify.js`.

- `assets/registry.js`: all 196 screens (ID, name, roles, menu section, kind, parent, description, built flag), plus
  each portal's organisation, portal name and each role's person. A screen is built when its ID is in `BUILT`.
- `assets/shell.js`: review bar; link helper `P.setLink` (a link is live only if the target is built and, within the
  portal, available to the signed-in role; otherwise it is inert, muted, with a reason). Use `data-link="PRI-ORD-02"`,
  `data-signin`, `data-directory`. **New in Phase 3, for screens shared by several roles:** `data-role="OWN MGR"` shows an
  element only to those roles; `data-me="name|role|email|initials"` fills in the signed-in person; `data-count="selector"` counts
  the visible matches (used by Notifications and My Profile).
- `assets/chrome.js`: sidebar (menu sections from the registry, unbuilt items muted), top bar (breadcrumbs from the
  parent chain, search, notification bell, profile menu), mobile drawer, `<i data-icon="plus"></i>` icons (new: `upload`).
- `assets/charts.js`: bars, line, donut from data attributes (month names written in full).
- `assets/app.css`: application layout and components (cards, KPI tiles, tables, filters, tabs, steps, track, swatches,
  product cards, quantity stepper, forms, alert, feed). Phase 3 additions at the end: `.drop`/`.file` (uploads), `.thread`/`.msg`
  (ticket conversation), `.feed.ntf` (notifications), `.btn.danger`, `.av-lg`, `td.c` (centred check cells), `[hidden]`.
  `assets/styles.css`: tokens, buttons, chips, forms, review bar, directory, authentication.
- `docs/DATA.md`: products, prices, stock, people, number series, the order flow and formats, and (Phase 3) the dealers, sales
  ledger, dealer price list, invoices, payments, schemes, returns, tickets and users. **Read before building.**
- `tools/author/`: Python generators. **The generator scripts are the source of the screens they write** (each file is
  stamped "Generated by ... edit the generator"); change the script and re-run it from `tools/author` (`python3
  phase3a.py`), never hand-edit a generated screen. `data.py` holds the data model (Phase 3: `DEALERS`, `SALES`,
  `INVOICES`, `PAYMENTS`, `dp()`, with asserts that the totals reconcile) and the markup helpers (`tabs`, `kpi`, `table`, `fld`,
  `form`, `card`, `kv`, `filters`, `pager`, `link`). `tools/inventory.mjs`: registry check and `docs/SCREEN-INVENTORY.md`.
  `tools/verify.js`: browser check over `file://` (needs Playwright). Set `PYTHONDONTWRITEBYTECODE=1` when running the generators
  (a `__pycache__` file is tracked in git).
- To add a screen: write it in a generator, add its ID to `BUILT`, run `node tools/inventory.mjs` and
  `node tools/verify.js <folder> <ID prefix>`, and look at the screenshots.

## Verified in Phase 6

`node tools/verify.js <folder>` with no filter: ALL OK (every built screen and role at 1440, 1366 × 768 and 390 px over `file://`). Every one of the
21 Phase 6 screens was looked at in a 1440 screenshot (the shared Return Requests, My Profile and Notifications also as Manager), as were the six
Phase 5 screens not looked at before (Product Catalogue, Product Details, Place Order, Order Confirmation, Order History, Add Retailer Request);
Tertiary Sales Entry, Invoice Details and Notifications were also looked at at 390. A search of `screens/secondary` for Crestline, Alpha's emails,
Bhiwandi, Rajesh Menon, Suresh Iyer and the Crestline number series found only legitimate Distributor Alpha references. `ML()` now rounds halves up
(₹1,35,500 is ₹1.36 lakh, ₹5,59,500 is ₹5.60 lakh); only three Secondary screens changed. Not yet checked in Firefox or Safari.

## Changes to Phase 2 and 3 screens made in Phase 4 (user's answers to the Phase 3 open items, 2026-10-26)

- **ORD-2026-10398 "Partly Paid": confirmed.**
- **Festive Volume Rebate target is now 2,500 sheets** (was 3,000). Progress 2,750 of 2,500: "Target Reached" chip on the Owner Dashboard,
  Schemes and Incentives and Scheme Details; tiles "Sheets Above Festive Target 250"; the rebate applies to ORD-2026-10482 only (the
  order that takes the total from 1,990 over the target). Notification renamed "Scheme Target Reached".
- **Chart axis:** `assets/charts.js` now picks the smallest 1, 2, 2.5 or 5 step that reaches the peak in six intervals or fewer (₹33.5 lakh
  peak: ₹40 lakh axis, not ₹50 lakh). All charts on every screen use it.
- **Found while building Stock Movement History:** ORD-2026-10431 (delivered 20/10) includes 60 sheets of Calacatta, but Inventory Item
  Details had no receipt that day. Fixed: Item Details now shows "Receipt +60" on 20/10, the balances before it are 60 lower (opening 325),
  the chart's weekly points follow, batch B-2610-14 (20/10, 60) is added, and Inventory Reports ageing for Calacatta is 60 / 0 / 155. Column
  "Dealer or Reason" is now "Name or Reason"; "Damaged in handling" is now "Damaged in Handling".

## Screen text rules

Set by the user after the first Phase 2 review: see DECISIONS.md, "Screen text rules". `tools/verify.js` fails on text under 13px
and on paragraph text. Phase 3 keeps to them: no text under titles, no helper sentences (sentences only in the ticket conversation
and the ticket description, which are user content).

## Open items for the user

All earlier open items (1 to 13, 15, 16) were answered "do what you recommend" on 2026-10-27 and are applied as recorded in DECISIONS.md, "Answered 2026-10-27 (open items)". Nothing is waiting on the user except the hosting question at the end of Phase 14.

## Next

**Phase 14: Review and hand-over** (PLAN.md): (1) links between related screens: the gaps above, and a pass over every screen for links that open a different screen than the label says (every list row opens the one Details screen of its type, by design); (2) a full responsive pass at 1440, 1366 × 768 and 390 px with a look at every screen, not only the automated checks; (3) README for stakeholders (how to open the prototype, the four portals, the screen directory and screen map); (4) regenerate `docs/SCREEN-INVENTORY.md` and check the counts against the brief (196); (5) optional hosting (GitHub Pages) once the user decides; (6) check Firefox and Safari if available; (7) a read-through of DECISIONS.md against the screens (money formats, no helper text, full names, 13px). Open items: none, except the hosting decision (item 5).
Call the advisor before starting and after committing.
