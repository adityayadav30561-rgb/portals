"""Phase 2, part C: Primary Customer Owner: Order History, Order Details, Inventory Overview, Inventory Item Details."""
from data import *

# ---------- Order History ----------
H = [('ORD-2026-10482','26/10/2026',760,949752,'31/10/2026','requested','Awaiting Confirmation','Unpaid'),
     ('ORD-2026-10459','23/10/2026',280,336500,'29/10/2026','planned','Confirmed','Unpaid'),
     ('ORD-2026-10447','19/10/2026',360,442930,'27/10/2026','expected','In Transit','Unpaid'),
     ('ORD-2026-10431','15/10/2026',520,618400,'20/10/2026','','Delivered','Partly Paid'),
     ('ORD-2026-10398','08/10/2026',430,524100,'13/10/2026','','Delivered','Paid'),
     ('ORD-2026-10372','01/10/2026',400,481200,'06/10/2026','','Delivered','Paid'),
     ('ORD-2026-10341','24/09/2026',470,572300,'29/09/2026','','Delivered','Paid'),
     ('ORD-2026-10316','17/09/2026',330,398650,'22/09/2026','','Delivered','Paid'),
     ('ORD-2026-10290','10/09/2026',500,605900,'15/09/2026','','Delivered','Paid'),
     ('ORD-2026-10265','03/09/2026',200,241000,'','','Cancelled','Not Applicable')]
rows = ''
for o,d,s,v,dl,note,st,pay in H:
    dcell = f'{dl}<small>{note}</small>' if note else (dl or '—')
    rows += f'<tr><td><a data-link="PRI-ORD-02"><b>{o}</b></a></td><td>{d}</td><td class="num">{N(s)}</td><td class="num"><b>{M(v)}</b></td><td>{dcell}</td><td>{chip(st)}</td><td>{chip(pay)}</td><td><div class="row-actions"><a class="btn sm" data-link="PRI-ORD-02">View</a></div></td></tr>\n'
tabs = [('All Orders',142,True),('Awaiting Confirmation',2,False),('Confirmed',3,False),('In Transit',2,False),('Delivered',132,False),('Cancelled',3,False)]
tabs_html = ''.join(f'<span class="{"on" if on else ""}">{t}<b>{n}</b></span>' for t,n,on in tabs)
body = f'''  <div class="head">
    <div><h1>Order History</h1><p>142 orders since 12 April 2018</p></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Orders</button><a class="btn pri" data-link="PRI-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    <div class="card kpi"><label>Orders This Month</label><strong>6</strong><div class="foot"><span>1 to 26 October 2026</span></div></div>
    <div class="card kpi"><label>Order Value This Month</label><strong>{M(3352882)}</strong><div class="foot"><span class="delta up">+38.0%</span><span>compared with September</span></div></div>
    <div class="card kpi"><label>In Transit</label><strong>2</strong><div class="foot"><span>next delivery 27/10/2026</span></div></div>
    <div class="card kpi"><label>Awaiting Confirmation</label><strong>2</strong><div class="foot"><span>oldest placed 26/10/2026</span></div></div>
  </div>
  <section class="card flush">
    <div style="padding:0 1.125rem"><div class="tabs">{tabs_html}</div></div>
    <div class="filters" style="padding:1rem 1.125rem 0">
      <label class="finder grow"><i data-icon="search"></i><input type="search" placeholder="Search by order number or product" aria-label="Search orders"></label>
      <span class="sel"><small>Date Range</small> Last 90 days <i data-icon="down"></i></span>
      <span class="sel"><small>Payment</small> All <i data-icon="down"></i></span>
      <span class="sel"><small>Delivery Location</small> All <i data-icon="down"></i></span></div>
    <div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Order Number</th><th>Order Date</th><th class="num">Sheets</th><th class="num">Value</th><th>Delivery Date</th><th>Order Status</th><th>Payment</th><th></th></tr></thead><tbody>{rows}</tbody></table></div>
      <div class="pg"><span>Showing 1 to 10 of 142 orders</span><div class="pages"><span class="on">1</span><span>2</span><span>3</span><span>…</span><span>15</span></div></div></div>
  </section>
'''
page('primary','order-history','PRI-ORD-01','Primary Customer — Owner — Order History (PRI-ORD-01)', body)

