"""Phase 11, part B: Company Administration, Super Admin: User Directory, User Details, Product Management, Product Details, Create Product, Edit Product.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md "Phase 11 data"."""
from data import *

def prod_cell(s, sid=None):
    name = f'<a data-link="{sid}"><b>{BY[s][1]}</b></a>' if sid else f'<b>{BY[s][1]}</b>'
    return f'<div class="prod">{sw(s)}<div>{name}</div></div>'
tick = lambda v: '<i data-icon="check"></i>' if v else '<span class="no">—</span>'

# ---------- User Directory ----------
ORG_ROWS = [(org, dom, u) for org, dom, users in USER_ORGS for u in users]
urows = ''.join(f'<tr><td>{link("CMP-USR-02", u[0])}</td><td>{org}</td><td>{u[1]}</td><td class="nowrap">{user_email(u[0], dom)}</td><td class="nowrap">{u[3]}</td><td>{chip(u[4])}</td></tr>' for org, dom, u in ORG_ROWS[:12])
body = f'''  <div class="head">
    <h1>User Directory</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Users</button></div>
  </div>
  <div class="kpis">
    {kpi('Users', str(USERS_ALL))}
    {kpi('Crestline Staff', str(len(CRL_USERS)))}
    {kpi('Customer Users', str(USERS_ALL - len(CRL_USERS)))}
    {kpi('Invited', str(USER_STATUS['Invited']), chip('Not Yet Signed In', 'plain'))}
  </div>
  <section class="card flush">
    {tabs([('All Users', USERS_ALL, True), ('Active', USER_STATUS['Active'], False), ('Invited', USER_STATUS['Invited'], False), ('Inactive', USER_STATUS['Inactive'], False)])}
    {filters('Search by name, email address or organisation', 'Search users', ('Organisation', 'All'), ('Role', 'All'), ('Sort by', 'Organisation'))}
    <div class="body">{table([('Name', ''), ('Organisation', ''), ('Role', ''), ('Email Address', ''), ('Last Sign-In', ''), ('Status', '')], [urows], 'wrap')}
      <div class="pg"><span>Showing 1 to 12 of {USERS_ALL} users</span><div class="pages"><span class="on">1</span><span>2</span><span>3</span><span>…</span><span>{-(-USERS_ALL // 12)}</span></div></div></div>
  </section>
'''
page('company', 'user-directory', 'CMP-USR-01', 'Company Administration — Super Admin — User Directory (CMP-USR-01)', body)

# ---------- User Details (Vikram Chopra, Sales Manager) ----------
vc = next(u for u in CRL_USERS if u[0] == 'Vikram Chopra')
act = [('26/10/2026 09:10', 'Signed in'), ('24/10/2026 10:05', 'Confirmed order ORD-2026-10459'), ('22/10/2026 11:30', 'Opened dealer request DRQ-2026-0017'),
       ('20/10/2026 09:40', 'Confirmed order ORD-2026-10447'), ('19/10/2026 09:05', 'Signed in'), ('30/09/2026 15:10', 'Approved dealer request DRQ-2026-0014')]
ACCESS = [('Dashboard', 1), ('Customers', 0), ('Users', 0), ('Products', 0), ('Orders and Dispatch', 0), ('Inventory and Returns', 0), ('Sales Analytics', 0), ('Performance', 1), ('Analysis', 1),
          ('Orders and Campaigns', 1), ('Finance and Schemes', 0), ('Support', 0), ('Administration', 0), ('My Profile and Notifications', 1)]
