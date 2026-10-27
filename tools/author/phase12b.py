"""Phase 12, part B: Company Administration, Super Admin: Invoice Management, Invoice Details, Scheme Management, Scheme Details, Create Scheme,
Support Ticket Management and Support Ticket Details (the last two shared with the Operations Manager). Crestline's view of the documents Distributor Alpha sees.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md "Phase 12 data"."""
from data import *

# ---------- Invoice Management ----------
rows = [f'<tr><td>{link("CMP-BIL-02", i[0])}</td><td class="nowrap">{link("CMP-ORD-02", i[1], False)}</td><td>Distributor Alpha</td><td>{i[2]}</td><td>{i[3]}</td><td class="num">{M(i[4])}</td><td class="num"><b>{M(i[4] - i[5])}</b></td><td>{inv_chip(i)}</td></tr>' for i in OPEN_INV]
foot = f'<tfoot><tr><td colspan="5">Total</td><td class="num">{M(sum(i[4] for i in OPEN_INV))}</td><td class="num">{M(OUTSTANDING)}</td><td></td></tr></tfoot>'
age_rows = ''.join(f'<tr><td><b>{b}</b></td><td class="num">{len(AGE[b])}</td><td class="num"><b>{M(AGE_AMT[b])}</b></td></tr>' for b in BUCKETS)
age_foot = f'<tfoot><tr><td>Total</td><td class="num">{len(OPEN_INV)}</td><td class="num">{M(OUTSTANDING)}</td></tr></tfoot>'
body = f'''  <div class="head">
    <h1>Invoice Management</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Invoices</button></div>
  </div>
  <div class="kpis">
    {kpi('Invoiced This Month', ML(INV_ISSUED_OCT), chip('4 invoices', 'plain'))}
    {kpi('Payments Received This Month', ML(sum(p[2] for p in PAID_OCT)), chip('5 payments', 'plain'))}
    {kpi('Outstanding Balance', ML(OUTSTANDING), chip('37% of Credit Limit', 'warn'))}
    {kpi('Overdue', ML(sum(i[4] - i[5] for i in OVERDUE)), '<span class="delta down">2 invoices</span>')}
  </div>
  <div class="grid g-2">
    {card('Payments Received by Month', chart('bars', MONTHS, [{'name': 'Payments from Distributor Alpha', 'values': PAID_MONTH, 'color': 'var(--ok)'}], money=True, height=260))}
    <section class="card flush"><header><h2>Outstanding by Age</h2></header><div class="body">{table([('Age', ''), ('Invoices', 'num'), ('Balance', 'num')], [age_rows], 'wrap', foot=age_foot)}</div></section>
  </div>
  <section class="card flush">
    {tabs([('Open Invoices', INV_COUNT['open'], True), ('Overdue', INV_COUNT['overdue'], False), ('Paid', INV_COUNT['paid'], False), ('All Invoices', INV_COUNT['total'], False)])}
    {filters('Search by invoice number, order number or customer', 'Search invoices', ('Date Range', 'Last 90 days'), ('Customer', 'All'), ('Status', 'All'))}
    <div class="body">{table([('Invoice Number', ''), ('Order Number', ''), ('Customer', ''), ('Issue Date', ''), ('Due Date', ''), ('Invoice Amount', 'num'), ('Balance Due', 'num'), ('Status', '')], rows, 'wrap', foot=foot)}
      {pager('Showing 1 to 5 of 5 open invoices', 1)}</div>
  </section>
'''
page('company', 'invoice-management', 'CMP-BIL-01', 'Company Administration — Super Admin — Invoice Management (CMP-BIL-01)', body)

