"""Phase 4, part A: Primary Customer Sales and Operations Manager: Dashboard, Low Stock Overview, Stock Movement History,
Dispatch Overview, Dealer Order Activity, Dealer Performance, Pending Dealer Requests.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md "Phase 4 data"."""
from data import *

SQ = chr(0x2212)                                                       # minus sign
def signed(n): return f'+{n}' if n > 0 else f'{SQ}{abs(n)}' if n < 0 else '0'
def prod_cell(s, sid=None):
    name = f'<a data-link="{sid}"><b>{BY[s][1]}</b></a>' if sid else f'<b>{BY[s][1]}</b>'
    return f'<div class="prod">{sw(s)}<div>{name}</div></div>'
FUL = {'Delivered': 'ok', 'In Transit': 'blue', 'Being Packed': 'warn', 'Awaiting Confirmation': 'warn'}
PEND = f'<tr><td class="mono nowrap"><b>{NEW_ORDER}</b></td><td>26/10/2026</td><td>{{DEALER}}</td>{{SHEETS}}<td class="num"><b>{M(NEW_TOTAL)}</b></td><td>{chip("Awaiting Confirmation")}</td>{{TAIL}}</tr>'
def ful(st): return chip(st, FUL[st])
def growth(a, b):
    if not b: return chip('New', 'blue')
    v = (a - b) / b * 100
    return f'<span class="delta {"up" if v >= 0 else "down"}"><i data-icon="trend"></i>{abs(v):.1f}%</span>'
WEEK_VALUE = [sum(s['value'] for s in week_sales(a, b)) for _, a, b in WEEKS]
assert sum(WEEK_VALUE) == 3120000
OUT_ACTIVE = STATUS_COUNT['Being Packed'] + STATUS_COUNT['In Transit']          # 3 outgoing dispatches in progress
IN_ACTIVE = sum(1 for _o, (_d, st, _l) in OPEN_ORDERS.items() if st == 'In Transit')   # 1 incoming shipment on its way
DISPATCHES = []                                                                  # dispatches in progress: incoming first, then outgoing
for o, (dt, st, lines) in OPEN_ORDERS.items():
    if st == 'In Transit': DISPATCHES.append(('DSP-2026-5523', 'Incoming', 'Crestline Laminates', sum(q for _, q in lines), dt, st))
for s in SALES:
    if s['status'] != 'Delivered': DISPATCHES.append((s['dispatch'], 'Outgoing', DLR[s['dealer']][1], s['sheets'], s['expected'], s['status']))
assert len(DISPATCHES) == OUT_ACTIVE + IN_ACTIVE == 4
dsp_rows = ''.join(f'<tr><td class="mono nowrap"><b>{d[0]}</b></td><td>{chip(d[1], "plain")}</td><td>{d[2]}</td><td class="num">{N(d[3])}</td><td>{d[4]}</td><td>{ful(d[5])}</td></tr>' for d in DISPATCHES)
DSP_HEADS = [('Dispatch Number', ''), ('Direction', ''), ('Company or Dealer', ''), ('Sheets', 'num'), ('Expected', ''), ('Status', '')]

# ---------- Dashboard ----------
recent = ''.join(f'<tr><td class="mono nowrap"><b>{s["number"]}</b></td><td>{s["date"]}</td><td>{link("PRI-DLR-02", DLR[s["dealer"]][1])}</td><td class="num"><b>{M(s["value"])}</b></td><td>{ful(s["status"])}</td></tr>' for s in SALES[:5])
recent = PEND.replace('{DEALER}', link("PRI-DLR-02", 'Dealer Bravo')).replace('{SHEETS}', '').replace('{TAIL}', '') + recent
req_list = ''.join(f'<li><div class="grow"><div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap"><b>{r[1]}</b><span class="tag">{r[2]}</span></div></div>{chip(r[10])}</li>' for r in REQUESTS)
low_rows = ''.join(f'<tr><td>{prod_cell(p[0], "PRI-INV-03")}</td><td class="mono nowrap">{p[0]}</td><td class="num"><b>{N(p[10])}</b></td><td class="num">{N(p[12])}</td><td class="num">{N(REORDER_QTY[p[0]])}</td><td>{chip(p[13])}</td></tr>' for p in LOW)
ful_donut = chart('donut', series=[{'name': 'Delivered', 'value': STATUS_COUNT['Delivered'], 'color': 'var(--ok)'}, {'name': 'In Transit', 'value': STATUS_COUNT['In Transit'], 'color': 'var(--accent)'},
                                   {'name': 'Being Packed', 'value': STATUS_COUNT['Being Packed'], 'color': '#e0a030'}], center='32', caption='orders')
