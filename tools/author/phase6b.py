"""Phase 6, part B: Secondary Customer Owner: Schemes and Incentives, Scheme Details, Sales Reports, Inventory Reports, Return Requests, Create Return Request,
Support Ticket List, Create Support Ticket, Support Ticket Details, User Management, Create User, User Details; shared with the Manager: Return Requests,
Create Return Request, My Profile, Notifications. Dealer Bravo, Pune; supplier Distributor Alpha.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md "Phase 5 data" and "Phase 6 data"."""
from data import *

SQ = chr(0x2212)
def cancel(sid): return f'<a class="btn" data-link="{sid}">Cancel</a>'
em = lambda n: n.lower().replace(' ', '.') + '@dealerbravo.example'
cp_used = round(BRV_OWES / BRV_LIMIT * 100)
fin_col = {'Matte': '#0a48fd', 'Woodgrain': '#0b8fa8', 'Texture': '#7a36fb', 'Gloss': '#e0a030', 'Suede': '#0c9b6a', 'High Gloss': '#d43a2f', 'Metallic': '#8b93a3'}
def change(a, b):
    if not b: return chip('New', 'blue')
    v = (a - b) / b * 100
    return f'<span class="delta {"up" if v >= 0 else "down"}"><i data-icon="trend"></i>{abs(v):.1f}%</span>'

# ---------- Schemes and Incentives ----------
def prog(done, goal):
    pc = min(100, round(done / goal * 100))
    return f'<span class="inline-meter" style="justify-content:flex-start"><span class="meter {"ok" if done >= goal else ""}"><i style="width:{pc}%"></i></span><span style="white-space:nowrap"><b style="min-width:0">{N(done)}</b> of {N(goal)}</span></span>'
def sch_card(s):
    pc = round(s[6] / s[7] * 100)
    reached = f'{chip("Target Reached", "ok")} ' if s[6] >= s[7] else ''
    return f'''<section class="card"><header><h2>{s[1]}</h2><span style="margin-left:auto">{reached}{chip(s[5])}</span></header><div class="body">
      <div style="display:flex;align-items:baseline;gap:.5rem"><b style="font-size:1.5rem;letter-spacing:-.02em">{N(s[6])}</b><span>of {N(s[7])} sheets</span><b style="margin-left:auto">{pc}%</b></div>
      <span class="meter {"ok" if pc >= 90 else ""}" style="margin:.75rem 0 1.25rem"><i style="width:{min(pc, 100)}%"></i></span>
      {kv([('Scheme Number', f'<span class="mono">{s[0]}</span>'), ('Type', s[2]), ('Reward', s[8]), ('Ends', s[4])])}
      <a class="btn block" data-link="SEC-SCH-02" style="margin-top:1.25rem">View Scheme</a></div></section>'''
sch_rows = [f'<tr><td>{link("SEC-SCH-02", s[1])}</td><td class="mono nowrap">{s[0]}</td><td>{s[4]}</td><td>{prog(s[6], s[7]) if s[5] != "Upcoming" else "—"}</td><td class="nowrap">{s[8]}</td><td>{chip(s[5])}</td></tr>' for s in BSCH]
fest = BSCH[0]
body = f'''  <div class="head">
    <h1>Schemes and Incentives</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Scheme Summary</button><a class="btn pri" data-link="SEC-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Active Schemes', '2')}
    {kpi('Incentives Earned This Year', M(B_INCENTIVES))}
    {kpi('Sheets to Festive Target', f'{fest[7] - fest[6]} <small>sheets</small>', chip('35 days left', 'warn'))}
    {kpi('Upcoming Schemes', '1')}
  </div>
  <div class="grid g-2">{sch_card(BSCH[0])}{sch_card(BSCH[1])}</div>
  <section class="card flush"><header><h2>All Schemes</h2></header>
    <div class="body">{table([('Scheme', ''), ('Scheme Number', ''), ('Ends', ''), ('Progress in Sheets', ''), ('Reward', ''), ('Status', '')], sch_rows)}</div></section>
'''
page('secondary', 'schemes-and-incentives', 'SEC-SCH-01', 'Secondary Customer — Owner — Schemes and Incentives (SEC-SCH-01)', body)

