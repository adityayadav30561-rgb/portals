"""Phase 7, part A: Secondary Customer Sales and Inventory Manager (Arjun Nair, Dealer Bravo): Dashboard, Low Stock Overview, Stock Movement History,
Incoming Stock, Reorder Recommendations. Design rule: no text under page titles, no captions beside card titles, no helper sentences.
Data: docs/DATA.md "Phase 5 data", "Phase 6 data" and "Phase 7 data"."""
from data import *

SQ = chr(0x2212)
def signed(n): return f'+{n}' if n > 0 else f'{SQ}{abs(n)}' if n < 0 else '0'
def prod_cell(s, sid=None):
    name = f'<a data-link="{sid}"><b>{BY[s][1]}</b></a>' if sid else f'<b>{BY[s][1]}</b>'
    return f'<div class="prod">{sw(s)}<div>{name}</div></div>'
def cover_text(s):
    c = b_cover(s); return '—' if c is None else str(round(c))
INCOMING = [(O40['number'], O40['dispatch'], O40['sheets'], O40['value'], O40['expected'], 'In Transit', O40['lines']),
            (NEW_ORDER, '—', 210, NEW_TOTAL, '30/10/2026', 'Awaiting Confirmation', NEW_LINES)]
assert sum(i[2] for i in INCOMING) == 310 == sum(b['on_order'] for b in BSTOCK.values())
URGENT = sorted(BSTOCK, key=lambda s: (BREC[s]['action'] == 'No Order Needed', BSTOCK[s]['status'] != 'Out of Stock', b_cover(s) if b_cover(s) is not None else 0))
ORDER_NOW = [s for s in URGENT if BREC[s]['action'] != 'No Order Needed']                  # CAL, CHR, CPR, STN in urgency order
assert len(ORDER_NOW) == 4

# ---------- Dashboard ----------
recent = (f'<tr><td class="mono nowrap"><b>{PEND_ORDER["number"]}</b></td><td>{PEND_ORDER["date"]}</td><td>{link("SEC-RTL-02", RTL["CHR"][1])}</td><td class="num"><b>{M(PEND_TOTAL)}</b></td><td>{chip("Awaiting Confirmation")}</td></tr>'
          + ''.join(f'<tr><td class="mono nowrap"><b>{s["number"]}</b></td><td>{s["date"]}</td><td>{link("SEC-RTL-02", RTL[s["retailer"]][1])}</td><td class="num"><b>{M(s["value"])}</b></td><td>{chip(s["fstatus"])}</td></tr>' for s in TSALES[:5]))
req_list = ''.join(f'<li style="display:block"><b>{r[1]}</b><div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap;margin-top:.5rem"><span class="tag">{r[2]}</span>{chip(r[9])}</div></li>' for r in RREQUESTS)
inc_rows = ''.join(f'<tr><td>{link("SEC-ORD-02", i[0])}</td><td class="num">{N(i[2])}</td><td>{i[4]}</td><td>{chip(i[5])}</td></tr>' for i in INCOMING)
rec_rows = ''.join(f'<tr><td>{prod_cell(s, "SEC-INV-02")}</td><td class="mono nowrap">{s}</td><td class="num"><b>{N(BSTOCK[s]["available"])}</b></td><td class="num">{N(BSTOCK[s]["level"])}</td>'
                   f'<td class="num">{N(BREC[s]["qty"]) if BREC[s]["qty"] else "—"}</td><td>{chip(BREC[s]["action"])}</td></tr>' for s in ORDER_NOW)
inc_rows_full = ''.join(f'<tr><td>{link("SEC-ORD-02", i[0])}</td><td class="mono nowrap">{i[1]}</td><td class="num">{N(i[2])}</td><td class="num"><b>{M(i[3])}</b></td><td>{i[4]}</td><td>{chip(i[5])}</td></tr>' for i in INCOMING)
ful_donut = chart('donut', series=[{'name': 'Delivered', 'value': RSTATUS_COUNT['Delivered'], 'color': 'var(--ok)'}, {'name': 'In Transit', 'value': RSTATUS_COUNT['In Transit'], 'color': 'var(--accent)'},
                                   {'name': 'Being Packed', 'value': RSTATUS_COUNT['Being Packed'], 'color': '#e0a030'}], center='12', caption='orders')