body = f'''  <div class="head">
    <h1>Dashboard</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><a class="btn pri" data-link="PRI-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Dealer Orders This Month', str(SALE_COUNT), chip(ML(3120000), 'blue'))}
    {kpi('Low Stock Products', str(len(LOW)), '<span class="delta down">1 Out of Stock</span>')}
    {kpi('Pending Dealer Requests', str(len(REQUESTS)), '<span class="delta down">2 Awaiting Your Review</span>')}
    {kpi('Dispatches in Progress', str(len(DISPATCHES)), chip('1 Incoming', 'plain'))}
  </div>
  <div class="grid g-chart">
    {card('Dealer Orders by Week', chart('bars', [w[0] for w in WEEKS], [{'name': 'Order value', 'values': WEEK_VALUE, 'color': 'var(--teal)'}], money=True, height=280))}
    <section class="card"><header><h2>Order Fulfilment</h2></header><div class="body center">{ful_donut}</div></section>
  </div>
  <div class="grid g-main-side" style="--side:20rem">
    <section class="card flush"><header><h2>Recent Dealer Orders</h2><a class="more" data-link="PRI-DLR-04">All dealer orders</a></header>
      <div class="body">{table([('Sale Number', ''), ('Date', ''), ('Dealer', ''), ('Value', 'num'), ('Status', '')], [recent])}</div></section>
    <section class="card"><header><h2>Pending Dealer Requests</h2><a class="more" data-link="PRI-DLR-06">All requests</a></header>
      <div class="body"><ul class="list">{req_list}</ul>{kv([('Requested Credit', ML(sum(r[7] for r in REQUESTS)))], 'total')}</div></section>
  </div>
  <section class="card flush"><header><h2>Dispatches in Progress</h2><a class="more" data-link="PRI-DSP-01">Dispatch overview</a></header>
    <div class="body">{table(DSP_HEADS, [dsp_rows])}</div></section>
  <section class="card flush"><header><h2>Low Stock</h2><a class="more" data-link="PRI-INV-03">Low stock overview</a></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Available', 'num'), ('Reorder Level', 'num'), ('Suggested Order', 'num'), ('Status', '')], [low_rows])}</div></section>
'''
page('primary', 'sales-and-operations-manager-dashboard', 'PRI-MGR-01', 'Primary Customer — Sales and Operations Manager — Dashboard (PRI-MGR-01)', body)

# ---------- Low Stock Overview ----------
low_tbl = ''
for p in sorted(LOW, key=lambda p: (p[13] != 'Out of Stock', p[10] / p[12])):
    s = p[0]; q = REORDER_QTY[s]
    low_tbl += (f'<tr><td>{prod_cell(s, "PRI-INV-02")}</td><td class="mono nowrap">{s}</td><td class="num"><b>{N(p[10])}</b></td><td class="num">{N(p[12])}</td>'
                f'<td class="num">{N(p[11]) if p[11] else "—"}</td><td>{chip(p[13])}</td>'
                f'<td class="num"><b>{N(q)}</b></td><td class="num">{M(LOW_VALUE[s])}</td></tr>\n')
