"""Phase 6, part A: Secondary Customer Owner: Tertiary Sales Overview, Tertiary Sales Entry, Tertiary Sales History (Entry and History are shared
with the Manager), Invoices Overview, Invoice Details, Payments Overview, Payment Details. Dealer Bravo, Pune; supplier Distributor Alpha.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md "Phase 5 data" and "Phase 6 data"."""
from data import *

SQ = chr(0x2212)
cp_used = round(BRV_OWES / BRV_LIMIT * 100)
def rtl_link(sid, text): return link(sid, text)
INV_BY = {i[0]: i for i in BINV}
def b_status(i):
    if i[4] == i[5]: return chip('Paid')
    return chip('Partly Paid') if i[5] else chip('Unpaid')
DISPATCH = {s['number']: s['dispatch'] for s in BRV_SALES}
fin_col = {'Matte': '#0a48fd', 'Woodgrain': '#0b8fa8', 'Texture': '#7a36fb', 'Gloss': '#e0a030', 'Suede': '#0c9b6a', 'High Gloss': '#d43a2f', 'Metallic': '#8b93a3'}

# ---------- Tertiary Sales Overview ----------
TFIN = {}
for s_, q_ in TSOLD.items(): TFIN[BY[s_][2]] = TFIN.get(BY[s_][2], 0) + q_
share_rows = ''
for r in sorted(RETAILERS, key=lambda r: -r[9][-1]):
    sh = r[9][-1] / 630000 * 100
    share_rows += (f'<tr><td class="nowrap">{link("SEC-RTL-02", r[1])} <span class="tag">{r[3]}</span></td><td class="num">{N(RTL_SHEETS[r[0]])}</td><td class="num"><b>{M(r[9][-1])}</b></td>'
                   f'<td><span class="inline-meter"><span class="meter"><i style="width:{sh / 45 * 100:.0f}%"></i></span><b>{sh:.1f}%</b></span></td></tr>')
top = sorted(TSOLD, key=lambda s: -TSOLD[s])[:5]
top_rows = ''.join(f'<li>{sw(s, "", "width:2.5rem;height:2.5rem;flex:none")}<div class="grow"><b>{BY[s][1]}</b><span class="meter" style="margin-top:.5rem"><i style="width:{TSOLD[s] / TSOLD[top[0]] * 100:.0f}%"></i></span></div><b>{N(TSOLD[s])}</b></li>' for s in top)
body = f'''  <div class="head">
    <h1>Tertiary Sales Overview</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Download Report</button><a class="btn pri" data-link="SEC-TSL-02"><i data-icon="plus"></i>Record Sale</a></div>
  </div>
  <div class="kpis">
    {kpi('Sales This Month', ML(630000), up(pct(630000, 600000)))}
    {kpi('Sheets Sold', N(370))}
    {kpi('Sales Recorded', str(len(TSALES)))}
    {kpi('Average Sale Value', M(630000 // len(TSALES)))}
  </div>
  <div class="grid g-chart">
    {card('Sales to Retailers by Month', chart('bars', MONTHS, [{'name': 'Sales to Retailers', 'values': BRV_RETAIL_MONTH, 'color': 'var(--teal)'}], money=True, height=280))}
    <section class="card"><header><h2>Sheets Sold by Finish</h2></header><div class="body center">{chart('donut', series=[{'name': f, 'value': v, 'color': fin_col[f]} for f, v in sorted(TFIN.items(), key=lambda x: -x[1])], center='370', caption='sheets')}</div></section>
  </div>
  <div class="grid g-main-side" style="--side:26rem">
    <section class="card flush"><header><h2>Sales by Retailer</h2><a class="more" data-link="SEC-RTL-01">All retailers</a></header>
      <div class="body">{table([('Retailer', ''), ('Sheets', 'num'), ('Sales', 'num'), ('Share of Sales', '')], [share_rows], foot=f'<tfoot><tr><td>Total</td><td class="num">{N(370)}</td><td class="num">{M(630000)}</td><td></td></tr></tfoot>')}</div></section>
    {card('Top Products by Sheets', f'<ul class="list">{top_rows}</ul>')}
  </div>
'''
page('secondary', 'tertiary-sales-overview', 'SEC-TSL-01', 'Secondary Customer — Owner — Tertiary Sales Overview (SEC-TSL-01)', body)