body = f'''  <div class="head">
    <div class="title-row"><h1>{vc[0]}</h1>{chip(vc[4])}<span class="tag">{vc[1]}</span></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="lock"></i>Reset Password</button><button class="btn" type="button"><i data-icon="edit"></i>Edit User</button><button class="btn danger" type="button">Deactivate User</button></div>
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      {card('Profile', kv([('Full Name', vc[0]), ('Email Address', user_email(vc[0], 'crestlinelaminates.example')), ('Mobile Number', f'+91 90000 {vc[2]}'), ('Role', vc[1]), ('Organisation', 'Crestline Laminates'),
                           ('Territory', 'Maharashtra and Goa'), ('Added On', '15/05/2017'), ('Added By', 'Anita Deshmukh'), ('Last Sign-In', vc[3])]))}
      <section class="card flush"><header><h2>Recent Activity</h2></header><div class="body">{table([('Date', ''), ('Activity', '')], [f'<tr><td class="nowrap">{d}</td><td><b>{t}</b></td></tr>' for d, t in act])}</div></section>
    </div>
    <section class="card flush"><header><h2>Access</h2></header><div class="body">{table([('Area', ''), ('Access', 'c')], [f'<tr><td><b>{n}</b></td><td class="c">{tick(v)}</td></tr>' for n, v in ACCESS])}</div></section>
  </div>
'''
page('company', 'user-details', 'CMP-USR-02', 'Company Administration — Super Admin — User Details (CMP-USR-02)', body)

# ---------- Product Management ----------
prows = ''.join(f'<tr><td>{prod_cell(p[0], "CMP-PRD-02")}</td><td class="mono nowrap">{p[0]}</td><td>{p[2]}</td><td>{p[3]}</td><td class="num"><b>{M(p[4][0])}</b></td>'
                f'<td class="num">{N(CSTK[p[0]]["available"])}</td><td class="num">{N(CSTK[p[0]]["level"])}</td><td>{chip(CSTK[p[0]]["status"])}</td>'
                f'<td><div class="row-actions"><a class="btn sm" data-link="CMP-PRD-02">View</a><a class="btn sm" data-link="CMP-PRD-04">Edit</a></div></td></tr>\n' for p in P)
finishes = len({p[2] for p in P}); assert finishes == 7
body = f'''  <div class="head">
    <h1>Product Management</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Products</button><a class="btn pri" data-link="CMP-PRD-03"><i data-icon="plus"></i>Create Product</a></div>
  </div>
  <div class="kpis">
    {kpi('Products', str(len(P)))}
    {kpi('In Stock', str(CSTK_COUNT['In Stock']))}
    {kpi('Low Stock', str(CSTK_COUNT['Low Stock']), '<span class="delta down">Carrara Stone Finish</span>')}
    {kpi('Finishes', str(finishes))}
  </div>
  <section class="card flush">
    {tabs([('All Products', len(P), True), ('In Stock', CSTK_COUNT['In Stock'], False), ('Low Stock', CSTK_COUNT['Low Stock'], False), ('Out of Stock', 0, False)])}
    {filters('Search by product name or SKU', 'Search products', ('Finish', 'All'), ('Thickness', 'All'), ('Sort by', 'SKU'))}
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Finish', ''), ('Thickness', ''), ('Price per Sheet', 'num'), ('Available Sheets', 'num'), ('Reorder Level', 'num'), ('Status', ''), ('', '')], [prows], 'wrap')}
      {pager(f'Showing 1 to 12 of {len(P)} products', 1)}</div>
  </section>
'''
page('company', 'product-management', 'CMP-PRD-01', 'Company Administration — Super Admin — Product Management (CMP-PRD-01)', body)

# ---------- Product Details (LM-WNT-001) ----------
sku = 'LM-WNT-001'; p = BY[sku]; st = CSTK[sku]
slab_rows = ''.join(f'<tr{" class=hl" if i == 2 else ""}><td>{a}</td><td class="num"><b>{M(b)}</b></td><td class="num">{M(b * 25)}</td></tr>' for i, (a, b) in enumerate([('1–49', p[4][0]), ('50–199', p[4][1]), ('200+', p[4][2])]))
specs = [('SKU', sku), ('Finish', p[2]), ('Thickness', p[3]), ('Sheet Size', '8 ft × 4 ft (2,440 mm × 1,220 mm)'), ('Weight per Sheet', '6.1 kg'), ('Grade', 'Decorative'), ('Pack Size', '25 sheets'), ('Colour Family', 'Brown')]
wh_rows = (f'<tr><td><b>{WAREHOUSES[0][0]}, {WAREHOUSES[0][1].split(",")[0]}</b></td><td class="num">{N(st["vapi"])}</td><td class="num">{N(st["reserved"])}</td><td class="num"><b>{N(st["vapi_avail"])}</b></td></tr>'
           f'<tr><td><b>{WAREHOUSES[1][0]}, {WAREHOUSES[1][1].split(",")[0]}</b></td><td class="num">{N(st["taloja"])}</td><td class="num">0</td><td class="num"><b>{N(st["taloja"])}</b></td></tr>')
