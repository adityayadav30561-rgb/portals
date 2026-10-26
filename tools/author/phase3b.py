"""Phase 3, part B: Primary Customer Owner (and Accountant for the invoice and payment screens): Invoices Overview, Invoice
Details, Payments Overview, Payment Details, Schemes and Incentives, Scheme Details, Sales Reports, Inventory Reports.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md."""
from data import *
import datetime

TODAY = datetime.date(2026, 10, 26)
def d(s): return datetime.date(int(s[6:]), int(s[3:5]), int(s[:2]))
def inv_status(i):
    bal = i[4] - i[5]
    if bal == 0: return chip('Paid')
    if d(i[3]) < TODAY: return chip(f'Overdue {(TODAY - d(i[3])).days} days', 'bad')
    return chip('Partly Paid') if i[5] else chip('Unpaid')

# ---------- Invoices Overview ----------
rows = [f'<tr><td>{link("PRI-BIL-02", i[0])}</td><td class="mono nowrap">{i[1]}</td><td>{i[2]}</td><td>{i[3]}</td><td class="num">{M(i[4])}</td><td class="num"><b>{M(i[4] - i[5])}</b></td><td>{inv_status(i)}</td></tr>' for i in OPEN_INV]
foot = f'<tfoot><tr><td colspan="4">Total</td><td class="num">{M(sum(i[4] for i in OPEN_INV))}</td><td class="num">{M(OUTSTANDING)}</td><td></td></tr></tfoot>'
body = f'''  <div class="head">
    <h1>Invoices Overview</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Invoices</button></div>
  </div>
  <div class="kpis">
    {kpi('Outstanding Balance', ML(OUTSTANDING), chip('37% of Credit Limit', 'warn'))}
    {kpi('Invoiced This Month', ML(INV_ISSUED_OCT), chip('4 invoices', 'plain'))}
    {kpi('Paid This Month', ML(sum(p[2] for p in PAID_OCT)), chip('5 payments', 'plain'))}
    {kpi('Overdue', ML(sum(i[4] - i[5] for i in OVERDUE)), '<span class="delta down">2 invoices</span>')}
  </div>
  <section class="card flush">
    {tabs([('Open Invoices', 5, True), ('Overdue', 2, False), ('Paid', 129, False), ('All Invoices', 134, False)])}
    {filters('Search by invoice or order number', 'Search invoices', ('Date Range', 'Last 90 days'), ('Status', 'All'))}
    <div class="body">{table([('Invoice Number',''), ('Order Number',''), ('Issue Date',''), ('Due Date',''), ('Invoice Amount','num'), ('Balance Due','num'), ('Status','')], rows, foot=foot)}
      {pager('Showing 1 to 5 of 5 open invoices', 1)}</div>
  </section>
'''
page('primary', 'invoices-overview', 'PRI-BIL-01', 'Primary Customer — Owner — Invoices Overview (PRI-BIL-01)', body)

