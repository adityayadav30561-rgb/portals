"""Phase 8, part A: Tertiary Customer Retailer Owner (screens shared with the Sales Executive and Inventory and Purchasing Executive use ?role=SLS / ?role=PUR):
Dashboard, Store Profile, Product Catalogue, Product Details, Place Order, Order Builder, Order Confirmation. Retailer Charlie, Camp, Pune; supplier Dealer Bravo.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md "Phase 8 data"."""
from data import *

SQ = chr(0x2212)
PO = PEND_ORDER
def steps(now):
    out = ''
    for i, n in enumerate(['Select Products', 'Order Details', 'Confirmation'], 1):
        cls = 'done' if i < now else 'now' if i == now else ''
        mark = '<i data-icon="check"></i>' if i < now else str(i)
        out += f'<li class="{cls}"><i>{mark}</i>{n}</li>'
    return f'<ol class="steps" aria-label="Order steps">{out}</ol>'
def avail_chip(s):
    st = BSTOCK[s]['status']                                                              # availability is Dealer Bravo's available stock
    return chip(st) if st != 'In Stock' else ''
def offer_item(o):
    pct_ = min(100, round(o[6] / o[7] * 100))
    return f'''<li style="display:block"><div style="display:flex;align-items:center;gap:.75rem;flex-wrap:wrap"><b style="flex:1;min-width:10rem">{o[1]}</b><span class="chip plain">Ends {o[4]}</span></div>
          <span class="meter {"ok" if pct_ >= 90 else ""}" style="margin-top:.75rem"><i style="width:{pct_}%"></i></span>
          <div style="margin-top:.5rem"><b>{N(o[6])}</b> of {N(o[7])} sheets</div></li>'''
fin_col = {'Matte': '#0a48fd', 'Woodgrain': '#0b8fa8', 'Texture': '#7a36fb', 'Gloss': '#e0a030', 'Suede': '#0c9b6a', 'High Gloss': '#d43a2f', 'Metallic': '#8b93a3'}
NO_ORDER = 'data-role="OWN PUR"'                                                         # the Sales Executive has no ordering screens

# ---------- Dashboard ----------
recent = ''.join(f'<tr><td><a data-link="TER-ORD-02"><b>{o}</b></a></td><td>{d}</td><td class="num">{N(sh)}</td><td class="num"><b>{M(v)}</b></td><td>{chip(st)}</td></tr>' for o, d, sh, v, dl, st, pay in CHR_ORDERS[:7])
top = sorted((s for s in CSOLD if CSOLD[s]), key=lambda s: -CSOLD[s])[:5]
top_rows = ''.join(f'<li>{sw(s, "", "width:2.5rem;height:2.5rem;flex:none")}<div class="grow"><b>{BY[s][1]}</b><span class="meter" style="margin-top:.5rem"><i style="width:{CSOLD[s] / CSOLD[top[0]] * 100:.0f}%"></i></span></div><b>{N(CSOLD[s])}</b></li>' for s in top)
alert_order = sorted(CLOW, key=lambda s: (CSTOCK[s]['status'] != 'Out of Stock', CSTOCK[s]['available'] / CSTOCK[s]['level']))
alert_rows = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><a data-link="TER-INV-02"><b>{BY[s][1]}</b></a></div></div></td><td class="mono nowrap">{s}</td><td class="num"><b>{N(CSTOCK[s]["available"])}</b></td><td class="num">{N(CSTOCK[s]["level"])}</td><td>{chip(CSTOCK[s]["status"])}</td></tr>' for s in alert_order)
fin_series = [{'name': n, 'value': v, 'color': fin_col[n]} for n, v in sorted(CFINISH.items(), key=lambda x: -x[1])]
body = f'''  <div class="head">
    <h1>Dashboard</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><a class="btn" data-link="TER-RTS-01"><i data-icon="plus"></i>Record Retail Sale</a><a class="btn pri" data-link="TER-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Sales to Customers This Month', ML(CRETAIL_OCT), up(pct(CRETAIL_OCT, CHR_RETAIL_SEPT)))}
    {kpi('Purchases This Month', ML(264000), up(pct(264000, 240000)))}
    {kpi('Outstanding Balance', ML(CHR_OWES), chip(f'{CHR_USED}% of Credit Limit', 'ok'))}
    {kpi('Stock on Hand', f'{N(216)} <small>sheets</small>', '<span class="delta down">3 Low Stock</span>')}
  </div>
  <div class="grid g-chart">
    {card('Sales to Customers and Purchases', chart('bars', MONTHS, [{'name': 'Sales to customers', 'values': CHR_RETAIL_MONTH, 'color': 'var(--teal)'}, {'name': 'Purchases from Dealer Bravo', 'values': CHR_BUY_MONTH, 'color': 'var(--accent)'}], money=True, height=280))}
    <section class="card"><header><h2>Stock by Finish</h2></header><div class="body center">{chart('donut', series=fin_series, center=N(216), caption='sheets')}</div></section>
  </div>
  <div class="grid g-main-side">
    <section class="card flush"><header><h2>Recent Orders</h2><a class="more" data-link="TER-ORD-01">View all orders</a></header>
      <div class="body">{table([('Order Number', ''), ('Date', ''), ('Sheets', 'num'), ('Value', 'num'), ('Status', '')], [recent], 'wrap')}</div></section>
    <section class="card"><header><h2>Best Selling Products</h2></header>
      <div class="body"><ul class="list">{top_rows}</ul>{kv([('Sheets Sold This Month', N(163))], 'total')}</div></section>
  </div>
  <div class="grid g-main-side" style="--side:22rem">
    <section class="card flush"><header><h2>Stock Alerts</h2><a class="more" data-link="TER-INV-01">My inventory</a></header>
      <div class="body">{table([('Product', ''), ('SKU', ''), ('Available', 'num'), ('Reorder Level', 'num'), ('Status', '')], [alert_rows], 'wrap')}</div></section>
    <section class="card"><header><h2>Active Offers</h2><a class="more" data-link="TER-SCH-01">All offers</a></header>
      <div class="body"><ul class="list">{offer_item(COFFERS[0])}{offer_item(COFFERS[1])}</ul>{kv([('Earned on Active Offers', M(140))], 'total')}</div></section>
  </div>
'''
page('tertiary', 'retailer-owner-dashboard', 'TER-OWN-01', 'Tertiary Customer — Retailer Owner — Dashboard (TER-OWN-01)', body)

