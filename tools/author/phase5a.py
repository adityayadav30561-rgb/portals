"""Phase 5, part A: Secondary Customer Owner (screens shared with the Manager use ?role=MGR): Dashboard, Company Profile, Product
Catalogue, Product Details, Place Order, Order Builder, Order Confirmation, Order History, Order Details, Inventory Overview,
Inventory Item Details, Retailer Network, Retailer Details, Add Retailer Request. Dealer Bravo, Pune; supplier Distributor Alpha.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md "Phase 5 data"."""
from data import *

SQ = chr(0x2212)
cp_used = round(BRV_OWES / BRV_LIMIT * 100)                                                 # 33

def steps(now):
    out = ''
    for i, n in enumerate(['Select Products', 'Order Details', 'Confirmation'], 1):
        cls = 'done' if i < now else 'now' if i == now else ''
        mark = '<i data-icon="check"></i>' if i < now else str(i)
        out += f'<li class="{cls}"><i>{mark}</i>{n}</li>'
    return f'<ol class="steps" aria-label="Order steps">{out}</ol>'
def avail_chip(s):
    st = BY[s][13]                                                                          # availability is Distributor Alpha's available stock
    return chip(st) if st != 'In Stock' else ''
def sch_item(sc):
    pct = min(100, round(sc[2] / sc[3] * 100))
    return f'''<li style="display:block"><div style="display:flex;align-items:center;gap:.75rem;flex-wrap:wrap"><b style="flex:1;min-width:10rem">{sc[1]}</b><span class="chip plain">Ends {sc[4]}</span></div>
          <span class="meter {"ok" if pct >= 90 else ""}" style="margin-top:.75rem"><i style="width:{pct}%"></i></span>
          <div style="margin-top:.5rem"><b>{N(sc[2])}</b> of {N(sc[3])} sheets</div></li>'''

H = BRV_ORDERS
STATUS_CHIP.update({'Sale to Retailer': 'blue'})

# ---------- Dashboard ----------
recent = ''.join(f'<tr><td><a data-link="SEC-ORD-02"><b>{o}</b></a></td><td>{d}</td><td class="num">{N(sh)}</td><td class="num">{M(v)}</td><td>{chip(st)}</td></tr>' for o, d, sh, v, dl, st, pay in H[:7])
top_ret = sorted(RETAILERS, key=lambda r: -r[9][-1])
ret_rows = ''.join(f'<li><div class="grow"><div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap"><b>{r[1]}</b><span class="tag">{r[3]}</span></div><span class="meter" style="margin-top:.625rem"><i style="width:{r[9][-1] / top_ret[0][9][-1] * 100:.0f}%"></i></span></div><b>{ML(r[9][-1])}</b></li>' for r in top_ret)
alerts = ['LM-STN-009', 'LM-CHR-007', 'LM-CAL-003']
alert_rows = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num"><b>{N(BSTOCK[s]["available"])}</b></td><td class="num">{N(BSTOCK[s]["level"])}</td><td>{chip(BSTOCK[s]["status"])}</td></tr>' for s in alerts)
fin_col = {'Matte': '#0a48fd', 'Woodgrain': '#0b8fa8', 'Texture': '#7a36fb', 'Gloss': '#e0a030', 'Suede': '#0c9b6a', 'High Gloss': '#d43a2f', 'Metallic': '#8b93a3'}
fin_series = [{'name': n, 'value': v, 'color': fin_col[n]} for n, v in sorted(BFINISH.items(), key=lambda x: -x[1])]
body = f'''  <div class="head">
    <h1>Dashboard</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Download Report</button><a class="btn pri" data-link="SEC-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Purchases This Month', ML(684000), up(pct(684000, 610000)))}
    {kpi('Sales to Retailers This Month', ML(630000), up(pct(630000, 600000)))}
    {kpi('Outstanding Balance', ML(BRV_OWES), chip(f'{cp_used}% of Credit Limit', 'ok'))}
    {kpi('Stock on Hand', f'{N(1058)} <small>sheets</small>', '<span class="delta down">3 Low Stock</span>')}
  </div>
  <div class="grid g-chart">
    {card('Purchases and Sales to Retailers', chart('bars', MONTHS, [{'name': 'Purchases from Distributor Alpha', 'values': BRV_PURCH_MONTH, 'color': 'var(--accent)'}, {'name': 'Sales to Retailers', 'values': BRV_RETAIL_MONTH, 'color': 'var(--teal)'}], money=True, height=280))}
    <section class="card"><header><h2>Stock by Finish</h2></header><div class="body center">{chart('donut', series=fin_series, center=N(1058), caption='sheets')}</div></section>
  </div>
  <div class="grid g-main-side">
    <section class="card flush"><header><h2>Recent Orders</h2><a class="more" data-link="SEC-ORD-01">View all orders</a></header>
      <div class="body">{table([('Order Number', ''), ('Date', ''), ('Sheets', 'num'), ('Value', 'num'), ('Status', '')], [recent])}</div></section>
    <section class="card"><header><h2>Top Retailers This Month</h2><a class="more" data-link="SEC-RTL-01">All retailers</a></header>
      <div class="body"><ul class="list">{ret_rows}</ul>{kv([('Sales This Month', ML(630000))], 'total')}</div></section>
  </div>
  <div class="grid g-main-side" style="--side:22rem">
    <section class="card flush"><header><h2>Stock Alerts</h2><a class="more" data-link="SEC-INV-01">Inventory overview</a></header>
      <div class="body">{table([('Product', ''), ('SKU', ''), ('Available', 'num'), ('Reorder Level', 'num'), ('Status', '')], [alert_rows])}</div></section>
    <section class="card"><header><h2>Active Schemes</h2></header>
      <div class="body"><ul class="list">{sch_item(SCH_FESTIVE)}{sch_item(SCH_MARBLE)}</ul></div></section>
  </div>
'''
page('secondary', 'owner-dashboard', 'SEC-OWN-01', 'Secondary Customer — Owner — Dashboard (SEC-OWN-01)', body)

