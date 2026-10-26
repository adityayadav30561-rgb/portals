"""Phase 4, part B: Primary Customer Accountant: Dashboard, Purchase History, Outstanding Balances, Overdue Invoices, Record Payment,
Invoice Ageing Report, Purchase Summary Report, Financial Reports, Invoice Disputes, Invoice Dispute Details.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md "Phase 4 data".
Purchases are orders placed (PURCH_MONTH); invoiced amounts are named as such."""
from data import *

SQ = chr(0x2212)
OVERDUE_TOTAL = sum(i[4] - i[5] for i in OVERDUE)
def inv_status(i):
    if i[4] == i[5]: return chip('Paid')
    o = days_over(i)
    if o > 0: return chip(f'Overdue {o} days', 'bad')
    return chip('Partly Paid') if i[5] else chip('Unpaid')
def age_chip(i):
    o = days_over(i)
    return chip(f'{o} days overdue', 'bad') if o > 0 else chip(f'Due in {-o} days', 'blue')
def inv_link(i): return link('PRI-BIL-02', i[0])
def dispute_for(inv): return next((d for d in DISPUTES if d[1] == inv and d[6] != 'Resolved'), None)
cp = round(OUTSTANDING / CREDIT_LIMIT * 100)
assert cp == 37
credit_card = card('Credit Usage', f'''<span class="meter {meter_cls(cp)}" style="margin-bottom:1rem"><i style="width:{cp}%"></i></span>''' +
                   kv([('Credit Limit', ML(CREDIT_LIMIT)), ('Outstanding Balance', ML(OUTSTANDING)), ('Used', f'{cp}%'), ('Overdue', ML(OVERDUE_TOTAL)), ('Open Disputes', M(sum(d[5] for d in OPEN_DISPUTES)))]) + kv([('Credit Available', ML(CREDIT_AVAILABLE))], 'total'))
AGE_LABELS = ['Not Yet Due', '1 to 30 Days', '31 to 60 Days', '61 to 90 Days', 'Over 90 Days']
age_chart = chart('bars', AGE_LABELS, [{'name': 'Balance', 'values': [AGE_AMT[b] for b in BUCKETS], 'color': 'var(--accent)'}], money=True, height=230)
pay_rows = ''.join(f'<tr><td>{link("PRI-BIL-04", p[0])}</td><td>{p[1]}</td><td>{p[3]}</td><td>{link("PRI-BIL-02", p[4], False)}</td><td class="num"><b>{M(p[2])}</b></td></tr>' for p in PAYMENTS[:5])
open_rows = ''.join(f'<tr><td>{inv_link(i)}</td><td>{i[3]}</td><td class="num">{M(i[4])}</td><td class="num"><b>{M(i[4] - i[5])}</b></td><td>{inv_status(i)}</td></tr>' for i in OPEN_INV)

# ---------- Dashboard ----------
disp_list = ''.join(f'<li><div class="grow"><b>{d[0]}</b></div>{chip(d[6])}</li>' for d in DISPUTES)
body = f'''  <div class="head">
    <h1>Dashboard</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><a class="btn pri" data-link="PRI-BIL-08"><i data-icon="plus"></i>Record Payment</a></div>
  </div>
  <div class="kpis">
    {kpi('Outstanding Balance', ML(OUTSTANDING), chip(f'{cp}% of Credit Limit', 'warn'))}
    {kpi('Overdue', ML(OVERDUE_TOTAL), '<span class="delta down">2 invoices</span>')}
    {kpi('Paid This Month', ML(sum(p[2] for p in PAID_OCT)), chip('5 payments', 'plain'))}
    {kpi('Open Disputes', str(len(OPEN_DISPUTES)), chip(M(sum(d[5] for d in OPEN_DISPUTES)) + ' disputed', 'warn'))}
  </div>
  <div class="grid g-chart">
    {card('Balance by Age', age_chart)}
    {credit_card}
  </div>
  <div class="grid g-main-side" style="--side:22rem">
    <section class="card flush"><header><h2>Open Invoices</h2><a class="more" data-link="PRI-BIL-06">Outstanding balances</a></header>
      <div class="body">{table([('Invoice Number', ''), ('Due Date', ''), ('Invoice Amount', 'num'), ('Balance Due', 'num'), ('Status', '')], [open_rows], foot=f'<tfoot><tr><td colspan="3">Total</td><td class="num">{M(OUTSTANDING)}</td><td></td></tr></tfoot>')}</div></section>
    <section class="card"><header><h2>Invoice Disputes</h2><a class="more" data-link="PRI-BIL-09">All disputes</a></header>
      <div class="body"><ul class="list">{disp_list}</ul>{kv([('Open Disputed Amount', M(sum(d[5] for d in OPEN_DISPUTES)))], 'total')}</div></section>
  </div>
  <section class="card flush"><header><h2>Recent Payments</h2><a class="more" data-link="PRI-BIL-03">All payments</a></header>
    <div class="body">{table([('Payment Number', ''), ('Date', ''), ('Mode', ''), ('Invoice', ''), ('Amount', 'num')], [pay_rows])}</div></section>
'''
page('primary', 'accountant-dashboard', 'PRI-ACC-01', 'Primary Customer — Accountant — Dashboard (PRI-ACC-01)', body)

