"""Phase 11, part A: Company Administration, Super Admin: Dashboard, Customer Directory, Customer Details, Customer Approval Queue,
Customer Hierarchy Explorer. Crestline Laminates sees the chain Distributor Alpha, its eight dealers and their 20 retailers.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md "Phase 11 data"."""
from data import *

def person_cell(name): return f'<td class="nowrap">{name}</td>'
PARENT_NAME = {c['key']: ('Crestline Laminates' if c['parent'] is None else CUS[c['parent']]['name']) for c in CUSTOMERS}

# ---------- Dashboard ----------
region_colors = {'West Maharashtra': '#0a48fd', 'North Maharashtra': '#0b8fa8', 'Konkan': '#7a36fb', 'Vidarbha': '#e0a030', 'Goa': '#0c9b6a'}
open_rows = ''
for o in ALPHA_ORDERS[:3]:
    dsp = '<span class="mono">DSP-2026-5521</span>' if o[0] == 'ORD-2026-10447' else '—'
    open_rows += (f'<tr><td class="nowrap">{link("CMP-ORD-02", o[0])}</td><td>Distributor Alpha</td><td>{o[1]}</td><td class="num">{N(o[2])}</td><td class="num"><b>{M(o[3])}</b></td>'
                  f'<td>{o[4]}</td><td>{dsp}</td><td>{chip(o[5])}</td></tr>')
tk_rows = ''.join(f'<tr><td class="mono nowrap">{link("CMP-SUP-02", t[0])}</td><td>Distributor Alpha</td><td>{t[2]}</td><td>{chip(t[4])}</td><td>{chip(t[6])}</td><td>{t[5]}</td></tr>' for t in CRL_TICKETS_OPEN)
od_rows = ''.join(f'<tr><td class="mono nowrap">{link("CMP-BIL-02", i[0])}</td><td>{i[3]}</td><td class="num">{days_over(i)}</td><td class="num"><b>{M(i[4] - i[5])}</b></td></tr>' for i in sorted(OVERDUE, key=lambda i: -days_over(i)))
od_foot = f'<tfoot><tr><td colspan="3">Total</td><td class="num">{M(sum(i[4] - i[5] for i in OVERDUE))}</td></tr></tfoot>'
body = f'''  <div class="head">
    <h1>Dashboard</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><a class="btn" data-link="CMP-CUS-03">Customer Approval Queue</a><a class="btn pri" data-link="CMP-ORD-01">Order Management</a></div>
  </div>
  <div class="kpis">
    {kpi('Orders This Month', '6', chip('1 Awaiting Confirmation', 'warn'))}
    {kpi('Order Value This Month', ML(PURCH_MONTH[-1]), up(pct(PURCH_MONTH[-1], PURCH_MONTH[-2])))}
    {kpi('Customers', str(len(CUSTOMERS)), chip('2 New', 'blue'))}
    {kpi('Shipments in Transit', '1', chip('Arriving 27/10/2026', 'blue'))}
    {kpi('Open Support Tickets', str(len(CRL_TICKETS_OPEN)), '<span class="delta down">1 High Priority</span>')}
  </div>
  <div class="grid g-chart">
    {card('Order Value by Month', chart('bars', MONTHS, [{'name': 'Orders from Distributors', 'values': PURCH_MONTH, 'color': 'var(--accent)'}], money=True, height=290))}
    <section class="card"><header><h2>Sales to Dealers by Region</h2></header><div class="body center">{chart('donut', series=[{'name': r, 'value': v, 'color': region_colors[r]} for r, v in sorted(REGION_SALES.items(), key=lambda x: -x[1])], center='5', caption='regions')}</div></section>
  </div>
  <section class="card flush"><header><h2>Open Orders</h2><a class="more" data-link="CMP-ORD-01">All orders</a></header>
    <div class="body">{table([('Order Number', ''), ('Customer', ''), ('Order Date', ''), ('Sheets', 'num'), ('Value', 'num'), ('Delivery Date', ''), ('Dispatch Number', ''), ('Status', '')], [open_rows], 'wrap')}</div></section>
  <section class="card flush"><header><h2>Open Support Tickets</h2><a class="more" data-link="CMP-SUP-01">All tickets</a></header>
    <div class="body">{table([('Ticket Number', ''), ('Customer', ''), ('Subject', ''), ('Priority', ''), ('Status', ''), ('Last Updated', '')], [tk_rows], 'wrap')}</div></section>
  <div class="grid g-2">
    <section class="card"><header><h2>Customer Approval Queue</h2><a class="more" data-link="CMP-CUS-03">Open queue</a></header><div class="body">{kv([('Request Number', f'<span class="mono">{PENDING_DRQ["number"]}</span>'), ('Dealer', PENDING_DRQ['name']), ('City', PENDING_DRQ['city']),
        ('Requested Credit', ML(PENDING_DRQ['credit'])), ('Days Waiting', str(DAYS_WAITING)), ('Assigned To', PENDING_DRQ['assigned']), ('Status', chip('Waiting for Decision'))])}</div></section>
    <section class="card flush"><header><h2>Overdue Invoices</h2><a class="more" data-link="CMP-BIL-01">All invoices</a></header>
      <div class="body">{table([('Invoice Number', ''), ('Due Date', ''), ('Days Overdue', 'num'), ('Balance', 'num')], [od_rows], 'wrap', foot=od_foot)}</div></section>
  </div>
'''
page('company', 'super-admin-dashboard', 'CMP-ADM-01', 'Company Administration — Super Admin — Dashboard (CMP-ADM-01)', body)

