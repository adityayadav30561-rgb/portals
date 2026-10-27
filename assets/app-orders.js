/*
 * Behaviour layer, part 3: the order flow in the three ordering portals (Primary, Secondary, Tertiary).
 *   Product Catalogue / Product Details  -> add to the order draft (cart)
 *   Place Order                          -> quantities per product, draft summary
 *   Order Builder                        -> lines, delivery details, totals, credit check, submit
 *   Order Confirmation                   -> the submitted order
 *   Order History / Order Details        -> the submitted order appears and has its own details
 * Prices, stock, rebate and credit rules come from assets/catalog.js (written by tools/author/runtime_data.py from data.py).
 * The cart lives in the URL state (see app-core.js). Until it is changed it is the designed draft, so a screen opens as designed.
 */
(function () {
  var A = window.APP, C = window.CATALOG;
  if (!C || !A.portal) return;
  var cfg = C.portals[A.portal.id];
  if (!cfg) return;                                       // the Company portal does not order
  var q = A.q, qa = A.qa, esc = A.esc, M = A.fmtM, ML = A.fmtML, N = A.fmtN;
  var pid = A.portal.id, sid = A.screen, part = sid.split('-').slice(1).join('-');
  var PRODUCTS = {}; C.products.forEach(function (p) { PRODUCTS[p.sku] = p; });
  var person = (A.portal.roles.filter(function (r) { return r.code === A.role; })[0] || {}).person || '';
  var params = new URLSearchParams(location.search);

  // ---------- Cart ----------
  A.cart = {
    lines: function () { var c = (A.state.c || {})[pid]; return (c ? c : cfg.draft).map(function (l) { return [l[0], l[1]]; }); },
    set: function (lines) { A.state.c = A.state.c || {}; A.state.c[pid] = lines.filter(function (l) { return l[1] > 0; }); A.save(); updateBadge(); },
    qty: function (sku) { var l = A.cart.lines().filter(function (x) { return x[0] === sku; })[0]; return l ? l[1] : 0; },
    setQty: function (sku, n) {
      var ls = A.cart.lines(), hit = false;
      ls = ls.map(function (l) { if (l[0] === sku) { hit = true; return [sku, n]; } return l; });
      if (!hit && n > 0) ls.push([sku, n]);
      A.cart.set(ls);
    },
    count: function () { return A.cart.lines().length; }
  };
  var orders = function () { return (A.state.o || {})[pid] || []; };
  var form = function () { return ((A.state.f || {})[pid]) || {}; };
  var setForm = function (patch) { A.state.f = A.state.f || {}; var f = A.state.f[pid] = A.state.f[pid] || {}; for (var k in patch) f[k] = patch[k]; A.save(); };

  // ---------- Pricing ----------
  var price = function (sku, qty) {
    if (cfg.mode === 'flat') return cfg.price[sku];
    var s = cfg.slabs[sku]; return qty >= 200 ? s[2] : qty >= 50 ? s[1] : s[0];
  };
  var sessionSheets = function () { return orders().reduce(function (n, o) { return n + o.sheets; }, 0); };
  A.calc = function (lines, transport, noRebate) {
    var rows = lines.map(function (l) { var p = price(l[0], l[1]); return { sku: l[0], qty: l[1], price: p, amount: l[1] * p }; });
    var sheets = rows.reduce(function (n, r) { return n + r.qty; }, 0), sub = rows.reduce(function (n, r) { return n + r.amount; }, 0);
    var rebate = 0, rb = cfg.rebate;
    if (rb && !noRebate && sheets && rb.before + sessionSheets() + sheets >= rb.target) rebate = A.roundHE(sub * rb.pct / 100);
    var taxable = sub - rebate, gst = A.roundHE(taxable * cfg.gst / 100);
    var pickup = transport === 'pickup';
    var freight = !sub || pickup ? 0 : (cfg.freight.free_at && sub < cfg.freight.free_at ? cfg.freight.fee : 0);
    var total = taxable + 2 * gst + freight, cr = cfg.credit;
    return { rows: rows, sheets: sheets, sub: sub, rebate: rebate, taxable: taxable, gst: gst, freight: freight, pickup: pickup, total: total,
      limit: cr.limit, outstanding: cr.outstanding, used: cr.outstanding + total, available: cr.limit - cr.outstanding - total,
      usedPct: Math.round((cr.outstanding + total) / cr.limit * 100) };
  };
  var meterClass = function (pct) { var t = pid === 'primary' ? [90, 75] : [80, 50]; return pct >= t[0] ? 'bad' : pct >= t[1] ? 'warn' : 'ok'; };
  var freightHtml = function (c) { return c.pickup ? A.chipHtml('Self Pickup', 'plain') : c.freight ? M(c.freight) : A.chipHtml('Free', 'ok'); };

  // ---------- Small renderers ----------
  var swatch = function (p) { return '<div class="sw ' + p.kind + (p.gloss ? ' gloss' : '') + ' " style="--a:' + p.colour + ';" role="img" aria-label="' + esc(p.name) + ' swatch"></div>'; };
  var qtyHtml = function (v, max) { return '<span class="qty"' + (max ? ' data-max="' + max + '"' : '') + '><span>−</span><input value="' + v + '" aria-label="Sheets" inputmode="numeric"><span>+</span></span>'; };
  var own = function (el) { el.setAttribute('data-own', '1'); };
  var label = function (el) { return el ? el.textContent.trim() : ''; };
  var setKV = function (root, dt, value, html) {
    qa('dt', root).forEach(function (d) { if (label(d) === dt) { var dd = d.nextElementSibling; if (html) dd.innerHTML = value; else dd.textContent = value; } });
  };
  var kvHtml = function (rows, cls) { return '<dl class="kv' + (cls ? ' ' + cls : '') + '">' + rows.map(function (r) { return '<dt>' + esc(r[0]) + '</dt><dd' + (r[2] ? ' style="' + r[2] + '"' : '') + '>' + r[1] + '</dd>'; }).join('') + '</dl>'; };
  var updateBadge = function () {
    qa('main .acts a .chip, main .head a .chip').forEach(function (c) { if (c.closest('a[data-link$="-ORD-03"]') || /Order Draft/.test(c.parentElement.textContent)) c.textContent = A.cart.count(); });
  };
  var go = function (target, extra) {
    var u = new URL(A.link(target), location.href);
    for (var k in extra) u.searchParams.set(k, extra[k]);
    location.href = u.toString();
  };

  // ---------- Add to order: used by the catalogue, product details and recommendations ----------
  var stockOk = function (sku, qty) {
    var p = PRODUCTS[sku], have = cfg.supply[sku];
    if (cfg.status[sku] === 'Out of Stock' || have <= 0) { A.toast(p.name + ' is out of stock at ' + cfg.supplier, 'bad'); return false; }
    if (qty > have) { A.toast('Only ' + N(have) + ' sheets of ' + p.name + ' are available at ' + cfg.supplier, 'bad'); return false; }
    return true;
  };
  A.addToOrder = function (sku, qty, quiet) {
    var p = PRODUCTS[sku]; qty = Math.round(qty);
    if (!(qty > 0)) { A.toast('Enter the number of sheets to order', 'warn'); return false; }
    if (!stockOk(sku, qty)) return false;
    var had = A.cart.qty(sku);
    A.cart.setQty(sku, qty);
    if (!quiet) A.toast((had ? 'Updated ' : 'Added ') + N(qty) + ' sheets of ' + p.name + (had ? ' in' : ' to') + ' the order draft', 'ok', { label: 'View Order Draft', fn: function () { A.go2(pid.slice(0, 3).toUpperCase() + '-ORD-03'); } });
    return true;
  };

  // ---------- Product Catalogue ----------
  var setupCatalogue = function () {
    qa('main .pcard').forEach(function (card) {
      var sku = label(q('.tag.mono', card)), buy = q('.buy', card), p = PRODUCTS[sku];
      if (!p || !buy) return;
      var inp = q('.qty input', buy), btn = q('button.btn', buy), box = q('.qty', buy);
      var out = cfg.status[sku] === 'Out of Stock' || cfg.supply[sku] <= 0;
      var refresh = function () {
        var inCart = A.cart.qty(sku);
        card.classList.toggle('in-order', inCart > 0);
        btn.innerHTML = A.icon('plus') + (out ? 'Out of Stock' : inCart ? 'Update Order' : 'Add to Order');
        btn.disabled = out; if (out) btn.setAttribute('aria-disabled', 'true');
        var slabs = qa('.slabs > div', card);
        if (slabs.length) { var v = parseInt(inp.value, 10) || 0, i = v >= 200 ? 2 : v >= 50 ? 1 : 0; slabs.forEach(function (s, k) { s.classList.toggle('cur', k === i); }); }
        var tag = q('.in-draft', card);
        if (inCart && !tag) { tag = document.createElement('span'); tag.className = 'tag in-draft'; q('.tags', card).appendChild(tag); }
        if (tag) { if (inCart) tag.textContent = N(inCart) + ' in order draft'; else tag.remove(); }
      };
      var have = A.cart.qty(sku);
      if (have && inp) inp.value = have;
      if (box && A.wireQty) { A.wireQty(box); }
      if (box) box.addEventListener('qtychange', refresh);
      own(btn); btn.addEventListener('click', function () { if (out) return; if (A.addToOrder(sku, parseInt(inp.value, 10) || 0)) refresh(); });
      refresh();
    });
    updateBadge();
  };

  // ---------- Product Details ----------
  var setupDetails = function () {
    var box = q('.qty'), btn = qa('main button.btn.pri').filter(function (b) { return /Add to Order/.test(b.textContent); })[0];
    var sku = '';
    qa('main dt').forEach(function (d) { if (label(d) === 'SKU') sku = label(d.nextElementSibling); });
    var p = PRODUCTS[sku]; if (!box || !btn || !p) return;
    var inp = q('input', box), amount = qa('dl.kv.total dd').filter(function (d) { return /Amount/.test(label(d.previousElementSibling)); })[0], big = q('.big-value');
    var have = A.cart.qty(sku); if (have) inp.value = have;
    var out = cfg.status[sku] === 'Out of Stock' || cfg.supply[sku] <= 0;
    var refresh = function () {
      var n = parseInt(inp.value, 10) || 0, pr = price(sku, n || 1);
      if (amount) amount.textContent = M(n * pr);
      if (big && cfg.mode === 'slab') big.textContent = M(pr);
      qa('table.tbl tbody tr').forEach(function (tr) {
        var r = label(tr.cells[0]); var m = r.match(/^(\d+)–(\d+)$|^(\d+)\+$/);
        if (!m) return;
        var lo = +(m[1] || m[3]), hi = m[2] ? +m[2] : Infinity;
        tr.classList.toggle('hl', n >= lo && n <= hi);
      });
      var inCart = A.cart.qty(sku);
      btn.innerHTML = A.icon('plus') + (out ? 'Out of Stock' : inCart ? 'Update Order' : 'Add to Order');
      btn.disabled = out;
    };
    A.wireQty(box);
    box.addEventListener('qtychange', refresh);
    own(btn); btn.addEventListener('click', function () { if (A.addToOrder(sku, parseInt(inp.value, 10) || 0)) refresh(); });
    refresh();
  };

  // ---------- Place Order ----------
  var setupPlaceOrder = function () {
    var rows = qa('main table.tbl tbody tr').filter(function (r) { return q('td.mono', r); });
    var aside = q('main aside.card'), draftBody = aside ? q('tbody', aside) : null;
    var cart = function () { return A.cart.lines(); };
    var sync = function () {
      var lines = cart(), c = A.calc(lines, form().transport);
      rows.forEach(function (tr) {
        var sku = label(q('td.mono', tr)), n = A.cart.qty(sku), inp = q('.qty input', tr), cells = tr.cells;
        var pr = price(sku, n || 1);
        if (inp && document.activeElement !== inp) inp.value = n;
        cells[2].textContent = M(n ? pr : (cfg.mode === 'slab' ? cfg.slabs[sku][0] : pr));
        cells[4].innerHTML = n ? '<b>' + M(n * pr) + '</b>' : '<b>—</b>';
        tr.classList.toggle('selected', n > 0);
      });
      if (draftBody) {
        draftBody.innerHTML = c.rows.length ? c.rows.map(function (r) { return '<tr><td><b>' + esc(PRODUCTS[r.sku].name) + '</b></td><td class="num">' + N(r.qty) + '</td><td class="num"><b>' + M(r.amount) + '</b></td></tr>'; }).join('')
          : '<tr class="empty-row"><td colspan="3">No products in the order draft</td></tr>';
        var kvs = qa('dl.kv', aside);
        setKV(aside, 'Sheets', N(c.sheets)); setKV(aside, 'Freight', freightHtml(c), true); setKV(aside, 'Subtotal', M(c.sub));
        var go = q('a.btn.pri', aside); if (go) go.classList.toggle('is-off', !c.rows.length);
      }
    };
    rows.forEach(function (tr) {
      var box = q('.qty', tr); if (!box) return;
      var sku = label(q('td.mono', tr));
      A.wireQty(box);
      box.addEventListener('qtychange', function (e) {
        var n = e.detail.value;
        if (n > 0 && !stockOk(sku, n)) { var max = cfg.supply[sku]; box.setSheets(Math.max(0, cfg.status[sku] === 'Out of Stock' ? 0 : max)); n = Math.max(0, cfg.status[sku] === 'Out of Stock' ? 0 : max); }
        A.cart.setQty(sku, n); sync();
      });
    });
    sync();
    var cont = aside ? q('a.btn.pri', aside) : null;
    if (cont) cont.addEventListener('click', function (e) { if (!A.cart.count()) { e.preventDefault(); A.toast('Add at least one product to the order draft', 'warn'); } });
    qa('button', aside || document).forEach(function (b) { if (/Save Draft/.test(b.textContent)) { own(b); b.addEventListener('click', function () { A.save(); A.toast('Order draft saved', 'ok'); }); } });
    // "Reorder from a Previous Order"
    var re = qa('main .sel').filter(function (s) { return /Reorder from a Previous Order/.test(s.textContent); })[0];
    if (re) {
      re.setAttribute('data-own', '1'); re.setAttribute('role', 'button'); re.setAttribute('tabindex', '0'); re.setAttribute('aria-haspopup', 'listbox');
      var open = function () {
        var items = cfg.prev.map(function (o) { var sh = o.lines.reduce(function (n, l) { return n + l[1]; }, 0); return { label: o.no, value: o.no, hint: N(sh) + ' sheets, ' + o.date }; });
        A.menu(re, items, { onPick: function (it) {
          var o = cfg.prev.filter(function (x) { return x.no === it.value; })[0];
          A.cart.set(o.lines.map(function (l) { return [l[0], l[1]]; })); sync(); A.toast('Order draft now holds the sheets of ' + o.no, 'ok');
        } });
      };
      re.addEventListener('click', open);
      re.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
    }
  };

  // ---------- Order Builder ----------
  var nextNumber = function () {
    var s = cfg.series, n = s.first + orders().length;
    return s.prefix + String(n).padStart(s.width, '0');
  };
  var validDate = function (t) {
    var d = A.parseDate(t); if (d === null || !/^\d{2}\/\d{2}\/\d{4}$/.test(t.trim())) return 'Enter the date as dd/mm/yyyy';
    if (d <= A.today) return 'Choose a date after today';
    if (d > A.today + 120 * A.DAY) return 'Choose a date within the next 120 days';
    return '';
  };
  var setupBuilder = function () {
    var itemsBody = q('main section.card.flush tbody'), summary, creditCard, rebateChip = q('main section.card.flush header .chip');
    qa('main section.card').forEach(function (s) {
      var h = label(q('header h2', s));
      if (h === 'Order Summary') summary = q('.body', s);
      if (h === 'Credit') creditCard = q('.body', s);
    });
    var submit = qa('main .head .acts a, main .head .acts button').filter(function (x) { return /Submit Order/.test(x.textContent); })[0];
    var f = form();
    var el = function (id) { return document.getElementById(id); };
    // restore the delivery form
    if (f.loc !== undefined && el('loc')) el('loc').value = f.loc;
    if (f.date && el('date')) el('date').value = f.date;
    if (f.ref !== undefined && el('ref')) el('ref').value = f.ref;
    if (f.contact && el('contact')) el('contact').value = f.contact;
    if (f.notes !== undefined && el('notes')) el('notes').value = f.notes;
    var radios = qa('input[name=t]'), pickup = f.transport === 'pickup';
    if (radios.length === 2) radios[pickup ? 1 : 0].checked = true;
    var syncRadios = function () { radios.forEach(function (r) { r.closest('label').classList.toggle('on', r.checked); }); };
    syncRadios();
    var save = function () {
      setForm({ loc: el('loc') && el('loc').value, date: el('date') && el('date').value, ref: el('ref') && el('ref').value, contact: el('contact') && el('contact').value,
        notes: el('notes') && el('notes').value, transport: radios.length === 2 && radios[1].checked ? 'pickup' : 'company' });
    };
    ['loc', 'date', 'ref', 'contact', 'notes'].forEach(function (id) { if (el(id)) el(id).addEventListener('change', save); });
    radios.forEach(function (r) { r.addEventListener('change', function () { syncRadios(); save(); render(); }); });

    var render = function () {
      var lines = A.cart.lines(), c = A.calc(lines, form().transport);
      if (itemsBody) {
        itemsBody.innerHTML = c.rows.length ? c.rows.map(function (r) {
          var p = PRODUCTS[r.sku];
          return '<tr data-sku="' + r.sku + '"><td><div class="prod">' + swatch(p) + '<div><b>' + esc(p.name) + '</b></div></div></td><td class="mono nowrap">' + r.sku + '</td><td>' + qtyHtml(r.qty) + '</td><td class="num">' + M(r.price) +
            '</td><td class="num"><b>' + M(r.amount) + '</b></td><td><button class="icon-btn" type="button" aria-label="Remove ' + esc(p.name) + '">' + A.icon('trash') + '</button></td></tr>';
        }).join('') : '<tr class="empty-row"><td colspan="6">No products in the order. Choose products to continue.</td></tr>';
        qa('tr[data-sku]', itemsBody).forEach(function (tr) {
          var sku = tr.getAttribute('data-sku'), box = q('.qty', tr);
          A.wireQty(box);
          box.addEventListener('qtychange', function (e) {
            var n = e.detail.value;
            if (n > 0 && !stockOk(sku, n)) { n = Math.max(0, Math.min(n, cfg.supply[sku])); }
            A.cart.setQty(sku, n); render();
          });
          own(q('.icon-btn', tr)); q('.icon-btn', tr).addEventListener('click', function () {
            var was = A.cart.qty(sku); A.cart.setQty(sku, 0); render();
            A.toast('Removed ' + PRODUCTS[sku].name + ' from the order', 'warn', { label: 'Undo', fn: function () { A.cart.setQty(sku, was); render(); } });
          });
        });
      }
      if (rebateChip) rebateChip.hidden = !c.rebate;
      if (summary) {
        var rows = [['Sheets', N(c.sheets)], ['Subtotal', M(c.sub)]];
        if (cfg.rebate && c.rebate) { rows.push([cfg.rebate.label, '−' + M(c.rebate), 'color:var(--ok)']); rows.push(['Taxable Amount', M(c.taxable)]); }
        rows.push(['Central GST ' + cfg.gst + '%', M(c.gst)], ['State GST ' + cfg.gst + '%', M(c.gst)], ['Freight', freightHtml(c)]);
        summary.innerHTML = kvHtml(rows) + kvHtml([['Total', M(c.total)]], 'total');
      }
      if (creditCard) {
        var cls = c.available < 0 ? 'bad' : meterClass(c.usedPct);
        creditCard.innerHTML = kvHtml([['Credit Limit', ML(c.limit)], ['Outstanding Balance', ML(c.outstanding)], ['This Order', M(c.total)]]) +
          '<span class="meter ' + cls + '" style="margin-top:1rem"><i style="width:' + Math.min(100, c.usedPct) + '%"></i></span>' +
          kvHtml([['Credit Available', c.available < 0 ? '−' + ML(-c.available) : ML(c.available), c.available < 0 ? 'color:var(--bad)' : '']], 'total');
      }
      if (submit) { submit.classList.toggle('is-off', !c.rows.length); }
    };
    render();
    // buttons
    qa('main .head .acts button').forEach(function (b) { if (/Save Draft/.test(b.textContent)) { own(b); b.addEventListener('click', function () { save(); A.toast('Order draft saved', 'ok'); }); } });
    if (submit) submit.addEventListener('click', function (e) {
      e.preventDefault(); save();
      var lines = A.cart.lines(), fm = form(), c = A.calc(lines, fm.transport);
      qa('.field.invalid').forEach(function (x) { x.classList.remove('invalid'); var er = q('.err', x); if (er) er.remove(); });
      var bad = function (id, msg) { var fld = el(id).closest('.field'); fld.classList.add('invalid'); var er = document.createElement('div'); er.className = 'err'; er.textContent = msg; fld.appendChild(er); el(id).focus(); };
      if (!c.rows.length) { A.toast('Add at least one product to place the order', 'warn'); return; }
      var dm = validDate(el('date').value); if (dm) { bad('date', dm); return; }
      if (!el('contact').value.trim()) { bad('contact', 'Enter the receiving contact'); return; }
      for (var i = 0; i < c.rows.length; i++) { var r = c.rows[i]; if (r.qty > cfg.supply[r.sku]) { A.toast('Only ' + N(cfg.supply[r.sku]) + ' sheets of ' + PRODUCTS[r.sku].name + ' are available at ' + cfg.supplier, 'bad'); return; } }
      if (c.available < 0) { A.toast('This order is ' + ML(-c.available) + ' above the credit available. Remove products or sheets to continue.', 'bad'); return; }
      var now = new Date(), hh = ('0' + now.getHours()).slice(-2) + ':' + ('0' + now.getMinutes()).slice(-2);
      var order = { no: nextNumber(), date: '26/10/2026', time: hh, lines: lines, sheets: c.sheets, sub: c.sub, rebate: c.rebate, taxable: c.taxable, gst: c.gst, freight: c.freight, total: c.total,
        req: el('date').value.trim(), loc: el('loc').value, ref: el('ref').value.trim(), contact: el('contact').value.trim(), transport: c.pickup ? 'Self Pickup' : cfg.transport,
        notes: el('notes').value.trim(), by: person, status: 'Awaiting Confirmation', avail: c.available };
      A.state.o = A.state.o || {}; (A.state.o[pid] = A.state.o[pid] || []).push(order);
      A.state.c = A.state.c || {}; A.state.c[pid] = []; delete (A.state.f || {})[pid];
      A.save();
      go(pid.slice(0, 3).toUpperCase() + '-ORD-05', { ord: order.no });
    });
  };

  // ---------- Order Confirmation ----------
  var findOrder = function (no) { var l = orders(); if (no) return l.filter(function (o) { return o.no === no; })[0]; return l[l.length - 1]; };
  var addDays = function (d, n) { return A.fmtDate(A.parseDate(d) + n * A.DAY); };
  var setupConfirmation = function () {
    var o = findOrder(params.get('ord')); if (!o) return;          // no order submitted in this session: the designed example stays
    var P = PRODUCTS;
    var big = q('.big-value.mono'); if (big) big.textContent = o.no;
    var stats = qa('.stats > div'); stats.forEach(function (d) {
      var k = label(q('span', d)), b = q('b', d) || q('.chip', d);
      if (k === 'Placed') b.textContent = o.date + ' ' + o.time; else if (k === 'Sheets') b.textContent = N(o.sheets); else if (k === 'Total') b.textContent = M(o.total);
    });
    var vd = qa('main a.btn').filter(function (a) { return /View Order Details/.test(a.textContent); })[0];
    if (vd) vd.setAttribute('href', A.link(pid.slice(0, 3).toUpperCase() + '-ORD-02') + '&ord=' + encodeURIComponent(o.no));
    var tr = qa('ol.track li'); if (tr.length === 5) {
      q('span', tr[0]).textContent = o.date;
      var t = cfg.track; q('span', tr[2]).textContent = addDays(o.req, t[0]); q('span', tr[3]).textContent = addDays(o.req, t[1]); q('span', tr[4]).textContent = o.req;
    }
    qa('main section.card').forEach(function (s) {
      var h = label(q('header h2', s)), body = q('.body', s);
      if (h === 'Order Summary') {
        q('tbody', body).innerHTML = o.lines.map(function (l) { var pr = price(l[0], l[1]); return '<tr><td><b>' + esc(P[l[0]].name) + '</b></td><td class="num">' + N(l[1]) + '</td><td class="num"><b>' + M(l[1] * pr) + '</b></td></tr>'; }).join('');
        qa('dl', body).forEach(function (d) { d.remove(); });
        var rows = [];
        if (cfg.rebate && o.rebate) rows.push(['Rebate', '−' + M(o.rebate), 'color:var(--ok)']);
        rows.push(['Central GST ' + cfg.gst + '%', M(o.gst)], ['State GST ' + cfg.gst + '%', M(o.gst)]);
        if (o.freight) rows.push(['Freight', M(o.freight)]);
        body.insertAdjacentHTML('beforeend', kvHtml(rows) + kvHtml([['Total', M(o.total)]], 'total'));
      }
      if (h === 'Delivery') {
        qa('dt', body).forEach(function (d) {
          var k = label(d), dd = d.nextElementSibling;
          if (k === 'Location' || k === 'Deliver To') dd.textContent = o.loc; else if (k === 'Requested Date' || k === 'Requested') dd.textContent = o.req;
          else if (k === 'Transport') dd.textContent = o.transport; else if (k === 'Receiving Contact') dd.textContent = o.contact.split(',')[0]; else if (k === 'Placed By') dd.textContent = o.by;
        });
      }
      if (h === 'Credit') qa('dt', body).forEach(function (d) { if (label(d) === 'Credit Available') d.nextElementSibling.textContent = o.avail < 0 ? '−' + ML(-o.avail) : ML(o.avail); });
    });
  };

  // ---------- Order History ----------
  var setupHistory = function () {
    var table = q('main table.tbl'); if (!table || !orders().length) return;
    var heads = qa('thead th', table).map(label), tbody = table.tBodies[0];
    var col = function (n) { return heads.indexOf(n); };
    var detailsHref = function (no) { return A.link(pid.slice(0, 3).toUpperCase() + '-ORD-02') + '&ord=' + encodeURIComponent(no); };
    var rowOf = function (no) { return qa('tr', tbody).filter(function (r) { return label(r.cells[0]).indexOf(no) === 0; })[0]; };
    orders().slice().reverse().forEach(function (o) {
      var tr = rowOf(o.no);
      if (!tr) { tr = tbody.rows[0].cloneNode(true); tbody.insertBefore(tr, tbody.rows[0]); tr.classList.add('row-new'); }
      var set = function (name, html) { var i = col(name); if (i >= 0) tr.cells[i].innerHTML = html; };
      set('Order Number', '<a><b>' + o.no + '</b></a>'); set('Order Date', o.date); set('Sheets', N(o.sheets)); set('Value', '<b>' + M(o.total) + '</b>');
      set('Delivery Date', o.req); set('Order Status', A.chipHtml(o.status)); set('Payment', A.chipHtml('Unpaid', 'plain'));
      qa('a', tr).forEach(function (a) { a.removeAttribute('data-link'); a.removeAttribute('aria-disabled'); a.setAttribute('href', detailsHref(o.no)); });
      var act = q('.row-actions', tr); if (act && !q('a', act)) act.innerHTML = '<a class="btn sm" href="' + detailsHref(o.no) + '">View</a>';
    });
    // tiles that are counts or sums of the rows
    var rows = qa('tbody tr', table), val = function (r, name) { return col(name) >= 0 ? label(r.cells[col(name)]) : ''; };
    var inOct = rows.filter(function (r) { return /\/10\/2026$/.test(val(r, 'Order Date')) && !/Cancelled/.test(val(r, 'Order Status')); });
    var tile = function (name, v) { qa('main .kpi').forEach(function (k) { if (label(q('label', k)) === name) q('strong', k).textContent = v; }); };
    tile('Orders This Month', inOct.length);
    tile('Order Value This Month', M(inOct.reduce(function (n, r) { return n + (A.parseMoney(val(r, 'Value')) || 0); }, 0)));
    ['In Transit', 'Awaiting Confirmation', 'Being Packed'].forEach(function (st) { tile(st, rows.filter(function (r) { return val(r, 'Order Status') === st; }).length); });
  };

  // ---------- Order links carry the order they belong to ----------
  var DETAIL_FILE = (function () { var t = P_find(pid.slice(0, 3).toUpperCase() + '-ORD-02'); return t ? t.screen.file.split('/').pop() : 'order-details.html'; })();
  function P_find(id) { return window.PORTAL.find(id); }
  var NO = /^[A-Z]{3}-\d{4}-[A-Z]?\d+$/;
  var decorateOrderLinks = function () {
    qa('main a[href]').forEach(function (a) {
      var href = a.getAttribute('href') || ''; if (href.indexOf(DETAIL_FILE) < 0 || /[?&]ord=/.test(href)) return;
      var tr = a.closest('tr'), no = text0(a).split(' ')[0];
      if (tr && !NO.test(no)) no = text0(tr.cells[0]).split(' ')[0];
      if (!NO.test(no)) return;
      var u = new URL(href, location.href); u.searchParams.set('ord', no);
      if (tr && tr.closest('table')) {
        var heads = qa('thead th', tr.closest('table')).map(text0), pick = function (re) { var i = -1; heads.forEach(function (h, k) { if (i < 0 && re.test(h)) i = k; }); return i >= 0 && tr.cells[i] ? text0(tr.cells[i]) : ''; };
        [['d', /^(order )?date$/i], ['r', /delivery date|expected/i], ['s', /status|fulfilment/i], ['p', /^payment$/i], ['n', /^sheets$/i], ['v', /^(value|amount|total)$/i]].forEach(function (m) { var v = pick(m[1]); if (v && v !== '—') u.searchParams.set(m[0], v); });
      }
      a.setAttribute('href', u.toString());
    });
  };
  function text0(el) { return el ? el.textContent.replace(/\s+/g, ' ').trim() : ''; }

  // ---------- Order Details ----------
  // The order to show: one placed in this session, or one from the history (its lines come from catalog.js, its dates and status from the clicked row).
  var STAGE = { 'Awaiting Confirmation': 1, 'Confirmed': 2, 'Being Packed': 2, 'Packed': 2, 'In Transit': 3, 'Delivered': 5, 'Cancelled': 0 };
  var detailsOrder = function () {
    var no = params.get('ord'); if (!no) return null;
    var o = findOrder(no); if (o) return o;
    if (no === label(q('main h1'))) return null;                                   // the order this screen already shows in full
    var pv = cfg.prev.filter(function (x) { return x.no === no; })[0], date = params.get('d') || (pv && pv.date) || '26/10/2026';
    var seed = cfg.series.prefix + String(cfg.series.first).padStart(cfg.series.width, '0');   // the designed pending order is the designed draft
    var lines = pv ? pv.lines : (no === seed ? cfg.draft : null), c = lines ? A.calc(lines, '', no !== seed) : null, v = params.get('v') ? A.parseMoney(params.get('v')) : (c ? c.total : 0);
    return { no: no, date: date, time: '', lines: lines, sheets: params.get('n') ? parseInt(params.get('n').replace(/,/g, ''), 10) : (c ? c.sheets : 0), total: v, req: params.get('r') || addDays(date, 5),
      status: params.get('s') || 'Delivered', pay: params.get('p') || 'Paid', loc: cfg.loc, history: true, calc: c, by: '—', ref: '', transport: cfg.transport };
  };
  var setupOrderDetails = function () {
    var h1 = q('main h1');
    qa('main .head button').forEach(function (b) {                                  // Reorder
      if (!/Reorder/.test(b.textContent)) return;
      own(b);
      b.addEventListener('click', function () {
        var o = detailsOrder(), no = label(h1), lines = o ? o.lines : (cfg.prev.filter(function (x) { return x.no === no; })[0] || {}).lines;
        if (!lines) { A.toast('The sheets of ' + no + ' are not recorded in the prototype', 'warn'); return; }
        A.cart.set(lines.map(function (l) { return [l[0], l[1]]; }));
        go(pid.slice(0, 3).toUpperCase() + '-ORD-03', {});
      });
    });
    var o = detailsOrder(); if (!o) return;
    var P = PRODUCTS, stage = STAGE[o.status] === undefined ? 1 : STAGE[o.status], cancelled = o.status === 'Cancelled';
    h1.textContent = o.no;
    var chips = qa('.title-row .chip'); if (chips[0]) A.applyChip(chips[0], o.status); if (chips[1]) A.applyChip(chips[1], o.pay || 'Unpaid');
    var tr = qa('ol.track li');
    if (tr.length === 5) {
      var t = cfg.track, spans = tr.map(function (li) { return q('span', li); }), planned = [o.date, addDays(o.date, 1), addDays(o.req, t[0]), addDays(o.req, t[1]), o.req];
      tr.forEach(function (li, i) { li.className = stage >= 5 || i < stage ? 'done' : i === stage ? 'now' : 'todo'; });
      spans.forEach(function (sp, i) { sp.textContent = cancelled && i ? '—' : (i === 0 ? planned[0] + (o.time ? ' ' + o.time : '') : (i === 1 && stage === 1 ? 'Pending' : planned[i])); });
    }
    qa('main section.card').forEach(function (s) {
      var h = label(q('header h2', s)), body = q('.body', s);
      if (h === 'Items') {
        if (!o.lines) { body.innerHTML = '<div style="padding:1rem 1.125rem">' + kvHtml([['Sheets', N(o.sheets)], ['Order Value', M(o.total)]], '') + '</div>'; return; }
        var c = o.calc || A.calc(o.lines, o.transport === 'Self Pickup' ? 'pickup' : ''), exact = !o.history || c.total === o.total;
        var heads = qa('thead th', body).map(label), tb = q('tbody', body), keep = heads.map(function (hd) { return exact || !/^(Price per Sheet|Amount)$/.test(hd); });
        if (!exact) qa('thead th', body).forEach(function (th, i) { if (!keep[i]) th.remove(); });     // old orders were priced on other terms: show what is recorded, not derived prices
        tb.innerHTML = o.lines.map(function (l) {
          var p = P[l[0]], pr = price(l[0], l[1]), cells = heads.map(function (hd, i) {
            if (!keep[i]) return '';
            if (hd === 'Product') return '<td><div class="prod">' + swatch(p) + '<div><b>' + esc(p.name) + '</b></div></div></td>';
            if (hd === 'SKU') return '<td class="mono nowrap">' + l[0] + '</td>';
            if (hd === 'Sheets') return '<td class="num">' + N(l[1]) + '</td>';
            if (hd === 'Price per Sheet') return '<td class="num">' + M(pr) + '</td>';
            return '<td class="num"><b>' + M(l[1] * pr) + '</b></td>';
          }); return '<tr>' + cells.join('') + '</tr>';
        }).join('');
        var tf = q('tfoot', body), kvs = qa('dl.kv', body);
        if (!exact) {
          if (tf) tf.remove();
          if (kvs[0]) kvs[0].remove();
          if (kvs[1]) setKV(body, 'Total', M(o.total));
          return;
        }
        var tfc = q('tfoot td.num', body); if (tfc) tfc.textContent = M(o.sub !== undefined ? o.sub : c.sub);
        if (kvs.length) {
          var gst = o.gst !== undefined ? o.gst : c.gst, rebate = o.rebate !== undefined ? o.rebate : c.rebate, fr = o.freight !== undefined ? o.freight : c.freight, rows = [];
          if (cfg.rebate && rebate) rows.push([cfg.rebate.label, '−' + M(rebate), 'color:var(--ok)'], ['Taxable Amount', M(c.taxable)]);
          rows.push(['Central GST ' + cfg.gst + '%', M(gst)], ['State GST ' + cfg.gst + '%', M(gst)]);
          if (fr) rows.push(['Freight', M(fr)]);
          kvs[0].outerHTML = kvHtml(rows).replace('<dl class="kv"', '<dl class="kv" style="max-width:22rem;margin-left:auto"');
          if (kvs[1]) setKV(body, 'Total', M(o.total));
        }
      }
      if (h === 'Order Activity') {
        var ev = [[o.date + (o.time ? ' ' + o.time : ''), 'Order placed', o.by === '—' ? A.portal.org : o.by]];
        if (!cancelled && stage >= 2 || stage >= 5) ev.push([addDays(o.date, 1), 'Order confirmed', cfg.supplier]);
        if (stage >= 3 && !cancelled) ev.push([addDays(o.req, cfg.track[1]), 'Shipment dispatched', cfg.supplier]);
        if (stage >= 5) ev.push([o.req, 'Delivered', A.portal.org]);
        if (cancelled) ev.push([addDays(o.date, 1), 'Order cancelled', cfg.supplier]);
        q('tbody', s).innerHTML = ev.reverse().map(function (r) { return '<tr><td class="nowrap">' + r[0] + '</td><td><b>' + r[1] + '</b></td><td>' + esc(r[2]) + '</td></tr>'; }).join('');
      }
      if (h === 'Delivery') qa('dt', body).forEach(function (d) {
        var k = label(d), dd = d.nextElementSibling;
        if (k === 'Deliver To') dd.textContent = o.loc; else if (k === 'Expected') dd.textContent = o.req; else dd.innerHTML = '—';
      });
      if (h === 'Invoice') s.hidden = true;
      if (h === 'Order Information') qa('dt', body).forEach(function (d) {
        var k = label(d), dd = d.nextElementSibling;
        if (k === 'Placed By') dd.textContent = o.by; else if (k === 'Payment Terms') dd.textContent = cfg.terms; else if (k === 'Transport') dd.textContent = o.transport;
        else if (k === 'Reference Number') dd.textContent = o.ref || '—'; else if (k === 'Scheme' || k === 'Offer') dd.textContent = o.rebate ? cfg.rebate.label : 'None';
      });
    });
  };

  // ---------- Reorder from stock screens: "Order Now" chips and the Reorder button ----------
  var setupReorder = function () {
    qa('main table.tbl').forEach(function (t) {
      var heads = qa('thead th', t).map(label), sc = heads.indexOf('SKU'), qc = heads.indexOf('Suggested Quantity');
      if (sc < 0 || qc < 0) return;
      qa('tbody tr', t).forEach(function (tr) {
        var chip = qa('.chip', tr).filter(function (c) { return label(c) === 'Order Now'; })[0]; if (!chip) return;
        var sku = label(tr.cells[sc]), n = parseInt(label(tr.cells[qc]).replace(/[^\d]/g, ''), 10) || 0;
        var b = document.createElement('button'); b.type = 'button'; b.className = 'btn sm'; b.innerHTML = A.icon('plus') + 'Order Now';
        chip.replaceWith(b); own(b);
        b.addEventListener('click', function () { if (A.addToOrder(sku, n)) { b.innerHTML = A.icon('check') + 'In Order Draft'; } });
      });
    });
    // Inventory Item Details: Reorder adds the reorder quantity of this product
    var rb = qa('main .head .acts a, main .head .acts button').filter(function (b) { return label(b) === 'Reorder'; })[0];
    if (rb && /INV-02$/.test(part)) {
      var sku = '', n = 0;
      qa('main dt').forEach(function (d) { var k = label(d); if (k === 'SKU') sku = label(d.nextElementSibling); if (k === 'Reorder Quantity') n = parseInt(label(d.nextElementSibling).replace(/[^\d]/g, ''), 10) || 0; });
      if (sku) { own(rb); rb.addEventListener('click', function (e) { e.preventDefault(); if (A.addToOrder(sku, n)) { /* stays on the screen; the toast offers the order draft */ } }); }
    }
  };

  A.onReady(20, function () {
    if (/^CAT-01$/.test(part)) setupCatalogue();
    if (/^CAT-02$/.test(part)) setupDetails();
    if (/^ORD-03$/.test(part)) setupPlaceOrder();
    if (/^ORD-04$/.test(part)) setupBuilder();
    if (/^ORD-05$/.test(part)) setupConfirmation();
    if (/^ORD-01$/.test(part)) setupHistory();
    if (/^ORD-02$/.test(part)) setupOrderDetails();
    decorateOrderLinks();
    setupReorder();
    updateBadge();
  });
})();