# ---------- Purchase History ----------
inv_hist = ''.join(f'<tr><td>{inv_link(i)}</td><td class="mono nowrap">{i[1]}</td><td>{i[2]}</td><td class="num"><b>{M(i[4])}</b></td><td class="num">{M(i[4] - i[5]) if i[4] - i[5] else "—"}</td><td>{inv_status(i)}</td></tr>' for i in INVOICES)
top_b = sorted(BOUGHT, key=lambda s: -BOUGHT[s])
bought_list = ''.join(f'<li>{sw(s, "", "width:2.5rem;height:2.5rem;flex:none")}<div class="grow"><b>{BY[s][1]}</b><span class="meter" style="margin-top:.5rem"><i style="width:{BOUGHT[s] / BOUGHT[top_b[0]] * 100:.0f}%"></i></span></div><b>{N(BOUGHT[s])}</b></li>' for s in top_b[:7])
body = f'''  <div class="head">
    <h1>Purchase History</h1>
    <div class="acts"><span class="sel"><small>Period</small> May to October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Purchases</button></div>
  </div>
  <div class="kpis">
    {kpi('Orders Placed This Month', ML(PURCH_MONTH[-1]), up('38.0%'))}
    {kpi('Invoiced This Month', ML(INV_ISSUED_OCT), chip('4 invoices', 'plain'))}
    {kpi('Sheets Purchased', N(2750), chip('6 orders', 'plain'))}
    {kpi('Orders in Six Months', ML(sum(PURCH_MONTH)))}
  </div>
  <div class="grid g-main-side" style="--side:26rem">
    {card('Purchases by Month', chart('bars', MONTHS, [{'name': 'Orders placed', 'values': PURCH_MONTH, 'color': 'var(--accent)'}], money=True, height=300))}
    {card('Sheets Purchased by Product', f'<ul class="list">{bought_list}</ul>')}
  </div>
  <section class="card flush"><header><h2>Invoices From Crestline</h2><a class="more" data-link="PRI-BIL-01">Invoices overview</a></header>
    <div class="body">{table([('Invoice Number', ''), ('Order Number', ''), ('Issue Date', ''), ('Invoice Amount', 'num'), ('Balance Due', 'num'), ('Status', '')], [inv_hist])}</div></section>
'''
page('primary', 'purchase-history', 'PRI-BIL-05', 'Primary Customer — Accountant — Purchase History (PRI-BIL-05)', body)

