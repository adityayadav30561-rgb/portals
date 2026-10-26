# Laminates Customer Portal: screen prototype plan

_Drafted 2026-10-26. Status: **approved 2026-10-26** (decisions in DECISIONS.md). Live status: [STATUS.md](STATUS.md)._

A static, clickable HTML prototype of every proposed screen in the four portals, for stakeholders to review
and approve before the real application is built. No backend, login, database, storage or business logic.

## 1. Screen coverage review

### What the brief lists

| Portal | Roles | Screen entries listed |
|---|---|---|
| Company Administration | Super Admin 27, Sales Manager 10, Operations Manager 12 | 49 |
| Primary Distributor | Owner 31, Sales / Operations Manager 19, Accountant 15 | 65 |
| Secondary Dealer | Owner 30, Sales / Inventory Manager 20 | 50 |
| Tertiary Retailer | Owner 30, Sales Executive 13, Inventory / Purchasing Executive 14 | 57 |
| Shared sign-in screens | | 9 |
| **Total** | **11 roles** | **230** |

Many entries are the same screen seen by two or three roles (Product Catalogue, Order Details, My Profile).
These are designed **once per portal** and listed under every role that uses them; each role still sees its
own sidebar, name and role in the top bar. Every role's dashboard is its own design.

That leaves **177 distinct screens** (after the merges below), plus the recommended additions: **194**.

### Entries that are the same screen under two names (recommend merging)

