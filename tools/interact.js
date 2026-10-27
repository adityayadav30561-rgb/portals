// Dead-control audit. Opens every built screen, for every role that sees it, straight from disk (file://) and clicks every control:
// buttons, link-buttons without a destination, dropdowns, tabs, steppers, checkboxes and radios, sort headers, pager buttons, icon buttons.
// A control passes when clicking it changes something observable: the page, the address, a dialog, a toast, a menu, a download, a print or a file picker.
// Anything else is a dead control and is listed. The run must end with "0 dead controls" (CLAUDE.md, "No dead controls").
// Needs Playwright. Usage: node tools/interact.js [ID prefix] [--json out.json] [--workers 4] [--verbose]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const flag = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
const only = args.filter((a, i) => !a.startsWith('--') && (i === 0 || !args[i - 1].startsWith('--')))[0] || '';
const workers = +flag('--workers', 4), jsonOut = flag('--json', ''), verbose = args.includes('--verbose');
const sb = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(root, 'assets/registry.js'), 'utf8'), sb);
const P = sb.window.PORTAL;

const targets = [];
for (const p of P.portals) for (const s of p.screens) if (s.built && s.id.startsWith(only)) for (const r of s.roles) {
  targets.push({ id: s.id, role: r, url: 'file://' + path.join(root, s.file) + (r !== s.roles[0] && r !== 'ALL' ? `?role=${r}` : '') + (s.file.includes('?') ? '' : '') });
}

// Everything that is meant to be clicked.
const CONTROLS = [
  'main button:not([disabled]):not(.on)', 'main a.btn:not([href]):not([aria-disabled])', 'main .sel', 'main .tabs [data-tab]:not(.on)', 'main .qty > span[role=button]:not([aria-disabled=true])',
  'main input[type=checkbox]', 'main input[type=radio]:not(:checked)', 'main th[data-sort]', 'main .pg .pages button:not([disabled]):not(.on)', 'main .view-toggle [role=button]:not(.on)',
  'main [role=button]:not([aria-disabled=true]):not(.on)', 'main summary', 'main label.radio:not(.on)', '.top .icon-btn:not([href])', '.top .who > button', 'main .chip[role=button]'
].join(',');

const signature = () => {
  const main = document.querySelector('main') || document.body;
  const vals = [...document.querySelectorAll('input, select, textarea')].map((i) => (i.type === 'checkbox' || i.type === 'radio' ? i.checked : i.value)).join('|');
  const over = [...document.querySelectorAll('.toast, .modal, .pop, .menu.open')].map((e) => e.outerHTML).join('');
  return location.href + '#' + main.innerHTML.length + '#' + main.innerHTML + '#' + vals + '#' + over + '#' + document.querySelectorAll('[aria-expanded="true"]').length;
};

const describe = (el) => {
  const t = (el.getAttribute('aria-label') || el.textContent || el.getAttribute('placeholder') || '').replace(/\s+/g, ' ').trim().slice(0, 50);
  const c = [...el.classList].slice(0, 3).join('.');
  return `${el.tagName.toLowerCase()}${c ? '.' + c : ''} "${t}"`;
};