# ---------- Outstanding Balances ----------
ob_rows = ''.join(f'<tr><td>{inv_link(i)}</td><td class="mono nowrap">{i[1]}</td><td>{i[3]}</td><td class="num">{M(i[4])}</td><td class="num">{M(i[5]) if i[5] else "—"}</td><td class="num"><b>{M(i[4] - i[5])}</b></td><td>{bucket(i)}</td><td>{inv_status(i)}</td></tr>' for i in OPEN_INV)
body = f'''  <div class="head">
    <h1>Outstanding Balances</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Statement</button><a class="btn pri" data-link="PRI-BIL-08"><i data-icon="plus"></i>Record Payment</a></div>
  </div>
  <div class="kpis">
    {kpi('Outstanding Balance', ML(OUTSTANDING), chip('5 invoices', 'plain'))}
    {kpi('Not Yet Due', ML(AGE_AMT['Not Yet Due']), chip('3 invoices', 'ok'))}
    {kpi('Overdue', ML(OVERDUE_TOTAL), '<span class="delta down">2 invoices</span>')}
    {kpi('Credit Available', ML(CREDIT_AVAILABLE))}
  </div>
  <div class="grid g-chart">
    {card('Balance by Age', age_chart)}
    {credit_card}
  </div>
  <section class="card flush"><header><h2>Invoices Behind the Balance</h2></header>
    <div class="body">{table([('Invoice Number', ''), ('Order Number', ''), ('Due Date', ''), ('Invoice Amount', 'num'), ('Paid', 'num'), ('Balance Due', 'num'), ('Age', ''), ('Status', '')], [ob_rows],
      foot=f'<tfoot><tr><td colspan="3">Total</td><td class="num">{M(sum(i[4] for i in OPEN_INV))}</td><td class="num">{M(sum(i[5] for i in OPEN_INV))}</td><td class="num">{M(OUTSTANDING)}</td><td colspan="2"></td></tr></tfoot>')}</div></section>
'''
page('primary', 'outstanding-balances', 'PRI-BIL-06', 'Primary Customer — Accountant — Outstanding Balances (PRI-BIL-06)', body)

# ---------- Overdue Invoices ----------
od_rows = ''
for i in OVERDUE:
    d = dispute_for(i[0])
    od_rows += (f'<tr><td>{inv_link(i)}</td><td>{i[3]}</td><td>{chip(f"{days_over(i)} days", "bad")}</td><td class="num">{M(i[4])}</td><td class="num"><b>{M(i[4] - i[5])}</b></td>'
                f'<td>{link("PRI-BIL-10", d[0], False) + " " + chip(d[6]) if d else "—"}</td><td><div class="row-actions"><a class="btn sm pri" data-link="PRI-BIL-08">Record Payment</a></div></td></tr>')
oldest = max(days_over(i) for i in OVERDUE)
body = f'''  <div class="head">
    <h1>Overdue Invoices</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Overdue Invoices</button><a class="btn pri" data-link="PRI-BIL-08"><i data-icon="plus"></i>Record Payment</a></div>
  </div>
  <div class="kpis">
    {kpi('Overdue Balance', ML(OVERDUE_TOTAL))}
    {kpi('Overdue Invoices', str(len(OVERDUE)))}
    {kpi('Oldest Overdue', f'{oldest} <small>days</small>')}
    {kpi('Share of Outstanding Balance', f'{OVERDUE_TOTAL / OUTSTANDING * 100:.1f}%')}
  </div>
  <section class="card flush">
    {tabs([('All Overdue', 2, True), ('1 to 30 Days', 1, False), ('31 to 60 Days', 1, False), ('Over 60 Days', 0, False)])}
    {filters('Search by invoice or order number', 'Search overdue invoices', ('Age', 'All'), ('Dispute', 'All'))}
    <div class="body">{table([('Invoice Number', ''), ('Due Date', ''), ('Days Overdue', ''), ('Invoice Amount', 'num'), ('Balance Due', 'num'), ('Dispute', ''), ('', '')], [od_rows],
      foot=f'<tfoot><tr><td colspan="3">Total</td><td class="num">{M(sum(i[4] for i in OVERDUE))}</td><td class="num">{M(OVERDUE_TOTAL)}</td><td colspan="2"></td></tr></tfoot>')}
      {pager('Showing 1 to 2 of 2 overdue invoices', 1)}</div>
  </section>
'''
page('primary', 'overdue-invoices', 'PRI-BIL-07', 'Primary Customer — Accountant — Overdue Invoices (PRI-BIL-07)', body)

