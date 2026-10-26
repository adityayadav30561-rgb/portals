"""Phase 8, part B: Tertiary Customer Retailer Owner (shared with the Executives via ?role=SLS / ?role=PUR): Order History, Order Details, My Inventory,
Inventory Item Details, Stock Movement History, Reorder Recommendations, Purchase History. Retailer Charlie, Camp, Pune; supplier Dealer Bravo.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md "Phase 8 data"."""
from data import *

SQ = chr(0x2212)
def signed(n): return f'+{n}' if n > 0 else f'{SQ}{abs(n)}' if n < 0 else '0'
def prod_cell(s, sid=None):
    name = f'<a data-link="{sid}"><b>{BY[s][1]}</b></a>' if sid else f'<b>{BY[s][1]}</b>'
    return f'<div class="prod">{sw(s)}<div>{name}</div></div>'
def cover_text(s):
    c = c_cover(s); return '—' if c is None else str(round(c))
NO_ORDER = 'data-role="OWN PUR"'
INCOMING = [(O12['number'], O12['delivery'], O12['sheets'], O12['value'], O12['expected'], 'Being Packed'),
            (PEND_ORDER['number'], '—', PEND_SHEETS, PEND_TOTAL, PEND_ORDER['requested'], 'Awaiting Confirmation')]
assert sum(i[2] for i in INCOMING) == 100 == sum(b['on_order'] for b in CSTOCK.values())
URGENT = sorted(CSTOCK, key=lambda s: (CREC[s]['action'] == 'No Order Needed', CSTOCK[s]['status'] != 'Out of Stock', c_cover(s) if c_cover(s) is not None else 0))

# ---------- Order History ----------
rows = ''.join(f'<tr><td><a data-link="TER-ORD-02"><b>{o}</b></a></td><td>{d}</td><td class="num">{N(sh)}</td><td class="num"><b>{M(v)}</b></td><td>{dl}</td><td>{chip(st)}</td><td>{pay_chip(pay)}</td><td><div class="row-actions"><a class="btn sm" data-link="TER-ORD-02">View</a></div></td></tr>\n' for o, d, sh, v, dl, st, pay in CHR_ORDERS)
body = f'''  <div class="head">
    <h1>Order History</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Orders</button><a class="btn pri" data-link="TER-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Orders This Month', '5')}
    {kpi('Order Value This Month', ML(264000), up(pct(264000, 240000)))}
    {kpi('Being Packed', '1')}
    {kpi('Awaiting Confirmation', '1')}
  </div>
  <section class="card flush">
    {tabs([('All Orders', C_ORDER_TOTAL, True), ('Awaiting Confirmation', 1, False), ('Being Packed', 1, False), ('Delivered', C_ORDER_COUNT['delivered'], False), ('Cancelled', 2, False)])}
    {filters('Search by order number or product', 'Search orders', ('Date Range', 'Last 90 days'), ('Payment', 'All'), ('Status', 'All'))}
    <div class="body">{table([('Order Number', ''), ('Order Date', ''), ('Sheets', 'num'), ('Value', 'num'), ('Delivery Date', ''), ('Order Status', ''), ('Payment', ''), ('', '')], [rows], 'wrap')}
      {pager(f'Showing 1 to 10 of {C_ORDER_TOTAL} orders')}</div>
  </section>
'''
page('tertiary', 'order-history', 'TER-ORD-01', 'Tertiary Customer — Retailer Owner — Order History (TER-ORD-01)', body)