short = sum(p[12] - p[10] for p in LOW)
assert short == 460
arr_rows = ''.join(f'<tr><td class="mono nowrap"><b>{o}</b></td><td class="num">{N(sum(q for _, q in l))}</td><td>{d}</td><td>{chip(st)}</td></tr>' for o, (d, st, l) in OPEN_ORDERS.items())
body = f'''  <div class="head">
    <h1>Low Stock Overview</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Low Stock</button><a class="btn pri" data-link="PRI-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Products Below Reorder Level', str(len(LOW)), chip('3 Low Stock', 'warn'))}
    {kpi('Out of Stock', '1', '<span class="delta down">LM-STN-009</span>')}
    {kpi('Sheets Short of Reorder Level', N(short))}
    {kpi('Suggested Order Value', ML(sum(LOW_VALUE.values())))}
  </div>
  <div class="grid g-main-side" style="--side:36rem">
    {card('Available Sheets Against Reorder Level', chart('bars', [p[0] for p in LOW], [{'name': 'Available', 'values': [p[10] for p in LOW], 'color': 'var(--accent)'}, {'name': 'Reorder level', 'values': [p[12] for p in LOW], 'color': 'var(--bad)'}], height=210))}
    <section class="card flush"><header><h2>Arriving From Crestline</h2></header><div class="body">{table([('Order Number', ''), ('Sheets', 'num'), ('Expected', ''), ('Status', '')], [arr_rows])}</div></section>
  </div>
  <section class="card flush">
    {tabs([('All Products', len(LOW), True), ('Low Stock', 3, False), ('Out of Stock', 1, False)])}
    {filters('Search by product name or SKU', 'Search low stock products', ('Finish', 'All'), ('Sort by', 'Urgency'))}
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Available', 'num'), ('Reorder Level', 'num'), ('On Order', 'num'), ('Status', ''), ('Suggested Order', 'num'), ('Estimated Value', 'num')], [low_tbl],
      foot=f'<tfoot><tr><td colspan="6">Total</td><td class="num">{N(sum(REORDER_QTY.values()))}</td><td class="num">{M(sum(LOW_VALUE.values()))}</td></tr></tfoot>')}</div>
  </section>
'''
page('primary', 'low-stock-overview', 'PRI-INV-03', 'Primary Customer — Sales and Operations Manager — Low Stock Overview (PRI-INV-03)', body)

# ---------- Stock Movement History ----------
TYPE_CHIP = {'Receipt': 'ok', 'Sale to Dealer': 'blue', 'Stock Adjustment': 'warn'}
mv_rows = ''.join(f'<tr><td>{m["date"]}</td><td>{chip(m["type"], TYPE_CHIP[m["type"]])}</td><td>{prod_cell(m["sku"], "PRI-INV-02")}</td><td class="mono nowrap">{m["sku"]}</td><td>{m["who"]}</td>'
                  f'<td class="mono nowrap">{m["ref"]}</td><td class="num"><b>{signed(m["sheets"])}</b></td></tr>\n' for m in MOVES[:12])
n_type = lambda t: sum(1 for m in MOVES if m['type'] == t)
by_prod = ''.join(f'<tr><td>{prod_cell(p[0], "PRI-INV-02")}</td><td class="mono nowrap">{p[0]}</td><td class="num">{N(MOVE_BY[p[0]]["received"]) if MOVE_BY[p[0]]["received"] else "—"}</td>'
                  f'<td class="num">{N(MOVE_BY[p[0]]["sold"]) if MOVE_BY[p[0]]["sold"] else "—"}</td><td class="num">{signed(MOVE_BY[p[0]]["adjusted"]) if MOVE_BY[p[0]]["adjusted"] else "—"}</td>'
                  f'<td class="num"><b>{signed(MOVE_BY[p[0]]["received"] - MOVE_BY[p[0]]["sold"] + MOVE_BY[p[0]]["adjusted"])}</b></td><td class="num">{N(p[8])}</td></tr>' for p in P)