# ---------- Scheme Details (SCH-2026-07) ----------
FESTIVE_ORDERS = [(o[0], o[1], o[2], o[5]) for o in BRV_ORDERS[:7]]
assert sum(f[2] for f in FESTIVE_ORDERS) == fest[6] == 690
q_rows = ''.join(f'<tr><td class="mono nowrap"><b>{o}</b></td><td>{d}</td><td>{chip(st)}</td><td class="num">{N(sh)}</td></tr>' for o, d, sh, st in FESTIVE_ORDERS)
body = f'''  <div class="head">
    <div class="title-row"><h1>{fest[1]}</h1>{chip('Active')}<span class="tag mono">{fest[0]}</span></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Terms</button><a class="btn pri" data-link="SEC-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Sheets Counted', N(fest[6]), chip(f'{fest[6] / fest[7] * 100:.0f}% of Target', 'blue'))}
    {kpi('Sheets Remaining', str(fest[7] - fest[6]))}
    {kpi('Days Left', '35')}
    {kpi('Rebate Rate', '1%')}
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      <section class="card"><header><h2>Progress to Target</h2></header><div class="body">
        <div style="display:flex;align-items:baseline;gap:.5rem"><b style="font-size:1.75rem;letter-spacing:-.02em">{N(fest[6])}</b><span>of {N(fest[7])} sheets</span><b style="margin-left:auto">{fest[6] / fest[7] * 100:.0f}%</b></div>
        <span class="meter ok" style="margin:.75rem 0 1.25rem"><i style="width:{fest[6] / fest[7] * 100:.0f}%"></i></span>
        {kv([('Rebate Earned So Far', M(0))])}</div></section>
      <section class="card flush"><header><h2>Qualifying Orders</h2></header><div class="body">{table([('Order Number', ''), ('Order Date', ''), ('Order Status', ''), ('Sheets Counted', 'num')], [q_rows], foot=f'<tfoot><tr><td colspan="3">Total</td><td class="num">{N(fest[6])}</td></tr></tfoot>')}</div></section>
    </div>
    <div class="stack">
      {card('Scheme Terms', kv([('Scheme Type', 'Volume Rebate'), ('Rebate Rate', '1% of order value'), ('Target', '750 sheets'), ('Start Date', '01/10/2026'), ('End Date', '30/11/2026'), ('Eligible Products', 'All 12 products'), ('Eligible Customers', 'Secondary Dealers')]))}
      <section class="card flush"><header><h2>Documents</h2></header><div class="body">{table([('Document', ''), ('Type', ''), ('', '')], [f'<tr><td><b>Scheme Terms</b></td><td><span class="tag">PDF</span></td><td><div class="row-actions">{dl_btn("Download terms")}</div></td></tr>'])}</div></section>
    </div>
  </div>
'''
page('secondary', 'scheme-details', 'SEC-SCH-02', 'Secondary Customer — Owner — Scheme Details (SEC-SCH-02)', body)

# ---------- Sales Reports ----------
fin_val = {}
for s_, v in TSOLD_VALUE.items(): fin_val[BY[s_][2]] = fin_val.get(BY[s_][2], 0) + v
area_val = {r[2]: r[9][-1] for r in RETAILERS}
area_col = {'Camp': 'var(--accent)', 'Kothrud': '#0b8fa8', 'Pimpri Chinchwad': '#e0a030'}
rr = ''.join(f'<tr><td class="nowrap">{link("SEC-RTL-02", r[1])} <span class="tag">{r[3]}</span></td><td>{r[2]}</td><td class="num">{N(RTL_SHEETS[r[0]])}</td><td class="num"><b>{M(r[9][-1])}</b></td><td class="num">{M(r[8])}</td><td>{change(r[9][-1], r[8])}</td></tr>' for r in sorted(RETAILERS, key=lambda r: -r[9][-1]))
pr = ''.join(f'<tr><td><div class="prod">{sw(s_)}<div><b>{BY[s_][1]}</b></div></div></td><td class="mono nowrap">{s_}</td><td class="num">{N(TSOLD[s_]) if TSOLD[s_] else "—"}</td><td class="num"><b>{M(TSOLD_VALUE[s_]) if TSOLD[s_] else "—"}</b></td>'
             f'<td><span class="inline-meter"><span class="meter"><i style="width:{TSOLD_VALUE[s_] / max(TSOLD_VALUE.values()) * 100:.0f}%"></i></span><b>{TSOLD_VALUE[s_] / 630000 * 100:.1f}%</b></span></td></tr>' for s_ in sorted(TSOLD, key=lambda x: -TSOLD_VALUE[x]) if TSOLD[s_])