# ---------- Company Profile ----------
def block(title, rows): return card(title, kv(rows))
nw = lambda t: f'<span style="white-space:nowrap">{t}</span>'
contacts = [('Sunita Rao', 'Owner', 'sunita.rao@dealerbravo.example', '+91 90000 31001'), ('Arjun Nair', 'Sales and Inventory Manager', 'arjun.nair@dealerbravo.example', '+91 90000 31002'),
            ('Rekha Sawant', 'Accountant', 'rekha.sawant@dealerbravo.example', '+91 90000 31003')]
contact_rows = ''.join(f'<tr><td class="nowrap"><b>{n}</b></td><td>{r}</td><td class="nowrap">{e}</td><td class="nowrap">{p}</td></tr>' for n, r, e, p in contacts)
doc_rows = ''.join(f'<tr><td><b>{n}</b></td><td><span class="tag">PDF</span></td><td>{d}</td><td><div class="row-actions">{dl_btn("Download " + n)}</div></td></tr>' for n, d in
                   [('GST Registration Certificate', '04/09/2019'), ('Trade Licence', '10/04/2026'), ('Dealer Agreement 2026–27', '02/04/2026')])
body = f'''  <div class="head">
    <h1>Company Profile</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Profile</button><button class="btn pri" type="button"><i data-icon="edit"></i>Edit Profile</button></div>
  </div>
  <section class="card pad" style="flex-direction:row;align-items:center;gap:1.25rem;flex-wrap:wrap">
    <div class="org" style="margin:0;padding:0;border:0;background:none"><i style="width:4rem;height:4rem;border-radius:1rem;font-size:1.25rem">DB</i></div>
    <div style="flex:1;min-width:16rem;display:grid;gap:.5rem"><h2 style="font-size:1.25rem">Dealer Bravo</h2>
      <div style="display:flex;flex-wrap:wrap;gap:.5rem">{chip('Active', 'ok')}<span class="tag">Dealer Tier B</span><span class="tag"><i data-icon="pin"></i>Pune District</span></div></div>
    <dl class="kv left" style="grid-template-columns:auto auto;gap:.5rem 1.25rem"><dt>Customer Code</dt><dd class="mono">CUS-0127</dd><dt>Customer Since</dt><dd>3 September 2019</dd></dl>
  </section>
  <div class="grid g-3" style="--cols:1.1fr 1.2fr 1.2fr">
    {block('Business Details', [('Legal Name', 'Bravo Laminate Traders'), ('GST Number', nw('27AAKFB3318D1ZP')), ('Business Type', 'Dealer'), ('Established', '2015')])}
    {block('Addresses', [('Shop', 'Shop 6, Laminate Market Road, Hadapsar, Pune, Postal Code 411028'), ('Godown', 'Godown 2, Hadapsar Godown Lane, Pune, Postal Code 411028')])}
    {card('Commercial Terms', kv([('Price Tier', 'Dealer Tier B'), ('Credit Limit', ML(BRV_LIMIT)), ('Outstanding Balance', ML(BRV_OWES)), ('Credit Used', f'<span class="inline-meter"><span class="meter ok"><i style="width:{cp_used}%"></i></span><b>{cp_used}%</b></span>'), ('Credit Period', '30 days')]))}
  </div>
  <section class="card flush"><header><h2>Contacts</h2><button class="btn sm" type="button" style="margin-left:auto"><i data-icon="plus"></i>Add Contact</button></header>
    <div class="body">{table([('Name', ''), ('Role', ''), ('Email', ''), ('Phone', '')], [contact_rows])}</div></section>
  <div class="grid g-2">
    {card('Relationship Manager', kv([('Name', '<b>Kavita Joshi</b>'), ('Role', 'Sales and Operations Manager'), ('Organisation', 'Distributor Alpha Private Limited'), ('Email', 'kavita.joshi@<wbr>distributoralpha.example'), ('Phone', '+91 90000 21002'), ('Territory', 'Pune District')]))}
    <section class="card flush"><header><h2>Documents</h2></header><div class="body">{table([('Document', ''), ('Type', ''), ('Date', ''), ('', '')], [doc_rows])}</div></section>
  </div>
'''
page('secondary', 'company-profile', 'SEC-PRO-01', 'Secondary Customer — Owner — Company Profile (SEC-PRO-01)', body)