# ---------- Customer Directory ----------
rows = []
for c in TREE[:12]:
    rows.append(f'<tr><td>{link("CMP-CUS-02", c["name"])}</td><td class="mono nowrap">{c["code"]}</td><td>{PARENT_NAME[c["key"]]}</td><td>{c["city"]}</td><td>{c["region"]}</td>'
                f'<td>{chip(c["status"])}</td><td class="nowrap">{c["since"]}</td><td><div class="row-actions"><a class="btn sm" data-link="CMP-CUS-02">View</a></div></td></tr>')
body = f'''  <div class="head">
    <h1>Customer Directory</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Customers</button><a class="btn pri" data-link="CMP-CUS-03">Customer Approval Queue</a></div>
  </div>
  <div class="kpis">
    {kpi('Customers', str(len(CUSTOMERS)), chip('2 New', 'blue'))}
    {kpi('Distributors', str(CUS_TYPE['Distributor']))}
    {kpi('Dealers', str(CUS_TYPE['Dealer']), chip('1 New', 'blue'))}
    {kpi('Retailers', str(CUS_TYPE['Retailer']), chip('1 New', 'blue'))}
  </div>
  <section class="card flush">
    {tabs([('All Customers', len(CUSTOMERS), True), ('Distributors', CUS_TYPE['Distributor'], False), ('Dealers', CUS_TYPE['Dealer'], False), ('Retailers', CUS_TYPE['Retailer'], False)])}
    {filters('Search by customer name, code or city', 'Search customers', ('Region', 'All'), ('Status', 'All'), ('Sort by', 'Hierarchy'))}
    <div class="body">{table([('Customer', ''), ('Customer Code', ''), ('Parent Customer', ''), ('City', ''), ('Region', ''), ('Status', ''), ('Customer Since', ''), ('', '')], rows, 'wrap')}
      {pager(f'Showing 1 to 12 of {len(CUSTOMERS)} customers')}</div>
  </section>
'''
page('company', 'customer-directory', 'CMP-CUS-01', 'Company Administration — Super Admin — Customer Directory (CMP-CUS-01)', body)