# ---------- Record Payment ----------
SEL = {'INV-2026-02986', 'INV-2026-03021'}
pay_total = sum(i[4] - i[5] for i in OPEN_INV if i[0] in SEL)
assert pay_total == OVERDUE_TOTAL == 318400
inv_pick = ''
for i in OPEN_INV:
    on = i[0] in SEL; bal = i[4] - i[5]
    inv_pick += (f'<tr><td class="c"><input type="checkbox" aria-label="Pay {i[0]}"{" checked" if on else ""}></td><td>{inv_link(i)}</td><td>{i[3]}</td><td>{chip("Overdue", "bad") if days_over(i) > 0 else inv_status(i)}</td><td class="num">{M(bal)}</td>'
                 f'<td class="num"><input class="input sm" style="width:7rem;text-align:right" aria-label="Amount to pay for {i[0]}" value="{M(bal) if on else ""}" placeholder="₹0"></td></tr>\n')
def upload(name, fname=None):
    inner = f'<span class="file"><i data-icon="doc"></i>{fname}</span>' if fname else ''
    return f'<div class="drop"><b>{name}</b>{inner}<button class="btn sm" type="button"><i data-icon="upload"></i>{"Replace" if fname else "Upload"}</button></div>'
body = f'''  <div class="head">
    <h1>Record Payment</h1>
    <div class="acts"><a class="btn" data-link="PRI-BIL-03">Cancel</a><button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Record Payment</button></div>
  </div>
  <div class="grid g-main-side" style="--side:19rem">
    <div class="stack">
      {form('Payment Details', fld('Payment Date', 'pd', '26/10/2026'), fld('Payment Mode', 'pm', 'Bank Transfer', 'select', ['Bank Transfer', 'Net Banking', 'Cheque']),
            fld('Paid From', 'pf', 'Sahyadri Bank, Bhiwandi Branch', 'select', ['Sahyadri Bank, Bhiwandi Branch']), fld('Bank Reference', 'br', 'SB26102600502'))}
      <section class="card flush"><header><h2>Invoices to Pay</h2></header>
        <div class="body">{table([('', 'c'), ('Invoice Number', ''), ('Due Date', ''), ('Status', ''), ('Balance Due', 'num'), ('Amount to Pay', 'num')], [inv_pick])}</div></section>
      <section class="card"><header><h2>Proof of Payment</h2></header><div class="body">{upload('Bank Confirmation', 'bank-confirmation.pdf')}</div></section>
    </div>
    <div class="stack">
      {card('Payment Summary', kv([('Invoices Selected', str(len(SEL))), ('Mode', 'Bank Transfer'), ('Payment Date', '26/10/2026')]) + kv([('Payment Total', M(pay_total))], 'total'))}
      {card('Balance After Payment', kv([('Outstanding Balance', ML(OUTSTANDING - pay_total)), ('Overdue', M(0)), ('Credit Available', ML(CREDIT_AVAILABLE + pay_total))]))}
    </div>
  </div>
'''
page('primary', 'record-payment', 'PRI-BIL-08', 'Primary Customer — Accountant — Record Payment (PRI-BIL-08)', body)

# ---------- Invoice Ageing Report ----------
tot = OUTSTANDING
sum_rows = ''.join(f'<tr><td><b>{b}</b></td><td class="num">{len(AGE[b])}</td><td class="num"><b>{M(AGE_AMT[b]) if AGE_AMT[b] else "—"}</b></td>'
                   f'<td><span class="inline-meter"><span class="meter {"" if b == "Not Yet Due" else "bad" if "Over 90" in b or "61" in b else "warn"}"><i style="width:{AGE_AMT[b] / tot * 100:.0f}%"></i></span><b>{AGE_AMT[b] / tot * 100:.1f}%</b></span></td></tr>' for b in BUCKETS)