# ---------- Product Catalogue ----------
cards = ''
for p in P:
    sku = p[0]; q = 100 if sku in ('LM-WNT-001', 'LM-ARC-002') else 25
    cards += f'''      <article class="card pcard"><a data-link="SEC-CAT-02" aria-label="{p[1]}">{sw(sku)}</a>
        <div class="in"><div><h3><a data-link="SEC-CAT-02" style="color:inherit">{p[1]}</a></h3></div>
          <div class="tags"><span class="tag mono">{sku}</span><span class="tag">{p[2]}</span><span class="tag">{p[3]}</span>{avail_chip(sku)}</div>
          <div><span class="label-top" style="margin-bottom:.25rem">Price per Sheet</span><div class="big-value" style="font-size:1.5rem">{M(dp(sku))}</div></div>
          <div class="buy">{qty(q)}<button class="btn pri" type="button"><i data-icon="plus"></i>Add to Order</button></div></div></article>
'''
body = f'''  <div class="head">
    <h1>Product Catalogue</h1>
    <div class="acts"><a class="btn pri" data-link="SEC-ORD-03"><i data-icon="cart"></i>Order Draft<span class="chip" style="margin-left:.25rem;background:#fff;color:var(--accent-ink);border:0">4</span></a></div>
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
page('secondary', 'product-catalogue', 'SEC-CAT-01', 'Secondary Customer — Owner — Product Catalogue (SEC-CAT-01)', body)

# ---------- Product Details (LM-WNT-001) ----------
sku = 'LM-WNT-001'; p = BY[sku]; b = BSTOCK[sku]
price_rows = ''.join(f'<tr><td>{a}</td><td class="num"><b>{M(v)}</b></td><td class="num">{M(v * 25)}</td></tr>' for a, v in [('Dealer Price', dp(sku)), ('Retailer Price', rp(sku))])
specs = [('SKU', sku), ('Finish', 'Woodgrain'), ('Thickness', '1.0 mm'), ('Sheet Size', '8 ft × 4 ft (2,440 mm × 1,220 mm)'), ('Weight per Sheet', '6.1 kg'), ('Grade', 'Decorative'), ('Pack Size', '25 sheets'), ('Colour Family', 'Brown')]
related = ['LM-WNG-011', 'LM-TEK-006', 'LM-OAK-004', 'LM-SLT-005']
rel = ''.join(f'<a class="card" data-link="SEC-CAT-02" style="overflow:hidden;color:inherit">{sw(r, "", "aspect-ratio:4/3;border-radius:0")}<div style="padding:.875rem 1rem"><b>{BY[r][1]}</b><div style="margin-top:.5rem;font-weight:620">{M(dp(r))} <span class="dim" style="font-weight:450">per sheet</span></div></div></a>' for r in related)
body = f'''  <div class="head">
    <div class="title-row"><h1>{p[1]}</h1>{chip('In Stock')}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Specification</button><a class="btn" data-link="SEC-INV-02"><i data-icon="stack"></i>View Inventory Item</a></div>
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
      <section class="card pad"><span class="label-top">Dealer Price per Sheet</span><div class="big-value">{M(dp(sku))}</div>
        <div class="field" style="margin-top:1.25rem"><label>Sheets to Order</label>{qty(60)}</div>
        <dl class="kv total" style="margin-top:1.25rem"><dt>Amount</dt><dd>{M(60 * dp(sku))}</dd></dl>
        <button class="btn pri block" type="button" style="margin-top:1rem"><i data-icon="plus"></i>Add to Order</button></section>
      {card('Your Stock', kv([('On Hand', f'{b["on_hand"]} sheets'), ('Reserved for Retailers', f'{b["reserved"]} sheets'), ('Available', f'<b>{b["available"]} sheets</b>'), ('On Order', f'{b["on_order"]} sheets'), ('Arriving', '30/10/2026'), ('Reorder Level', f'{b["level"]} sheets')]))}
      {card('Distributor Alpha Availability', kv([('Bhiwandi Warehouse', f'{N(BY[sku][10])} sheets'), ('Dispatch Time', '1 to 2 days')]))}
    </div>
  </div>
  <section><h2 style="margin-bottom:1rem">Related Products</h2><div class="products four">{rel}</div></section>
'''
page('secondary', 'product-details', 'SEC-CAT-02', 'Secondary Customer — Owner — Product Details (SEC-CAT-02)', body)

# ---------- Place Order ----------
QTY = dict(NEW_LINES)
rows = ''
for p in P:
    s = p[0]; q = QTY.get(s, 0)
    rows += (f'<tr><td><div class="prod">{sw(s)}<div><b>{p[1]}</b>{avail_chip(s)}</div></div></td><td class="mono nowrap">{s}</td>'
             f'<td class="num">{M(dp(s))}</td><td>{qty(q)}</td><td class="num"><b>{M(q * dp(s)) if q else "—"}</b></td></tr>\n')
draft = ''.join(f'<tr><td><b>{BY[s][1]}</b></td><td class="num">{N(q)}</td><td class="num"><b>{M(q * dp(s))}</b></td></tr>' for s, q in NEW_LINES)
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
        {kv([('Sheets', '210'), ('Freight', chip('Free', 'ok'))], '')}
        {kv([('Subtotal', M(NEW_SUB))], 'total')}
        <a class="btn pri block" data-link="SEC-ORD-04" style="margin-top:1.25rem">Continue to Order Details<i data-icon="arrow"></i></a>
        <button class="btn block" type="button" style="margin-top:.5rem">Save Draft</button></div></aside>
  </div>
'''
page('secondary', 'place-order', 'SEC-ORD-03', 'Secondary Customer — Owner — Place Order (SEC-ORD-03)', body)

# ---------- Order Builder ----------
item_rows = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td>{qty(q)}</td><td class="num">{M(dp(s))}</td>'
                    f'<td class="num"><b>{M(q * dp(s))}</b></td><td><button class="icon-btn" type="button" aria-label="Remove {BY[s][1]}"><i data-icon="trash"></i></button></td></tr>\n' for s, q in NEW_LINES)
