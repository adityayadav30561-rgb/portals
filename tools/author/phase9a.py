"""Phase 9, part A: Tertiary Customer Retailer Owner: Record Retail Sale, Retail Sales History, Retail Sale Details (shared with the Sales Executive via ?role=SLS),
Invoices Overview, Invoice Details, Payments Overview, Payment Details, Schemes and Offers, Scheme Details, Sales Reports, Inventory Reports.
Retailer Charlie, Camp, Pune; supplier Dealer Bravo. Design rule: no text under page titles, no captions beside card titles, no helper sentences.
Data: docs/DATA.md "Phase 8 data" and "Phase 9 data"."""
from data import *

SQ = chr(0x2212)
fin_col = {'Matte': '#0a48fd', 'Woodgrain': '#0b8fa8', 'Texture': '#7a36fb', 'Gloss': '#e0a030', 'Suede': '#0c9b6a', 'High Gloss': '#d43a2f', 'Metallic': '#8b93a3'}
def b_status(i): return chip('Paid') if i[3] == i[4] else chip('Unpaid')
def change(a, b):
    v = (a - b) / b * 100
    return f'<span class="delta {"up" if v >= 0 else "down"}"><i data-icon="trend"></i>{abs(v):.1f}%</span>'
PAYMODES = ['Cash', 'Card', 'Bank Transfer', 'Cheque']
def mode_chip(m): return chip(m, 'plain')

# ---------- Record Retail Sale (shared with the Sales Executive) ----------
ENTRY = {'LM-ARC-002': 3, 'LM-WNT-001': 1, 'LM-TEK-006': 3}                                    # 12,838: not equal to any figure of today's sales
e_sub = sum(q * crp(s) for s, q in ENTRY.items()); e_gst = round(e_sub * 0.09); e_total = e_sub + 2 * e_gst
assert all(q <= CSTOCK[s]['available'] for s, q in ENTRY.items())
lines = ''
for p in P:
    s = p[0]; q = ENTRY.get(s, 0)
    lines += (f'<tr><td><div class="prod">{sw(s)}<div><b>{p[1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num">{N(CSTOCK[s]["available"])}</td>'
              f'<td class="num">{M(crp(s))}</td><td>{qty(q)}</td><td class="num"><b>{M(q * crp(s)) if q else "—"}</b></td></tr>\n')
body = f'''  <div class="head">
    <h1>Record Retail Sale</h1>
    <div class="acts"><a class="btn" data-link="TER-RTS-02">Cancel</a><button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Record Sale</button></div>
  </div>
  <div class="grid g-main-side" style="--side:17rem">
    <div class="stack">
      {form('Sale Details', fld('Customer Name', 'cn', 'Rakesh Bhalerao'), fld('Mobile Number', 'mb', '+91 98900 49991'), fld('Sale Date', 'sd', '26/10/2026'),
            fld('Payment Mode', 'pm', 'Card', 'select', PAYMODES))}
      <section class="card flush"><header><h2>Products</h2><label class="finder" style="margin-left:auto;min-width:18rem"><i data-icon="search"></i><input type="search" placeholder="Search by name or SKU" aria-label="Search products"></label></header>
        <div class="body">{table([('Product', ''), ('SKU', ''), ('Available', 'num'), ('Price per Sheet', 'num'), ('Sheets', ''), ('Amount', 'num')], [lines], 'stack-sm')}</div></section>
    </div>
    <div class="stack">
      {card('Sale Summary', kv([('Sheets', str(sum(ENTRY.values()))), ('Subtotal', M(e_sub)), ('Central GST 9%', M(e_gst)), ('State GST 9%', M(e_gst))]) + kv([('Total', M(e_total))], 'total'))}
      {card('Payment', kv([('Payment Mode', 'Card'), ('Amount to Receive', f'<b>{M(e_total)}</b>')]))}
    </div>
  </div>
'''
page('tertiary', 'record-retail-sale', 'TER-RTS-01', 'Tertiary Customer — Retailer Owner — Record Retail Sale (TER-RTS-01)', body)