# ---------- Order Details (TSL-2026-0412) ----------
o = O12
lrows = ''.join(f'<tr><td><div class="prod">{sw(k)}<div><b>{BY[k][1]}</b></div></div></td><td class="mono nowrap">{k}</td><td class="num">{N(q)}</td><td class="num"><b>{M(O12_AMT[k])}</b></td></tr>' for k, q in o['lines'])
body = f'''  <div class="head">
    <div class="title-row"><h1>{o["number"]}</h1>{chip("Being Packed")}{pay_chip("Unpaid")}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Order Copy</button><a class="btn" data-link="TER-SUP-02" data-role="OWN"><i data-icon="help"></i>Raise Support Ticket</a><button class="btn pri" type="button" {NO_ORDER}><i data-icon="repeat"></i>Reorder</button></div>
  </div>
  <section class="card pad"><ol class="track">
    <li class="done"><i></i><b>Placed</b><span>25/10/2026 16:50</span></li><li class="done"><i></i><b>Confirmed</b><span>25/10/2026 17:20</span></li><li class="now"><i></i><b>Being Packed</b><span>26/10/2026</span></li>
    <li class="todo"><i></i><b>In Transit</b><span>26/10/2026</span></li><li class="todo"><i></i><b>Delivered</b><span>{o["expected"]}</span></li></ol></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      <section class="card flush"><header><h2>Items</h2></header>
        <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Amount', 'num')], [lrows], foot=f'<tfoot><tr><td colspan="3">Taxable Amount</td><td class="num">{M(O12_TAX)}</td></tr></tfoot>')}
          <div style="padding:1rem 1.125rem"><dl class="kv" style="max-width:22rem;margin-left:auto"><dt>Central GST 9%</dt><dd>{M(O12_GST)}</dd><dt>State GST 9%</dt><dd>{M(O12_GST)}</dd></dl>
          <dl class="kv total" style="max-width:22rem;margin-left:auto"><dt>Total</dt><dd>{M(o["value"])}</dd></dl></div></div></section>
      <section class="card flush"><header><h2>Order Activity</h2></header><div class="body">{table([('Date', ''), ('Event', ''), ('By', '')], [
        '<tr><td class="nowrap">26/10/2026 10:15</td><td><b>Packing started</b></td><td>Hadapsar Godown</td></tr>',
        '<tr><td class="nowrap">25/10/2026 17:20</td><td><b>Order confirmed and sale recorded</b></td><td>Dealer Bravo</td></tr>',
        '<tr><td class="nowrap">25/10/2026 16:50</td><td><b>Order placed</b></td><td>Imran Sheikh</td></tr>'])}</div></section>
    </div>
    <div class="stack">
      {card('Delivery', kv([('Delivery Number', f'<span class="mono">{o["delivery"]}</span>'), ('Deliver To', 'Shop 12, MG Road, Camp, Pune'), ('Expected', o['expected']), ('Dispatched From', 'Hadapsar Godown'), ('Vehicle', o['vehicle'][0]), ('Driver', o['vehicle'][2]), ('Driver Phone', o['vehicle'][3])]))}
      <section class="card"><header><h2>Invoice</h2></header><div class="body">{kv([('Invoice Number', f'<span class="mono">{o["number"]}</span>'), ('Issued', '25/10/2026'), ('Due', '09/11/2026'), ('Amount', f'<b>{M(o["value"])}</b>'), ('Status', chip('Unpaid'))])}
        <a class="btn block" data-link="TER-BIL-02" data-role="OWN" style="margin-top:1rem">View Invoice</a></div></section>
      {card('Order Information', kv([('Placed By', 'Imran Sheikh'), ('Payment Terms', '15 days'), ('Transport', 'Dealer Transport'), ('Offer', 'Retailer Festive Volume Rebate'), ('Reference Number', 'CL-2026-118')]))}
    </div>
  </div>
'''
page('tertiary', 'order-details', 'TER-ORD-02', 'Tertiary Customer — Retailer Owner — Order Details (TER-ORD-02)', body)

# ---------- My Inventory (shared with both Executives) ----------
def stock_bar(s):
    b = CSTOCK[s]; pct_ = 0 if b['on_hand'] == 0 else min(100, round(b['on_hand'] / (b['level'] * 3) * 100))
    return pct_