used_after = round((BRV_OWES + NEW_TOTAL) / BRV_LIMIT * 100)
body = f'''  <div class="head">
    <h1>Order Builder</h1>
    <div class="acts"><a class="btn" data-link="SEC-ORD-03"><i data-icon="back"></i>Back to Products</a><button class="btn" type="button">Save Draft</button><a class="btn pri" data-link="SEC-ORD-05">Submit Order</a></div>
  </div>
  {steps(2)}
  <div class="grid g-main-side" style="--side:18rem">
    <div class="stack">
      <section class="card flush"><header><h2>Order Items</h2></header>
        <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', ''), ('Price per Sheet', 'num'), ('Amount', 'num'), ('', '')], [item_rows], 'stack-sm')}</div></section>
      <section class="card"><header><h2>Delivery</h2></header><div class="body"><div class="form-grid">
        <div class="field"><label for="loc">Delivery Location</label><select class="input" id="loc"><option>Shop and Godown, Hadapsar, Pune</option></select></div>
        <div class="field"><label for="date">Requested Delivery Date</label><input class="input" id="date" value="30/10/2026"></div>
        <div class="field"><label for="ref">Your Reference Number</label><input class="input" id="ref" placeholder="Reference from your records"></div>
        <div class="field"><label for="contact">Receiving Contact</label><input class="input" id="contact" value="Arjun Nair, +91 90000 31002"></div>
        <div class="full"><span class="label">Transport</span><div class="form-grid" style="margin-top:.375rem">
          <label class="radio on"><input type="radio" name="t" checked><span style="flex:1;display:flex;align-items:center;justify-content:space-between;gap:.75rem"><b>Distributor Transport</b>{chip('Free', 'ok')}</span></label>
          <label class="radio"><input type="radio" name="t"><span><b>Self Pickup</b></span></label></div></div>
        <div class="field full"><label for="notes">Order Notes</label><textarea class="input" id="notes" placeholder="Notes for the dispatch team"></textarea></div>
      </div></div></section>
    </div>
    <div class="stack">
      {card('Order Summary', kv([('Sheets', '210'), ('Subtotal', M(NEW_SUB)), ('Central GST 9%', M(NEW_GST)), ('State GST 9%', M(NEW_GST)), ('Freight', chip('Free', 'ok'))]) + kv([('Total', M(NEW_TOTAL))], 'total'))}
      <section class="card"><header><h2>Credit</h2></header><div class="body">
        {kv([('Credit Limit', ML(BRV_LIMIT)), ('Outstanding Balance', ML(BRV_OWES)), ('This Order', M(NEW_TOTAL))])}
        <span class="meter {meter_cls(used_after)}" style="margin-top:1rem"><i style="width:{used_after}%"></i></span>
        {kv([('Credit Available', ML(BRV_LIMIT - BRV_OWES - NEW_TOTAL))], 'total')}</div></section>
    </div>
  </div>
'''
page('secondary', 'order-builder', 'SEC-ORD-04', 'Secondary Customer — Owner — Order Builder (SEC-ORD-04)', body)

# ---------- Order Confirmation ----------
line_rows = ''.join(f'<tr><td><b>{BY[s][1]}</b></td><td class="num">{N(q)}</td><td class="num"><b>{M(q * dp(s))}</b></td></tr>' for s, q in NEW_LINES)
body = f'''  <div class="head"><h1>Order Confirmation</h1></div>
  {steps(4)}
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      <section class="card pad" style="display:grid;justify-items:center;gap:1.5rem;text-align:center;padding:2.25rem 1.5rem">
        <div class="state" style="padding:0;gap:.75rem"><div class="badge"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg></div>
          <h2 style="font-size:1.5rem">Order Submitted</h2><div class="big-value mono" style="font-size:1.375rem">{NEW_ORDER}</div></div>
        <div class="stats" style="--cols:1.6fr 2fr .8fr 1.3fr"><div><span>Placed</span><b>26/10/2026 16:05</b></div><div><span>Status</span>{chip('Awaiting Confirmation')}</div><div><span>Sheets</span><b>210</b></div><div><span>Total</span><b>{M(NEW_TOTAL)}</b></div></div>
        <div class="actions" style="display:flex;flex-wrap:wrap;gap:.75rem;justify-content:center"><a class="btn pri" data-link="SEC-ORD-02">View Order Details</a><a class="btn" data-link="SEC-ORD-03">Place Another Order</a><button class="btn" type="button"><i data-icon="download"></i>Download Order Copy</button></div>
      </section>
      <section class="card"><header><h2>Order Progress</h2></header><div class="body">
        <ol class="track"><li class="done"><i></i><b>Placed</b><span>26/10/2026</span></li><li class="now"><i></i><b>Confirmation</b><span>Pending</span></li><li class="todo"><i></i><b>Packing</b><span>28/10/2026</span></li><li class="todo"><i></i><b>Dispatch</b><span>28/10/2026</span></li><li class="todo"><i></i><b>Delivery</b><span>30/10/2026</span></li></ol></div></section>
    </div>
    <div class="stack">
      <section class="card"><header><h2>Order Summary</h2></header><div class="body"><div class="table-wrap" style="margin:-.25rem -1.125rem 0"><table class="tbl"><thead><tr><th>Product</th><th class="num">Sheets</th><th class="num">Amount</th></tr></thead><tbody>{line_rows}</tbody></table></div>
        {kv([('Central GST 9%', M(NEW_GST)), ('State GST 9%', M(NEW_GST))])}{kv([('Total', M(NEW_TOTAL))], 'total')}</div></section>
      {card('Delivery', kv([('Deliver To', 'Shop and Godown, Hadapsar, Pune'), ('Requested', '30/10/2026'), ('Transport', 'Distributor Transport'), ('Receiving Contact', 'Arjun Nair'), ('Placed By', 'Sunita Rao')]))}
      {card('Credit', kv([('Credit Limit', ML(BRV_LIMIT)), ('Credit Available', ML(BRV_LIMIT - BRV_OWES - NEW_TOTAL))]))}
    </div>
  </div>
'''
page('secondary', 'order-confirmation', 'SEC-ORD-05', 'Secondary Customer — Owner — Order Confirmation (SEC-ORD-05)', body)