# ---------- Retail Sales History (shared with the Sales Executive) ----------
def mcnt(m): return CMODE_SALES[m][0]
hist = ''.join(f'<tr><td class="mono nowrap"><a data-link="TER-RTS-03"><b>{s["number"]}</b></a></td><td>{s["date"]}</td><td>{s["customer"]}</td><td class="num">{N(s["sheets"])}</td><td class="num"><b>{M(s["total"])}</b></td>'
               f'<td>{mode_chip(s["pay"])}</td><td><div class="row-actions">{dl_btn("Download sale invoice")}</div></td></tr>\n' for s in CSALES[:12])
body = f'''  <div class="head">
    <h1>Retail Sales History</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Sales</button><a class="btn pri" data-link="TER-RTS-01"><i data-icon="plus"></i>Record Retail Sale</a></div>
  </div>
  <div class="kpis">
    {kpi('Sales This Month', ML(CRETAIL_OCT), up(pct(CRETAIL_OCT, CHR_RETAIL_SEPT)))}
    {kpi('Sales Recorded', str(len(CSALES)))}
    {kpi('Sheets Sold', N(163))}
    {kpi('Average Sale Value', M(round(CRETAIL_OCT / len(CSALES))))}
  </div>
  <section class="card flush">
    {tabs([('All Sales', len(CSALES), True)] + [(m, mcnt(m), False) for m in PAYMODES])}
    {filters('Search by sale number or customer', 'Search sales', ('Date Range', 'October 2026'), ('Payment Mode', 'All'))}
    <div class="body">{table([('Sale Number', ''), ('Date', ''), ('Customer', ''), ('Sheets', 'num'), ('Value', 'num'), ('Payment Mode', ''), ('', '')], [hist], 'wrap')}
      {pager(f'Showing 1 to 12 of {len(CSALES)} sales', 4)}</div>
  </section>
'''
page('tertiary', 'retail-sales-history', 'TER-RTS-02', 'Tertiary Customer — Retailer Owner — Retail Sales History (TER-RTS-02)', body)

# ---------- Retail Sale Details (RSL-2026-0395) ----------
sale = next(s for s in CSALES if s['number'] == 'RSL-2026-0395')
assert sale['sub'] == sum(q * crp(k) for k, q in sale['lines']) and sale['total'] == 17180 and sale['date'] == '24/10/2026'
lrows = ''.join(f'<tr><td><div class="prod">{sw(k)}<div><b>{BY[k][1]}</b></div></div></td><td class="mono nowrap">{k}</td><td class="num">{N(q)}</td><td class="num">{M(crp(k))}</td><td class="num"><b>{M(q * crp(k))}</b></td></tr>' for k, q in sale['lines'])
body = f'''  <div class="head">
    <div class="title-row"><h1>{sale["number"]}</h1>{chip("Paid")}{mode_chip(sale["pay"])}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="print"></i>Print Sale Invoice</button><button class="btn" type="button"><i data-icon="download"></i>Download Sale Invoice</button></div>
  </div>
  <section class="card pad"><div class="stats" style="--cols:repeat(4,minmax(0,1fr))"><div><span>Sale Date</span><b>{sale["date"]} {sale["time"]}</b></div><div><span>Customer</span><b>{sale["customer"]}</b></div><div><span>Sheets</span><b>{sale["sheets"]}</b></div><div><span>Total</span><b>{M(sale["total"])}</b></div></div></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      <section class="card flush"><header><h2>Items</h2></header>
        <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Price per Sheet', 'num'), ('Amount', 'num')], [lrows], 'wrap', foot=f'<tfoot><tr><td colspan="4">Subtotal</td><td class="num">{M(sale["sub"])}</td></tr></tfoot>')}
          <div style="padding:1rem 1.125rem"><dl class="kv" style="max-width:22rem;margin-left:auto"><dt>Central GST 9%</dt><dd>{M(sale["gst"])}</dd><dt>State GST 9%</dt><dd>{M(sale["gst"])}</dd></dl>
          <dl class="kv total" style="max-width:22rem;margin-left:auto"><dt>Total</dt><dd>{M(sale["total"])}</dd></dl></div></div></section>
      <section class="card flush"><header><h2>Sale Activity</h2></header><div class="body">{table([('Date', ''), ('Event', ''), ('By', '')], [
        f'<tr><td class="nowrap">{sale["date"]} {sale["time"]}</td><td><b>Payment received</b></td><td>{sale["by"]}</td></tr>',
        f'<tr><td class="nowrap">{sale["date"]} {sale["time"]}</td><td><b>Sale recorded</b></td><td>{sale["by"]}</td></tr>'])}</div></section>
    </div>
    <div class="stack">
      {card('Customer', kv([('Name', sale['customer']), ('Mobile Number', f'<span style="white-space:nowrap">{sale["phone"]}</span>')]))}
      {card('Payment', kv([('Payment Mode', sale['pay']), ('Amount Received', f'<b>{M(sale["total"])}</b>'), ('Status', chip('Paid')), ('Recorded By', sale['by'])]))}
      {card('Sale Information', kv([('Sale Number', f'<span class="mono">{sale["number"]}</span>'), ('Store', 'Retailer Charlie, Camp'), ('Stock Taken From', 'Shop, Camp')]))}
    </div>
  </div>
'''
page('tertiary', 'retail-sale-details', 'TER-RTS-03', 'Tertiary Customer — Retailer Owner — Retail Sale Details (TER-RTS-03)', body)

