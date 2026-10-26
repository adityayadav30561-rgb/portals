# Laminates Customer Portal: screen prototype

Static HTML prototype of the four portals (Company Administration, Primary Distributor, Secondary Dealer,
Tertiary Retailer) for stakeholder approval. No backend, login, storage or business logic. Uses the official
MAVRO.AI logo only.

## Read before doing anything

1. [docs/STATUS.md](docs/STATUS.md): where the work is, what is next, open questions. Always read.
2. [docs/WORKFLOW.md](docs/WORKFLOW.md): session protocol; one phase per session, then clear context.
3. [docs/DECISIONS.md](docs/DECISIONS.md): what the user asked for and rejected. Read before any design change.
4. [docs/PLAN.md](docs/PLAN.md): screen list by portal and role, rules for every screen, build approach, phases.

## Rules that always apply

- Work in this repository only. The `mavro-ai` repository (`prototype/`, `prototype/modules/`) is a read-only visual
  reference for how screens look.
- Screen names, menus, breadcrumbs, headings and buttons in full; no abbreviations. IDs are reference codes next to
  the full name.
- No eyebrow text, taglines or paragraphs describing the screen. Text on screen must carry information.
- Fictional laminates data only. Logo: `brand/mavro-logo.jpg` and `assets/brand/`, never redrawn or recoloured.
- Verify in the browser at 1440, 1366 × 768 and 390 px before calling a phase done.
- Keep the docs current: at the end of every task update docs/STATUS.md (and DECISIONS.md for preferences), then
  commit and push to `claude/relaxed-cerf-p4czn7`.
