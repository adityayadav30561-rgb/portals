/*
 * Behaviour layer, part 1: state, helpers and small UI pieces (toast, dialog, dropdown). Classic script, no imports.
 * Load after registry.js, shell.js and (on app screens) chrome.js. Other modules (app-lists, app-orders, app-forms,
 * app-files) add to window.APP.
 *
 * State lives in the URL, never in browser storage: one `st` parameter holds a small JSON object (cart, submitted
 * orders, created records, changed statuses). Every internal link carries it; every change writes it back into the
 * address bar, so a reload keeps it. "Reset Data" in the review bar clears it. Shape (all keys optional):
 *   c: { portalId: [[sku, qty], ...] }     draft order (absent: the designed draft)
 *   o: { portalId: [order, ...] }          orders submitted in this session
 *   r: { collection: [row, ...] }          records created by forms; row = { "Column Heading": "text", ... }
 *   x: { "SCREEN|row key": "New Status" }  status changes (approve, close, mark as packed ...)
 *   d: [ "SCREEN|row key", ... ]           removed rows
 *   n: [ "SCREEN|row key", ... ]           notifications read
 *   m: { "SCREEN|ticket": [[who, text, time], ...] }  conversation messages added
 */
(function () {
  var P = window.PORTAL;
  var A = window.APP = window.APP || {};
  A.q = function (sel, el) { return (el || document).querySelector(sel); };
  A.qa = function (sel, el) { return Array.prototype.slice.call((el || document).querySelectorAll(sel)); };
  A.esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  A.screen = document.body.getAttribute('data-screen') || '';
  A.role = P && P.current ? P.current.role : null;
  A.portal = P && P.current ? P.current.portal : null;
  A.icon = function (n) { return P && P.icon ? P.icon(n).replace('<svg ', '<svg class="ic" ') : ''; };

  // ---------- State in the URL ----------
  var enc = function (o) { return btoa(unescape(encodeURIComponent(JSON.stringify(o)))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); };
  var dec = function (s) {
    try { return JSON.parse(decodeURIComponent(escape(atob(s.replace(/-/g, '+').replace(/_/g, '/'))))); } catch (e) { return {}; }
  };
  var params = new URLSearchParams(location.search);
  A.state = params.get('st') ? dec(params.get('st')) : {};
  // Empty containers are left out of the URL (the state object itself keeps them, so modules can always write into it).
  var clean = function () {
    var o = {};
    Object.keys(A.state).forEach(function (k) {
      var v = A.state[k];
      if (v == null || (Array.isArray(v) && !v.length)) return;
      if (typeof v === 'object' && !Array.isArray(v)) {
        var inner = {}; Object.keys(v).forEach(function (j) { var w = v[j]; if (!(w == null || (Array.isArray(w) && !w.length && k !== 'c') || (typeof w === 'object' && !Array.isArray(w) && !Object.keys(w).length))) inner[j] = w; });
        if (!Object.keys(inner).length) return; v = inner;
      }
      o[k] = v;
    });
    return o;
  };
  A.encoded = function () { var c = clean(); return Object.keys(c).length ? enc(c) : ''; };
  A.save = function () {
    var u = new URL(location.href), e = A.encoded();
    if (e) u.searchParams.set('st', e); else u.searchParams.delete('st');
    try { history.replaceState(null, '', u.toString()); } catch (x) { /* some browsers refuse on file:// with a long query; links still carry the state */ }
  };
  // The URL of a screen with the current state added.
  A.withState = function (href) {
    var e = A.encoded();
    if (!href || /^(mailto:|tel:|#|javascript:)/.test(href)) return href;
    var u;
    try { u = new URL(href, location.href); } catch (x) { return href; }
    if (u.protocol !== 'file:' && u.origin !== location.origin) return href;
    if (!/\.html$/.test(u.pathname)) return href;
    if (e) u.searchParams.set('st', e); else u.searchParams.delete('st');
    return u.toString();
  };
  A.go = function (href) { location.href = A.withState(href); };
  A.link = function (sid) {              // href of another screen (same portal and role) with state
    var t = P.find(sid); if (!t) return '#';
    var r = t.portal.id === A.portal.id ? A.role : t.screen.roles[0];
    var h = P.href(P.root, t.screen, r);
    if (new URLSearchParams(location.search).get('review') === 'off') h += (h.indexOf('?') >= 0 ? '&' : '?') + 'review=off';
    return A.withState(h);
  };
  A.go2 = function (sid) { location.href = A.link(sid); };
  // Links pick up the latest state right before they are used (click, middle click, keyboard, hover for "open in new tab").
  var refresh = function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var h = a.getAttribute('href'), n = A.withState(h);
    if (n && n !== h) a.setAttribute('href', n);
  };
  ['mousedown', 'click', 'auxclick', 'keydown', 'focusin', 'mouseover', 'touchstart'].forEach(function (t) { document.addEventListener(t, refresh, true); });
  if (A.encoded()) A.qa('a[href]').forEach(function (a) { var h = a.getAttribute('href'), n = A.withState(h); if (n && n !== h) a.setAttribute('href', n); });

  // ---------- Formatting (the same rules as tools/author/data.py: M, ML, N) ----------
  A.fmtN = function (n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); };
  A.fmtM = function (n) {
    var neg = n < 0; n = Math.abs(Math.round(n));
    var s = String(n);
    if (s.length > 3) {
      var head = s.slice(0, -3), tail = s.slice(-3), parts = [];
      while (head.length > 2) { parts.unshift(head.slice(-2)); head = head.slice(0, -2); }
      if (head) parts.unshift(head);
      s = parts.join(',') + ',' + tail;
    }
    return (neg ? '−' : '') + '₹' + s;
  };
  var q2 = function (v) { return (Math.floor(v * 100 + 0.5 + 1e-9) / 100).toFixed(2); };   // halves round up
  A.fmtML = function (n) {
    if (n >= 10000000) return '₹' + q2(n / 10000000) + ' crore';
    if (n >= 100000) return '₹' + q2(n / 100000) + ' lakh';
    return A.fmtM(n);
  };
  // Python's round() goes to the even number on halves; the generators use it, so the totals here do too.
  A.roundHE = function (x) {
    var f = Math.floor(x), d = x - f;
    if (Math.abs(d - 0.5) < 1e-9) return f % 2 === 0 ? f : f + 1;
    return Math.round(x);
  };
  // Money in text -> number: ₹1,23,000  ₹6.84 lakh  ₹1.25 crore  −₹16,426
  A.parseMoney = function (t) {
    var m = String(t).replace(/−/g, '-').match(/(-)?\s*₹\s*([\d,]+(?:\.\d+)?)\s*(lakh|crore)?/i);
    if (!m) return null;
    var v = parseFloat(m[2].replace(/,/g, ''));
    if (m[3]) v *= m[3].toLowerCase() === 'lakh' ? 100000 : 10000000;
    return m[1] ? -v : v;
  };
  // dd/mm/yyyy[ hh:mm] -> ms, or null
  A.parseDate = function (t) {
    var m = String(t).match(/(\d{1,2})\/(\d{1,2})\/(\d{4})(?:\s+(\d{1,2}):(\d{2}))?/);
    return m ? new Date(+m[3], +m[2] - 1, +m[1], +(m[4] || 0), +(m[5] || 0)).getTime() : null;
  };
  A.today = new Date(2026, 9, 26).getTime();     // the prototype's "today": 26 October 2026
  A.DAY = 86400000;
  A.fmtDate = function (ms) { var d = new Date(ms); return ('0' + d.getDate()).slice(-2) + '/' + ('0' + (d.getMonth() + 1)).slice(-2) + '/' + d.getFullYear(); };
  A.slug = function (t) { return String(t).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); };

  // ---------- Toast ----------
  var stack = null;
  A.toast = function (text, kind, action) {
    if (!stack) { stack = document.createElement('div'); stack.className = 'toasts'; stack.setAttribute('role', 'status'); stack.setAttribute('aria-live', 'polite'); document.body.appendChild(stack); }
    var t = document.createElement('div');
    t.className = 'toast ' + (kind || 'ok');
    t.innerHTML = '<span class="tt">' + A.esc(text) + '</span>';
    if (action) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'ta'; b.textContent = action.label;
      b.addEventListener('click', function () { action.fn(); t.remove(); });
      t.appendChild(b);
    }
    var x = document.createElement('button'); x.type = 'button'; x.className = 'tx'; x.setAttribute('aria-label', 'Dismiss'); x.innerHTML = A.icon('x');
    x.addEventListener('click', function () { t.remove(); });
    t.appendChild(x);
    stack.appendChild(t);
    setTimeout(function () { t.classList.add('out'); setTimeout(function () { t.remove(); }, 250); }, action ? 6500 : 3800);
    return t;
  };

  // ---------- Dialog ----------
  // A.dialog({ title, body (html), ok: 'Label', cancel: 'Label' | false, danger: bool, onOk: fn(box) -> false to keep open })
  A.dialog = function (o) {
    var prev = document.activeElement;
    var wrap = document.createElement('div'); wrap.className = 'modal';
    wrap.innerHTML = '<div class="box" role="dialog" aria-modal="true" aria-labelledby="dlg-t"><header><h2 id="dlg-t">' + A.esc(o.title) + '</h2><button type="button" class="icon-btn" data-x aria-label="Close">' + A.icon('x') + '</button></header>' +
      '<div class="dbody">' + (o.body || '') + '</div><footer>' + (o.cancel === false ? '' : '<button type="button" class="btn" data-c>' + A.esc(o.cancel || 'Cancel') + '</button>') +
      '<button type="button" class="btn ' + (o.danger ? 'danger' : 'pri') + '" data-ok>' + A.esc(o.ok || 'OK') + '</button></footer></div>';
    document.body.appendChild(wrap);
    var box = wrap.firstChild;
    var close = function () { wrap.remove(); document.removeEventListener('keydown', key, true); if (prev && prev.focus) prev.focus(); };
    var key = function (e) {
      if (e.key === 'Escape') { e.stopPropagation(); close(); }
      if (e.key === 'Tab') {
        var f = A.qa('button, input, select, textarea, a[href]', box).filter(function (x) { return !x.disabled && x.offsetParent !== null; });
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    };
    document.addEventListener('keydown', key, true);
    wrap.addEventListener('mousedown', function (e) { if (e.target === wrap) close(); });
    A.qa('[data-x], [data-c]', box).forEach(function (b) { b.addEventListener('click', close); });
    A.q('[data-ok]', box).addEventListener('click', function () {
      if (o.onOk && o.onOk(box) === false) return;
      close();
    });
    var f0 = A.q('input, select, textarea', box) || A.q('[data-ok]', box); f0.focus();
    return { box: box, close: close };
  };

  // ---------- Dropdown (popover list) ----------
  // A.menu(anchor, [{ label, value, hint, disabled }], { selected: value, onPick: fn(item), footer: 'text' })
  var openMenu = null;
  A.closeMenu = function () { if (openMenu) { openMenu.el.remove(); openMenu.anchor.setAttribute('aria-expanded', 'false'); openMenu = null; } };
  A.menu = function (anchor, items, o) {
    o = o || {};
    if (openMenu && openMenu.anchor === anchor && !o.noFocus) { A.closeMenu(); return; }
    A.closeMenu();
    var el = document.createElement('div'); el.className = 'pop'; el.setAttribute('role', 'listbox');
    el.innerHTML = items.map(function (it, i) {
      var sel = o.selected !== undefined && it.value === o.selected;
      return '<button type="button" role="option" class="opt' + (sel ? ' on' : '') + '" data-i="' + i + '" aria-selected="' + sel + '"' + (it.disabled ? ' disabled' : '') + '><span class="ck">' + (sel ? A.icon('check') : '') + '</span><span>' + A.esc(it.label) + '</span>' + (it.hint ? '<small>' + A.esc(it.hint) + '</small>' : '') + '</button>';
    }).join('') + (o.footer ? '<div class="foot">' + A.esc(o.footer) + '</div>' : '');
    document.body.appendChild(el);
    var r = anchor.getBoundingClientRect(), w = Math.max(r.width, 13 * 16);
    el.style.minWidth = w + 'px';
    var left = Math.min(r.left, window.innerWidth - el.offsetWidth - 8);
    el.style.left = Math.max(8, left) + 'px';
    var below = window.innerHeight - r.bottom, h = el.offsetHeight;
    if (below < h + 12 && r.top > below) { el.style.bottom = (window.innerHeight - r.top + 6) + 'px'; el.style.maxHeight = Math.max(160, r.top - 16) + 'px'; }
    else { el.style.top = (r.bottom + 6) + 'px'; el.style.maxHeight = Math.max(160, below - 16) + 'px'; }
    anchor.setAttribute('aria-expanded', 'true');
    openMenu = { el: el, anchor: anchor };
    var btns = A.qa('.opt:not([disabled])', el);
    var cur = btns.filter(function (b) { return b.classList.contains('on'); })[0] || btns[0];
    if (cur && !o.noFocus) cur.focus();
    el.addEventListener('click', function (e) {
      var b = e.target.closest('.opt'); if (!b) return;
      var it = items[+b.getAttribute('data-i')];
      A.closeMenu(); if (!o.noFocus) anchor.focus();
      if (o.onPick) o.onPick(it);
    });
    el.addEventListener('keydown', function (e) {
      var i = btns.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') { e.preventDefault(); btns[Math.min(btns.length - 1, i + 1)].focus(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); btns[Math.max(0, i - 1)].focus(); }
      else if (e.key === 'Escape') { e.preventDefault(); A.closeMenu(); anchor.focus(); }
      else if (e.key === 'Tab') { A.closeMenu(); }
    });
  };
  document.addEventListener('mousedown', function (e) { if (openMenu && !openMenu.el.contains(e.target) && !openMenu.anchor.contains(e.target)) A.closeMenu(); });
  window.addEventListener('scroll', function (e) { if (openMenu && !openMenu.el.contains(e.target)) A.closeMenu(); }, true);
  window.addEventListener('resize', A.closeMenu);

  // ---------- Reset Data (review bar) ----------
  var bar = A.q('.review .pager');
  if (bar) {
    var rb = document.createElement('button'); rb.type = 'button'; rb.className = 'reset'; rb.textContent = 'Reset Data';
    rb.title = 'Clear everything changed in this session: cart, submitted orders, created records and statuses';
    rb.addEventListener('click', function () {
      A.dialog({ title: 'Reset Data', body: '<p>This clears the order draft, submitted orders, created records and changed statuses, and restores the prototype’s starting data.</p>', ok: 'Reset Data', danger: true,
        onOk: function () { A.state = {}; var u = new URL(location.href); u.searchParams.delete('st'); location.href = u.toString(); } });
    });
    bar.insertBefore(rb, bar.firstChild);
  }

  // ---------- Keys for rows (status changes and removals persist by key) ----------
  A.rowKey = function (tr) {
    var cells = tr.querySelectorAll('th, td'), t = '';
    for (var i = 0; i < cells.length && !t; i++) {
      var c = cells[i], mono = c.querySelector('.mono, a b, a, b');
      t = (mono ? mono.textContent : c.textContent).trim().replace(/\s+/g, ' ');
    }
    return A.screen + '|' + t;
  };
  A.setStatus = function (key, status) { A.state.x = A.state.x || {}; A.state.x[key] = status; A.save(); };
  A.dismiss = function (key) { A.state.d = A.state.d || []; if (A.state.d.indexOf(key) < 0) A.state.d.push(key); A.save(); };
  A.chipClass = function (t) {
    var l = String(t).toLowerCase();
    if (/^(paid|delivered|active|approved|resolved|confirmed payment|credit issued|credit applied|applied|target reached|above target|completed|received|in stock|reached|closed won|on time|accepted|online|reviewed|issued|cleared|done|available|complete|free|current session|passed|met)/.test(l)) return 'ok';
    if (/^(rejected|cancelled|out of stock|overdue|failed|late|below target|deactivated|high|returned|damaged|declined|expired|critical|withdrawn|not applicable|no stock)/.test(l)) return /not applicable/.test(l) ? 'plain' : 'bad';
    if (/^(awaiting|pending|under review|partly paid|low stock|near target|waiting|medium|invited|in progress|draft|planned|upcoming|on hold|due|being packed|pickup scheduled|new|open)/.test(l)) return /^(new|open)/.test(l) ? 'blue' : /^(draft|planned|upcoming)/.test(l) ? 'blue' : 'warn';
    if (/^(in transit|confirmed|sent|dispatched|submitted|scheduled|blue|shipped|packed|received|dispatch planned|pickup scheduled|information requested|upcoming)/.test(l)) return 'blue';
    return 'plain';
  };
  A.chipHtml = function (t, cls) { return '<span class="chip ' + (cls || A.chipClass(t)) + '">' + A.esc(t) + '</span>'; };
  // Replace the text of the status chip in a row (or the element) and its colour.
  A.applyChip = function (chip, status) {
    chip.textContent = status;
    chip.className = 'chip ' + A.chipClass(status);
  };
  // ---------- Start-up order: modules register init functions; app-boot.js runs them once everything is loaded ----------
  var ready = [];
  A.onReady = function (priority, fn) { ready.push({ p: priority, fn: fn, n: ready.length }); };
  A.boot = function () {
    ready.sort(function (a, b) { return a.p - b.p || a.n - b.n; }).forEach(function (r) {
      try { r.fn(); } catch (e) { console.error('app: init failed: ' + (e && e.stack || e)); }
    });
    document.documentElement.classList.add('app-ready');
  };
  document.documentElement.classList.add('js-app');
})();
