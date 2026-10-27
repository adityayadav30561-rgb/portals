/*
 * Behaviour layer, part 5: files. "Export …" writes a CSV of the rows currently listed (after search, tabs, filters and sorting);
 * "Download …" writes a PDF of the screen (a small PDF writer, no library); "Print …" opens the print dialog.
 * Nothing leaves the browser: the files are built from what is on the screen.
 */
(function () {
  var A = window.APP, q = A.q, qa = A.qa;
  var text = function (el) { return el ? el.textContent.replace(/\s+/g, ' ').trim() : ''; };

  A.saveFile = function (name, data, mime) {
    var blob = new Blob([data], { type: mime });
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; a.style.display = 'none';
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
  };
  var fileBase = function () { var h = q('main h1'); return ((h && text(h)) || document.title.split(' (')[0] || 'screen').replace(/[^\w]+/g, '-').replace(/^-|-$/g, '').toLowerCase(); };

  // ---------- CSV ----------
  var cellText = function (c) {
    var inp = q('input:not([type=checkbox]):not([type=radio])', c); if (inp) return inp.value;
    var chips = qa('.chip', c); if (chips.length && text(c) === chips.map(text).join(' ')) return chips.map(text).join(' ');
    return text(c);
  };
  A.tableToCsv = function (table) {
    var heads = qa('thead th', table), keep = heads.map(function (h, i) { return text(h) && !q('input', h) ? i : -1; }).filter(function (i) { return i >= 0; });
    var rows = qa('tbody tr', table).filter(function (r) { return !r.hidden && !r.classList.contains('empty-row') && r.cells.length >= keep.length; });
    var esc = function (v) { v = String(v).replace(/\s+/g, ' ').trim(); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    var out = [keep.map(function (i) { return esc(text(heads[i])); }).join(',')];
    rows.forEach(function (r) { out.push(keep.map(function (i) { return esc(cellText(r.cells[i])); }).join(',')); });
    return { csv: '﻿' + out.join('\r\n') + '\r\n', rows: rows.length };
  };
  A.exportCsv = function () {
    var lists = A.lists.filter(function (l) { return l.kind === 'table'; });
    var t = (lists.sort(function (a, b) { return b.items.length - a.items.length; })[0] || {}).el || qa('main table.tbl').sort(function (a, b) { return b.rows.length - a.rows.length; })[0];
    if (!t) { A.toast('There is no table on this screen to export', 'warn'); return; }
    var r = A.tableToCsv(t);
    A.saveFile(fileBase() + '.csv', r.csv, 'text/csv;charset=utf-8');
    A.toast('Exported ' + r.rows + ' ' + (r.rows === 1 ? 'row' : 'rows') + ' to ' + fileBase() + '.csv', 'ok');
  };

  // ---------- PDF ----------
  var latin = function (s) {
    return String(s).replace(/₹/g, 'Rs. ').replace(/[−–—]/g, '-').replace(/[•●·]/g, '-').replace(/…/g, '...').replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/[^\x20-\x7e]/g, '?');
  };
  var wrap = function (s, n) {
    var out = [], line = '';
    String(s).split(' ').forEach(function (w) { if ((line + ' ' + w).trim().length > n) { out.push(line); line = w; } else line = (line + ' ' + w).trim(); });
    if (line) out.push(line);
    return out.length ? out : [''];
  };
  // lines: [{ t: 'text', b: bold, size: 10, gap: 0 }]
  A.makePdf = function (lines) {
    var pages = [[]], y = 800, W = 595, H = 842;
    lines.forEach(function (l) {
      var size = l.size || 10, lead = size + 5 + (l.gap || 0);
      if (y - lead < 50) { pages.push([]); y = 800; }
      y -= lead;
      wrap(latin(l.t), Math.floor(100 * 10 / size)).forEach(function (part, k) {
        if (k) { y -= size + 3; if (y < 50) { pages.push([]); y = 800; } }
        pages[pages.length - 1].push('BT /' + (l.b ? 'F2' : 'F1') + ' ' + size + ' Tf 50 ' + y + ' Td (' + part.replace(/([\\()])/g, '\\$1') + ') Tj ET');
      });
    });
    var objs = [];
    var add = function (s) { objs.push(s); return objs.length; };
    add('<< /Type /Catalog /Pages 2 0 R >>');
    add('PAGES');
    add('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>');
    add('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>');
    var kids = [];
    pages.forEach(function (p) {
      var stream = p.join('\n'), c = add('<< /Length ' + stream.length + ' >>\nstream\n' + stream + '\nendstream');
      kids.push(add('<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ' + W + ' ' + H + '] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents ' + c + ' 0 R >>') + ' 0 R');
    });
    objs[1] = '<< /Type /Pages /Kids [' + kids.join(' ') + '] /Count ' + kids.length + ' >>';
    var out = '%PDF-1.4\n', offs = [];
    objs.forEach(function (o, i) { offs.push(out.length); out += (i + 1) + ' 0 obj\n' + o + '\nendobj\n'; });
    var xref = out.length;
    out += 'xref\n0 ' + (objs.length + 1) + '\n0000000000 65535 f \n' + offs.map(function (o) { return ('0000000000' + o).slice(-10) + ' 00000 n \n'; }).join('') +
      'trailer\n<< /Size ' + (objs.length + 1) + ' /Root 1 0 R >>\nstartxref\n' + xref + '\n%%EOF';
    return out;
  };
  // The content of the screen as lines of text: title, tiles, key-value lists, tables.
  A.pageLines = function () {
    var L = [], main = q('main'), h1 = q('h1', main);
    L.push({ t: 'Laminates Customer Portal', size: 9 });
    L.push({ t: (h1 ? text(h1) : fileBase()), b: true, size: 18, gap: 4 });
    L.push({ t: (A.portal ? A.portal.org + ' - ' + A.portal.portalName : '') + ' - 26 October 2026', size: 9, gap: 8 });
    var st = qa('.title-row .chip', main).map(text); if (st.length) L.push({ t: 'Status: ' + st.join(', '), size: 10 });
    var tiles = qa('.kpi', main).filter(function (k) { return !k.closest('[hidden]'); });
    if (tiles.length) { L.push({ t: 'Summary', b: true, size: 12, gap: 8 }); tiles.forEach(function (k) { L.push({ t: text(q('label', k)) + ': ' + text(q('strong', k)), size: 10 }); }); }
    qa('section.card, aside.card', main).forEach(function (s) {
      if (s.hidden || s.closest('[hidden]') || q('.chart', s) && !q('table, dl', s)) return;
      var h = text(q('header h2', s)); if (h) L.push({ t: h, b: true, size: 12, gap: 8 });
      qa('dl.kv, table.tbl', s).forEach(function (el) {
        if (el.matches('dl')) { qa('dt', el).forEach(function (dt) { L.push({ t: text(dt) + ': ' + text(dt.nextElementSibling), size: 10 }); }); return; }
        var heads = qa('thead th', el).map(text);
        L.push({ t: heads.filter(Boolean).join(' | '), b: true, size: 9 });
        qa('tbody tr', el).filter(function (r) { return !r.hidden && !r.classList.contains('empty-row'); }).forEach(function (r) {
          L.push({ t: qa('td', r).map(cellText).filter(function (x) { return x; }).join(' | '), size: 9 });
        });
        qa('tfoot tr', el).forEach(function (r) { L.push({ t: qa('td', r).map(text).filter(Boolean).join(' | '), b: true, size: 9 }); });
      });
    });
    return L;
  };
  A.downloadPdf = function (name) {
    var base = (name || fileBase()).replace(/[^\w.-]+/g, '-').toLowerCase();
    A.saveFile(base + '.pdf', A.makePdf(A.pageLines()), 'application/pdf');
    A.toast('Downloaded ' + base + '.pdf', 'ok');
  };
  A.printPage = function () { window.print(); };
})();