# ---------- Invoices Overview ----------
rows = ''.join(f'<tr><td>{link("TER-BIL-02", i[0])}</td><td>{i[1]}</td><td>{i[2]}</td><td class="num">{N(i[5])}</td><td class="num">{M(i[3])}</td><td class="num"><b>{M(i[3] - i[4]) if i[3] > i[4] else "—"}</b></td><td>{b_status(i)}</td></tr>' for i in CINV)
body = f'''  <div class="head">
    <h1>Invoices Overview</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Invoices</button></div>
  </div>
  <div class="kpis">
    {kpi('Outstanding Balance', ML(CHR_OWES), chip(f'{CHR_USED}% of Credit Limit', 'ok'))}
    {kpi('Invoiced This Month', ML(264000), chip('5 invoices', 'plain'))}
    {kpi('Paid This Month', ML(CPAID_OCT), chip('5 payments', 'plain'))}
    {kpi('Overdue', M(0), chip('None', 'ok'))}
  </div>
  <section class="card flush">
    {tabs([('All Invoices', C_INV_COUNT, True), ('Open Invoices', len(COPEN), False), ('Overdue', 0, False), ('Paid', C_PAY_COUNT, False)])}
    {filters('Search by invoice number', 'Search invoices', ('Date Range', 'Last 90 days'), ('Status', 'All'))}
    <div class="body">{table([('Invoice Number', ''), ('Issue Date', ''), ('Due Date', ''), ('Sheets', 'num'), ('Invoice Amount', 'num'), ('Balance Due', 'num'), ('Status', '')], [rows], 'wrap')}
      {pager(f'Showing 1 to {len(CINV)} of {C_INV_COUNT} invoices', 25)}</div>
  </section>
'''
page('tertiary', 'invoices-overview', 'TER-BIL-01', 'Tertiary Customer — Retailer Owner — Invoices Overview (TER-BIL-01)', body)