# ---------- Order Details (ORD-2026-10447) ----------
L = [('LM-WNT-001',100,1140),('LM-ARC-002',150,905),('LM-CHR-007',60,1055),('LM-WNG-011',50,1170)]
sub = sum(q*p for _,q,p in L); assert sub == 371550
rows = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b><small>{s}</small></div></div></td><td class="num">{N(q)}</td><td class="num">{M(p)}</td><td class="num"><b>{M(q*p)}</b></td></tr>' for s,q,p in L)
total = sub + 33440*2 + 4500; assert total == 442930, total
body = f'''  <div class="head">
    <div><div class="title-row"><h1>ORD-2026-10447</h1>{chip('In Transit')}{chip('Unpaid')}</div><p>Placed 19/10/2026 by Rajesh Menon · 360 sheets</p></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Order Copy</button><a class="btn" data-link="PRI-SUP-02"><i data-icon="help"></i>Raise Support Ticket</a><button class="btn pri" type="button"><i data-icon="repeat"></i>Reorder</button></div>
  </div>
  <section class="card pad"><ol class="track">
    <li class="done"><i></i><b>Placed</b><span>19/10/2026 10:15</span></li><li class="done"><i></i><b>Confirmed</b><span>20/10/2026 09:40</span></li><li class="done"><i></i><b>Packed</b><span>23/10/2026 17:05</span></li>
    <li class="now"><i></i><b>In Transit</b><span>dispatched 24/10/2026 06:30</span></li><li class="todo"><i></i><b>Delivered</b><span>expected 27/10/2026</span></li></ol></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      <section class="card flush"><header><h2>Items</h2><span class="meta">4 products</span></header>
        <div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Product</th><th class="num">Sheets</th><th class="num">Price per Sheet</th><th class="num">Amount</th></tr></thead><tbody>{rows}</tbody>
          <tfoot><tr><td colspan="3">Subtotal</td><td class="num">{M(sub)}</td></tr></tfoot></table></div>
          <div style="padding:1rem 1.125rem"><dl class="kv" style="max-width:22rem;margin-left:auto"><dt>Central GST 9%</dt><dd>{M(33440)}</dd><dt>State GST 9%</dt><dd>{M(33440)}</dd><dt>Freight</dt><dd>{M(4500)}</dd></dl>
          <dl class="kv total" style="max-width:22rem;margin-left:auto"><dt>Total</dt><dd>{M(total)}</dd></dl></div></div></section>
      <section class="card"><header><h2>Order Activity</h2></header><div class="body"><ul class="feed">
        <li><span class="dot"><i data-icon="truck"></i></span><div><b>Shipment dispatched</b><span class="sub">Western Freight Carriers collected 360 sheets from the Vapi plant warehouse</span></div><time>24/10/2026 06:30</time></li>
        <li><span class="dot"><i data-icon="cart"></i></span><div><b>Packing completed</b><span class="sub">15 packs prepared by Neha Kulkarni’s team</span></div><time>23/10/2026 17:05</time></li>
        <li><span class="dot ok"><i data-icon="check"></i></span><div><b>Order confirmed</b><span class="sub">Confirmed by Crestline Laminates</span></div><time>20/10/2026 09:40</time></li>
        <li><span class="dot"><i data-icon="doc"></i></span><div><b>Order placed</b><span class="sub">Placed by Rajesh Menon</span></div><time>19/10/2026 10:15</time></li></ul></div></section>
    </div>
    <div class="stack">
      <section class="card"><header><h2>Delivery</h2><span class="meta mono">DSP-2026-5521</span></header><div class="body"><dl class="kv"><dt>Deliver To</dt><dd>Bhiwandi Warehouse, Thane District</dd><dt>Expected</dt><dd>27/10/2026</dd><dt>Transporter</dt><dd>Western Freight Carriers</dd><dt>Vehicle</dt><dd>MH 04 KP 7712</dd><dt>Driver</dt><dd>Ramesh Pawar<br><span class="sub">+91 90000 12345</span></dd></dl></div></section>
      <section class="card"><header><h2>Invoice</h2></header><div class="body"><dl class="kv"><dt>Invoice Number</dt><dd><a data-link="PRI-BIL-02">INV-2026-03318</a></dd><dt>Issued</dt><dd>24/10/2026</dd><dt>Due</dt><dd>08/12/2026</dd><dt>Amount</dt><dd><b>{M(total)}</b></dd><dt>Status</dt><dd>{chip('Unpaid')}</dd></dl>
        <a class="btn block" data-link="PRI-BIL-02" style="margin-top:1rem">View Invoice</a></div></section>
      <section class="card"><header><h2>Order Information</h2></header><div class="body"><dl class="kv"><dt>Payment Terms</dt><dd>45 days from invoice</dd><dt>Transport</dt><dd>Company Transport</dd><dt>Scheme</dt><dd>None applied</dd><dt>Reference Number</dt><dd>DA-OCT-117</dd></dl></div></section>
    </div>
  </div>
'''
page('primary','order-details','PRI-ORD-02','Primary Customer — Owner — Order Details (PRI-ORD-02)', body)