# ---------- Invoice Details (INV-2026-03318) ----------
L = [('LM-WNT-001', 100, 1140), ('LM-ARC-002', 150, 905), ('LM-CHR-007', 60, 1055), ('LM-WNG-011', 50, 1170)]
sub = sum(q * p for _, q, p in L); total = sub + 33440 * 2 + 4500; assert (sub, total) == (371550, 442930)
inv = INVOICES[0]; assert inv[0] == 'INV-2026-03318' and inv[4] == total and ORDER_VALUE[inv[1]] == total
lines = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num">{N(q)}</td><td class="num">{M(p)}</td><td class="num"><b>{M(q * p)}</b></td></tr>' for s, q, p in L)
body = f'''  <div class="head">
    <div class="title-row"><h1>{inv[0]}</h1>{chip('Unpaid')}{chip('Due in 43 days', 'blue')}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="print"></i>Print Invoice</button><button class="btn" type="button"><i data-icon="download"></i>Download Invoice</button><button class="btn pri" type="button">Send Payment Reminder</button></div>
  </div>
  <section class="card pad"><div class="stats" style="--cols:repeat(5,minmax(0,1fr))"><div><span>Issue Date</span><b>{inv[2]}</b></div><div><span>Due Date</span><b>{inv[3]}</b></div><div><span>Invoice Amount</span><b>{M(total)}</b></div><div><span>Amount Received</span><b>{M(0)}</b></div><div><span>Balance Due</span><b>{M(total)}</b></div></div></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
    <section class="card flush"><header><h2>Items</h2></header>
      <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Price per Sheet', 'num'), ('Amount', 'num')], [lines], foot=f'<tfoot><tr><td colspan="4">Subtotal</td><td class="num">{M(sub)}</td></tr></tfoot>')}
        <div style="padding:1rem 1.125rem"><dl class="kv" style="max-width:22rem;margin-left:auto"><dt>Central GST 9%</dt><dd>{M(33440)}</dd><dt>State GST 9%</dt><dd>{M(33440)}</dd><dt>Freight</dt><dd>{M(4500)}</dd></dl>
        <dl class="kv total" style="max-width:22rem;margin-left:auto"><dt>Total</dt><dd>{M(total)}</dd></dl></div></div></section>
    <section class="card flush"><header><h2>Invoice Activity</h2></header><div class="body">{table([('Date', ''), ('Event', ''), ('By', '')], [
      '<tr><td class="nowrap">25/10/2026 10:12</td><td><b>Invoice viewed</b></td><td>Rajesh Menon</td></tr>',
      '<tr><td class="nowrap">24/10/2026 06:32</td><td><b>Invoice sent by email</b></td><td>Crestline Laminates</td></tr>',
      '<tr><td class="nowrap">24/10/2026 06:30</td><td><b>Invoice issued</b></td><td>Crestline Laminates</td></tr>'])}</div></section>
    </div>
    <div class="stack">
      {card('Invoice Information', kv([('Invoice Number', f'<span class="mono">{inv[0]}</span>'), ('Order Number', link('CMP-ORD-02', inv[1], False)), ('Dispatch Number', '<span class="mono">DSP-2026-5523</span>'), ('Payment Terms', '45 days'), ('Status', chip('Unpaid'))]))}
      {card('Billed To', kv([('Customer', link('CMP-CUS-02', 'Distributor Alpha Private Limited', False)), ('Customer Code', '<span class="mono">CUS-0018</span>'), ('GST Number', '<span style="white-space:nowrap">27AABCD4521F1Z7</span>'), ('Address', 'Plot 14, Bhiwandi Logistics Park, Thane District, Maharashtra, Postal Code 421302')]))}
      {card('Issued By', kv([('Company', 'Crestline Laminates'), ('GST Number', '<span style="white-space:nowrap">24AABCC7782M1Z4</span>'), ('Warehouse', 'Plant Warehouse, Vapi, Gujarat')]))}
    </div>
  </div>
'''
page('company', 'invoice-details', 'CMP-BIL-02', 'Company Administration — Super Admin — Invoice Details (CMP-BIL-02)', body)

# ---------- Scheme Management ----------
def prog(done, goal):
    pc = min(100, round(done / goal * 100))
    return f'<span class="inline-meter" style="justify-content:flex-start"><span class="meter {"ok" if done >= goal else ""}"><i style="width:{pc}%"></i></span><span style="white-space:nowrap"><b style="min-width:0">{N(done)}</b> of {N(goal)}</span></span>'