# ---------- Invoice Details (INV-2026-03318) ----------
L = [('LM-WNT-001', 100, 1140), ('LM-ARC-002', 150, 905), ('LM-CHR-007', 60, 1055), ('LM-WNG-011', 50, 1170)]
sub = sum(q * p for _, q, p in L); total = sub + 33440 * 2 + 4500; assert (sub, total) == (371550, 442930)
inv = INVOICES[0]; assert inv[0] == 'INV-2026-03318' and inv[4] == total
lines = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num">{N(q)}</td><td class="num">{M(p)}</td><td class="num"><b>{M(q * p)}</b></td></tr>' for s, q, p in L)
body = f'''  <div class="head">
    <div class="title-row"><h1>{inv[0]}</h1>{chip('Unpaid')}{chip('Due in 43 days', 'blue')}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="print"></i>Print Invoice</button><button class="btn" type="button"><i data-icon="download"></i>Download Invoice</button><a class="btn pri" data-link="PRI-SUP-02" data-role="OWN"><i data-icon="help"></i>Raise Support Ticket</a></div>
  </div>
  <section class="card pad"><div class="stats" style="--cols:repeat(5,minmax(0,1fr))"><div><span>Issue Date</span><b>{inv[2]}</b></div><div><span>Due Date</span><b>{inv[3]}</b></div><div><span>Invoice Amount</span><b>{M(total)}</b></div><div><span>Amount Paid</span><b>{M(0)}</b></div><div><span>Balance Due</span><b>{M(total)}</b></div></div></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
    <section class="card flush"><header><h2>Items</h2></header>
      <div class="body">{table([('Product',''), ('SKU',''), ('Sheets','num'), ('Price per Sheet','num'), ('Amount','num')], [lines], foot=f'<tfoot><tr><td colspan="4">Subtotal</td><td class="num">{M(sub)}</td></tr></tfoot>')}
        <div style="padding:1rem 1.125rem"><dl class="kv" style="max-width:22rem;margin-left:auto"><dt>Central GST 9%</dt><dd>{M(33440)}</dd><dt>State GST 9%</dt><dd>{M(33440)}</dd><dt>Freight</dt><dd>{M(4500)}</dd></dl>
        <dl class="kv total" style="max-width:22rem;margin-left:auto"><dt>Total</dt><dd>{M(total)}</dd></dl></div></div></section>
    <section class="card flush"><header><h2>Invoice Activity</h2></header><div class="body">{table([('Date',''), ('Event',''), ('By','')], [
      '<tr><td class="nowrap">25/10/2026 10:12</td><td><b>Invoice viewed</b></td><td>Rajesh Menon</td></tr>',
      '<tr><td class="nowrap">24/10/2026 06:32</td><td><b>Invoice sent by email</b></td><td>Crestline Laminates</td></tr>',
      '<tr><td class="nowrap">24/10/2026 06:30</td><td><b>Invoice issued</b></td><td>Crestline Laminates</td></tr>'])}</div></section>
    </div>
    <div class="stack">
      {card('Invoice Information', kv([('Invoice Number', f'<span class="mono">{inv[0]}</span>'), ('Order Number', link('PRI-ORD-02', inv[1], False)), ('Dispatch Number', '<span class="mono">DSP-2026-5521</span>'), ('Payment Terms', '45 days'), ('Status', chip('Unpaid'))]))}
      {card('Billed To', kv([('Customer', 'Distributor Alpha Private Limited'), ('GST Number', '<span style="white-space:nowrap">27AABCD4521F1Z7</span>'), ('Address', 'Plot 14, Bhiwandi Logistics Park, Thane District, Maharashtra, Postal Code 421302')]))}
      {card('Issued By', kv([('Company', 'Crestline Laminates'), ('GST Number', '<span style="white-space:nowrap">24AABCC7782M1Z4</span>'), ('Warehouse', 'Plant Warehouse, Vapi, Gujarat')]))}
    </div>
  </div>
'''
page('primary', 'invoice-details', 'PRI-BIL-02', 'Primary Customer — Owner — Invoice Details (PRI-BIL-02)', body)

# ---------- Payments Overview ----------
pay_rows = [f'<tr><td class="mono nowrap"><b>{link("PRI-BIL-04", p[0], False)}</b></td><td>{p[1]}</td><td>{p[3]}</td><td class="mono nowrap">{p[4]}</td><td class="num"><b>{M(p[2])}</b></td><td>{chip("Confirmed", "ok")}</td><td><div class="row-actions"><a class="btn sm" data-link="PRI-BIL-04">View</a></div></td></tr>' for p in PAYMENTS]
paid_oct = sum(p[2] for p in PAID_OCT)
mode_col = {'Bank Transfer': 'var(--accent)', 'Net Banking': '#0b8fa8', 'Cheque': '#e0a030'}
body = f'''  <div class="head">
    <h1>Payments Overview</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Payments</button></div>
  </div>
  <div class="kpis">
    {kpi('Paid This Month', ML(paid_oct), chip('5 payments', 'plain'))}
    {kpi('Largest Payment', ML(max(p[2] for p in PAID_OCT)))}
    {kpi('Average Payment', ML(round(paid_oct / 5)))}
    {kpi('Outstanding Balance', ML(OUTSTANDING))}
  </div>
  <div class="grid g-chart">
    {card('Payments by Month', chart('bars', MONTHS, [{'name': 'Payments to Crestline', 'values': PAID_MONTH, 'color': 'var(--ok)'}], money=True, height=280))}
    <section class="card"><header><h2>Payments by Mode</h2></header><div class="body center">{chart('donut', series=[{'name': m, 'value': v, 'color': mode_col[m]} for m, v in sorted(MODE_OCT.items(), key=lambda x: -x[1])], center='5', caption='payments')}</div></section>
  </div>
  <section class="card flush">
    {filters('Search by payment or invoice number', 'Search payments', ('Date Range', 'Last 90 days'), ('Mode', 'All'))}
    <div class="body">{table([('Payment Number',''), ('Date',''), ('Mode',''), ('Invoice Number',''), ('Amount','num'), ('Status',''), ('','')], pay_rows)}
      {pager('Showing 1 to 10 of 131 payments')}</div>
  </section>
'''
page('primary', 'payments-overview', 'PRI-BIL-03', 'Primary Customer — Owner — Payments Overview (PRI-BIL-03)', body)

