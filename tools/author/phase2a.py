"""Phase 2, part A: Primary Customer Owner: Dashboard, Company Profile, Product Catalogue, Product Details.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Information is carried by
titles, labels, values, chips, meters and tables."""
from data import *

# ---------- Dashboard ----------
months = ['May','June','July','August','September','October']
purch = [2210000,2560000,1980000,2740000,2430000,3352882]
sales = [2480000,2810000,2240000,3060000,2790000,3120000]
finish = [('Matte',2910,'#0a48fd'),('Woodgrain',2680,'#0b8fa8'),('Texture',640,'#7a36fb'),('Gloss',465,'#e0a030'),('Suede',410,'#0c9b6a'),('High Gloss',215,'#d43a2f'),('Metallic',95,'#8b93a3')]
orders = [('ORD-2026-10482','26/10/2026',760,949752,'Awaiting Confirmation'),('ORD-2026-10459','23/10/2026',280,336500,'Confirmed'),
          ('ORD-2026-10447','19/10/2026',360,442930,'In Transit'),('ORD-2026-10431','15/10/2026',520,618400,'Delivered'),
          ('ORD-2026-10398','08/10/2026',430,524100,'Delivered'),('ORD-2026-10372','01/10/2026',400,481200,'Delivered'),('ORD-2026-10341','24/09/2026',470,572300,'Delivered')]
order_rows = ''.join(f'<tr><td><a data-link="PRI-ORD-02"><b>{o}</b></a></td><td>{d}</td><td class="num">{N(s)}</td><td class="num">{M(v)}</td><td>{chip(st)}</td></tr>' for o,d,s,v,st in orders)
dealers = [('Dealer Bravo','Pune',684000),('Dealer Delta','Nashik',592000),('Dealer Foxtrot','Thane',476000),('Dealer Gopal','Kolhapur',411000),('Dealer Harsh','Nagpur',338000)]
dealer_rows = ''.join(f'<li><div class="grow"><div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap"><b>{n}</b><span class="tag">{c}</span></div><span class="meter" style="margin-top:.625rem"><i style="width:{v/684000*100:.0f}%"></i></span></div><b>{ML(v)}</b></li>' for n,c,v in dealers)
alerts = [('LM-STN-009',0,150),('LM-CHR-007',60,200),('LM-CAL-003',125,250)]
alert_rows = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num"><b>{N(a)}</b></td><td class="num">{N(r)}</td><td>{chip(BY[s][13])}</td></tr>' for s,a,r in alerts)
def scheme(name, ends, done, goal, pct, cls):
    return f'''<li style="display:block"><div style="display:flex;align-items:center;gap:.75rem;flex-wrap:wrap"><b style="flex:1;min-width:10rem">{name}</b><span class="chip plain">Ends {ends}</span></div>
          <span class="meter {cls}" style="margin-top:.75rem"><i style="width:{pct}%"></i></span>
          <div style="display:flex;justify-content:space-between;margin-top:.5rem"><b>{N(done)} sheets</b><span class="sub">{N(goal)} sheets</span></div></li>'''