body = f'''  <div class="head">
    <h1>Dashboard</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><a class="btn pri" data-link="SEC-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Retailer Orders This Month', str(len(TSALES)), chip(ML(630000), 'blue'))}
    {kpi(link('SEC-INV-03', 'Low Stock Products', False), str(len(BLOW)), '<span class="delta down">1 Out of Stock</span>')}
    {kpi('Incoming Stock', f'{N(310)} <small>sheets</small>', chip('1 Arriving Today', 'plain'))}
    {kpi('Pending Retailer Requests', str(len(RREQUESTS)), '<span class="delta down">2 Awaiting Your Review</span>')}
  </div>
  <div class="grid g-chart">
    {card('Retailer Orders by Week', chart('bars', [w[0] for w in WEEKS], [{'name': 'Order value', 'values': RWEEK_VALUE, 'color': 'var(--teal)'}], money=True, height=280))}
    <section class="card"><header><h2>Order Fulfilment</h2></header><div class="body center">{ful_donut}</div></section>
  </div>
  <div class="grid g-main-side" style="--side:17rem">
    <section class="card flush"><header><h2>Recent Retailer Orders</h2><a class="more" data-link="SEC-RTL-04">All retailer orders</a></header>
      <div class="body">{table([('Order Number', ''), ('Date', ''), ('Retailer', ''), ('Value', 'num'), ('Status', '')], [recent], 'wrap')}</div></section>
    <section class="card"><header><h2>Pending Retailer Requests</h2><a class="more" data-link="SEC-RTL-06">All requests</a></header>
      <div class="body"><ul class="list">{req_list}</ul>{kv([('Total Credit', ML(sum(r[6] for r in RREQUESTS)))], 'total')}</div></section>
  </div>
  <section class="card flush"><header><h2>Reorder Suggestions</h2><a class="more" data-link="SEC-INV-06">All recommendations</a></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Available', 'num'), ('Reorder Level', 'num'), ('Suggested Quantity', 'num'), ('Action', '')], [rec_rows], 'wrap')}</div></section>
  <section class="card flush"><header><h2>Incoming Stock</h2><a class="more" data-link="SEC-INV-05">Incoming stock</a></header>
    <div class="body">{table([('Order Number', ''), ('Dispatch Number', ''), ('Sheets', 'num'), ('Value', 'num'), ('Expected Arrival', ''), ('Status', '')], [inc_rows_full], 'wrap')}</div></section>
'''
page('secondary', 'sales-and-inventory-manager-dashboard', 'SEC-MGR-01', 'Secondary Customer — Sales and Inventory Manager — Dashboard (SEC-MGR-01)', body)

# ---------- Low Stock Overview ----------
low_tbl = ''
for s in ORDER_NOW:
    b = BSTOCK[s]; r = BREC[s]
    low_tbl += (f'<tr><td>{prod_cell(s, "SEC-INV-02")}</td><td class="mono nowrap">{s}</td><td class="num"><b>{N(b["available"])}</b></td><td class="num">{N(b["level"])}</td>'
                f'<td class="num">{N(b["on_order"]) if b["on_order"] else "—"}</td><td class="num">{cover_text(s)}</td><td>{chip(b["status"])}</td>'
                f'<td class="num"><b>{N(r["qty"]) if r["qty"] else "—"}</b></td><td class="num">{M(r["value"]) if r["value"] else "—"}</td></tr>\n')