srows = [f'<tr><td>{link("CMP-SCH-02", s[1])}</td><td class="mono nowrap">{s[0]}</td><td>{s[2]}</td><td class="nowrap">{s[4]}</td><td>{prog(s[6], s[7]) if s[5] != "Upcoming" else "—"}</td><td>{s[8]}</td><td>{chip(s[5])}</td></tr>' for s in CSCH]
n_act = sum(1 for s in CSCH if s[5] == 'Active')
body = f'''  <div class="head">
    <h1>Scheme Management</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Schemes</button><a class="btn pri" data-link="CMP-SCH-03"><i data-icon="plus"></i>Create Scheme</a></div>
  </div>
  <div class="kpis">
    {kpi('Active Schemes', str(n_act))}
    {kpi('Credited This Year', M(SCH_CREDITED), chip('2 completed schemes', 'plain'))}
    {kpi('Accruing on Active Schemes', M(SCH_ACCRUING), chip('Target Reached', 'ok'))}
    {kpi('Upcoming Schemes', '1')}
  </div>
  {card('Sheets Against Target by Scheme', chart('bars', [s[0] for s in CSCH if s[5] != 'Upcoming'], [{'name': 'Sheets counted', 'values': [s[6] for s in CSCH if s[5] != 'Upcoming'], 'color': 'var(--accent)'}, {'name': 'Target', 'values': [s[7] for s in CSCH if s[5] != 'Upcoming'], 'color': 'var(--bad)'}], height=260))}
  <section class="card flush">
    {tabs([('All Schemes', len(CSCH), True), ('Active', n_act, False), ('Upcoming', 1, False), ('Completed', 2, False)])}
    {filters('Search by scheme name or number', 'Search schemes', ('Type', 'All'), ('Status', 'All'))}
    <div class="body">{table([('Scheme', ''), ('Scheme Number', ''), ('Type', ''), ('Ends', ''), ('Progress in Sheets', ''), ('Reward', ''), ('Status', '')], srows, 'wrap')}
      {pager(f'Showing 1 to {len(CSCH)} of {len(CSCH)} schemes', 1)}</div>
  </section>
'''
page('company', 'scheme-management', 'CMP-SCH-01', 'Company Administration — Super Admin — Scheme Management (CMP-SCH-01)', body)

# ---------- Scheme Details (SCH-2026-04) ----------
s0 = CSCH[0]
q_rows = ''.join(f'<tr><td class="mono nowrap"><b>{o}</b></td><td>{dt}</td><td>{chip(st)}</td><td class="num">{N(sh)}</td></tr>' for o, dt, sh, st in FESTIVE_ORDERS)
body = f'''  <div class="head">
    <div class="title-row"><h1>{s0[1]}</h1>{chip('Active')}<span class="tag mono">{s0[0]}</span></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Terms</button><button class="btn" type="button"><i data-icon="edit"></i>Edit Scheme</button><button class="btn danger" type="button">End Scheme</button></div>
  </div>
  <div class="kpis">
    {kpi('Sheets Counted', N(2750), chip('Target Reached', 'ok'))}
    {kpi('Customers Participating', '1')}
    {kpi('Rebate on ORD-2026-10482', M(REBATE_10482), chip('Awaiting Confirmation', 'warn'))}
    {kpi('Days Left', '35')}
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      <section class="card flush"><header><h2>Customers Participating</h2></header><div class="body">{table([('Customer', ''), ('Sheets Counted', 'num'), ('Target', 'num'), ('Progress', ''), ('Rebate', 'num')],
        [f'<tr><td>{link("CMP-CUS-02", "Distributor Alpha")}</td><td class="num"><b>2,750</b></td><td class="num">2,500</td><td>{prog(2750, 2500)}</td><td class="num"><b>{M(REBATE_10482)}</b></td></tr>'], 'wrap')}</div></section>
      <section class="card flush"><header><h2>Qualifying Orders</h2></header><div class="body">{table([('Order Number', ''), ('Order Date', ''), ('Order Status', ''), ('Sheets Counted', 'num')], [q_rows], foot='<tfoot><tr><td colspan="3">Total</td><td class="num">2,750</td></tr></tfoot>')}</div></section>
    </div>
    <div class="stack">
      {card('Scheme Terms', kv([('Scheme Type', 'Volume Rebate'), ('Rebate Rate', '2% of order value'), ('Target', '2,500 sheets'), ('Start Date', '01/10/2026'), ('End Date', '30/11/2026'), ('Eligible Products', 'All 12 products'), ('Eligible Customers', 'Primary Distributors')]))}
      <section class="card flush"><header><h2>Documents</h2></header><div class="body">{table([('Document', ''), ('Type', ''), ('', '')], [f'<tr><td><b>Scheme Terms</b></td><td><span class="tag">PDF</span></td><td><div class="row-actions">{dl_btn("Download terms")}</div></td></tr>'])}</div></section>
    </div>
  </div>
'''
page('company', 'scheme-details', 'CMP-SCH-02', 'Company Administration — Super Admin — Scheme Details (CMP-SCH-02)', body)

