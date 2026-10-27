"""Phase 13, part B: Company Administration, Operations Manager: Dashboard, Order Processing Queue, Delayed Orders, Dispatch Details, Stock Movement History,
Return Requests, Delivery Issues, Operational Reports. Links go only to screens the Operations Manager can open (Order Details, Dispatch Management,
Inventory Overview, Support Ticket Management and Details, and the screens below). Design rule: no text under page titles, no captions beside card titles,
no helper sentences. Data: docs/DATA.md "Phase 11", "Phase 12" and "Phase 13 data"."""
from data import *

SQ = chr(0x2212)
STATUS_CHIP.update({'Due Today': 'warn', 'On Time': 'ok', 'Late': 'bad', 'Resolved': 'ok', 'Stock Reserved': 'ok', 'Not Started': 'plain'})
cust = 'Distributor Alpha'
O59R = ORDER_LINES['ORD-2026-10459']
def signed(v): return f'+{v}' if v > 0 else f'{SQ}{abs(v)}' if v < 0 else '0'
wk_ship = [sum(s[3] for s in SHIP_OCT if a <= int(s[4][:2]) <= b) for _, a, b in WEEKS]

# ---------- Dashboard ----------
queue_row = (f'<tr><td>{link("CMP-ORD-02", "ORD-2026-10459")}</td><td>{cust}</td><td class="num">280</td><td>{chip("Stock Reserved")}</td><td>{chip("Due Today")}</td><td>26/10/2026</td><td>29/10/2026</td></tr>')
ship_rows = ''.join(f'<tr><td class="mono nowrap">{link("CMP-OPS-04", s[0])}</td><td>{s[1]}</td><td>{s[2]}</td><td class="num">{N(s[3])}</td><td>{s[5]}</td><td>{chip(s[6])}</td></tr>' for s in SHIPMENTS if s[6] == 'In Transit')
ret_rows = ''.join(f'<tr><td class="mono nowrap">{link("CMP-OPS-06", r[0])}</td><td>{r[1]}</td><td>{BY[r[3]][1]}</td><td class="num">{r[4]}</td><td>{r[5]}</td><td>{chip(r[6])}</td></tr>' for r in RET_OPEN)
low = [s for s, b in CSTK.items() if b['status'] != 'In Stock']
low_rows = ''.join(f'<li>{sw(s, "", "width:2.5rem;height:2.5rem;flex:none")}<div class="grow"><b>{BY[s][1]}</b><span class="meter warn" style="margin-top:.5rem"><i style="width:{CSTK[s]["available"] / CSTK[s]["level"] * 100:.0f}%"></i></span></div><b>{N(CSTK[s]["available"])} of {N(CSTK[s]["level"])}</b></li>' for s in low)
body = f'''  <div class="head">
    <h1>Dashboard</h1>
    <div class="acts"><span class="sel"><small>Day</small> 26 October 2026 <i data-icon="down"></i></span><a class="btn" data-link="CMP-DSP-01">Dispatch Management</a><a class="btn pri" data-link="CMP-OPS-02">Order Processing Queue</a></div>
  </div>
  <div class="kpis">
    {kpi('Orders Waiting to Be Processed', '1', chip('Packing Due Today', 'warn'))}
    {kpi('Dispatches Due Today', '1', chip('280 sheets', 'plain'))}
    {kpi('Delayed Orders', '0', chip('None Open', 'ok'))}
    {kpi('Open Return Requests', str(len(RET_OPEN)), chip(f'{RET_OPEN_SHEETS} sheets', 'plain'))}
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    {card('Sheets Dispatched by Week', chart('bars', [w[0] for w in WEEKS], [{'name': 'Sheets dispatched', 'values': wk_ship, 'color': 'var(--teal)'}], height=300))}
    {card('Low Stock Products', f'<ul class="list">{low_rows}</ul>' + '<a class="btn block" data-link="CMP-INV-01" style="margin-top:1rem">Inventory Overview</a>')}
  </div>
  <section class="card flush"><header><h2>Orders to Process</h2><a class="more" data-link="CMP-OPS-02">Order processing queue</a></header>
    <div class="body">{table([('Order Number', ''), ('Customer', ''), ('Sheets', 'num'), ('Stock', ''), ('Packing', ''), ('Dispatch Planned', ''), ('Expected Delivery', '')], [queue_row], 'wrap')}</div></section>
  <div class="stack">
    <section class="card flush"><header><h2>Shipments in Transit</h2><a class="more" data-link="CMP-DSP-01">All shipments</a></header><div class="body">{table([('Dispatch Number', ''), ('Order', ''), ('Transporter', ''), ('Sheets', 'num'), ('Expected', ''), ('Status', '')], [ship_rows], 'wrap')}</div></section>
    <section class="card flush"><header><h2>Open Return Requests</h2><a class="more" data-link="CMP-OPS-06">All requests</a></header><div class="body">{table([('Request', ''), ('Date', ''), ('Product', ''), ('Sheets', 'num'), ('Reason', ''), ('Status', '')], [ret_rows], 'wrap')}</div></section>
  </div>
'''
page('company', 'operations-manager-dashboard', 'CMP-OPS-01', 'Company Administration — Operations Manager — Dashboard (CMP-OPS-01)', body)