# ---------- Order History ----------
rows = ''.join(f'<tr><td><a data-link="SEC-ORD-02"><b>{o}</b></a></td><td>{d}</td><td class="num">{N(sh)}</td><td class="num"><b>{M(v)}</b></td><td>{dl}</td><td>{chip(st)}</td><td>{pay_chip(pay)}</td><td><div class="row-actions"><a class="btn sm" data-link="SEC-ORD-02">View</a></div></td></tr>\n' for o, d, sh, v, dl, st, pay in H)
body = f'''  <div class="head">
    <h1>Order History</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Orders</button><a class="btn pri" data-link="SEC-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Orders This Month', '6')}
    {kpi('Order Value This Month', ML(684000), up(pct(684000, 610000)))}
    {kpi('In Transit', '1')}
    {kpi('Awaiting Confirmation', '1')}
  </div>
  <section class="card flush">
    {tabs([('All Orders', 212, True), ('Awaiting Confirmation', 1, False), ('In Transit', 1, False), ('Delivered', 208, False), ('Cancelled', 2, False)])}
    {filters('Search by order number or product', 'Search orders', ('Date Range', 'Last 90 days'), ('Payment', 'All'), ('Status', 'All'))}
    <div class="body">{table([('Order Number', ''), ('Order Date', ''), ('Sheets', 'num'), ('Value', 'num'), ('Delivery Date', ''), ('Order Status', ''), ('Payment', ''), ('', '')], [rows])}
      {pager('Showing 1 to 10 of 212 orders')}</div>
  </section>
'''
page('secondary', 'order-history', 'SEC-ORD-01', 'Secondary Customer — Owner — Order History (SEC-ORD-01)', body)

# ---------- Order Details (SAL-2026-3040) ----------
o = O40
lrows = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num">{N(q)}</td><td class="num">{M(dp(s))}</td><td class="num"><b>{M(q * dp(s))}</b></td></tr>' for s, q in o['lines'])
body = f'''  <div class="head">
    <div class="title-row"><h1>{o["number"]}</h1>{chip("In Transit")}{pay_chip("Unpaid")}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Order Copy</button><a class="btn" data-link="SEC-SUP-02" data-role="OWN"><i data-icon="help"></i>Raise Support Ticket</a><button class="btn pri" type="button"><i data-icon="repeat"></i>Reorder</button></div>
  </div>
  <section class="card pad"><ol class="track">
    <li class="done"><i></i><b>Placed</b><span>23/10/2026 16:40</span></li><li class="done"><i></i><b>Confirmed</b><span>24/10/2026 09:10</span></li><li class="done"><i></i><b>Packed</b><span>24/10/2026 13:30</span></li>
    <li class="now"><i></i><b>In Transit</b><span>24/10/2026 17:45</span></li><li class="todo"><i></i><b>Delivered</b><span>26/10/2026</span></li></ol></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      <section class="card flush"><header><h2>Items</h2></header>
        <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Price per Sheet', 'num'), ('Amount', 'num')], [lrows], foot=f'<tfoot><tr><td colspan="4">Subtotal</td><td class="num">{M(O40_SUB)}</td></tr></tfoot>')}
          <div style="padding:1rem 1.125rem"><dl class="kv" style="max-width:22rem;margin-left:auto"><dt>Trade Discount</dt><dd style="color:var(--ok)">{SQ}{M(O40_DISC)}</dd><dt>Taxable Amount</dt><dd>{M(O40_TAX)}</dd><dt>Central GST 9%</dt><dd>{M(O40_GST)}</dd><dt>State GST 9%</dt><dd>{M(O40_GST)}</dd></dl>
          <dl class="kv total" style="max-width:22rem;margin-left:auto"><dt>Total</dt><dd>{M(o["value"])}</dd></dl></div></div></section>
      <section class="card flush"><header><h2>Order Activity</h2></header><div class="body">{table([('Date', ''), ('Event', ''), ('By', '')], [
        '<tr><td class="nowrap">24/10/2026 17:45</td><td><b>Shipment dispatched</b></td><td>Distributor Alpha</td></tr>',
        '<tr><td class="nowrap">24/10/2026 13:30</td><td><b>Packing completed</b></td><td>Bhiwandi Warehouse</td></tr>',
        '<tr><td class="nowrap">24/10/2026 09:10</td><td><b>Order confirmed</b></td><td>Distributor Alpha</td></tr>',
        '<tr><td class="nowrap">23/10/2026 16:40</td><td><b>Order placed</b></td><td>Sunita Rao</td></tr>'])}</div></section>
    </div>
    <div class="stack">
      {card('Delivery', kv([('Dispatch Number', f'<span class="mono">{o["dispatch"]}</span>'), ('Deliver To', 'Shop and Godown, Hadapsar, Pune'), ('Expected', o['expected']), ('Dispatched From', 'Bhiwandi Warehouse'), ('Vehicle', 'MH 12 QR 4418'), ('Driver', 'Santosh Gaikwad'), ('Driver Phone', '+91 90000 12346')]))}
      <section class="card"><header><h2>Invoice</h2></header><div class="body">{kv([('Invoice Number', f'<span class="mono">{o["number"]}</span>'), ('Issued', '24/10/2026'), ('Due', '23/11/2026'), ('Amount', f'<b>{M(o["value"])}</b>'), ('Status', chip('Unpaid'))])}
        <a class="btn block" data-link="SEC-BIL-02" data-role="OWN" style="margin-top:1rem">View Invoice</a></div></section>
      {card('Order Information', kv([('Placed By', 'Sunita Rao'), ('Payment Terms', '30 days'), ('Transport', 'Distributor Transport'), ('Scheme', 'None'), ('Reference Number', 'DB-2026-203')]))}
    </div>
  </div>
'''
page('secondary', 'order-details', 'SEC-ORD-02', 'Secondary Customer — Owner — Order Details (SEC-ORD-02)', body)