# ---------- Payment Details (PAY-2026-02217) ----------
pay = PAYMENTS[0]; i291 = INVOICES[1]
assert pay[0] == 'PAY-2026-02217' and pay[4] == i291[0] and i291[4] - pay[2] == 418400
body = f'''  <div class="head">
    <div class="title-row"><h1>{pay[0]}</h1>{chip('Confirmed', 'ok')}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Receipt</button><a class="btn pri" data-link="PRI-BIL-02"><i data-icon="receipt"></i>View Invoice</a></div>
  </div>
  <section class="card pad"><div class="stats" style="--cols:repeat(4,minmax(0,1fr))"><div><span>Amount</span><b>{M(pay[2])}</b></div><div><span>Payment Date</span><b>{pay[1]}</b></div><div><span>Mode</span><b>{pay[3]}</b></div><div><span>Bank Reference</span><b class="mono">SB26102100417</b></div></div></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      <section class="card flush"><header><h2>Invoices Settled</h2></header><div class="body">{table([('Invoice Number',''), ('Invoice Amount','num'), ('This Payment','num'), ('Balance After','num'), ('Status','')],
        [f'<tr><td>{link("PRI-BIL-02", i291[0])}</td><td class="num">{M(i291[4])}</td><td class="num"><b>{M(pay[2])}</b></td><td class="num">{M(i291[4] - pay[2])}</td><td>{chip("Partly Paid")}</td></tr>'])}</div></section>
      <section class="card"><header><h2>Payment Progress</h2></header><div class="body"><ol class="track">
        <li class="done"><i></i><b>Recorded</b><span>21/10/2026 14:20</span></li><li class="done"><i></i><b>Received by Crestline</b><span>22/10/2026 10:05</span></li><li class="done"><i></i><b>Confirmed</b><span>22/10/2026 16:30</span></li></ol></div></section>
    </div>
    <div class="stack">
      {card('Payment Information', kv([('Payment Number', f'<span class="mono">{pay[0]}</span>'), ('Mode', pay[3]), ('Bank Reference', '<span class="mono">SB26102100417</span>'), ('Paid From', 'Sahyadri Bank, Bhiwandi Branch'), ('Paid To', 'Crestline Laminates'), ('Recorded By', 'Suresh Iyer'), ('Status', chip('Confirmed', 'ok'))]))}
      <section class="card flush"><header><h2>Receipt</h2></header><div class="body">{table([('Document',''), ('Type',''), ('','')], [f'<tr><td><b>Payment Receipt</b></td><td><span class="tag">PDF</span></td><td><div class="row-actions">{dl_btn("Download receipt")}</div></td></tr>'])}</div></section>
    </div>
  </div>
'''
page('primary', 'payment-details', 'PRI-BIL-04', 'Primary Customer — Owner — Payment Details (PRI-BIL-04)', body)