arr_rows = ''.join(f'<tr><td>{link("SEC-ORD-02", i[0])}</td><td class="num">{N(i[2])}</td><td>{i[4]}</td><td>{chip(i[5])}</td></tr>' for i in INCOMING)
body = f'''  <div class="head">
    <h1>Low Stock Overview</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Low Stock</button><a class="btn pri" data-link="SEC-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Products Below Reorder Level', str(len(BLOW)), chip('3 Low Stock', 'warn'))}
    {kpi('Out of Stock', '1', '<span class="delta down">LM-STN-009</span>')}
    {kpi('Sheets Short of Reorder Level', N(BSHORT))}
    {kpi('Suggested Order Value', ML(BREC_VALUE), chip(f'{N(BREC_SHEETS)} sheets', 'plain'))}
  </div>
  <div class="grid g-main-side" style="--side:36rem">
    {card('Available Sheets Against Reorder Level', chart('bars', ORDER_NOW, [{'name': 'Available', 'values': [BSTOCK[s]['available'] for s in ORDER_NOW], 'color': 'var(--accent)'}, {'name': 'Reorder level', 'values': [BSTOCK[s]['level'] for s in ORDER_NOW], 'color': 'var(--bad)'}], height=210))}
    <section class="card flush"><header><h2>Arriving From Distributor Alpha</h2><a class="more" data-link="SEC-INV-05">Incoming stock</a></header><div class="body">{table([('Order Number', ''), ('Sheets', 'num'), ('Expected', ''), ('Status', '')], [arr_rows])}<div style="padding:.5rem 1.125rem 1rem">{kv([('Sheets Arriving', N(310))], 'total')}</div></div></section>
  </div>
  <section class="card flush">
    {tabs([('All Products', len(BLOW), True), ('Low Stock', 3, False), ('Out of Stock', 1, False)])}
    {filters('Search by product name or SKU', 'Search low stock products', ('Finish', 'All'), ('Sort by', 'Urgency'))}
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Available', 'num'), ('Reorder Level', 'num'), ('On Order', 'num'), ('Days of Cover', 'num'), ('Status', ''), ('Suggested Quantity', 'num'), ('Estimated Cost', 'num')], [low_tbl], 'wrap',
      foot=f'<tfoot><tr><td colspan="7">Total</td><td class="num">{N(BREC_SHEETS)}</td><td class="num">{M(BREC_VALUE)}</td></tr></tfoot>')}</div>
  </section>
'''
page('secondary', 'low-stock-overview', 'SEC-INV-03', 'Secondary Customer — Sales and Inventory Manager — Low Stock Overview (SEC-INV-03)', body)

# ---------- Stock Movement History ----------
mv_rows = ''.join(f'<tr><td>{m["date"]}</td><td>{chip(m["type"])}</td><td>{prod_cell(m["sku"], "SEC-INV-02")}</td><td class="mono nowrap">{m["sku"]}</td><td>{m["who"]}</td>'
                  f'<td class="mono nowrap">{m["ref"]}</td><td class="num"><b>{signed(m["sheets"])}</b></td></tr>\n' for m in BMOVES[:12])
n_type = lambda t: sum(1 for m in BMOVES if m['type'] == t)
by_prod = ''.join(f'<tr><td>{prod_cell(p[0], "SEC-INV-02")}</td><td class="mono nowrap">{p[0]}</td><td class="num">{N(B_OPENING[p[0]])}</td>'
                  f'<td class="num">{N(BMOVE_BY[p[0]]["received"]) if BMOVE_BY[p[0]]["received"] else "—"}</td><td class="num">{N(BMOVE_BY[p[0]]["sold"]) if BMOVE_BY[p[0]]["sold"] else "—"}</td>'
                  f'<td class="num">{signed(BMOVE_BY[p[0]]["adjusted"]) if BMOVE_BY[p[0]]["adjusted"] else "—"}</td><td class="num"><b>{N(BSTOCK[p[0]]["on_hand"])}</b></td></tr>' for p in P)
