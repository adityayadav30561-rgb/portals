/*
 * Behaviour layer, part 2: lists. Search, dropdown filters, tabs, sorting, pagination, selection, grid/list toggle and
 * quantity steppers, for every table, product grid and notification feed, driven by the markup the generators write:
 *   .filters  (.finder input, .sel ...)   .tabs > span   table.tbl   .products > .pcard   ul.feed > li   .pg   .qty
 * Controls and the collection they act on are paired by position: the nearest following table, grid or feed.
 * Nothing is filtered until a control is used, so a screen opens exactly as designed.
 * Counts always describe the rows that exist (tab badges, "Showing x to y of z").
 */
(function () {
  var A = window.APP, q = A.q, qa = A.qa;
  var PAGE = 10;
  A.lists = [];
  var STOP = /\b(all|orders?|requests?|tickets?|invoices?|users?|movements?|products?|notifications?|issues?|payments?|shipments?|campaigns?|schemes?|offers?|returns?|retailers?|dealers?|deliveries|dispatches|sales|items?|of|to|and)\b/g;
  var stem = function (w) { return w.replace(/ies$/, 'y').replace(/([^s])s$/, '$1'); };
  var words = function (t) { return String(t).toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').split(/\s+/).filter(Boolean).map(stem); };
  var norm = function (t) { return String(t).toLowerCase().replace(/\s+/g, ' ').replace(/\d+/g, '').trim(); };

  // ---------- Which collection does a control act on? ----------
  var collectionFor = function (from) {
    var node = from.parentElement;
    while (node && node !== document.body) {
      var c = qa('.products, table.tbl, ul.feed', node).filter(function (x) { return (from.compareDocumentPosition(x) & 4) && !from.contains(x); })[0];
      if (c) return c;
      node = node.parentElement;
    }
    return null;
  };
  var kindOf = function (el) { return el.matches('table') ? 'table' : el.matches('.products') ? 'cards' : 'feed'; };

  var List = function (el) {
    this.el = el; this.kind = kindOf(el);
    this.items = this.kind === 'table' ? qa('tbody > tr', el).filter(function (r) { return !r.querySelector('td[colspan]') || r.cells.length > 1; })
      : this.kind === 'cards' ? qa(':scope > article, :scope > .pcard', el) : qa(':scope > li', el);
    this.card = el.closest('.card') || el.parentElement;
    this.query = ''; this.tab = null; this.filters = []; this.sort = null; this.page = 1; this.date = null;
    this.pg = null; this.noun = 'records'; this.selects = [];
    this.heads = this.kind === 'table' ? qa('thead th', el) : [];
    var self = this;
    this.items.forEach(function (it, i) { it._i = i; });
    var box = this.kind === 'table' ? (el.closest('.card') || el.parentElement) : (el.closest('.card') || el.parentElement);
    var pg = q('.pg', box);
    if (pg && (this.kind !== 'table' || pg.compareDocumentPosition(el) & 2 || true)) {
      this.pg = pg;
      var m = (q('span', pg) || {}).textContent || '';
      var n = m.match(/of\s+[\d,]+\s+(.+)$/);
      if (n) this.noun = n[1].trim();
    } else {
      var h = q('header h2', this.card);
      if (h) this.noun = h.textContent.trim().toLowerCase();
    }
    A.lists.push(this);
  };
  var colText = function (item, i) { var c = item.cells[i]; return c ? c.textContent.replace(/\s+/g, ' ').trim() : ''; };

  // ---------- Matching ----------
  var chipTexts = function (item) { return qa('.chip', item).map(function (c) { return norm(c.textContent); }); };
  var rowText = function (item) {
    var t = '';
    qa('input, select', item).forEach(function (i) { if (i.type !== 'checkbox' && i.type !== 'radio') t += ' ' + i.value; });
    return (item.textContent + t).toLowerCase().replace(/\s+/g, ' ');
  };
  var tabMatches = function (list, tab, item) {
    var key = tab.key;
    if (tab.all) return true;
    if (key === 'unread') return item.classList.contains('unread');
    var chips = chipTexts(item);
    if (tab.byChip === undefined) {                       // does any row of the list carry a chip with this label?
      tab.byChip = list.items.some(function (it) { return chipTexts(it).some(function (c) { return c === key || c.indexOf(key + ' ') === 0; }); });
    }
    if (tab.byChip) return chips.some(function (c) { return c === key || c.indexOf(key + ' ') === 0; });
    var kw = words(tab.label.replace(STOP, ' ')).filter(function (w) { return w; });
    if (!kw.length) return true;
    var rt = words(rowText(item));
    return kw.every(function (w) { return rt.indexOf(w) >= 0; });
  };
  var inDateRange = function (list, item) {
    var d = list.date; if (!d) return true;
    var col = d.col, t = null;
    if (col >= 0) t = A.parseDate(colText(item, col));
    if (t === null) { var m = A.parseDate(item.textContent); t = m; }
    if (t === null) return true;
    return t >= d.from && t <= d.to;
  };
  List.prototype.matches = function (item, ignoreTab) {
    var self = this;
    if (!ignoreTab && this.tab && !tabMatches(this, this.tab, item)) return false;
    if (this.query) {
      var rt = rowText(item), toks = this.query.split(/\s+/);
      if (!toks.every(function (w) { return rt.indexOf(w) >= 0; })) return false;
    }
    for (var i = 0; i < this.filters.length; i++) {
      var f = this.filters[i];
      if (f.value === null) continue;
      var v = f.get(item);
      if (f.match ? !f.match(v, f.value) : String(v).trim().toLowerCase() !== String(f.value).trim().toLowerCase()) return false;
    }
    return inDateRange(this, item);
  };

  // ---------- Sorting ----------
  var cellValue = function (list, item, col) {
    if (list.kind !== 'table') return '';
    var c = item.cells[col]; if (!c) return '';
    var inp = c.querySelector('input:not([type=checkbox]):not([type=radio])');
    var t = (inp ? inp.value : (c.querySelector('.prod b, a b, b') || c).textContent).replace(/\s+/g, ' ').trim();
    return t;
  };
  var colType = function (list, col) {
    if (list._types && list._types[col]) return list._types[col];
    list._types = list._types || {};
    var vals = list.items.map(function (it) { return cellValue(list, it, col); }).filter(function (v) { return v && v !== '—'; });
    var type = 'text';
    if (vals.length) {
      if (vals.every(function (v) { return A.parseMoney(v) !== null; })) type = 'money';
      else if (vals.every(function (v) { return A.parseDate(v) !== null; })) type = 'date';
      else if (vals.every(function (v) { return /^[-−]?[\d,]+(\.\d+)?\s*(%|sheets?|days?|kg|mm)?(\s|$)/i.test(v); })) type = 'number';
    }
    list._types[col] = type;
    return type;
  };
  var sortKey = function (type, v) {
    if (v === '' || v === '—') return null;
    if (type === 'money') return A.parseMoney(v);
    if (type === 'date') return A.parseDate(v);
    if (type === 'number') return parseFloat(v.replace(/,/g, '').replace('−', '-'));
    return v.toLowerCase();
  };
  List.prototype.sorted = function (items) {
    var s = this.sort; if (!s) return items.slice().sort(function (a, b) { return a._i - b._i; });
    var self = this, type = s.fn ? 'x' : colType(this, s.col), dir = s.dir === 'desc' ? -1 : 1;
    return items.slice().sort(function (a, b) {
      var ka = s.fn ? s.fn(a) : sortKey(type, cellValue(self, a, s.col)), kb = s.fn ? s.fn(b) : sortKey(type, cellValue(self, b, s.col));
      if (ka === null && kb === null) return a._i - b._i;
      if (ka === null) return 1; if (kb === null) return -1;
      var c = typeof ka === 'string' ? ka.localeCompare(kb, 'en', { numeric: true }) : ka - kb;
      return c * dir || (a._i - b._i);
    });
  };

  // ---------- Drawing ----------
  List.prototype.apply = function (resetPage) {
    var self = this;
    if (resetPage) this.page = 1;
    var vis = this.sorted(this.items.filter(function (it) { return !it.classList.contains('row-gone') && self.matches(it); }));
    var total = vis.length, pages = this.pg ? Math.max(1, Math.ceil(total / PAGE)) : 1;
    if (this.page > pages) this.page = pages;
    var from = this.pg ? (this.page - 1) * PAGE : 0, to = this.pg ? Math.min(total, from + PAGE) : total;
    var shown = vis.slice(from, to);
    var host = this.kind === 'table' ? this.el.tBodies[0] : this.el;
    this.items.forEach(function (it) { it.hidden = true; });
    shown.forEach(function (it) { it.hidden = false; host.appendChild(it); });
    // rows that are removed stay at the end, hidden
    this.items.forEach(function (it) { if (it.hidden) host.appendChild(it); });
    var old = q('.empty-row, .empty-block', this.kind === 'table' ? host : this.el.parentElement);
    if (old && old.getAttribute('data-for') === String(A.lists.indexOf(this))) old.remove();
    if (!total) {
      var msg = 'No ' + this.noun.replace(/^\w/, function (c) { return c.toLowerCase(); }) + ' to show';
      var id = String(A.lists.indexOf(this));
      if (this.kind === 'table') {
        var tr = document.createElement('tr'); tr.className = 'empty-row'; tr.setAttribute('data-for', id);
        tr.innerHTML = '<td colspan="' + (this.heads.length || 1) + '">' + A.esc(msg) + '</td>'; host.appendChild(tr);
      } else {
        var d = document.createElement('div'); d.className = 'empty-block'; d.setAttribute('data-for', id); d.textContent = msg;
        this.el.appendChild(d);
      }
    }
    this.drawPager(total, from, to, pages);
    this.syncHeaders();
    this.updateTabCounts();
    this.el.dispatchEvent(new CustomEvent('listchange', { bubbles: true }));
  };
  List.prototype.drawPager = function (total, from, to, pages) {
    if (!this.pg) return;
    var span = q('span', this.pg), box = q('.pages', this.pg), self = this;
    span.textContent = total ? 'Showing ' + (from + 1) + ' to ' + to + ' of ' + total + ' ' + this.noun : 'Showing 0 of 0 ' + this.noun;
    if (!box) return;
    if (pages <= 1) { box.innerHTML = '<span class="on">1</span>'; return; }
    var btn = function (label, p, cls, dis) { return '<button type="button" data-p="' + p + '"' + (cls ? ' class="' + cls + '"' : '') + (dis ? ' disabled' : '') + ' aria-label="' + (isNaN(label) ? label : 'Page ' + label) + '">' + label + '</button>'; };
    var h = btn('‹', this.page - 1, '', this.page === 1);
    var seq = [];
    for (var p = 1; p <= pages; p++) if (p === 1 || p === pages || Math.abs(p - this.page) <= 1) seq.push(p);
    var last = 0;
    seq.forEach(function (p) { if (p - last > 1) h += '<span class="gap" style="border:0;background:none">…</span>'; h += btn(p, p, p === self.page ? 'on' : ''); last = p; });
    h += btn('›', this.page + 1, '', this.page === pages);
    box.innerHTML = h;
  };
  List.prototype.syncHeaders = function () {
    var s = this.sort;
    this.heads.forEach(function (th, i) { if (th.hasAttribute('data-sort')) th.setAttribute('data-sort', s && !s.fn && s.col === i ? s.dir : 'none'); });
  };
  List.prototype.updateTabCounts = function () {
    var self = this;
    (this.tabs || []).forEach(function (t) {
      var n = self.items.filter(function (it) { return !it.classList.contains('row-gone') && self.matches(it, true) && (t.all || tabMatches(self, t, it)); }).length;
      if (t.b) t.b.textContent = n;
      t.el.setAttribute('aria-selected', String(self.tab === t || (!self.tab && t.initial)));
    });
  };

  // ---------- Tabs ----------
  var setupTabs = function (box, list) {
    var tabs = qa(':scope > span, :scope > a:not([href])', box).map(function (el, i) {
      var b = q('b', el), label = (b ? el.textContent.replace(b.textContent, '') : el.textContent).trim();
      var all = /^all\b/i.test(label) || (i === 0 && /^(all|open|active)/i.test(label) && false);
      var t = { el: el, b: b, label: label, key: norm(label), all: false, initial: el.classList.contains('on') };
      el.setAttribute('role', 'tab'); el.setAttribute('tabindex', '0'); el.setAttribute('data-tab', '');
      t.all = all || t.initial;                           // the tab the screen opens on holds every row that exists
      return t;
    });
    if (!tabs.length) return;
    list.tabs = (list.tabs || []).concat(tabs);
    box.setAttribute('role', 'tablist');
    var pick = function (t) {
      list.tabs.forEach(function (x) { x.el.classList.toggle('on', x === t); });
      list.tab = t.all ? null : t;
      list.apply(true);
    };
    tabs.forEach(function (t) {
      t.el.addEventListener('click', function () { pick(t); });
      t.el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(t); } });
    });
  };

  // ---------- Dropdowns ----------
  var HEAD_ALIAS = {
    status: ['status', 'order status', 'fulfilment', 'payment status', 'delivery status'], payment: ['payment', 'payment status'], region: ['region', 'territory'],
    warehouse: ['warehouse', 'dispatched from', 'location'], mode: ['mode', 'payment mode'], 'payment mode': ['payment mode', 'mode'], reason: ['reason'],
    role: ['role'], organisation: ['organisation'], dealer: ['dealer', 'sold to', 'customer'], retailer: ['retailer', 'customer'], customer: ['customer', 'dealer', 'retailer'],
    'issue type': ['issue type'], 'assigned to': ['assigned to'], 'recorded by': ['recorded by'], product: ['product'], type: ['type'], action: ['action'], area: ['area', 'territory'],
    city: ['city'], tier: ['tier'], vehicle: ['vehicle'], transporter: ['transporter'], category: ['category'], priority: ['priority'], user: ['user', 'by'], dispute: ['dispute']
  };
  var colFor = function (list, label) {
    if (list.kind !== 'table') return -1;
    var want = HEAD_ALIAS[label.toLowerCase()] || [label.toLowerCase()];
    for (var w = 0; w < want.length; w++)
      for (var i = 0; i < list.heads.length; i++) if (list.heads[i].textContent.trim().toLowerCase() === want[w]) return i;
    return -1;
  };
  var DATE_OPTIONS = [['Last 7 days', 7], ['Last 30 days', 30], ['Last 90 days', 90], ['Last 12 months', 365], ['All time', 100000]];
  var setSelValue = function (el, text) {
    var v = q('.v', el); if (v) v.textContent = text;
  };
  var prepSel = function (el) {
    var small = q('small', el), label = small ? small.textContent.trim() : '';
    var rest = []; Array.prototype.forEach.call(el.childNodes, function (n) { if (n.nodeType === 3 && n.textContent.trim()) rest.push(n); });
    var val = rest.map(function (n) { return n.textContent.trim(); }).join(' ');
    rest.forEach(function (n) { n.remove(); });
    var v = document.createElement('span'); v.className = 'v'; v.textContent = val;
    var ic = q('svg.ic, i[data-icon="down"]', el);
    if (ic && ic.parentNode === el) el.insertBefore(v, ic); else el.appendChild(v);
    el.insertBefore(document.createTextNode(' '), v);
    el.setAttribute('role', 'button'); el.setAttribute('tabindex', '0'); el.setAttribute('aria-haspopup', 'listbox'); el.setAttribute('aria-expanded', 'false');
    return { el: el, label: label, initial: val };
  };
  var wireSel = function (s, getOptions, onPick) {
    var open = function () {
      var o = getOptions();
      A.menu(s.el, o.items, { selected: o.selected, footer: o.footer, onPick: function (it) { setSelValue(s.el, it.show || it.label); o.selected = it.value; onPick(it); } });
    };
    s.el.addEventListener('click', open);
    s.el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowDown') { e.preventDefault(); open(); } });
  };

  var setupSel = function (el, list) {
    var s = prepSel(el), label = s.label.toLowerCase();
    var sel = { value: s.initial };
    var lbl = s.label || el.getAttribute('aria-label') || '';
    if (label === 'period' && /^October 2026$/.test(s.initial)) {                 // one month of data exists: the others are listed, greyed out
      var months = ['October 2026', 'September 2026', 'August 2026', 'July 2026', 'June 2026', 'May 2026'];
      wireSel(s, function () { return { items: months.map(function (m, i) { return { label: m, value: m, disabled: i > 0, hint: i > 0 ? 'No data' : '' }; }), selected: 'October 2026' }; }, function () {});
      return;
    }
    if (/^(period|as on|day|month|financial year|year)$/.test(label)) {          // a single value
      wireSel(s, function () { return { items: [{ label: s.initial, value: s.initial }], selected: s.initial }; }, function () {});
      return;
    }
    if (label === 'compared with') {
      wireSel(s, function () { return { items: [{ label: s.initial, value: 'on' }, { label: 'No comparison', value: 'off' }], selected: sel.cur || 'on' }; }, function (it) {
        sel.cur = it.value; qa('main .delta').forEach(function (d) { d.hidden = it.value === 'off'; });
      });
      return;
    }
    if (!list) { wireSel(s, function () { return { items: [{ label: s.initial, value: s.initial }], selected: s.initial }; }, function () {}); return; }
    if (label === 'sort by') {
      list.selects.push(s);
      wireSel(s, function () { return sortOptions(list, s); }, function (it) { list.sort = it.value ? { col: it.col, dir: it.dir, fn: it.fn } : null; list.apply(true); });
      return;
    }
    if (/^(date range|submitted|since|date)$/.test(label)) {
      var col = -1; list.heads.forEach(function (h, i) { if (col < 0 && /date|submitted|raised|issued|reported/i.test(h.textContent)) col = i; });
      var items = DATE_OPTIONS.map(function (o) { return { label: o[0], value: o[1] }; });
      var initialIdx = -1; items.forEach(function (it, i) { if (it.label.toLowerCase() === s.initial.toLowerCase()) initialIdx = i; });
      if (initialIdx < 0) items.unshift({ label: s.initial, value: -1 });
      var cur = initialIdx < 0 ? -1 : items[initialIdx].value;
      wireSel(s, function () { return { items: items, selected: cur }; }, function (it) {
        cur = it.value;
        list.date = it.value === -1 || it.value === 100000 ? null : { col: col, from: A.today - it.value * A.DAY, to: A.today + 400 * A.DAY };
        list.apply(true);
      });
      return;
    }
    // A filter on a column (tables) or on a card attribute (product grid).
    var f = { value: null, get: null, match: null };
    if (list.kind === 'cards') {
      f.get = function (it) { return cardAttr(it, label); };
    } else {
      var c = colFor(list, s.label);
      if (c < 0) { wireSel(s, function () { return { items: [{ label: s.initial, value: s.initial }], selected: s.initial }; }, function () {}); return; }
      f.get = function (it) { return colText(it, c).replace(/\s+\d+\s+days?$/i, '').replace(/\s*[-−]?\d+$/, ''); };
      f.col = c;
      f.match = function (cell, want) { return cell.toLowerCase().indexOf(want.toLowerCase()) === 0 || cell.toLowerCase() === want.toLowerCase(); };
    }
    list.filters.push(f); f.label = s.label;
    var optionValues = function () {
      var seen = {}, out = [];
      list.items.forEach(function (it) { var v = String(f.get(it)).trim(); if (v && v !== '—' && !seen[v.toLowerCase()]) { seen[v.toLowerCase()] = 1; out.push(v); } });
      out.sort(function (a, b) { return a.localeCompare(b, 'en', { numeric: true }); });
      return out;
    };
    f.options = optionValues;
    wireSel(s, function () {
      var vals = optionValues();
      var items = [{ label: s.initial, value: null, show: s.initial }].concat(vals.map(function (v) { return { label: v, value: v }; }));
      return { items: items, selected: f.value };
    }, function (it) { f.value = it.value; list.apply(true); });
  };
  var cardAttr = function (card, label) {
    var tags = qa('.tags .tag', card).map(function (t) { return t.textContent.trim(); });
    if (label === 'finish') return tags[1] || '';
    if (label === 'thickness') return tags.filter(function (t) { return /mm$/.test(t); })[0] || '';
    if (label === 'availability') { var c = q('.chip', card); return c ? c.textContent.trim() : 'In Stock'; }
    return '';
  };
  var cardName = function (c) { return (q('h3', c) || c).textContent.trim().toLowerCase(); };
  var cardPrice = function (c) { var b = q('.slabs b', c); return b ? A.parseMoney(b.textContent) : 0; };
  var sortOptions = function (list, s) {
    var items = [];
    if (list.kind === 'cards') {
      items = [{ label: 'Product Name', value: null, show: 'Product Name' },
        { label: 'Product Name, Z to A', value: 1, dir: 'desc', fn: cardName, show: 'Product Name, Z to A' },
        { label: 'Price, low to high', value: 1, dir: 'asc', fn: cardPrice, show: 'Price, low to high' },
        { label: 'Price, high to low', value: 1, dir: 'desc', fn: cardPrice, show: 'Price, high to low' },
        { label: 'Finish', value: 1, dir: 'asc', fn: function (c) { return cardAttr(c, 'finish').toLowerCase(); }, show: 'Finish' }];
      return { items: items, selected: list.sort ? items.filter(function (i) { return i.fn === list.sort.fn && i.dir === list.sort.dir; })[0].value : null };
    }
    items.push({ label: s.initial + ' (as listed)', value: null, show: s.initial });
    list.heads.forEach(function (th, i) {
      var t = th.textContent.trim(); if (!t || th.querySelector('input')) return;
      var type = colType(list, i);
      var d = type === 'date' ? ['newest first', 'oldest first'] : type === 'text' ? ['A to Z', 'Z to A'] : ['high to low', 'low to high'];
      var dirs = type === 'text' ? ['asc', 'desc'] : ['desc', 'asc'];
      items.push({ label: t + ', ' + d[0], value: 1, col: i, dir: dirs[0], show: t + ', ' + d[0] });
      items.push({ label: t + ', ' + d[1], value: 1, col: i, dir: dirs[1], show: t + ', ' + d[1] });
    });
    var cur = list.sort && !list.sort.fn ? items.filter(function (i) { return i.col === list.sort.col && i.dir === list.sort.dir; })[0] : null;
    return { items: items, selected: cur ? cur.value : null };
  };

  // ---------- Sortable table headers ----------
  var setupHeaders = function (list) {
    if (list.kind !== 'table' || list.items.length < 3 || list.el.hasAttribute('data-nosort')) return;
    list.heads.forEach(function (th, i) {
      if (!th.textContent.trim() || th.querySelector('input')) return;
      th.setAttribute('data-sort', 'none'); th.setAttribute('tabindex', '0'); th.setAttribute('role', 'columnheader');
      var go = function () {
        var cur = list.sort && !list.sort.fn && list.sort.col === i ? list.sort.dir : 'none';
        var type = colType(list, i), first = type === 'text' ? 'asc' : 'desc';
        var next = cur === 'none' ? first : cur === first ? (first === 'asc' ? 'desc' : 'asc') : 'none';
        list.sort = next === 'none' ? null : { col: i, dir: next };
        list.selects.forEach(function (s) { if (!list.sort) setSelValue(s.el, s.initial); });
        list.apply(true);
      };
      th.addEventListener('click', go);
      th.addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); });
    });
  };

  // ---------- Pager clicks ----------
  var setupPager = function (list) {
    if (!list.pg) return;
    list.pg.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-p]'); if (!b || b.disabled) return;
      list.page = +b.getAttribute('data-p'); list.apply(false);
      var top = list.card.getBoundingClientRect().top; if (top < 0) list.card.scrollIntoView({ block: 'start', behavior: 'smooth' });
    });
  };

  // ---------- Row selection ----------
  var setupSelection = function (list) {
    if (list.kind !== 'table') return;
    var head = q('thead input[type=checkbox]', list.el);
    var rows = function () { return list.items.filter(function (it) { return !it.hidden; }); };
    list.items.forEach(function (it) {
      var cb = q('td input[type=checkbox]', it); if (!cb) return;
      cb.addEventListener('change', function () { it.classList.toggle('selected', cb.checked); });
    });
    if (head) head.addEventListener('change', function () {
      rows().forEach(function (it) { var cb = q('td input[type=checkbox]', it); if (cb) { cb.checked = head.checked; it.classList.toggle('selected', head.checked); } });
    });
  };

  // ---------- Start ----------
  A.onReady(30, function () {
    var byEl = {};
    var listFor = function (el) { if (!el) return null; var id = A.lists.map(function (l) { return l.el; }).indexOf(el); return id >= 0 ? A.lists[id] : new List(el); };
    // 1. search boxes, dropdowns and tabs inside filter bars and card headers
    qa('main .filters, main .tabs').forEach(function (F) {
      var list = listFor(collectionFor(F));
      if (F.classList.contains('tabs')) { if (list) setupTabs(F, list); return; }
      qa('.finder input', F).forEach(function (inp) {
        if (!list) return;
        inp.addEventListener('input', function () { list.query = inp.value.trim().toLowerCase(); list.apply(true); });
      });
    });
    qa('main header .finder input').forEach(function (inp) {
      if (inp.closest('.filters')) return;
      var list = listFor(collectionFor(inp.closest('.finder')));
      if (list) inp.addEventListener('input', function () { list.query = inp.value.trim().toLowerCase(); list.apply(true); });
    });
    // dropdowns: all of them, wherever they are
    qa('main .sel').forEach(function (el) {
      if (el.hasAttribute('data-own')) return;
      var anchor = el.closest('.filters') || el;
      setupSel(el, listFor(collectionFor(anchor)));
    });
    // lists with no controls still get sortable headers and a pager
    qa('main table.tbl, main .products, main ul.feed').forEach(function (el) { listFor(el); });
    A.lists.forEach(function (l) { setupHeaders(l); setupPager(l); setupSelection(l); });
    // feeds: the "unread" tab needs the unread class; nothing else to do
    A.lists.forEach(function (l) { if (l.tabs || l.pg) l.apply(false); });
    // 2. grid and list view
    qa('main .view-toggle').forEach(function (vt) {
      var spans = qa(':scope > span', vt), grid = collectionFor(vt);
      spans.forEach(function (sp, i) {
        sp.setAttribute('role', 'button'); sp.setAttribute('tabindex', '0'); sp.setAttribute('aria-label', i === 0 ? 'Grid view' : 'List view');
        var go = function () { spans.forEach(function (x) { x.classList.toggle('on', x === sp); }); if (grid) grid.classList.toggle('list-view', i === 1); };
        sp.addEventListener('click', go);
        sp.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
      });
    });
    // 3. quantity steppers
    qa('.qty').forEach(wireQty);
    // 4. ?q=text (from the top-bar search) fills the first search box of the screen
    var qv = new URLSearchParams(location.search).get('q'), box = q('main .finder input');
    if (qv && box) { box.value = qv; box.dispatchEvent(new Event('input')); }
  });

  // ---------- Quantity steppers ----------
  var STEP = 10;
  var wireQty = function (box) {
    var inp = q('input', box), parts = qa(':scope > span', box), minus = parts[0], plus = parts[parts.length - 1];
    if (!inp || box._wired) return; box._wired = true;
    var get = function () { return Math.max(0, parseInt(String(inp.value).replace(/[^\d]/g, ''), 10) || 0); };
    var limits = function () {
      var max = +inp.getAttribute('data-max') || +box.getAttribute('data-max') || 0, min = +box.getAttribute('data-min') || 0;
      var row = box.closest('tr');
      if (!max && row) {                                   // returns: the most that can be returned is what was ordered
        var th = qa('thead th', row.closest('table')); th.forEach(function (h, i) { if (/^ordered sheets$/i.test(h.textContent.trim()) && row.cells[i]) max = parseInt(row.cells[i].textContent.replace(/[^\d]/g, ''), 10) || max; });
      }
      return { min: min, max: max };
    };
    var set = function (v, quiet) {
      var l = limits(); v = Math.max(l.min, l.max ? Math.min(l.max, v) : v);
      inp.value = v; box.classList.remove('bad');
      minus.setAttribute('aria-disabled', String(v <= l.min)); plus.setAttribute('aria-disabled', String(!!l.max && v >= l.max));
      if (!quiet) box.dispatchEvent(new CustomEvent('qtychange', { bubbles: true, detail: { value: v } }));
    };
    [[minus, -1, 'Decrease'], [plus, 1, 'Increase']].forEach(function (p) {
      var sp = p[0]; sp.setAttribute('role', 'button'); sp.setAttribute('tabindex', '0'); sp.setAttribute('aria-label', p[2] + ' sheets');
      var go = function () { var v = get(), s = +box.getAttribute('data-step') || STEP; set(p[1] < 0 ? Math.max(0, (v % s ? Math.floor(v / s) * s : v - s)) : (Math.floor(v / s) + 1) * s); };
      sp.addEventListener('click', go);
      sp.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
    });
    inp.addEventListener('change', function () { set(get()); });
    inp.addEventListener('input', function () { inp.value = String(inp.value).replace(/[^\d]/g, ''); });
    inp.addEventListener('keydown', function (e) { if (e.key === 'ArrowUp') { e.preventDefault(); plus.click(); } else if (e.key === 'ArrowDown') { e.preventDefault(); minus.click(); } else if (e.key === 'Enter') { inp.blur(); } });
    set(get(), true);
    box.setSheets = function (v) { set(v, true); };
  };
  A.wireQty = wireQty;
})();