body = f'''  <div class="head">
    <h1>Sales Reports</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><span class="sel"><small>Compared With</small> September 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="filters">{sel('Retailer', 'All Retailers')}{sel('Area', 'All Areas')}{sel('Finish', 'All Finishes')}</div>
  <div class="kpis">
    {kpi('Sales', ML(630000), up(pct(630000, 600000)))}
    {kpi('Sheets Sold', N(370))}
    {kpi('Average Sale Value', M(630000 // len(TSALES)))}
    {kpi('Active Retailers', '3')}
  </div>
  <div class="grid g-2">
    {card('Sales by Finish', chart('bars', list(fin_val), [{'name': 'Sales', 'values': list(fin_val.values()), 'color': 'var(--accent)'}], money=True, height=260))}
    <section class="card"><header><h2>Sales by Area</h2></header><div class="body center">{chart('donut', series=[{'name': a, 'value': v, 'color': area_col[a]} for a, v in sorted(area_val.items(), key=lambda x: -x[1])], center='3', caption='areas')}</div></section>
  </div>
  <section class="card flush"><header><h2>Sales by Retailer</h2></header>
    <div class="body">{table([('Retailer', ''), ('Area', ''), ('Sheets', 'num'), ('Sales', 'num'), ('September Sales', 'num'), ('Change', '')], [rr])}</div></section>
  <section class="card flush"><header><h2>Sales by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Sales', 'num'), ('Share of Sales', '')], [pr])}</div></section>
'''
page('secondary', 'sales-reports', 'SEC-RPT-01', 'Secondary Customer — Owner — Sales Reports (SEC-RPT-01)', body)

# ---------- Inventory Reports ----------
ag_tot = [sum(BAGE[s][i] for s in BAGE) for i in range(3)]
assert sum(ag_tot) == 1058
ir = ''.join(f'<tr><td><div class="prod">{sw(p[0])}<div><b>{p[1]}</b></div></div></td><td class="mono nowrap">{p[0]}</td><td class="num"><b>{N(BSTOCK[p[0]]["on_hand"])}</b></td><td class="num">{N(TSOLD[p[0]]) if TSOLD[p[0]] else "—"}</td>'
             f'<td class="num">{N(BAGE[p[0]][0]) if BAGE[p[0]][0] else "—"}</td><td class="num">{N(BAGE[p[0]][1]) if BAGE[p[0]][1] else "—"}</td><td class="num">{N(BAGE[p[0]][2]) if BAGE[p[0]][2] else "—"}</td></tr>' for p in P)
body = f'''  <div class="head">
    <h1>Inventory Reports</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('Stock Value', ML(BSTOCK_VALUE))}
    {kpi('Sheets on Hand', N(1058))}
    {kpi('Sheets Sold This Month', N(370))}
    {kpi('Sheets Over 60 Days', N(ag_tot[2]), chip(f'{ag_tot[2] / 1058 * 100:.0f}% of Stock', 'warn'))}
  </div>
  <div class="grid g-2">
    <section class="card"><header><h2>Stock by Finish</h2></header><div class="body center">{chart('donut', series=[{'name': f, 'value': v, 'color': fin_col[f]} for f, v in sorted(BFINISH.items(), key=lambda x: -x[1])], center=N(1058), caption='sheets')}</div></section>
    {card('Stock Ageing', chart('bars', ['Up to 30 days', '31 to 60 days', 'Over 60 days'], [{'name': 'Sheets on hand', 'values': ag_tot, 'color': 'var(--accent)'}], height=260))}
  </div>
  <section class="card flush"><header><h2>Stock by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('On Hand', 'num'), ('Sold This Month', 'num'), ('Up to 30 Days', 'num'), ('31 to 60 Days', 'num'), ('Over 60 Days', 'num')], [ir],
      foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(1058)}</td><td class="num">{N(370)}</td><td class="num">{N(ag_tot[0])}</td><td class="num">{N(ag_tot[1])}</td><td class="num">{N(ag_tot[2])}</td></tr></tfoot>')}</div></section>
'''
page('secondary', 'inventory-reports', 'SEC-RPT-02', 'Secondary Customer — Owner — Inventory Reports (SEC-RPT-02)', body)