inv_rows = ''.join(f'''<tr><td><div class="prod">{sw(p[0])}<div><a data-link="TER-INV-02"><b>{p[1]}</b></a></div></div></td><td class="mono nowrap">{p[0]}</td>
      <td class="num">{N(CSTOCK[p[0]]["on_hand"])}</td><td class="num">{N(CSTOCK[p[0]]["reserved"])}</td><td class="num"><b>{N(CSTOCK[p[0]]["available"])}</b></td><td class="num">{N(CSTOCK[p[0]]["on_order"]) if CSTOCK[p[0]]["on_order"] else "—"}</td><td class="num">{N(CSTOCK[p[0]]["level"])}</td><td>{chip(CSTOCK[p[0]]["status"])}</td></tr>
''' for p in P)
ship_rows = ''.join(f'<tr><td><a data-link="TER-ORD-02"><b>{i[0]}</b></a></td><td class="num">{N(i[2])}</td><td>{i[4]}</td><td>{chip(i[5])}</td></tr>' for i in INCOMING)
n_in = sum(1 for b in CSTOCK.values() if b['status'] == 'In Stock')
body = f'''  <div class="head">
    <h1>My Inventory</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Stock</button><a class="btn pri" data-link="TER-ORD-03" {NO_ORDER}><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Sheets on Hand', N(216))}
    {kpi('Stock Value', ML(CSTOCK_VALUE))}
    {kpi('Reserved for Customers', f'{N(27)} <small>sheets</small>')}
    {kpi('Arriving From Dealer Bravo', f'{N(100)} <small>sheets</small>')}
  </div>
  <div class="grid g-2" style="--cols:.8fr 1.2fr">
    <section class="card"><header><h2>Stock Health</h2></header><div class="body center">{chart('donut', series=[{'name': 'In Stock', 'value': n_in, 'color': 'var(--ok)'}, {'name': 'Low Stock', 'value': 3, 'color': '#e0a030'}, {'name': 'Out of Stock', 'value': 1, 'color': 'var(--bad)'}], center='12', caption='products')}</div></section>
    <section class="card flush"><header><h2>Incoming Shipments</h2></header><div class="body">{table([('Order', ''), ('Sheets', 'num'), ('Expected', ''), ('Status', '')], [ship_rows], 'wrap')}<div style="padding:.5rem 1.125rem 1rem">{kv([('Sheets Arriving', '100')], 'total')}</div></div></section>
  </div>
  <section class="card flush">
    {tabs([('All Products', 12, True), ('In Stock', n_in, False), ('Low Stock', 3, False), ('Out of Stock', 1, False)])}
    {filters('Search by product name or SKU', 'Search stock', ('Finish', 'All'), ('Thickness', 'All'))}
    <div class="body">{table([('Product', ''), ('SKU', ''), ('On Hand', 'num'), ('Reserved', 'num'), ('Available', 'num'), ('On Order', 'num'), ('Reorder Level', 'num'), ('Status', '')], [inv_rows], 'wrap')}</div></section>
'''
page('tertiary', 'my-inventory', 'TER-INV-01', 'Tertiary Customer — Retailer Owner — My Inventory (TER-INV-01)', body)

# ---------- Inventory Item Details (LM-CAL-003) ----------
sku = 'LM-CAL-003'; p = BY[sku]; b = CSTOCK[sku]
mv = [m for m in CMOVES if m['sku'] == sku]
_bal = b['on_hand']
for m in mv: m['balance'] = _bal; _bal -= m['sheets']
assert _bal == C_OPENING[sku]
def bal_on(day):                                                                       # closing balance at the end of a day of October
    x = C_OPENING[sku]
    for m in reversed(mv):
        if pd(m['date']) <= pd(day): x += m['sheets']
    return x
