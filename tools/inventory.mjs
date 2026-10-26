// Checks the screen registry against the brief and writes docs/SCREEN-INVENTORY.md.
// Authoring tool only: the prototype itself needs no Node and no build. Run:  node tools/inventory.mjs
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sandbox = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(root, 'assets/registry.js'), 'utf8'), sandbox);
const P = sandbox.window.PORTAL;

const errors = [];
const fail = (m) => errors.push(m);

// ---------- The brief, verbatim (sections 6 to 10). "Dashboard" entries are matched to the role's Dashboard. ----------
const dash = 'Dashboard';
const BRIEF = {
  'company/ADM': ['Company Super Admin Dashboard', 'Customer Directory', 'Customer Details', 'Customer Approval Queue', 'Customer Hierarchy Explorer', 'User Directory', 'User Details', 'Product Management', 'Product Details', 'Create Product', 'Edit Product', 'Order Management', 'Order Details', 'Dispatch Management', 'Inventory Overview', 'Sales Analytics', 'Primary Sales Report', 'Secondary Sales Report', 'Tertiary Sales Report', 'Retail Sales Report', 'Invoice Management', 'Scheme Management', 'Scheme Details', 'Support Ticket Management', 'Territory Management', 'Audit Activity', 'Prototype Settings'],
  'company/SAL': ['Sales Manager Dashboard', 'Distributor Performance', 'Dealer Performance', 'Retailer Performance', 'Sales Targets', 'Regional Sales Analysis', 'Product Sales Analysis', 'Customer Sales History', 'Sales Order Overview', 'Promotional Campaigns'],
  'company/OPS': ['Operations Dashboard', 'Order Processing Queue', 'Order Details and Processing', 'Dispatch Overview', 'Dispatch Details', 'Inventory Overview', 'Stock Movement History', 'Delayed Orders', 'Return Requests', 'Delivery Issues', 'Operational Reports', 'Support Ticket Queue'],
  'primary/OWN': ['Primary Customer Owner Dashboard', 'Company Profile', 'Product Catalogue', 'Product Details', 'Place Order', 'Order Builder', 'Order Confirmation', 'Order History', 'Order Details', 'Inventory Overview', 'Inventory Item Details', 'Dealer Network', 'Dealer Details', 'Add Dealer Request', 'Secondary Sales Overview', 'Secondary Sales Entry', 'Secondary Sales History', 'Invoices Overview', 'Invoice Details', 'Payments Overview', 'Payment Details', 'Schemes and Incentives', 'Scheme Details', 'Sales Reports', 'Inventory Reports', 'Support Ticket List', 'Create Support Ticket', 'User Management', 'Create User', 'User Details', 'My Profile'],
  'primary/MGR': ['Primary Customer Manager Dashboard', 'Product Catalogue', 'Product Details', 'Place Order', 'Order History', 'Order Details', 'Inventory Overview', 'Low Stock Overview', 'Dealer Network', 'Dealer Details', 'Dealer Order Activity', 'Secondary Sales Entry', 'Secondary Sales History', 'Dealer Performance', 'Stock Movement History', 'Dispatch Overview', 'Sales Reports', 'Inventory Reports', 'Pending Dealer Requests'],
  'primary/ACC': ['Primary Customer Accountant Dashboard', 'Purchase History', 'Invoice List', 'Invoice Details', 'Outstanding Balances', 'Overdue Invoices', 'Record Payment', 'Payment History', 'Payment Details', 'Invoice Ageing Report', 'Purchase Summary Report', 'Invoice Disputes', 'Invoice Dispute Details', 'Financial Reports', 'My Profile'],
  'secondary/OWN': ['Secondary Customer Owner Dashboard', 'Company Profile', 'Product Catalogue', 'Product Details', 'Place Order', 'Order Builder', 'Order Confirmation', 'Order History', 'Order Details', 'Inventory Overview', 'Inventory Item Details', 'Retailer Network', 'Retailer Details', 'Add Retailer Request', 'Tertiary Sales Overview', 'Tertiary Sales Entry', 'Tertiary Sales History', 'Invoices Overview', 'Invoice Details', 'Payments Overview', 'Schemes and Incentives', 'Scheme Details', 'Sales Reports', 'Inventory Reports', 'Support Ticket List', 'Create Support Ticket', 'User Management', 'Create User', 'User Details', 'My Profile'],
  'secondary/MGR': ['Secondary Customer Manager Dashboard', 'Product Catalogue', 'Product Details', 'Place Order', 'Order History', 'Order Details', 'Inventory Overview', 'Low Stock Overview', 'Stock Movement History', 'Retailer Network', 'Retailer Details', 'Retailer Order Activity', 'Tertiary Sales Entry', 'Tertiary Sales History', 'Retailer Performance', 'Dispatch Management', 'Incoming Stock', 'Reorder Recommendations', 'Operational Reports', 'Pending Retailer Requests'],
  'tertiary/OWN': ['Tertiary Retailer Owner Dashboard', 'Store Profile', 'Product Catalogue', 'Product Details', 'Place Order', 'Order Builder', 'Order Confirmation', 'Order History', 'Order Details', 'My Inventory', 'Inventory Item Details', 'Stock Movement History', 'Record Retail Sale', 'Retail Sales History', 'Retail Sale Details', 'Purchase History', 'Invoices Overview', 'Invoice Details', 'Payments Overview', 'Schemes and Offers', 'Scheme Details', 'Sales Reports', 'Inventory Reports', 'Reorder Recommendations', 'Support Ticket List', 'Create Support Ticket', 'User Management', 'Create User', 'User Details', 'My Profile'],
  'tertiary/SLS': ['Tertiary Sales Executive Dashboard', 'Product Catalogue', 'Product Details', 'My Inventory', 'Inventory Item Details', 'Record Retail Sale', 'Retail Sales History', 'Retail Sale Details', 'Low Stock Overview', 'Recent Transactions', 'Support Ticket List', 'Create Support Ticket', 'My Profile'],
  'tertiary/PUR': ['Tertiary Inventory Executive Dashboard', 'Product Catalogue', 'Product Details', 'Place Order', 'Order Builder', 'Order History', 'Order Details', 'My Inventory', 'Inventory Item Details', 'Stock Movement History', 'Incoming Deliveries', 'Reorder Recommendations', 'Purchase History', 'My Profile'],
  'authentication/ALL': ['Portal Selection', 'Company Login', 'Primary Customer Login', 'Secondary Customer Login', 'Tertiary Customer Login', 'Forgot Password', 'Password Reset Confirmation', 'Access Denied', 'Not Found']
};
// The six merges and the rename approved on 2026-10-26: brief entry -> registry name.
const ALIAS = {
  'Order Details and Processing': 'Order Details', 'Dispatch Overview@company': 'Dispatch Management', 'Support Ticket Queue': 'Support Ticket Management',
  'Invoice List': 'Invoices Overview', 'Payment History': 'Payments Overview', 'Prototype Settings': 'Portal Settings'
};
// Not in the brief: the 19 approved additions, plus My Profile for two roles that had none (flagged to the user).
const ADDITIONS = new Set([
  'CMP-NTF-01', 'PRI-NTF-01', 'SEC-NTF-01', 'TER-NTF-01', 'CMP-SUP-02', 'PRI-SUP-03', 'SEC-SUP-03', 'TER-SUP-03',
  'PRI-RET-01', 'PRI-RET-02', 'SEC-RET-01', 'SEC-RET-02', 'TER-RET-01', 'TER-RET-02', 'CMP-BIL-02', 'CMP-SCH-03', 'SEC-BIL-04',
  'CMP-PRO-02', 'TER-BIL-05' // added on 2026-10-26 at the user's request after the Phase 1 review
]);
const EXTRA_ROLE_TAGS = new Set(['PRI-PRO-02@MGR', 'SEC-PRO-02@MGR', 'PRI-ORD-04@MGR', 'PRI-ORD-05@MGR', 'PRI-INV-02@MGR', 'SEC-ORD-04@MGR', 'SEC-ORD-05@MGR', 'SEC-INV-02@MGR']);
const PINNED = { 'PRI-OWN-01': 'Dashboard', 'PRI-MGR-01': 'Dashboard', 'PRI-ACC-01': 'Dashboard', 'PRI-ORD-01': 'Order History', 'PRI-ORD-02': 'Order Details', 'PRI-INV-01': 'Inventory Overview' };
const EXPECTED = { company: 50, primary: 52, secondary: 45, tertiary: 40, authentication: 9 };
const BANNED = /\b(Qty|Amt|Mgr|Acct|Inv\.|No\.|Ref\.|Dept|Cust|Dist|Approx|Misc)\b/;

