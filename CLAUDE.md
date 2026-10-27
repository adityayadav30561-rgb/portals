# Laminates Customer Portal: screen prototype

Clickable HTML prototype of the four portals (Company Administration, Primary Distributor, Secondary Dealer,
Tertiary Retailer) for stakeholder approval. No backend, real login or storage, but **every control works in the
browser** (user, 2026-10-27): add to order, search, filters, tabs, sorting, forms, approvals, exports. Behaviour is
written once in `assets/app.js` and the other `assets/*.js` modules, not per screen. State travels in the URL
(never localStorage). Uses the official MAVRO.AI logo only.

## Read before doing anything

1. [docs/STATUS.md](docs/STATUS.md): where the work is, what is next, open questions. Always read.
2. [docs/WORKFLOW.md](docs/WORKFLOW.md): session protocol; one phase per session, then clear context.
3. [docs/DECISIONS.md](docs/DECISIONS.md): what the user asked for and rejected. Read before any design change.
4. [docs/PLAN.md](docs/PLAN.md): screen list by portal and role, rules for every screen, build approach, phases.

## Rules that always apply

- No dev server, no build step: `index.html` and every screen file must open by double-click (`file://`), with
  relative paths and classic scripts only. Test that way.
- Work in this repository only. The `mavro-ai` repository (`prototype/`, `prototype/modules/`) is a read-only visual
  reference for how screens look.
- Screen names, menus, breadcrumbs, headings and buttons in full; no abbreviations. IDs are reference codes next to
  the full name.
- No text under page titles, no captions beside card titles, no helper sentences, nothing under 13px. Information is
  carried by titles, labels, values, chips, meters and tables (docs/DECISIONS.md, "Screen text rules"). Every screen
  must look finished: no redesign later.
- No grey line under a name: SKU, city, role, date go in their own column, tag or labelled row (the top-bar user block and
  the sidebar organisation block are the only exemption). Money: compact (₹33.53 lakh) in stat tiles, chart axes and
  summaries; exact (₹9,49,752) in orders, invoices, prices and tables; one format per amount on a screen. Helpers in
  `tools/author/data.py` (`M`, `ML`, `OPEN_ORDERS`); read docs/DATA.md.
- Screens are written by the generator scripts in `tools/author/`; change the script, never the generated file.
- **No dead controls.** Every button, link-button, dropdown, tab, stepper and checkbox must do something observable
  (`node tools/interact.js` audits this and must report zero). New markup follows the conventions in `assets/app.js`
  (docs/BEHAVIOUR.md); a control with no behaviour is a bug.
- Fictional laminates data only. Logo: `brand/mavro-logo.jpg` and `assets/brand/`, never redrawn or recoloured.
- Verify in the browser at 1440, 1366 × 768 and 390 px before calling a phase done.
- Keep the docs current: at the end of every task update docs/STATUS.md (and DECISIONS.md for preferences), then
  commit and push to `claude/relaxed-cerf-p4czn7`; the finished prototype is also pushed to `main` (user, 2026-10-27).