# ---------- Customer Details (Distributor Alpha) ----------
a = CUS['ALP']; used = credit_pct(OUTSTANDING, CREDIT_LIMIT); assert used == 37
order_rows = ''.join(f'<tr><td class="nowrap">{link("CMP-ORD-02", o[0])}</td><td>{o[1]}</td><td class="num">{N(o[2])}</td><td class="num"><b>{M(o[3])}</b></td><td>{o[4]}</td><td>{chip(o[5])}</td><td>{chip(o[6])}</td></tr>' for o in ALPHA_ORDERS[:6])
dealer_rows = ''.join(f'<tr><td><b>{d[1]}</b></td><td>{d[2]}</td><td>{chip(d[4])}</td><td class="num">{d[6]}</td><td class="num"><b>{M(d[7])}</b></td></tr>' for d in DEALERS)
dealer_foot = f'<tfoot><tr><td colspan="3">Total</td><td class="num">{sum(d[6] for d in DEALERS)}</td><td class="num">{M(sum(d[7] for d in DEALERS))}</td></tr></tfoot>'
contacts = [('Rajesh Menon', 'Owner', '+91 90000 21001'), ('Kavita Joshi', 'Sales and Operations Manager', '+91 90000 21002'), ('Suresh Iyer', 'Accountant', '+91 90000 21003')]
docs = [('GST Registration Certificate', 'PDF', '18/04/2018'), ('Trade Licence', 'PDF', '02/04/2026'), ('Distributor Agreement 2026–27', 'PDF', '02/04/2026')]
body = f'''  <div class="head">
    <div class="title-row"><h1>{a["name"]}</h1>{chip("Active")}<span class="tag">Primary Distributor Tier A</span><span class="tag"><i data-icon="pin"></i>{a["city"]}</span></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Customer Profile</button><button class="btn" type="button"><i data-icon="edit"></i>Edit Customer</button><button class="btn danger" type="button">Place on Hold</button></div>
  </div>
  <div class="kpis">
    {kpi('Order Value This Month', ML(PURCH_MONTH[-1]), up(pct(PURCH_MONTH[-1], PURCH_MONTH[-2])))}
    {kpi('Outstanding Balance', ML(OUTSTANDING), '<span class="delta down">2 Overdue</span>')}
    {kpi('Credit Limit', ML(CREDIT_LIMIT), chip(f'{used}% Used', 'plain'))}
    {kpi('Dealers', str(CUS_TYPE['Dealer']), chip(f'{CUS_TYPE["Retailer"]} Retailers', 'plain'))}
  </div>
  <div class="grid g-main-side" style="--side:28rem">
    {card('Orders by Month', chart('bars', MONTHS, [{'name': 'Orders from Distributor Alpha', 'values': PURCH_MONTH, 'color': 'var(--accent)'}], money=True, height=380))}
    {card('Account', kv([('Customer Code', f'<span class="mono">{a["code"]}</span>'), ('Customer Type', 'Distributor'), ('Price Tier', 'Primary Distributor Tier A'), ('Credit Limit', ML(CREDIT_LIMIT)),
                         ('Credit Used', f'<span class="inline-meter"><span class="meter {meter_cls(used)}"><i style="width:{used}%"></i></span><b>{used}%</b></span>'), ('Credit Period', '45 days'),
                         ('Customer Since', a['since']), ('Territory', 'Maharashtra and Goa'), ('Account Manager', 'Vikram Chopra'), ('GST Number', '<span style="white-space:nowrap">27AABCD4521F1Z7</span>'),
                         ('Permanent Account Number', '<span style="white-space:nowrap">AABCD4521F</span>'), ('Registered Office', 'Plot 14, Bhiwandi Logistics Park, Thane District, Maharashtra, Postal Code 421302')]))}
  </div>
  <section class="card flush"><header><h2>Recent Orders</h2><a class="more" data-link="CMP-ORD-01">All orders</a></header>
    <div class="body">{table([('Order Number', ''), ('Order Date', ''), ('Sheets', 'num'), ('Value', 'num'), ('Delivery Date', ''), ('Order Status', ''), ('Payment', '')], [order_rows], 'wrap')}</div></section>
  <div class="grid g-main-side" style="--side:26rem">
    <section class="card flush"><header><h2>Dealers</h2><a class="more" data-link="CMP-CUS-04">Customer hierarchy</a></header>
      <div class="body">{table([('Dealer', ''), ('City', ''), ('Status', ''), ('Retailers', 'num'), ('Purchases This Month', 'num')], [dealer_rows], 'wrap', foot=dealer_foot)}</div></section>
    <div class="stack">
      <section class="card flush"><header><h2>Contacts</h2></header><div class="body">{table([('Name', ''), ('Role', ''), ('Phone', '')], [f'<tr><td class="nowrap"><b>{n}</b></td><td>{r}</td><td class="nowrap">{p}</td></tr>' for n, r, p in contacts], 'wrap')}</div></section>
      <section class="card flush"><header><h2>Documents</h2></header><div class="body">{table([('Document', ''), ('Type', ''), ('Date', '')], [f'<tr><td><b>{n}</b></td><td>{t}</td><td class="nowrap">{d}</td></tr>' for n, t, d in docs], 'wrap')}</div></section>
    </div>
  </div>
'''
page('company', 'customer-details', 'CMP-CUS-02', 'Company Administration — Super Admin — Customer Details (CMP-CUS-02)', body)

# ---------- Customer Approval Queue ----------
q = PENDING_DRQ
q_rows = (f'<tr><td class="mono nowrap"><b>{q["number"]}</b></td><td><b>{q["name"]}</b></td><td>{q["city"]}</td><td>{q["submitted"]}</td><td class="num">{M(q["credit"])}</td><td class="num">{q["docs"]} of 3</td>'
          f'<td>{chip("Waiting for Decision")}</td><td>—</td><td>{q["assigned"]}</td></tr>')