| Portal | Listed as | Merge into |
|---|---|---|
| Company | Operations Manager "Order Details and Processing" | Order Details (with processing actions) |
| Company | Operations Manager "Dispatch Overview" | Dispatch Management |
| Company | Operations Manager "Support Ticket Queue" | Support Ticket Management |
| Company | Operations Manager "Inventory Overview" | Inventory Overview (Super Admin's) |
| Primary | Accountant "Invoice List" | Invoices Overview |
| Primary | Accountant "Payment History" | Payments Overview |

Also rename Company "Prototype Settings" to **Portal Settings** (company-level configuration: customer tiers,
order rules, notification rules). "Prototype Settings" reads as a setting of the mock-up itself.

### Gaps: recommended additions (17 screens)

| Add | Where | Why |
|---|---|---|
| Support Ticket Details | all 4 portals | Every portal lists and creates tickets, but nowhere shows one ticket and its replies |
| Notifications | all 4 portals | The bell in every top bar needs a screen to open |
| Return Requests, Create Return Request | Primary, Secondary, Tertiary | The company's Return Requests and Delivery Issues queues have no customer screen feeding them; breakage and wrong shades in transit are routine for laminates |
| Invoice Details | Company | Invoice Management has no detail screen |
| Create Scheme | Company | Scheme Management has no way to set one up |
| Payment Details | Secondary | Primary has it; Secondary Payments Overview has nothing to open |

### Optional additions (not in the counts; include only if wanted)

| Add | Where | Why |
|---|---|---|
| Account Statement (ledger of invoices, payments, credit notes) | Primary Accountant, Secondary Owner, Tertiary Owner | Standard in distributor portals; often the first thing a dealer asks for |
| Account Activation (set password from an invitation) | Shared sign-in | Create User implies the new user gets an invitation |
| Sample and Shade Card Requests | Primary, Secondary, Tertiary | Laminate-specific: dealers and retailers request sample folders and shade cards |
| Price Lists | Company | Price per customer tier; only if pricing should be visible in the review |

## 2. Screens per portal (distinct designs)

✓ = role sees this screen. **New** = recommended addition.

### Company Administration: 45 + 4 new = 49

| Screen | Super Admin | Sales Manager | Operations Manager |
|---|---|---|---|
| Super Admin Dashboard / Sales Manager Dashboard / Operations Dashboard | ✓ | ✓ | ✓ (one each) |
| Customer Directory, Customer Details, Customer Approval Queue, Customer Hierarchy Explorer | ✓ | | |
| User Directory, User Details | ✓ | | |
| Product Management, Product Details, Create Product, Edit Product | ✓ | | |
| Order Management | ✓ | | |
| Order Details | ✓ | | ✓ |
| Order Processing Queue, Delayed Orders | | | ✓ |
| Dispatch Management | ✓ | | ✓ |
| Dispatch Details, Stock Movement History | | | ✓ |
| Inventory Overview | ✓ | | ✓ |
| Return Requests, Delivery Issues, Operational Reports | | | ✓ |
| Sales Analytics; Primary, Secondary, Tertiary and Retail Sales Reports | ✓ | | |
| Invoice Management, Invoice Details **New** | ✓ | | |
| Scheme Management, Scheme Details, Create Scheme **New** | ✓ | | |
| Support Ticket Management, Support Ticket Details **New** | ✓ | | ✓ |
| Territory Management, Audit Activity, Portal Settings | ✓ | | |
| Distributor, Dealer and Retailer Performance | | ✓ | |
| Sales Targets, Regional Sales Analysis, Product Sales Analysis | | ✓ | |
| Customer Sales History, Sales Order Overview, Promotional Campaigns | | ✓ | |
| Notifications **New** | ✓ | ✓ | ✓ |

### Primary Distributor: 48 + 4 new = 52

| Screen | Owner | Manager | Accountant |
|---|---|---|---|
| Owner / Manager / Accountant Dashboard | ✓ | ✓ | ✓ (one each) |
| Company Profile | ✓ | | |
| Product Catalogue, Product Details, Place Order, Order History, Order Details | ✓ | ✓ | |
| Order Builder, Order Confirmation | ✓ | | |
| Inventory Overview | ✓ | ✓ | |
| Inventory Item Details | ✓ | | |
| Low Stock Overview, Stock Movement History, Dispatch Overview | | ✓ | |
| Dealer Network, Dealer Details | ✓ | ✓ | |
| Add Dealer Request | ✓ | | |
| Dealer Order Activity, Dealer Performance, Pending Dealer Requests | | ✓ | |
| Secondary Sales Overview | ✓ | | |
| Secondary Sales Entry, Secondary Sales History | ✓ | ✓ | |
| Invoices Overview, Invoice Details, Payments Overview, Payment Details | ✓ | | ✓ |
| Purchase History, Outstanding Balances, Overdue Invoices, Record Payment | | | ✓ |
| Invoice Ageing Report, Purchase Summary Report, Financial Reports | | | ✓ |
| Invoice Disputes, Invoice Dispute Details | | | ✓ |
| Schemes and Incentives, Scheme Details | ✓ | | |
| Sales Reports, Inventory Reports | ✓ | ✓ | |
| Return Requests **New**, Create Return Request **New** | ✓ | ✓ | |
| Support Ticket List, Create Support Ticket, Support Ticket Details **New** | ✓ | | |
| User Management, Create User, User Details | ✓ | | |
| My Profile | ✓ | | ✓ |
| Notifications **New** | ✓ | ✓ | ✓ |

### Secondary Dealer: 40 + 5 new = 45

| Screen | Owner | Manager |
|---|---|---|
| Owner / Manager Dashboard | ✓ | ✓ (one each) |
| Company Profile, Order Builder, Order Confirmation, Inventory Item Details | ✓ | |
| Product Catalogue, Product Details, Place Order, Order History, Order Details, Inventory Overview | ✓ | ✓ |
| Low Stock Overview, Stock Movement History, Incoming Stock, Reorder Recommendations | | ✓ |
| Retailer Network, Retailer Details | ✓ | ✓ |
| Add Retailer Request | ✓ | |
| Retailer Order Activity, Retailer Performance, Pending Retailer Requests, Dispatch Management | | ✓ |
| Tertiary Sales Overview | ✓ | |
| Tertiary Sales Entry, Tertiary Sales History | ✓ | ✓ |
| Invoices Overview, Invoice Details, Payments Overview, Payment Details **New** | ✓ | |
| Schemes and Incentives, Scheme Details, Sales Reports, Inventory Reports | ✓ | |
| Operational Reports | | ✓ |
| Return Requests **New**, Create Return Request **New** | ✓ | ✓ |
| Support Ticket List, Create Support Ticket, Support Ticket Details **New** | ✓ | |
| User Management, Create User, User Details, My Profile | ✓ | |
| Notifications **New** | ✓ | ✓ |

### Tertiary Retailer: 35 + 4 new = 39

| Screen | Owner | Sales Executive | Inventory Executive |
|---|---|---|---|
| Owner / Sales Executive / Inventory Executive Dashboard | ✓ | ✓ | ✓ (one each) |
| Store Profile, Invoices Overview, Invoice Details, Payments Overview | ✓ | | |
| Product Catalogue, Product Details, My Inventory, Inventory Item Details | ✓ | ✓ | ✓ |
| Place Order, Order Builder, Order History, Order Details, Stock Movement History, Reorder Recommendations, Purchase History | ✓ | | ✓ |
| Order Confirmation | ✓ | | |
| Incoming Deliveries | | | ✓ |
| Record Retail Sale, Retail Sales History, Retail Sale Details | ✓ | ✓ | |
| Low Stock Overview, Recent Transactions | | ✓ | |
| Schemes and Offers, Scheme Details, Sales Reports, Inventory Reports | ✓ | | |
| Return Requests **New**, Create Return Request **New** | ✓ | | |
| Support Ticket List, Create Support Ticket | ✓ | ✓ | |
| Support Ticket Details **New** | ✓ | ✓ | |
| User Management, Create User, User Details | ✓ | | |
| My Profile | ✓ | ✓ | ✓ |
| Notifications **New** | ✓ | ✓ | ✓ |

### Shared sign-in screens: 9

Portal Selection, Company Login, Primary Customer Login, Secondary Customer Login, Tertiary Customer Login,
Forgot Password, Password Reset Confirmation, Access Denied, Not Found.

### Totals

| | Distinct screens | Of which new |
|---|---|---|
| Company Administration | 49 | 4 |
| Primary Distributor | 52 | 4 |
| Secondary Dealer | 45 | 5 |
| Tertiary Retailer | 39 | 4 |
| Shared sign-in | 9 | |
| **Total** | **194** | **17** |

Exact figures are generated from the screen registry in Phase 1 and kept in `docs/SCREEN-INVENTORY.md`.

## 3. Rules for every screen

- **Full names, no abbreviations.** Screen names, menu items, breadcrumbs, table headings and buttons are
  written in full ("Quantity", "Purchase Order", "Secondary Customer — Owner — Order Details"). Only codes
  everyone in the trade uses stay short: SKU, GST, PDF.
- **Screen IDs** follow the brief's pattern and are reference codes only, shown next to the full name, never
  instead of it: dashboards by role (`PRI-OWN-01`), other screens by function (`PRI-ORD-02` Order Details). A
  screen shared by two roles keeps one ID.
- **No filler text.** No eyebrow labels, taglines or explanatory paragraphs. The line under a screen title
  appears only when it carries information (a date, a count, a status: "3 orders waiting for dispatch"), not
  a description of the screen. Descriptions belong in the screen directory, not on the screen.
- **Each dashboard is designed for its role**: the Owner sees business health, the Accountant money owed and
  due, the Inventory Executive stock and deliveries.
- **Fictional data only**, laminates-realistic: Distributor Alpha, Dealer Bravo, Retailer Charlie; Walnut
  Woodgrain, Arctic White Matte, Calacatta Marble Finish; 1 mm and 0.8 mm sheets, 8 × 4 ft, finishes (matte,
  gloss, suede, high gloss), shade codes, sheets and boxes. Product images are CSS swatches of the finish.
- **Design language** taken from the MAVRO product screens (`mavro-ai/prototype`): Inter, deep navy text,
  blue accent, white cards on light grey, subtle borders, chips, readable tables. Unlike those (fixed
  1440 × 960 for screenshots), these screens are **responsive**: sidebar collapses to a menu on phones,
  tables scroll inside their card, cards stack.

## 4. How it is built

Plain HTML, CSS and a little JavaScript; opens by double-clicking `index.html` (no build step, no server).

**Opens without a server (user requirement, 2026-10-26):** `index.html` and every individual screen file open by
double-click, from a folder, a zip or any host. Each screen file is self-contained: it links the shared stylesheet
and classic scripts by relative paths and sets its own default role, so it never depends on the directory having been
opened first. No dev server, no build step, no `npm`. Checked in Phase 1 by opening files straight from disk
(`file://`), not through any server.

**`file://` constraint:** browsers block `type="module"` scripts and `fetch()` on `file://`, so the MAVRO shell
pattern (ES module importing `.ts` from a dev server, fonts from `/node_modules/`) must not be copied. The registry
and shell are classic `<script>` files that expose a global, with no imports and no fetch; fonts and images are
bundled and referenced by relative paths.

```
index.html                 Screen Directory: the four portal cards
directory/<portal>.html    Portal screen directory: roles → screens (ID, name, role, description, Preview)
screens/<portal>/*.html    one file per distinct screen
screens/auth/*.html        shared sign-in screens
assets/styles.css          the design system (tokens, layout, components)
assets/registry.js         every screen: ID, portal, roles, name, description, file, status
assets/shell.js            draws sidebar, top bar and review bar from the registry
docs/SCREEN-INVENTORY.md   generated from the registry: every screen and the counts per portal and role
```

- **One registry drives everything**: the directory, each role's sidebar, the inventory document and the
  counts. A screen is added in one place and nothing drifts.
- **Role-aware shared screens**: Preview opens `screens/primary/order-details.html?role=manager`, and the
  shell shows that role's sidebar, user and dashboard link.
- **Review bar** (thin strip above every screen): screen ID and full name, Back to directory, Previous / Next
  screen for that role. It can be hidden for clean screenshots.
- Screens not yet built appear in the directory as **Planned** with Preview disabled, so the directory is
  complete from Phase 1.

## 5. Phases

One phase per session. Each ends with a browser check at desktop (1440), laptop (1366 × 768) and phone (390)
widths, the inventory regenerated, docs/STATUS.md updated, a commit and a push.

| Phase | Scope | Screens | Done when |
|---|---|---|---|
| **1. Foundations** ✓ done 2026-10-26 | Design system, registry with all 194 screens (including menu group and parent screen), review bar, Screen Directory and the four portal directories, shared sign-in screens, coverage check | 9 | Directory lists every screen; sign-in screens done; check passes |
| **2. Primary Owner, part 1** | Application sidebar and top bar, Owner Dashboard, Company Profile, Product Catalogue, Product Details, Place Order, Order Builder, Order Confirmation, Order History, Order Details, Inventory Overview, Inventory Item Details | 11 | **Design checkpoint: you approve the look before the rest is built** |
| **3. Primary Owner, part 2** | Dealer network, secondary sales, invoices and payments, schemes, reports, returns, support, users, profile, notifications | 24 | |
| **4. Primary Manager and Accountant** | Both dashboards and their own screens | 17 | Primary Distributor complete (52) |
| **5. Secondary Owner, part 1** | Dashboard, profile, catalogue, ordering, orders, inventory, retailer network | about 17 | |
| **6. Secondary Owner, part 2** | Tertiary sales, invoices and payments, schemes, reports, returns, support, users, notifications | about 18 | |
| **7. Secondary Manager** | Dashboard and the manager's own screens | 10 | Secondary Dealer complete (45) |
| **8. Tertiary Retailer Owner, part 1** | Dashboard, store profile, catalogue, ordering, orders, inventory | about 15 | |
| **9. Tertiary Retailer Owner, part 2** | Retail sales, invoices and payments, schemes, reports, returns, support, users, notifications | about 14 | |
| **10. Tertiary Sales Executive and Inventory Executive** | Both dashboards and their own screens | about 10 | Tertiary Retailer complete (39) |
| **11. Company Super Admin, part 1** | Dashboard, customers, hierarchy explorer, users, products, orders | 13 | |
| **12. Company Super Admin, part 2** | Dispatch, inventory, analytics, the four sales reports, invoices, schemes, support, territory, audit, settings, notifications | 18 | |
| **13. Company Sales and Operations Managers** | Both dashboards and their own screens | 18 | Company Administration complete (49) |
| **14. Review and hand-over** | Links between related screens, full responsive pass, README, screen inventory and counts, optional hosting for stakeholders | | Definition of Done in the brief met |

Portal naming: screen names use the brief's pattern with the portal as "Primary Customer", "Secondary Customer",
"Tertiary Customer" and "Company"; the directory cards use the brief's card titles (Primary Distributor, and so on).

## 6. Decisions

All answered on 2026-10-26; see DECISIONS.md. Open: Company My Profile, Tertiary Payment Details, two-part or three-part screen names.
