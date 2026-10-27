// Do the list controls tell the truth? For every list on every screen: each tab shows as many rows as its badge says, search finds a row that
// exists, and every dropdown option returns at least one row. Needs Playwright. Usage: node tools/lists-check.js [ID prefix]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.resolve(__dirname, '..');
const only = process.argv[2] || '';
const sb = { window: {} }; vm.runInNewContext(fs.readFileSync(path.join(root, 'assets/registry.js'), 'utf8'), sb);
const P = sb.window.PORTAL, targets = [];
for (const p of P.portals) for (const s of p.screens) if (s.built && s.id.startsWith(only)) for (const r of s.roles) targets.push({ id: s.id, role: r, url: 'file://' + path.join(root, s.file) + (r !== s.roles[0] && r !== 'ALL' ? `?role=${r}` : '') });

const check = () => {
  const out = [], A = window.APP; if (!A || !A.lists) return out;
  const vis = (l) => l.items.filter((it) => !it.hidden && !it.classList.contains('row-gone')).length;
  const name = (l) => (l.noun || 'list') + ' (' + l.kind + ')';
  A.lists.forEach((l) => {
    if (l.el.closest('[hidden]')) return;
    const total = l.items.filter((it) => !it.classList.contains('row-gone')).length;
    if (l.tabs) l.tabs.forEach((t) => {
      t.el.click();
      const want = t.b ? +t.b.textContent : null, got = l.items.filter((it) => !it.hidden).length + (l.pg ? 0 : 0);
      const matching = l.items.filter((it) => !it.classList.contains('row-gone') && l.matches(it)).length;
      if (want !== null && matching !== want) out.push(`${name(l)} tab "${t.label}": badge ${want}, rows ${matching}`);
      if (matching && !got) out.push(`${name(l)} tab "${t.label}": has ${matching} rows but shows none`);
    });
    if (l.tabs) { const init = l.tabs.filter((t) => t.initial)[0] || l.tabs[0]; init.el.click(); }
    const box = (l.card || document).querySelector('.finder input');
    if (box && total >= 2) {
      const first = l.items.filter((it) => !it.classList.contains('row-gone'))[0];
      const cell = first.cells ? [...first.cells].map((c) => c.textContent.trim()).filter((t) => t.length > 3 && !/^[₹\d,.\s%/-]+$/.test(t))[1] || '' : first.textContent.trim();
      const term = (cell || '').split(/\s+/)[0].slice(0, 8);
      if (term.length > 2) { box.value = term; box.dispatchEvent(new Event('input')); const n = vis(l); if (n < 1) out.push(`${name(l)} search "${term}" finds nothing though row 1 has it`); box.value = ''; box.dispatchEvent(new Event('input')); }
    }
    l.filters.forEach((f) => {
      if (!f.options) return;
      f.options().forEach((v) => { f.value = v; l.apply(true); if (vis(l) < 1 && l.items.length) out.push(`${name(l)} filter ${f.label} = "${v}" shows no rows`); });
      f.value = null; l.apply(true);
    });
    if (vis(l) !== Math.min(total, l.pg ? 10 : total)) out.push(`${name(l)}: ${vis(l)} rows shown after resetting, expected ${Math.min(total, l.pg ? 10 : total)}`);
  });
  return out;
};

(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } }); let bad = 0, lists = 0;
  const queue = targets.slice();
  await Promise.all([1, 2, 3, 4].map(async () => {
    const page = await ctx.newPage();
    while (queue.length) {
      const t = queue.shift();
      try { await page.goto(t.url); await page.waitForTimeout(80); lists += await page.evaluate(() => (window.APP && window.APP.lists ? window.APP.lists.length : 0)); const out = await page.evaluate(check); out.forEach((o) => { bad++; console.log(`${t.id} ${t.role}: ${o}`); }); }
      catch (e) { bad++; console.log(`${t.id} ${t.role}: ERROR ${String(e).slice(0, 120)}`); }
    }
    await page.close();
  }));
  await b.close();
  console.log(bad ? `${bad} problem(s) in ${lists} lists` : `ALL OK: ${lists} lists checked`);
  process.exit(bad ? 1 : 0);
})();