body = f'''  <div class="head">
    <h1>Dashboard</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span>
      <button class="btn" type="button"><i data-icon="download"></i>Download Report</button>
      <a class="btn pri" data-link="PRI-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>

  <div class="kpis">
    <div class="card kpi"><label>Purchases This Month</label><strong>{ML(3352882)}</strong><div class="foot"><span class="delta up" title="Compared with September"><i data-icon="trend"></i>38.0%</span></div></div>
    <div class="card kpi"><label>Sales to Dealers This Month</label><strong>{ML(3120000)}</strong><div class="foot"><span class="delta up" title="Compared with September"><i data-icon="trend"></i>11.8%</span></div></div>
    <div class="card kpi"><label>Outstanding Balance</label><strong>{ML(1486320)}</strong><div class="foot"><span class="delta down">{ML(318400)} overdue</span></div></div>
    <div class="card kpi"><label>Stock on Hand</label><strong>7,415 <small>sheets</small></strong><div class="foot"><span class="delta down">3 Low Stock</span></div></div>
  </div>

  <div class="grid g-chart">
    <section class="card"><header><h2>Purchases and Sales to Dealers</h2></header>
      <div class="body">{chart('bars', months, [{'name':'Purchases from Crestline','values':purch,'color':'var(--accent)'},{'name':'Sales to Dealers','values':sales,'color':'var(--teal)'}], money=True, height=280)}</div></section>
    <section class="card"><header><h2>Stock by Finish</h2></header>
      <div class="body center">{chart('donut', series=[{'name':n,'value':v,'color':c} for n,v,c in finish], center='7,415', caption='sheets')}</div></section>
  </div>

  <div class="grid g-main-side">
    <section class="card flush"><header><h2>Recent Orders</h2><a class="more" data-link="PRI-ORD-01">View all orders</a></header>
      <div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Order Number</th><th>Date</th><th class="num">Sheets</th><th class="num">Value</th><th>Status</th></tr></thead><tbody>{order_rows}</tbody></table></div></div></section>
    <section class="card"><header><h2>Top Dealers This Month</h2><a class="more" data-link="PRI-DLR-01">All dealers</a></header>
      <div class="body"><ul class="list">{dealer_rows}</ul></div></section>
  </div>

  <div class="grid g-main-side" style="--side:22rem">
    <section class="card flush"><header><h2>Stock Alerts</h2><a class="more" data-link="PRI-INV-01">Inventory overview</a></header>
      <div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Product</th><th>SKU</th><th class="num">Available</th><th class="num">Reorder Level</th><th>Status</th></tr></thead><tbody>{alert_rows}</tbody></table></div></div></section>
    <section class="card"><header><h2>Active Schemes</h2><a class="more" data-link="PRI-SCH-01">All schemes</a></header>
      <div class="body"><ul class="list">
        {scheme('Festive Volume Rebate','30/11/2026',2750,3000,92,'ok')}
        {scheme('Marble Finish Launch Incentive','31/12/2026',180,300,60,'')}
      </ul></div></section>
  </div>
'''
page('primary','owner-dashboard','PRI-OWN-01','Primary Customer — Owner — Dashboard (PRI-OWN-01)', body)

# ---------- Company Profile ----------
def block(title, rows):
    kv = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in rows)
    return f'<section class="card"><header><h2>{title}</h2></header><div class="body"><dl class="kv">{kv}</dl></div></section>'
