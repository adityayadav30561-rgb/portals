"""Phase 2, part A: Primary Customer Owner: Dashboard, Company Profile, Product Catalogue, Product Details."""
from data import *

# ---------- Dashboard ----------
months = ['May','June','July','August','September','October']
purch = [2210000,2560000,1980000,2740000,2430000,3352882]
sales = [2480000,2810000,2240000,3060000,2790000,3120000]
finish = [('Matte',2910,'#0a48fd'),('Woodgrain',2680,'#0b8fa8'),('Texture',640,'#7a36fb'),('Gloss',465,'#e0a030'),('Suede',410,'#0c9b6a'),('High Gloss',215,'#d43a2f'),('Metallic',95,'#8b93a3')]
orders = [('ORD-2026-10482','26/10/2026',760,949752,'Awaiting Confirmation'),('ORD-2026-10459','23/10/2026',280,336500,'Confirmed'),
          ('ORD-2026-10447','19/10/2026',360,442930,'In Transit'),('ORD-2026-10431','15/10/2026',520,618400,'Delivered'),('ORD-2026-10398','08/10/2026',430,524100,'Delivered')]
order_rows = ''.join(f'<tr><td><a data-link="PRI-ORD-02"><b>{o}</b></a></td><td>{d}</td><td class="num">{N(s)}</td><td class="num">{M(v)}</td><td>{chip(st)}</td></tr>' for o,d,s,v,st in orders)
dealers = [('Dealer Bravo','Pune',684000),('Dealer Delta','Nashik',592000),('Dealer Foxtrot','Thane',476000),('Dealer Gopal','Kolhapur',411000),('Dealer Harsh','Nagpur',338000)]
dealer_rows = ''.join(f'<li><div class="grow"><b>{n}</b><span class="sub">{c}</span><span class="meter" style="margin-top:.375rem"><i style="width:{v/684000*100:.0f}%"></i></span></div><b>{M(v)}</b></li>' for n,c,v in dealers)

body = f'''  <div class="head">
    <div><h1>Dashboard</h1><p>Distributor Alpha · 1 October to 26 October 2026</p></div>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span>
      <button class="btn" type="button"><i data-icon="download"></i>Download Report</button>
      <a class="btn pri" data-link="PRI-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>

  <div class="kpis">
    <div class="card kpi"><label>Purchases This Month</label><strong>{M(3352882)}</strong><div class="foot"><span class="delta up">+38.0%</span><span>compared with September</span></div></div>
    <div class="card kpi"><label>Sales to Dealers This Month</label><strong>{M(3120000)}</strong><div class="foot"><span class="delta up">+11.8%</span><span>compared with September</span></div></div>
    <div class="card kpi"><label>Outstanding Balance</label><strong>{M(1486320)}</strong><div class="foot"><span class="delta down">{M(318400)} overdue</span><span>37% of credit limit used</span></div></div>
    <div class="card kpi"><label>Stock on Hand</label><strong>7,415 <small>sheets</small></strong><div class="foot"><span class="delta flat">{M(7842000)}</span><span>3 products low</span></div></div>
  </div>

  <div class="grid g-chart">
    <section class="card"><header><h2>Purchases and Sales to Dealers</h2><span class="meta">May to October 2026</span></header>
      <div class="body">{chart('bars', months, [{'name':'Purchases from Crestline','values':purch,'color':'var(--accent)'},{'name':'Sales to Dealers','values':sales,'color':'var(--teal)'}], money=True)}</div></section>
    <section class="card"><header><h2>Stock by Finish</h2><span class="meta">sheets on hand</span></header>
      <div class="body">{chart('donut', series=[{'name':n,'value':v,'color':c} for n,v,c in finish], center='7,415', caption='sheets')}</div></section>
  </div>

  <div class="grid g-main-side">
    <section class="card flush"><header><h2>Recent Orders</h2><a class="more" data-link="PRI-ORD-01">View all orders</a></header>
      <div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Order Number</th><th>Date</th><th class="num">Sheets</th><th class="num">Value</th><th>Status</th></tr></thead><tbody>{order_rows}</tbody></table></div></div></section>
    <section class="card"><header><h2>Top Dealers This Month</h2><a class="more" data-link="PRI-DLR-01">All dealers</a></header>
      <div class="body"><ul class="list">{dealer_rows}</ul></div></section>
  </div>

  <div class="grid g-2">
    <section class="card"><header><h2>Stock Alerts</h2><a class="more" data-link="PRI-INV-01">Inventory overview</a></header>
      <div class="body"><ul class="list">
        <li>{sw('LM-STN-009','','width:2.5rem;flex:none')}<div class="grow"><b>Carrara Stone Finish Laminate</b><span class="sub">LM-STN-009 · 250 sheets on order</span></div>{chip('Out of Stock')}</li>
        <li>{sw('LM-CHR-007','','width:2.5rem;flex:none')}<div class="grow"><b>Charcoal Black Gloss Laminate</b><span class="sub">LM-CHR-007 · 60 available, reorder level 200</span></div>{chip('Low Stock')}</li>
        <li>{sw('LM-CAL-003','','width:2.5rem;flex:none')}<div class="grow"><b>Calacatta Marble Finish Laminate</b><span class="sub">LM-CAL-003 · 125 available, reorder level 250</span></div>{chip('Low Stock')}</li>
      </ul></div></section>
    <section class="card"><header><h2>Active Schemes</h2><a class="more" data-link="PRI-SCH-01">All schemes</a></header>
      <div class="body"><ul class="list">
        <li><div class="grow"><b>Festive Volume Rebate</b><span class="sub">2% rebate on 3,000 sheets across October and November · ends 30 November 2026</span>
          <span class="meter ok" style="margin-top:.5rem"><i style="width:92%"></i></span><span class="sub" style="margin-top:.25rem">2,750 of 3,000 sheets</span></div></li>
        <li><div class="grow"><b>Marble Finish Launch Incentive</b><span class="sub">{M(25)} per sheet of Calacatta Marble Finish · ends 31 December 2026</span>
          <span class="meter" style="margin-top:.5rem"><i style="width:60%"></i></span><span class="sub" style="margin-top:.25rem">180 of 300 sheets</span></div></li>
      </ul></div></section>
  </div>
'''
page('primary','owner-dashboard','PRI-OWN-01','Primary Customer — Owner — Dashboard (PRI-OWN-01)', body)

