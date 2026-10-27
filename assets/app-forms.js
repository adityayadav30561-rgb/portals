/*
 * Behaviour layer, part 4: forms, records and actions.
 *   - Forms validate, create a record and open the list it belongs to (users, tickets, returns, requests, sales, payments, products, schemes).
 *   - Buttons are wired by what they say: Approve, Reject, Close Ticket, Send Reply, Deactivate User, Mark All as Read, Edit ..., Upload ..., Download ..., Export ...
 *   - Everything that changes is kept in the URL state (see app-core.js): created rows (r), status changes (x), removed rows (d),
 *     edited values (e), messages (m), read notifications (n).
 * A control that is not covered here is reported by `node tools/interact.js` as a dead control.
 */
(function () {
  var A = window.APP, P = window.PORTAL, q = A.q, qa = A.qa, esc = A.esc;
  var pid = A.portal ? A.portal.id : '', sid = A.screen, part = sid.split('-').slice(1).join('-'), pre = sid.split('-')[0];
  var text = function (el) { return el ? el.textContent.replace(/\s+/g, ' ').trim() : ''; };
  var params = new URLSearchParams(location.search);
  var person = ((A.portal && (A.portal.roles || []).filter(function (r) { return r.code === A.role; })[0]) || {}).person || 'You';
  A.lists = A.lists || [];
  var nowTime = function () { var d = new Date(); return ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2); };
  var today = '26/10/2026';
  var own = function (el) { el.setAttribute('data-own', '1'); };
  var sidOf = function (suffix) { return pre + '-' + suffix; };
  A.state.x = A.state.x || {}; A.state.d = A.state.d || []; A.state.r = A.state.r || {}; A.state.e = A.state.e || {}; A.state.n = A.state.n || {}; A.state.m = A.state.m || {};
  var persist = function () { A.save(); };

  // ---------- Forms: values, validation ----------
  var OPTIONAL = /optional|note|reference|description|comment|remark|message|^address$|district|colour|weight|grade|pack size|sheet size|bank reference|related|paid from|permanent account|gst number|legal name|postal/i;
  A.formValues = function (scope) {
    var v = {};
    qa('.field', scope).forEach(function (f) {
      var l = q('label', f), c = q('input:not([type=checkbox]):not([type=radio]), select, textarea', f);
      if (l && c) v[text(l)] = c.value.trim();
    });
    qa('label.radio input:checked', scope).forEach(function (r) { v.__radio = text(r.closest('label')).replace(/Free$/, '').trim(); });
    return v;
  };
  var clearErrors = function (scope) { qa('.field.invalid', scope).forEach(function (f) { f.classList.remove('invalid'); }); qa('.err', scope).forEach(function (e) { e.remove(); }); };
  var markBad = function (field, msg) {
    field.classList.add('invalid');
    var e = document.createElement('div'); e.className = 'err'; e.textContent = msg; field.appendChild(e);
  };
  // Returns true when the form is complete. Empty required fields, bad e-mail addresses and non-positive numbers are marked.
  A.validate = function (scope, opts) {
    opts = opts || {}; clearErrors(scope); var first = null, ok = true;
    qa('.field', scope).forEach(function (f) {
      var l = q('label', f), c = q('input:not([type=checkbox]):not([type=radio]), select, textarea', f); if (!l || !c || f.closest('[hidden]')) return;
      var name = text(l), val = c.value.trim(), req = opts.required ? opts.required.indexOf(name) >= 0 : !(c.tagName === 'TEXTAREA' || OPTIONAL.test(name) || c.hasAttribute('data-optional'));
      var msg = '';
      if (req && !val) msg = 'Enter the ' + name.toLowerCase();
      else if (val && /e-?mail/i.test(name) && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(val)) msg = 'Enter a valid email address';
      else if (val && /mobile|phone/i.test(name) && val.replace(/\D/g, '').length < 10) msg = 'Enter a 10-digit mobile number';
      if (msg) { markBad(f, msg); ok = false; if (!first) first = c; }
    });
    if (first) first.focus();
    return ok;
  };

  // ---------- Form dialog ----------
  // A.formDialog({ title, ok, fields: [{ label, value, type: text|select|textarea|date|number, options, required }], onOk(values) })
  A.formDialog = function (o) {
    var html = '<div class="form-grid">' + o.fields.map(function (f, i) {
      var id = 'fd' + i, ctl;
      if (f.type === 'select') ctl = '<select class="input" id="' + id + '">' + f.options.map(function (x) { return '<option' + (x === f.value ? ' selected' : '') + '>' + esc(x) + '</option>'; }).join('') + '</select>';
      else if (f.type === 'textarea') ctl = '<textarea class="input" id="' + id + '" placeholder="' + esc(f.placeholder || '') + '">' + esc(f.value || '') + '</textarea>';
      else ctl = '<input class="input" id="' + id + '" value="' + esc(f.value || '') + '" placeholder="' + esc(f.placeholder || '') + '"' + (f.type === 'number' ? ' inputmode="numeric"' : '') + '>';
      return '<div class="field' + (f.full ? ' full' : '') + '"><label for="' + id + '">' + esc(f.label) + '</label>' + ctl + '</div>';
    }).join('') + '</div>';
    return A.dialog({ title: o.title, body: (o.intro ? '<p>' + esc(o.intro) + '</p>' : '') + html, ok: o.ok || 'Save', danger: o.danger, extra: o.extra, onOk: function (box) {
      var req = o.fields.filter(function (f) { return f.required !== false && f.type !== 'textarea' || f.required; }).map(function (f) { return f.label; });
      if (!A.validate(box, { required: req })) return false;
      var v = {}; o.fields.forEach(function (f, i) { v[f.label] = q('#fd' + i, box).value.trim(); });
      return o.onOk(v);
    } });
  };

  // ---------- Hydrate: apply what earlier screens changed ----------
  var statusCol = function (tr) {
    var heads = qa('thead th', tr.closest('table')).map(text), i = -1;
    heads.forEach(function (h, k) { if (i < 0 && /^(status|order status|fulfilment|decision)$/i.test(h)) i = k; });
    return i;
  };
  var applyRowStatus = function (tr, status) {
    var ci = statusCol(tr), cell = ci >= 0 ? tr.cells[ci] : null, chips = qa('.chip', cell || tr);
    if (cell && qa('button, a.btn', cell).length) { cell.innerHTML = A.chipHtml(status); return; }
    if (chips.length) A.applyChip(chips[chips.length > 1 && !cell ? chips.length - 1 : 0], status);
    else if (cell) cell.innerHTML = A.chipHtml(status);
  };
  A.hydrate = function () {
    var px = sid + '|';
    qa('main table.tbl tbody tr').forEach(function (tr) {
      var k = A.rowKey(tr);
      if (A.state.d.indexOf(k) >= 0) tr.classList.add('row-gone');
      if (A.state.x[k]) applyRowStatus(tr, A.state.x[k]);
    });
    var page = A.state.x[px + 'page'];
    if (page) { var c = q('.title-row .chip') || q('main .head .chip'); if (c) A.applyChip(c, page); }
    var ed = A.state.e[sid];
    if (ed) qa('main dt').forEach(function (dt) { var v = ed[text(dt)]; if (v !== undefined) dt.nextElementSibling.textContent = v; });
    if (ed && ed.__title) { var h1 = q('main h1'); if (h1) h1.textContent = ed.__title; }
  };

  // ---------- Created records appear in their lists ----------
  var addRows = function () {
    var recs = A.state.r[sid]; if (!recs || !recs.length) return;
    var table = q('main table.tbl'); if (!table) return;
    var heads = qa('thead th', table).map(text), tbody = table.tBodies[0], tpl = tbody.rows[0];
    recs.slice().reverse().forEach(function (rec) {
      var tr = tpl ? tpl.cloneNode(true) : document.createElement('tr');
      tr.classList.remove('row-gone', 'selected'); tr.hidden = false; tr.classList.add('row-new');
      heads.forEach(function (h, i) {
        var c = tr.cells[i]; if (!c) return;
        var v = rec[h]; if (v === undefined) { if (h) c.innerHTML = '—'; return; }
        if (/^(status|order status|fulfilment|decision)$/i.test(h) || /^(Payment|Payment Mode|Priority)$/.test(h) && /^(Paid|Partly Paid|Unpaid|High|Medium|Low)$/.test(v)) c.innerHTML = A.chipHtml(v);
        else if (i === 0) c.innerHTML = '<b>' + esc(v) + '</b>';
        else if (/^(sheets|value|amount|credit amount|requested credit|price per sheet)$/i.test(h)) c.innerHTML = '<b>' + esc(v) + '</b>';
        else c.textContent = v;
      });
      qa('.row-actions', tr).forEach(function (ra) { ra.innerHTML = '<button class="btn sm" type="button">View</button>'; });
      tbody.insertBefore(tr, tbody.firstChild);
    });
  };

  // Collections: a form screen -> the list that receives its record.
  var series = { tickets: { primary: ['TKT-2026-', 735, 4], secondary: ['TKT-2026-D', 751, 4], tertiary: ['TKT-2026-B', 455, 4] },
    returns: { primary: ['RTN-2026-', 413, 4], secondary: ['RTN-2026-D', 512, 4], tertiary: ['RTN-2026-B', 218, 4] },
    dealerReq: { primary: ['DRQ-2026-', 18, 4] }, retailerReq: { secondary: ['RRQ-2026-', 8, 4] },
    sale: { primary: ['SAL-2026-', 3043, 4], secondary: ['TSL-2026-', 414, 4], tertiary: ['RSL-2026-', 399, 4] }, payment: { primary: ['PAY-2026-', 2218, 5] } };
  var numberFor = function (kind, listId) {
    var s = series[kind][pid], n = s[1] + (A.state.r[listId] || []).length;
    return s[0] + String(n).padStart(s[2], '0');
  };
  var dateIn = function () { return today; };
  var COLL = {
    'USR-02': { list: 'USR-01', make: function (v) { return { Name: v['First Name'] + ' ' + v['Last Name'], Role: v.__radio, 'Email Address': v['Email Address'], 'Last Sign-In': 'Not yet', Status: 'Invited' }; }, msg: function (r) { return 'Invitation sent to ' + r['Email Address']; } },
    'SUP-02': { list: 'SUP-01', make: function (v, lid) { return { 'Ticket Number': numberFor('tickets', lid), Subject: v.Subject, Category: v.Category, Priority: v.Priority, Created: today, 'Last Updated': today, Status: 'Open' }; }, msg: function (r) { return 'Ticket ' + r['Ticket Number'] + ' submitted'; } },
    'RET-02': { list: 'RET-01', make: function (v, lid) {
      var rows = qa('main table.tbl tbody tr').map(function (tr) { var inp = q('.qty input', tr); return { sku: text(q('td.mono', tr)), name: text(q('b', tr)), n: inp ? parseInt(inp.value, 10) || 0 : 0 }; }).filter(function (r) { return r.n > 0; });
      return { 'Return Number': numberFor('returns', lid), Date: today, 'Order Number': (v.Order || '').split(' ')[0], Product: rows.length > 1 ? rows[0].name + ' and ' + (rows.length - 1) + ' more' : rows[0].name, Sheets: String(rows.reduce(function (n, r) { return n + r.n; }, 0)), Reason: v['Return Reason'], Status: 'Under Review', 'Credit Amount': '—' };
    }, check: function () { return qa('main table.tbl .qty input').some(function (i) { return parseInt(i.value, 10) > 0; }) || 'Enter the sheets to return for at least one product'; }, msg: function (r) { return 'Return request ' + r['Return Number'] + ' submitted'; } },
    'DLR-03': { list: 'DLR-06', make: function (v, lid) { return { 'Request Number': numberFor('dealerReq', lid), Dealer: v['Dealer Business Name'], Submitted: today, 'Requested Credit': v['Requested Credit Limit'], Documents: '0 of 3', Decision: 'Awaiting Your Review' }; }, msg: function (r) { return 'Dealer request ' + r['Request Number'] + ' submitted for review'; } },
    'RTL-03': { list: 'RTL-06', make: function (v, lid) { return { 'Request Number': numberFor('retailerReq', lid), Retailer: v['Retailer Business Name'], Owner: v['Owner Name'], Submitted: today, 'Requested Credit': v['Requested Credit Limit'], 'Sheets per Month': v['Expected Monthly Volume in Sheets'], Documents: '0 of 3', Decision: 'Awaiting Your Review' }; }, msg: function (r) { return 'Retailer request ' + r['Request Number'] + ' submitted for review'; } },
    'PRD-03': { list: 'PRD-01', make: function (v) { return { Product: v['Product Name'], SKU: v.SKU, Finish: v.Finish, Thickness: v.Thickness, 'Price per Sheet': v['1 to 49 Sheets'], 'Available Sheets': '0', 'Reorder Level': v['Reorder Level in Sheets'], Status: v['Product Status'] === 'Draft' ? 'Draft' : 'Out of Stock' }; }, msg: function (r) { return 'Product ' + r.Product + ' created'; } },
    'SCH-03': { list: 'SCH-01', make: function (v) { return { Scheme: v['Scheme Name'], 'Scheme Number': v['Scheme Number'], Type: v['Scheme Type'], Ends: v['End Date'], 'Progress in Sheets': '0 of ' + v['Target in Sheets'], Reward: v['Reward Value'] + ' ' + v['Reward Basis'], Status: 'Upcoming' }; }, msg: function (r) { return 'Scheme ' + r.Scheme + ' created'; } }
  };
  var SALE_TARGET = { primary: ['SAL-02', 'SAL-03'], secondary: ['TSL-02', 'TSL-03'], tertiary: ['RTS-01', 'RTS-02'] };

  var submitRecord = function (key, extra) {
    var cfg = COLL[key]; if (!cfg) return false;
    var scope = q('main');
    if (!A.validate(scope)) { A.toast('Complete the highlighted fields', 'warn'); return true; }
    if (cfg.check) { var c = cfg.check(); if (c !== true) { A.toast(c, 'warn'); return true; } }
    var listId = sidOf(cfg.list), rec = cfg.make(A.formValues(scope), listId, extra);
    (A.state.r[listId] = A.state.r[listId] || []).push(rec);
    A.state.t = { m: cfg.msg(rec) };
    persist();
    A.goList(listId);
    return true;
  };

  // ---------- Button wiring by label ----------
  var wired = function (b) { return b.hasAttribute('data-own') || b._act; };
  var back = function () {
    var par = P.parent ? P.parent(A.portal, P.current.screen, A.role) : null;
    if (par && par.built) A.go2(par.id); else if (history.length > 1 && document.referrer) history.back(); else A.go2(P.dashboard(A.portal, A.role).id);
  };
  var rowOf = function (b) { return b.closest('tbody tr'); };
  var refOf = function (b) {
    var r = rowOf(b); if (r) return text(r.cells[0]).split(' ')[0];
    var m = q('.title-row h1, main h1'); return m ? text(m) : '';
  };
  var setStatusFor = function (b, status, noun) {
    var r = rowOf(b), key = r ? A.rowKey(r) : sid + '|page', before;
    A.state.x[key] = status;
    if (r) { applyRowStatus(r, status); }
    else {
      var c = q('.title-row .chip') || q('main .head .chip'); if (c) { before = text(c); A.applyChip(c, status); }
      // the same record may be listed further down the screen: keep it in step
      var ref = text(q('main .mono')) || '';
      qa('main table.tbl tbody tr').forEach(function (tr) { if (ref && text(tr.cells[0]).indexOf(ref) === 0) { A.state.x[A.rowKey(tr)] = status; applyRowStatus(tr, status); } });
      qa('main .card header .chip, main .card .chip').forEach(function (c2) { if (/^(Waiting|Awaiting|Pending|Under Review|Open|New)/.test(text(c2)) && !c2.closest('tbody')) A.applyChip(c2, status); });
    }
    persist(); A.lists.forEach(function (l) { l.apply(false); });
    return before;
  };
  var disable = function (b, label) { b.disabled = true; b.setAttribute('aria-disabled', 'true'); if (label) b.textContent = label; };
  var STATUS_ACTIONS = [
    // [label regex, new status, toast verb, needs a reason, asks first, button after]
    [/^Approve Customer$/, 'Approved', 'Approved', 0, 0], [/^Approve Request$/, 'Approved', 'Approved', 0, 0], [/^Approve$/, 'Approved', 'Approved', 0, 0],
    [/^Approve and Schedule Pickup$/, 'Pickup Scheduled', 'Pickup scheduled for', 0, 0], [/^Reject( Request)?$/, 'Rejected', 'Rejected', 1, 0],
    [/^Request More Information$/, 'Information Requested', 'Information requested for', 2, 0], [/^Place on Hold$/, 'On Hold', 'Placed on hold:', 0, 1], [/^Hold Order$/, 'On Hold', 'Order on hold:', 0, 1],
    [/^Confirm Order$/, 'Confirmed', 'Confirmed', 0, 0], [/^Mark as Packed$/, 'Packed', 'Marked as packed:', 0, 0], [/^Receive Shipment$/, 'Received', 'Received', 0, 0],
    [/^Cancel Order$/, 'Cancelled', 'Cancelled', 1, 1], [/^End Scheme$/, 'Completed', 'Ended', 0, 1], [/^Withdraw Dispute$/, 'Withdrawn', 'Withdrawn', 0, 1], [/^Close Ticket$/, 'Closed', 'Closed', 0, 1]
  ];
  var wireStatusActions = function () {
    qa('main button, main a.btn:not([href])').forEach(function (b) {
      if (wired(b)) return;
      var lab = text(b), act = STATUS_ACTIONS.filter(function (a) { return a[0].test(lab); })[0]; if (!act) return;
      b._act = 1;
      b.addEventListener('click', function () {
        var ref = refOf(b), run = function (reason) {
          var rk = rowOf(b), was = setStatusFor(b, act[1]);
          var t = A.toast(act[2] + ' ' + ref, 'ok');
          if (!rowOf(b) && /^(Approve|Reject|Cancel Order|Close|Confirm|Mark|Withdraw|End|Receive)/.test(lab)) disable(b, lab === 'Close Ticket' ? 'Ticket Closed' : b.textContent);
          if (rowOf(b)) qa('button', rowOf(b)).forEach(function (x) { if (/^(Approve|Reject)/.test(text(x))) x.remove(); });
        };
        if (act[3] === 1 || act[3] === 2) {
          A.formDialog({ title: lab + ': ' + ref, ok: lab, danger: act[3] === 1, fields: [{ label: act[3] === 1 ? 'Reason' : 'What do you need to know?', type: 'textarea', required: true, full: true }], onOk: function () { run(); } });
        } else if (act[4]) {
          A.dialog({ title: lab + '?', body: '<p>' + esc(ref) + ' will be shown as ' + act[1].toLowerCase() + '.</p>', ok: lab, danger: /Cancel|End|Withdraw/.test(lab), onOk: function () { run(); } });
        } else run();
      });
    });
  };

  // ---------- Generic download / export / print / save ----------
  var rowPdfLines = function (tr) {
    var heads = qa('thead th', tr.closest('table')).map(text), L = [{ t: 'Laminates Customer Portal', size: 9 }, { t: text(q('main h1')) || document.title, b: true, size: 16, gap: 4 }, { t: A.portal.org + ' - ' + today, size: 9, gap: 8 }];
    qa('td', tr).forEach(function (c, i) { if (heads[i]) L.push({ t: heads[i] + ': ' + text(c), size: 10 }); });
    return L;
  };
  var wireFiles = function () {
    qa('main button, main a.btn:not([href]), main .icon-btn:not([href])').forEach(function (b) {
      if (wired(b)) return;
      var lab = text(b) || b.getAttribute('aria-label') || '', tr = rowOf(b);
      if (/^Export\b/.test(lab)) { b._act = 1; b.addEventListener('click', A.exportCsv); }
      else if (/^Print\b/.test(lab)) { b._act = 1; b.addEventListener('click', A.printPage); }
      else if (/^Download\b/i.test(lab)) {
        b._act = 1;
        b.addEventListener('click', function () {
          if (tr) { var name = text(tr.cells[0]).split(' ')[0] + '-' + A.slug(lab.replace(/^Download\s*/i, '')); A.saveFile(name.toLowerCase() + '.pdf', A.makePdf(rowPdfLines(tr)), 'application/pdf'); A.toast('Downloaded ' + name.toLowerCase() + '.pdf', 'ok'); }
          else {
            var base = lab.replace(/^Download\s*/i, ''), ref = text(q('main h1')); var nm = (/^(Report|Invoice|Order Copy|Receipt|Statement|Terms|Specification|Dispatch Note|Packing List|Scheme Summary|Sale Invoice)$/i.test(base) ? ref + ' ' + base : base + ' ' + ref);
            A.downloadPdf(A.slug(nm));
          }
        });
      }
      else if (/^Send Payment Reminder$/.test(lab)) { b._act = 1; b.addEventListener('click', function () { A.toast('Payment reminder sent to ' + (text(q('main dd a, main dd')) || 'the customer'), 'ok'); }); }
      else if (/^Save Draft$/.test(lab)) { b._act = 1; b.addEventListener('click', function () { A.toast('Draft saved', 'ok'); }); }
      else if (/^Cancel$/.test(lab) && b.closest('.head')) { b._act = 1; b.addEventListener('click', back); }
      else if (/^(Save Settings)$/.test(lab)) { b._act = 1; b.addEventListener('click', function () { A.toast('Settings saved', 'ok'); }); }
    });
  };

  // ---------- Uploads ----------
  var wireUploads = function () {
    qa('main button').forEach(function (b) {
      if (wired(b)) return;
      var lab = text(b); if (!/^(Upload( Files| Photos)?|Attach Files|Replace)$/.test(lab)) return;
      b._act = 1;
      var inp = document.createElement('input'); inp.type = 'file'; inp.hidden = true; inp.multiple = lab !== 'Replace'; if (/Photos/.test(lab)) inp.accept = 'image/*';
      b.insertAdjacentElement('afterend', inp);
      b.addEventListener('click', function () { inp.click(); });
      inp.addEventListener('change', function () {
        var files = Array.prototype.slice.call(inp.files); if (!files.length) return;
        var host = b.closest('.drop') || b.closest('.row') || b.parentElement;
        if (lab === 'Replace') { var f = q('.file', b.closest('tr, .drop, .card') || host); if (f) f.lastChild.textContent = files[0].name; A.toast('Replaced with ' + files[0].name, 'ok'); inp.value = ''; return; }
        var box = q('.files', b.closest('.reply') || host) || host;
        files.forEach(function (fl) {
          var s = document.createElement('span'); s.className = 'file added'; s.innerHTML = A.icon('doc') + esc(fl.name);
          if (box === host) host.insertBefore(s, b); else box.appendChild(s);
        });
        A.toast(files.length === 1 ? 'Added ' + files[0].name : 'Added ' + files.length + ' files', 'ok'); inp.value = '';
      });
    });
  };

  // ---------- Conversations ----------
  var initials = function (n) { return n.split(' ').map(function (w) { return w[0]; }).join('').slice(0, 2); };
  var msgHtml = function (who, when, body, files) {
    return '<div class="msg me"><div class="av">' + esc(initials(who)) + '</div><div><div class="top-line"><b>' + esc(who) + '</b><time>' + esc(when) + '</time></div><div class="bubble">' + esc(body) +
      (files && files.length ? '<div class="files">' + files.map(function (f) { return '<span class=file>' + A.icon('doc') + esc(f) + '</span>'; }).join('') + '</div>' : '') + '</div></div></div>';
  };
  var setupThread = function () {
    var thread = q('main .thread'); if (!thread) return;
    var key = sid, saved = A.state.m[key] || [];
    saved.forEach(function (m) { thread.insertAdjacentHTML('beforeend', msgHtml(m[0], m[1], m[2], m[3])); });
    var ta = q('main .reply textarea'), send = qa('main .reply button').filter(function (b) { return /Send Reply/.test(text(b)); })[0]; if (!send) return;
    send._act = 1;
    send.addEventListener('click', function () {
      var f = ta.closest('.reply'); qa('.err', f).forEach(function (e) { e.remove(); });
      if (!ta.value.trim()) { var e = document.createElement('div'); e.className = 'err'; e.textContent = 'Write a reply first'; ta.insertAdjacentElement('afterend', e); ta.focus(); return; }
      var files = qa('.reply .file', f).map(text), when = today + ' ' + nowTime();
      thread.insertAdjacentHTML('beforeend', msgHtml(person, when, ta.value.trim(), files));
      (A.state.m[key] = A.state.m[key] || []).push([person, when, ta.value.trim(), files]); persist();
      qa('.reply .file', f).forEach(function (x) { x.remove(); }); ta.value = '';
      thread.lastElementChild.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); A.toast('Reply sent', 'ok');
    });
  };

  // ---------- Notifications ----------
  var nkey = pid + ':' + A.role;
  var readIds = function () { return A.state.n[nkey] || []; };
  var bell = function () {
    var dot = q('.top .icon-btn .dot'); if (!dot) return;
    var unread = Math.max(0, 3 - readIds().length);
    dot.textContent = unread; dot.hidden = unread === 0;
  };
  var setupNotifications = function () {
    var feed = qa('main .ntf li').filter(function (li) { return !li.closest('[hidden]'); });
    var idOf = function (li) { return text(li); };
    feed.forEach(function (li) {
      if (readIds().indexOf(idOf(li)) >= 0) li.classList.remove('unread');
      var a = q('a', li);
      if (a) a.addEventListener('click', function () { if (li.classList.contains('unread')) { A.state.n[nkey] = readIds().concat([idOf(li)]); persist(); } });
    });
    var all = qa('main .head button').filter(function (b) { return /Mark All as Read/.test(text(b)); })[0];
    if (all) { all._act = 1; all.addEventListener('click', function () {
      var ids = readIds(); feed.forEach(function (li) { if (li.classList.contains('unread')) { ids.push(idOf(li)); li.classList.remove('unread'); } });
      A.state.n[nkey] = ids.filter(function (x, i) { return ids.indexOf(x) === i; }); persist(); bell();
      A.lists.forEach(function (l) { l.apply(false); }); A.toast('All notifications marked as read', 'ok');
    }); }
    var cnt = function () { qa('[data-count]').forEach(function (e) { e.textContent = qa('main ' + e.getAttribute('data-count')).filter(function (x) { return !x.closest('[hidden]'); }).length; }); };
    A.lists.forEach(function (l) { l.el.addEventListener('listchange', cnt); }); cnt();
  };

  // ---------- Edit dialogs: values shown as key-value rows ----------
  var SKIP_EDIT = /^(status|credit used|credit limit|credit available|owes|invoice number|ticket number|order|return number|dispatch number|delivery number|account manager|relationship manager|customer code|last sign-in|added on|added by|retailer code|price tier)$/i;
  var editable = function (scope) {
    var rows = [];
    qa('dl.kv', scope).forEach(function (d) { qa('dt', d).forEach(function (dt) {
      var dd = dt.nextElementSibling; if (!dd || q('.chip, .meter, a', dd) || SKIP_EDIT.test(text(dt)) || /^(₹|—)/.test(text(dd)) && /balance|amount/i.test(text(dt))) return;
      rows.push({ dt: dt, dd: dd });
    }); });
    return rows.slice(0, 10);
  };
  var wireEdit = function () {
    qa('main button').forEach(function (b) {
      if (wired(b)) return;
      var lab = text(b); if (!/^(Edit( User| Profile| Customer| Scheme| Product)?)$/.test(lab)) return;
      var inCard = b.closest('.card'), inHead = b.closest('.head');
      b._act = 1;
      b.addEventListener('click', function () {
        var scope = inCard && !inHead ? inCard : q('main'), rows = editable(scope);
        if (!rows.length) { A.toast('Nothing to edit on this screen', 'warn'); return; }
        var roleOpts = null;
        var fields = rows.map(function (r) {
          var t = text(r.dt), f = { label: t, value: text(r.dd), required: !/note|reference|email|phone/i.test(t) };
          if (/^Role$/.test(t) && A.portal) { f.type = 'select'; f.options = A.portal.roles.map(function (x) { return x.label; }); if (f.options.indexOf(f.value) < 0) f.options.unshift(f.value); }
          return f;
        });
        A.formDialog({ title: lab.indexOf(' ') > 0 ? lab : 'Edit Details', ok: 'Save Changes', fields: fields, onOk: function (v) {
          var ed = A.state.e[sid] = A.state.e[sid] || {};
          rows.forEach(function (r) { var t = text(r.dt); if (v[t] !== undefined && v[t] !== text(r.dd)) { r.dd.textContent = v[t]; ed[t] = v[t]; } });
          var h1 = q('main h1'), name = v['Full Name'] || v['Customer Name']; if (h1 && name && h1.closest('.title-row')) { h1.textContent = name; ed.__title = name; }
          var tag = q('.title-row .tag'); if (tag && v.Role) tag.textContent = v.Role;
          persist(); A.toast('Changes saved', 'ok');
        } });
      });
    });
  };

  // ---------- Page-level actions that need a small form ----------
  var wireDialogs = function () {
    var by = function (re) { return qa('main button, main a.btn:not([href])').filter(function (b) { return !wired(b) && re.test(text(b)); }); };
    by(/^Reset Password$/).forEach(function (b) { b._act = 1; b.addEventListener('click', function () {
      var email = ''; qa('main dt').forEach(function (d) { if (/Email/.test(text(d))) email = text(d.nextElementSibling); });
      A.dialog({ title: 'Reset Password', body: '<p>A link to choose a new password will be sent to ' + esc(email || 'this user') + '.</p>', ok: 'Send Reset Link', onOk: function () { A.toast('Password reset link sent to ' + (email || 'the user'), 'ok'); } });
    }); });
    by(/^Deactivate User$/).forEach(function (b) { b._act = 1; b.addEventListener('click', function () {
      var on = /^Deactivate/.test(text(b));
      A.dialog({ title: on ? 'Deactivate User' : 'Reactivate User', body: '<p>' + esc(text(q('main h1'))) + (on ? ' will no longer be able to sign in.' : ' will be able to sign in again.') + '</p>', ok: on ? 'Deactivate User' : 'Reactivate User', danger: on, onOk: function () {
        var c = q('.title-row .chip'); A.state.x[sid + '|page'] = on ? 'Inactive' : 'Active'; if (c) A.applyChip(c, on ? 'Inactive' : 'Active');
        b.textContent = on ? 'Reactivate User' : 'Deactivate User'; b.classList.toggle('danger', !on); persist(); A.toast(text(q('main h1')) + (on ? ' deactivated' : ' reactivated'), 'ok');
      } });
    }); });
    by(/^Add Contact$/).forEach(function (b) { b._act = 1; b.addEventListener('click', function () {
      A.formDialog({ title: 'Add Contact', ok: 'Add Contact', fields: [{ label: 'Name' }, { label: 'Role', type: 'select', options: A.portal.roles.map(function (r) { return r.label; }).concat(['Accountant']).filter(function (x, i, a) { return a.indexOf(x) === i; }) }, { label: 'Email', required: true }, { label: 'Phone', required: false }], onOk: function (v) {
        var t = b.closest('.card').querySelector('table.tbl tbody'); if (!t) return;
        var tr = document.createElement('tr'); tr.className = 'row-new'; tr.innerHTML = '<td>' + esc(v.Name) + '</td><td>' + esc(v.Role) + '</td><td>' + esc(v.Email) + '</td><td>' + esc(v.Phone || '—') + '</td>'; t.appendChild(tr); A.toast(v.Name + ' added to contacts', 'ok');
      } });
    }); });
    by(/^Create Campaign$/).forEach(function (b) { b._act = 1; b.addEventListener('click', function () {
      A.formDialog({ title: 'Create Campaign', ok: 'Create Campaign', fields: [{ label: 'Campaign Name' }, { label: 'Audience', type: 'select', options: ['Dealers', 'Retailers', 'Distributors', 'Dealers and retailers'] }, { label: 'Budget in Rupees', type: 'number' }], onOk: function (v) {
        A.state.r[sid] = (A.state.r[sid] || []).concat([{ Campaign: v['Campaign Name'], 'Campaign Number': 'PRM-2026-' + String(7 + (A.state.r[sid] || []).length).padStart(2, '0'), Audience: v.Audience, 'Customers Reached': '0', 'Orders Influenced': '0', 'Spent Against Budget': '₹0 of ' + A.fmtM(+v['Budget in Rupees'].replace(/\D/g, '')), Status: 'Planned' }]);
        persist(); A.toast('Campaign ' + v['Campaign Name'] + ' created', 'ok'); setTimeout(function () { location.href = A.withState(location.href); }, 700);
      } });
    }); });
    by(/^Create Territory$/).forEach(function (b) { b._act = 1; b.addEventListener('click', function () {
      A.formDialog({ title: 'Create Territory', ok: 'Create Territory', fields: [{ label: 'Territory Name' }, { label: 'Account Manager', type: 'select', options: ['Vikram Chopra', 'Kavita Joshi', 'Neha Kulkarni'] }, { label: 'Sales Target in Rupees', type: 'number' }], onOk: function (v) {
        A.state.r[sid] = (A.state.r[sid] || []).concat([{ Territory: v['Territory Name'], Dealers: '0', Retailers: '0', 'Sales to Dealers': '₹0', Target: A.fmtM(+v['Sales Target in Rupees'].replace(/\D/g, '')), Achievement: '—', Status: 'Upcoming', 'Account Manager': v['Account Manager'] }]);
        persist(); A.toast('Territory ' + v['Territory Name'] + ' created', 'ok'); setTimeout(function () { location.href = A.withState(location.href); }, 700);
      } });
    }); });
    by(/^Reassign Manager$/).forEach(function (b) { b._act = 1; b.addEventListener('click', function () {
      var rows = qa('main table.tbl tbody tr').filter(function (r) { return r.cells.length > 7; }), names = rows.map(function (r) { return text(r.cells[0]); });
      A.formDialog({ title: 'Reassign Manager', ok: 'Reassign Manager', fields: [{ label: 'Territory', type: 'select', options: names }, { label: 'New Account Manager', type: 'select', options: ['Vikram Chopra', 'Kavita Joshi', 'Neha Kulkarni'] }], onOk: function (v) {
        var r = rows.filter(function (x) { return text(x.cells[0]) === v.Territory; })[0]; if (r) { r.cells[7].textContent = v['New Account Manager']; A.toast(v.Territory + ' is now managed by ' + v['New Account Manager'], 'ok'); }
      } });
    }); });
    by(/^Set Targets$/).forEach(function (b) { b._act = 1; b.addEventListener('click', function () {
      var rows = qa('main table.tbl tbody tr'), t = rows.filter(function (r) { return /^Q\d/.test(text(r.cells[0])); });
      A.formDialog({ title: 'Set Targets', ok: 'Save Targets', fields: [{ label: 'Quarter', type: 'select', options: t.map(function (r) { return text(r.cells[0]); }) }, { label: 'New Target in Rupees', type: 'number' }], onOk: function (v) {
        var r = t.filter(function (x) { return text(x.cells[0]) === v.Quarter; })[0], heads = qa('thead th', r.closest('table')).map(text), ti = heads.indexOf('Target');
        if (ti >= 0) r.cells[ti].textContent = A.fmtM(+v['New Target in Rupees'].replace(/\D/g, '')); A.toast('Target for ' + v.Quarter.split(' ')[0] + ' updated', 'ok');
      } });
    }); });
    by(/^Plan Dispatch$/).forEach(function (b) { b._act = 1; b.addEventListener('click', function () {
      A.formDialog({ title: 'Plan Dispatch', ok: 'Plan Dispatch', fields: [{ label: 'Dispatch Date', value: '28/10/2026' }, { label: 'Transporter', type: 'select', options: ['Western Freight Carriers', 'Konkan Roadlines'] }], onOk: function (v) {
        var e = A.parseDate(v['Dispatch Date']); if (e === null || e <= A.today) { A.toast('Choose a dispatch date after today', 'warn'); return false; }
        setStatusFor(b, 'Dispatch Planned'); A.toast('Dispatch planned for ' + v['Dispatch Date'] + ' with ' + v.Transporter, 'ok');
      } });
    }); });
    by(/^Update Delivery Status$/).forEach(function (b) { b._act = 1; b.addEventListener('click', function () {
      A.formDialog({ title: 'Update Delivery Status', ok: 'Update Status', fields: [{ label: 'Delivery Status', type: 'select', options: ['In Transit', 'Delivered', 'Delayed'], value: 'In Transit' }, { label: 'Note', type: 'textarea', required: false, full: true }], onOk: function (v) {
        setStatusFor(b, v['Delivery Status']); A.toast('Delivery status is now ' + v['Delivery Status'], 'ok');
      } });
    }); });
    by(/^Update Password$/).forEach(function (b) { b._act = 1; b.addEventListener('click', function () {
      var card = b.closest('.card'); clearErrors(card);
      var f = qa('.field', card), val = function (i) { return q('input', f[i]).value; };
      if (!val(0)) { markBad(f[0], 'Enter your current password'); return; }
      if (val(1).length < 8) { markBad(f[1], 'Use at least 8 characters'); return; }
      if (val(1) !== val(2)) { markBad(f[2], 'The new passwords do not match'); return; }
      qa('input', card).forEach(function (i) { i.value = ''; }); A.toast('Password updated', 'ok');
    }); });
    by(/^Save Changes$/).forEach(function (b) { b._act = 1; b.addEventListener('click', function () {
      var scope = q('main'); if (!A.validate(scope, { required: ['Full Name', 'Email Address'] })) { A.toast('Complete the highlighted fields', 'warn'); return; }
      A.toast('Changes saved', 'ok');
    }); });
    by(/^Raise Invoice Dispute$/).forEach(function (b) { b._act = 1; b.addEventListener('click', function () {
      A.formDialog({ title: 'Raise Invoice Dispute', ok: 'Raise Invoice Dispute', fields: [{ label: 'Invoice Number', value: 'INV-2026-03264' }, { label: 'Reason', type: 'select', options: ['Wrong Product Delivered', 'Quantity Shortfall', 'Tax Amount Mismatch', 'Price Mismatch', 'Damaged in Transit'] }, { label: 'Disputed Amount in Rupees', type: 'number' }, { label: 'What is wrong?', type: 'textarea', required: false, full: true }], onOk: function (v) {
        var amt = +v['Disputed Amount in Rupees'].replace(/\D/g, ''); if (!amt) { A.toast('Enter the disputed amount', 'warn'); return false; }
        var n = 15 + (A.state.r[sid] || []).length;
        (A.state.r[sid] = A.state.r[sid] || []).push({ 'Dispute Number': 'DIS-2026-' + String(n).padStart(4, '0'), 'Invoice Number': v['Invoice Number'], Raised: today, Reason: v.Reason, 'Disputed Amount': A.fmtM(amt), Status: 'Awaiting Your Reply', 'Company Response': '—' });
        A.state.t = { m: 'Dispute DIS-2026-' + String(n).padStart(4, '0') + ' raised for ' + v['Invoice Number'] }; persist(); location.href = A.withState(location.href);
      } });
    }); });
    by(/^Record Payment$/).forEach(function (b) { if (/BIL-08/.test(sid)) return; b._act = 1; b.addEventListener('click', function () { A.go2(sidOf('BIL-08')); }); });
  };

  // ---------- Form submit buttons ----------
  var wireSubmits = function () {
    var key = part;
    qa('main .head .acts button, main .head .acts a.btn:not([href])').forEach(function (b) {
      if (wired(b)) return;
      var lab = text(b);
      if (/^(Submit Ticket|Submit Return Request|Submit Request|Send Invitation|Create Product|Create Scheme)$/.test(lab) && COLL[key]) {
        b._act = 1; b.addEventListener('click', function (e) { e.preventDefault(); submitRecord(key); });
      }
    });
  };

  // ---------- Sale entry and payment entry ----------
  var parseQty = function (tr) { var i = q('.qty input', tr); return i ? parseInt(i.value, 10) || 0 : 0; };
  var setupSaleEntry = function () {
    var table = q('main table.tbl'); if (!table) return;
    var heads = qa('thead th', table).map(text), pc = heads.indexOf(heads.filter(function (h) { return /Price per Sheet/.test(h); })[0]), ac = heads.indexOf('Amount');
    var rows = qa('tbody tr', table), sumCard, creditCard, payCard, party = (window.CATALOG && window.CATALOG.parties || {})[pid] || {};
    qa('main section.card').forEach(function (s) { var h = text(q('header h2', s)); if (h === 'Sale Summary') sumCard = q('.body', s); if (/^(Dealer|Retailer) Credit$/.test(h)) creditCard = q('.body', s); if (h === 'Payment') payCard = q('.body', s); });
    var kv = function (root, label, html) { qa('dt', root).forEach(function (d) { if (text(d) === label) d.nextElementSibling.innerHTML = html; }); };
    var calc = function () {
      var sheets = 0, sub = 0;
      rows.forEach(function (tr) { var n = parseQty(tr), pr = A.parseMoney(text(tr.cells[pc])) || 0; sheets += n; sub += n * pr; if (ac >= 0) tr.cells[ac].innerHTML = n ? '<b>' + A.fmtM(n * pr) + '</b>' : '<b>—</b>'; });
      var gst = A.roundHE(sub * 0.09), total = sub + 2 * gst;
      if (sumCard) { kv(sumCard, 'Sheets', A.fmtN(sheets)); kv(sumCard, 'Subtotal', A.fmtM(sub)); kv(sumCard, 'Central GST 9%', A.fmtM(gst)); kv(sumCard, 'State GST 9%', A.fmtM(gst)); kv(sumCard, 'Total', A.fmtM(total)); }
      if (payCard) kv(payCard, 'Amount to Receive', '<b>' + A.fmtM(total) + '</b>');
      var sel = q('#dl, #rt'), pr = sel && party[sel.value], credit = null;
      if (creditCard && pr) {
        var used = Math.round((pr.owes + total) / pr.limit * 100), avail = pr.limit - pr.owes - total, m = q('.meter', creditCard);
        kv(creditCard, 'Credit Limit', A.fmtML(pr.limit)); kv(creditCard, 'Owes', A.fmtML(pr.owes)); kv(creditCard, 'This Sale', A.fmtM(total));
        kv(creditCard, 'Credit Available', avail < 0 ? '−' + A.fmtML(-avail) : A.fmtML(avail));
        qa('dt', creditCard).forEach(function (d) { if (text(d) === 'Credit Available') d.nextElementSibling.style.color = avail < 0 ? 'var(--bad)' : ''; });
        if (m) { m.className = 'meter ' + (avail < 0 ? 'bad' : used >= 80 ? 'bad' : used >= 50 ? 'warn' : 'ok'); q('i', m).style.width = Math.min(100, used) + '%'; }
        credit = { avail: avail, name: sel.value };
      }
      return { sheets: sheets, sub: sub, total: total, credit: credit };
    };
    rows.forEach(function (tr) { var box = q('.qty', tr); if (box) { A.wireQty(box); box.addEventListener('qtychange', calc); } });
    var mode = q('#pm'); if (mode && payCard) mode.addEventListener('change', function () { kv(payCard, 'Payment Mode', esc(mode.value)); });
    var psel = q('#dl, #rt'); if (psel) psel.addEventListener('change', calc);
    calc();
    var rec = qa('main .head .acts button').filter(function (b) { return /^Record Sale$/.test(text(b)); })[0];
    if (!rec) return; rec._act = 1;
    rec.addEventListener('click', function () {
      var scope = q('main'); if (!A.validate(scope, { required: qa('.field label', q('main section.card')).map(text).filter(function (l) { return /Name|Dealer|Retailer|Date/.test(l); }) })) { A.toast('Complete the highlighted fields', 'warn'); return; }
      var c = calc(); if (!c.sheets) { A.toast('Enter the sheets sold for at least one product', 'warn'); return; }
      if (c.credit && c.credit.avail < 0) { A.toast('This sale is ' + A.fmtML(-c.credit.avail) + ' above the credit available for ' + c.credit.name.split(',')[0], 'bad'); return; }
      var v = A.formValues(scope), list = sidOf(SALE_TARGET[pid][1]), n = numberFor('sale', list);
      var who = v.Dealer || v.Retailer || v['Customer Name'] || '', pay = v['Payment Mode'] || v.__radio || (v['Payment Terms'] ? 'Unpaid' : 'Paid');
      var r = { 'Sale Number': n, Date: v['Sale Date'] || today, Dealer: who, Retailer: who, Customer: who, Sheets: A.fmtN(c.sheets), Value: A.fmtM(c.total), Payment: /Immediate|Paid/.test(pay) && !v['Payment Terms'] ? 'Paid' : 'Unpaid', 'Payment Mode': pay, 'Dispatch Number': '—' };
      (A.state.r[list] = A.state.r[list] || []).push(r); A.state.t = { m: 'Sale ' + n + ' recorded for ' + who.split(',')[0] }; persist(); A.goList(list);
    });
  };
  var setupPaymentEntry = function () {
    var table = q('main table.tbl'); if (!table) return;
    var rows = qa('tbody tr', table), sum = qa('main section.card').filter(function (s) { return text(q('header h2', s)) === 'Payment Summary'; })[0], after = qa('main section.card').filter(function (s) { return text(q('header h2', s)) === 'Balance After Payment'; })[0];
    var kv = function (root, label, html) { qa('dt', root).forEach(function (d) { if (text(d) === label) d.nextElementSibling.innerHTML = html; }); };
    var base = after ? { out: A.parseMoney(text(qa('dd', after)[0])), over: A.parseMoney(text(qa('dd', after)[1])), avail: A.parseMoney(text(qa('dd', after)[2])) } : null;
    var amt = function (tr) { return A.parseMoney(q('td input.input', tr).value) || 0; };
    var calc = function () {
      var picked = rows.filter(function (tr) { return q('input[type=checkbox]', tr).checked; }), total = picked.reduce(function (n, tr) { return n + amt(tr); }, 0);
      if (sum) { kv(sum, 'Invoices Selected', String(picked.length)); kv(sum, 'Payment Total', A.fmtM(total)); var m = q('#pm'), d = q('#pd'); if (m) kv(sum, 'Mode', esc(m.value)); if (d) kv(sum, 'Payment Date', esc(d.value)); }
      if (after && base) {
        var overPaid = rows.reduce(function (n, tr) { return n + (q('input[type=checkbox]', tr).checked && /Overdue/.test(text(tr.cells[3])) ? Math.min(amt(tr), A.parseMoney(text(tr.cells[4])) || 0) : 0); }, 0);
        kv(after, 'Outstanding Balance', A.fmtML(base.out - total)); kv(after, 'Overdue', A.fmtM(Math.max(0, base.over - overPaid))); kv(after, 'Credit Available', A.fmtML(base.avail + total));
      }
      return { picked: picked, total: total };
    };
    rows.forEach(function (tr) {
      var cb = q('input[type=checkbox]', tr), inp = q('td input.input', tr), due = A.parseMoney(text(tr.cells[4])) || 0;
      cb.addEventListener('change', function () { if (cb.checked && !amt(tr)) inp.value = A.fmtM(due); if (!cb.checked) inp.value = ''; calc(); });
      inp.addEventListener('change', function () { var v = A.parseMoney(inp.value.indexOf('₹') < 0 ? '₹' + inp.value : inp.value) || 0; v = Math.min(v, due); inp.value = v ? A.fmtM(v) : ''; cb.checked = v > 0; calc(); });
    });
    ['pm', 'pd'].forEach(function (id) { var e = document.getElementById(id); if (e) e.addEventListener('change', calc); });
    calc();
    var rec = qa('main .head .acts button').filter(function (b) { return /^Record Payment$/.test(text(b)); })[0]; if (!rec) return; rec._act = 1;
    rec.addEventListener('click', function () {
      var c = calc(); if (!c.picked.length || !c.total) { A.toast('Select an invoice and enter the amount to pay', 'warn'); return; }
      var date = q('#pd') ? q('#pd').value : today, bad = A.parseDate(date) === null; if (bad) { markBad(q('#pd').closest('.field'), 'Enter the date as dd/mm/yyyy'); return; }
      var list = sidOf('BIL-03'), mode = q('#pm') ? q('#pm').value : 'Bank Transfer';
      c.picked.forEach(function (tr) {
        var no = text(tr.cells[1]).split(' ')[0], due = A.parseMoney(text(tr.cells[4])) || 0, st = amt(tr) >= due ? 'Paid' : 'Partly Paid';
        A.state.x[sidOf('BIL-01') + '|' + no] = st; A.state.x[sidOf('BIL-07') + '|' + no] = st;
        (A.state.r[list] = A.state.r[list] || []).push({ 'Payment Number': numberFor('payment', list), Date: date, Mode: mode, 'Invoice Number': no, Amount: A.fmtM(amt(tr)), Status: 'Confirmed' });
      });
      A.state.t = { m: 'Payment of ' + A.fmtM(c.total) + ' recorded' }; persist(); A.goList(list);
    });
  };

  // ---------- Tiles open what they count ----------
  var TSTOP = /\b(this|month|week|year|in|of|to|and|the|total|today|current|by|for|with|all|new|open|awaiting|pending|your|you|per|average|sheets?)\b/g;
  var tiles = function (str) { return str.toLowerCase().replace(/[^a-z ]+/g, ' ').replace(TSTOP, ' ').split(/\s+/).filter(Boolean).map(function (w) { return w.replace(/ies$/, 'y').replace(/([^s])s$/, '$1'); }); };
  // Tiles that the generic word match gets wrong: label -> screens that show it, in order of preference.
  var TILE_TO = [[/outstanding balance|^overdue|\bowes\b/i, ['Outstanding Balances', 'Invoices Overview']], [/purchases/i, ['Purchase History', 'Order History']], [/sales to (dealers|retailers)/i, ['Secondary Sales Overview', 'Tertiary Sales Overview']],
    [/sales to customers|^sales (today|this month)|sheets sold today/i, ['Retail Sales History']], [/stock on hand/i, ['Inventory Overview', 'My Inventory']], [/dispatch|in transit|shipment/i, ['Dispatch Management', 'Dispatch Overview']],
    [/suggested order|to reorder/i, ['Reorder Recommendations']], [/^orders this month|^order value this month/i, ['Order Management', 'Order History']], [/low stock|running low/i, ['Low Stock Overview']], [/incoming/i, ['Incoming Stock', 'Incoming Deliveries']]];
  var tileTarget = function (label) {
    for (var i = 0; i < TILE_TO.length; i++) if (TILE_TO[i][0].test(label)) {
      for (var j = 0; j < TILE_TO[i][1].length; j++) {
        var hit = P.forRole(A.portal, A.role).filter(function (x) { return x.built && x.name === TILE_TO[i][1][j] && x.id !== sid; })[0];
        if (hit) return hit;
      }
    }
    var lt = tiles(label); if (!lt.length) return null;
    var best = null;
    P.forRole(A.portal, A.role).forEach(function (x) {
      if (!x.built || x.kind !== 'm' || x.id === sid || /Dashboard|Profile|Notifications/.test(x.name)) return;
      var nt = tiles(x.name), dt = tiles(x.description || ''), no = nt.filter(function (w) { return lt.indexOf(w) >= 0; }).length, dd = dt.filter(function (w) { return lt.indexOf(w) >= 0; }).length;
      var score = 3 * no + dd; if (score < 2 || (!no && dd < 2)) return;
      var rank = score * 100 - nt.length * 10;
      if (!best || rank > best.rank) best = { screen: x, rank: rank };
    });
    return best && best.screen;
  };
  var setupTiles = function () {
    qa('main .kpi').forEach(function (k) {
      if (q('a[href], button', k) || k.hasAttribute('data-own')) return;
      var label = text(q('label', k)); if (!label) return;
      var chip = text(q('.chip, .delta', k)), full = label + ' ' + chip;
      k.setAttribute('role', 'link'); k.setAttribute('tabindex', '0'); k.setAttribute('aria-label', label + ': ' + text(q('strong', k)) + '. Open details'); k._act = 1;
      var go = function () {
        var hit = A.openTab && A.openTab(label);
        if (hit) { hit.card.scrollIntoView({ block: 'center', behavior: 'smooth' }); hit.card.classList.remove('flash'); void hit.card.offsetWidth; hit.card.classList.add('flash'); return; }
        var t = tileTarget(label) || tileTarget(full);
        if (t) { var u = new URL(A.link(t.id), location.href); u.searchParams.set('tab', label); location.href = u.toString(); return; }
        // nothing else counts this: bring the closest card on this screen into view
        var lt = tiles(full), card = qa('main section.card, main aside.card').map(function (c) { var h = tiles(text(q('header h2', c))), n = h.filter(function (w) { return lt.indexOf(w) >= 0; }).length; return { c: c, n: n }; }).sort(function (a, b) { return b.n - a.n; })[0];
        var target = card && card.c || q('main section.card');
        if (target) { target.scrollIntoView({ block: 'center', behavior: 'smooth' }); target.classList.remove('flash'); void target.offsetWidth; target.classList.add('flash'); var tt = text(q('header h2', target)); A.toast(tt ? 'Showing ' + tt + ' for ' + label : label + ': ' + text(q('strong', k)), 'ok'); }
      };
      k.addEventListener('click', go);
      k.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
    });
  };

  // ---------- Top-bar search: screens and products ----------
  var setupGlobalSearch = function () {
    var box = q('.top .search'), inp = box && q('input', box); if (!inp || !P.forRole) return;
    var C = window.CATALOG, screens = P.forRole(A.portal, A.role).filter(function (x) { return x.built && x.id !== sid; });
    var find = function (term) {
      var t = term.toLowerCase().trim(); if (t.length < 2) return [];
      var out = [];
      screens.forEach(function (x) { if ((x.name + ' ' + x.id + ' ' + (x.description || '')).toLowerCase().indexOf(t) >= 0) out.push({ label: x.name, value: x.id, hint: 'Screen', kind: 'screen' }); });
      if (C) C.products.forEach(function (p) { if ((p.name + ' ' + p.sku + ' ' + p.finish).toLowerCase().indexOf(t) >= 0) out.push({ label: p.name, value: p.sku, hint: p.sku, kind: 'product' }); });
      return out.slice(0, 9);
    };
    var go = function (it) {
      if (it.kind === 'screen') { A.go2(it.value); return; }
      var cat = pid === 'company' ? 'PRD-01' : 'CAT-01', u = new URL(A.link(sidOf(cat)), location.href); u.searchParams.set('q', it.value); location.href = u.toString();
    };
    var cur = [];
    inp.addEventListener('input', function () {
      cur = find(inp.value); A.closeMenu();
      if (cur.length) A.menu(box, cur, { noFocus: true, onPick: go });
      else if (inp.value.trim().length >= 2) A.menu(box, [{ label: 'No screens or products match', value: null, disabled: true }], { noFocus: true });
    });
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); var r = find(inp.value); if (r.length) go(r[0]); else A.toast('No screens or products match “' + inp.value.trim() + '”', 'warn'); }
      else if (e.key === 'Escape') { A.closeMenu(); inp.blur(); }
      else if (e.key === 'ArrowDown') { var o = q('.pop .opt'); if (o) { e.preventDefault(); o.focus(); } }
    });
  };

  // ---------- Radio groups: the selected option looks selected ----------
  var syncRadios = function () {
    qa('main label.radio input[type=radio]').forEach(function (r) {
      var paint = function () { qa('input[type=radio][name="' + r.name + '"]', r.form || document).forEach(function (x) { x.closest('label').classList.toggle('on', x.checked); }); };
      r.addEventListener('change', paint); if (r.checked) paint();
    });
  };

  // ---------- Documents: preview ----------
  var wireDocuments = function () {
    qa('main .drop button, main .files button').forEach(function (b) {
      if (wired(b) || !/^View$/.test(text(b))) return;
      b._act = 1;
      b.addEventListener('click', function () {
        var d = b.closest('.drop'), name = text(q('.file', d)) || 'document.pdf', title = text(q('b', d)) || name;
        A.dialog({ title: title, ok: 'Download', cancel: 'Close', body: '<div class="docview"><div class="page"><b>' + esc(title) + '</b><span>' + esc(name) + '</span><i></i><i></i><i></i><i class="s"></i></div><p>Sample document</p></div>', onOk: function () {
          A.saveFile(name.replace(/\.pdf$/, '') + '.pdf', A.makePdf([{ t: 'Laminates Customer Portal', size: 9 }, { t: title, b: true, size: 16, gap: 4 }, { t: 'Sample document: ' + name, size: 10 }]), 'application/pdf'); A.toast('Downloaded ' + name, 'ok');
        } });
      });
    });
  };

  // ---------- Hierarchy tree ----------
  var wireTree = function () { qa('main details.node > summary').forEach(function (s) { s._act = 1; }); };

  // ---------- Sign-in screens (no app chrome) ----------
  var setupAuth = function () {
    var form = q('form'); if (!form) return;
    var email = q('input[type=email]'), pw = q('input[type=password]');
    var go = q('a[data-signin]'), send = qa('a.btn, button.btn').filter(function (b) { return /Send Reset Link/.test(text(b)); })[0];
    if (go) go.addEventListener('click', function (e) {
      qa('.err', form).forEach(function (x) { x.remove(); });
      var bad = function (inp, m) { e.preventDefault(); var er = document.createElement('div'); er.className = 'err'; er.textContent = m; inp.closest('.field').appendChild(er); inp.focus(); };
      if (!email.value.trim() || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value.trim())) return bad(email, 'Enter a valid email address');
      if (!pw.value) return bad(pw, 'Enter your password');
    });
    if (send) send.addEventListener('click', function (e) {
      qa('.err', form).forEach(function (x) { x.remove(); });
      if (!email.value.trim() || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value.trim())) { e.preventDefault(); var er = document.createElement('div'); er.className = 'err'; er.textContent = 'Enter a valid email address'; email.closest('.field').appendChild(er); email.focus(); }
    });
    form.addEventListener('submit', function (e) { e.preventDefault(); if (go) go.click(); else if (send) send.click(); });
  };

  // ---------- Row-level View and similar ----------
  var wireRowButtons = function () {
    qa('main tbody tr button, main tbody tr a.btn:not([href])').forEach(function (b) {
      if (wired(b)) return;
      var lab = text(b) || b.getAttribute('aria-label') || '';
      if (/^(View|Review)$/.test(lab)) {
        b._act = 1;
        b.addEventListener('click', function () {
          var tr = rowOf(b), heads = qa('thead th', tr.closest('table')).map(text);
          var rows = qa('td', tr).map(function (c, i) { return heads[i] && text(c) ? [heads[i], text(c)] : null; }).filter(Boolean);
          A.dialog({ title: text(tr.cells[0]).split(' ')[0], body: '<dl class="kv">' + rows.map(function (r) { return '<dt>' + esc(r[0]) + '</dt><dd>' + esc(r[1]) + '</dd>'; }).join('') + '</dl>', ok: 'Close', cancel: false });
        });
      }
    });
  };
  var wireRemoveRows = function () {
    qa('main tbody tr .icon-btn').forEach(function (b) {
      if (wired(b) || !/trash|remove|delete/i.test((b.getAttribute('aria-label') || '') + (q('svg', b) ? '' : ''))) return;
      b._act = 1;
      b.addEventListener('click', function () { var tr = rowOf(b), k = A.rowKey(tr); tr.classList.add('row-gone'); A.dismiss(k); A.lists.forEach(function (l) { l.apply(false); }); A.toast('Removed ' + text(tr.cells[0]).split(' ')[0], 'warn', { label: 'Undo', fn: function () { tr.classList.remove('row-gone'); A.state.d = A.state.d.filter(function (x) { return x !== k; }); persist(); A.lists.forEach(function (l) { l.apply(false); }); } }); });
    });
  };

  // ---------- Reorder settings "Edit" (Inventory Item Details) ----------
  // handled by wireEdit (the key-value rows of its card)

  // ---------- Start ----------
  A.onReady(10, function () { if (!A.screen) return; A.hydrate(); addRows(); });
  A.onReady(25, function () {
    if (!q('main')) { setupAuth(); return; }
    setupTiles(); setupGlobalSearch(); syncRadios(); wireDocuments(); wireUploads(); setupThread(); setupNotifications(); wireStatusActions(); wireFiles(); wireEdit(); wireDialogs(); wireSubmits(); wireRowButtons(); wireRemoveRows(); wireTree();
    if (/^(SAL-02|TSL-02|RTS-01)$/.test(part)) setupSaleEntry();
    if (/^BIL-08$/.test(part) && pid === 'primary') setupPaymentEntry();
    bell();
    if (A.state.t) { var t = A.state.t; delete A.state.t; persist(); setTimeout(function () { A.toast(t.m, 'ok'); }, 150); }
  });
  if (!document.querySelector('main')) A.onReady(25, setupAuth);
})();