dates = ['27/07/2026', '03/08/2026', '10/08/2026', '17/08/2026', '24/08/2026', '31/08/2026', '07/09/2026', '14/09/2026', '21/09/2026', '28/09/2026', '05/10/2026', '12/10/2026', '19/10/2026', '26/10/2026']
levels = [30, 26, 22, 28, 24, 20, 26, 22, 18, 16] + [bal_on(d) for d in dates[10:]]
assert levels[-1] == b['on_hand']
mv_rows = ''.join(f'<tr><td>{m["date"]}</td><td>{chip(m["type"])}</td><td>{m["who"]}</td><td class="mono nowrap">{m["ref"]}</td><td class="num"><b>{signed(m["sheets"])}</b></td><td class="num">{N(m["balance"])}</td></tr>' for m in mv)
sold_cal = CSOLD[sku]; cover = round(b['available'] / (sold_cal / 26))
assert CREORDER_QTY[sku] == 25 == CREC[sku]['qty'] and cover == 13
body = f'''  <div class="head">
    <div class="title-row"><h1>{p[1]}</h1>{chip(b["status"])}</div>
    <div class="acts"><a class="btn" data-link="TER-CAT-02"><i data-icon="box"></i>View Product</a><a class="btn pri" data-link="TER-ORD-03" {NO_ORDER}><i data-icon="plus"></i>Reorder</a></div>
  </div>
  <div class="kpis">
    {kpi('On Hand', f'{b["on_hand"]} <small>sheets</small>')}
    {kpi('Reserved for Customers', f'{b["reserved"]} <small>sheets</small>')}
    {kpi('Available', f'{b["available"]} <small>sheets</small>', '<span class="delta down">Below Reorder Level</span>')}
    {kpi('On Order', f'{b["on_order"]} <small>sheets</small>', f'<span class="delta flat">Arriving {O12["expected"]}</span>')}
    {kpi('Days of Cover', f'{cover} <small>days</small>')}
  </div>
  <div class="grid g-main-side" style="--side:19rem">
    <div class="stack">
      {card('Stock Level', chart('line', dates, [{'name': 'Sheets on hand', 'values': levels, 'color': 'var(--accent)'}, {'name': 'Reorder level', 'values': [b['level']] * 14, 'color': 'var(--bad)', 'dots': False}], area=True))}
      <section class="card flush"><header><h2>Stock Movements</h2><a class="more" data-link="TER-INV-03" {NO_ORDER}>Stock movement history</a></header>
        <div class="body">{table([('Date', ''), ('Type', ''), ('Customer or Dealer', ''), ('Reference', ''), ('Sheets', 'num'), ('Balance', 'num')], [mv_rows], 'wrap')}</div></section>
    </div>
    <div class="stack">
      <section class="card pad" style="display:grid;gap:1rem">{sw(sku, 'lg', 'aspect-ratio:16/9')}{kv([('SKU', f'<span class="mono">{sku}</span>'), ('Finish', p[2]), ('Thickness', p[3]), ('Sheet Size', '8 ft × 4 ft')])}</section>
      <section class="card flush"><header><h2>Batches</h2></header><div class="body">{table([('Batch', ''), ('Received', ''), ('Sheets', 'num')], ['<tr><td class="mono">B-2610-31</td><td>13/10/2026</td><td class="num">8</td></tr>', '<tr><td class="mono">B-2609-26</td><td>30/09/2026</td><td class="num">1</td></tr>'])}</div></section>
      <section class="card"><header><h2>Reorder Settings</h2><button class="btn sm" type="button" style="margin-left:auto"><i data-icon="edit"></i>Edit</button></header><div class="body">{kv([('Reorder Level', f'{b["level"]} sheets'), ('Reorder Quantity', f'{CREORDER_QTY[sku]} sheets'), ('Lead Time', '2 days'), ('Preferred Location', 'Shop, Camp')])}</div></section>
    </div>
  </div>
'''
page('tertiary', 'inventory-item-details', 'TER-INV-02', 'Tertiary Customer — Retailer Owner — Inventory Item Details (TER-INV-02)', body)

# ---------- Stock Movement History ----------
mv_rows = ''.join(f'<tr><td>{m["date"]}</td><td>{chip(m["type"])}</td><td>{prod_cell(m["sku"], "TER-INV-02")}</td><td class="mono nowrap">{m["sku"]}</td><td>{m["who"]}</td>'
                  f'<td class="mono nowrap">{m["ref"]}</td><td class="num"><b>{signed(m["sheets"])}</b></td></tr>\n' for m in CMOVES[:12])
n_type = lambda t: sum(1 for m in CMOVES if m['type'] == t)
by_prod = ''.join(f'<tr><td>{prod_cell(p[0], "TER-INV-02")}</td><td class="mono nowrap">{p[0]}</td><td class="num">{N(C_OPENING[p[0]])}</td>'
                  f'<td class="num">{N(CMOVE_BY[p[0]]["received"]) if CMOVE_BY[p[0]]["received"] else "—"}</td><td class="num">{N(CMOVE_BY[p[0]]["sold"]) if CMOVE_BY[p[0]]["sold"] else "—"}</td>'
                  f'<td class="num">{signed(CMOVE_BY[p[0]]["adjusted"]) if CMOVE_BY[p[0]]["adjusted"] else "—"}</td><td class="num"><b>{N(CSTOCK[p[0]]["on_hand"])}</b></td></tr>' for p in P)
