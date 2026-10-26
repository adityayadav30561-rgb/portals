/*
 * Charts drawn from data attributes, so screens stay static HTML and open from disk. Classic script, no libraries.
 *
 *   <div class="chart" data-type="bars" data-labels='["May","June"]' data-money="true" data-height="260"
 *        data-series='[{"name":"Purchases","values":[1,2],"color":"var(--accent)"}]'></div>
 *   data-type: bars (grouped columns), line (add data-area="true" to fill under the first series), donut.
 *   Donut: data-series is [{"name":"Matte","value":2910,"color":"#..."}], data-center="7,415" data-caption="sheets".
 * Month names are written in full by the page; labels that do not fit are turned, never shortened.
 */
(function () {
  var NS = 'http://www.w3.org/2000/svg';
  var el = function (name, attrs, text) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (text != null) n.textContent = text;
    return n;
  };
  var fmt = function (n) { return Number(n).toLocaleString('en-IN'); };
  var nice = function (max) {
    var exp = Math.pow(10, Math.floor(Math.log10(max || 1))), f = max / exp;
    return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * exp;
  };

  function axes(box, svg, W, H, labels, series, money) {
    var all = [];
    series.forEach(function (s) { s.values.forEach(function (v) { all.push(v); }); });
    var top = nice(Math.max.apply(null, all)), ticks = 4;
    var leftPad = (money ? 2 : 0) + fmt(top).length * 6.4 + 14;
    var maxLabel = Math.max.apply(null, labels.map(function (l) { return l.length; }));
    var plotW = W - leftPad - 8;
    var slot = plotW / labels.length;
    var rotate = slot < maxLabel * 6.4 + 6;
    var bottom = rotate ? 18 + maxLabel * 4.6 : 26;
    var plotH = H - bottom - 8;
    for (var i = 0; i <= ticks; i++) {
      var y = 8 + plotH - (plotH * i) / ticks;
      svg.appendChild(el('line', { x1: leftPad, x2: W - 8, y1: y, y2: y, stroke: '#e7e9ee', 'stroke-width': 1 }));
      svg.appendChild(el('text', { x: leftPad - 8, y: y + 3.5, 'text-anchor': 'end' }, (money ? '₹' : '') + fmt((top * i) / ticks)));
    }
    var every = Math.ceil(labels.length > 8 ? labels.length / 7 : 1);
    labels.forEach(function (l, i) {
      if (i % every) return;
      var x = leftPad + slot * i + slot / 2, y = 8 + plotH + 16;
      var t = el('text', { x: x, y: y, 'text-anchor': rotate ? 'end' : 'middle' }, l);
      if (rotate) t.setAttribute('transform', 'rotate(-35 ' + x + ' ' + y + ')');
      svg.appendChild(t);
    });
    return { left: leftPad, slot: slot, plotH: plotH, top: top, y: function (v) { return 8 + plotH - (plotH * v) / top; } };
  }

  function bars(box, a) {
    var W = Math.max(box.clientWidth, 260), H = +box.getAttribute('data-height') || 260;
    var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, role: 'img' });
    var g = axes(box, svg, W, H, a.labels, a.series, a.money);
    var n = a.series.length, bw = Math.min(26, (g.slot * 0.7) / n), gap = 3;
    a.labels.forEach(function (l, i) {
      var x0 = g.left + g.slot * i + g.slot / 2 - (n * bw + (n - 1) * gap) / 2;
      a.series.forEach(function (s, k) {
        var y = g.y(s.values[i]);
        var r = el('rect', { x: x0 + k * (bw + gap), y: y, width: bw, height: Math.max(0, 8 + g.plotH - y), rx: 3, style: 'fill:' + s.color });
        r.appendChild(el('title', {}, s.name + ', ' + l + ': ' + (a.money ? '₹' : '') + fmt(s.values[i])));
        svg.appendChild(r);
      });
    });
    return svg;
  }

  function line(box, a) {
    var W = Math.max(box.clientWidth, 260), H = +box.getAttribute('data-height') || 260;
    var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, role: 'img' });
    var g = axes(box, svg, W, H, a.labels, a.series, a.money);
    a.series.forEach(function (s, k) {
      var pts = s.values.map(function (v, i) { return [g.left + g.slot * i + g.slot / 2, g.y(v)]; });
      var d = pts.map(function (p, i) { return (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join(' ');
      if (a.area && k === 0) svg.appendChild(el('path', { d: d + ' L' + pts[pts.length - 1][0] + ' ' + (8 + g.plotH) + ' L' + pts[0][0] + ' ' + (8 + g.plotH) + ' Z', style: 'fill:' + s.color + ';opacity:.12' }));
      svg.appendChild(el('path', { d: d, fill: 'none', 'stroke-width': 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round', style: 'stroke:' + s.color }));
      if (pts.length <= 14 && s.dots !== false) pts.forEach(function (p, i) {
        var c = el('circle', { cx: p[0], cy: p[1], r: 3, style: 'fill:#fff;stroke-width:2;stroke:' + s.color });
        c.appendChild(el('title', {}, s.name + ', ' + a.labels[i] + ': ' + fmt(s.values[i])));
        svg.appendChild(c);
      });
    });
    return svg;
  }

  function donut(box, a) {
    var size = 176, r = 68, w = 26, c = size / 2, total = a.series.reduce(function (t, s) { return t + s.value; }, 0), acc = 0;
    var svg = el('svg', { viewBox: '0 0 ' + size + ' ' + size, width: size, height: size, role: 'img' });
    svg.setAttribute('class', 'donut-svg');
    a.series.forEach(function (s) {
      var f = s.value / total, circ = 2 * Math.PI * r;
      var arc = el('circle', { cx: c, cy: c, r: r, fill: 'none', 'stroke-width': w, transform: 'rotate(' + (-90 + acc * 360) + ' ' + c + ' ' + c + ')',
        'stroke-dasharray': (f * circ - 1.5).toFixed(2) + ' ' + circ.toFixed(2), style: 'stroke:' + s.color });
      arc.appendChild(el('title', {}, s.name + ': ' + fmt(s.value) + ' (' + (f * 100).toFixed(1) + '%)'));
      svg.appendChild(arc);
      acc += f;
    });
    svg.appendChild(el('text', { x: c, y: c + 2, 'text-anchor': 'middle', class: 'big' }, a.center || fmt(total)));
    svg.appendChild(el('text', { x: c, y: c + 20, 'text-anchor': 'middle', class: 'cap' }, a.caption || ''));
    var wrap = document.createElement('div');
    wrap.className = 'donut';
    wrap.appendChild(svg);
    var lg = document.createElement('div');
    lg.className = 'legend';
    a.series.forEach(function (s) {
      var sp = document.createElement('span');
      sp.style.setProperty('--c', s.color);
      sp.innerHTML = s.name + '<em>' + (s.value / total * 100).toFixed(1) + '%</em>';
      lg.appendChild(sp);
    });
    wrap.appendChild(lg);
    return wrap;
  }

  function render(box) {
    var a = {
      type: box.getAttribute('data-type'), labels: JSON.parse(box.getAttribute('data-labels') || '[]'), series: JSON.parse(box.getAttribute('data-series') || '[]'),
      money: box.getAttribute('data-money') === 'true', area: box.getAttribute('data-area') === 'true',
      center: box.getAttribute('data-center'), caption: box.getAttribute('data-caption')
    };
    box.textContent = '';
    box.appendChild(a.type === 'donut' ? donut(box, a) : a.type === 'line' ? line(box, a) : bars(box, a));
    if (a.type !== 'donut' && a.series.length > 1) {
      var lg = document.createElement('div');
      lg.className = 'legend';
      lg.style.marginTop = '0.5rem';
      a.series.forEach(function (s) { var sp = document.createElement('span'); sp.style.setProperty('--c', s.color); sp.textContent = s.name; lg.appendChild(sp); });
      box.appendChild(lg);
    }
  }

  var boxes = Array.prototype.slice.call(document.querySelectorAll('.chart[data-type]'));
  var draw = function () { boxes.forEach(render); };
  draw();
  var t, last = window.innerWidth;
  window.addEventListener('resize', function () {
    if (window.innerWidth === last) return;
    last = window.innerWidth; clearTimeout(t); t = setTimeout(draw, 120);
  });
})();