# ---------- Order Processing Queue ----------
done_rows = ''.join(f'<tr><td>{link("CMP-ORD-02", s[1])}</td><td class="mono nowrap">{link("CMP-OPS-04", s[0])}</td><td>{s[2]}</td><td class="num">{N(s[3])}</td><td>{s[4]}</td><td>{s[5]}</td><td>{chip(s[6])}</td></tr>' for s in SHIPMENTS if s[4].endswith('/10/2026') and s[6] != 'Being Packed')
body = f'''  <div class="head">
    <h1>Order Processing Queue</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Queue</button></div>
  </div>
  <div class="kpis">
    {kpi('Orders in Queue', '1')}
    {kpi('Sheets to Pack', N(280))}
    {kpi('Packing Due Today', '1', chip('ORD-2026-10459', 'warn'))}
    {kpi('Dispatched This Month', str(len(SHIP_OCT)), chip(f'{N(SHIP_OCT_SHEETS)} sheets', 'plain'))}
  </div>
  <section class="card flush">
    {tabs([('Waiting', 1, True), ('Packing', 0, False), ('Ready to Dispatch', 0, False)])}
    <div class="body" style="margin-top:1rem">{table([('Order Number', ''), ('Confirmed', ''), ('Sheets', 'num'), ('Stock Check', ''), ('Packing', ''), ('Dispatch Planned', ''), ('', '')],
      [f'<tr><td>{link("CMP-ORD-02", "ORD-2026-10459")}</td><td class="nowrap">23/10/2026 16:10</td><td class="num">280</td><td>{chip("Stock Reserved")}</td><td>{chip("Due Today")}</td><td>26/10/2026</td><td><div class="row-actions"><button class="btn sm pri" type="button">Mark as Packed</button></div></td></tr>'], 'wrap')}</div>
  </section>
  <section class="card flush"><header><h2>Processed This Month</h2></header><div class="body">{table([('Order Number', ''), ('Dispatch Number', ''), ('Transporter', ''), ('Sheets', 'num'), ('Dispatched', ''), ('Expected Delivery', ''), ('Status', '')], [done_rows], 'wrap')}</div></section>
'''
page('company', 'order-processing-queue', 'CMP-OPS-02', 'Company Administration — Operations Manager — Order Processing Queue (CMP-OPS-02)', body)

# ---------- Delayed Orders ----------
d_row = (f'<tr><td>{link("CMP-ORD-02", "ORD-2026-10398")}</td><td>{cust}</td><td class="num">430</td><td>{PROMISED["ORD-2026-10398"][0]}</td><td>{PROMISED["ORD-2026-10398"][1]}</td><td class="num">1</td><td>Batch Quality Check</td>'
         f'<td>{link("CMP-SUP-02", "TKT-2026-0688", False)}</td><td>{chip("Resolved")}</td></tr>')