# ---------- Company Profile ----------
def block(title, rows, extra=''):
    kv = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in rows)
    return f'<section class="card"><header><h2>{title}</h2></header><div class="body"><dl class="kv">{kv}</dl>{extra}</div></section>'
contacts = [('Rajesh Menon','Owner','rajesh.menon@distributoralpha.example','+91 90000 21001'),('Kavita Joshi','Sales and Operations Manager','kavita.joshi@distributoralpha.example','+91 90000 21002'),('Suresh Iyer','Accountant','suresh.iyer@distributoralpha.example','+91 90000 21003')]
contact_rows = ''.join(f'<tr><td><b>{n}</b></td><td>{r}</td><td style="overflow-wrap:anywhere">{e}</td><td class="nowrap">{p}</td></tr>' for n,r,e,p in contacts)
body = f'''  <div class="head">
    <div><h1>Company Profile</h1><p>Customer since 12 April 2018</p></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Profile</button><button class="btn pri" type="button"><i data-icon="edit"></i>Edit Profile</button></div>
  </div>

  <section class="card pad" style="display:flex;align-items:center;gap:1.25rem;flex-wrap:wrap">
    <div class="org" style="margin:0;padding:0;border:0;background:none"><i style="width:4rem;height:4rem;border-radius:1rem;font-size:1.25rem">DA</i></div>
    <div style="flex:1;min-width:14rem"><div class="title-row"><h2 style="font-size:1.25rem">Distributor Alpha Private Limited</h2>{chip('Active','ok')}</div>
      <p class="sub" style="font-size:.875rem;margin-top:.25rem">Bhiwandi, Maharashtra · Primary Distributor Tier A · Territory: Maharashtra and Goa</p></div>
    <dl class="kv left" style="grid-template-columns:auto auto;gap:.375rem 1rem"><dt>Customer Code</dt><dd class="mono">CUS-0018</dd><dt>Account Manager</dt><dd>Vikram Chopra</dd></dl>
  </section>

  <div class="grid g-main-side">
    <div class="stack">
      <div class="grid g-2">
        {block('Business Details', [('Legal Name','Distributor Alpha Private Limited'),('GST Number','<span class="nowrap" style="white-space:nowrap">27AABCD4521F1Z7</span>'),('Permanent Account Number','AABCD4521F'),('Business Type','Distributor'),('Established','2011')])}
        {block('Addresses', [('Registered Office','Plot 14, Bhiwandi Logistics Park, Thane District, Maharashtra, Postal Code 421302'),('Pune Warehouse','Survey 88, Hadapsar Industrial Estate, Pune, Postal Code 411013')])}
      </div>
      <section class="card flush"><header><h2>Contacts</h2><button class="btn sm" type="button" style="margin-left:auto"><i data-icon="plus"></i>Add Contact</button></header>
        <div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Name</th><th>Role</th><th>Email</th><th>Phone</th></tr></thead><tbody>{contact_rows}</tbody></table></div></div></section>
    </div>
    <div class="stack">
      <section class="card"><header><h2>Commercial Terms</h2></header><div class="body">
        <dl class="kv"><dt>Price Tier</dt><dd>Primary Distributor Tier A</dd><dt>Credit Limit</dt><dd>{M(4000000)}</dd><dt>Credit Period</dt><dd>45 days</dd><dt>Outstanding Balance</dt><dd>{M(1486320)}</dd></dl>
        <span class="meter warn" style="margin-top:.875rem"><i style="width:37%"></i></span><p class="sub" style="margin-top:.375rem">37% of the credit limit is used</p></div></section>
      <section class="card"><header><h2>Account Manager</h2></header><div class="body">
        <div class="list"><li style="padding-top:0"><span class="who"><span class="av" style="display:grid">VC</span></span><div class="grow"><b>Vikram Chopra</b><span class="sub">Sales Manager, Crestline Laminates</span></div></li></div>
        <ul class="list" style="margin-top:.5rem;font-size:.8125rem"><li style="padding:.375rem 0;border:0"><i data-icon="mail"></i><span>vikram.chopra@crestlinelaminates.example</span></li><li style="padding:.375rem 0;border:0"><i data-icon="phone"></i><span>+91 90000 11223</span></li></ul></div></section>
      <section class="card"><header><h2>Documents</h2></header><div class="body"><ul class="list">
        <li><i data-icon="doc"></i><div class="grow"><b>GST Registration Certificate</b><span class="sub">PDF · uploaded 18/04/2018</span></div><button class="btn sm" type="button"><i data-icon="download"></i></button></li>
        <li><i data-icon="doc"></i><div class="grow"><b>Trade Licence</b><span class="sub">PDF · renewed 02/04/2026</span></div><button class="btn sm" type="button"><i data-icon="download"></i></button></li>
        <li><i data-icon="doc"></i><div class="grow"><b>Distributor Agreement 2026–27</b><span class="sub">PDF · signed 02/04/2026</span></div><button class="btn sm" type="button"><i data-icon="download"></i></button></li>
      </ul></div></section>
    </div>
  </div>
'''
page('primary','company-profile','PRI-PRO-01','Primary Customer — Owner — Company Profile (PRI-PRO-01)', body)