contacts = [('Rajesh Menon','Owner','rajesh.menon@distributoralpha.example','+91 90000 21001'),('Kavita Joshi','Sales and Operations Manager','kavita.joshi@distributoralpha.example','+91 90000 21002'),('Suresh Iyer','Accountant','suresh.iyer@distributoralpha.example','+91 90000 21003')]
contact_rows = ''.join(f'<tr><td class="nowrap"><b>{n}</b></td><td>{r}</td><td class="nowrap">{e}</td><td class="nowrap">{p}</td></tr>' for n,r,e,p in contacts)
nw = lambda t: f'<span style="white-space:nowrap">{t}</span>'
body = f'''  <div class="head">
    <h1>Company Profile</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Profile</button><button class="btn pri" type="button"><i data-icon="edit"></i>Edit Profile</button></div>
  </div>

  <section class="card pad" style="flex-direction:row;align-items:center;gap:1.25rem;flex-wrap:wrap">
    <div class="org" style="margin:0;padding:0;border:0;background:none"><i style="width:4rem;height:4rem;border-radius:1rem;font-size:1.25rem">DA</i></div>
    <div style="flex:1;min-width:16rem;display:grid;gap:.5rem"><h2 style="font-size:1.25rem">Distributor Alpha Private Limited</h2>
      <div style="display:flex;flex-wrap:wrap;gap:.5rem">{chip('Active','ok')}<span class="tag">Primary Distributor Tier A</span><span class="tag"><i data-icon="pin"></i>Maharashtra and Goa</span></div></div>
    <dl class="kv left" style="grid-template-columns:auto auto;gap:.5rem 1.25rem"><dt>Customer Code</dt><dd class="mono">CUS-0018</dd><dt>Customer Since</dt><dd>12 April 2018</dd></dl>
  </section>

  <div class="grid g-3" style="--cols:1.1fr 1.2fr 1.2fr">
    {block('Business Details', [('Legal Name','Distributor Alpha Private Limited'),('GST Number',nw('27AABCD4521F1Z7')),('Business Type','Distributor'),('Established','2011')])}
    {block('Addresses', [('Registered Office','Plot 14, Bhiwandi Logistics Park, Thane District, Maharashtra, Postal Code 421302'),('Pune Warehouse','Survey 88, Hadapsar Industrial Estate, Pune, Postal Code 411013')])}
    <section class="card"><header><h2>Commercial Terms</h2></header><div class="body"><dl class="kv"><dt>Price Tier</dt><dd>Primary Distributor Tier A</dd><dt>Credit Limit</dt><dd>{ML(4000000)}</dd><dt>Outstanding Balance</dt><dd>{ML(1486320)}</dd><dt>Credit Used</dt><dd><span class="inline-meter"><span class="meter warn"><i style="width:37%"></i></span><b>37%</b></span></dd><dt>Credit Period</dt><dd>45 days</dd></dl></div></section>
  </div>

  <section class="card flush"><header><h2>Contacts</h2><button class="btn sm" type="button" style="margin-left:auto"><i data-icon="plus"></i>Add Contact</button></header>
    <div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Name</th><th>Role</th><th>Email</th><th>Phone</th></tr></thead><tbody>{contact_rows}</tbody></table></div></div></section>

  <div class="grid g-2">
    <section class="card"><header><h2>Account Manager</h2></header><div class="body">
      <dl class="kv"><dt>Name</dt><dd><b>Vikram Chopra</b></dd><dt>Role</dt><dd>Sales Manager</dd><dt>Organisation</dt><dd>Crestline Laminates</dd><dt>Email</dt><dd>vikram.chopra@crestlinelaminates.example</dd><dt>Phone</dt><dd>+91 90000 11223</dd><dt>Territory</dt><dd>Maharashtra and Goa</dd></dl></div></section>
    <section class="card flush"><header><h2>Documents</h2></header><div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Document</th><th>Type</th><th>Date</th><th></th></tr></thead><tbody>
      <tr><td><b>GST Registration Certificate</b></td><td><span class="tag">PDF</span></td><td>18/04/2018</td><td><div class="row-actions"><button class="btn sm" type="button" aria-label="Download"><i data-icon="download"></i></button></div></td></tr>
      <tr><td><b>Trade Licence</b></td><td><span class="tag">PDF</span></td><td>02/04/2026</td><td><div class="row-actions"><button class="btn sm" type="button" aria-label="Download"><i data-icon="download"></i></button></div></td></tr>
      <tr><td><b>Distributor Agreement 2026\u201327</b></td><td><span class="tag">PDF</span></td><td>02/04/2026</td><td><div class="row-actions"><button class="btn sm" type="button" aria-label="Download"><i data-icon="download"></i></button></div></td></tr>
    </tbody></table></div></div></section>
  </div>
'''
page('primary','company-profile','PRI-PRO-01','Primary Customer — Owner — Company Profile (PRI-PRO-01)', body)

# ---------- Product Catalogue ----------
def slabs(sku):
    s = BY[sku][4]
    return f'<div class="slabs"><div><span>1–49</span><b>{M(s[0])}</b></div><div><span>50–199</span><b>{M(s[1])}</b></div><div class="best"><span>200+</span><b>{M(s[2])}</b></div></div>'