due_row = (f'<tr><td>{link("CMP-ORD-02", "ORD-2026-10459")}</td><td>{cust}</td><td class="num">280</td><td>{PROMISED["ORD-2026-10459"][0]}</td><td>{chip("Due Today")}</td><td>Mark as Packed</td></tr>')
body = f'''  <div class="head">
    <h1>Delayed Orders</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Delays</button></div>
  </div>
  <div class="kpis">
    {kpi('Delayed Orders Now', '0', chip('None Open', 'ok'))}
    {kpi('Delayed This Month', '1', chip('ORD-2026-10398', 'plain'))}
    {kpi('Average Delay', '1 <small>day</small>')}
    {kpi('Dispatched On Time', f'{len(ON_TIME_OCT) / len(SHIP_OCT) * 100:.1f}%', chip(f'{len(ON_TIME_OCT)} of {len(SHIP_OCT)}', 'plain'))}
  </div>
  <section class="card flush"><header><h2>Due for Dispatch Today</h2></header><div class="body">{table([('Order Number', ''), ('Customer', ''), ('Sheets', 'num'), ('Promised Dispatch', ''), ('Status', ''), ('Next Action', '')], [due_row], 'wrap')}</div></section>
  <section class="card flush">
    {tabs([('All Delayed Orders', 1, True), ('Open', 0, False), ('Resolved', 1, False)])}
    <div class="body" style="margin-top:1rem">{table([('Order Number', ''), ('Customer', ''), ('Sheets', 'num'), ('Promised Dispatch', ''), ('Dispatched', ''), ('Days Late', 'num'), ('Reason', ''), ('Support Ticket', ''), ('Status', '')], [d_row], 'wrap')}</div>
  </section>
'''
page('company', 'delayed-orders', 'CMP-OPS-03', 'Company Administration — Operations Manager — Delayed Orders (CMP-OPS-03)', body)

# ---------- Dispatch Details (DSP-2026-5523) ----------
sh = SHIPMENTS[1]; assert sh[0] == 'DSP-2026-5523'
L = ORDER_LINES['ORD-2026-10447']; kg = {s: q * 6.1 for s, q in L}; assert all(BY[s][3] == '1.0 mm' for s, _ in L) and sum(kg.values()) == 2196
i_rows = ''.join(f'<tr><td>{prod_cell(s)}</td><td class="mono nowrap">{s}</td><td class="num">{N(q)}</td><td class="num">{N(round(kg[s]))} kg</td></tr>' for s, q in L)
body = f'''  <div class="head">
    <div class="title-row"><h1>{sh[0]}</h1>{chip("In Transit")}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Dispatch Note</button><button class="btn pri" type="button">Update Delivery Status</button></div>
  </div>
  <section class="card pad"><ol class="track">
    <li class="done"><i></i><b>Order Confirmed</b><span>20/10/2026 09:40</span></li><li class="done"><i></i><b>Packed</b><span>23/10/2026 17:05</span></li><li class="done"><i></i><b>Dispatched</b><span>24/10/2026 06:30</span></li>
    <li class="now"><i></i><b>In Transit</b><span>Expected 27/10/2026</span></li><li class="todo"><i></i><b>Delivered</b><span>27/10/2026</span></li></ol></section>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
    <section class="card flush"><header><h2>Items</h2></header><div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Weight', 'num')], [i_rows], 'wrap',
      foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(sh[3])}</td><td class="num">{N(2196)} kg</td></tr></tfoot>')}</div></section>
    <section class="card flush"><header><h2>Shipment Activity</h2></header><div class="body">{table([('Date', ''), ('Event', ''), ('By', '')], [
      '<tr><td class="nowrap">24/10/2026 06:32</td><td><b>Invoice sent by email</b></td><td>Crestline Laminates</td></tr>',
      '<tr><td class="nowrap">24/10/2026 06:30</td><td><b>Shipment dispatched</b></td><td>Neha Kulkarni</td></tr>',
      '<tr><td class="nowrap">23/10/2026 17:05</td><td><b>Packing completed</b></td><td>Plant Warehouse, Vapi</td></tr>',
      '<tr><td class="nowrap">20/10/2026 09:40</td><td><b>Order confirmed</b></td><td>Vikram Chopra</td></tr>'], 'wrap')}</div></section>
    </div>
    <div class="stack">
      {card('Shipment', kv([('Dispatch Number', f'<span class="mono">{sh[0]}</span>'), ('Order', link('CMP-ORD-02', sh[1], False)), ('Customer', cust), ('Dispatched From', 'Plant Warehouse, Vapi'), ('Deliver To', 'Bhiwandi Warehouse, Thane District'), ('Dispatched', '24/10/2026 06:30'), ('Expected Delivery', sh[5])]))}
      {card('Transport', kv([('Transporter', sh[2]), ('Vehicle', 'MH 04 KP 7712'), ('Driver', 'Ramesh Pawar'), ('Driver Phone', '+91 90000 12345'), ('Invoice', '<span class="mono">INV-2026-03318</span>')]))}
    </div>
  </div>
'''
page('company', 'dispatch-details', 'CMP-OPS-04', 'Company Administration — Operations Manager — Dispatch Details (CMP-OPS-04)', body)