# ---------- Inventory Overview ----------
def stock_bar(p):
    on, lvl = p[8], p[12]
    pct = 0 if on == 0 else min(100, round(on / (lvl * 3) * 100))
    cls = 'bad' if p[13]=='Out of Stock' else 'warn' if p[13]=='Low Stock' else 'ok'
    return f'<span class="meter {cls}" style="width:6rem"><i style="width:{pct}%"></i></span>'
rows = ''
for p in P:
    rows += f'''<tr><td><div class="prod">{sw(p[0])}<div><a data-link="PRI-INV-02"><b>{p[1]}</b></a><small>{p[0]} · {p[2]}, {p[3]}</small></div></div></td>
      <td class="num">{N(p[8])}</td><td class="num">{N(p[9])}</td><td class="num"><b>{N(p[10])}</b></td><td class="num">{N(p[11]) if p[11] else '—'}</td><td class="num">{N(p[12])}</td><td>{stock_bar(p)}</td><td>{chip(p[13])}</td></tr>
'''
tabs = [('All Products',12,True),('In Stock',8,False),('Low Stock',3,False),('Out of Stock',1,False)]
tabs_html = ''.join(f'<span class="{"on" if on else ""}">{t}<b>{n}</b></span>' for t,n,on in tabs)
body = f'''  <div class="head">
    <div><h1>Inventory Overview</h1><p>Bhiwandi and Pune warehouses · position on 26 October 2026</p></div>
    <div class="acts"><span class="sel"><small>Warehouse</small> All Warehouses <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Stock</button><a class="btn pri" data-link="PRI-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    <div class="card kpi"><label>Sheets on Hand</label><strong>7,415</strong><div class="foot"><span>12 products</span></div></div>
    <div class="card kpi"><label>Stock Value</label><strong>{M(7842000)}</strong><div class="foot"><span>at purchase cost</span></div></div>
    <div class="card kpi"><label>Reserved for Dealers</label><strong>1,875 <small>sheets</small></strong><div class="foot"><span>25% of stock on hand</span></div></div>
    <div class="card kpi"><label>Arriving From Crestline</label><strong>1,450 <small>sheets</small></strong><div class="foot"><span>next arrival 27/10/2026</span></div></div>
  </div>
  <div class="grid g-chart" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr)">
    <section class="card"><header><h2>Stock Health</h2><span class="meta">12 products</span></header><div class="body">{chart('donut', series=[{'name':'In Stock','value':8,'color':'var(--ok)'},{'name':'Low Stock','value':3,'color':'#e0a030'},{'name':'Out of Stock','value':1,'color':'var(--bad)'}], center='12', caption='products')}</div></section>
    <section class="card"><header><h2>Incoming Shipments</h2></header><div class="body"><ul class="list">
      <li><span style="width:2rem;height:2rem;border-radius:.5rem;display:grid;place-items:center;background:var(--accent-soft);color:var(--accent-ink)"><i data-icon="truck"></i></span><div class="grow"><b class="mono">DSP-2026-5521</b><span class="sub">ORD-2026-10447 \u00b7 360 sheets \u00b7 in transit</span></div><span class="sub">27/10/2026</span></li>
      <li><span style="width:2rem;height:2rem;border-radius:.5rem;display:grid;place-items:center;background:var(--accent-soft);color:var(--accent-ink)"><i data-icon="truck"></i></span><div class="grow"><b>ORD-2026-10459</b><span class="sub">280 sheets \u00b7 packing</span></div><span class="sub">29/10/2026</span></li>
      <li><span style="width:2rem;height:2rem;border-radius:.5rem;display:grid;place-items:center;background:var(--accent-soft);color:var(--accent-ink)"><i data-icon="truck"></i></span><div class="grow"><b>ORD-2026-10482</b><span class="sub">760 sheets \u00b7 awaiting confirmation</span></div><span class="sub">31/10/2026</span></li>
    </ul></div></section>
  </div>
  <section class="card flush"><div style="padding:0 1.125rem"><div class="tabs">{tabs_html}</div></div>
    <div class="filters" style="padding:1rem 1.125rem 0"><label class="finder grow"><i data-icon="search"></i><input type="search" placeholder="Search by product name or SKU" aria-label="Search stock"></label><span class="sel"><small>Finish</small> All <i data-icon="down"></i></span><span class="sel"><small>Thickness</small> All <i data-icon="down"></i></span></div>
    <div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Product</th><th class="num">On Hand</th><th class="num">Reserved</th><th class="num">Available</th><th class="num">On Order</th><th class="num">Reorder Level</th><th>Stock Level</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>
'''
page('primary','inventory-overview','PRI-INV-01','Primary Customer — Owner — Inventory Overview (PRI-INV-01)', body)