# ---------- Tertiary Sales Entry ----------
ENTRY = {'LM-WNT-001': 20, 'LM-ARC-002': 30, 'LM-CAL-003': 5, 'LM-OAK-004': 10}
e_sub = sum(q * rp(s) for s, q in ENTRY.items()); e_gst = round(e_sub * 0.09); e_total = e_sub + 2 * e_gst
assert (e_sub, e_gst, e_total) == (88800, 7992, 104784), (e_sub, e_gst, e_total)
ch = RTL['CHR']; e_after = RTL_OWES['CHR'] + e_total
assert ch[6] - e_after == 133216 and all(q <= BSTOCK[s]['available'] for s, q in ENTRY.items())
lines = ''
for p in P:
    s = p[0]; q = ENTRY.get(s, 0)
    lines += (f'<tr><td><div class="prod">{sw(s)}<div><b>{p[1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num">{N(BSTOCK[s]["available"])}</td>'
              f'<td class="num">{M(rp(s))}</td><td>{qty(q)}</td><td class="num"><b>{M(q * rp(s)) if q else "—"}</b></td></tr>\n')
used = round(e_after / ch[6] * 100)
body = f'''  <div class="head">
    <h1>Tertiary Sales Entry</h1>
    <div class="acts"><a class="btn" data-link="SEC-TSL-03">Cancel</a><button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Record Sale</button></div>
  </div>
  <div class="grid g-main-side" style="--side:17rem">
    <div class="stack">
      {form('Sale Details', fld('Retailer', 'rt', 'Retailer Charlie, Pune', 'select', [f'{r[1]}, {r[3]}' for r in RETAILERS]), fld('Sale Date', 'sd', '26/10/2026'),
            fld('Dispatch From', 'wh', 'Hadapsar Godown', 'select', ['Hadapsar Godown', 'Shop, Hadapsar']), fld('Payment Terms', 'pt', '15 days', 'select', ['Immediate', '15 days', '30 days']))}
      <section class="card flush"><header><h2>Products</h2><label class="finder" style="margin-left:auto;min-width:18rem"><i data-icon="search"></i><input type="search" placeholder="Search by name or SKU" aria-label="Search products"></label></header>
        <div class="body">{table([('Product', ''), ('SKU', ''), ('Available', 'num'), ('Price per Sheet', 'num'), ('Sheets', ''), ('Amount', 'num')], [lines], 'stack-sm')}</div></section>
    </div>
    <div class="stack">
      {card('Sale Summary', kv([('Sheets', str(sum(ENTRY.values()))), ('Subtotal', M(e_sub)), ('Central GST 9%', M(e_gst)), ('State GST 9%', M(e_gst))]) + kv([('Total', M(e_total))], 'total'))}
      <section class="card"><header><h2>Retailer Credit</h2></header><div class="body">{kv([('Credit Limit', ML(ch[6])), ('Owes', ML(RTL_OWES['CHR'])), ('This Sale', M(e_total))])}
        <span class="meter {meter_cls(used)}" style="margin-top:1rem"><i style="width:{used}%"></i></span>
        {kv([('Credit Available', ML(ch[6] - e_after))], 'total')}</div></section>
    </div>
  </div>
'''
page('secondary', 'tertiary-sales-entry', 'SEC-TSL-02', 'Secondary Customer — Owner — Tertiary Sales Entry (SEC-TSL-02)', body)

# ---------- Tertiary Sales History ----------
def tcnt(st): return sum(1 for s in TSALES if s['payment'] == st)
hist = ''.join(f'<tr><td class="mono nowrap"><b>{s["number"]}</b></td><td>{s["date"]}</td><td>{link("SEC-RTL-02", RTL[s["retailer"]][1])}</td><td class="num">{N(s["sheets"])}</td><td class="num"><b>{M(s["value"])}</b></td>'
               f'<td>{pay_chip(s["payment"])}</td><td><div class="row-actions">{dl_btn("Download sale invoice")}</div></td></tr>\n' for s in TSALES)