# ---------- Schemes and Incentives ----------
SCH = [  # number, name, type, start, end, status, done, goal, reward text
 ('SCH-2026-04', 'Festive Volume Rebate', 'Volume Rebate', '01/10/2026', '30/11/2026', 'Active', 2750, 2500, '2% rebate'),
 ('SCH-2026-05', 'Marble Finish Launch Incentive', 'Product Incentive', '01/09/2026', '31/12/2026', 'Active', 180, 300, f'{M(4500)} earned'),
 ('SCH-2026-06', 'Winter Season Volume Bonus', 'Volume Bonus', '01/12/2026', '31/01/2027', 'Upcoming', 0, 3500, '3% bonus'),
 ('SCH-2026-02', 'Monsoon Fast Mover Bonus', 'Product Incentive', '01/07/2026', '30/09/2026', 'Completed', 2550, 2400, f'{M(38250)} credited'),
 ('SCH-2026-01', 'Summer Stock Incentive', 'Volume Incentive', '01/04/2026', '30/06/2026', 'Completed', 2310, 2000, f'{M(46200)} credited'),
]
assert 180 * 25 == 4500 and 2550 * 15 == 38250 and 2310 * 20 == 46200
earned = 4500 + 38250 + 46200
def prog(done, goal):
    pc = min(100, round(done / goal * 100))
    return f'<span class="inline-meter" style="justify-content:flex-start"><span class="meter {"ok" if done >= goal else ""}"><i style="width:{pc}%"></i></span><span style="white-space:nowrap"><b style="min-width:0">{N(done)}</b> of {N(goal)}</span></span>'
def sch_card(s):
    pc = round(s[6] / s[7] * 100)
    reached = f'{chip("Target Reached", "ok")} ' if s[6] >= s[7] else ''
    return f'''<section class="card"><header><h2>{s[1]}</h2><span style="margin-left:auto">{reached}{chip(s[5])}</span></header><div class="body">
      <div style="display:flex;align-items:baseline;gap:.5rem"><b style="font-size:1.5rem;letter-spacing:-.02em">{N(s[6])}</b><span>of {N(s[7])} sheets</span><b style="margin-left:auto">{pc}%</b></div>
      <span class="meter {"ok" if pc >= 90 else ""}" style="margin:.75rem 0 1.25rem"><i style="width:{min(pc, 100)}%"></i></span>
      {kv([('Scheme Number', f'<span class="mono">{s[0]}</span>'), ('Type', s[2]), ('Reward', s[8] if s[0] != "SCH-2026-04" else "2% rebate on order value"), ('Ends', s[4])])}
      <a class="btn block" data-link="PRI-SCH-02" style="margin-top:1.25rem">View Scheme</a></div></section>'''
sch_rows = [f'<tr><td>{link("PRI-SCH-02", s[1])}</td><td class="mono nowrap">{s[0]}</td><td>{s[4]}</td><td>{prog(s[6], s[7]) if s[5] != "Upcoming" else "—"}</td><td class="nowrap">{s[8]}</td><td>{chip(s[5])}</td></tr>' for s in SCH]
body = f'''  <div class="head">
    <h1>Schemes and Incentives</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Scheme Summary</button><a class="btn pri" data-link="PRI-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Active Schemes', '2')}
    {kpi('Incentives Earned This Year', M(earned))}
    {kpi('Sheets Above Festive Target', '250 <small>sheets</small>', chip('Target Reached', 'ok'))}
    {kpi('Upcoming Schemes', '1')}
  </div>
  <div class="grid g-2">{sch_card(SCH[0])}{sch_card(SCH[1])}</div>
  <section class="card flush"><header><h2>All Schemes</h2></header>
    <div class="body">{table([('Scheme',''), ('Scheme Number',''), ('Ends',''), ('Progress in Sheets',''), ('Reward',''), ('Status','')], sch_rows)}</div></section>
'''
page('primary', 'schemes-and-incentives', 'PRI-SCH-01', 'Primary Customer — Owner — Schemes and Incentives (PRI-SCH-01)', body)