# ---------- Create Scheme (SCH-2026-10, unsaved) ----------
body = f'''  <div class="head">
    <h1>Create Scheme</h1>
    <div class="acts">{cancel('CMP-SCH-01')}<button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Create Scheme</button></div>
  </div>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      {form('Scheme Details', fld('Scheme Name', 'sn', 'Spring Stock Incentive', full=True), fld('Scheme Number', 'sm', 'SCH-2026-10'), fld('Scheme Type', 'st', 'Volume Incentive', 'select', ['Volume Rebate', 'Volume Incentive', 'Volume Bonus', 'Product Incentive']),
            fld('Start Date', 'sd', '01/03/2027'), fld('End Date', 'ed', '31/05/2027'))}
      {form('Target and Reward', fld('Target in Sheets', 'tg', '2,000'), fld('Reward Basis', 'rb', 'Per sheet', 'select', ['Per sheet', 'Percentage of order value']), fld('Reward Value', 'rv', '₹20'), fld('Maximum Reward in Rupees', 'mx', '₹1,00,000'))}
      {form('Eligibility', fld('Eligible Customers', 'ec', 'Primary Distributors', 'select', ['Primary Distributors']), fld('Eligible Products', 'ep', 'All 12 products', 'select', ['All 12 products', 'Selected products']),
            fld('Customers Notified by', 'nb', 'Email and Portal Notification', 'select', ['Email and Portal Notification', 'Portal Notification']))}
    </div>
    <div class="stack">
      {card('Scheme Summary', kv([('Scheme', 'Spring Stock Incentive'), ('Scheme Number', '<span class="mono">SCH-2026-10</span>'), ('Period', '01/03/2027 to 31/05/2027'), ('Target', '2,000 sheets'), ('Reward', '₹20 per sheet'), ('Customers', '1'), ('Status', chip('Draft', 'plain'))]))}
    </div>
  </div>
'''
page('company', 'create-scheme', 'CMP-SCH-03', 'Company Administration — Super Admin — Create Scheme (CMP-SCH-03)', body)