# ---------- Inventory Overview ----------
def stock_bar(s):
    b = BSTOCK[s]; pct_ = 0 if b['on_hand'] == 0 else min(100, round(b['on_hand'] / (b['level'] * 3) * 100))
    return f'<span class="meter {"bad" if b["status"] == "Out of Stock" else "warn" if b["status"] == "Low Stock" else "ok"}" style="width:6rem"><i style="width:{pct_}%"></i></span>'
inv_rows = ''.join(f'''<tr><td><div class="prod">{sw(p[0])}<div><a data-link="SEC-INV-02"><b>{p[1]}</b></a></div></div></td><td class="mono nowrap">{p[0]}</td>
      <td class="num">{N(BSTOCK[p[0]]["on_hand"])}</td><td class="num">{N(BSTOCK[p[0]]["reserved"])}</td><td class="num"><b>{N(BSTOCK[p[0]]["available"])}</b></td><td class="num">{N(BSTOCK[p[0]]["on_order"]) if BSTOCK[p[0]]["on_order"] else "—"}</td><td class="num">{N(BSTOCK[p[0]]["level"])}</td><td>{chip(BSTOCK[p[0]]["status"])}</td></tr>
''' for p in P)
ship_rows = (f'<tr><td><a data-link="SEC-ORD-02"><b>{O40["number"]}</b></a></td><td class="num">{N(O40["sheets"])}</td><td>{O40["expected"]}</td><td>{chip("In Transit")}</td></tr>'
             f'<tr><td><a data-link="SEC-ORD-02"><b>{NEW_ORDER}</b></a></td><td class="num">210</td><td>30/10/2026</td><td>{chip("Awaiting Confirmation")}</td></tr>')
body = f'''  <div class="head">
    <h1>Inventory Overview</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Stock</button><a class="btn pri" data-link="SEC-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Sheets on Hand', N(1058))}
    {kpi('Stock Value', ML(BSTOCK_VALUE))}
    {kpi('Reserved for Retailers', f'{N(261)} <small>sheets</small>')}
    {kpi('Arriving From Distributor Alpha', f'{N(310)} <small>sheets</small>')}
  </div>
  <div class="grid g-2" style="--cols:.8fr 1.2fr">
    <section class="card"><header><h2>Stock Health</h2></header><div class="body center">{chart('donut', series=[{'name': 'In Stock', 'value': 8, 'color': 'var(--ok)'}, {'name': 'Low Stock', 'value': 3, 'color': '#e0a030'}, {'name': 'Out of Stock', 'value': 1, 'color': 'var(--bad)'}], center='12', caption='products')}</div></section>
    <section class="card flush"><header><h2>Incoming Shipments</h2></header><div class="body">{table([('Order', ''), ('Sheets', 'num'), ('Expected', ''), ('Status', '')], [ship_rows])}<div style="padding:.5rem 1.125rem 1rem">{kv([('Sheets Arriving', '310')], 'total')}</div></div></section>
  </div>
  <section class="card flush">
    {tabs([('All Products', 12, True), ('In Stock', 8, False), ('Low Stock', 3, False), ('Out of Stock', 1, False)])}
    {filters('Search by product name or SKU', 'Search stock', ('Finish', 'All'), ('Thickness', 'All'))}
    <div class="body">{table([('Product', ''), ('SKU', ''), ('On Hand', 'num'), ('Reserved', 'num'), ('Available', 'num'), ('On Order', 'num'), ('Reorder Level', 'num'), ('Status', '')], [inv_rows])}</div></section>
'''
page('secondary', 'inventory-overview', 'SEC-INV-01', 'Secondary Customer — Owner — Inventory Overview (SEC-INV-01)', body)

