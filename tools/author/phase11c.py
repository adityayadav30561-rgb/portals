"""Phase 11, part C: Company Administration: Order Management (Super Admin) and Order Details (Super Admin and Operations Manager).
Order Details shows ORD-2026-10459, confirmed and ready for packing; each role sees its own actions. Data: docs/DATA.md "Phase 11 data"."""
from data import *

# ---------- Order Management ----------
chain = [('Primary', 'Crestline Laminates', 'Distributor Alpha', ORDERS_BY_TIER['Primary'], VALUE_BY_TIER['Primary']),
         ('Secondary', 'Distributor Alpha', f'{CUS_TYPE["Dealer"]} Dealers', ORDERS_BY_TIER['Secondary'], VALUE_BY_TIER['Secondary']),
         ('Tertiary', f'{CUS_TYPE["Dealer"]} Dealers', f'{CUS_TYPE["Retailer"]} Retailers', ORDERS_BY_TIER['Tertiary'], VALUE_BY_TIER['Tertiary'])]
chain_rows = ''.join(f'<tr><td><b>{t}</b></td><td>{s}</td><td>{b}</td><td class="num">{n}</td><td class="num"><b>{M(v)}</b></td><td class="num">1</td></tr>' for t, s, b, n, v in chain)
chain_foot = f'<tfoot><tr><td colspan="3">Total</td><td class="num">{ORDERS_ALL}</td><td class="num">{M(sum(c[4] for c in chain))}</td><td class="num">3</td></tr></tfoot>'
AW_DATE = {'ORD-2026-10482': '26/10/2026', NEW_ORDER: '26/10/2026', PEND_ORDER['number']: '26/10/2026'}
aw_rows = ''.join(f'<tr><td class="mono nowrap"><b>{o[0]}</b></td><td>{o[1]}</td><td>{o[3]}</td><td>{o[2]}</td><td>{AW_DATE[o[0]]}</td><td class="num"><b>{M(o[4])}</b></td></tr>' for o in AWAITING)
aw_foot = f'<tfoot><tr><td colspan="5">Total</td><td class="num">{M(sum(o[4] for o in AWAITING))}</td></tr></tfoot>'
prim = ''.join(f'<tr><td class="nowrap">{link("CMP-ORD-02", o[0])}</td><td>Distributor Alpha</td><td>{o[1]}</td><td class="num">{N(o[2])}</td><td class="num"><b>{M(o[3])}</b></td><td>{o[4]}</td><td>{chip(o[5])}</td><td>{chip(o[6])}</td></tr>' for o in ALPHA_ORDERS[:6])
prim_foot = f'<tfoot><tr><td colspan="3">Total</td><td class="num">{N(sum(o[2] for o in ALPHA_ORDERS[:6]))}</td><td class="num">{M(sum(o[3] for o in ALPHA_ORDERS[:6]))}</td><td colspan="3"></td></tr></tfoot>'
body = f'''  <div class="head">
    <h1>Order Management</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Orders</button></div>
  </div>
  <div class="kpis">
    {kpi('Orders This Month', str(ORDERS_ALL), chip('3 Awaiting Confirmation', 'warn'))}
    {kpi('Primary Orders', str(ORDERS_BY_TIER['Primary']), chip(ML(VALUE_BY_TIER['Primary']), 'plain'))}
    {kpi('Secondary Orders', str(ORDERS_BY_TIER['Secondary']), chip(ML(VALUE_BY_TIER['Secondary']), 'plain'))}
    {kpi('Tertiary Orders', str(ORDERS_BY_TIER['Tertiary']), chip(ML(VALUE_BY_TIER['Tertiary']), 'plain'))}
  </div>
  <div class="stack">
    <section class="card flush"><header><h2>Orders by Tier</h2></header><div class="body">{table([('Tier', ''), ('Seller', ''), ('Buyer', ''), ('Orders', 'num'), ('Value', 'num'), ('Awaiting', 'num')], [chain_rows], 'wrap', foot=chain_foot)}</div></section>
    <section class="card flush"><header><h2>Awaiting Confirmation</h2></header><div class="body">{table([('Order Number', ''), ('Tier', ''), ('Seller', ''), ('Buyer', ''), ('Order Date', ''), ('Value', 'num')], [aw_rows], 'wrap', foot=aw_foot)}</div></section>
  </div>
  <section class="card flush">
    {tabs([('Primary Orders', ORDERS_BY_TIER['Primary'], True), ('Secondary Orders', ORDERS_BY_TIER['Secondary'], False), ('Tertiary Orders', ORDERS_BY_TIER['Tertiary'], False)])}
    {filters('Search by order number or customer', 'Search orders', ('Status', 'All'), ('Payment', 'All'), ('Sort by', 'Order Date'))}
    <div class="body">{table([('Order Number', ''), ('Customer', ''), ('Order Date', ''), ('Sheets', 'num'), ('Value', 'num'), ('Delivery Date', ''), ('Order Status', ''), ('Payment', '')], [prim], 'wrap', foot=prim_foot)}
      {pager(f'Showing 1 to {ORDERS_BY_TIER["Primary"]} of {ORDERS_BY_TIER["Primary"]} orders', 1)}</div>
  </section>
'''
page('company', 'order-management', 'CMP-ORD-01', 'Company Administration — Super Admin — Order Management (CMP-ORD-01)', body)