for r in DECIDED_DRQ:
    q_rows += (f'<tr><td class="mono nowrap"><b>{r[0]}</b></td><td><b>{r[1]}</b></td><td>{r[2]}</td><td>{r[5]}</td><td class="num">{M(r[6])}</td><td class="num">{r[8]} of 3</td>'
               f'<td>{chip(r[11])}</td><td>{r[10]}</td><td>{r[12]}</td></tr>')
def doc_row(name, fname): return f'<div class="drop"><b>{name}</b><span class="file"><i data-icon="doc"></i>{fname}</span><button class="btn sm" type="button">View</button></div>'
steps = [('Request Submitted: Rajesh Menon', 'Completed 19/10/2026', 'ok'), ('Distributor Review: Kavita Joshi', 'Approved 21/10/2026', 'ok'),
         ('Crestline Approval: Vikram Chopra', 'Waiting for Decision', 'warn'), ('Dealer Activated', 'Pending', 'plain')]
path = '<ul class="list">' + ''.join(f'<li><div class="grow"><b>{n}</b></div>{chip(c, k)}</li>' for n, c, k in steps) + '</ul>'
body = f'''  <div class="head">
    <h1>Customer Approval Queue</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Requests</button></div>
  </div>
  <div class="kpis">
    {kpi('Waiting for Decision', '1', chip(q['assigned'], 'blue'))}
    {kpi('Requested Credit', ML(q['credit']))}
    {kpi('Days Waiting', str(DAYS_WAITING))}
    {kpi('Average Days to Decision', f'{sum(DECISION_DAYS) / len(DECISION_DAYS):.0f}', chip('2 decided requests', 'plain'))}
  </div>
  <section class="card flush">
    {tabs([('All Requests', 3, True), ('Waiting for Decision', 1, False), ('Approved', 1, False), ('Rejected', 1, False)])}
    <div class="body" style="margin-top:1rem">{table([('Request Number', ''), ('Dealer', ''), ('City', ''), ('Submitted', ''), ('Requested Credit', 'num'), ('Documents', 'num'), ('Status', ''), ('Decided On', ''), ('Assigned To or Decided By', '')], [q_rows], 'wrap')}</div>
  </section>
  <div class="head"><div class="title-row"><h2>{q["name"]}</h2>{chip("Waiting for Decision")}<span class="mono">{q["number"]}</span></div></div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      {card('Business Details', kv([('Dealer Business Name', q['name']), ('Legal Name', q['legal']), ('Business Type', 'Dealer'), ('GST Number', f'<span style="white-space:nowrap">{q["gst"]}</span>'),
                                    ('Permanent Account Number', f'<span style="white-space:nowrap">{q["pan"]}</span>'), ('Expected Monthly Volume', f'{q["sheets"]} sheets')]))}
      <div class="grid g-2">
        {card('Owner Contact', kv([('Owner Name', q['owner']), ('Mobile Number', q['phone']), ('Email Address', q['email']), ('Address', q['address'])]))}
        {card('Proposed Terms', kv([('Region', q['region']), ('Territory', q['territory']), ('Price Tier', q['tier']), ('Requested Credit', ML(q['credit'])), ('Credit Period', q['period'])]))}
      </div>
      <section class="card"><header><h2>Documents</h2></header><div class="body"><div class="stack">{doc_row('GST Registration Certificate', 'gst-certificate.pdf')}{doc_row('Trade Licence', 'trade-licence.pdf')}{doc_row('Address Proof', 'address-proof.pdf')}</div></div></section>
    </div>
    <div class="stack">
      {card('Approval Path', path)}
      <section class="card"><header><h2>Decision</h2></header><div class="body"><div class="stack">{fld('Decision Note', 'dn', '', 'textarea', full=True)}
        <button class="btn pri block" type="button">Approve Customer</button><button class="btn block" type="button">Request More Information</button><button class="btn danger block" type="button">Reject Request</button></div></div></section>
    </div>
  </div>
'''
page('company', 'customer-approval-queue', 'CMP-CUS-03', 'Company Administration — Super Admin — Customer Approval Queue (CMP-CUS-03)', body)

# ---------- Customer Hierarchy Explorer ----------
def row_cells(c, lvl, caret, extra_tags=''):
    return (f'<span class="name" style="--lvl:{lvl}">{caret}<a data-link="CMP-CUS-02"><b>{c["name"]}</b></a><span class="tag">{c["type"]}</span>{extra_tags}</span>'
            f'<span class="c-code mono">{c["code"]}</span><span class="c-city">{c["city"]}</span><span class="c-status">{chip(c["status"])}</span><span class="num"><b>{M(c["purchases"])}</b></span>')
