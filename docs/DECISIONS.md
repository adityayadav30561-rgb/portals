# Decisions and user preferences

What the user asked for, liked and rejected. Read before any design change; never reintroduce anything under
"Rejected". Add an entry as soon as the user states a preference.

## Standing preferences

| Preference | Detail | Date |
|---|---|---|
| This repository is the workspace | All work happens in `portals`. The `mavro-ai` repository is only a visual reference for how screens look (`prototype/`, `prototype/modules/`). Never edit it. | 2026-10-26 |
| Official MAVRO.AI logo only | `brand/mavro-logo.jpg`, transparent versions in `assets/brand/`. Never redrawn, recoloured or replaced by a made-up company logo; light backgrounds only. | 2026-10-26 |
| Docs-driven development | Work is staged in phases; state lives in `docs/*.md` so the session can be cleared after every phase (docs/WORKFLOW.md). | 2026-10-26 |
| Four portals | Company Administration, Primary Distributor, Secondary Dealer, Tertiary Retailer; all four are built. | 2026-10-26 |
| Full screen names | Names, menus, breadcrumbs, table headings and buttons are written in full so everyone understands; no abbreviations (SKU, GST, PDF excepted). Screen IDs are reference codes next to the full name, never instead of it. | 2026-10-26 |
| No filler text | No eyebrow labels, taglines or paragraphs that describe the screen. A line under the title appears only when it carries information (counts, dates, status). | 2026-10-26 |
| Opens by double-click | No dev server. `index.html` and each individual screen HTML file must open directly from disk (`file://`); verify that way, never only through a local server. Relative paths, classic scripts, bundled font and logo. | 2026-10-26 |
| Static prototype | HTML/CSS/small JavaScript. No backend, login, database, storage, real logic. Fictional data. | 2026-10-26 |
| Design language | Light theme, deep navy text, blue accent, Inter, white cards on light grey, as in the MAVRO product screens; responsive (unlike the fixed-size MAVRO captures). | 2026-10-26 |

## Pending approval (asked 2026-10-26, see PLAN.md section 6)

- Six merges of duplicate screens and the rename "Prototype Settings" to "Portal Settings".
- 17 recommended additional screens; any of the 4 optional ones.
- Branch: the session set `claude/relaxed-cerf-p4czn7`; the repository had no commits, so it is the only branch. The user insisted on `main` only in `mavro-ai`. Working on the session branch until answered.
- Portal names in screen names: Company, Primary Customer, Secondary Customer, Tertiary Customer (brief's pattern); directory cards use the brief's card titles.
- Whether stakeholders need a shareable link (for example GitHub Pages) or a zipped folder.

## Rejected

Nothing yet.
