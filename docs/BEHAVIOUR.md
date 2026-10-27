# Behaviour layer: how the screens work

Every control in the prototype works in the browser (DECISIONS.md, "Everything works"). Nothing is sent anywhere; there is no
storage. The behaviour is written once, in `assets/app-*.js`, and attaches to the markup the generators write. A control with no
behaviour is a bug: `node tools/interact.js` must report **0 dead controls**.

## Modules (classic scripts, loaded in this order by `page()` in `tools/author/data.py`)

| File | What it does |
|---|---|
| `assets/catalog.js` | Written by `tools/author/runtime_data.py` from `data.py`: products, per-portal prices (Primary slabs, dealer and retailer prices), supplier stock, rebate rule, credit limits, the designed draft orders, previous orders. Re-run the script after changing prices, stock or credit. |
| `assets/app-core.js` | URL state, formatting (`fmtM`, `fmtML`, `fmtN`: the same rules as `M`, `ML`, `N` in `data.py`), toast, dialog, dropdown (`A.menu`), Reset Data, status chips. |
| `assets/app-lists.js` | Search, dropdown filters, tabs, sortable headers, pager, grid and list view, quantity steppers, for every table, product grid and feed. |
| `assets/app-orders.js` | The cart and the order flow in Primary, Secondary and Tertiary. |
| `assets/app-forms.js` | Validation, created records, status actions, uploads, conversations, notifications, edit dialogs, sale and payment entry, top-bar search, sign-in. |
| `assets/app-files.js` | CSV export of the listed rows, PDF download of a screen (small PDF writer), print. |
| `assets/app-boot.js` | Runs the start-up functions in priority order (10 hydrate, 20 orders, 25 forms, 30 lists). |
| `assets/behaviour.css` | Styles for the above (toast, dialog, dropdown, sort arrows, empty states, validation, list view, print). |

## State: the URL, never browser storage

One `st` URL parameter holds a small JSON object, kept on every internal link and written into the address bar on every change. A reload
keeps it; **Reset Data** in the review bar clears it. Keys: `c` cart by portal, `o` submitted orders, `f` delivery form, `r` created rows
by list screen, `x` status changes (`"SCREEN|row key"` and `"SCREEN|page"`), `d` removed rows, `e` edited values, `m` conversation messages,
`n` read notifications, `t` a one-time toast shown on the next screen.

## Conventions the markup must follow

- **Search and filters.** `.filters` (or a card header) with `.finder input`, `.sel` dropdowns (`<small>Label</small> Value`), and `.tabs > span`
  sit before the table, `.products` grid or `ul.feed` they control. A dropdown filters the table column with the same heading (see `HEAD_ALIAS`
  in app-lists.js); a tab matches the status chip with its label. The tab a screen opens on holds every row.
- **Counts follow the rows.** Tab badges and "Showing x to y of z" are recomputed from the rows that exist.
- **Dropdowns only offer what the data can answer.** `Period` offers October 2026 only (the one month of data); `Compared With` can switch the
  change chips off; `Date Range` filters the first date column.
- **Steppers.** `.qty` with `−`, an input and `+`. Optional `data-max`, `data-min`, `data-step`.
- **Buttons are wired by their label** (app-forms.js): `Export …` (CSV), `Download …` (PDF), `Print …`, `Save Draft`, `Cancel`, `Approve`, `Reject`,
  `Confirm Order`, `Close Ticket`, `Send Reply`, `Deactivate User`, `Edit …`, `Upload …`, `Attach Files`, `Mark All as Read`, and the create and
  submit buttons of the forms in `COLL`. A new button needs a label that matches one of these, or a new handler.
- **Created records** appear first in the list named in `COLL` (form screen, list screen, how to build the row from the form). Row cells are
  filled by column heading.
- **Orders.** Totals come from `A.calc` (slab or flat price, rebate, GST split, freight, credit). The designed draft must reproduce the static
  totals exactly (Primary ₹9,49,752, Secondary ₹2,93,820, Tertiary ₹1,04,784); `node tools/e2e.js` checks it.

## Checks

| Command | What it checks |
|---|---|
| `node tools/verify.js [folder] [prefix]` | Every screen, role and width: errors, overflow, text size, abbreviations, links, no browser storage. |
| `node tools/interact.js [prefix]` | Clicks every control; lists the ones that do nothing. Must end with 0 dead controls. |
| `node tools/e2e.js` | Order flows in three portals (totals, stock limit, credit block, numbering), forms, approvals, downloads. |

## Known limits (stated plainly)

- Rows in a list open the one Details screen of their type (the sample record), as before; only orders placed in the session get their own details.
- Lists contain the sample rows that exist; the prototype has no further pages of data.
- Period selectors offer October 2026 only; KPI tiles and charts do not recompute.
- Dashboard tiles are not recomputed after an order or approval (Order History tiles are).