CARET = '<span class="caret"><i data-icon="down"></i></span>'
def node(c, lvl, open_=False):
    kids = [k for k in CUSTOMERS if k['parent'] == c['key']]
    if not kids: return f'<div class="row leaf">{row_cells(c, lvl, "")}</div>'
    noun = 'Dealer' if c['type'] == 'Distributor' else 'Retailer'
    tag = f'<span class="tag">{len(kids)} {noun}{"s" if len(kids) != 1 else ""}</span>'
    return (f'<details class="node"{" open" if open_ else ""}><summary class="row">{row_cells(c, lvl, CARET, tag)}</summary>'
            + ''.join(node(k, lvl + 1) for k in kids) + '</details>')
tree = (f'<div class="tree"><div class="row head-row"><span>Customer</span><span class="c-code">Customer Code</span><span class="c-city">City</span><span class="c-status">Status</span><span class="num">Purchases This Month</span></div>'
        f'<details class="node" open><summary class="row root"><span class="name" style="--lvl:0">{CARET}<b>Crestline Laminates</b><span class="tag">Company</span><span class="tag">1 Distributor</span></span><span class="c-code"></span><span class="c-city">Vapi</span><span class="c-status"></span><span class="num"></span></summary>'
        f'<details class="node" open><summary class="row">{row_cells(CUS["ALP"], 1, CARET, f"""<span class="tag">{CUS_TYPE["Dealer"]} Dealers</span>""")}</summary>'
        + ''.join(node(CUS[d[0]], 2, d[0] == 'BRV') for d in DEALERS) + '</details></details></div>')
reg_rows = ''
for reg in REGION_SALES:
    nd = sum(1 for c in CUSTOMERS if c['type'] == 'Dealer' and c['region'] == reg); nr = sum(1 for c in CUSTOMERS if c['type'] == 'Retailer' and c['region'] == reg)
    reg_rows += f'<tr><td><b>{reg}</b></td><td class="num">{nd}</td><td class="num">{nr}</td></tr>'
assert sum(sum(1 for c in CUSTOMERS if c['type'] == 'Dealer' and c['region'] == reg) for reg in REGION_SALES) == 8
reg_foot = f'<tfoot><tr><td>Total</td><td class="num">{CUS_TYPE["Dealer"]}</td><td class="num">{CUS_TYPE["Retailer"]}</td></tr></tfoot>'
body = f'''  <div class="head">
    <h1>Customer Hierarchy Explorer</h1>
    <div class="acts"><button class="btn" type="button" data-expand="none">Collapse All</button><button class="btn" type="button" data-expand="all">Expand All</button><a class="btn pri" data-link="CMP-CUS-01">Customer Directory</a></div>
  </div>
  <div class="kpis">
    {kpi('Distributors', str(CUS_TYPE['Distributor']))}
    {kpi('Dealers', str(CUS_TYPE['Dealer']), chip('1 New', 'blue'))}
    {kpi('Retailers', str(CUS_TYPE['Retailer']), chip('1 New', 'blue'))}
    {kpi('Orders by Distributors', ML(PURCH_MONTH[-1]))}
  </div>
  <section class="card flush"><header><h2>Customer Hierarchy</h2></header><div class="body">{tree}</div></section>
  <div class="grid g-2">
    {card('Distributor Alpha', kv([('Customer Code', f'<span class="mono">{a["code"]}</span>'), ('Customer Since', a['since']), ('Price Tier', 'Primary Distributor Tier A'), ('Territory', 'Maharashtra and Goa'), ('Account Manager', 'Vikram Chopra'),
                                      ('Credit Limit', ML(CREDIT_LIMIT)), ('Outstanding Balance', ML(OUTSTANDING)), ('Dealers', str(CUS_TYPE['Dealer'])), ('Retailers', str(CUS_TYPE['Retailer']))]) + '<a class="btn block" data-link="CMP-CUS-02" style="margin-top:1rem">View Customer Details</a>')}
    <section class="card flush"><header><h2>Customers by Region</h2></header><div class="body">{table([('Region', ''), ('Dealers', 'num'), ('Retailers', 'num')], [reg_rows], foot=reg_foot)}</div></section>
  </div>
'''
page('company', 'customer-hierarchy-explorer', 'CMP-CUS-04', 'Company Administration — Super Admin — Customer Hierarchy Explorer (CMP-CUS-04)', body)