wh_foot = f'<tfoot><tr><td>Total</td><td class="num">{N(st["on_hand"])}</td><td class="num">{N(st["reserved"])}</td><td class="num">{N(st["available"])}</td></tr></tfoot>'
tier_rows = (f'<tr><td><b>Primary Distributor Tier A</b></td><td>Crestline Laminates</td><td class="num"><b>{M(p[4][0])}</b></td></tr>'
             f'<tr><td><b>Dealer Tier B</b></td><td>Distributor Alpha</td><td class="num"><b>{M(dp(sku))}</b></td></tr>'
             f'<tr><td><b>Retailer Tier C</b></td><td>Dealer Bravo</td><td class="num"><b>{M(rp(sku))}</b></td></tr>')
ordered = [(o, q) for o, ls in ORDER_LINES.items() for s, q in ls if s == sku]
assert sum(q for _, q in ordered) == BOUGHT[sku] == 600 and len(ordered) == 5
res_orders = [o for o in ('ORD-2026-10482', 'ORD-2026-10459') if any(s == sku for s, _ in ORDER_LINES[o])]
assert len(res_orders) == 1 and sum(q for s, q in ORDER_LINES[res_orders[0]] if s == sku) == st['reserved']
body = f'''  <div class="head">
    <div class="title-row"><h1>{p[1]}</h1>{chip(st["status"])}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Specification</button><a class="btn pri" data-link="CMP-PRD-04"><i data-icon="edit"></i>Edit Product</a></div>
  </div>
  <div class="kpis">
    {kpi('Available Sheets', N(st['available']))}
    {kpi('Reserved for Orders', N(st['reserved']), chip(f'{len(res_orders)} order' + ('s' if len(res_orders) != 1 else ''), 'plain'))}
    {kpi('Sheets Ordered This Month', N(BOUGHT[sku]), chip(f'{len(ordered)} orders', 'plain'))}
    {kpi('Reorder Level', N(st['level']))}
  </div>
  <div class="grid g-main-side" style="--side:28rem">
    <div class="stack">
      <section class="card pad">{sw(sku, 'lg', 'aspect-ratio:3/2;width:100%')}</section>
      {card('Specifications', kv(specs))}
    </div>
    <div class="stack">
      <section class="card flush"><header><h2>Stock by Warehouse</h2></header><div class="body">{table([('Warehouse', ''), ('On Hand', 'num'), ('Reserved', 'num'), ('Available', 'num')], [wh_rows], 'wrap', foot=wh_foot)}</div></section>
      <section class="card flush"><header><h2>Price per Sheet</h2></header><div class="body">{table([('Quantity', ''), ('Per Sheet', 'num'), ('Per Pack of 25', 'num')], [slab_rows])}</div></section>
      <section class="card flush"><header><h2>Price by Tier</h2></header><div class="body">{table([('Price Tier', ''), ('Set By', ''), ('Price per Sheet', 'num')], [tier_rows], 'wrap')}</div></section>
    </div>
  </div>
'''
page('company', 'product-details', 'CMP-PRD-02', 'Company Administration — Super Admin — Product Details (CMP-PRD-02)', body)