tot_net = RECEIVED - 2195 + ADJUSTED
wk_recv = [sum(m['sheets'] for m in MOVES if m['type'].startswith('Receipt') and a <= int(m['date'][:2]) <= b) for _, a, b in WEEKS]
wk_sold = [sum(-m['sheets'] for m in MOVES if m['type'].startswith('Sale') and a <= int(m['date'][:2]) <= b) for _, a, b in WEEKS]
assert sum(wk_recv) == 1350 and sum(wk_sold) == 2195
body = f'''  <div class="head">
    <h1>Stock Movement History</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Movements</button></div>
  </div>
  <div class="kpis">
    {kpi('Received From Crestline', f'{N(RECEIVED)} <small>sheets</small>', chip('3 orders', 'plain'))}
    {kpi('Sold to Dealers', f'{N(2195)} <small>sheets</small>', chip(f'{SALE_COUNT} sales', 'plain'))}
    {kpi('Stock Adjustments', f'{SQ}30 <small>sheets</small>', chip('6 adjustments', 'plain'))}
    {kpi('Sheets on Hand', '7,415')}
  </div>
  {card('Sheets Moved by Week', chart('bars', [w[0] for w in WEEKS], [{'name': 'Received from Crestline', 'values': wk_recv, 'color': 'var(--teal)'}, {'name': 'Sold to dealers', 'values': wk_sold, 'color': 'var(--accent)'}], height=260))}
  <section class="card flush">
    {tabs([('All Movements', len(MOVES), True), ('Receipts', n_type('Receipt'), False), ('Sales to Dealers', n_type('Sale to Dealer'), False), ('Adjustments', n_type('Stock Adjustment'), False)])}
    {filters('Search by product, dealer or reference', 'Search stock movements', ('Date Range', 'October 2026'), ('Product', 'All'), ('Type', 'All'))}
    <div class="body">{table([('Date', ''), ('Type', ''), ('Product', ''), ('SKU', ''), ('Name or Reason', ''), ('Reference', ''), ('Sheets', 'num')], [mv_rows])}
      {pager(f'Showing 1 to 12 of {len(MOVES)} movements')}</div>
  </section>
  <section class="card flush"><header><h2>Movement by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Received', 'num'), ('Sold to Dealers', 'num'), ('Adjusted', 'num'), ('Net Change', 'num'), ('On Hand Now', 'num')], [by_prod],
      foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(RECEIVED)}</td><td class="num">{N(2195)}</td><td class="num">{signed(ADJUSTED)}</td><td class="num">{signed(tot_net)}</td><td class="num">7,415</td></tr></tfoot>')}</div></section>
'''
page('primary', 'stock-movement-history', 'PRI-INV-04', 'Primary Customer — Sales and Operations Manager — Stock Movement History (PRI-INV-04)', body)

# ---------- Dispatch Overview ----------
out_rows = ''.join(f'<tr><td class="mono nowrap"><b>{s["dispatch"]}</b></td><td class="mono nowrap">{s["number"]}</td><td>{link("PRI-DLR-02", DLR[s["dealer"]][1])}</td><td>{s["city"]}</td><td class="num">{N(s["sheets"])}</td><td>{s["date"]}</td><td>{s["expected"]}</td><td>{ful(s["status"])}</td></tr>' for s in SALES[:10])
inc_rows = ''
for o, (dt, st, lines) in OPEN_ORDERS.items():
    inc_rows += (f'<tr><td>{link("PRI-ORD-02", o)}</td><td class="{"mono nowrap" if st == "In Transit" else ""}">{"DSP-2026-5523" if st == "In Transit" else "—"}</td><td>{"Western Freight Carriers" if st == "In Transit" else "—"}</td>'
                 f'<td class="num">{N(sum(q for _, q in lines))}</td><td>{dt}</td><td>{chip(st)}</td></tr>')
body = f'''  <div class="head">
    <h1>Dispatch Overview</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Dispatches</button></div>
  </div>
  <div class="kpis">
    {kpi('Incoming Shipments', str(len(OPEN_ORDERS)), chip(f'{N(OPEN_SHEETS)} sheets', 'plain'))}
    {kpi('Outgoing Being Packed', str(STATUS_COUNT['Being Packed']))}
    {kpi('Outgoing in Transit', str(STATUS_COUNT['In Transit']))}
    {kpi('Delivered This Month', str(STATUS_COUNT['Delivered']), chip(f'of {SALE_COUNT} dispatches', 'plain'))}
  </div>
  <section class="card flush"><header><h2>Incoming Shipments From Crestline</h2><a class="more" data-link="PRI-ORD-01">Order history</a></header>
    <div class="body">{table([('Order Number', ''), ('Dispatch Number', ''), ('Transporter', ''), ('Sheets', 'num'), ('Expected Delivery', ''), ('Status', '')], [inc_rows])}</div></section>
  <section class="card flush"><header><h2>Outgoing Deliveries to Dealers</h2></header>
    {tabs([('All Deliveries', SALE_COUNT, True), ('Being Packed', STATUS_COUNT['Being Packed'], False), ('In Transit', STATUS_COUNT['In Transit'], False), ('Delivered', STATUS_COUNT['Delivered'], False)])}
    {filters('Search by dispatch number, sale number or dealer', 'Search deliveries', ('Date Range', 'October 2026'), ('Dealer', 'All'))}
    <div class="body">{table([('Dispatch Number', ''), ('Sale Number', ''), ('Dealer', ''), ('City', ''), ('Sheets', 'num'), ('Dispatched', ''), ('Expected Delivery', ''), ('Status', '')], [out_rows])}
      {pager(f'Showing 1 to 10 of {SALE_COUNT} deliveries')}</div></section>
'''
page('primary', 'dispatch-overview', 'PRI-DSP-01', 'Primary Customer — Sales and Operations Manager — Dispatch Overview (PRI-DSP-01)', body)

