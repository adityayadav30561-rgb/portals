/*
 * Review bar for every screen. Reads assets/registry.js (load it first). Classic script: no imports, no fetch.
 *   <body data-screen="PRI-ORD-02">  <script src="../../assets/registry.js"></script>  <script src="../../assets/shell.js"></script>
 * The role comes from ?role=MGR, otherwise the screen's first role. ?review=off hides the bar for clean screenshots.
 */
(function () {
  var P = window.PORTAL;
  var me = document.currentScript;
  var root = new URL('../', me.src).href;          // folder that holds index.html
  P.root = root;

  var ICON = {
    back: '<path d="M10 3 5 8l5 5"/>',
    next: '<path d="m6 3 5 5-5 5"/>'
  };
  var svg = function (n) { return '<svg viewBox="0 0 16 16" aria-hidden="true">' + ICON[n] + '</svg>'; };
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  var id = document.body.getAttribute('data-screen');
  if (!id) return;
  var found = null;
  P.portals.forEach(function (p) { p.screens.forEach(function (s) { if (s.id === id) found = { p: p, s: s }; }); });
  if (!found) { console.error('shell.js: unknown screen ' + id); return; }
  var p = found.p, s = found.s;

  var params = new URLSearchParams(location.search);
  var role = params.get('role');
  if (s.roles.indexOf(role) < 0) role = s.roles[0];
  var off = params.get('review') === 'off';
  var keep = off ? '?review=off' : '';

  P.current = { portal: p, screen: s, role: role };
  document.title = P.fullName(p, s, role) + ' (' + s.id + ')';

  // Links between screens, resolved from the registry so no page hard-codes a file name:
  //   data-link="PRI-ORD-02"  that screen (in the same portal as this page when the ID has no prefix, see P.find)
  //   data-signin="primary"   the portal's first role dashboard once built, otherwise the portal's directory
  //   data-directory="index"  the Screen Directory
  var keepQuery = off ? '?review=off' : '';
  var withKeep = function (h) { return h + (off ? (h.indexOf('?') >= 0 ? '&review=off' : keepQuery) : ''); };
  Array.prototype.forEach.call(document.querySelectorAll('[data-link]'), function (a) {
    var t = P.find(a.getAttribute('data-link'));
    if (t) a.setAttribute('href', withKeep(P.href(root, t.screen, t.screen.roles.indexOf(role) >= 0 ? role : t.screen.roles[0])));
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-signin]'), function (a) {
    var tp = P.portal(a.getAttribute('data-signin'));
    var d = P.dashboard(tp, tp.roles[0].code);
    a.setAttribute('href', withKeep(d && d.built ? P.href(root, d, tp.roles[0].code) : root + 'directory/' + tp.id + '.html'));
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-directory]'), function (a) {
    var k = a.getAttribute('data-directory');
    a.setAttribute('href', withKeep(root + (k === 'index' ? 'index.html' : 'directory/' + k + '.html')));
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-toggle-password]'), function (b) {
    b.addEventListener('click', function () {
      var i = document.getElementById(b.getAttribute('data-toggle-password'));
      i.type = i.type === 'password' ? 'text' : 'password';
    });
  });
  if (off) return;

  // Previous and next built screen for this role, in the order of the directory.
  var list = P.forRole(p, role).filter(function (x) { return x.built; });
  var at = list.indexOf(s);
  var link = function (x) {
    var h = P.href(root, x, role);
    return h + (keep ? (h.indexOf('?') >= 0 ? '&review=off' : keep) : '');
  };
  var prev = at > 0 ? list[at - 1] : null;
  var next = at >= 0 && at < list.length - 1 ? list[at + 1] : null;

  var bar = document.createElement('div');
  bar.className = 'review';
  bar.innerHTML =
    '<a class="back" href="' + root + 'directory/' + p.id + '.html#role-' + role + '">' + svg('back') + 'Screen Directory</a>' +
    '<div class="title"><span class="id">' + esc(s.id) + '</span><span>' + esc(P.fullName(p, s, role)) + '</span></div>' +
    '<nav class="pager" aria-label="Screens in this role">' +
    (prev ? '<a href="' + link(prev) + '" title="' + esc(prev.name) + '">' + svg('back') + 'Previous</a>' : '<span>' + svg('back') + 'Previous</span>') +
    (next ? '<a href="' + link(next) + '" title="' + esc(next.name) + '">Next' + svg('next') + '</a>' : '<span>Next' + svg('next') + '</span>') +
    '</nav>';
  document.body.insertBefore(bar, document.body.firstChild);
})();