# ---------- Inventory Item Details (LM-CAL-003) ----------
sku = 'LM-CAL-003'; p = BY[sku]; b = BSTOCK[sku]
dates = ['27/07/2026', '03/08/2026', '10/08/2026', '17/08/2026', '24/08/2026', '31/08/2026', '07/09/2026', '14/09/2026', '21/09/2026', '28/09/2026', '05/10/2026', '12/10/2026', '19/10/2026', '26/10/2026']
levels = [58, 52, 47, 41, 75, 69, 63, 57, 51, 46, 42, 53, 48, 38]            # weekly closing levels; October follows the movement balances below
mv_rows = ''.join(f'<tr><td>{m["date"]}</td><td>{chip(m["type"], "ok" if m["type"] == "Receipt" else "blue")}</td><td>{m["who"]}</td><td class="mono nowrap">{m["ref"]}</td><td class="num"><b>{"+" if m["sheets"] > 0 else SQ}{abs(m["sheets"])}</b></td><td class="num">{N(m["balance"])}</td></tr>' for m in BCAL)
cover = round(b['available'] / (BCAL_SOLD / 26))
body = f'''  <div class="head">
    <div class="title-row"><h1>{p[1]}</h1>{chip(b["status"])}</div>
    <div class="acts"><a class="btn" data-link="SEC-CAT-02"><i data-icon="box"></i>View Product</a><a class="btn pri" data-link="SEC-ORD-03"><i data-icon="plus"></i>Reorder</a></div>
  </div>
  <div class="kpis">
    {kpi('On Hand', f'{b["on_hand"]} <small>sheets</small>')}
    {kpi('Reserved for Retailers', f'{b["reserved"]} <small>sheets</small>')}
    {kpi('Available', f'{b["available"]} <small>sheets</small>', '<span class="delta down">Below Reorder Level</span>')}
    {kpi('On Order', f'{b["on_order"]} <small>sheets</small>', f'<span class="delta flat">Arriving {O40["expected"]}</span>')}
    {kpi('Days of Cover', f'{cover} <small>days</small>')}
  </div>
  <div class="grid g-main-side" style="--side:19rem">
    <div class="stack">
      {card('Stock Level', chart('line', dates, [{'name': 'Sheets on hand', 'values': levels, 'color': 'var(--accent)'}, {'name': 'Reorder level', 'values': [b['level']] * 14, 'color': 'var(--bad)', 'dots': False}], area=True))}
      <section class="card flush"><header><h2>Stock Movements</h2><a class="more" data-link="SEC-INV-01">Inventory overview</a></header>
        <div class="body">{table([('Date', ''), ('Type', ''), ('Retailer or Distributor', ''), ('Reference', ''), ('Sheets', 'num'), ('Balance', 'num')], [mv_rows])}</div></section>
    </div>
    <div class="stack">
      <section class="card pad" style="display:grid;gap:1rem">{sw(sku, 'lg', 'aspect-ratio:16/9')}{kv([('SKU', f'<span class="mono">{sku}</span>'), ('Finish', p[2]), ('Thickness', p[3]), ('Sheet Size', '8 ft × 4 ft')])}</section>
      <section class="card flush"><header><h2>Batches</h2></header><div class="body">{table([('Batch', ''), ('Received', ''), ('Sheets', 'num')], ['<tr><td class="mono">B-2610-19</td><td>10/10/2026</td><td class="num">25</td></tr>', '<tr><td class="mono">B-2609-08</td><td>12/09/2026</td><td class="num">13</td></tr>'])}</div></section>
      <section class="card"><header><h2>Reorder Settings</h2><button class="btn sm" type="button" style="margin-left:auto"><i data-icon="edit"></i>Edit</button></header><div class="body">{kv([('Reorder Level', f'{b["level"]} sheets'), ('Reorder Quantity', '100 sheets'), ('Lead Time', '2 days'), ('Preferred Location', 'Hadapsar Godown')])}</div></section>
    </div>
  </div>
'''
page('secondary', 'inventory-item-details', 'SEC-INV-02', 'Secondary Customer — Owner — Inventory Item Details (SEC-INV-02)', body)

# ---------- Retailer Network ----------
net_rows = ''
for r in RETAILERS:
    k = r[0]; cu = credit_pct(RTL_OWES[k], r[6])
    net_rows += (f'<tr><td class="nowrap">{link("SEC-RTL-02", r[1])} <span class="tag">{r[3]}</span></td><td>{chip("Active")}</td><td class="num">{N(RTL_SHEETS[k])}</td><td class="num"><b>{M(r[9][-1])}</b></td><td class="num">{M(RTL_OWES[k]) if RTL_OWES[k] else "—"}</td>'
                 f'<td><span class="inline-meter"><span class="meter {meter_cls(cu)}"><i style="width:{cu}%"></i></span><b>{cu}%</b></span></td><td>{RTL_LAST[k]}</td></tr>')
body = f'''  <div class="head">
    <h1>Retailer Network</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Retailers</button><a class="btn pri" data-link="SEC-RTL-03" data-role="OWN"><i data-icon="plus"></i>Add Retailer Request</a></div>
  </div>
  <div class="kpis">
    {kpi('Retailers', '3', chip('All Active', 'ok'))}
    {kpi('Sales This Month', ML(630000), up(pct(630000, 600000)))}
    {kpi('Owed by Retailers', ML(sum(RTL_OWES.values())))}
    {kpi('Sheets Sold', N(370))}
  </div>
  <section class="card flush">
    {tabs([('All Retailers', 3, True), ('Active', 3, False)])}
    {filters('Search by retailer name or area', 'Search retailers', ('City', 'All'), ('Status', 'All'), ('Sort by', 'Sales This Month'))}
    <div class="body">{table([('Retailer', ''), ('Status', ''), ('Sheets', 'num'), ('Sales This Month', 'num'), ('Owes', 'num'), ('Credit Used', ''), ('Last Sale', '')], [net_rows],
      foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(370)}</td><td class="num">{M(630000)}</td><td class="num">{M(sum(RTL_OWES.values()))}</td><td colspan="2"></td></tr></tfoot>')}
      {pager('Showing 1 to 3 of 3 retailers', 1)}</div>
  </section>
'''
page('secondary', 'retailer-network', 'SEC-RTL-01', 'Secondary Customer — Owner — Retailer Network (SEC-RTL-01)', body)