body = f'''  <div class="head">
    <h1>Tertiary Sales History</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Sales</button><a class="btn pri" data-link="SEC-TSL-02"><i data-icon="plus"></i>Record Sale</a></div>
  </div>
  <div class="kpis">
    {kpi('Sales This Month', ML(630000), up(pct(630000, 600000)))}
    {kpi('Sales Recorded', str(len(TSALES)))}
    {kpi('Sheets Sold', N(370))}
    {kpi('Awaiting Payment', ML(sum(RTL_OWES.values())))}
  </div>
  <section class="card flush">
    {tabs([('All Sales', len(TSALES), True), ('Paid', tcnt('Paid'), False), ('Unpaid', tcnt('Unpaid'), False)])}
    {filters('Search by sale number or retailer', 'Search sales', ('Date Range', 'October 2026'), ('Retailer', 'All'), ('Payment', 'All'))}
    <div class="body">{table([('Sale Number', ''), ('Date', ''), ('Retailer', ''), ('Sheets', 'num'), ('Value', 'num'), ('Payment', ''), ('', '')], [hist])}
      {pager(f'Showing 1 to {len(TSALES)} of {len(TSALES)} sales', 1)}</div>
  </section>
'''
page('secondary', 'tertiary-sales-history', 'SEC-TSL-03', 'Secondary Customer — Owner — Tertiary Sales History (SEC-TSL-03)', body)

# ---------- Invoices Overview ----------
inv_oct = [i for i in BINV if i[2].endswith('/10/2026')]
assert len(inv_oct) == 6 and sum(i[4] for i in inv_oct) == 684000
rows = ''.join(f'<tr><td>{link("SEC-BIL-02", i[0])}</td><td class="mono nowrap">{DISPATCH[i[0]]}</td><td>{i[2]}</td><td>{i[3]}</td><td class="num">{M(i[4])}</td><td class="num"><b>{M(i[4] - i[5])}</b></td><td>{b_status(i)}</td></tr>' for i in BOPEN)
body = f'''  <div class="head">
    <h1>Invoices Overview</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Invoices</button></div>
  </div>
  <div class="kpis">
    {kpi('Outstanding Balance', ML(BRV_OWES), chip(f'{cp_used}% of Credit Limit', 'ok'))}
    {kpi('Invoiced This Month', ML(684000), chip('6 invoices', 'plain'))}
    {kpi('Paid This Month', ML(BPAID_OCT), chip('5 payments', 'plain'))}
    {kpi('Overdue', M(0), chip('None', 'ok'))}
  </div>
  <section class="card flush">
    {tabs([('Open Invoices', len(BOPEN), True), ('Overdue', 0, False), ('Paid', B_INV_COUNT - len(BOPEN), False), ('All Invoices', B_INV_COUNT, False)])}
    {filters('Search by invoice or dispatch number', 'Search invoices', ('Date Range', 'Last 90 days'), ('Status', 'All'))}
    <div class="body">{table([('Invoice Number', ''), ('Dispatch Number', ''), ('Issue Date', ''), ('Due Date', ''), ('Invoice Amount', 'num'), ('Balance Due', 'num'), ('Status', '')], [rows],
      foot=f'<tfoot><tr><td colspan="4">Total</td><td class="num">{M(sum(i[4] for i in BOPEN))}</td><td class="num">{M(BRV_OWES)}</td><td></td></tr></tfoot>')}
      {pager(f'Showing 1 to {len(BOPEN)} of {len(BOPEN)} open invoices', 1)}</div>
  </section>
'''
page('secondary', 'invoices-overview', 'SEC-BIL-01', 'Secondary Customer — Owner — Invoices Overview (SEC-BIL-01)', body)