# ---------- Invoice Details (TSL-2026-0412) ----------
inv = CINV_BY['TSL-2026-0412']; o = O12
lrows = ''.join(f'<tr><td><div class="prod">{sw(k)}<div><b>{BY[k][1]}</b></div></div></td><td class="mono nowrap">{k}</td><td class="num">{N(q)}</td><td class="num"><b>{M(O12_AMT[k])}</b></td></tr>' for k, q in o['lines'])
due_in = (pd(inv[2]) - TODAY).days
body = f'''  <div class="head">
    <div class="title-row"><h1>{inv[0]}</h1>{chip('Unpaid')}{chip(f'Due in {due_in} days', 'blue')}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="print"></i>Print Invoice</button><button class="btn" type="button"><i data-icon="download"></i>Download Invoice</button><a class="btn pri" data-link="TER-SUP-02"><i data-icon="help"></i>Raise Support Ticket</a></div>
  </div>
  <section class="card pad"><div class="stats" style="--cols:repeat(5,minmax(0,1fr))"><div><span>Issue Date</span><b>{inv[1]}</b></div><div><span>Due Date</span><b>{inv[2]}</b></div><div><span>Invoice Amount</span><b>{M(inv[3])}</b></div><div><span>Amount Paid</span><b>{M(0)}</b></div><div><span>Balance Due</span><b>{M(inv[3])}</b></div></div></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      <section class="card flush"><header><h2>Items</h2></header>
        <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Amount', 'num')], [lrows], foot=f'<tfoot><tr><td colspan="3">Taxable Amount</td><td class="num">{M(O12_TAX)}</td></tr></tfoot>')}
          <div style="padding:1rem 1.125rem"><dl class="kv" style="max-width:22rem;margin-left:auto"><dt>Central GST 9%</dt><dd>{M(O12_GST)}</dd><dt>State GST 9%</dt><dd>{M(O12_GST)}</dd></dl>
          <dl class="kv total" style="max-width:22rem;margin-left:auto"><dt>Total</dt><dd>{M(inv[3])}</dd></dl></div></div></section>
      <section class="card flush"><header><h2>Invoice Activity</h2></header><div class="body">{table([('Date', ''), ('Event', ''), ('By', '')], [
        '<tr><td class="nowrap">26/10/2026 09:45</td><td><b>Invoice viewed</b></td><td>Imran Sheikh</td></tr>',
        '<tr><td class="nowrap">25/10/2026 17:21</td><td><b>Invoice sent by email</b></td><td>Dealer Bravo</td></tr>',
        '<tr><td class="nowrap">25/10/2026 17:20</td><td><b>Invoice issued</b></td><td>Dealer Bravo</td></tr>'])}</div></section>
    </div>
    <div class="stack">
      {card('Invoice Information', kv([('Invoice Number', f'<span class="mono">{inv[0]}</span>'), ('Order Number', link('TER-ORD-02', inv[0], False)), ('Delivery Number', f'<span class="mono">{o["delivery"]}</span>'), ('Payment Terms', '15 days'), ('Status', chip('Unpaid'))]))}
      {card('Billed To', kv([('Customer', 'Charlie Laminates Private Limited'), ('GST Number', '<span style="white-space:nowrap">27AAJCC4410E1ZK</span>'), ('Address', 'Shop 12, MG Road, Camp, Pune, Postal Code 411001')]))}
      {card('Issued By', kv([('Company', 'Bravo Laminate Traders'), ('GST Number', '<span style="white-space:nowrap">27AAKFB3318D1ZP</span>'), ('Godown', 'Hadapsar Godown, Pune')]))}
    </div>
  </div>
'''
page('tertiary', 'invoice-details', 'TER-BIL-02', 'Tertiary Customer — Retailer Owner — Invoice Details (TER-BIL-02)', body)