wk_recv = [sum(m['sheets'] for m in CMOVES if m['type'] == 'Receipt' and a <= int(m['date'][:2]) <= b_) for _, a, b_ in WEEKS]
wk_sold = [sum(-m['sheets'] for m in CMOVES if m['type'] == 'Retail Sale' and a <= int(m['date'][:2]) <= b_) for _, a, b_ in WEEKS]
assert sum(wk_recv) == 120 and sum(wk_sold) == 163 and sum(C_OPENING.values()) == 261
body = f'''  <div class="head">
    <h1>Stock Movement History</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Movements</button></div>
  </div>
  <div class="kpis">
    {kpi('Received From Dealer Bravo', f'{N(120)} <small>sheets</small>', chip('4 orders', 'plain'))}
    {kpi('Sold to Customers', f'{N(163)} <small>sheets</small>', chip(f'{len(CSALES)} sales', 'plain'))}
    {kpi('Stock Adjustments', f'{SQ}{abs(CADJUSTED)} <small>sheets</small>', chip(f'{len(CADJ)} adjustments', 'plain'))}
    {kpi('Sheets on Hand', N(216))}
  </div>
  {card('Sheets Moved by Week', chart('bars', [w[0] for w in WEEKS], [{'name': 'Received from Dealer Bravo', 'values': wk_recv, 'color': 'var(--teal)'}, {'name': 'Sold to customers', 'values': wk_sold, 'color': 'var(--accent)'}], height=260))}
  <section class="card flush">
    {tabs([('All Movements', len(CMOVES), True), ('Receipts', n_type('Receipt'), False), ('Sales to Customers', n_type('Retail Sale'), False), ('Adjustments', n_type('Stock Adjustment'), False)])}
    {filters('Search by product, customer or reference', 'Search stock movements', ('Date Range', 'October 2026'), ('Product', 'All'), ('Type', 'All'))}
    <div class="body">{table([('Date', ''), ('Type', ''), ('Product', ''), ('SKU', ''), ('Name or Reason', ''), ('Reference', ''), ('Sheets', 'num')], [mv_rows], 'wrap')}
      {pager(f'Showing 1 to 12 of {len(CMOVES)} movements', 7)}</div>
  </section>
  <section class="card flush"><header><h2>Movement by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Opening Stock', 'num'), ('Received', 'num'), ('Sold to Customers', 'num'), ('Adjusted', 'num'), ('On Hand Now', 'num')], [by_prod], 'wrap',
      foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(261)}</td><td class="num">{N(120)}</td><td class="num">{N(163)}</td><td class="num">{signed(CADJUSTED)}</td><td class="num">{N(216)}</td></tr></tfoot>')}</div></section>
'''
page('tertiary', 'stock-movement-history', 'TER-INV-03', 'Tertiary Customer — Retailer Owner — Stock Movement History (TER-INV-03)', body)

# ---------- Reorder Recommendations ----------
rec_tbl = ''
for s in URGENT:
    b = CSTOCK[s]; r = CREC[s]
    rec_tbl += (f'<tr><td>{prod_cell(s, "TER-INV-02")}</td><td class="num"><b>{N(b["available"])}</b></td><td class="num">{N(b["on_order"]) if b["on_order"] else "—"}</td><td class="num">{N(b["level"])}</td>'
                f'<td class="num">{N(CSOLD[s]) if CSOLD[s] else "—"}</td><td class="num">{cover_text(s)}</td><td class="num">{N(BSTOCK[s]["available"]) if BSTOCK[s]["available"] else "—"}</td>'
                f'<td class="num"><b>{N(r["qty"]) if r["qty"] else "—"}</b></td><td class="num">{M(r["value"]) if r["value"] else "—"}</td><td>{chip(r["action"])}</td></tr>\n')