wk_recv = [sum(m['sheets'] for m in BMOVES if m['type'] == 'Receipt' and a <= int(m['date'][:2]) <= b) for _, a, b in WEEKS]
wk_sold = [sum(-m['sheets'] for m in BMOVES if m['type'] == 'Sale to Retailer' and a <= int(m['date'][:2]) <= b) for _, a, b in WEEKS]
assert sum(wk_recv) == 380 and sum(wk_sold) == 370
body = f'''  <div class="head">
    <h1>Stock Movement History</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Movements</button></div>
  </div>
  <div class="kpis">
    {kpi('Received From Distributor Alpha', f'{N(BM_RECV)} <small>sheets</small>', chip('5 orders', 'plain'))}
    {kpi('Sold to Retailers', f'{N(BM_SOLD)} <small>sheets</small>', chip(f'{len(TSALES)} sales', 'plain'))}
    {kpi('Stock Adjustments', f'{SQ}{abs(BADJUSTED)} <small>sheets</small>', chip(f'{len(BADJ)} adjustments', 'plain'))}
    {kpi('Sheets on Hand', N(1058))}
  </div>
  {card('Sheets Moved by Week', chart('bars', [w[0] for w in WEEKS], [{'name': 'Received from Distributor Alpha', 'values': wk_recv, 'color': 'var(--teal)'}, {'name': 'Sold to retailers', 'values': wk_sold, 'color': 'var(--accent)'}], height=260))}
  <section class="card flush">
    {tabs([('All Movements', len(BMOVES), True), ('Receipts', n_type('Receipt'), False), ('Sales to Retailers', n_type('Sale to Retailer'), False), ('Adjustments', n_type('Stock Adjustment'), False)])}
    {filters('Search by product, retailer or reference', 'Search stock movements', ('Date Range', 'October 2026'), ('Product', 'All'), ('Type', 'All'))}
    <div class="body">{table([('Date', ''), ('Type', ''), ('Product', ''), ('SKU', ''), ('Name or Reason', ''), ('Reference', ''), ('Sheets', 'num')], [mv_rows])}
      {pager(f'Showing 1 to 12 of {len(BMOVES)} movements', 6)}</div>
  </section>
  <section class="card flush"><header><h2>Movement by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Opening Stock', 'num'), ('Received', 'num'), ('Sold to Retailers', 'num'), ('Adjusted', 'num'), ('On Hand Now', 'num')], [by_prod],
      foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(sum(B_OPENING.values()))}</td><td class="num">{N(BM_RECV)}</td><td class="num">{N(BM_SOLD)}</td><td class="num">{signed(BADJUSTED)}</td><td class="num">{N(1058)}</td></tr></tfoot>')}</div></section>
'''
page('secondary', 'stock-movement-history', 'SEC-INV-04', 'Secondary Customer — Sales and Inventory Manager — Stock Movement History (SEC-INV-04)', body)

# ---------- Incoming Stock ----------
ship_rows = ''
for i in INCOMING:
    act = '<button class="btn sm pri" type="button">Receive Shipment</button>' if i[5] == 'In Transit' else ''
    ship_rows += (f'<tr><td>{link("SEC-ORD-02", i[0])}</td><td class="mono nowrap">{i[1]}</td><td class="num">{N(i[2])}</td><td class="num"><b>{M(i[3])}</b></td><td>{i[4]}</td><td>{chip(i[5])}</td><td><div class="row-actions">{act}</div></td></tr>')
arr_prod = ''
for s in BSTOCK:
    b = BSTOCK[s]
    if not b['on_order']: continue
    a40 = dict(O40['lines']).get(s, 0); a42 = dict(NEW_LINES).get(s, 0); after = b['available'] + b['on_order']
    arr_prod += (f'<tr><td>{prod_cell(s, "SEC-INV-02")}</td><td class="mono nowrap">{s}</td><td class="num">{N(b["available"])}</td><td class="num">{N(a40) if a40 else "—"}</td><td class="num">{N(a42) if a42 else "—"}</td>'
                 f'<td class="num"><b>{N(after)}</b></td><td>{chip("In Stock" if after >= b["level"] else "Low Stock")}</td></tr>')
rec_hist = ''.join(f'<tr><td>{link("SEC-ORD-02", s["number"])}</td><td>{s["expected"]}</td><td class="num">{N(s["sheets"])}</td><td class="num">{M(s["value"])}</td></tr>' for s in BRV_SALES if s['status'] == 'Delivered')
assert sum(1 for s in BRV_SALES if s['status'] == 'Delivered') == 5
body = f'''  <div class="head">
    <h1>Incoming Stock</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Shipments</button><a class="btn pri" data-link="SEC-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Shipments Arriving', str(len(INCOMING)))}
    {kpi('Sheets Arriving', f'{N(310)} <small>sheets</small>')}
    {kpi('Arriving Today', f'{N(O40["sheets"])} <small>sheets</small>', chip(O40['number'], 'blue'))}
    {kpi('Value Arriving', ML(sum(i[3] for i in INCOMING)), chip('GST Included', 'plain'))}
  </div>
  <section class="card flush"><header><h2>Shipments From Distributor Alpha</h2></header>
    <div class="body">{table([('Order Number', ''), ('Dispatch Number', ''), ('Sheets', 'num'), ('Value', 'num'), ('Expected Arrival', ''), ('Status', ''), ('', '')], [ship_rows])}</div></section>
  <section class="card flush"><header><h2>Arriving by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Available Now', 'num'), ('Arriving Today', 'num'), ('Arriving 30 October', 'num'), ('Available After Both', 'num'), ('Status After Arrival', '')], [arr_prod], 'wrap',
      foot=f'<tfoot><tr><td colspan="3">Total</td><td class="num">{N(O40["sheets"])}</td><td class="num">{N(210)}</td><td colspan="2"></td></tr></tfoot>')}</div></section>
  <div class="grid g-2">
    {card('Arriving Today', kv([('Order Number', f'<span class="mono">{O40["number"]}</span>'), ('Dispatch Number', f'<span class="mono">{O40["dispatch"]}</span>'), ('Dispatched', '24/10/2026 17:45'), ('Deliver To', 'Shop and Godown, Hadapsar, Pune'),
                                  ('Vehicle', 'MH 12 QR 4418'), ('Driver', 'Santosh Gaikwad'), ('Driver Phone', '+91 90000 12346')]))}
    <section class="card flush"><header><h2>Recent Receipts</h2></header><div class="body">{table([('Order Number', ''), ('Received', ''), ('Sheets', 'num'), ('Value', 'num')], [rec_hist])}</div></section>
  </div>
'''
page('secondary', 'incoming-stock', 'SEC-INV-05', 'Secondary Customer — Sales and Inventory Manager — Incoming Stock (SEC-INV-05)', body)