# ---------- Store Profile ----------
def block(title, rows): return card(title, kv(rows))
nw = lambda t: f'<span style="white-space:nowrap">{t}</span>'
contacts = [('Imran Sheikh', 'Retailer Owner', 'imran.sheikh@retailercharlie.example', '+91 90000 51001'), ('Pooja Verma', 'Sales Executive', 'pooja.verma@retailercharlie.example', '+91 90000 51002'),
            ('Faisal Khan', 'Inventory and Purchasing Executive', 'faisal.khan@retailercharlie.example', '+91 90000 51003')]
contact_rows = ''.join(f'<tr><td class="nowrap"><b>{n}</b></td><td>{r}</td><td class="nowrap">{e}</td><td class="nowrap">{p}</td></tr>' for n, r, e, p in contacts)
doc_rows = ''.join(f'<tr><td><b>{n}</b></td><td><span class="tag">PDF</span></td><td>{d}</td><td><div class="row-actions">{dl_btn("Download " + n)}</div></td></tr>' for n, d in
                   [('GST Registration Certificate', '12/05/2021'), ('Shop Licence', '08/04/2026'), ('Retailer Agreement 2026–27', '03/04/2026')])
body = f'''  <div class="head">
    <h1>Store Profile</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Profile</button><button class="btn pri" type="button"><i data-icon="edit"></i>Edit Profile</button></div>
  </div>
  <section class="card pad" style="flex-direction:row;align-items:center;gap:1.25rem;flex-wrap:wrap">
    <div class="org" style="margin:0;padding:0;border:0;background:none"><i style="width:4rem;height:4rem;border-radius:1rem;font-size:1.25rem">RC</i></div>
    <div style="flex:1;min-width:16rem;display:grid;gap:.5rem"><h2 style="font-size:1.25rem">Retailer Charlie</h2>
      <div style="display:flex;flex-wrap:wrap;gap:.5rem">{chip('Active', 'ok')}<span class="tag">Retailer Tier C</span><span class="tag"><i data-icon="pin"></i>Camp, Pune</span></div></div>
    <dl class="kv left" style="grid-template-columns:auto auto;gap:.5rem 1.25rem"><dt>Retailer Code</dt><dd class="mono">RTL-0041</dd><dt>Customer Since</dt><dd>11 May 2021</dd></dl>
  </section>
  <div class="grid g-3" style="--cols:1.1fr 1.2fr 1.2fr">
    {block('Business Details', [('Legal Name', 'Charlie Laminates Private Limited'), ('GST Number', nw('27AAJCC4410E1ZK')), ('Business Type', 'Retailer'), ('Established', '2018')])}
    {block('Address', [('Shop', 'Shop 12, MG Road, Camp, Pune, Postal Code 411001'), ('Area', 'Camp')])}
    {card('Commercial Terms', kv([('Supplier', 'Dealer Bravo'), ('Price Tier', 'Retailer Tier C'), ('Credit Limit', ML(CHR_LIMIT)), ('Outstanding Balance', ML(CHR_OWES)), ('Credit Used', f'<span class="inline-meter"><span class="meter ok"><i style="width:{CHR_USED}%"></i></span><b>{CHR_USED}%</b></span>'), ('Credit Period', '15 days')]))}
  </div>
  <section class="card flush"><header><h2>Contacts</h2><button class="btn sm" type="button" style="margin-left:auto"><i data-icon="plus"></i>Add Contact</button></header>
    <div class="body">{table([('Name', ''), ('Role', ''), ('Email', ''), ('Phone', '')], [contact_rows])}</div></section>
  <div class="grid g-2">
    {card('Relationship Manager', kv([('Name', '<b>Arjun Nair</b>'), ('Role', 'Sales and Inventory Manager'), ('Organisation', 'Dealer Bravo'), ('Email', 'arjun.nair@<wbr>dealerbravo.example'), ('Phone', '+91 90000 31002'), ('Area', 'Camp, Pune')]))}
    <section class="card flush"><header><h2>Documents</h2></header><div class="body">{table([('Document', ''), ('Type', ''), ('Date', ''), ('', '')], [doc_rows])}</div></section>
  </div>
'''
page('tertiary', 'store-profile', 'TER-PRO-01', 'Tertiary Customer — Retailer Owner — Store Profile (TER-PRO-01)', body)

