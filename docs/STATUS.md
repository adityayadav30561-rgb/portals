# Status

_Last updated: 2026-10-26. Update at the end of every task and phase._

## Where we are

**Phase 11 (Company Super Admin, part 1) is built and verified: 13 screens, 159 of 196 built** (9 sign-in, Primary 52, Secondary 45, Tertiary 40, Company 13). The Phase 10 review was taken as approval ("START NEXT PHASE", 2026-10-26); the open items below stay as my recommendations until the user answers.
Remaining: 37 Company Administration screens (Phase 12: dispatch, inventory, analytics and the four sales reports, invoices, schemes, support, territory, audit, settings, notifications, My Profile; Phase 13: Sales Manager and Operations Manager).

Phase 11 screens (generators `tools/author/phase11a.py`, `11b`, `11c`; folder `screens/company/`): Super Admin Dashboard (`super-admin-dashboard.html`), Customer Directory, Customer Details (Distributor Alpha), Customer Approval Queue (DRQ-2026-0017 Dealer Omkar, with decided history), Customer Hierarchy Explorer (native `<details>` tree, Expand All / Collapse All via `data-expand` in shell.js, CSS `.tree` at the end of app.css), User Directory, User Details (Vikram Chopra), Product Management, Product Details (LM-WNT-001), Create Product (LM-ASH-013, unsaved), Edit Product, Order Management, Order Details (ORD-2026-10459, shared by the Super Admin and the Operations Manager; `data-role` shows each role its own actions; the Operations Manager's breadcrumb parent, Order Processing Queue, is not built yet).
Data: DATA.md "Phase 11 data" and `data.py` section "Phase 11" (asserts tie everything to Phases 2 to 10). **Decisions I made (recommended, change if you disagree):** one distributor only (no other distributors invented); the 17 unnamed retailers are named; Meera Kapoor is a "Customer Support Agent" user with no portal screens; Crestline gets a second warehouse (Regional Warehouse, Taloja) next to Plant Warehouse, Vapi; company stock numbers and reorder levels; Order Management lists the Primary tab with tier counts for the other two; User Directory counts 70 users (52 unnamed, counts only); Customer Approval Queue shows Vikram Chopra as assignee with the Super Admin able to decide; labels flipped to Crestline's perspective ("Awaiting Customer Reply", "Waiting for Decision"). Earlier generators re-run: no change to any earlier screen.
Verified: `node tools/verify.js <folder> CMP-`: ALL OK (13 screens, Order Details also as Operations Manager, at 1440, 1366 × 768 and 390 px over `file://`); every screen looked at in a 1440 screenshot, Hierarchy Explorer also at 390. Not yet checked in Firefox or Safari. The bell badge (3) and unbuilt menu items are inert until Phase 12.

**Review gaps, stated plainly:** Phases 4 and 5 had no post-commit advisor review. Shared screens do not yet link the newest screens in every place (Bravo's Manager screens do not link Low Stock Overview or Incoming Stock; Charlie's PUR notification and My Inventory's Incoming Shipments card open Order Details, not Incoming Deliveries).

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

1. **Dealer schemes are placeholders** (SCH-2026-07 Dealer Festive Volume Rebate 1% at 750 sheets; SCH-2026-08 Marble Finish Dealer Incentive
   ₹15 per sheet; SCH-2026-09 Winter Season Dealer Bonus; SCH-2026-03 Monsoon Dealer Incentive). They now have full screens; confirm or replace.
2. **Dealer order numbers** are Alpha's sale numbers (SAL-2026-3040) and Bravo's invoice numbers are the same. Say if dealers should have their
   own series.
3. **"D" number series** for documents issued by Distributor Alpha (PAY-2026-D0521, RTN-2026-D0508, TKT-2026-D0746) keep them apart from the
   Crestline series; say if you prefer another format.
4. **Number series Dealer Bravo issues itself (new in Phase 7):** retailer requests RRQ-2026-0005 to 0007, deliveries DLV-2026-0401 to 0412, stock adjustments
   ADJ-2026-B0011 to B0015. Say if you prefer another format.
5. **Retailer order TSL-2026-0413** (Charlie, awaiting confirmation) is both the Phase 6 Tertiary Sales Entry example and the order the Tertiary portal will show; confirm.
6. **Retailer targets** (Charlie ₹2,50,000; Kiran ₹2,20,000; Mehta ₹1,70,000) and the three pending retailer requests are placeholders.
7. **Known point:** the Reorder Recommendations total (₹3,35,500, ₹3,95,890 with GST) is above Bravo's credit available after SAL-2026-3042 (₹2,46,180); the rule is unchanged, say if you want it to respect credit.
8. **Phase 8 placeholders (new):** Charlie's own numbers RSL-2026-xxxx (sales to customers) and ADJ-2026-C000x (adjustments); the 25% selling-price rule (`crp()`); the 38 customer names
   and payment modes; Charlie's stock levels and reorder levels; the offers OFR-2026-01 and 02 from Dealer Bravo; Store Profile legal name (Charlie Laminates Private Limited), code RTL-0041, established 2018.
9. **Phase 9 placeholders (new):** the letter "B" for documents Bravo issues to retailers; Charlie's payments, returns and tickets; the offers OFR-2026-03 (Monsoon, ₹1,880) and 04 (Winter); the five users (Mohit Gawande invited, Sneha Ranpise inactive); the 13-area access matrix.
10. **Phase 11 decisions (new):** the scope and data choices listed under "Where we are"; also the 17 retailer names, owners and purchases, Dealer Omkar's details, DRQ-2026-0014 and 0011, the Taloja warehouse and company stock, Vikram Chopra's user history.
11. **Sales Manager and approvals (new, your call):** the registry gives the Sales Manager neither Order Details (Super Admin and Operations Manager) nor the Customer Approval Queue (Super Admin only), yet Vikram Chopra confirms orders and approves dealer requests in the Phase 11 data. Recommendation: tag the Sales Manager onto Customer Approval Queue (as the Managers were tagged onto existing screens in Phase 2) and give Sales Order Overview (SAL-09) a Confirm action in Phase 13. Adding a role to a screen changes the per-role counts in PLAN.md, so it waits for you.
12. Order Management's "Orders by Tier" shows an order-count total only (93); a value total across tiers would count the same sheets up to three times.
13. Earlier answers applied from my recommendations (change if you disagree): Marble Finish Launch Incentive 140 of 300; Dealer Lakshya not in
   Pending Dealer Requests; Financial Reports May to October; May to September tax split kept.

## Next

**Phase 12: Company Super Admin, part 2** (PLAN.md; 18 screens): Dispatch Management (DSP-01, shared with the Operations Manager), Inventory Overview (INV-01, shared; use the Phase 11 company stock), Sales Analytics (ANL-01), Primary, Secondary, Tertiary and Retail Sales Reports (RPT-01 to 04; Tertiary and Retail need retailer-level October figures: the 20 retailers' purchases exist in `RETAIL_OCT`, September and by-product splits do not), Invoice Management and Invoice Details (BIL-01, 02), Scheme Management, Scheme Details, Create Scheme (SCH-01 to 03), Support Ticket Management and Details (SUP-01, 02, shared; tickets are Alpha's six in `CRL_TICKETS`), Territory Management (the five regions of the dealers), Audit Activity, Portal Settings, My Profile (PRO-02) and Notifications (NTF-01, three roles). Phase 13: Sales Manager and Operations Manager.
**Open item carried into Phase 12 (Scheme Management):** the SCH-2026 series mixes the two companies: Crestline's schemes to Alpha are SCH-2026-01, 02, 04, 05, 06; SCH-2026-03 and 07 to 09 are Alpha's schemes to its dealers. List Crestline's only (recommended) or show Alpha's as "issued by a distributor"; say which in DATA.md. The DSP-2026-55xx series is also shared (5521 is Crestline's shipment to Alpha; the rest are Alpha's dispatches to dealers).
**Shared number series to check before inventing any Crestline number:** Alpha also uses ADJ-2026-00xx, DRQ-2026-00xx and the "D" series (PAY, RTN, TKT); Bravo uses RRQ, DLV, ADJ-2026-B and "B" documents; Charlie uses RSL and ADJ-2026-C. Crestline's own: ORD, INV, PAY, RTN-2026-0xxx, TKT-2026-0xxx, CN, DIS, DSP-5521, CUS.
Call the advisor before starting and after committing.