(async () => {
  const b = await chromium.launch();
  const dead = [], errors = []; let clicked = 0, pages = 0;
  const queue = targets.slice();
  const work = async () => {
    const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, acceptDownloads: true });
    await ctx.addInitScript(() => { window.__print = 0; window.print = () => { window.__print++; }; window.open = () => { window.__print++; return null; }; });
    while (queue.length) {
      const t = queue.shift(); pages++;
      const page = await ctx.newPage();
      let downloaded = 0, chooser = 0, perr = [];
      page.on('download', () => downloaded++);
      page.on('filechooser', async (fc) => { chooser++; try { await fc.setFiles([]); } catch (e) { /* closed */ } });
      page.on('pageerror', (e) => perr.push(String(e)));
      page.on('console', (m) => m.type() === 'error' && perr.push(m.text()));
      page.on('dialog', (d) => d.dismiss().catch(() => {}));
      try {
        await page.goto(t.url); await page.waitForTimeout(120);
        const n = await page.evaluate((sel) => document.querySelectorAll(sel).length, CONTROLS);
        for (let i = 0; i < n; i++) {
          const info = await page.evaluate(([sel, i]) => {
            const el = [...document.querySelectorAll(sel)][i]; if (!el) return null;
            const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
            if (!r.width || !r.height || cs.visibility === 'hidden' || el.closest('[hidden]') || el.closest('.modal')) return { skip: true };
            el.scrollIntoView({ block: 'center' });
            const r2 = el.getBoundingClientRect(), hit = document.elementFromPoint(r2.x + r2.width / 2, r2.y + r2.height / 2);
            if (!hit || !(hit === el || el.contains(hit) || hit.contains(el))) return { skip: true };   // covered or inside a closed section: not clickable
            return { skip: false };
          }, [CONTROLS, i]);
          if (!info || info.skip) continue;
          const before = await page.evaluate(signature), d0 = downloaded, c0 = chooser, p0 = await page.evaluate(() => window.__print);
          const handle = (await page.$$(CONTROLS))[i];
          if (!handle) continue;
          await page.evaluate(() => { window.__marker = 1; });
          try { await handle.click({ timeout: 2500, force: false }); } catch (e) { try { await handle.click({ timeout: 1500, force: true }); } catch (e2) { dead.push({ ...t, control: await handle.evaluate((el) => el.outerHTML.slice(0, 90)).catch(() => '?'), why: 'not clickable: ' + String(e2).split('\n')[0].slice(0, 90) }); continue; } }
          clicked++;
          await page.waitForTimeout(90);
          const gone = !(await page.evaluate(() => window.__marker === 1).catch(() => false));
          let after, changed = false;
          try { after = await page.evaluate(signature); changed = after !== before; } catch (e) { changed = true; }
          const extra = downloaded > d0 || chooser > c0 || (await page.evaluate(() => window.__print).catch(() => 1)) > p0;
          if (!(changed || gone || extra)) {
            const label = await handle.evaluate((el) => { const t = (el.getAttribute('aria-label') || el.textContent || el.getAttribute('placeholder') || '').replace(/\s+/g, ' ').trim().slice(0, 50); return el.tagName.toLowerCase() + ([...el.classList].length ? '.' + [...el.classList].slice(0, 3).join('.') : '') + ' "' + t + '"'; }).catch(() => '?');
            dead.push({ id: t.id, role: t.role, control: label, why: 'no observable change' });
          }
          if (gone) { await page.goto(t.url); await page.waitForTimeout(100); }
          else { await page.keyboard.press('Escape').catch(() => {}); await page.evaluate(() => document.querySelectorAll('.modal').forEach((m) => m.remove())); }
        }
        if (perr.length) errors.push({ id: t.id, role: t.role, errors: [...new Set(perr)].slice(0, 3) });
      } catch (e) { errors.push({ id: t.id, role: t.role, errors: [String(e).slice(0, 160)] }); }
      await page.close();
      if (verbose) console.log(`${t.id} ${t.role}: ${dead.filter((x) => x.id === t.id && x.role === t.role).length} dead`);
    }
    await ctx.close();
  };
  await Promise.all(Array.from({ length: workers }, work));
  await b.close();
  // summary grouped by control label
  const groups = {};
  dead.forEach((d) => { const k = d.control.replace(/\d+/g, '#'); (groups[k] = groups[k] || []).push(d.id + (d.role && d.role !== 'ALL' ? ':' + d.role : '')); });
  Object.keys(groups).sort((a, b) => groups[b].length - groups[a].length).forEach((k) => console.log(`${String(groups[k].length).padStart(4)}  ${k}   [${[...new Set(groups[k])].slice(0, 4).join(', ')}${new Set(groups[k]).size > 4 ? ', …' : ''}]`));
  errors.forEach((e) => console.log('ERROR', e.id, e.role, e.errors.join(' | ')));
  console.log(`\n${pages} screen views, ${clicked} controls clicked, ${dead.length} dead controls, ${errors.length} pages with errors`);
  if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify({ dead, errors }, null, 1));
  process.exit(dead.length || errors.length ? 1 : 0);
})();