# ---------- Stock Movement History ----------
TYPE_CHIP = {'Production Receipt': 'ok', 'Dispatch to Customer': 'blue', 'Transfer': 'warn'}
mv_rows = ''.join(f'<tr><td>{m["date"]}</td><td>{chip(m["type"], TYPE_CHIP[m["type"]])}</td><td>{prod_cell(m["sku"])}</td><td class="mono nowrap">{m["sku"]}</td><td>{m["wh"]}</td><td class="mono nowrap">{m["ref"]}</td><td class="num"><b>{signed(m["sheets"])}</b></td></tr>' for m in CMOVES2[:12])
n_type = lambda t: sum(1 for m in CMOVES2 if m['type'] == t)
recv = {s: sum(m['sheets'] for m in CMOVES2 if m['sku'] == s and m['type'] == 'Production Receipt') for s in BY}
iss = {s: -sum(m['sheets'] for m in CMOVES2 if m['sku'] == s and m['type'] == 'Dispatch to Customer') for s in BY}
by_prod = ''.join(f'<tr><td>{prod_cell(p[0])}</td><td class="mono nowrap">{p[0]}</td><td class="num">{N(sum(CRL_OPENING[p[0]]))}</td><td class="num">{N(recv[p[0]]) if recv[p[0]] else "—"}</td><td class="num">{N(iss[p[0]]) if iss[p[0]] else "—"}</td><td class="num"><b>{N(CSTK[p[0]]["on_hand"])}</b></td></tr>' for p in P)
assert all(sum(CRL_OPENING[s]) + recv[s] - iss[s] == CSTK[s]['on_hand'] for s in BY)
wk_r = [sum(m['sheets'] for m in CMOVES2 if m['type'] == 'Production Receipt' and a <= int(m['date'][:2]) <= b) for _, a, b in WEEKS]
wk_i = [sum(-m['sheets'] for m in CMOVES2 if m['type'] == 'Dispatch to Customer' and a <= int(m['date'][:2]) <= b) for _, a, b in WEEKS]
assert sum(wk_r) == 8000 and sum(wk_i) == 1710
body = f'''  <div class="head">
    <h1>Stock Movement History</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><span class="sel"><small>Warehouse</small> All Warehouses <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Movements</button></div>
  </div>
  <div class="kpis">
    {kpi('Produced', f'{N(C_RECEIVED)} <small>sheets</small>', chip('3 batches', 'plain'))}
    {kpi('Dispatched to Customers', f'{N(C_ISSUED)} <small>sheets</small>', chip(f'{len(SHIP_OCT)} shipments', 'plain'))}
    {kpi('Transferred to Taloja', f'{N(C_TRANSFERRED)} <small>sheets</small>', chip('2 transfers', 'plain'))}
    {kpi('Sheets on Hand', N(CSTK_ON_HAND))}
  </div>
  {card('Sheets Moved by Week', chart('bars', [w[0] for w in WEEKS], [{'name': 'Production receipts', 'values': wk_r, 'color': 'var(--ok)'}, {'name': 'Dispatched to customers', 'values': wk_i, 'color': 'var(--accent)'}], height=260))}
  <section class="card flush">
    {tabs([('All Movements', len(CMOVES2), True), ('Production Receipts', n_type('Production Receipt'), False), ('Dispatches', n_type('Dispatch to Customer'), False), ('Transfers', n_type('Transfer'), False)])}
    {filters('Search by product, warehouse or reference', 'Search stock movements', ('Date Range', 'October 2026'), ('Product', 'All'), ('Warehouse', 'All'))}
    <div class="body">{table([('Date', ''), ('Type', ''), ('Product', ''), ('SKU', ''), ('Warehouse', ''), ('Reference', ''), ('Sheets', 'num')], [mv_rows], 'wrap')}
      {pager(f'Showing 1 to 12 of {len(CMOVES2)} movements')}</div>
  </section>
  <section class="card flush"><header><h2>Movement by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Opening Stock', 'num'), ('Produced', 'num'), ('Dispatched', 'num'), ('On Hand Now', 'num')], [by_prod], 'wrap',
      foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(sum(sum(CRL_OPENING[s]) for s in BY))}</td><td class="num">{N(C_RECEIVED)}</td><td class="num">{N(C_ISSUED)}</td><td class="num">{N(CSTK_ON_HAND)}</td></tr></tfoot>')}</div></section>
'''
page('company', 'stock-movement-history', 'CMP-OPS-05', 'Company Administration — Operations Manager — Stock Movement History (CMP-OPS-05)', body)

