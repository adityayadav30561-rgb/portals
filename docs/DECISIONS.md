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

## Answered at the Phase 2 checkpoint (user, 2026-10-26)

| Decision | Detail |
|---|---|
| Look approved | Sidebar, cards, colours, swatches and charts. |
| Managers can order | Primary and Secondary Managers are tagged onto Order Builder, Order Confirmation and Inventory Item Details (no new screens). |
| Money format | Compact, with full words: ₹33.53 lakh, ₹1.25 crore. Used in stat tiles, chart axes and summary cards (credit, balances). Exact figures (₹9,49,752) stay in orders, invoices, price lists and tables, where the precise amount is the point. Under ₹1 lakh always exact. Never "L", "Cr", "K". |
| Date format | 26/10/2026 in tables, "26 October 2026" in text (not objected to). |
| Lines under names | **No grey secondary line under a name anywhere.** Each attribute is its own labelled column (SKU, City, Role, Date), a tag (SKU on cards, city beside a dealer name, PDF) or a key-value row. Chosen by Claude on the user's instruction "whichever is more qualified to be in our portal". |

## Screen text rules (user, 2026-10-26, after the Phase 2 review: "every block, every phrase, every text should look like a finished product, no redesign later")

Applies to every screen, in every phase. `tools/verify.js` enforces what a machine can.

| Rule | Detail |
|---|---|
| Nothing under a page title | No subtitle, description or context line. Organisation is in the sidebar, the period is in its selector, status is a chip beside the title. |
| Nothing beside a card title | Card header = title plus, at most, an action link or button on the right. No grey captions ("May to October 2026", "sheets on hand"). |
| Stat tiles | Label, value, and at most one chip (change, status, or exception). No footnote sentences. A comparison period lives in the chip's tooltip, not in visible text. |
| No helper sentences or banners | Status is carried by chips, icons, colours and meters (an alert banner with a sentence is replaced by a chip). Sentences are allowed only on state screens (confirmation, error) and for user content (notes, activity feed). |
| No lines under names | **No grey secondary line under a name, anywhere on a screen.** Each attribute is its own labelled column (SKU, City, Role, Date), a tag (SKU on cards, city beside a dealer name, PDF) or a key-value row. Exemption, by design: the frame, i.e. the top-bar user block (name, role) and the sidebar organisation block (organisation, portal name), the standard identity pattern. `tools/verify.js` fails on `<small>`/`.sub` lines inside tables, lists and cards. |
| Minimum text size | 13px (0.8125rem), everywhere including chips, table headings, axis labels and avatars. |
| Layout quality | Cards in a row have equal height; no dead space inside cards; no clipped values; tables never scroll sideways inside a card on desktop; every number has a label. |

## Approved by the user (2026-10-26, "go with your recommendations")

| Decision | Detail |
|---|---|
| Six merges + rename | Company Operations Manager's Order Details and Processing, Dispatch Overview, Support Ticket Queue, Inventory Overview are the Super Admin's screens; Primary Accountant's Invoice List and Payment History are Invoices Overview and Payments Overview. "Prototype Settings" is named **Portal Settings**. |
| 19 additions | (17 on 2026-10-26, plus Company My Profile and Tertiary Payment Details after the Phase 1 review.) Notifications and Support Ticket Details in all four portals; Return Requests and Create Return Request in Primary, Secondary, Tertiary; Company Invoice Details and Create Scheme; Secondary Payment Details; Company My Profile; Tertiary Payment Details. None of the 4 optional ones. **Total 196 screens** (Company 50, Primary 52, Secondary 45, Tertiary 40, sign-in 9). |
| Sharing | Folder or zip now; hosting (GitHub Pages) is decided in the last phase. |
| Branch | Stay on `claude/relaxed-cerf-p4czn7`. The `main`-only rule belongs to `mavro-ai`. |
| Screen name pattern | Three parts, generated from portal, role and screen name: "Primary Customer — Owner — Order Details". Portal labels: Company Administration, Primary Customer, Secondary Customer, Tertiary Customer. Directory cards use the brief's titles (Primary Distributor, Secondary Dealer, Tertiary Retailer). |
| Role labels | Words, not slashes: Super Admin, Sales Manager, Operations Manager; Owner, Sales and Operations Manager, Accountant; Owner, Sales and Inventory Manager; Retailer Owner, Sales Executive, Inventory and Purchasing Executive. |
| No localStorage | The brief bans it, including for review-bar settings; use URL parameters only. |

## Raised in Phase 1, answered 2026-10-26 ("go with your recommendations")

- **My Profile for roles without one.** DONE: add a Company My Profile (Company 50); Primary and Secondary Managers use the existing My Profile.
- (was) **My Profile for roles without one.** Primary and Secondary Managers were tagged onto the existing My Profile screen (no new screen). The three Company roles have none; add a Company My Profile (+1 screen)?
- **Tertiary Payment Details.** DONE: added (Tertiary 40, total 196).
- (was) **Tertiary Payment Details.** Tertiary Payments Overview has nothing to open; add Payment Details (Tertiary 40, total 195)?
- **Screen name pattern:** DONE: three-part kept.
- (was) **Screen name pattern:** three-part (above) or the brief's two-part examples ("Primary Customer — Product Catalogue")? One-line change.

## Rejected

Nothing yet.