# ---------- Reorder Recommendations ----------
rec_tbl = ''
for s in URGENT:
    b = BSTOCK[s]; r = BREC[s]
    rec_tbl += (f'<tr><td>{prod_cell(s, "SEC-INV-02")}</td><td class="num"><b>{N(b["available"])}</b></td><td class="num">{N(b["on_order"]) if b["on_order"] else "—"}</td><td class="num">{N(b["level"])}</td>'
                f'<td class="num">{N(TSOLD[s]) if TSOLD[s] else "—"}</td><td class="num">{cover_text(s)}</td><td class="num">{N(BY[s][10]) if BY[s][10] else "—"}</td>'
                f'<td class="num"><b>{N(r["qty"]) if r["qty"] else "—"}</b></td><td class="num">{M(r["value"]) if r["value"] else "—"}</td><td>{chip(r["action"])}</td></tr>\n')
shortest = min((s for s in BSTOCK if TSOLD[s]), key=b_cover)
assert shortest == 'LM-CHR-007'
body = f'''  <div class="head">
    <h1>Reorder Recommendations</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Recommendations</button><a class="btn pri" data-link="SEC-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Products to Reorder', str(sum(1 for r in BREC.values() if r['action'] == 'Order Now')), chip('1 Not Available', 'bad'))}
    {kpi('Suggested Sheets', N(BREC_SHEETS))}
    {kpi('Estimated Cost', ML(BREC_VALUE), chip('Before GST', 'plain'))}
    {kpi('Shortest Days of Cover', f'{round(b_cover(shortest))} <small>days</small>', chip(shortest, 'warn'))}
  </div>
  {card('Available Sheets and October Sales by Product', chart('bars', list(BSTOCK), [{'name': 'Available', 'values': [BSTOCK[s]['available'] for s in BSTOCK], 'color': 'var(--accent)'}, {'name': 'Sold to retailers in October', 'values': [TSOLD[s] for s in BSTOCK], 'color': 'var(--teal)'}], height=260))}
  <section class="card flush">
    {tabs([('All Products', 12, True), ('Order Now', 3, False), ('Out at Distributor Alpha', 1, False), ('No Order Needed', 8, False)])}
    {filters('Search by product name or SKU', 'Search recommendations', ('Finish', 'All'), ('Action', 'All'))}
    <div class="body">{table([('Product', ''), ('Available', 'num'), ('On Order', 'num'), ('Reorder Level', 'num'), ('Sold in October', 'num'), ('Days of Cover', 'num'), ('Distributor Alpha Stock', 'num'), ('Suggested Quantity', 'num'), ('Estimated Cost', 'num'), ('Action', '')], [rec_tbl], 'wrap tight',
      foot=f'<tfoot><tr><td colspan="7">Total</td><td class="num">{N(BREC_SHEETS)}</td><td class="num">{M(BREC_VALUE)}</td><td></td></tr></tfoot>')}</div>
  </section>
'''
page('secondary', 'reorder-recommendations', 'SEC-INV-06', 'Secondary Customer — Sales and Inventory Manager — Reorder Recommendations (SEC-INV-06)', body)