# ---------- Payments Overview ----------
pay_rows = ''.join(f'<tr><td class="mono nowrap"><b>{link("TER-BIL-05", p[0], False)}</b></td><td>{p[1]}</td><td>{p[3]}</td><td class="mono nowrap">{p[4]}</td><td class="num"><b>{M(p[2])}</b></td><td>{chip("Confirmed", "ok")}</td><td><div class="row-actions"><a class="btn sm" data-link="TER-BIL-05">View</a></div></td></tr>' for p in CPAY_L)
mode_col = {'Bank Transfer': 'var(--accent)', 'Net Banking': '#0b8fa8', 'Cheque': '#e0a030'}
body = f'''  <div class="head">
    <h1>Payments Overview</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Payments</button></div>
  </div>
  <div class="kpis">
    {kpi('Paid This Month', ML(CPAID_OCT), chip('5 payments', 'plain'))}
    {kpi('Largest Payment', ML(max(p[2] for p in CPAY_OCT)))}
    {kpi('Average Payment', ML(round(CPAID_OCT / 5)))}
    {kpi('Outstanding Balance', ML(CHR_OWES))}
  </div>
  <div class="grid g-chart">
    {card('Payments by Month', chart('bars', MONTHS, [{'name': 'Payments to Dealer Bravo', 'values': CPAID_MONTH, 'color': 'var(--ok)'}], money=True, height=280))}
    <section class="card"><header><h2>Payments by Mode</h2></header><div class="body center">{chart('donut', series=[{'name': m, 'value': v, 'color': mode_col[m]} for m, v in sorted(CMODE_OCT.items(), key=lambda x: -x[1])], center='5', caption='payments')}</div></section>
  </div>
  <section class="card flush">
    {filters('Search by payment or invoice number', 'Search payments', ('Date Range', 'Last 90 days'), ('Mode', 'All'))}
    <div class="body">{table([('Payment Number', ''), ('Date', ''), ('Mode', ''), ('Invoice Number', ''), ('Amount', 'num'), ('Status', ''), ('', '')], [pay_rows], 'wrap')}
      {pager(f'Showing 1 to 10 of {C_PAY_COUNT} payments', 25)}</div>
  </section>
'''
page('tertiary', 'payments-overview', 'TER-BIL-03', 'Tertiary Customer — Retailer Owner — Payments Overview (TER-BIL-03)', body)

# ---------- Payment Details (PAY-2026-B0388) ----------
pay = CPAY_L[0]; pinv = CINV_BY[pay[4]]
assert pay[0] == 'PAY-2026-B0388' and pinv[3] == pay[2]
body = f'''  <div class="head">
    <div class="title-row"><h1>{pay[0]}</h1>{chip('Confirmed', 'ok')}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Receipt</button><a class="btn pri" data-link="TER-BIL-02"><i data-icon="receipt"></i>View Invoice</a></div>
  </div>
  <section class="card pad"><div class="stats" style="--cols:repeat(4,minmax(0,1fr))"><div><span>Amount</span><b>{M(pay[2])}</b></div><div><span>Payment Date</span><b>{pay[1]}</b></div><div><span>Mode</span><b>{pay[3]}</b></div><div><span>Bank Reference</span><b class="mono">DM26102200211</b></div></div></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      <section class="card flush"><header><h2>Invoices Settled</h2></header><div class="body">{table([('Invoice Number', ''), ('Invoice Amount', 'num'), ('This Payment', 'num'), ('Balance After', 'num'), ('Status', '')],
        [f'<tr><td>{link("TER-BIL-02", pinv[0])}</td><td class="num">{M(pinv[3])}</td><td class="num"><b>{M(pay[2])}</b></td><td class="num">{M(pinv[3] - pay[2])}</td><td>{chip("Paid")}</td></tr>'], 'wrap')}</div></section>
      <section class="card"><header><h2>Payment Progress</h2></header><div class="body"><ol class="track">
        <li class="done"><i></i><b>Recorded</b><span>22/10/2026 11:15</span></li><li class="done"><i></i><b>Received by Dealer Bravo</b><span>22/10/2026 15:40</span></li><li class="done"><i></i><b>Confirmed</b><span>23/10/2026 10:05</span></li></ol></div></section>
    </div>
    <div class="stack">
      {card('Payment Information', kv([('Payment Number', f'<span class="mono">{pay[0]}</span>'), ('Mode', pay[3]), ('Bank Reference', '<span class="mono">DM26102200211</span>'), ('Paid From', 'Deccan Merchants Bank, Camp Branch'), ('Paid To', 'Dealer Bravo'), ('Recorded By', 'Imran Sheikh'), ('Status', chip('Confirmed', 'ok'))]))}
      <section class="card flush"><header><h2>Receipt</h2></header><div class="body">{table([('Document', ''), ('Type', ''), ('', '')], [f'<tr><td><b>Payment Receipt</b></td><td><span class="tag">PDF</span></td><td><div class="row-actions">{dl_btn("Download receipt")}</div></td></tr>'])}</div></section>
    </div>
  </div>
'''
page('tertiary', 'payment-details', 'TER-BIL-05', 'Tertiary Customer — Retailer Owner — Payment Details (TER-BIL-05)', body)