# ---------- Product Catalogue (shared with the Sales Executive and the Inventory and Purchasing Executive) ----------
cards = ''
for p in P:
    sku = p[0]; q = 25 if sku in ('LM-WNT-001', 'LM-ARC-002') else 5
    cards += f'''      <article class="card pcard"><a data-link="TER-CAT-02" aria-label="{p[1]}">{sw(sku)}</a>
        <div class="in"><div><h3><a data-link="TER-CAT-02" style="color:inherit">{p[1]}</a></h3></div>
          <div class="tags"><span class="tag mono">{sku}</span><span class="tag">{p[2]}</span><span class="tag">{p[3]}</span>{avail_chip(sku)}</div>
          <div><span class="label-top" style="margin-bottom:.25rem">Price per Sheet</span><div class="big-value" style="font-size:1.5rem">{M(rp(sku))}</div></div>
          <div class="buy" {NO_ORDER}>{qty(q)}<button class="btn pri" type="button"><i data-icon="plus"></i>Add to Order</button></div></div></article>
'''
body = f'''  <div class="head">
    <h1>Product Catalogue</h1>
    <div class="acts" {NO_ORDER}><a class="btn pri" data-link="TER-ORD-03"><i data-icon="cart"></i>Order Draft<span class="chip" style="margin-left:.25rem;background:#fff;color:var(--accent-ink);border:0">4</span></a></div>
  </div>
  <div class="filters">
    <label class="finder grow"><i data-icon="search"></i><input type="search" placeholder="Search by product name or SKU" aria-label="Search products"></label>
    <span class="sel"><small>Finish</small> All <i data-icon="down"></i></span>
    <span class="sel"><small>Thickness</small> All <i data-icon="down"></i></span>
    <span class="sel"><small>Availability</small> All <i data-icon="down"></i></span>
    <span class="sel"><small>Sort by</small> Product Name <i data-icon="down"></i></span>
    <span class="view-toggle" aria-label="View"><span class="on"><i data-icon="grid"></i></span><span><i data-icon="list"></i></span></span>
  </div>
  <div class="products">
{cards}  </div>
'''
page('tertiary', 'product-catalogue', 'TER-CAT-01', 'Tertiary Customer — Retailer Owner — Product Catalogue (TER-CAT-01)', body)