# ---------- Return Requests ----------
rr = ''.join(f'<tr><td class="mono nowrap"><b>{r[0]}</b></td><td>{r[1]}</td><td>{cust}</td><td class="mono nowrap">{link("CMP-ORD-02", r[2], False)}</td><td>{BY[r[3]][1]}</td><td class="num">{r[4]}</td><td>{r[5]}</td><td>{chip(r[6])}</td><td class="num">{M(CRL_CREDIT[r[0]]) if r[0] in CRL_CREDIT else "—"}</td></tr>' for r in CRL_RET)
body = f'''  <div class="head">
    <h1>Return Requests</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Requests</button></div>
  </div>
  <div class="kpis">
    {kpi('Open Requests', str(len(RET_OPEN)))}
    {kpi('Sheets Under Return', str(RET_OPEN_SHEETS))}
    {kpi('Credit Issued', M(sum(CRL_CREDIT.values())), chip('3 requests', 'plain'))}
    {kpi('Return Rate This Month', f'{RET_RATE:.1f}%', chip(f'{RET_OCT_SHEETS} of {N(SHIP_OCT_SHEETS)} sheets', 'plain'))}
  </div>
  <section class="card flush">
    {tabs([('All Requests', len(CRL_RET), True), ('Open', len(RET_OPEN), False), ('Credit Issued', 3, False), ('Rejected', 1, False)])}
    {filters('Search by request number, order or product', 'Search return requests', ('Reason', 'All'), ('Status', 'All'))}
    <div class="body">{table([('Request Number', ''), ('Date', ''), ('Customer', ''), ('Order', ''), ('Product', ''), ('Sheets', 'num'), ('Reason', ''), ('Status', ''), ('Credit', 'num')], [rr], 'wrap',
      foot=f'<tfoot><tr><td colspan="5">Total</td><td class="num">{sum(r[4] for r in CRL_RET)}</td><td colspan="2"></td><td class="num">{M(sum(CRL_CREDIT.values()))}</td></tr></tfoot>')}
      {pager(f'Showing 1 to {len(CRL_RET)} of {len(CRL_RET)} requests', 1)}</div>
  </section>
  <section class="card"><header><h2>RTN-2026-0412</h2><span style="margin-left:auto">{chip('Under Review')}</span></header><div class="body"><div class="grid g-2" style="gap:2rem">
    {kv([('Customer', cust), ('Order', link('CMP-ORD-02', 'ORD-2026-10431', False)), ('Product', BY['LM-CAL-003'][1]), ('Sheets', '12'), ('Reason', 'Damaged in Transit'), ('Support Ticket', link('CMP-SUP-02', 'TKT-2026-0731', False))])}
    <div class="stack"><div class="files" style="display:flex;flex-wrap:wrap;gap:.5rem"><span class="file"><i data-icon="doc"></i>damaged-corners-1.jpg</span><span class="file"><i data-icon="doc"></i>damaged-corners-2.jpg</span><span class="file"><i data-icon="doc"></i>packing-list.pdf</span></div>
    <div style="display:flex;flex-wrap:wrap;gap:.5rem"><button class="btn danger" type="button">Reject Request</button><button class="btn" type="button">Approve and Schedule Pickup</button><button class="btn pri" type="button">Approve Request</button></div></div></div></div></section>
'''
page('company', 'return-requests', 'CMP-OPS-06', 'Company Administration — Operations Manager — Return Requests (CMP-OPS-06)', body)