# ---------- Schemes and Offers ----------
def prog(done, goal):
    pc = min(100, round(done / goal * 100))
    return f'<span class="inline-meter" style="justify-content:flex-start"><span class="meter {"ok" if done >= goal else ""}"><i style="width:{pc}%"></i></span><span style="white-space:nowrap"><b style="min-width:0">{N(done)}</b> of {N(goal)}</span></span>'
def off_card(s):
    pc = round(s[6] / s[7] * 100)
    return f'''<section class="card"><header><h2>{s[1]}</h2><span style="margin-left:auto">{chip(s[5])}</span></header><div class="body">
      <div style="display:flex;align-items:baseline;gap:.5rem"><b style="font-size:1.5rem;letter-spacing:-.02em">{N(s[6])}</b><span>of {N(s[7])} sheets</span><b style="margin-left:auto">{pc}%</b></div>
      <span class="meter {"ok" if pc >= 90 else ""}" style="margin:.75rem 0 1.25rem"><i style="width:{min(pc, 100)}%"></i></span>
      {kv([('Offer Number', f'<span class="mono">{s[0]}</span>'), ('Type', s[2]), ('Reward', s[8]), ('Ends', s[4])])}
      <a class="btn block" data-link="TER-SCH-02" style="margin-top:1.25rem">View Offer</a></div></section>'''
off_rows = [f'<tr><td>{link("TER-SCH-02", s[1])}</td><td class="mono nowrap">{s[0]}</td><td>{s[4]}</td><td>{prog(s[6], s[7]) if s[5] != "Upcoming" else "—"}</td><td class="nowrap">{s[8]}</td><td>{chip(s[5])}</td></tr>' for s in COFFERS_ALL]
fest = COFFERS[0]
body = f'''  <div class="head">
    <h1>Schemes and Offers</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Offer Summary</button><a class="btn pri" data-link="TER-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Active Offers', '2')}
    {kpi('Incentives Earned This Year', M(C_INCENTIVES))}
    {kpi('Sheets to Festive Target', f'{fest[7] - fest[6]} <small>sheets</small>', chip('35 days left', 'warn'))}
    {kpi('Upcoming Offers', '1')}
  </div>
  <div class="grid g-2">{off_card(COFFERS[0])}{off_card(COFFERS[1])}</div>
  <section class="card flush"><header><h2>All Offers</h2></header>
    <div class="body">{table([('Offer', ''), ('Offer Number', ''), ('Ends', ''), ('Progress in Sheets', ''), ('Reward', ''), ('Status', '')], off_rows, 'wrap')}</div></section>
'''
page('tertiary', 'schemes-and-offers', 'TER-SCH-01', 'Tertiary Customer — Retailer Owner — Schemes and Offers (TER-SCH-01)', body)