# ---------- Product Details (LM-WNT-001) ----------
sku = 'LM-WNT-001'; p = BY[sku]; b = CSTOCK[sku]; bb = BSTOCK[sku]
price_rows = ''.join(f'<tr><td>{a}</td><td class="num"><b>{M(v)}</b></td><td class="num">{M(v * 25)}</td></tr>' for a, v in [('Your Price', rp(sku)), ('Your Price with GST', round(rp(sku) * 1.18)), ('Selling Price to Customers', crp(sku)), ('Margin per Sheet', crp(sku) - rp(sku))])
specs = [('SKU', sku), ('Finish', 'Woodgrain'), ('Thickness', '1.0 mm'), ('Sheet Size', '8 ft × 4 ft (2,440 mm × 1,220 mm)'), ('Weight per Sheet', '6.1 kg'), ('Grade', 'Decorative'), ('Pack Size', '25 sheets'), ('Colour Family', 'Brown')]
related = ['LM-WNG-011', 'LM-TEK-006', 'LM-OAK-004', 'LM-SLT-005']
rel = ''.join(f'<a class="card" data-link="TER-CAT-02" style="overflow:hidden;color:inherit">{sw(r, "", "aspect-ratio:4/3;border-radius:0")}<div style="padding:.875rem 1rem"><b>{BY[r][1]}</b><div style="margin-top:.5rem;font-weight:620">{M(rp(r))} <span class="dim" style="font-weight:450">per sheet</span></div></div></a>' for r in related)
body = f'''  <div class="head">
    <div class="title-row"><h1>{p[1]}</h1>{chip(bb["status"])}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Specification</button><a class="btn" data-link="TER-INV-02"><i data-icon="stack"></i>View Inventory Item</a></div>
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      <section class="card pad">{sw(sku, 'lg', 'aspect-ratio:16/9;width:100%')}</section>
      <div class="grid g-2">
        {card('Specifications', kv(specs))}
        <section class="card flush"><header><h2>Price per Sheet</h2></header><div class="body">{table([('Price', ''), ('Per Sheet', 'num'), ('Per Pack of 25', 'num')], [price_rows])}</div></section>
      </div>
    </div>
    <div class="stack">
      <section class="card pad"><span class="label-top">Your Price per Sheet</span><div class="big-value">{M(rp(sku))}</div>
        <div {NO_ORDER}><div class="field" style="margin-top:1.25rem"><label>Sheets to Order</label>{qty(25)}</div>
        <dl class="kv total" style="margin-top:1.25rem"><dt>Amount</dt><dd>{M(25 * rp(sku))}</dd></dl>
        <button class="btn pri block" type="button" style="margin-top:1rem"><i data-icon="plus"></i>Add to Order</button></div></section>
      {card('Your Stock', kv([('On Hand', f'{b["on_hand"]} sheets'), ('Reserved for Customers', f'{b["reserved"]} sheets'), ('Available', f'<b>{b["available"]} sheets</b>'), ('On Order', f'{b["on_order"]} sheets'), ('Arriving', '28/10/2026'), ('Reorder Level', f'{b["level"]} sheets')]))}
      {card('Dealer Bravo Availability', kv([('Hadapsar Godown', f'{N(bb["available"])} sheets'), ('Delivery Time', '1 to 2 days')]))}
    </div>
  </div>
  <section><h2 style="margin-bottom:1rem">Related Products</h2><div class="products four">{rel}</div></section>
'''
page('tertiary', 'product-details', 'TER-CAT-02', 'Tertiary Customer — Retailer Owner — Product Details (TER-CAT-02)', body)

# ---------- Place Order ----------
QTY = dict(PO['lines'])
rows = ''
for p in P:
    s = p[0]; q = QTY.get(s, 0)
    rows += (f'<tr><td><div class="prod">{sw(s)}<div><b>{p[1]}</b>{('<div style="margin-top:.25rem">' + avail_chip(s) + '</div>') if avail_chip(s) else ''}</div></div></td><td class="mono nowrap">{s}</td>'
             f'<td class="num">{M(rp(s))}</td><td>{qty(q)}</td><td class="num"><b>{M(q * rp(s)) if q else "—"}</b></td></tr>\n')