# ---------- Invoice Details (SAL-2026-3040) ----------
inv = INV_BY['SAL-2026-3040']; o = O40
due_in = (pd(inv[3]) - TODAY).days
lrows = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num">{N(q)}</td><td class="num">{M(dp(s))}</td><td class="num"><b>{M(q * dp(s))}</b></td></tr>' for s, q in o['lines'])
body = f'''  <div class="head">
    <div class="title-row"><h1>{inv[0]}</h1>{chip('Unpaid')}{chip(f'Due in {due_in} days', 'blue')}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="print"></i>Print Invoice</button><button class="btn" type="button"><i data-icon="download"></i>Download Invoice</button><a class="btn pri" data-link="SEC-SUP-02"><i data-icon="help"></i>Raise Support Ticket</a></div>
  </div>
  <section class="card pad"><div class="stats" style="--cols:repeat(5,minmax(0,1fr))"><div><span>Issue Date</span><b>{inv[2]}</b></div><div><span>Due Date</span><b>{inv[3]}</b></div><div><span>Invoice Amount</span><b>{M(inv[4])}</b></div><div><span>Amount Paid</span><b>{M(0)}</b></div><div><span>Balance Due</span><b>{M(inv[4])}</b></div></div></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      <section class="card flush"><header><h2>Items</h2></header>
        <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Price per Sheet', 'num'), ('Amount', 'num')], [lrows], foot=f'<tfoot><tr><td colspan="4">Subtotal</td><td class="num">{M(O40_SUB)}</td></tr></tfoot>')}
          <div style="padding:1rem 1.125rem"><dl class="kv" style="max-width:22rem;margin-left:auto"><dt>Trade Discount</dt><dd style="color:var(--ok)">{SQ}{M(O40_DISC)}</dd><dt>Taxable Amount</dt><dd>{M(O40_TAX)}</dd><dt>Central GST 9%</dt><dd>{M(O40_GST)}</dd><dt>State GST 9%</dt><dd>{M(O40_GST)}</dd></dl>
          <dl class="kv total" style="max-width:22rem;margin-left:auto"><dt>Total</dt><dd>{M(inv[4])}</dd></dl></div></div></section>
      <section class="card flush"><header><h2>Invoice Activity</h2></header><div class="body">{table([('Date', ''), ('Event', ''), ('By', '')], [
        '<tr><td class="nowrap">25/10/2026 09:48</td><td><b>Invoice viewed</b></td><td>Sunita Rao</td></tr>',
        '<tr><td class="nowrap">24/10/2026 17:46</td><td><b>Invoice sent by email</b></td><td>Distributor Alpha</td></tr>',
        '<tr><td class="nowrap">24/10/2026 17:45</td><td><b>Invoice issued</b></td><td>Distributor Alpha</td></tr>'])}</div></section>
    </div>
    <div class="stack">
      {card('Invoice Information', kv([('Invoice Number', f'<span class="mono">{inv[0]}</span>'), ('Order Number', link('SEC-ORD-02', inv[1], False)), ('Dispatch Number', f'<span class="mono">{o["dispatch"]}</span>'), ('Payment Terms', '30 days'), ('Status', chip('Unpaid'))]))}
      {card('Billed To', kv([('Customer', 'Bravo Laminate Traders'), ('GST Number', '<span style="white-space:nowrap">27AAKFB3318D1ZP</span>'), ('Address', 'Shop 6, Laminate Market Road, Hadapsar, Pune, Postal Code 411028')]))}
      {card('Issued By', kv([('Company', 'Distributor Alpha Private Limited'), ('GST Number', '<span style="white-space:nowrap">27AABCD4521F1Z7</span>'), ('Warehouse', 'Bhiwandi Warehouse, Thane District')]))}
    </div>
  </div>
'''
page('secondary', 'invoice-details', 'SEC-BIL-02', 'Secondary Customer — Owner — Invoice Details (SEC-BIL-02)', body)