# ---------- Dealer Order Activity ----------
cnt = lambda st: sum(1 for s in SALES if s['status'] == st)
act_rows = ''.join(f'<tr><td class="mono nowrap"><b>{s["number"]}</b></td><td>{s["date"]}</td><td>{link("PRI-DLR-02", DLR[s["dealer"]][1])}</td><td class="num">{N(s["sheets"])}</td><td class="num"><b>{M(s["value"])}</b></td><td>{ful(s["status"])}</td><td>{pay_chip(s["payment"])}</td></tr>' for s in SALES[:9])
act_rows = PEND.replace('{DEALER}', link("PRI-DLR-02", 'Dealer Bravo')).replace('{SHEETS}', '<td class="num">210</td>').replace('{TAIL}', f'<td>{pay_chip("Unpaid")}</td>') + act_rows
by_dealer = sorted(DEALERS, key=lambda d: -sum(1 for s in SALES if s['dealer'] == d[0]))
mx = max(sum(1 for s in SALES if s['dealer'] == d[0]) for d in DEALERS)
dealer_list = ''.join(f'<li><div class="grow"><div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap"><b>{d[1]}</b><span class="tag">{d[2]}</span></div><span class="meter" style="margin-top:.625rem"><i style="width:{sum(1 for s in SALES if s["dealer"] == d[0]) / mx * 100:.0f}%"></i></span></div><b>{sum(1 for s in SALES if s["dealer"] == d[0])}</b></li>' for d in by_dealer)
body = f'''  <div class="head">
    <h1>Dealer Order Activity</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Orders</button></div>
  </div>
  <div class="kpis">
    {kpi('Confirmed Orders', str(SALE_COUNT))}
    {kpi('Order Value', ML(3120000), up('11.8%'))}
    {kpi('Awaiting Confirmation', '1', chip(ML(NEW_TOTAL), 'warn'))}
    {kpi('Awaiting Dispatch', str(cnt('Being Packed')), chip('Being Packed', 'warn'))}
  </div>
  <div class="grid g-main-side" style="--side:26rem">
    {card('Order Value by Week', chart('bars', [w[0] for w in WEEKS], [{'name': 'Order value', 'values': WEEK_VALUE, 'color': 'var(--teal)'}], money=True, height=470))}
    {card('Orders by Dealer', f'<ul class="list">{dealer_list}</ul>')}
  </div>
  <section class="card flush">
    {tabs([('All Orders', SALE_COUNT + 1, True), ('Awaiting Confirmation', 1, False), ('Being Packed', cnt('Being Packed'), False), ('In Transit', cnt('In Transit'), False), ('Delivered', cnt('Delivered'), False)])}
    {filters('Search by sale number or dealer', 'Search dealer orders', ('Date Range', 'October 2026'), ('Dealer', 'All'), ('Payment', 'All'))}
    <div class="body">{table([('Sale Number', ''), ('Date', ''), ('Dealer', ''), ('Sheets', 'num'), ('Value', 'num'), ('Fulfilment', ''), ('Payment', '')], [act_rows])}
      {pager(f'Showing 1 to 10 of {SALE_COUNT + 1} orders')}</div>
  </section>
'''
page('primary', 'dealer-order-activity', 'PRI-DLR-04', 'Primary Customer — Sales and Operations Manager — Dealer Order Activity (PRI-DLR-04)', body)

# ---------- Dealer Performance ----------
rank = sorted(DEALERS, key=lambda d: -d[7])
perf_rows = ''
for n, d in enumerate(rank, 1):
    k = d[0]; a = achievement(k)
    perf_rows += (f'<tr><td class="num">{n}</td><td>{link("PRI-DLR-02", d[1])}</td><td>{d[2]}</td><td class="num"><b>{M(d[7])}</b></td><td>{growth(d[7], d[8])}</td>'
                  f'<td class="num">{M(TARGET[k])}</td><td><span class="inline-meter"><span class="meter {"ok" if a >= 100 else "warn" if a >= 95 else "bad"}"><i style="width:{min(a, 100):.0f}%"></i></span><b>{a:.1f}%</b></span></td><td>{chip(perf_status(k))}</td></tr>')