# ---------- Inventory Item Details (LM-CAL-003) ----------
sku = 'LM-CAL-003'; p = BY[sku]
dates = ['27/07/2026','03/08/2026','10/08/2026','17/08/2026','24/08/2026','31/08/2026','07/09/2026','14/09/2026','21/09/2026','28/09/2026','05/10/2026','12/10/2026','19/10/2026','26/10/2026']
levels = [480,420,365,300,690,630,575,510,445,385,330,300,260,215]
reorder = [250]*14
mv = [('26/10/2026','Sale to Dealer','Dealer Delta · DSP-2026-5534','−20',215),('24/10/2026','Sale to Dealer','Dealer Bravo · DSP-2026-5527','−25',235),
      ('22/10/2026','Sale to Dealer','Dealer Foxtrot · DSP-2026-5519','−15',260),('19/10/2026','Sale to Dealer','Dealer Gopal · DSP-2026-5508','−30',275),
      ('15/10/2026','Sale to Dealer','Dealer Harsh · DSP-2026-5496','−25',305),('12/10/2026','Stock Adjustment','Damaged in handling · ADJ-2026-0034','−5',330),
      ('08/10/2026','Sale to Dealer','Dealer Bravo · DSP-2026-5471','−25',335),('03/10/2026','Sale to Dealer','Dealer Delta · DSP-2026-5452','−25',360)]
