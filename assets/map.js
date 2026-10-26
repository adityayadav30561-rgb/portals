/*
 * Screen Map: a tree from the sign-in screens through the portals and their roles to every screen, built from assets/registry.js
 * (load it first). Classic script: no imports, no fetch, so the page opens straight from disk.
 *   Sign In -> Portal Selection -> the four login screens -> portal -> role -> menu section -> screen -> the screens opened from it
 * A built screen is a link; a planned screen is greyed out. Section and screen nodes open and close; search and "Built only" prune the tree.
 */
(function () {
  var P = window.PORTAL;
  var root = new URL('../', document.currentScript.src).href;
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var $ = function (sel, el) { return (el || document).querySelector(sel); };
  var appPortals = P.portals.filter(function (p) { return p.id !== 'authentication'; });
  var auth = P.portal('authentication');
  var authScreen = function (code) { return auth.screens.filter(function (s) { return s.code === code; })[0]; };

  // ---------- Build the tree ----------
  var uid = 0;
  var node = function (kind, title, extra) {
    var n = { key: 'n' + (uid++), kind: kind, title: title, kids: [] };
    for (var k in extra) n[k] = extra[k];
    return n;
  };
  var screenNode = function (p, s, role, kind) {
    return node(kind || 'screen', s.name, { id: s.id, built: s.built, href: s.built ? P.href(root, s, role) : null, description: s.description, screen: s });
  };

  // The screens of one role: each screen hangs under the screen it is opened from, the rest under their menu section.
  var roleNodes = function (p, role) {
    var list = P.forRole(p, role.code), byCode = {}, made = {};
    list.forEach(function (s) { byCode[s.code] = s; });
    var make = function (s) { if (!made[s.id]) made[s.id] = screenNode(p, s, role.code); return made[s.id]; };
    var groups = [], gnode = {};
    list.forEach(function (s) {
      var par = P.parent(p, s, role.code);
      if (par && byCode[par.code] && par.code !== s.code) return;
      var g = P.group(s, role.code);
      if (!gnode[g]) { gnode[g] = node('group', g, {}); groups.push(gnode[g]); }
      gnode[g].kids.push(make(s));
    });
    list.forEach(function (s) {
      var par = P.parent(p, s, role.code);
      if (par && byCode[par.code] && par.code !== s.code) make(byCode[par.code]).kids.push(make(s));
    });
    return groups;
  };

  var tree = node('start', 'Sign In', {});
  var selection = screenNode(auth, authScreen('01'), 'ALL', 'sg');
  tree.kids.push(selection);
  appPortals.forEach(function (p, i) {
    var login = screenNode(auth, authScreen('0' + (i + 2)), 'ALL', 'sg');
    var pn = node('portal', p.card, { sub: p.org, portalId: p.id, directory: root + 'directory/' + p.id + '.html', portal: p });
    p.roles.forEach(function (role) {
      var rn = node('role', role.label, { sub: role.person, roleCode: role.code, portal: p });
      rn.kids = roleNodes(p, role);
      pn.kids.push(rn);
    });
    login.kids.push(pn);
    selection.kids.push(login);
  });
  var forgot = screenNode(auth, authScreen('06'), 'ALL', 'sg');
  forgot.kids.push(screenNode(auth, authScreen('07'), 'ALL', 'sg'));
  tree.kids.push(forgot);
  var errors = node('group', 'Error Screens', {});
  errors.kids.push(screenNode(auth, authScreen('08'), 'ALL', 'sg'), screenNode(auth, authScreen('09'), 'ALL', 'sg'));
  tree.kids.push(errors);

  // Counts of built and total screens below every node; a screen that appears more than once below a node (shared by roles) counts once.
  var count = function (n) {
    var ids = {};
    if (n.id) ids[n.id] = n.built;
    n.kids.forEach(function (k) { var c = count(k); for (var id in c.ids) ids[id] = c.ids[id]; });
    n.ids = ids; n.t = 0; n.b = 0;
    for (var id in ids) { n.t++; if (ids[id]) n.b++; }
    return n;
  };
  count(tree);

  // ---------- State and drawing ----------
  var open = {}, onlyBuilt = false, query = '';
  var defaultOpen = function (n) { return n.kind === 'start' || n.kind === 'sg' || n.kind === 'portal'; };
  var matches = function (n) {
    return !query || (n.id + ' ' + n.title + ' ' + (n.description || '')).toLowerCase().indexOf(query) >= 0;
  };
  // A screen node is kept when it matches; any other node is kept when something below it is.
  var keep = function (n) {
    if (!query && !onlyBuilt) return true;
    var self = n.id ? ((!onlyBuilt || n.built) && matches(n)) : false;
    var kidsKept = n.kids.filter(keep).length > 0;
    n.keepSelf = self;
    return self || kidsKept || (n.kind === 'start');
  };
  var isOpen = function (n) {
    if (query || onlyBuilt) return n.kids.length > 0;
    return open[n.key] !== undefined ? open[n.key] : defaultOpen(n);
  };
  var badge = function (n) {
    if (!n.t || n.kind === 'start' || n.kind === 'sg' || n.kind === 'screen') return '';
    var cls = n.b === n.t ? 'ok' : n.b === 0 ? 'plain' : 'warn';
    return '<span class="chip ' + cls + ' plain cnt" title="' + n.b + ' of ' + n.t + ' screens built">' + n.b + ' of ' + n.t + '</span>';
  };
  var toggle = function (n, kids, isO) {
    if (!kids.length) return '';
    return '<button type="button" class="tg" data-k="' + n.key + '" aria-expanded="' + isO + '" aria-label="' + (isO ? 'Collapse ' : 'Expand ') + esc(n.title) + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg></button>';
  };
  var body = function (n) {
    if (n.id) {
      var inner = '<span class="sid">' + esc(n.id) + '</span><b>' + esc(n.title) + '</b>' + (n.built ? '' : '<span class="plan">Planned</span>');
      return n.built ? '<a class="lbl" href="' + n.href + '">' + inner + '</a>' : '<span class="lbl" title="Not built yet">' + inner + '</span>';
    }
    var sub = n.sub ? '<span class="sub">' + esc(n.sub) + '</span>' : '';
    var dir = n.directory ? '<a class="dirlink" href="' + n.directory + '">Screen directory</a>' : '';
    return '<span class="lbl"><b>' + esc(n.title) + '</b>' + sub + dir + '</span>';
  };
  var draw = function (n) {
    var kids = n.kids.filter(keep);
    var o = isOpen(n);
    var cls = 'n ' + n.kind + (n.id ? (n.built ? ' built' : ' planned') : '');
    var h = '<li class="' + cls + '"><div class="nd">' + body(n) + badge(n) + toggle(n, kids, o) + '</div>';
    if (kids.length && o) h += '<ul class="kids">' + kids.map(draw).join('') + '</ul>';
    return h + '</li>';
  };

  var total = P.count(), built = P.built();
  var portalCards = appPortals.map(function (p) {
    var b = p.screens.filter(function (s) { return s.built; }).length, t = p.screens.length, pct = Math.round(b / t * 100);
    return '<div class="stat"><span>' + esc(p.card) + '</span><b>' + b + ' of ' + t + '</b><span class="meter"><i style="width:' + pct + '%"></i></span></div>';
  }).join('');
  var ab = auth.screens.filter(function (s) { return s.built; }).length;
  var app = $('#app');
  app.innerHTML =
    '<header class="topbar"><div class="in"><a href="' + root + 'index.html" aria-label="Laminates Customer Portal — Screen Directory"><img class="logo" src="' + root + 'assets/brand/logo-480.webp" srcset="' +
    root + 'assets/brand/logo-480.webp 480w, ' + root + 'assets/brand/logo-960.webp 960w" sizes="10rem" width="150" height="28" alt="MAVRO.AI"></a>' +
    '<a class="btn sm" style="margin-left:auto" href="' + root + 'index.html">Screen directory</a></div></header>' +
    '<main class="map-page"><div class="dir-head"><div><h1>Laminates Customer Portal — Screen Map</h1>' +
    '<div class="facts"><span class="chip blue plain">' + total + ' screens</span><span class="chip plain">4 portals</span><span class="chip ok">' + built + ' of ' + total + ' screens built</span></div></div></div>' +
    '<div class="stats-row">' + portalCards + '<div class="stat"><span>Shared Sign-In Screens</span><b>' + ab + ' of ' + auth.screens.length + '</b><span class="meter"><i style="width:' + Math.round(ab / auth.screens.length * 100) + '%"></i></span></div></div>' +
    '<div class="tools"><input class="input" id="q" type="search" placeholder="Search by ID or name" aria-label="Search screens">' +
    '<div class="seg" role="group" aria-label="Filter"><button type="button" aria-pressed="true" data-f="all">All screens</button><button type="button" aria-pressed="false" data-f="built">Built only</button></div>' +
    '<div class="seg" role="group" aria-label="Detail level" id="lvl"><button type="button" aria-pressed="true" data-l="0">Roles</button><button type="button" aria-pressed="false" data-l="1">Sections</button><button type="button" aria-pressed="false" data-l="2">Screens</button></div>' +
    '<span class="legend"><span class="key built">Built</span><span class="key planned">Planned</span></span></div>' +
    '<div class="map" id="map" tabindex="0" aria-label="Screen map"></div></main>';
  document.title = 'Laminates Customer Portal — Screen Map';

  var render = function () {
    var x = $('#map'), sl = x.scrollLeft;
    var html = keep(tree) ? '<ul class="tr">' + draw(tree) + '</ul>' : '';
    x.innerHTML = html || '<div class="card empty">No screens match.</div>';
    x.scrollLeft = sl;
  };
  var all = function (n, fn) { fn(n); n.kids.forEach(function (k) { all(k, fn); }); };

  $('#map').addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('.tg') : null;
    if (!b) return;
    var k = b.getAttribute('data-k'), cur = b.getAttribute('aria-expanded') === 'true';
    open[k] = !cur;
    render();
    var again = document.querySelector('.tg[data-k="' + k + '"]'); if (again) again.focus({ preventScroll: true });
  });
  $('#q').addEventListener('input', function (e) { query = e.target.value.trim().toLowerCase(); render(); });
  Array.prototype.forEach.call(document.querySelectorAll('.seg button'), function (b) {
    b.addEventListener('click', function () {
      onlyBuilt = b.getAttribute('data-f') === 'built';
      Array.prototype.forEach.call(document.querySelectorAll('.seg button'), function (y) { y.setAttribute('aria-pressed', String(y === b)); });
      render();
    });
  });
  // Detail level: 0 shows portals and roles, 1 also the menu sections, 2 every screen.
  var setLevel = function (l) {
    open = {};
    all(tree, function (n) {
      if (n.kind === 'role') open[n.key] = l >= 1;
      else if (n.kind === 'group' || n.kind === 'screen') open[n.key] = l >= 2;
    });
    Array.prototype.forEach.call(document.querySelectorAll('#lvl button'), function (y) { y.setAttribute('aria-pressed', String(+y.getAttribute('data-l') === l)); });
    render();
  };
  Array.prototype.forEach.call(document.querySelectorAll('#lvl button'), function (b) {
    b.addEventListener('click', function () { setLevel(+b.getAttribute('data-l')); });
  });
  render();
})();