det_rows = ''.join(f'<tr><td>{inv_link(i)}</td><td class="mono nowrap">{i[1]}</td><td>{i[2]}</td><td>{i[3]}</td><td>{bucket(i)}</td><td class="num"><b>{M(i[4] - i[5])}</b></td></tr>' for b in BUCKETS for i in AGE[b])
body = f'''  <div class="head">
    <h1>Invoice Ageing Report</h1>
    <div class="acts"><span class="sel"><small>As On</small> 26 October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('Outstanding Balance', ML(OUTSTANDING), chip('5 invoices', 'plain'))}
    {kpi('Not Yet Due', ML(AGE_AMT['Not Yet Due']), chip(f'{AGE_AMT["Not Yet Due"] / tot * 100:.1f}%', 'ok'))}
    {kpi('Overdue', ML(OVERDUE_TOTAL), chip(f'{OVERDUE_TOTAL / tot * 100:.1f}%', 'bad'))}
    {kpi('Oldest Overdue', f'{oldest} <small>days</small>')}
  </div>
  <div class="grid g-2">
    {card('Balance by Age', age_chart)}
    <section class="card"><header><h2>Share of Balance</h2></header><div class="body center">{chart('donut', series=[{'name': b, 'value': AGE_AMT[b], 'color': c} for b, c in zip(BUCKETS[:3], ['var(--ok)', '#e0a030', 'var(--bad)'])], center='5', caption='invoices')}</div></section>
  </div>
  <section class="card flush"><header><h2>Ageing Summary</h2></header>
    <div class="body">{table([('Age Group', ''), ('Invoices', 'num'), ('Balance Due', 'num'), ('Share of Balance', '')], [sum_rows], foot=f'<tfoot><tr><td>Total</td><td class="num">5</td><td class="num">{M(OUTSTANDING)}</td><td></td></tr></tfoot>')}</div></section>
  <section class="card flush"><header><h2>Invoices by Age</h2></header>
    <div class="body">{table([('Invoice Number', ''), ('Order Number', ''), ('Issue Date', ''), ('Due Date', ''), ('Age Group', ''), ('Balance Due', 'num')], [det_rows])}</div></section>
'''
page('primary', 'invoice-ageing-report', 'PRI-RPT-03', 'Primary Customer — Accountant — Invoice Ageing Report (PRI-RPT-03)', body)

# ---------- Purchase Summary Report ----------
oct_t = MONTH_TAX[-1]
mon_rows = ''.join(f'<tr><td><b>{m}</b></td><td class="num">{M(t["taxable"])}</td><td class="num">{M(t["gst"])}</td><td class="num">{M(t["gst"])}</td><td class="num">{M(t["freight"])}</td><td class="num"><b>{M(t["total"])}</b></td></tr>' for m, t in zip(MONTHS, MONTH_TAX))
sum_t = {k: sum(t[k] for t in MONTH_TAX) for k in ('taxable', 'gst', 'freight', 'total')}
assert sum_t['total'] == 15272882
prod_rows = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num">{N(BOUGHT[s])}</td><td class="num"><b>{M(BOUGHT_VALUE[s])}</b></td>'
                    f'<td><span class="inline-meter"><span class="meter"><i style="width:{BOUGHT_VALUE[s] / max(BOUGHT_VALUE.values()) * 100:.0f}%"></i></span><b>{BOUGHT_VALUE[s] / PURCH_MONTH[-1] * 100:.1f}%</b></span></td></tr>' for s in sorted(BOUGHT, key=lambda x: -BOUGHT_VALUE[x]))
body = f'''  <div class="head">
    <h1>Purchase Summary Report</h1>
    <div class="acts"><span class="sel"><small>Period</small> May to October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('Orders Placed This Month', ML(PURCH_MONTH[-1]), up('38.0%'))}
    {kpi('Taxable Amount', ML(oct_t['taxable']))}
    {kpi('Central GST and State GST', ML(2 * oct_t['gst']))}
    {kpi('Freight', M(oct_t['freight']))}
  </div>
  <div class="grid g-2">
    {card('Purchases by Month', chart('bars', MONTHS, [{'name': 'Taxable amount', 'values': [t['taxable'] for t in MONTH_TAX], 'color': 'var(--accent)'}, {'name': 'Central GST and State GST', 'values': [2 * t['gst'] for t in MONTH_TAX], 'color': '#e0a030'}], money=True, height=250))}
    <section class="card"><header><h2>Tax in October</h2></header><div class="body">{kv([('Orders Placed', '6'), ('Sheets Purchased', N(2750)), ('Taxable Amount', M(oct_t['taxable'])), ('Central GST 9%', M(oct_t['gst'])), ('State GST 9%', M(oct_t['gst'])), ('Freight', M(oct_t['freight']))]) + kv([('Total Purchases', M(oct_t['total']))], 'total')}</div></section>
  </div>
  <section class="card flush"><header><h2>Purchases and Tax by Month</h2></header>
    <div class="body">{table([('Month', ''), ('Taxable Amount', 'num'), ('Central GST', 'num'), ('State GST', 'num'), ('Freight', 'num'), ('Total Purchases', 'num')], [mon_rows],
      foot=f'<tfoot><tr><td>Total</td><td class="num">{M(sum_t["taxable"])}</td><td class="num">{M(sum_t["gst"])}</td><td class="num">{M(sum_t["gst"])}</td><td class="num">{M(sum_t["freight"])}</td><td class="num">{M(sum_t["total"])}</td></tr></tfoot>')}</div></section>
  <section class="card flush"><header><h2>Purchases by Product in October</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Purchases', 'num'), ('Share of Purchases', '')], [prod_rows],
      foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(2750)}</td><td class="num">{M(PURCH_MONTH[-1])}</td><td></td></tr></tfoot>')}</div></section>
'''
page('primary', 'purchase-summary-report', 'PRI-RPT-04', 'Primary Customer — Accountant — Purchase Summary Report (PRI-RPT-04)', body)