# ---------- Product Catalogue ----------
avail = {'LM-STN-009':('Low Stock','warn')}
cards = ''
for p in P:
    sku = p[0]; a = avail.get(sku, ('In Stock','ok'))
    q = 200 if sku in ('LM-WNT-001','LM-ARC-002') else 50
    cards += f'''      <article class="card pcard"><a data-link="PRI-CAT-02" aria-label="{p[1]}">{sw(sku)}</a>
        <div class="in"><div><h3><a data-link="PRI-CAT-02" style="color:inherit">{p[1]}</a></h3><span class="sub mono">{sku}</span></div>
          <div class="tags"><span class="tag">{p[2]}</span><span class="tag">{p[3]}</span>{chip(a[0], a[1])}</div>
          <div class="price">{M(p[4][0])} <small>per sheet</small><span class="sub">{M(p[4][2])} for 200 sheets or more</span></div>
          <div class="buy">{qty(q)}<button class="btn pri" type="button"><i data-icon="plus"></i>Add to Order</button></div></div></article>
'''
body = f'''  <div class="head">
    <div><h1>Product Catalogue</h1><p>12 products · prices per sheet before GST for Primary Distributor Tier A</p></div>
    <div class="acts"><a class="btn pri" data-link="PRI-ORD-03"><i data-icon="cart"></i>View Order Draft (5 products)</a></div>
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
page('primary','product-catalogue','PRI-CAT-01','Primary Customer — Owner — Product Catalogue (PRI-CAT-01)', body)

# ---------- Product Details ----------
sku = 'LM-WNT-001'; p = BY[sku]
slabs = [('1 to 49 sheets',p[4][0]),('50 to 199 sheets',p[4][1]),('200 sheets or more',p[4][2])]
slab_rows = ''.join(f'<tr{" class=hl" if i==2 else ""}><td>{a}</td><td class="num"><b>{M(b)}</b></td><td class="num">{M(b*25)}</td></tr>' for i,(a,b) in enumerate(slabs))
specs = [('Finish','Woodgrain'),('Thickness','1.0 mm'),('Sheet Size','8 ft × 4 ft (2,440 mm × 1,220 mm)'),('Weight per Sheet','6.1 kg'),('Grade','Decorative'),('Pack Size','25 sheets'),('Colour Family','Brown')]
spec_kv = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in specs)
related = ['LM-WNG-011','LM-TEK-006','LM-OAK-004','LM-SLT-005']
rel = ''.join(f'<a class="card" data-link="PRI-CAT-02" style="overflow:hidden;color:inherit">{sw(r,'','aspect-ratio:4/3;border-radius:0')}<div style="padding:.75rem .875rem"><b style="font-size:.875rem">{BY[r][1]}</b><span class="sub">{BY[r][0]} · {M(BY[r][4][0])} per sheet</span></div></a>' for r in related)
body = f'''  <div class="head">
    <div><div class="title-row"><h1>{p[1]}</h1>{chip('In Stock')}</div><p class="mono">{sku}</p></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Specification</button><a class="btn" data-link="PRI-INV-02"><i data-icon="stack"></i>View Inventory Item</a></div>
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      <section class="card pad"><div style="display:grid;grid-template-columns:minmax(0,1fr) 5rem;gap:1rem">
        {sw(sku,'lg','aspect-ratio:4/3')}
        <div style="display:grid;gap:.75rem;align-content:start">{''.join(sw(sku,'','outline:2px solid var(--accent);outline-offset:2px;' if i==0 else '') for i in range(4))}</div></div></section>
      <div class="grid g-2">
        <section class="card"><header><h2>Specifications</h2></header><div class="body"><dl class="kv">{spec_kv}</dl></div></section>
        <section class="card flush"><header><h2>Price per Sheet</h2><span class="meta">before GST</span></header><div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Quantity</th><th class="num">Per Sheet</th><th class="num">Per Pack of 25</th></tr></thead><tbody>{slab_rows}</tbody></table></div></div></section>
      </div>
    </div>
    <div class="stack">
      <section class="card pad"><div class="price" style="font-size:1.75rem;font-weight:650;letter-spacing:-.03em">{M(p[4][0])} <small style="font-size:.875rem;color:var(--ink-3);font-weight:450">per sheet</small></div>
        <p class="sub" style="margin-top:.25rem">{M(p[4][2])} per sheet for 200 sheets or more</p>
        <div class="field" style="margin-top:1rem"><label>Sheets to Order</label>{qty(200)}</div>
        <div class="kv" style="margin-top:1rem"><dt>Amount</dt><dd><b>{M(200*p[4][2])}</b></dd></div>
        <button class="btn pri block" type="button" style="margin-top:1rem"><i data-icon="plus"></i>Add to Order</button></section>
      <section class="card"><header><h2>Your Stock</h2><span class="meta">Bhiwandi and Pune warehouses</span></header><div class="body"><dl class="kv"><dt>On Hand</dt><dd>1,240 sheets</dd><dt>Reserved for Dealers</dt><dd>310 sheets</dd><dt>Available</dt><dd><b>930 sheets</b></dd><dt>On Order</dt><dd>600 sheets, arriving 30/10/2026</dd><dt>Reorder Level</dt><dd>400 sheets</dd></dl></div></section>
      <section class="card"><header><h2>Crestline Availability</h2></header><div class="body"><dl class="kv"><dt>Plant Warehouse, Vapi</dt><dd>12,400 sheets</dd><dt>Dispatch Time</dt><dd>2 to 3 days</dd></dl></div></section>
    </div>
  </div>
  <section><h2 style="margin-bottom:.75rem">Related Products</h2><div class="products four">{rel}</div></section>
'''
page('primary','product-details','PRI-CAT-02','Primary Customer — Owner — Product Details (PRI-CAT-02)', body)