above = sum(1 for d in DEALERS if achievement(d[0]) >= 100)
assert above == 4
best = max((d for d in DEALERS if d[8]), key=lambda d: d[7] / d[8])
body = f'''  <div class="head">
    <h1>Dealer Performance</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Performance</button></div>
  </div>
  <div class="kpis">
    {kpi('Sales This Month', ML(3120000), up('11.8%'))}
    {kpi('Sales Target', ML(TARGET_TOTAL))}
    {kpi('Target Achievement', f'{3120000 / TARGET_TOTAL * 100:.1f}%', chip('Near Target', 'warn'))}
    {kpi('Dealers Above Target', f'{above} <small>of 8</small>')}
  </div>
  {card('Sales Against Target by Dealer', chart('bars', [d[1] for d in rank], [{'name': 'Sales', 'values': [d[7] for d in rank], 'color': 'var(--accent)'}, {'name': 'Target', 'values': [TARGET[d[0]] for d in rank], 'color': '#c9ccd3'}], money=True, height=300))}
  <section class="card flush"><header><h2>Dealers Ranked by Sales</h2><a class="more" data-link="PRI-DLR-01">Dealer network</a></header>
    <div class="body">{table([('Rank', 'num'), ('Dealer', ''), ('City', ''), ('Sales This Month', 'num'), ('Growth Over September', ''), ('Sales Target', 'num'), ('Target Achievement', ''), ('Status', '')], [perf_rows],
      foot=f'<tfoot><tr><td colspan="3">Total</td><td class="num">{M(3120000)}</td><td></td><td class="num">{M(TARGET_TOTAL)}</td><td colspan="2"></td></tr></tfoot>')}</div></section>
'''
page('primary', 'dealer-performance', 'PRI-DLR-05', 'Primary Customer — Sales and Operations Manager — Dealer Performance (PRI-DLR-05)', body)

# ---------- Pending Dealer Requests ----------
def req_actions(r):
    if r[10] == 'Awaiting Your Review':
        return '<div class="row-actions"><button class="btn sm" type="button">Reject</button><button class="btn sm pri" type="button">Approve</button></div>'
    return f'<div class="row-actions">{chip(r[10])}</div>'
req_rows = ''.join(f'<tr><td class="mono nowrap"><b>{r[0]}</b></td><td class="nowrap"><b>{r[1]}</b> <span class="tag">{r[2]}</span></td><td>{r[5]}</td><td class="num">{M(r[7])}</td>'
                   f'<td>{chip(f"{r[9]} of 3", "ok" if r[9] == 3 else "warn")}</td><td>{req_actions(r)}</td></tr>' for r in REQUESTS)
body = f'''  <div class="head">
    <h1>Pending Dealer Requests</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Requests</button></div>
  </div>
  <div class="kpis">
    {kpi('Pending Requests', str(len(REQUESTS)))}
    {kpi('Awaiting Your Review', '2', chip('Decision needed', 'warn'))}
    {kpi('Sent to Crestline', '1', chip('Vikram Chopra', 'blue'))}
    {kpi('Requested Credit', ML(sum(r[7] for r in REQUESTS)))}
  </div>
  <section class="card flush">
    {tabs([('All Pending', len(REQUESTS), True), ('Awaiting Your Review', 2, False), ('Sent to Crestline', 1, False)])}
    {filters('Search by dealer name or city', 'Search dealer requests', ('Region', 'All'), ('Submitted', 'Last 30 days'))}
    <div class="body">{table([('Request Number', ''), ('Dealer', ''), ('Submitted', ''), ('Requested Credit', 'num'), ('Documents', ''), ('Decision', '')], [req_rows])}
      {pager('Showing 1 to 3 of 3 requests', 1)}</div>
  </section>
'''
page('primary', 'pending-dealer-requests', 'PRI-DLR-06', 'Primary Customer — Sales and Operations Manager — Pending Dealer Requests (PRI-DLR-06)', body)