draft = ''.join(f'<tr><td><b>{BY[s][1]}</b></td><td class="num">{N(q)}</td><td class="num"><b>{M(q * rp(s))}</b></td></tr>' for s, q in PO['lines'])
body = f'''  <div class="head">
    <h1>Place Order</h1>
    <div class="acts"><span class="sel"><i data-icon="repeat"></i>Reorder from a Previous Order <i data-icon="down"></i></span></div>
  </div>
  {steps(1)}
  <div class="grid g-main-side" style="--side:22rem">
    <section class="card flush">
      <header><h2>Products</h2><label class="finder" style="margin-left:auto;min-width:18rem"><i data-icon="search"></i><input type="search" placeholder="Search by name or SKU" aria-label="Search products"></label></header>
      <div class="body">{table([('Product', ''), ('SKU', ''), ('Price per Sheet', 'num'), ('Sheets', ''), ('Amount', 'num')], [rows], 'stack-sm')}</div>
    </section>
    <aside class="card" style="align-self:start;position:sticky;top:calc(var(--review-h) + 4.5rem)"><header><h2>Order Draft</h2></header>
      <div class="body"><div class="table-wrap" style="margin:-.25rem -1.125rem 0"><table class="tbl"><thead><tr><th>Product</th><th class="num">Sheets</th><th class="num">Amount</th></tr></thead><tbody>{draft}</tbody></table></div>
        {kv([('Sheets', str(PEND_SHEETS)), ('Freight', chip('Free', 'ok'))], '')}
        {kv([('Subtotal', M(PEND_SUB))], 'total')}
        <a class="btn pri block" data-link="TER-ORD-04" style="margin-top:1.25rem">Continue to Order Details<i data-icon="arrow"></i></a>
        <button class="btn block" type="button" style="margin-top:.5rem">Save Draft</button></div></aside>
  </div>
'''
page('tertiary', 'place-order', 'TER-ORD-03', 'Tertiary Customer — Retailer Owner — Place Order (TER-ORD-03)', body)

# ---------- Order Builder ----------
item_rows = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td>{qty(q)}</td><td class="num">{M(rp(s))}</td>'
                    f'<td class="num"><b>{M(q * rp(s))}</b></td><td><button class="icon-btn" type="button" aria-label="Remove {BY[s][1]}"><i data-icon="trash"></i></button></td></tr>\n' for s, q in PO['lines'])
used_after = round((CHR_OWES + PEND_TOTAL) / CHR_LIMIT * 100)
body = f'''  <div class="head">
    <h1>Order Builder</h1>
    <div class="acts"><a class="btn" data-link="TER-ORD-03"><i data-icon="back"></i>Back to Products</a><button class="btn" type="button">Save Draft</button><a class="btn pri" data-link="TER-ORD-05" data-role="OWN">Submit Order</a><a class="btn pri" data-link="TER-ORD-01" data-role="PUR">Submit Order</a></div>
  </div>
  {steps(2)}
  <div class="grid g-main-side" style="--side:18rem">
    <div class="stack">
      <section class="card flush"><header><h2>Order Items</h2></header>
        <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', ''), ('Price per Sheet', 'num'), ('Amount', 'num'), ('', '')], [item_rows], 'stack-sm')}</div></section>
      <section class="card"><header><h2>Delivery</h2></header><div class="body"><div class="form-grid">
        <div class="field"><label for="loc">Delivery Location</label><select class="input" id="loc"><option>Shop 12, MG Road, Camp, Pune</option></select></div>
        <div class="field"><label for="date">Requested Delivery Date</label><input class="input" id="date" value="{PO['requested']}"></div>
        <div class="field"><label for="ref">Your Reference Number</label><input class="input" id="ref" placeholder="Reference from your records"></div>
        <div class="field"><label for="contact">Receiving Contact</label><input class="input" id="contact" value="Faisal Khan, +91 90000 51003"></div>
        <div class="full"><span class="label">Transport</span><div class="form-grid" style="margin-top:.375rem">
          <label class="radio on"><input type="radio" name="t" checked><span style="flex:1;display:flex;align-items:center;justify-content:space-between;gap:.75rem"><b>Dealer Transport</b>{chip('Free', 'ok')}</span></label>
          <label class="radio"><input type="radio" name="t"><span><b>Self Pickup</b></span></label></div></div>
        <div class="field full"><label for="notes">Order Notes</label><textarea class="input" id="notes" placeholder="Notes for the dispatch team"></textarea></div>
      </div></div></section>
    </div>
    <div class="stack">
      {card('Order Summary', kv([('Sheets', str(PEND_SHEETS)), ('Subtotal', M(PEND_SUB)), ('Central GST 9%', M(PEND_GST)), ('State GST 9%', M(PEND_GST)), ('Freight', chip('Free', 'ok'))]) + kv([('Total', M(PEND_TOTAL))], 'total'))}
      <section class="card"><header><h2>Credit</h2></header><div class="body">
        {kv([('Credit Limit', ML(CHR_LIMIT)), ('Outstanding Balance', ML(CHR_OWES)), ('This Order', M(PEND_TOTAL))])}
        <span class="meter {meter_cls(used_after)}" style="margin-top:1rem"><i style="width:{used_after}%"></i></span>
        {kv([('Credit Available', ML(CHR_LIMIT - CHR_OWES - PEND_TOTAL))], 'total')}</div></section>
    </div>
  </div>
'''
page('tertiary', 'order-builder', 'TER-ORD-04', 'Tertiary Customer — Retailer Owner — Order Builder (TER-ORD-04)', body)