# ---------- Create Product and Edit Product ----------
FINISHES = ['Matte', 'Woodgrain', 'Texture', 'Gloss', 'Suede', 'High Gloss', 'Metallic']
def upload(name, fname=None):
    inner = f'<span class="file"><i data-icon="doc"></i>{fname}</span>' if fname else ''
    return f'<div class="drop"><b>{name}</b>{inner}<button class="btn sm" type="button"><i data-icon="upload"></i>{"Replace" if fname else "Upload"}</button></div>'
def form3(title, *fields):
    return f'<section class="card"><header><h2>{title}</h2></header><div class="body"><div class="form-grid three">{"".join(fields)}</div></div></section>'
def product_form(v, summary_title):
    return f'''  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      {form('Product Details', fld('Product Name', 'pn', v['name'], full=True), fld('SKU', 'sk', v['sku']), fld('Finish', 'fi', v['finish'], 'select', FINISHES), fld('Thickness', 'th', v['thick'], 'select', ['1.0 mm', '0.8 mm']),
            fld('Sheet Size', 'ss', '8 ft × 4 ft (2,440 mm × 1,220 mm)', 'select', ['8 ft × 4 ft (2,440 mm × 1,220 mm)']), fld('Weight per Sheet', 'wt', v['weight']), fld('Grade', 'gr', 'Decorative', 'select', ['Decorative']),
            fld('Pack Size', 'pk', '25 sheets'), fld('Colour Family', 'cf', v['colour'], 'select', ['Brown', 'Grey', 'White', 'Black', 'Blue', 'Cream', 'Copper']))}
      {form3('Price per Sheet', fld('1 to 49 Sheets', 'p1', v['p'][0]), fld('50 to 199 Sheets', 'p2', v['p'][1]), fld('200 Sheets and Above', 'p3', v['p'][2]))}
      {form3('Availability', fld('Product Status', 'ps', v['status'], 'select', ['Active', 'Draft', 'Discontinued']), fld('Reorder Level in Sheets', 'rl', v['level']), fld('Show in Distributor Catalogue', 'sc', 'Yes', 'select', ['Yes', 'No']))}
      <section class="card"><header><h2>Product Image</h2></header><div class="body">{upload('Image File', v['image'])}</div></section>
    </div>
    <div class="stack">{card(summary_title, kv(v['summary']))}</div>
  </div>
'''
nv = dict(name='Nordic Ash Woodgrain Laminate', sku='LM-ASH-013', finish='Woodgrain', thick='1.0 mm', weight='6.1 kg', colour='Grey', p=['₹1,150', '₹1,110', '₹1,065'], status='Draft', level='2,000', image=None,
          summary=[('Product', 'Nordic Ash Woodgrain Laminate'), ('SKU', '<span class="mono">LM-ASH-013</span>'), ('Finish', 'Woodgrain'), ('Price from', M(1150)), ('Status', chip('Draft', 'plain'))])
body = f'''  <div class="head">
    <h1>Create Product</h1>
    <div class="acts"><a class="btn" data-link="CMP-PRD-01">Cancel</a><button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Create Product</button></div>
  </div>
{product_form(nv, 'Product Summary')}'''
page('company', 'create-product', 'CMP-PRD-03', 'Company Administration — Super Admin — Create Product (CMP-PRD-03)', body)

ev = dict(name=p[1], sku=sku, finish=p[2], thick=p[3], weight='6.1 kg', colour='Brown', p=[M(x) for x in p[4]], status='Active', level=N(st['level']), image='walnut-woodgrain.jpg',
          summary=[('Product', p[1]), ('SKU', f'<span class="mono">{sku}</span>'), ('Finish', p[2]), ('Price from', M(p[4][0])), ('Available Sheets', N(st['available'])), ('Status', chip('In Stock'))])
body = f'''  <div class="head">
    <h1>Edit Product</h1>
    <div class="acts"><a class="btn" data-link="CMP-PRD-02">Cancel</a><button class="btn pri" type="button">Save Changes</button></div>
  </div>
{product_form(ev, 'Product Summary')}'''
page('company', 'edit-product', 'CMP-PRD-04', 'Company Administration — Super Admin — Edit Product (CMP-PRD-04)', body)