# ---------- Scheme Details (SCH-2026-04) ----------
s0 = SCH[0]
q_rows = ''.join(f'<tr><td class="mono nowrap"><b>{o}</b></td><td>{dt}</td><td>{chip(st)}</td><td class="num">{N(sh)}</td></tr>' for o, dt, sh, st in FESTIVE_ORDERS)
body = f'''  <div class="head">
    <div class="title-row"><h1>{s0[1]}</h1>{chip('Active')}<span class="tag mono">{s0[0]}</span></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Terms</button><a class="btn pri" data-link="PRI-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Sheets Counted', N(2750), chip('Target Reached', 'ok'))}
    {kpi('Sheets Above Target', '250')}
    {kpi('Days Left', '35')}
    {kpi('Rebate Rate', '2%')}
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      <section class="card"><header><h2>Progress to Target</h2></header><div class="body">
        <div style="display:flex;align-items:baseline;gap:.5rem"><b style="font-size:1.75rem;letter-spacing:-.02em">2,750</b><span>of 2,500 sheets</span><b style="margin-left:auto">110%</b></div>
        <span class="meter ok" style="margin:.75rem 0 1.25rem"><i style="width:100%"></i></span>
        {kv([('Rebate on ORD-2026-10482', M(16426))])}</div></section>
      <section class="card flush"><header><h2>Qualifying Orders</h2></header><div class="body">{table([('Order Number',''), ('Order Date',''), ('Order Status',''), ('Sheets Counted','num')], [q_rows], foot='<tfoot><tr><td colspan="3">Total</td><td class="num">2,750</td></tr></tfoot>')}</div></section>
    </div>
    <div class="stack">
      {card('Scheme Terms', kv([('Scheme Type', 'Volume Rebate'), ('Rebate Rate', '2% of order value'), ('Target', '2,500 sheets'), ('Start Date', '01/10/2026'), ('End Date', '30/11/2026'), ('Eligible Products', 'All 12 products'), ('Eligible Customers', 'Primary Distributors')]))}
      <section class="card flush"><header><h2>Documents</h2></header><div class="body">{table([('Document',''), ('Type',''), ('','')], [f'<tr><td><b>Scheme Terms</b></td><td><span class="tag">PDF</span></td><td><div class="row-actions">{dl_btn("Download terms")}</div></td></tr>'])}</div></section>
    </div>
  </div>
'''
page('primary', 'scheme-details', 'PRI-SCH-02', 'Primary Customer — Owner — Scheme Details (PRI-SCH-02)', body)

# ---------- Sales Reports ----------
fin_val = {}
for s_, v in SOLD_VALUE.items(): fin_val[BY[s_][2]] = fin_val.get(BY[s_][2], 0) + v
regions = {}
for dd in DEALERS: regions[dd[3]] = regions.get(dd[3], 0) + dd[7]
reg_col = {'West Maharashtra': 'var(--accent)', 'North Maharashtra': '#0b8fa8', 'Konkan': '#e0a030', 'Vidarbha': '#7a36fb', 'Goa': '#0c9b6a'}
def change(a, b):
    if not b: return chip('New', 'blue')
    v = (a - b) / b * 100
    return f'<span class="delta {"up" if v >= 0 else "down"}"><i data-icon="trend"></i>{abs(v):.1f}%</span>'
dr = ''.join(f'<tr><td>{link("PRI-DLR-02", dd[1])}</td><td>{dd[2]}</td><td>{dd[3]}</td><td class="num">{N(DEALER_SHEETS[dd[0]])}</td><td class="num"><b>{M(dd[7])}</b></td><td class="num">{M(dd[8]) if dd[8] else "—"}</td><td>{change(dd[7], dd[8])}</td></tr>' for dd in sorted(DEALERS, key=lambda x: -x[7]))
pr = ''.join(f'<tr><td><div class="prod">{sw(s_)}<div><b>{BY[s_][1]}</b></div></div></td><td class="mono nowrap">{s_}</td><td class="num">{N(SOLD[s_])}</td><td class="num"><b>{M(SOLD_VALUE[s_])}</b></td>'
             f'<td><span class="inline-meter"><span class="meter"><i style="width:{SOLD_VALUE[s_] / max(SOLD_VALUE.values()) * 100:.0f}%"></i></span><b>{SOLD_VALUE[s_] / 3120000 * 100:.1f}%</b></span></td></tr>' for s_ in sorted(SOLD, key=lambda x: -SOLD_VALUE[x]))
body = f'''  <div class="head">
    <h1>Sales Reports</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><span class="sel"><small>Compared With</small> September 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="filters">{sel('Dealer', 'All Dealers')}{sel('Region', 'All Regions')}{sel('Finish', 'All Finishes')}</div>
  <div class="kpis">
    {kpi('Sales', ML(3120000), up('11.8%'))}
    {kpi('Sheets Sold', N(2195))}
    {kpi('Average Sale Value', M(3120000 // SALE_COUNT))}
    {kpi('Active Dealers', '8')}
  </div>
  <div class="grid g-2">
    {card('Sales by Finish', chart('bars', list(fin_val), [{'name': 'Sales', 'values': list(fin_val.values()), 'color': 'var(--accent)'}], money=True, height=260))}
    <section class="card"><header><h2>Sales by Region</h2></header><div class="body center">{chart('donut', series=[{'name': r, 'value': v, 'color': reg_col[r]} for r, v in sorted(regions.items(), key=lambda x: -x[1])], center='5', caption='regions')}</div></section>
  </div>
  <section class="card flush"><header><h2>Sales by Dealer</h2></header>
    <div class="body">{table([('Dealer',''), ('City',''), ('Region',''), ('Sheets','num'), ('Sales','num'), ('September Sales','num'), ('Change','')], [dr])}</div></section>
  <section class="card flush"><header><h2>Sales by Product</h2></header>
    <div class="body">{table([('Product',''), ('SKU',''), ('Sheets','num'), ('Sales','num'), ('Share of Sales','')], [pr])}</div></section>
'''
page('primary', 'sales-reports', 'PRI-RPT-01', 'Primary Customer — Owner — Sales Reports (PRI-RPT-01)', body)