cards = ''
for p in P:
    sku = p[0]
    q = 200 if sku in ('LM-WNT-001','LM-ARC-002') else 50
    flag = chip('Low Stock','warn') if sku == 'LM-STN-009' else ''
    cards += f'''      <article class="card pcard"><a data-link="PRI-CAT-02" aria-label="{p[1]}">{sw(sku)}</a>
        <div class="in"><div><h3><a data-link="PRI-CAT-02" style="color:inherit">{p[1]}</a></h3></div>
          <div class="tags"><span class="tag mono">{sku}</span><span class="tag">{p[2]}</span><span class="tag">{p[3]}</span>{flag}</div>
          <div><span class="label-top" style="margin-bottom:.25rem">Price per Sheet</span>{slabs(sku)}</div>
          <div class="buy">{qty(q)}<button class="btn pri" type="button"><i data-icon="plus"></i>Add to Order</button></div></div></article>
'''
body = f'''  <div class="head">
    <h1>Product Catalogue</h1>
    <div class="acts"><a class="btn pri" data-link="PRI-ORD-03"><i data-icon="cart"></i>Order Draft<span class="chip" style="margin-left:.25rem;background:#fff;color:var(--accent-ink);border:0">5</span></a></div>
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
slab_rows = ''.join(f'<tr{" class=hl" if i==2 else ""}><td>{a}</td><td class="num"><b>{M(b)}</b></td><td class="num">{M(b*25)}</td></tr>' for i,(a,b) in enumerate([('1\u201349',p[4][0]),('50\u2013199',p[4][1]),('200+',p[4][2])]))
specs = [('SKU',sku),('Finish','Woodgrain'),('Thickness','1.0 mm'),('Sheet Size','8 ft × 4 ft (2,440 mm × 1,220 mm)'),('Weight per Sheet','6.1 kg'),('Grade','Decorative'),('Pack Size','25 sheets'),('Colour Family','Brown')]
spec_kv = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in specs)
related = ['LM-WNG-011','LM-TEK-006','LM-OAK-004','LM-SLT-005']
rel = ''.join(f'<a class="card" data-link="PRI-CAT-02" style="overflow:hidden;color:inherit">{sw(r,"","aspect-ratio:4/3;border-radius:0")}<div style="padding:.875rem 1rem"><b>{BY[r][1]}</b><div style="margin-top:.5rem;font-weight:620">{M(BY[r][4][0])} <span class="dim" style="font-weight:450">per sheet</span></div></div></a>' for r in related)
body = f'''  <div class="head">
    <div class="title-row"><h1>{p[1]}</h1>{chip('In Stock')}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Specification</button><a class="btn" data-link="PRI-INV-02"><i data-icon="stack"></i>View Inventory Item</a></div>
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      <section class="card pad">{sw(sku,'lg','aspect-ratio:16/9;width:100%')}</section>
      <div class="grid g-2">
        <section class="card"><header><h2>Specifications</h2></header><div class="body"><dl class="kv">{spec_kv}</dl></div></section>
        <section class="card flush"><header><h2>Price per Sheet</h2></header><div class="body"><div class="table-wrap"><table class="tbl"><thead><tr><th>Quantity</th><th class="num">Per Sheet</th><th class="num">Per Pack of 25</th></tr></thead><tbody>{slab_rows}</tbody></table></div></div></section>
      </div>
    </div>
    <div class="stack">
      <section class="card pad"><span class="label-top">Price per Sheet</span><div class="big-value">{M(p[4][2])}</div>
        <div class="field" style="margin-top:1.25rem"><label>Sheets to Order</label>{qty(200)}</div>
        <dl class="kv total" style="margin-top:1.25rem"><dt>Amount</dt><dd>{M(200*p[4][2])}</dd></dl>
        <button class="btn pri block" type="button" style="margin-top:1rem"><i data-icon="plus"></i>Add to Order</button></section>
      <section class="card"><header><h2>Your Stock</h2></header><div class="body"><dl class="kv"><dt>On Hand</dt><dd>1,240 sheets</dd><dt>Reserved for Dealers</dt><dd>310 sheets</dd><dt>Available</dt><dd><b>930 sheets</b></dd><dt>On Order</dt><dd>600 sheets</dd><dt>Arriving</dt><dd>30/10/2026</dd><dt>Reorder Level</dt><dd>400 sheets</dd></dl></div></section>
      <section class="card"><header><h2>Crestline Availability</h2></header><div class="body"><dl class="kv"><dt>Plant Warehouse, Vapi</dt><dd>12,400 sheets</dd><dt>Dispatch Time</dt><dd>2 to 3 days</dd></dl></div></section>
    </div>
  </div>
  <section><h2 style="margin-bottom:1rem">Related Products</h2><div class="products four">{rel}</div></section>
'''
page('primary','product-details','PRI-CAT-02','Primary Customer — Owner — Product Details (PRI-CAT-02)', body)