# ---------- Support Ticket Management ----------
def age(t): return (TODAY - pd(t[1])).days
trows = [f'<tr><td class="mono nowrap">{link("CMP-SUP-02", t[0])}</td><td>Distributor Alpha</td><td>{t[2]}</td><td>{chip(t[4])}</td><td class="nowrap">Meera Kapoor</td><td class="num">{age(t)}</td><td>{t[5]}</td><td>{chip(t[6])}</td></tr>' for t in CRL_TICKETS]
body = f'''  <div class="head">
    <h1>Support Ticket Management</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Tickets</button></div>
  </div>
  <div class="kpis">
    {kpi('Open Tickets', str(len(CRL_TICKETS_OPEN)))}
    {kpi('High Priority', '1', chip('TKT-2026-0731', 'bad'))}
    {kpi('Awaiting Customer Reply', '1', chip('TKT-2026-0724', 'warn'))}
    {kpi('Resolved This Month', '1')}
  </div>
  <section class="card flush">
    {tabs([('All Tickets', 6, True), ('Open', 3, False), ('Resolved', 1, False), ('Closed', 2, False)])}
    {filters('Search by ticket number, customer or subject', 'Search tickets', ('Category', 'All'), ('Priority', 'All'), ('Assigned To', 'All'))}
    <div class="body">{table([('Ticket Number', ''), ('Customer', ''), ('Subject', ''), ('Priority', ''), ('Assigned To', ''), ('Age in Days', 'num'), ('Last Updated', ''), ('Status', '')], trows, 'wrap')}
      {pager('Showing 1 to 6 of 6 tickets', 1)}</div>
  </section>
'''
page('company', 'support-ticket-management', 'CMP-SUP-01', 'Company Administration — Super Admin — Support Ticket Management (CMP-SUP-01)', body)

# ---------- Support Ticket Details (TKT-2026-0731) ----------
def msg(who, init, when, text, me=False, files=()):
    fl = f'<div class="files">{"".join(f"<span class=file><i data-icon=doc></i>{f}</span>" for f in files)}</div>' if files else ''
    return f'<div class="msg{" me" if me else ""}"><div class="av">{init}</div><div><div class="top-line"><b>{who}</b><time>{when}</time></div><div class="bubble">{text}{fl}</div></div></div>'
thread = ''.join([
    msg('Rajesh Menon, Distributor Alpha', 'RM', '24/10/2026 16:20', 'Twelve sheets of Calacatta Marble Finish Laminate arrived with cracked corners in ORD-2026-10431. Photos are attached.', False, ['damaged-corners-1.jpg', 'damaged-corners-2.jpg']),
    msg('Meera Kapoor, Crestline Customer Support', 'MK', '25/10/2026 10:05', 'Thank you, Rajesh. We have the photos and have asked the Vapi plant to check the batch. A return request is the fastest way to get a credit note.', True),
    msg('Rajesh Menon, Distributor Alpha', 'RM', '25/10/2026 11:20', 'Return request RTN-2026-0412 is raised for 12 sheets.', False, ['packing-list.pdf']),
    msg('Meera Kapoor, Crestline Customer Support', 'MK', '26/10/2026 09:40', 'The return request is under review. We will confirm the pickup date within two working days.', True),
])
body = f'''  <div class="head">
    <div class="title-row"><h1>Damaged Sheets in ORD-2026-10431</h1>{chip('In Progress')}{chip('High')}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="check"></i>Close Ticket</button></div>
  </div>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      {card('Conversation', f'<div class="thread">{thread}</div>')}
      <section class="card"><header><h2>Reply</h2></header><div class="body"><div class="reply"><textarea class="input" aria-label="Reply" placeholder="Write a reply"></textarea>
        <div class="row"><button class="btn" type="button"><i data-icon="upload"></i>Attach Files</button><button class="btn pri" type="button">Send Reply</button></div></div></div></section>
    </div>
    <div class="stack">
      {card('Ticket Information', kv([('Ticket Number', '<span class="mono">TKT-2026-0731</span>'), ('Status', chip('In Progress')), ('Priority', chip('High')), ('Category', 'Delivery'), ('Created', '24/10/2026 16:20'), ('Last Updated', '26/10/2026 09:40'), ('Assigned To', 'Meera Kapoor')]))}
      {card('Customer', kv([('Customer', link('CMP-CUS-02', 'Distributor Alpha', False)), ('Raised By', 'Rajesh Menon'), ('Account Manager', 'Vikram Chopra')]))}
      {card('Related Records', kv([('Order', link('CMP-ORD-02', 'ORD-2026-10431', False)), ('Return Request', link('CMP-OPS-06', 'RTN-2026-0412', False))]))}
    </div>
  </div>
'''
page('company', 'support-ticket-details', 'CMP-SUP-02', 'Company Administration — Super Admin — Support Ticket Details (CMP-SUP-02)', body)