# ---------- Inventory Reports ----------
def ageing(p):
    if p[0] == 'LM-CAL-003': return (60, 0, 155)              # batches B-2610-14 (20/10, 60), B-2608-07 (24/08, 100) and B-2606-11 (14/06, 55)
    on = p[8]; a = round(on * 0.62 / 5) * 5; b = round(on * 0.26 / 5) * 5
    return (a, b, on - a - b)
AG = {p[0]: ageing(p) for p in P}
ag_tot = [sum(AG[s][i] for s in AG) for i in range(3)]
assert sum(ag_tot) == 7415
assert all(AG[s][0] >= sum(q for o, _ in RECEIPTS for k, q in ORDER_LINES[o] if k == s) for s in AG), 'October receipts must be in the youngest band'
ir = ''.join(f'<tr><td><div class="prod">{sw(p[0])}<div><b>{p[1]}</b></div></div></td><td class="mono nowrap">{p[0]}</td><td class="num"><b>{N(p[8])}</b></td><td class="num">{N(SOLD[p[0]]) if SOLD[p[0]] else "—"}</td>'
             f'<td class="num">{N(AG[p[0]][0]) if AG[p[0]][0] else "—"}</td><td class="num">{N(AG[p[0]][1]) if AG[p[0]][1] else "—"}</td><td class="num">{N(AG[p[0]][2]) if AG[p[0]][2] else "—"}</td></tr>' for p in P)
finish = [('Matte', 2910, '#0a48fd'), ('Woodgrain', 2680, '#0b8fa8'), ('Texture', 640, '#7a36fb'), ('Gloss', 465, '#e0a030'), ('Suede', 410, '#0c9b6a'), ('High Gloss', 215, '#d43a2f'), ('Metallic', 95, '#8b93a3')]
body = f'''  <div class="head">
    <h1>Inventory Reports</h1>
    <div class="acts"><span class="sel"><small>Warehouse</small> All Warehouses <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('Stock Value', ML(7842000))}
    {kpi('Sheets on Hand', '7,415')}
    {kpi('Sheets Sold This Month', N(2195))}
    {kpi('Sheets Over 60 Days', N(ag_tot[2]), chip(f'{ag_tot[2] / 7415 * 100:.0f}% of Stock', 'warn'))}
  </div>
  <div class="grid g-2">
    <section class="card"><header><h2>Stock by Finish</h2></header><div class="body center">{chart('donut', series=[{'name': n, 'value': v, 'color': c} for n, v, c in finish], center='7,415', caption='sheets')}</div></section>
    {card('Stock Ageing', chart('bars', ['Up to 30 days', '31 to 60 days', 'Over 60 days'], [{'name': 'Sheets on hand', 'values': ag_tot, 'color': 'var(--accent)'}], height=260))}
  </div>
  <section class="card flush"><header><h2>Stock by Product</h2></header>
    <div class="body">{table([('Product',''), ('SKU',''), ('On Hand','num'), ('Sold This Month','num'), ('Up to 30 Days','num'), ('31 to 60 Days','num'), ('Over 60 Days','num')], [ir],
      foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">7,415</td><td class="num">{N(2195)}</td><td class="num">{N(ag_tot[0])}</td><td class="num">{N(ag_tot[1])}</td><td class="num">{N(ag_tot[2])}</td></tr></tfoot>')}</div></section>
'''
page('primary', 'inventory-reports', 'PRI-RPT-02', 'Primary Customer — Owner — Inventory Reports (PRI-RPT-02)', body)
