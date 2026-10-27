// End-to-end checks of the behaviour layer, from disk (file://). Needs Playwright. Usage: node tools/e2e.js
// Parity: the designed draft orders must produce exactly the totals the static Order Builder screens show.
// Flows: Primary, Secondary and Tertiary ordering (stock limit, credit block, rebate threshold, numbering), lists (search, tabs, sort, filters),
// forms and records, approvals, replies, downloads (CSV and PDF).
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const R = 'file://' + path.resolve(__dirname, '..', 'screens') + '/';
let fails = 0, passes = 0;
const ok = (c, m) => { if (c) passes++; else { fails++; console.log('FAIL ' + m); } };

(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 }, acceptDownloads: true }); const p = await ctx.newPage();
  const errs = []; p.on('console', (m) => m.type() === 'error' && errs.push(m.text())); p.on('pageerror', (e) => errs.push(String(e) + ' @ ' + p.url().split('/screens/')[1]));
  const txt = async (sel) => (await p.$eval(sel, (e) => e.innerText)).replace(/\s+/g, ' ').trim();
  const search = () => p.evaluate(() => location.search.slice(1));
  const fill = async (label, v) => { const f = await p.$(`.field:has(label:text-is("${label}")) input, .field:has(label:text-is("${label}")) textarea`); if (f) await f.fill(v); };
  const rows = () => p.$$eval('main table.tbl tbody tr:not([hidden])', (r) => r.map((x) => x.cells[0].innerText.trim()));

  // ---- parity
  for (const [po, tot, avail] of [['primary', '₹9,49,752', '₹15.64 lakh'], ['secondary', '₹2,93,820', '₹2.46 lakh'], ['tertiary', '₹1,04,784', '₹1.33 lakh']]) {
    await p.goto(R + po + '/order-builder.html');
    ok((await p.$eval('dl.kv.total dd', (e) => e.innerText)) === tot, po + ' builder total is ' + tot);
    ok((await p.$$eval('dl.kv.total dd', (e) => e[e.length - 1].innerText)) === avail, po + ' credit available is ' + avail);
  }

  // ---- lists
  await p.goto(R + 'primary/order-history.html');
  ok((await p.$$eval('.tabs span', (s) => s.map((x) => x.innerText.replace(/\s+/g, ' ')))).join('|').startsWith('All Orders 10'), 'tab badges count the rows');
  await p.fill('.finder input', '10447'); ok((await rows()).join() === 'ORD-2026-10447', 'search narrows rows'); await p.fill('.finder input', '');
  await p.click('.tabs span:has-text("Delivered")'); ok((await rows()).length === (await p.$eval('.tabs span:has-text("Delivered") b', (b) => +b.innerText)), 'tab shows as many rows as its badge');
  await p.click('.tabs span:has-text("All Orders")');
  await p.click('th:has-text("Value")'); ok((await rows())[0] === 'ORD-2026-10482', 'sort by value, high first'); await p.click('th:has-text("Value")'); ok((await rows())[0] === 'ORD-2026-10265', 'sort by value, low first');
  await p.click('.sel:has-text("Payment")'); await p.click('.pop .opt:has-text("Paid")'); ok((await p.$eval('.pg', (e) => e.innerText)).includes('of 4'), 'filter updates the "Showing" line');
  await p.goto(R + 'primary/product-catalogue.html');
  await p.fill('.finder input', 'walnut'); ok((await p.$$('.pcard:not([hidden])')).length === 1, 'catalogue search'); await p.fill('.finder input', '');
  await p.click('.sel:has-text("Sort by")'); await p.click('.pop .opt:has-text("Price, high to low")'); ok((await p.$$eval('.pcard:not([hidden]) h3', (h) => h[0].innerText)) === 'Brushed Copper Metallic Laminate', 'catalogue sort by price');

  // ---- Primary order flow
  await p.goto(R + 'primary/product-catalogue.html');
  ok((await txt('.head .acts a .chip')) === '5', 'catalogue draft count equals the draft'); ok(await p.$eval('.pcard:first-child .qty input', (i) => i.value) === '200', 'card shows the draft quantity');
  await p.click('.pcard:has(.tag.mono:text("LM-CHR-007")) .buy button'); ok((await txt('.head .acts a .chip')) === '6', 'add to order raises the count');
  await p.click('.head .acts a'); await p.waitForURL('**/place-order.html*'); ok((await p.$$('aside tbody tr')).length === 6, 'place order lists the 6 lines');
  const row = 'tr:has(td.mono:text("LM-CHR-007"))'; await p.fill(row + ' .qty input', '0'); await p.press(row + ' .qty input', 'Tab'); ok((await p.$$('aside tbody tr')).length === 5, 'zero removes a line');
  await p.click('aside a.btn.pri'); await p.waitForURL('**/order-builder.html*'); ok((await txt('dl.kv.total dd')) === '₹9,49,752', 'builder total survives the round trip');
  for (const sku of ['LM-OAK-004', 'LM-CAL-003', 'LM-SLT-005']) await p.click('tr[data-sku="' + sku + '"] .icon-btn');
  ok(await p.$eval('main section.card.flush header .chip', (e) => e.hidden), 'rebate disappears below the threshold');
  await p.click('.toasts .ta'); ok((await p.$$('tr[data-sku]')).length === 3, 'undo restores a removed line');
  await p.fill('#date', '01/01/2020'); await p.click('main .head .acts a.btn.pri'); ok((await p.$$('.field.invalid')).length === 1, 'past delivery date is refused'); await p.fill('#date', '31/10/2026');
  await p.click('main .head .acts a.btn.pri'); await p.waitForURL('**/order-confirmation.html*'); ok((await txt('.big-value.mono')) === 'ORD-2026-10482', 'first order takes the designed number');
  await p.click('a:has-text("View Order Details")'); await p.waitForURL('**/order-details.html*'); ok((await txt('h1')) === 'ORD-2026-10482', 'the new order has its own details');
  const st = await search(); await p.goto(R + 'primary/order-history.html?' + st); ok((await rows())[0] === 'ORD-2026-10482', 'order history lists it'); ok((await p.$$eval('main .kpi', (k) => k.map((x) => x.innerText.replace(/\s+/g, ' ')))).some((t) => /Awaiting Confirmation 1/.test(t)), 'history tiles follow the rows');

  // ---- Secondary: stock limit, credit block, pickup, numbering
  await p.goto(R + 'secondary/product-catalogue.html');
  ok(await p.$eval('.pcard:has(.tag.mono:text("LM-STN-009")) .buy button', (b) => b.disabled), 'out-of-stock product cannot be added');
  const cal = '.pcard:has(.tag.mono:text("LM-CAL-003"))'; await p.fill(cal + ' .qty input', '200'); await p.press(cal + ' .qty input', 'Tab'); await p.click(cal + ' .buy button');
  ok((await txt('.toasts .toast .tt')).includes('Only 125 sheets'), 'stock limit message');
  await p.goto(R + 'secondary/place-order.html?' + (await search())); const w = 'tr:has(td.mono:text("LM-WNT-001"))'; await p.fill(w + ' .qty input', '500'); await p.press(w + ' .qty input', 'Tab');
  await p.click('aside a.btn.pri'); await p.waitForURL('**/order-builder.html*'); await p.click('main .head .acts a.btn.pri');
  ok((await txt('.toasts .toast:last-child .tt')).includes('above the credit available'), 'credit limit blocks submit');
  await p.fill('tr[data-sku="LM-WNT-001"] .qty input', '60'); await p.press('tr[data-sku="LM-WNT-001"] .qty input', 'Tab'); ok((await txt('dl.kv.total dd')) === '₹2,93,820', 'total back to the designed 2,93,820');
  await p.click('main .head .acts a.btn.pri'); await p.waitForURL('**/order-confirmation.html*'); ok((await txt('.big-value.mono')) === 'SAL-2026-3042', 'secondary number');
  await p.goto(R + 'secondary/product-catalogue.html?' + (await search())); ok((await txt('.head .acts a .chip')) === '0', 'cart is empty after submitting');
  await p.click('.pcard:has(.tag.mono:text("LM-ARC-002")) .buy button'); await p.click('.toasts .ta'); await p.waitForURL('**/place-order.html*');
  await p.click('aside a.btn.pri'); await p.waitForURL('**/order-builder.html*'); await p.click('main .head .acts a.btn.pri'); await p.waitForURL('**/order-confirmation.html*'); ok((await txt('.big-value.mono')) === 'SAL-2026-3043', 'second order number');

  // ---- Tertiary
  await p.goto(R + 'tertiary/order-builder.html'); await p.click('main .head .acts a.btn.pri'); await p.waitForURL('**/order-confirmation.html*'); ok((await txt('.big-value.mono')) === 'TSL-2026-0413', 'tertiary number');
  await p.goto(R + 'tertiary/product-catalogue.html?role=SLS'); ok(await p.$$eval('.buy', (b) => b.every((x) => x.hidden || getComputedStyle(x).display === 'none')), 'Sales Executive cannot order');

  // ---- forms and records
  await p.goto(R + 'primary/create-user.html'); for (const i of await p.$$('.field input')) await i.fill('');
  await p.click('main .head .acts .btn.pri'); ok((await p.$$('.field.invalid')).length >= 3, 'empty form is flagged');
  await fill('First Name', 'Meena'); await fill('Last Name', 'Kulkarni'); await fill('Email Address', 'meena.kulkarni@distributoralpha.example'); await fill('Mobile Number', '+91 90000 21009');
  await p.click('label.radio:has-text("Accountant")'); await p.click('main .head .acts .btn.pri'); await p.waitForURL('**/user-management.html*');
  ok((await txt('main table.tbl tbody tr:first-child')).startsWith('Meena Kulkarni Accountant'), 'new user is first in the list'); await p.waitForSelector('.toasts .toast'); ok((await txt('.toasts .toast .tt')).includes('Invitation sent'), 'confirmation toast on the list');
  await p.goto(R + 'primary/pending-dealer-requests.html?role=MGR'); await p.click('main table.tbl tbody tr:first-child button:has-text("Approve")'); ok((await txt('main table.tbl tbody tr:first-child')).endsWith('Approved'), 'approve changes the row');
  const st2 = await search(); await p.goto(R + 'primary/pending-dealer-requests.html?' + st2); ok((await txt('main table.tbl tbody tr:first-child')).endsWith('Approved'), 'approval persists to the next screen');
  await p.click('main table.tbl tbody tr:nth-child(2) button:has-text("Reject")'); await p.click('.modal [data-ok]'); ok((await p.$$('.modal .field.invalid')).length === 1, 'reject asks for a reason');
  await p.goto(R + 'primary/support-ticket-details.html'); await p.click('button:has-text("Send Reply")'); ok((await p.$$('.reply .err')).length === 1, 'empty reply is refused');
  await p.fill('.reply textarea', 'Thanks, please collect on Friday.'); await p.click('button:has-text("Send Reply")'); ok((await txt('.thread .msg:last-child')).includes('please collect on Friday'), 'reply joins the conversation');
  await p.click('main .head button:has-text("Close Ticket")'); await p.click('.modal [data-ok]'); ok((await p.$$eval('.title-row .chip', (c) => c.map((x) => x.innerText))).includes('Closed'), 'ticket closes');

  // ---- the Owner stays the Owner after a form that lists elsewhere
  await p.goto(R + 'primary/add-dealer-request.html'); await p.click('main .head .acts button:has-text("Submit Request")'); await p.waitForURL('**/dealer-network.html*');
  ok((await txt('.who .nm')) === 'Rajesh Menon', 'Add Dealer Request returns the Owner to Dealer Network, not to the Manager\'s list');
  await p.goto(R + 'primary/pending-dealer-requests.html?role=MGR&' + (await search()).replace(/^role=[^&]*&?/, '')); ok((await txt('main table.tbl tbody tr:first-child')).includes('Dealer Omkar') || (await txt('main table.tbl tbody tr:first-child')).includes('Awaiting'), 'the Manager sees the request in the pending list');
  // ---- rows open their own record
  await p.goto(R + 'primary/order-history.html'); await p.click('main table.tbl tbody tr:nth-child(4) a'); await p.waitForURL('**/order-details.html*');
  ok((await txt('h1')) === 'ORD-2026-10431', 'a history row opens its own order'); ok((await p.$$eval('.title-row .chip', (c) => c.map((x) => x.innerText))).join() === 'Delivered,Partly Paid', 'with its own status and payment');
  ok((await p.$$('main table.tbl tbody tr')).length >= 3, 'and its own lines');
  await p.goto(R + 'secondary/order-history.html'); await p.click('main table.tbl tbody tr:nth-child(2) a'); await p.waitForURL('**/order-details.html*'); ok((await txt('h1')) === 'SAL-2026-3040', 'secondary row opens its own order');
  // ---- sale entry: the credit card follows the sale
  await p.goto(R + 'primary/secondary-sales-entry.html'); const before = await txt('dl.kv:has(dt:text("This Sale")) dd:nth-of-type(3)');
  const wnt = 'tr:has(td.mono:text("LM-WNT-001"))'; await p.fill(wnt + ' .qty input', '300'); await p.press(wnt + ' .qty input', 'Tab');
  ok((await txt('dl.kv:has(dt:text("This Sale")) dd:nth-of-type(3)')) !== before, 'dealer credit card follows the quantities');
  await p.selectOption('#dl', { label: 'Dealer Kunal, Panaji' }); ok((await txt('dl.kv:has(dt:text("This Sale")) dd:nth-of-type(1)')) !== '₹8.00 lakh', 'dealer credit card follows the dealer');
  await p.fill(wnt + ' .qty input', '900'); await p.press(wnt + ' .qty input', 'Tab'); await p.click('main .head .acts button:has-text("Record Sale")'); ok((await txt('.toasts .toast:last-child .tt')).includes('above the credit available'), 'a sale above the dealer credit is refused');
  // ---- top-bar search
  await p.goto(R + 'primary/owner-dashboard.html'); await p.fill('.top .search input', 'walnut'); ok((await p.$$('.pop .opt')).length >= 1, 'top-bar search suggests'); await p.press('.top .search input', 'Enter'); await p.waitForURL('**/product-catalogue.html*');
  ok((await p.$$('.pcard:not([hidden])')).length === 1, 'search for walnut lands on the catalogue with one card');
  // ---- downloads
  await p.goto(R + 'primary/order-history.html'); const [d1] = await Promise.all([p.waitForEvent('download'), p.click('button:has-text("Export Orders")')]);
  ok(/\.csv$/.test(d1.suggestedFilename()) && fs.readFileSync(await d1.path(), 'utf8').includes('Order Number,Order Date'), 'CSV export');
  await p.goto(R + 'primary/order-details.html'); const [d2] = await Promise.all([p.waitForEvent('download'), p.click('button:has-text("Download Order Copy")')]);
  const pdf = fs.readFileSync(await d2.path()).toString(); ok(pdf.startsWith('%PDF-1.4') && pdf.includes('%%EOF') && pdf.includes('ORD-2026-10447'), 'PDF download');

  ok(!errs.length, 'no console errors' + (errs.length ? ': ' + errs.join(' | ') : ''));
  console.log(fails ? `${fails} FAILED, ${passes} passed` : `ALL ${passes} CHECKS PASSED`);
  await b.close(); process.exit(fails ? 1 : 0);
})();