# ---------- Payments Overview ----------
pay_rows = ''.join(f'<tr><td class="mono nowrap"><b>{link("SEC-BIL-04", p[0], False)}</b></td><td>{p[1]}</td><td>{p[3]}</td><td class="mono nowrap">{p[4]}</td><td class="num"><b>{M(p[2])}</b></td><td>{chip("Confirmed", "ok")}</td><td><div class="row-actions"><a class="btn sm" data-link="SEC-BIL-04">View</a></div></td></tr>' for p in BPAY)
mode_col = {'Bank Transfer': 'var(--accent)', 'Net Banking': '#0b8fa8', 'Cheque': '#e0a030'}
body = f'''  <div class="head">
    <h1>Payments Overview</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Payments</button></div>
  </div>
  <div class="kpis">
    {kpi('Paid This Month', ML(BPAID_OCT), chip('5 payments', 'plain'))}
    {kpi('Largest Payment', ML(max(p[2] for p in BPAY_OCT)))}
    {kpi('Average Payment', ML(round(BPAID_OCT / 5)))}
    {kpi('Outstanding Balance', ML(BRV_OWES))}
  </div>
  <div class="grid g-chart">
    {card('Payments by Month', chart('bars', MONTHS, [{'name': 'Payments to Distributor Alpha', 'values': BPAID_MONTH, 'color': 'var(--ok)'}], money=True, height=280))}
    <section class="card"><header><h2>Payments by Mode</h2></header><div class="body center">{chart('donut', series=[{'name': m, 'value': v, 'color': mode_col[m]} for m, v in sorted(BMODE_OCT.items(), key=lambda x: -x[1])], center='5', caption='payments')}</div></section>
  </div>
  <section class="card flush">
    {filters('Search by payment or invoice number', 'Search payments', ('Date Range', 'Last 90 days'), ('Mode', 'All'))}
    <div class="body">{table([('Payment Number', ''), ('Date', ''), ('Mode', ''), ('Invoice Number', ''), ('Amount', 'num'), ('Status', ''), ('', '')], [pay_rows])}
      {pager('Showing 1 to 10 of 394 payments')}</div>
  </section>
'''
page('secondary', 'payments-overview', 'SEC-BIL-03', 'Secondary Customer — Owner — Payments Overview (SEC-BIL-03)', body)

# ---------- Payment Details (PAY-2026-D0521) ----------
pay = BPAY[0]; pinv = INV_BY[pay[4]]
assert pay[0] == 'PAY-2026-D0521' and pinv[4] == pay[2]
body = f'''  <div class="head">
    <div class="title-row"><h1>{pay[0]}</h1>{chip('Confirmed', 'ok')}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Receipt</button><a class="btn pri" data-link="SEC-BIL-02"><i data-icon="receipt"></i>View Invoice</a></div>
  </div>
  <section class="card pad"><div class="stats" style="--cols:repeat(4,minmax(0,1fr))"><div><span>Amount</span><b>{M(pay[2])}</b></div><div><span>Payment Date</span><b>{pay[1]}</b></div><div><span>Mode</span><b>{pay[3]}</b></div><div><span>Bank Reference</span><b class="mono">SB26102200318</b></div></div></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      <section class="card flush"><header><h2>Invoices Settled</h2></header><div class="body">{table([('Invoice Number', ''), ('Invoice Amount', 'num'), ('This Payment', 'num'), ('Balance After', 'num'), ('Status', '')],
        [f'<tr><td>{link("SEC-BIL-02", pinv[0])}</td><td class="num">{M(pinv[4])}</td><td class="num"><b>{M(pay[2])}</b></td><td class="num">{M(pinv[4] - pay[2])}</td><td>{chip("Paid")}</td></tr>'])}</div></section>
      <section class="card"><header><h2>Payment Progress</h2></header><div class="body"><ol class="track">
        <li class="done"><i></i><b>Recorded</b><span>22/10/2026 10:40</span></li><li class="done"><i></i><b>Received by Distributor Alpha</b><span>22/10/2026 15:10</span></li><li class="done"><i></i><b>Confirmed</b><span>23/10/2026 09:20</span></li></ol></div></section>
    </div>
    <div class="stack">
      {card('Payment Information', kv([('Payment Number', f'<span class="mono">{pay[0]}</span>'), ('Mode', pay[3]), ('Bank Reference', '<span class="mono">SB26102200318</span>'), ('Paid From', 'Sahyadri Bank, Hadapsar Branch'), ('Paid To', 'Distributor Alpha'), ('Recorded By', 'Sunita Rao'), ('Status', chip('Confirmed', 'ok'))]))}
      <section class="card flush"><header><h2>Receipt</h2></header><div class="body">{table([('Document', ''), ('Type', ''), ('', '')], [f'<tr><td><b>Payment Receipt</b></td><td><span class="tag">PDF</span></td><td><div class="row-actions">{dl_btn("Download receipt")}</div></td></tr>'])}</div></section>
    </div>
  </div>
'''
page('secondary', 'payment-details', 'SEC-BIL-04', 'Secondary Customer — Owner — Payment Details (SEC-BIL-04)', body)