# ---------- Order Confirmation ----------
line_rows = ''.join(f'<tr><td><b>{BY[s][1]}</b></td><td class="num">{N(q)}</td><td class="num"><b>{M(q * rp(s))}</b></td></tr>' for s, q in PO['lines'])
body = f'''  <div class="head"><h1>Order Confirmation</h1></div>
  {steps(4)}
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      <section class="card pad" style="display:grid;justify-items:center;gap:1.5rem;text-align:center;padding:2.25rem 1.5rem">
        <div class="state" style="padding:0;gap:.75rem"><div class="badge"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg></div>
          <h2 style="font-size:1.5rem">Order Submitted</h2><div class="big-value mono" style="font-size:1.375rem">{PO['number']}</div></div>
        <div class="stats" style="--cols:1.6fr 2fr .8fr 1.3fr"><div><span>Placed</span><b>{PO['date']} {PO['time']}</b></div><div><span>Status</span>{chip('Awaiting Confirmation')}</div><div><span>Sheets</span><b>{PEND_SHEETS}</b></div><div><span>Total</span><b>{M(PEND_TOTAL)}</b></div></div>
        <div class="actions" style="display:flex;flex-wrap:wrap;gap:.75rem;justify-content:center"><a class="btn pri" data-link="TER-ORD-02">View Order Details</a><a class="btn" data-link="TER-ORD-03">Place Another Order</a><button class="btn" type="button"><i data-icon="download"></i>Download Order Copy</button></div>
      </section>
      <section class="card"><header><h2>Order Progress</h2></header><div class="body">
        <ol class="track"><li class="done"><i></i><b>Placed</b><span>{PO['date']}</span></li><li class="now"><i></i><b>Confirmation</b><span>Pending</span></li><li class="todo"><i></i><b>Packing</b><span>27/10/2026</span></li><li class="todo"><i></i><b>Dispatch</b><span>27/10/2026</span></li><li class="todo"><i></i><b>Delivery</b><span>{PO['requested']}</span></li></ol></div></section>
    </div>
    <div class="stack">
      <section class="card"><header><h2>Order Summary</h2></header><div class="body"><div class="table-wrap" style="margin:-.25rem -1.125rem 0"><table class="tbl"><thead><tr><th>Product</th><th class="num">Sheets</th><th class="num">Amount</th></tr></thead><tbody>{line_rows}</tbody></table></div>
        {kv([('Central GST 9%', M(PEND_GST)), ('State GST 9%', M(PEND_GST))])}{kv([('Total', M(PEND_TOTAL))], 'total')}</div></section>
      {card('Delivery', kv([('Deliver To', 'Shop 12, MG Road, Camp, Pune'), ('Requested', PO['requested']), ('Transport', 'Dealer Transport'), ('Receiving Contact', 'Faisal Khan'), ('Placed By', PO['placed_by'])]))}
      {card('Credit', kv([('Credit Limit', ML(CHR_LIMIT)), ('Credit Available', ML(CHR_LIMIT - CHR_OWES - PEND_TOTAL))]))}
    </div>
  </div>
'''
page('tertiary', 'order-confirmation', 'TER-ORD-05', 'Tertiary Customer — Retailer Owner — Order Confirmation (TER-ORD-05)', body)