# ---------- Return Requests (shared with the Manager) ----------
OPEN = ('Under Review', 'Approved', 'Pickup Scheduled')
rows = [f'<tr><td class="mono nowrap"><b>{r[0]}</b></td><td>{r[1]}</td><td class="mono nowrap">{r[2]}</td><td>{BY[r[3]][1]}</td><td class="num">{r[4]}</td><td>{r[5]}</td><td>{chip(r[6])}</td><td class="num">{M(BCREDIT[r[0]]) if r[0] in BCREDIT else "—"}</td></tr>' for r in BRET]
body = f'''  <div class="head">
    <h1>Return Requests</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Requests</button><a class="btn pri" data-link="SEC-RET-02"><i data-icon="plus"></i>Create Return Request</a></div>
  </div>
  <div class="kpis">
    {kpi('Open Requests', str(sum(1 for r in BRET if r[6] in OPEN)))}
    {kpi('Sheets Under Return', str(sum(r[4] for r in BRET if r[6] in OPEN)))}
    {kpi('Credit Issued', M(sum(BCREDIT.values())), chip('2 requests', 'plain'))}
    {kpi('Requests This Year', str(len(BRET)))}
  </div>
  <section class="card flush">
    {tabs([('All Requests', len(BRET), True), ('Open', 2, False), ('Credit Issued', 2, False), ('Rejected', 1, False)])}
    {filters('Search by return or order number', 'Search return requests', ('Date Range', 'Last 90 days'), ('Reason', 'All'))}
    <div class="body">{table([('Return Number', ''), ('Date', ''), ('Order Number', ''), ('Product', ''), ('Sheets', 'num'), ('Reason', ''), ('Status', ''), ('Credit Amount', 'num')], rows)}
      {pager(f'Showing 1 to {len(BRET)} of {len(BRET)} requests', 1)}</div>
  </section>
'''
page('secondary', 'return-requests', 'SEC-RET-01', 'Secondary Customer — Owner — Return Requests (SEC-RET-01)', body)

# ---------- Create Return Request ----------
o33 = next(s for s in BRV_SALES if s['number'] == 'SAL-2026-3033')
RQ = {'LM-TEK-006': 5, 'LM-IVR-008': 2}
assert all(q <= dict(o33['lines'])[s] for s, q in RQ.items())
lines = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num">{N(q)}</td><td>{qty(RQ.get(s, 0))}</td></tr>' for s, q in o33['lines'])
def radio(title, on=False, name='r'):
    return f'<label class="radio{" on" if on else ""}"><input type="radio" name="{name}"{" checked" if on else ""}><span><b>{title}</b></span></label>'
body = f'''  <div class="head">
    <h1>Create Return Request</h1>
    <div class="acts">{cancel('SEC-RET-01')}<button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Submit Return Request</button></div>
  </div>
  <div class="grid g-main-side" style="--side:20rem">
    <div class="stack">
      {form('Return Details', fld('Order', 'ord', 'SAL-2026-3033', 'select', ['SAL-2026-3040', 'SAL-2026-3033', 'SAL-2026-3029', 'SAL-2026-3021']), fld('Return Reason', 'rs', 'Surface Defect', 'select', ['Damaged in Transit', 'Surface Defect', 'Wrong Product Delivered', 'Shade Mismatch']),
            fld('Pickup Location', 'pl', 'Hadapsar Godown', 'select', ['Hadapsar Godown', 'Shop, Hadapsar']), fld('Contact for Pickup', 'cp', 'Arjun Nair, +91 90000 31002'))}
      <section class="card flush"><header><h2>Items to Return</h2></header><div class="body">{table([('Product', ''), ('SKU', ''), ('Ordered Sheets', 'num'), ('Sheets to Return', '')], [lines], 'stack-sm')}</div></section>
      <section class="card"><header><h2>Photos</h2></header><div class="body"><div class="drop"><span class="file"><i data-icon="doc"></i>surface-defect-1.jpg</span><span class="file"><i data-icon="doc"></i>surface-defect-2.jpg</span><button class="btn sm" type="button"><i data-icon="upload"></i>Upload Photos</button></div></div></section>
      <section class="card"><header><h2>Notes</h2></header><div class="body"><div class="field"><label for="nt">Notes for Distributor Alpha</label><textarea class="input" id="nt" placeholder="Describe the issue"></textarea></div></div></section>
    </div>
    <div class="stack">
      <section class="card"><header><h2>Preferred Resolution</h2></header><div class="body"><div class="stack">{radio('Credit Note', True, 'res')}{radio('Replacement Sheets', False, 'res')}</div></div></section>
      {card('Return Summary', kv([('Order', '<span class="mono">SAL-2026-3033</span>'), ('Products', '2'), ('Sheets to Return', str(sum(RQ.values()))), ('Pickup Location', 'Hadapsar Godown')]))}
    </div>
  </div>
'''
page('secondary', 'create-return-request', 'SEC-RET-02', 'Secondary Customer — Owner — Create Return Request (SEC-RET-02)', body)