mv_rows = ''.join(f'<tr><td>{d}</td><td>{chip(t, "warn" if t=="Stock Adjustment" else "blue")}</td><td>{r}</td><td class="num"><b>{q}</b></td><td class="num">{N(b)}</td></tr>' for d,t,r,q,b in mv)
body = f'''  <div class="head">
    <div><div class="title-row"><h1>{p[1]}</h1>{chip('Low Stock')}</div><p class="mono">{sku} · {p[2]}, {p[3]}</p></div>
    <div class="acts"><a class="btn" data-link="PRI-CAT-02"><i data-icon="box"></i>View Product</a><a class="btn pri" data-link="PRI-ORD-03"><i data-icon="plus"></i>Reorder</a></div>
  </div>
  <div class="alert"><i data-icon="warn"></i><span>Available stock of 125 sheets is below the reorder level of 250 sheets. 300 sheets are on order and arrive on 30/10/2026.</span></div>
  <div class="kpis">
    <div class="card kpi"><label>On Hand</label><strong>215</strong><div class="foot"><span>sheets in two batches</span></div></div>
    <div class="card kpi"><label>Reserved for Dealers</label><strong>90</strong><div class="foot"><span>5 open dealer orders</span></div></div>
    <div class="card kpi"><label>Available</label><strong>125</strong><div class="foot"><span class="delta down">below reorder level</span></div></div>
    <div class="card kpi"><label>On Order</label><strong>300</strong><div class="foot"><span>arriving 30/10/2026</span></div></div>
    <div class="card kpi"><label>Days of Cover</label><strong>9</strong><div class="foot"><span>14 sheets sold a day</span></div></div>
  </div>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      <section class="card"><header><h2>Stock Level</h2><span class="meta">weekly, 27 July to 26 October 2026</span></header>
        <div class="body">{chart('line', dates, [{'name':'Sheets on hand','values':levels,'color':'var(--accent)'},{'name':'Reorder level','values':reorder,'color':'var(--bad)','dots':False}], area=True)}</div></section>
      <section class="card flush"><header><h2>Stock Movements</h2><a class="more" data-link="PRI-INV-01">Inventory overview</a></header>
        <div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Date</th><th>Type</th><th>Reference</th><th class="num">Sheets</th><th class="num">Balance</th></tr></thead><tbody>{mv_rows}</tbody></table></div></div></section>
    </div>
    <div class="stack">
      <section class="card pad" style="display:grid;gap:.75rem">{sw(sku,'lg','aspect-ratio:16/9')}<dl class="kv"><dt>Finish</dt><dd>{p[2]}</dd><dt>Thickness</dt><dd>{p[3]}</dd><dt>Sheet Size</dt><dd>8 ft × 4 ft</dd></dl></section>
      <section class="card flush"><header><h2>Batches</h2></header><div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Batch</th><th>Received</th><th class="num">Sheets</th><th>Rack</th></tr></thead><tbody>
        <tr><td class="mono">B-2608-07</td><td>24/08/2026</td><td class="num">160</td><td>B-04</td></tr><tr><td class="mono">B-2606-11</td><td>14/06/2026</td><td class="num">55</td><td>B-05</td></tr></tbody></table></div></div></section>
      <section class="card"><header><h2>Reorder Settings</h2><button class="btn sm" type="button" style="margin-left:auto"><i data-icon="edit"></i>Edit</button></header><div class="body"><dl class="kv"><dt>Reorder Level</dt><dd>250 sheets</dd><dt>Reorder Quantity</dt><dd>400 sheets</dd><dt>Lead Time</dt><dd>6 days</dd><dt>Preferred Warehouse</dt><dd>Bhiwandi Warehouse</dd></dl></div></section>
    </div>
  </div>
'''
page('primary','inventory-item-details','PRI-INV-02','Primary Customer — Owner — Inventory Item Details (PRI-INV-02)', body)