# ---------- Order Details (ORD-2026-10459), Super Admin and Operations Manager ----------
o = O59; t = O59_TAX
item_rows = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num">{N(q)}</td><td class="num">{N(CSTK[s]["vapi"])}</td>'
                    f'<td class="num"><b>{M(O59_AMT[s])}</b></td></tr>' for s, q in o['lines'])
assert all(CSTK[s]['vapi_avail'] >= q for s, q in o['lines'])
acts = ('<button class="btn" type="button" data-role="ADM"><i data-icon="download"></i>Download Order Copy</button><button class="btn danger" type="button" data-role="ADM">Cancel Order</button>'
        '<button class="btn" type="button" data-role="OPS"><i data-icon="download"></i>Download Packing List</button><button class="btn" type="button" data-role="OPS">Plan Dispatch</button><button class="btn pri" type="button" data-role="OPS">Mark as Packed</button>')
steps = [('Stock Reserved at Plant Warehouse', 'Completed 24/10/2026', 'ok'), ('Packing', f'Planned {o["packing"]}', 'warn'), ('Dispatch', f'Planned {o["dispatch"]}', 'plain')]
checklist = '<ul class="list">' + ''.join(f'<li><div class="grow"><b>{n}</b></div>{chip(c, k)}</li>' for n, c, k in steps) + '</ul>'
body = f'''  <div class="head">
    <div class="title-row"><h1>{o["number"]}</h1>{chip("Confirmed")}{chip("Unpaid")}</div>
    <div class="acts">{acts}</div>
  </div>
  <section class="card pad"><ol class="track">
    <li class="done"><i></i><b>Placed</b><span>{o["placed"]}</span></li><li class="done"><i></i><b>Confirmed</b><span>{o["confirmed"]}</span></li><li class="now"><i></i><b>Packed</b><span>Planned {o["packing"]}</span></li>
    <li class="todo"><i></i><b>Dispatched</b><span>Planned {o["dispatch"]}</span></li><li class="todo"><i></i><b>Delivered</b><span>Planned {o["expected"]}</span></li></ol></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      <section class="card flush"><header><h2>Items</h2></header>
        <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Plant Warehouse Stock', 'num'), ('Amount', 'num')], [item_rows], 'wrap', foot=f'<tfoot><tr><td colspan="4">Subtotal</td><td class="num">{M(t["taxable"])}</td></tr></tfoot>')}
          <div style="padding:1rem 1.125rem"><dl class="kv" style="max-width:22rem;margin-left:auto"><dt>Central GST 9%</dt><dd>{M(t["gst"])}</dd><dt>State GST 9%</dt><dd>{M(t["gst"])}</dd><dt>Freight</dt><dd>{M(t["freight"])}</dd></dl>
          <dl class="kv total" style="max-width:22rem;margin-left:auto"><dt>Total</dt><dd>{M(o["total"])}</dd></dl></div></div></section>
      <section class="card flush"><header><h2>Order Activity</h2></header><div class="body">{table([('Date', ''), ('Event', ''), ('By', '')], [
        '<tr><td class="nowrap">24/10/2026 11:20</td><td><b>Stock reserved at Plant Warehouse, Vapi</b></td><td>Neha Kulkarni</td></tr>',
        f'<tr><td class="nowrap">{o["confirmed"]}</td><td><b>Order confirmed</b></td><td>{o["confirmed_by"]}</td></tr>',
        f'<tr><td class="nowrap">{o["placed"]}</td><td><b>Order placed</b></td><td>{o["placed_by"]}</td></tr>'])}</div></section>
      <section class="card"><header><h2>Order Information</h2></header><div class="body">{kv([('Placed By', o['placed_by']), ('Confirmed By', o['confirmed_by']), ('Payment Terms', '45 days'), ('Invoice', 'Not Yet Raised'), ('Scheme', 'None'), ('Reference Number', o['ref'])])}</div></section>
    </div>
    <div class="stack">
      <section class="card"><header><h2>Customer</h2></header><div class="body">{kv([('Customer', '<a data-link="CMP-CUS-02"><b>Distributor Alpha</b></a>'), ('Customer Code', '<span class="mono">CUS-0018</span>'), ('City', 'Bhiwandi'), ('Account Manager', 'Vikram Chopra')])}</div></section>
      <section class="card" data-role="ADM"><header><h2>Credit Check</h2></header><div class="body">{kv([('Credit Limit', ML(CREDIT_LIMIT)), ('Outstanding Balance', ML(OUTSTANDING)), ('This Order', ML(o['total'])), ('Credit Available After', ML(CREDIT_AFTER_59))])}</div></section>
      <section class="card"><header><h2>Processing</h2></header><div class="body">{checklist}</div></section>
      <section class="card"><header><h2>Delivery</h2></header><div class="body">{kv([('Dispatch From', 'Plant Warehouse, Vapi'), ('Deliver To', o['deliver']), ('Planned Dispatch', o['dispatch']), ('Expected Delivery', o['expected']), ('Transporter', o['transporter'])])}</div></section>
    </div>
  </div>
'''
page('company', 'order-details', 'CMP-ORD-02', 'Company Administration — Super Admin — Order Details (CMP-ORD-02)', body)