# ---------- Financial Reports ----------
paid_total = sum(PAID_MONTH); assert paid_total == 13399660
cn_rows = ''.join(f'<tr><td class="mono nowrap"><b>{c[0]}</b></td><td>{c[1]}</td><td class="mono nowrap">{c[2]}</td><td class="mono nowrap">{c[3]}</td><td class="num"><b>{M(c[4])}</b></td><td>{chip("Applied", "ok")}</td></tr>' for c in CREDIT_NOTES)
mode_col = {'Bank Transfer': 'var(--accent)', 'Net Banking': '#0b8fa8', 'Cheque': '#e0a030'}
oct_pay_rows = ''.join(f'<tr><td>{link("PRI-BIL-04", p[0])}</td><td>{p[1]}</td><td>{p[3]}</td><td class="num"><b>{M(p[2])}</b></td></tr>' for p in PAID_OCT)
body = f'''  <div class="head">
    <h1>Financial Reports</h1>
    <div class="acts"><span class="sel"><small>Period</small> May to October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('Payments Made', ML(paid_total))}
    {kpi('Credit Notes', M(sum(c[4] for c in CREDIT_NOTES)), chip('3 credit notes', 'plain'))}
    {kpi('Orders Placed', ML(sum(PURCH_MONTH)))}
    {kpi('Outstanding Balance', ML(OUTSTANDING), chip(f'{cp}% of Credit Limit', 'warn'))}
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    {card('Orders Placed and Payments Made by Month', chart('bars', MONTHS, [{'name': 'Orders placed', 'values': PURCH_MONTH, 'color': 'var(--accent)'}, {'name': 'Payments made', 'values': PAID_MONTH, 'color': 'var(--teal)'}], money=True, height=260))}
    {card('Balance Summary', kv([('Credit Limit', ML(CREDIT_LIMIT)), ('Outstanding Balance', ML(OUTSTANDING)), ('Credit Used', f'{cp}%'), ('Overdue', ML(OVERDUE_TOTAL)), ('Open Disputes', M(sum(d[5] for d in OPEN_DISPUTES)))]) + kv([('Credit Available', ML(CREDIT_AVAILABLE))], 'total'))}
  </div>
  <div class="grid g-2">
    <section class="card"><header><h2>Payments by Mode in October</h2></header><div class="body center">{chart('donut', series=[{'name': m, 'value': v, 'color': mode_col[m]} for m, v in sorted(MODE_OCT.items(), key=lambda x: -x[1])], center='5', caption='payments')}</div></section>
    <section class="card flush"><header><h2>Payments in October</h2><a class="more" data-link="PRI-BIL-03">All payments</a></header><div class="body">{table([('Payment Number', ''), ('Date', ''), ('Mode', ''), ('Amount', 'num')], [oct_pay_rows], foot=f'<tfoot><tr><td colspan="3">Total</td><td class="num">{M(sum(MODE_OCT.values()))}</td></tr></tfoot>')}</div></section>
  </div>
  <section class="card flush"><header><h2>Credit Notes</h2></header>
    <div class="body">{table([('Credit Note Number', ''), ('Date', ''), ('Return Request', ''), ('Order Number', ''), ('Credit Amount', 'num'), ('Status', '')], [cn_rows],
      foot=f'<tfoot><tr><td colspan="4">Total</td><td class="num">{M(sum(c[4] for c in CREDIT_NOTES))}</td><td></td></tr></tfoot>')}</div></section>
'''
page('primary', 'financial-reports', 'PRI-RPT-05', 'Primary Customer — Accountant — Financial Reports (PRI-RPT-05)', body)