# ---------- Support Ticket List ----------
rows = [f'<tr><td class="mono nowrap">{link("SEC-SUP-03", t[0])}</td><td>{t[2]}</td><td>{t[3]}</td><td>{chip(t[4])}</td><td>{t[1]}</td><td>{t[5]}</td><td>{chip(t[6])}</td></tr>' for t in BTK]
body = f'''  <div class="head">
    <h1>Support Ticket List</h1>
    <div class="acts"><a class="btn pri" data-link="SEC-SUP-02"><i data-icon="plus"></i>Create Support Ticket</a></div>
  </div>
  <div class="kpis">
    {kpi('Open Tickets', '2')}
    {kpi('In Progress', '1', chip('TKT-2026-D0746', 'blue'))}
    {kpi('Resolved This Month', '1')}
    {kpi('Closed', '2')}
  </div>
  <section class="card flush">
    {tabs([('All Tickets', len(BTK), True), ('Open', 2, False), ('Resolved', 1, False), ('Closed', 2, False)])}
    {filters('Search by ticket number or subject', 'Search tickets', ('Category', 'All'), ('Priority', 'All'))}
    <div class="body">{table([('Ticket Number', ''), ('Subject', ''), ('Category', ''), ('Priority', ''), ('Created', ''), ('Last Updated', ''), ('Status', '')], rows)}
      {pager(f'Showing 1 to {len(BTK)} of {len(BTK)} tickets', 1)}</div>
  </section>
'''
page('secondary', 'support-ticket-list', 'SEC-SUP-01', 'Secondary Customer — Owner — Support Ticket List (SEC-SUP-01)', body)

# ---------- Create Support Ticket ----------
body = f'''  <div class="head">
    <h1>Create Support Ticket</h1>
    <div class="acts">{cancel('SEC-SUP-01')}<button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Submit Ticket</button></div>
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      {form('Ticket Details', fld('Subject', 'sb', 'Credit Note Missing for RTN-2026-D0486', full=True), fld('Category', 'cg', 'Billing', 'select', ['Delivery', 'Billing', 'Account', 'Schemes', 'Product']), fld('Priority', 'pr', 'Medium', 'select', ['Low', 'Medium', 'High']),
            fld('Related Order', 'ro', 'SAL-2026-3017', 'select', ['None', 'SAL-2026-3042', 'SAL-2026-3040', 'SAL-2026-3033', 'SAL-2026-3029', 'SAL-2026-3021', 'SAL-2026-3017']), fld('Related Invoice', 'ri', 'SAL-2026-3017', 'select', ['None', 'SAL-2026-3040', 'SAL-2026-3033', 'SAL-2026-3029', 'SAL-2026-3021', 'SAL-2026-3017']),
            fld('Description', 'ds', f'The credit of {M(BCREDIT["RTN-2026-D0486"])} for return request RTN-2026-D0486 is not shown against invoice SAL-2026-3017.', 'textarea', full=True))}
      <section class="card"><header><h2>Attachments</h2></header><div class="body"><div class="drop"><span class="file"><i data-icon="doc"></i>credit-note.pdf</span><button class="btn sm" type="button"><i data-icon="upload"></i>Upload Files</button></div></div></section>
    </div>
    <div class="stack">
      {card('Distributor Alpha Support', kv([('Relationship Manager', 'Kavita Joshi'), ('Phone', '+91 90000 21002'), ('Email', 'kavita.joshi@<wbr>distributoralpha.example'), ('Support Hours', 'Monday to Saturday, 09:30 to 18:30')]))}
    </div>
  </div>
'''
page('secondary', 'create-support-ticket', 'SEC-SUP-02', 'Secondary Customer — Owner — Create Support Ticket (SEC-SUP-02)', body)

# ---------- Support Ticket Details (TKT-2026-D0746) ----------
def msg(who, init, when, text, me=False, files=()):
    fl = f'<div class="files">{"".join(f"<span class=file><i data-icon=doc></i>{f}</span>" for f in files)}</div>' if files else ''
    return f'<div class="msg{" me" if me else ""}"><div class="av">{init}</div><div><div class="top-line"><b>{who}</b><time>{when}</time></div><div class="bubble">{text}{fl}</div></div></div>'