# ---------- Retailer Details (Retailer Charlie) ----------
r = RTL['CHR']; rs = [s for s in TSALES if s['retailer'] == 'CHR']; cu = credit_pct(RTL_OWES['CHR'], r[6])
assert r[9][-1] == 264000 and r[9][-2] == r[8]
sale_rows = ''.join(f'<tr><td class="mono nowrap"><b>{s["number"]}</b></td><td>{s["date"]}</td><td class="num">{N(s["sheets"])}</td><td class="num"><b>{M(s["value"])}</b></td><td>{pay_chip(s["payment"])}</td></tr>' for s in rs)
rcontacts = [('Imran Sheikh', 'Retailer Owner', '+91 90000 51001'), ('Pooja Verma', 'Sales Executive', '+91 90000 51002'), ('Faisal Khan', 'Inventory and Purchasing Executive', '+91 90000 51003')]
body = f'''  <div class="head">
    <div class="title-row"><h1>{r[1]}</h1>{chip("Active")}<span class="tag"><i data-icon="pin"></i>{r[3]}</span></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Statement</button><a class="btn pri" data-link="SEC-TSL-02"><i data-icon="plus"></i>Record Sale</a></div>
  </div>
  <div class="kpis">
    {kpi('Sales This Month', ML(r[9][-1]), up(pct(r[9][-1], r[8])))}
    {kpi('Owes', ML(RTL_OWES['CHR']))}
    {kpi('Credit Limit', ML(r[6]))}
    {kpi('Sheets This Month', N(RTL_SHEETS['CHR']))}
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    {card('Sales by Month', chart('bars', MONTHS, [{'name': 'Sales to Retailer Charlie', 'values': r[9], 'color': 'var(--accent)'}], money=True, height=330))}
    {card('Account', kv([('Price Tier', 'Retailer Tier C'), ('Credit Limit', ML(r[6])), ('Credit Used', f'<span class="inline-meter"><span class="meter {meter_cls(cu)}"><i style="width:{cu}%"></i></span><b>{cu}%</b></span>'),
                         ('Credit Period', f'{r[7]} days'), ('Customer Since', r[5]), ('Area', r[2]), ('Relationship Manager', 'Arjun Nair'),
                         ('GST Number', '<span style="white-space:nowrap">27AAJCC4410E1ZK</span>'), ('Address', 'Shop 12, MG Road, Camp, Pune, Postal Code 411001')]))}
  </div>
  <section class="card flush"><header><h2>Recent Sales</h2><a class="more" data-link="SEC-TSL-03">All sales</a></header>
    <div class="body">{table([('Sale Number', ''), ('Date', ''), ('Sheets', 'num'), ('Value', 'num'), ('Payment', '')], [sale_rows])}</div></section>
  <section class="card flush"><header><h2>Contacts</h2></header>
    <div class="body">{table([('Name', ''), ('Role', ''), ('Phone', '')], [f'<tr><td class="nowrap"><b>{n}</b></td><td>{ro}</td><td class="nowrap">{ph}</td></tr>' for n, ro, ph in rcontacts])}</div></section>
'''
page('secondary', 'retailer-details', 'SEC-RTL-02', 'Secondary Customer — Owner — Retailer Details (SEC-RTL-02)', body)

# ---------- Add Retailer Request ----------
nr = RETAILER_REQUEST
stepsl = [('Submit Request', 'Draft', 'plain'), ('Dealer Review: Arjun Nair', 'Pending', 'warn'), ('Distributor Approval: Kavita Joshi', 'Pending', 'warn'), ('Retailer Activated', 'Pending', 'warn')]
approval = '<ul class="list">' + ''.join(f'<li><div class="grow"><b>{n}</b></div>{chip(c, k)}</li>' for n, c, k in stepsl) + '</ul>'
def upload(name, fname=None):
    inner = f'<span class="file"><i data-icon="doc"></i>{fname}</span>' if fname else ''
    return f'<div class="drop"><b>{name}</b>{inner}<button class="btn sm" type="button"><i data-icon="upload"></i>{"Replace" if fname else "Upload"}</button></div>'
body = f'''  <div class="head">
    <h1>Add Retailer Request</h1>
    <div class="acts"><a class="btn" data-link="SEC-RTL-01">Cancel</a><button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Submit Request</button></div>
  </div>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      {form('Business Details', fld('Retailer Business Name', 'bn', nr[0]), fld('Legal Name', 'ln', 'Dhruv Interiors and Furnishings'), fld('Business Type', 'bt', 'Retailer', 'select', ['Retailer', 'Fabricator', 'Interior Contractor']),
            fld('GST Number', 'gst', nr[4]), fld('Permanent Account Number', 'pan', 'AAHFD6620L'), fld('Expected Monthly Volume in Sheets', 'vol', str(nr[6])))}
      {form('Owner Contact', fld('Owner Name', 'on', nr[3]), fld('Mobile Number', 'mob', '+91 90000 52001'), fld('Email Address', 'em', 'dhruv.patil@retailerdhruv.example', full=True))}
      {form('Address', fld('Address', 'ad', 'Shop 4, Wakad Road', full=True), fld('Area', 'ar', nr[1]), fld('City', 'ct', nr[2]), fld('State', 'st', 'Maharashtra', 'select', ['Maharashtra', 'Goa']), fld('Postal Code', 'pc', '411057'))}
      {form('Proposed Terms', fld('Price Tier', 'pt', 'Retailer Tier C', 'select', ['Retailer Tier A', 'Retailer Tier B', 'Retailer Tier C']), fld('Requested Credit Limit', 'cl', M(nr[5])), fld('Credit Period', 'cp', '15 days', 'select', ['Immediate', '15 days', '30 days']))}
      <section class="card"><header><h2>Documents</h2></header><div class="body"><div class="stack">
        {upload('GST Registration Certificate', 'gst-certificate.pdf')}{upload('Shop Licence', 'shop-licence.pdf')}{upload('Address Proof')}</div></div></section>
    </div>
    <div class="stack">{card('Approval Path', approval)}
      {card('Request Summary', kv([('Retailer', nr[0]), ('Area', nr[1]), ('Requested Credit', ML(nr[5])), ('Documents Attached', '2 of 3')]))}</div>
  </div>
'''
page('secondary', 'add-retailer-request', 'SEC-RTL-03', 'Secondary Customer — Owner — Add Retailer Request (SEC-RTL-03)', body)