# ---------- Invoice Disputes ----------
dis_rows = ''.join(f'<tr><td>{link("PRI-BIL-10", d[0])}</td><td class="nowrap">{link("PRI-BIL-02", d[1], False)}</td><td>{d[2]}</td><td>{d[3]}</td><td class="num"><b>{M(d[5])}</b></td><td>{chip(d[6])}</td><td>{d[7]}</td></tr>' for d in DISPUTES)
body = f'''  <div class="head">
    <h1>Invoice Disputes</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Disputes</button><button class="btn pri" type="button"><i data-icon="plus"></i>Raise Invoice Dispute</button></div>
  </div>
  <div class="kpis">
    {kpi('Open Disputes', str(len(OPEN_DISPUTES)))}
    {kpi('Disputed Amount', M(sum(d[5] for d in OPEN_DISPUTES)), chip('Inside the balance', 'plain'))}
    {kpi('Awaiting Your Reply', '1', chip('DIS-2026-0014', 'warn'))}
    {kpi('Resolved', '1')}
  </div>
  <section class="card flush">
    {tabs([('All Disputes', 3, True), ('Open', 2, False), ('Resolved', 1, False)])}
    {filters('Search by dispute or invoice number', 'Search invoice disputes', ('Date Range', 'Last 90 days'), ('Reason', 'All'), ('Status', 'All'))}
    <div class="body">{table([('Dispute Number', ''), ('Invoice Number', ''), ('Raised', ''), ('Reason', ''), ('Disputed Amount', 'num'), ('Status', ''), ('Company Response', '')], [dis_rows],
      foot=f'<tfoot><tr><td colspan="4">Total</td><td class="num">{M(sum(d[5] for d in DISPUTES))}</td><td colspan="2"></td></tr></tfoot>')}
      {pager('Showing 1 to 3 of 3 disputes', 1)}</div>
  </section>
'''
page('primary', 'invoice-disputes', 'PRI-BIL-09', 'Primary Customer — Accountant — Invoice Disputes (PRI-BIL-09)', body)

# ---------- Invoice Dispute Details (DIS-2026-0014) ----------
dd = DISPUTES[0]; assert dd[0] == 'DIS-2026-0014'
line_amt = 20 * 905; gst = round(0.09 * line_amt); assert (line_amt, gst, line_amt + 2 * gst) == (18100, 1629, dd[5])
inv64 = next(i for i in INVOICES if i[0] == dd[1])
def msg(who, init, when, text, me=False, files=()):
    fl = f'<div class="files">{"".join(f"<span class=file><i data-icon=doc></i>{f}</span>" for f in files)}</div>' if files else ''
    return f'<div class="msg{" me" if me else ""}"><div class="av">{init}</div><div><div class="top-line"><b>{who}</b><time>{when}</time></div><div class="bubble">{text}{fl}</div></div></div>'