thread = ''.join([
    msg('Sunita Rao', 'SR', '25/10/2026 11:05', 'SAL-2026-3040 was dispatched on 24 October. Please confirm when it will reach our godown in Hadapsar.', True, ['packing-list.pdf']),
    msg('Kavita Joshi, Distributor Alpha', 'KJ', '25/10/2026 14:20', 'The vehicle MH 12 QR 4418 is on its way and should reach Hadapsar by midday on 26 October.'),
    msg('Sunita Rao', 'SR', '25/10/2026 14:45', 'Thank you. We will keep the godown open. Please share the driver number.', True),
    msg('Kavita Joshi, Distributor Alpha', 'KJ', '26/10/2026 09:30', 'The driver is Santosh Gaikwad, +91 90000 12346.'),
])
t0 = BTK[0]
body = f'''  <div class="head">
    <div class="title-row"><h1>{t0[2]}</h1>{chip(t0[6])}{chip(t0[4])}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="check"></i>Close Ticket</button></div>
  </div>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      {card('Conversation', f'<div class="thread">{thread}</div>')}
      <section class="card"><header><h2>Reply</h2></header><div class="body"><div class="reply"><textarea class="input" aria-label="Reply" placeholder="Write a reply"></textarea>
        <div class="row"><button class="btn" type="button"><i data-icon="upload"></i>Attach Files</button><button class="btn pri" type="button">Send Reply</button></div></div></div></section>
    </div>
    <div class="stack">
      {card('Ticket Information', kv([('Ticket Number', f'<span class="mono">{t0[0]}</span>'), ('Status', chip(t0[6])), ('Priority', chip(t0[4])), ('Category', t0[3]), ('Created', '25/10/2026 11:05'), ('Last Updated', '26/10/2026 09:30'), ('Assigned To', 'Kavita Joshi')]))}
      {card('Related Records', kv([('Order', link('SEC-ORD-02', 'SAL-2026-3040', False)), ('Invoice', link('SEC-BIL-02', 'SAL-2026-3040', False))]))}
    </div>
  </div>
'''
page('secondary', 'support-ticket-details', 'SEC-SUP-03', 'Secondary Customer — Owner — Support Ticket Details (SEC-SUP-03)', body)

# ---------- User Management ----------
rows = [f'<tr><td>{link("SEC-USR-03", u[0])}</td><td>{u[1]}</td><td class="nowrap">{em(u[0])}</td><td class="nowrap">{u[3]}</td><td>{chip(u[4])}</td><td><div class="row-actions"><a class="btn sm" data-link="SEC-USR-03">View</a></div></td></tr>' for u in BUSERS]
body = f'''  <div class="head">
    <h1>User Management</h1>
    <div class="acts"><a class="btn pri" data-link="SEC-USR-02"><i data-icon="plus"></i>Create User</a></div>
  </div>
  <div class="kpis">
    {kpi('Users', str(len(BUSERS)))}
    {kpi('Active', '2')}
    {kpi('Invited', '1')}
    {kpi('Inactive', '1')}
  </div>
  <section class="card flush">
    {tabs([('All Users', len(BUSERS), True), ('Active', 2, False), ('Invited', 1, False), ('Inactive', 1, False)])}
    {filters('Search by name or email address', 'Search users', ('Role', 'All'))}
    <div class="body">{table([('Name', ''), ('Role', ''), ('Email Address', ''), ('Last Sign-In', ''), ('Status', ''), ('', '')], rows)}</div>
  </section>
'''
page('secondary', 'user-management', 'SEC-USR-01', 'Secondary Customer — Owner — User Management (SEC-USR-01)', body)

# ---------- Create User ----------
MODS = [('Product Catalogue and Orders', 1, 1), ('Inventory', 1, 1), ('Retailers', 1, 1), ('Tertiary Sales', 1, 1), ('Invoices and Payments', 1, 0), ('Schemes and Incentives', 1, 0),
        ('Reports', 1, 1), ('Return Requests', 1, 1), ('Support Tickets', 1, 0), ('User Management', 1, 0), ('Company Profile', 1, 0), ('My Profile and Notifications', 1, 1)]
tick = lambda v: '<i data-icon="check"></i>' if v else '<span class="no">—</span>'
mrows = [f'<tr><td><b>{m[0]}</b></td><td class="c">{tick(m[1])}</td><td class="c">{tick(m[2])}</td></tr>' for m in MODS]
mtable = table([('Area', ''), ('Owner', 'c'), ('Sales and Inventory Manager', 'c')], mrows)
body = f'''  <div class="head">
    <h1>Create User</h1>
    <div class="acts">{cancel('SEC-USR-01')}<button class="btn pri" type="button">Send Invitation</button></div>
  </div>
  <div class="grid g-main-side" style="--side:20rem">
    {form('Personal Details', fld('First Name', 'fn', 'Meena'), fld('Last Name', 'ln', 'Kulkarni'), fld('Email Address', 'em', em('Meena Kulkarni')), fld('Mobile Number', 'mb', '+91 90000 31004'))}
    <section class="card"><header><h2>Role</h2></header><div class="body"><div class="stack">{radio('Owner', False, 'role')}{radio('Sales and Inventory Manager', True, 'role')}</div></div></section>
  </div>
  <section class="card flush"><header><h2>Access by Role</h2></header><div class="body">{mtable}</div></section>
'''
page('secondary', 'create-user', 'SEC-USR-02', 'Secondary Customer — Owner — Create User (SEC-USR-02)', body)

