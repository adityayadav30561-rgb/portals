// Opens every built screen, for every role that sees it, straight from disk (file://) at three sizes and fails on:
// console errors, horizontal scroll, Inter not loaded, links to files that do not exist, leftover "#" links,
// abbreviations in the text that is actually rendered, browser storage use.
// Needs Playwright (npm i -D playwright). Usage: node tools/verify.js [screenshot-folder] [ID-prefix]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.resolve(__dirname, '..');
const out = process.argv[2], only = process.argv[3] || '';
const sb = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(root, 'assets/registry.js'), 'utf8'), sb);
const P = sb.window.PORTAL;
const BANNED = /\b(Qty|Amt|Mgr|Acct|Dept|Cust|Dist|Approx|Misc|YTD|MTD|FY|ETA|PO|CGST|SGST|vs|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|UPI|PAN|GSTIN|PIN|pcs)\b|\d\s?(L|Cr|K)\b|\bInv\.|\bNo\./;
const SIZES = [[1440, 900], [1366, 768], [390, 844]];

const targets = ['index.html', ...P.portals.filter((p) => p.id !== 'authentication').map((p) => `directory/${p.id}.html`), 'directory/authentication.html'];
const shots = [];
for (const p of P.portals) for (const s of p.screens) if (s.built && s.id.startsWith(only)) for (const r of s.roles) {
  targets.push(s.file + (r !== s.roles[0] && r !== 'ALL' ? `?role=${r}` : ''));
}
if (only) targets.splice(0, targets.findIndex((t) => t.startsWith('screens')) < 0 ? 0 : targets.findIndex((t) => t.startsWith('screens')));

(async () => {
  const b = await chromium.launch();
  let bad = 0;
  for (const [w, h] of SIZES) {
    const ctx = await b.newContext({ viewport: { width: w, height: h } });
    for (const t of targets) {
      const page = await ctx.newPage();
      const errs = [];
      page.on('console', (m) => m.type() === 'error' && errs.push(m.text()));
      page.on('pageerror', (e) => errs.push(String(e)));
      page.on('requestfailed', (r) => errs.push('request failed ' + r.url()));
      await page.goto('file://' + path.join(root, t));
      await page.waitForTimeout(250);
      const r = await page.evaluate(async () => {
        await document.fonts.ready;
        const links = [...document.querySelectorAll('a')].map((a) => a.getAttribute('href'));
        return {
          sw: document.documentElement.scrollWidth, iw: innerWidth, font: document.fonts.check('600 16px Inter'),
          hrefs: [...new Set(links.filter((h) => h && !h.startsWith('mailto')))], hash: links.filter((h) => h === '#').length,
          wideTables: innerWidth >= 1366 ? [...document.querySelectorAll('.table-wrap')].filter((t) => t.scrollWidth > t.clientWidth + 1).length : 0,
          tiny: [...document.querySelectorAll('body *')].filter((e) => e.children.length === 0 && e.textContent.trim() && parseFloat(getComputedStyle(e).fontSize) < 12.99 && !e.closest('script,style')).map((e) => `${e.tagName.toLowerCase()}.${e.className && e.className.baseVal === undefined ? e.className : ''} "${e.textContent.trim().slice(0, 24)}"`).slice(0, 3),
          prose: [...document.querySelectorAll('main p, main .head p')].filter((e) => !e.closest('.state, .auth-box')).map((e) => e.textContent.trim().slice(0, 40)).slice(0, 3),
          text: document.body.innerText, storage: /localStorage|sessionStorage/.test(document.documentElement.outerHTML)
        };
      });
      const problems = [];
      if (r.sw > r.iw) problems.push(`horizontal scroll ${r.sw} > ${r.iw}`);
      if (!r.font) problems.push('Inter not loaded');
      if (r.tiny.length) problems.push('text under 13px: ' + r.tiny.join(', '));
      if (r.prose.length) problems.push('paragraph text on a screen: ' + r.prose.join(' | '));
      if (r.wideTables) problems.push(`${r.wideTables} table(s) scroll sideways inside their card on a desktop screen`);
      if (errs.length) problems.push('errors: ' + errs.join(' | '));
      if (r.hash) problems.push(`${r.hash} link(s) with href="#"`);
      if (r.storage) problems.push('uses browser storage');
      const m = r.text.match(BANNED); if (m) problems.push(`abbreviation "${m[0]}" in: ...${r.text.slice(Math.max(0, m.index - 25), m.index + 25).replace(/\s+/g, ' ')}...`);
      const missing = r.hrefs.filter((hh) => { const u = new URL(hh, 'file://' + path.join(root, t)); return u.protocol === 'file:' && !fs.existsSync(decodeURIComponent(u.pathname)); });
      if (missing.length) problems.push('links to missing files: ' + missing.join(', '));
      console.log(`${w} ${t}: ${problems.length ? 'FAIL ' + problems.join('; ') : 'ok'}`);
      if (problems.length) bad++;
      if (out) { fs.mkdirSync(out, { recursive: true }); const full = await page.evaluate(() => document.documentElement.scrollHeight); await page.setViewportSize({ width: w, height: Math.max(h, full) }); await page.waitForTimeout(150); await page.screenshot({ path: path.join(out, `${w}-${t.replace(/[\/?=]/g, '_')}.png`), fullPage: false }); }
      await page.close();
    }
    await ctx.close();
  }
  await b.close();
  console.log(bad ? `FAILED: ${bad} problem page(s)` : 'ALL OK');
  process.exit(bad ? 1 : 0);
})();