thread = ''.join([
    msg('Suresh Iyer', 'SI', '22/10/2026 10:05', 'Twenty sheets of Arctic White Matte Laminate delivered with ORD-2026-10398 were the wrong product. Return request RTN-2026-0396 is raised. Please reduce INV-2026-03264 by ₹21,358.', True, ['wrong-product-photo.jpg', 'delivery-challan.pdf']),
    msg('Meera Kapoor, Crestline Customer Support', 'MK', '23/10/2026 14:30', 'Thank you, Suresh. The pickup is scheduled and a credit note will follow once the sheets reach the Vapi plant warehouse.'),
    msg('Suresh Iyer', 'SI', '24/10/2026 09:15', 'Understood. Please keep the balance of INV-2026-03264 open until the credit note is issued.', True),
    msg('Meera Kapoor, Crestline Customer Support', 'MK', '26/10/2026 11:00', 'Confirmed. Please share the name of the person who will hand over the sheets at Bhiwandi Warehouse.'),
])
steps = [('Raised', '22/10/2026', 'done'), ('Under Review', '23/10/2026', 'done'), ('Credit Note Pending', 'Awaiting Your Reply', 'now'), ('Resolved', '', '')]
track = '<ol class="track">' + ''.join(f'<li class="{c}"><i></i><b>{n}</b><span>{d}</span></li>' for n, d, c in steps) + '</ol>'
disp_line = f'<tr><td><div class="prod">{sw("LM-ARC-002")}<div><b>{BY["LM-ARC-002"][1]}</b></div></div></td><td class="mono nowrap">LM-ARC-002</td><td class="num">20</td><td class="num">{M(905)}</td><td class="num"><b>{M(line_amt)}</b></td></tr>'
ev_rows = ''.join(f'<tr><td><b>{n}</b></td><td><span class="tag">{t}</span></td><td><div class="row-actions">{dl_btn("Download " + n)}</div></td></tr>' for n, t in
                  [('Delivery Challan', 'PDF'), ('Delivered Sheets', 'Photo')])
body = f'''  <div class="head">
    <div class="title-row"><h1>{dd[0]}</h1>{chip(dd[6])}<span class="tag">{dd[3]}</span></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="check"></i>Withdraw Dispute</button></div>
  </div>
  <section class="card pad"><div class="stats" style="--cols:repeat(5,minmax(0,1fr))"><div><span>Invoice Number</span><b>{link("PRI-BIL-02", dd[1], False)}</b></div><div><span>Invoice Amount</span><b>{M(inv64[4])}</b></div><div><span>Disputed Amount</span><b>{M(dd[5])}</b></div><div><span>Balance Due on Invoice</span><b>{M(inv64[4] - inv64[5])}</b></div><div><span>Raised</span><b>{dd[2]}</b></div></div></section>
  <section class="card"><header><h2>Resolution Progress</h2></header><div class="body">{track}</div></section>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      <section class="card flush"><header><h2>Disputed Line</h2></header><div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets Disputed', 'num'), ('Price per Sheet', 'num'), ('Amount', 'num')], [disp_line])}
        <div style="padding:1rem 1.125rem"><dl class="kv" style="max-width:22rem;margin-left:auto"><dt>Central GST 9%</dt><dd>{M(gst)}</dd><dt>State GST 9%</dt><dd>{M(gst)}</dd></dl>
        <dl class="kv total" style="max-width:22rem;margin-left:auto"><dt>Disputed Amount</dt><dd>{M(dd[5])}</dd></dl></div></div></section>
      {card('Conversation', f'<div class="thread">{thread}</div>')}
      <section class="card"><header><h2>Reply</h2></header><div class="body"><div class="reply"><textarea class="input" aria-label="Reply" placeholder="Write a reply"></textarea>
        <div class="row"><button class="btn" type="button"><i data-icon="upload"></i>Attach Files</button><button class="btn pri" type="button">Send Reply</button></div></div></div></section>
    </div>
    <div class="stack">
      {card('Dispute Information', kv([('Dispute Number', f'<span class="mono">{dd[0]}</span>'), ('Status', chip(dd[6])), ('Reason', dd[3]), ('Raised By', 'Suresh Iyer'), ('Raised', dd[2]), ('Assigned To', 'Meera Kapoor'), ('Company Response', dd[7])]))}
      {card('Related Records', kv([('Invoice', link('PRI-BIL-02', dd[1], False)), ('Order', '<span class="mono">ORD-2026-10398</span>'), ('Return Request', '<span class="mono">RTN-2026-0396</span>'), ('Support Ticket', '<span class="mono">TKT-2026-0724</span>')]))}
      <section class="card flush"><header><h2>Evidence</h2></header><div class="body">{table([('Document', ''), ('Type', ''), ('', '')], [ev_rows])}</div></section>
    </div>
  </div>
'''
page('primary', 'invoice-dispute-details', 'PRI-BIL-10', 'Primary Customer — Accountant — Invoice Dispute Details (PRI-BIL-10)', body)