# ---------- User Details (Arjun Nair) ----------
act = [('26/10/2026 10:05', 'Placed order draft for SAL-2026-3042'), ('26/10/2026 08:55', 'Signed in'), ('25/10/2026 17:20', 'Recorded sale TSL-2026-0412'), ('22/10/2026 11:15', 'Raised return request RTN-2026-D0508'), ('21/10/2026 18:02', 'Recorded sale TSL-2026-0410')]
arows = [f'<tr><td class="nowrap">{d}</td><td><b>{a}</b></td></tr>' for d, a in act]
accrows = [f'<tr><td><b>{m[0]}</b></td><td class="c">{tick(m[2])}</td></tr>' for m in MODS]
body = f'''  <div class="head">
    <div class="title-row"><h1>Arjun Nair</h1>{chip('Active')}<span class="tag">Sales and Inventory Manager</span></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="lock"></i>Reset Password</button><button class="btn" type="button"><i data-icon="edit"></i>Edit User</button><button class="btn danger" type="button">Deactivate User</button></div>
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      {card('Profile', kv([('Full Name', 'Arjun Nair'), ('Email Address', em('Arjun Nair')), ('Mobile Number', '+91 90000 31002'), ('Role', 'Sales and Inventory Manager'), ('Added On', '18/06/2021'), ('Added By', 'Sunita Rao'), ('Last Sign-In', '26/10/2026 08:55')]))}
      <section class="card flush"><header><h2>Recent Activity</h2></header><div class="body">{table([('Date', ''), ('Activity', '')], arows)}</div></section>
    </div>
    <section class="card flush"><header><h2>Access</h2></header><div class="body">{table([('Area', ''), ('Access', 'c')], accrows)}</div></section>
  </div>
'''
page('secondary', 'user-details', 'SEC-USR-03', 'Secondary Customer — Owner — User Details (SEC-USR-03)', body)

# ---------- My Profile (Owner and Sales and Inventory Manager) ----------
PEOPLE = [('OWN', 'Sunita Rao', '+91 90000 31001', '26/10/2026 09:12'), ('MGR', 'Arjun Nair', '+91 90000 31002', '26/10/2026 08:55')]
def per_role(fn): return ''.join(f'<div data-role="{r}">{fn(r, n, ph, ls)}</div>' for r, n, ph, ls in PEOPLE)
def pform(r, n, ph, ls):
    return f'<div class="form-grid">{fld("Full Name", "nm" + r, n)}{fld("Mobile Number", "mb" + r, ph)}{fld("Email Address", "em" + r, em(n), full=True)}{fld("Language", "lg" + r, "English", "select", ["English", "Hindi", "Marathi"], full=True)}</div>'