# ---------- Delivery Issues ----------
ISSUES = [('25/10/2026', 'ORD-2026-10431', 'Damaged in Transit', BY['LM-CAL-003'][1], '12 sheets', 'RTN-2026-0412', 'Under Review'),
          ('16/10/2026', 'ORD-2026-10398', 'Wrong Product Delivered', BY['LM-ARC-002'][1], '20 sheets', 'RTN-2026-0396', 'Pickup Scheduled'),
          ('10/10/2026', 'ORD-2026-10171', 'Quantity Shortfall', 'Short quantity on invoice', M(16992), 'DIS-2026-0011', 'Under Review'),
          ('09/10/2026', 'ORD-2026-10372', 'Damaged in Transit', BY['LM-OAK-004'][1], '15 sheets', 'RTN-2026-0377', 'Credit Issued'),
          ('18/09/2026', 'ORD-2026-10290', 'Damaged in Transit', BY['LM-TEK-006'][1], '14 sheets', 'RTN-2026-0319', 'Credit Issued')]
assert [CRL_RET[i][0] for i in (0, 2, 3, 6)] == ['RTN-2026-0412', 'RTN-2026-0396', 'RTN-2026-0377', 'RTN-2026-0319']
isr = ''.join(f'<tr><td>{i[0]}</td><td>{cust}</td><td class="mono nowrap">{link("CMP-ORD-02", i[1], False)}</td><td><b>{i[2]}</b></td><td>{i[3]}</td><td class="num">{i[4]}</td><td class="mono nowrap">{i[5]}</td><td>{chip(i[6])}</td></tr>' for i in ISSUES)
open_i = sum(1 for i in ISSUES if i[6] != 'Credit Issued')
body = f'''  <div class="head">
    <h1>Delivery Issues</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Issues</button></div>
  </div>
  <div class="kpis">
    {kpi('Open Issues', str(open_i))}
    {kpi('Reported This Month', str(sum(1 for i in ISSUES if i[0].endswith('/10/2026'))))}
    {kpi('Damaged in Transit', str(sum(1 for i in ISSUES if i[2] == 'Damaged in Transit')), chip('3 shipments', 'plain'))}
    {kpi('Resolved With Credit', str(sum(1 for i in ISSUES if i[6] == 'Credit Issued')))}
  </div>
  <section class="card flush">
    {tabs([('All Issues', len(ISSUES), True), ('Open', open_i, False), ('Resolved', 2, False)])}
    {filters('Search by order number or linked record', 'Search delivery issues', ('Issue Type', 'All'), ('Status', 'All'))}
    <div class="body">{table([('Reported', ''), ('Customer', ''), ('Order', ''), ('Issue Type', ''), ('Product', ''), ('Quantity or Amount', 'num'), ('Linked Record', ''), ('Status', '')], [isr], 'wrap')}
      {pager(f'Showing 1 to {len(ISSUES)} of {len(ISSUES)} issues', 1)}</div>
  </section>
'''
page('company', 'delivery-issues', 'CMP-OPS-07', 'Company Administration — Operations Manager — Delivery Issues (CMP-OPS-07)', body)