shortest = min((s for s in CSTOCK if CSOLD[s]), key=c_cover)
body = f'''  <div class="head">
    <h1>Reorder Recommendations</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Recommendations</button><a class="btn pri" data-link="TER-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Products to Reorder', str(sum(1 for r in CREC.values() if r['action'] == 'Order Now')), chip('1 Not Available', 'bad'))}
    {kpi('Suggested Sheets', N(CREC_SHEETS))}
    {kpi('Estimated Cost', ML(CREC_VALUE), chip('Before GST', 'plain'))}
    {kpi('Shortest Days of Cover', f'{round(c_cover(shortest))} <small>days</small>', chip(shortest, 'warn'))}
  </div>
  {card('Available Sheets and October Sales by Product', chart('bars', list(CSTOCK), [{'name': 'Available', 'values': [CSTOCK[s]['available'] for s in CSTOCK], 'color': 'var(--accent)'}, {'name': 'Sold to customers in October', 'values': [CSOLD[s] for s in CSTOCK], 'color': 'var(--teal)'}], height=260))}
  <section class="card flush">
    {tabs([('All Products', 12, True), ('Order Now', 3, False), ('Out at Dealer Bravo', 1, False), ('No Order Needed', 8, False)])}
    {filters('Search by product name or SKU', 'Search recommendations', ('Finish', 'All'), ('Action', 'All'))}
    <div class="body">{table([('Product', ''), ('Available', 'num'), ('On Order', 'num'), ('Reorder Level', 'num'), ('Sold in October', 'num'), ('Days of Cover', 'num'), ('Dealer Bravo Stock', 'num'), ('Suggested Quantity', 'num'), ('Estimated Cost', 'num'), ('Action', '')], [rec_tbl], 'wrap tight',
      foot=f'<tfoot><tr><td colspan="7">Total</td><td class="num">{N(CREC_SHEETS)}</td><td class="num">{M(CREC_VALUE)}</td><td></td></tr></tfoot>')}</div>
  </section>
'''
page('tertiary', 'reorder-recommendations', 'TER-INV-04', 'Tertiary Customer — Retailer Owner — Reorder Recommendations (TER-INV-04)', body)

# ---------- Purchase History ----------
by_prod = sorted(CBOUGHT, key=lambda s: -CBOUGHT_VALUE[s])
pp_rows = ''.join(f'<tr><td>{prod_cell(s, "TER-CAT-02")}</td><td class="mono nowrap">{s}</td><td class="num">{N(CBOUGHT[s])}</td><td class="num"><b>{M(CBOUGHT_VALUE[s])}</b></td></tr>' for s in by_prod)
inv_rows = ''.join(f'<tr><td><a data-link="TER-ORD-02"><b>{o}</b></a></td><td>{d}</td><td class="num">{N(sh)}</td><td class="num"><b>{M(v)}</b></td><td>{pay_chip(pay)}</td></tr>' for o, d, sh, v, dl, st, pay in CHR_ORDERS[1:])
body = f'''  <div class="head">
    <h1>Purchase History</h1>
    <div class="acts"><span class="sel"><small>Period</small> May to October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Purchases</button></div>
  </div>
  <div class="kpis">
    {kpi('Purchases This Month', ML(264000), up(pct(264000, 240000)))}
    {kpi('Purchases in Six Months', ML(sum(CHR_BUY_MONTH)))}
    {kpi('Sheets This Month', N(155))}
    {kpi('Average Order Value', M(264000 // 5), chip('5 orders', 'plain'))}
  </div>
  {card('Purchases by Month', chart('bars', MONTHS, [{'name': 'Purchases from Dealer Bravo', 'values': CHR_BUY_MONTH, 'color': 'var(--accent)'}], money=True, height=280))}
  <div class="grid g-2" style="--cols:.47fr .53fr">
    <section class="card flush"><header><h2>Purchases by Product in October</h2></header>
      <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Value', 'num')], [pp_rows], 'wrap tight', foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(155)}</td><td class="num">{M(264000)}</td></tr></tfoot>')}</div></section>
    <section class="card flush"><header><h2>Invoices</h2></header>
      <div class="body">{table([('Invoice Number', ''), ('Date', ''), ('Sheets', 'num'), ('Value', 'num'), ('Payment', '')], [inv_rows], 'wrap')}</div></section>
  </div>
'''
page('tertiary', 'purchase-history', 'TER-BIL-04', 'Tertiary Customer — Retailer Owner — Purchase History (TER-BIL-04)', body)