prefs = [('Order Updates', 1, 1), ('Invoice and Payment Updates', 1, 1), ('Stock Alerts', 1, 1), ('Scheme Announcements', 0, 1), ('Support Replies', 1, 1)]
prow = [f'<tr><td><b>{e}</b></td><td class="c"><label class="check"><input type="checkbox"{" checked" if a else ""} aria-label="{e} by email"></label></td><td class="c"><label class="check"><input type="checkbox"{" checked" if b else ""} aria-label="{e} in the portal"></label></td></tr>' for e, a, b in prefs]
sess = [('Chrome on Windows', 'Pune', chip('Current Session', 'ok')), ('Chrome on Android', 'Pune', '25/10/2026 19:12'), ('Safari on iPhone', 'Pimpri', '22/10/2026 08:03')]
srow = [f'<tr><td class="nowrap"><b>{a}</b></td><td>{b}</td><td class="nowrap">{c}</td></tr>' for a, b, c in sess]
body = f'''  <div class="head">
    <h1>My Profile</h1>
    <div class="acts"><button class="btn" type="button">Cancel</button><button class="btn pri" type="button">Save Changes</button></div>
  </div>
  <section class="card pad" style="flex-direction:row;align-items:center;gap:1.25rem;flex-wrap:wrap">
    <div class="av-lg" data-me="initials"></div>
    <div style="flex:1;min-width:14rem;display:grid;gap:.5rem"><h2 style="font-size:1.25rem" data-me="name"></h2>
      <div style="display:flex;flex-wrap:wrap;gap:.5rem">{chip('Active', 'ok')}<span class="tag" data-me="role"></span></div></div>
    <dl class="kv left" style="grid-template-columns:auto auto;gap:.5rem 1.25rem"><dt>Organisation</dt><dd>Dealer Bravo</dd><dt>Last Sign-In</dt><dd>{per_role(lambda r, n, ph, ls: ls).replace('<div', '<span').replace('</div>', '</span>')}</dd></dl>
  </section>
  <div class="grid g-2">
    <section class="card"><header><h2>Personal Details</h2></header><div class="body">{per_role(pform)}</div></section>
    <section class="card"><header><h2>Change Password</h2></header><div class="body"><div class="form-grid">
      <div class="field full"><label for="cur">Current Password</label><input class="input" id="cur" type="password" value="password"></div>
      <div class="field"><label for="new">New Password</label><input class="input" id="new" type="password" value="password"></div>
      <div class="field"><label for="con">Confirm New Password</label><input class="input" id="con" type="password" value="password"></div></div>
      <button class="btn block" type="button" style="margin-top:1rem"><i data-icon="lock"></i>Update Password</button></div></section>
  </div>
  <div class="grid g-2">
    <section class="card flush"><header><h2>Notification Preferences</h2></header><div class="body">{table([('Notification', ''), ('Email', 'c'), ('In the Portal', 'c')], prow, 'pref')}</div></section>
    <section class="card flush"><header><h2>Signed-In Devices</h2></header><div class="body">{table([('Device', ''), ('City', ''), ('Last Active', '')], srow)}</div></section>
  </div>
'''
page('secondary', 'my-profile', 'SEC-PRO-02', 'Secondary Customer — Owner — My Profile (SEC-PRO-02)', body)

# ---------- Notifications (three unread for each role, matching the bell badge) ----------
def n(sid, title, ref, when, icon, kind='', unread=False):
    return (f'<li{" class=unread" if unread else ""}><span class="dot {kind}"><i data-icon="{icon}"></i></span><div class="title"><a data-link="{sid}">{title}</a><span class="tag mono">{ref}</span></div><time>{when}</time></li>')
def day(label, *items): return f'<div class="day">{label}</div><ul class="feed ntf">{"".join(items)}</ul>'
OWN = (day('Today', n('SEC-ORD-02', 'Order Submitted', NEW_ORDER, '16:05', 'cart', '', True), n('SEC-SUP-03', 'New Reply on Support Ticket', 'TKT-2026-D0746', '09:30', 'help', '', True), n('SEC-INV-02', 'Low Stock', 'LM-CAL-003', '08:30', 'warn', 'warn', True))
       + day('24 October 2026', n('SEC-ORD-02', 'Order In Transit', 'SAL-2026-3040', '17:45', 'truck'))
       + day('23 October 2026', n('SEC-BIL-04', 'Payment Confirmed', 'PAY-2026-D0521', '09:20', 'cash', 'ok'))
       + day('22 October 2026', n('SEC-RET-01', 'Return Request Submitted', 'RTN-2026-D0508', '11:20', 'ret')))
MGR = (day('Today', n('SEC-RET-01', 'Return Request Approved', 'RTN-2026-D0503', '09:40', 'ret', 'ok', True), n('SEC-INV-02', 'Low Stock', 'LM-CAL-003', '08:30', 'warn', 'warn', True), n('SEC-ORD-02', 'Delivery Due Today', 'SAL-2026-3040', '07:00', 'truck', '', True))
       + day('25 October 2026', n('SEC-TSL-03', 'Sale Recorded', 'TSL-2026-0412', '17:20', 'trend'))
       + day('24 October 2026', n('SEC-ORD-02', 'Order In Transit', 'SAL-2026-3040', '17:45', 'truck')))
body = f'''  <div class="head">
    <h1>Notifications</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="check"></i>Mark All as Read</button></div>
  </div>
  <section class="card flush">
    <div style="padding:0 1.125rem"><div class="tabs"><span class="on">All Notifications<b data-count=".ntf li"></b></span><span>Unread<b data-count=".ntf li.unread"></b></span></div></div>
    <div class="body" style="padding:0 1.125rem 1rem"><div data-role="OWN">{OWN}</div><div data-role="MGR">{MGR}</div></div>
  </section>
'''
page('secondary', 'notifications', 'SEC-NTF-01', 'Secondary Customer — Owner — Notifications (SEC-NTF-01)', body)