// ---------- Registry checks ----------
const byId = new Map();
const files = new Set();
for (const p of P.portals) {
  const codes = new Set();
  for (const s of p.screens) {
    if (byId.has(s.id)) fail(`duplicate ID ${s.id}`);
    byId.set(s.id, s);
    if (files.has(s.file)) fail(`two screens share the file ${s.file}`);
    files.add(s.file);
    if (codes.has(s.code)) fail(`duplicate code ${s.code} in ${p.id}`);
    codes.add(s.code);
    const roleCodes = p.roles.map((r) => r.code);
    for (const r of s.roles) if (!roleCodes.includes(r)) fail(`${s.id}: unknown role ${r}`);
    if (s.name === 'Dashboard' && s.roles.length !== 1) fail(`${s.id}: a dashboard belongs to exactly one role`);
    if (BANNED.test(s.name) || BANNED.test(s.description)) fail(`${s.id}: abbreviation in "${s.name}" / "${s.description}"`);
    if (s.description.length > 110) fail(`${s.id}: description is long (${s.description.length})`);
    if (s.parent) for (const code of new Set(typeof s.parent === 'object' ? Object.values(s.parent) : [s.parent])) {
      if (!p.screens.some((x) => x.code === code)) fail(`${s.id}: parent ${code} does not exist`);
    }
  }
  if (p.screens.length !== EXPECTED[p.id]) fail(`${p.id}: ${p.screens.length} screens, expected ${EXPECTED[p.id]}`);
  for (const r of p.roles) {
    const dashboards = p.screens.filter((s) => s.name === 'Dashboard' && s.roles[0] === r.code);
    if (p.id !== 'authentication' && dashboards.length !== 1) fail(`${p.id}/${r.code}: needs exactly one dashboard`);
  }
}
for (const [id, name] of Object.entries(PINNED)) if (!byId.get(id) || byId.get(id).name !== name) fail(`${id} must be ${name}`);

