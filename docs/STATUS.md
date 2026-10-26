# Status

_Last updated: 2026-10-26. Update at the end of every task and phase._

## Where we are

**Phase 9 (Tertiary Retailer Owner, part 2) is built and verified; waiting for the user's approval before Phase 10** (Sales Executive and Inventory and Purchasing Executive dashboards and their own screens).
"START NEXT" (2026-10-26) was taken as approval of Phase 8; the Phase 7 and Phase 8 open items stay as my recommendations until the user answers.
**141 of 196 screens are built:** 9 sign-in screens, Primary Distributor (52), Secondary Dealer (45) and 35 of the 40 Tertiary Retailer screens.

Phase 9 screens (21; generators `tools/author/phase9a.py` and `phase9b.py`; Retailer Charlie): Record Retail Sale, Retail Sales History, Retail Sale Details (shared with the Sales Executive), Invoices Overview,
Invoice Details, Payments Overview, Payment Details, Schemes and Offers, Scheme Details, Sales Reports, Inventory Reports, Return Requests, Create Return Request, Support Ticket List, Create Support Ticket,
Support Ticket Details (the three support screens shared with the Sales Executive), User Management, Create User, User Details, My Profile and Notifications (shared with both Executives; three unread each).
Data: DATA.md, "Phase 9 data". Highlights: invoices are Bravo's TSL sales (245, 1 open: TSL-2026-0412, ₹62,000, due 09/11); payments by Charlie reconcile (₹12,47,000 over six months = purchases ₹13,09,000 − ₹62,000, carry-in 0);
Sales Reports state their basis (sales including GST ₹3,27,557; tables before GST ₹2,77,595); no profit or margin total anywhere; documents Dealer Bravo issues to retailers carry a "B" (PAY-2026-B0388, RTN-2026-B0214, TKT-2026-B0452).
**Changes to Phase 8 made in Phase 9:** the last three sales to customers (RSL-2026-0396 to 0398) are dated today (26/10), every sale has a time and a recorder (rule in DATA.md), the dashboard line is now "Earned on Active Offers".
All earlier generators re-run: `screens/` differs only in those two Phase 8 screens (dashboard, Stock Movement History).

**Review gaps, stated plainly:** Phases 4 and 5 had no post-commit advisor review. The advisor reviewed the plans of Phases 6 to 9 and the finished Phases 6, 7 and 8; the finished Phase 9 also had its post-commit review (fixes: Sales Executive Support Ticket Details related records, average sale value rounded, donut order, ticket number). Not yet checked in Firefox or Safari.
Shared Bravo screens do not yet link Low Stock Overview or Incoming Stock for the Manager (the sidebar does).

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
10. Earlier answers applied from my recommendations (change if you disagree): Marble Finish Launch Incentive 140 of 300; Dealer Lakshya not in
   Pending Dealer Requests; Financial Reports May to October; May to September tax split kept.

## Next

**Phase 10: Tertiary Sales Executive and Inventory and Purchasing Executive** (PLAN.md; 5 screens): Sales Executive Dashboard, Low Stock Overview, Recent Transactions; Inventory and Purchasing Executive Dashboard, Incoming Deliveries.
Both roles already see the shared screens built in Phases 8 and 9. Build on: `CSALES` (today's three sales at 10:30, 13:10, 15:50), `CSTOCK`/`CREC`, `INCOMING`-style shipments (TSL-2026-0412 Being Packed expected 27/10; TSL-2026-0413 awaiting confirmation),
the notifications already shown to each role. Add the Phase 10 data to DATA.md first. Then Tertiary Retailer is complete (40). Call the advisor before starting and after committing.