# ---------- Operational Reports ----------
cyc = ''.join(f'<tr><td>{link("CMP-ORD-02", s[1])}</td><td>{ORDER_PLACED[s[1]]}</td><td>{PROMISED[s[1]][0]}</td><td>{PROMISED[s[1]][1] or s[4]}</td><td>{s[5]}</td><td class="num">{CYCLE_DAYS[s[1]] if s[1] in CYCLE_DAYS else "—"}</td><td>{chip("On Time" if PROMISED[s[1]][0] == (PROMISED[s[1]][1] or s[4]) else "Late")}</td></tr>' for s in SHIPMENTS if s[6] != 'Being Packed')
OCT_REASON = {}
for r in RET_OCT: OCT_REASON[r[5]] = (OCT_REASON.get(r[5], (0, 0))[0] + 1, OCT_REASON.get(r[5], (0, 0))[1] + r[4])
assert sum(v[1] for v in OCT_REASON.values()) == RET_OCT_SHEETS == 65
reas = ''.join(f'<tr><td><b>{k}</b></td><td class="num">{v[0]}</td><td class="num">{v[1]}</td></tr>' for k, v in sorted(OCT_REASON.items(), key=lambda x: -x[1][1]))
acc = ''.join(f'<tr><td><b>{w}</b></td><td class="num">{N(CSTK_VAPI if "Vapi" in w else CSTK_TALOJA)}</td><td class="num">{v}</td><td class="num"><b>{(1 - v / (CSTK_VAPI if "Vapi" in w else CSTK_TALOJA)) * 100:.1f}%</b></td></tr>' for w, v in C_COUNT_VAR.items())
reason_col = ['#0a48fd', '#0b8fa8', '#e0a030', '#7a36fb']
body = f'''  <div class="head">
    <h1>Operational Reports</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('Dispatched On Time', f'{len(ON_TIME_OCT) / len(SHIP_OCT) * 100:.1f}%', chip(f'{len(ON_TIME_OCT)} of {len(SHIP_OCT)}', 'plain'))}
    {kpi('Order to Delivery', '5 <small>days</small>', chip('Delivered Orders', 'plain'))}
    {kpi('Return Rate', f'{RET_RATE:.1f}%', chip(f'{RET_OCT_SHEETS} sheets', 'plain'))}
    {kpi('Stock Count Accuracy', f'{C_COUNT_ACC * 100:.1f}%', chip('12 products', 'plain'))}
  </div>
  <div class="grid g-2">
    {card('Dispatched On Time, Percentage by Month', chart('bars', ['September', 'October'], [{'name': 'On time', 'values': [100, round(len(ON_TIME_OCT) / len(SHIP_OCT) * 100)], 'color': 'var(--ok)'}], height=260))}
    <section class="card"><header><h2>Sheets Returned by Reason</h2></header><div class="body center">{chart('donut', series=[{'name': k, 'value': v[1], 'color': c} for (k, v), c in zip(sorted(OCT_REASON.items(), key=lambda x: -x[1][1]), reason_col)], center=str(RET_OCT_SHEETS), caption='sheets')}</div></section>
  </div>
  <section class="card flush"><header><h2>Order Cycle by Order</h2></header><div class="body">{table([('Order Number', ''), ('Placed', ''), ('Promised Dispatch', ''), ('Dispatched', ''), ('Delivery', ''), ('Days to Deliver', 'num'), ('Dispatch', '')], [cyc], 'wrap')}</div></section>
  <div class="grid g-2">
    <section class="card flush"><header><h2>Returns by Reason</h2></header><div class="body">{table([('Reason', ''), ('Requests', 'num'), ('Sheets', 'num')], [reas], 'wrap', foot=f'<tfoot><tr><td>Total</td><td class="num">{len(RET_OCT)}</td><td class="num">{RET_OCT_SHEETS}</td></tr></tfoot>')}</div></section>
    <section class="card flush"><header><h2>Stock Count of 19/10/2026</h2></header><div class="body">{table([('Warehouse', ''), ('Sheets on Hand', 'num'), ('Variance', 'num'), ('Accuracy', 'num')], [acc], 'wrap')}</div></section>
  </div>
'''
page('company', 'operational-reports', 'CMP-OPS-08', 'Company Administration — Operations Manager — Operational Reports (CMP-OPS-08)', body)