# ---------- Scheme Details (OFR-2026-01) ----------
q_rows = ''.join(f'<tr><td><a data-link="TER-ORD-02"><b>{o_}</b></a></td><td>{d}</td><td>{chip(st)}</td><td class="num">{N(sh)}</td></tr>' for o_, d, sh, st in C_FESTIVE_ORDERS)
body = f'''  <div class="head">
    <div class="title-row"><h1>{fest[1]}</h1>{chip('Active')}<span class="tag mono">{fest[0]}</span></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Terms</button><a class="btn pri" data-link="TER-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Sheets Counted', N(fest[6]), chip(f'{fest[6] / fest[7] * 100:.0f}% of Target', 'blue'))}
    {kpi('Sheets Remaining', str(fest[7] - fest[6]))}
    {kpi('Days Left', '35')}
    {kpi('Rebate Rate', '1.5%')}
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      <section class="card"><header><h2>Progress to Target</h2></header><div class="body">
        <div style="display:flex;align-items:baseline;gap:.5rem"><b style="font-size:1.75rem;letter-spacing:-.02em">{N(fest[6])}</b><span>of {N(fest[7])} sheets</span><b style="margin-left:auto">{fest[6] / fest[7] * 100:.0f}%</b></div>
        <span class="meter" style="margin:.75rem 0 1.25rem"><i style="width:{fest[6] / fest[7] * 100:.0f}%"></i></span>
        {kv([('Rebate Earned So Far', M(0))])}</div></section>
      <section class="card flush"><header><h2>Qualifying Orders</h2></header><div class="body">{table([('Order Number', ''), ('Order Date', ''), ('Order Status', ''), ('Sheets Counted', 'num')], [q_rows], 'wrap', foot=f'<tfoot><tr><td colspan="3">Total</td><td class="num">{N(fest[6])}</td></tr></tfoot>')}</div></section>
    </div>
    <div class="stack">
      {card('Offer Terms', kv([('Offer Type', 'Volume Rebate'), ('Rebate Rate', '1.5% of order value'), ('Target', '250 sheets'), ('Start Date', '01/10/2026'), ('End Date', '30/11/2026'), ('Eligible Products', 'All 12 products'), ('Eligible Customers', 'Retailers of Dealer Bravo')]))}
      <section class="card flush"><header><h2>Documents</h2></header><div class="body">{table([('Document', ''), ('Type', ''), ('', '')], [f'<tr><td><b>Offer Terms</b></td><td><span class="tag">PDF</span></td><td><div class="row-actions">{dl_btn("Download terms")}</div></td></tr>'])}</div></section>
    </div>
  </div>
'''
page('tertiary', 'scheme-details', 'TER-SCH-02', 'Tertiary Customer — Retailer Owner — Scheme Details (TER-SCH-02)', body)

# ---------- Sales Reports ----------
fin_val = dict(sorted(CFIN_SUB.items(), key=lambda x: -x[1]))
pr = ''.join(f'<tr><td><div class="prod">{sw(s_)}<div><b>{BY[s_][1]}</b></div></div></td><td class="mono nowrap">{s_}</td><td class="num">{N(CSOLD[s_])}</td><td class="num"><b>{M(CSOLD_SUB[s_])}</b></td>'
             f'<td><span class="inline-meter"><span class="meter"><i style="width:{CSOLD_SUB[s_] / max(CSOLD_SUB.values()) * 100:.0f}%"></i></span><b>{CSOLD_SUB[s_] / CSUB_TOTAL * 100:.1f}%</b></span></td></tr>' for s_ in sorted(CSOLD_SUB, key=lambda x: -CSOLD_SUB[x]))