// ---------- Brief coverage: every (role, brief entry) has a screen that includes the role ----------
const matched = new Set();
for (const [key, entries] of Object.entries(BRIEF)) {
  const [pid, role] = key.split('/');
  const p = P.portal(pid);
  if (!p) { fail(`no portal ${pid}`); continue; }
  for (const entry of entries) {
    const target = entry.endsWith(' Dashboard') ? dash : ALIAS[entry + '@' + pid] || ALIAS[entry] || entry;
    const hit = p.screens.find((s) => s.name === target && s.roles.includes(role));
    if (!hit) { fail(`${key}: brief entry "${entry}" has no screen (looked for "${target}")`); continue; }
    matched.add(hit.id + '@' + role);
  }
}
for (const p of P.portals) for (const s of p.screens) for (const r of s.roles) {
  const k = s.id + '@' + r;
  if (!matched.has(k) && !ADDITIONS.has(s.id) && !EXTRA_ROLE_TAGS.has(k)) fail(`${k} "${s.name}" is not in the brief and is not an approved addition`);
}
for (const id of ADDITIONS) if (!byId.has(id)) fail(`approved addition ${id} is missing`);
if (ADDITIONS.size !== 19) fail('expected 19 additions');

// ---------- Files ----------
for (const s of byId.values()) {
  const exists = fs.existsSync(path.join(root, s.file));
  if (s.built && !exists) fail(`${s.id} is marked built but ${s.file} does not exist`);
  if (!s.built && exists) fail(`${s.file} exists but ${s.id} is not marked built in registry.js`);
}
const screensDir = path.join(root, 'screens');
const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]));
if (fs.existsSync(screensDir)) for (const f of walk(screensDir)) {
  const rel = path.relative(root, f).split(path.sep).join('/');
  if (f.endsWith('.html') && !files.has(rel)) fail(`${rel} is not in the registry`);
  if (f.endsWith('.html') && !fs.readFileSync(f, 'utf8').includes('data-screen="')) fail(`${rel} has no data-screen`);
}
// Built screens must not use short forms or localStorage (the brief bans it).
for (const s of byId.values()) if (s.built && fs.existsSync(path.join(root, s.file))) {
  const html = fs.readFileSync(path.join(root, s.file), 'utf8');
  const text = html.replace(/<(script|style)[\s\S]*?<\/\1>/g, '').replace(/<[^>]+>/g, ' ');
  if (BANNED.test(text)) fail(`${s.file}: abbreviation on screen`);
  if (/localStorage|sessionStorage/.test(html)) fail(`${s.file}: uses browser storage`);
}

// ---------- Inventory document ----------
const total = P.count();
const built = P.built();
let md = `# Screen inventory\n\n_Generated by \`node tools/inventory.mjs\` from \`assets/registry.js\`. Do not edit by hand._\n\n`;
md += `## Summary\n\n| Portal | Roles | Screens | Built |\n|---|---|---|---|\n`;
for (const p of P.portals) md += `| ${p.card} | ${p.roles.length} | ${p.screens.length} | ${p.screens.filter((s) => s.built).length} |\n`;
md += `| **Total** | **11 roles** | **${total}** | **${built}** |\n\n`;
md += `A screen used by several roles is designed once and listed under each role; it counts once in the portal total.\n\n`;
md += `## Screens per role\n\n| Portal | Role | Screens the role sees |\n|---|---|---|\n`;
for (const p of P.portals) for (const r of p.roles) md += `| ${p.card} | ${r.label} | ${P.forRole(p, r.code).length} |\n`;
md += `\n`;
for (const p of P.portals) {
  md += `## ${p.card}\n\n`;
  for (const r of p.roles) {
    md += `### ${p.id === 'authentication' ? 'Screens' : r.label}\n\n| ID | Screen name | Menu section | Status | Description |\n|---|---|---|---|---|\n`;
    for (const s of P.forRole(p, r.code)) {
      md += `| ${s.id} | ${P.fullName(p, s, r.code)} | ${P.group(s, r.code)} | ${s.built ? 'Built' : 'Planned'} | ${s.description} |\n`;
    }
    md += `\n`;
  }
}
fs.writeFileSync(path.join(root, 'docs/SCREEN-INVENTORY.md'), md);

if (errors.length) {
  console.error(errors.map((e) => 'FAIL ' + e).join('\n'));
  process.exit(1);
}
console.log(`OK: ${total} screens, ${built} built, ${P.portals.length - 1} portals plus sign-in, ${P.portals.reduce((n, p) => n + p.roles.length, 0) - 1} roles. Wrote docs/SCREEN-INVENTORY.md`);