body = f'''  <div class="head">
    <h1>Sales Reports</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><span class="sel"><small>Compared With</small> September 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="filters">{sel('Product', 'All Products')}{sel('Finish', 'All Finishes')}{sel('Payment Mode', 'All Modes')}</div>
  <div class="kpis">
    {kpi('Sales Including GST', ML(CRETAIL_OCT), up(pct(CRETAIL_OCT, CHR_RETAIL_SEPT)))}
    {kpi('Sales Before GST', ML(CSUB_TOTAL))}
    {kpi('Sheets Sold', N(163))}
    {kpi('Average Sale Value', M(round(CRETAIL_OCT / len(CSALES))))}
  </div>
  <div class="grid g-2">
    {card('Sales by Week, Including GST', chart('bars', [w[0] for w in WEEKS], [{'name': 'Sales', 'values': CWEEK_VALUE, 'color': 'var(--accent)'}], money=True, height=260))}
    <section class="card"><header><h2>Sales by Payment Mode</h2></header><div class="body center">{chart('donut', series=sorted([{'name': m, 'value': CMODE_SALES[m][1], 'color': c} for m, c in zip(['Card', 'Cash', 'Bank Transfer', 'Cheque'], ['var(--accent)', '#0b8fa8', '#7a36fb', '#e0a030'])], key=lambda x: -x['value']), center=str(len(CSALES)), caption='sales')}</div></section>
  </div>
  {card('Sales by Finish, Before GST', chart('bars', list(fin_val), [{'name': 'Sales before GST', 'values': list(fin_val.values()), 'color': 'var(--accent)'}], money=True, height=260))}
  <section class="card flush"><header><h2>Sales by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Sales Before GST', 'num'), ('Share of Sales', '')], [pr], 'wrap',
      foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(163)}</td><td class="num">{M(CSUB_TOTAL)}</td><td></td></tr></tfoot>')}</div></section>
'''
page('tertiary', 'sales-reports', 'TER-RPT-01', 'Tertiary Customer — Retailer Owner — Sales Reports (TER-RPT-01)', body)

# ---------- Inventory Reports ----------
ag_tot = [sum(CAGE[s][i] for s in CAGE) for i in range(3)]
assert sum(ag_tot) == 216
ir = ''.join(f'<tr><td><div class="prod">{sw(p[0])}<div><b>{p[1]}</b></div></div></td><td class="mono nowrap">{p[0]}</td><td class="num"><b>{N(CSTOCK[p[0]]["on_hand"])}</b></td><td class="num">{N(CSOLD[p[0]]) if CSOLD[p[0]] else "—"}</td>'
             f'<td class="num">{N(CAGE[p[0]][0]) if CAGE[p[0]][0] else "—"}</td><td class="num">{N(CAGE[p[0]][1]) if CAGE[p[0]][1] else "—"}</td><td class="num">{N(CAGE[p[0]][2]) if CAGE[p[0]][2] else "—"}</td></tr>' for p in P)
body = f'''  <div class="head">
    <h1>Inventory Reports</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('Stock Value', ML(CSTOCK_VALUE))}
    {kpi('Sheets on Hand', N(216))}
    {kpi('Sheets Sold This Month', N(163))}
    {kpi('Sheets Over 60 Days', N(ag_tot[2]), chip(f'{ag_tot[2] / 216 * 100:.0f}% of Stock', 'warn'))}
  </div>
  <div class="grid g-2">
    <section class="card"><header><h2>Stock by Finish</h2></header><div class="body center">{chart('donut', series=[{'name': f, 'value': v, 'color': fin_col[f]} for f, v in sorted(CFINISH.items(), key=lambda x: -x[1])], center=N(216), caption='sheets')}</div></section>
    {card('Stock Ageing', chart('bars', ['Up to 30 days', '31 to 60 days', 'Over 60 days'], [{'name': 'Sheets on hand', 'values': ag_tot, 'color': 'var(--accent)'}], height=260))}
  </div>
  <section class="card flush"><header><h2>Stock by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('On Hand', 'num'), ('Sold This Month', 'num'), ('Up to 30 Days', 'num'), ('31 to 60 Days', 'num'), ('Over 60 Days', 'num')], [ir], 'wrap',
      foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(216)}</td><td class="num">{N(163)}</td><td class="num">{N(ag_tot[0])}</td><td class="num">{N(ag_tot[1])}</td><td class="num">{N(ag_tot[2])}</td></tr></tfoot>')}</div></section>
'''
page('tertiary', 'inventory-reports', 'TER-RPT-02', 'Tertiary Customer — Retailer Owner — Inventory Reports (TER-RPT-02)', body)
