"""Phase 3, part A: Primary Customer Owner: Dealer Network, Dealer Details, Add Dealer Request, Secondary Sales Overview,
Secondary Sales Entry, Secondary Sales History. Design rule: no text under page titles, no captions beside card titles, no
helper sentences. Data: docs/DATA.md "Dealers of Distributor Alpha"."""
from data import *

TOTAL_SHEETS = sum(DEALER_SHEETS.values())

# ---------- Dealer Network ----------
rows = []
for d in DEALERS:
    k = d[0]; pct_ = credit_pct(DEALER_OWES[k], d[9])
    rows.append(f'<tr><td>{link("PRI-DLR-02", d[1])}</td><td>{d[2]}</td><td>{chip(d[4])}</td><td class="num">{d[6]}</td><td class="num">{N(DEALER_SHEETS[k])}</td>'
                f'<td class="num"><b>{M(d[7])}</b></td><td class="num">{M(DEALER_OWES[k])}</td>'
                f'<td><span class="inline-meter"><span class="meter {meter_cls(pct_)}"><i style="width:{pct_}%"></i></span><b>{pct_}%</b></span></td>'
                f'<td><div class="row-actions"><a class="btn sm" data-link="PRI-DLR-02">View</a></div></td></tr>')
foot = (f'<tfoot><tr><td colspan="3">Total</td><td class="num">{sum(d[6] for d in DEALERS)}</td><td class="num">{N(TOTAL_SHEETS)}</td>'
        f'<td class="num">{M(sum(d[7] for d in DEALERS))}</td><td class="num">{M(OWED_TOTAL)}</td><td colspan="2"></td></tr></tfoot>')
body = f'''  <div class="head">
    <h1>Dealer Network</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Dealers</button><a class="btn pri" data-link="PRI-DLR-03"><i data-icon="plus"></i>Add Dealer Request</a></div>
  </div>
  <div class="kpis">
    {kpi('Dealers', '8', chip('1 New', 'blue'))}
    {kpi('Sales This Month', ML(3120000), up('11.8%'))}
    {kpi('Owed by Dealers', ML(OWED_TOTAL))}
    {kpi('Retailers Served', str(sum(d[6] for d in DEALERS)))}
  </div>
  <section class="card flush">
    {tabs([('All Dealers', 8, True), ('Active', 7, False), ('New', 1, False)])}
    {filters('Search by dealer name or city', 'Search dealers', ('Region', 'All'), ('Status', 'All'), ('Sort by', 'Sales This Month'))}
    <div class="body">{table([('Dealer',''), ('City',''), ('Status',''), ('Retailers','num'), ('Sheets','num'), ('Sales This Month','num'), ('Owes','num'), ('Credit Used',''), ('','')], rows, foot=foot)}
      {pager('Showing 1 to 8 of 8 dealers', 1)}</div>
  </section>
'''
page('primary', 'dealer-network', 'PRI-DLR-01', 'Primary Customer — Owner — Dealer Network (PRI-DLR-01)', body)

# ---------- Dealer Details (Dealer Bravo) ----------
b = DLR['BRV']; bs = [s for s in SALES if s['dealer'] == 'BRV']
owes = DEALER_OWES['BRV']; cp = credit_pct(owes, b[9])
bravo_month = [520000, 590000, 480000, 630000, 610000, 684000]
assert bravo_month[-1] == b[7] and bravo_month[-2] == b[8]
sale_rows = [f'<tr><td class="mono nowrap"><b>{s["number"]}</b></td><td>{s["date"]}</td><td class="num">{N(s["sheets"])}</td><td class="num"><b>{M(s["value"])}</b></td><td class="mono nowrap">{s["dispatch"]}</td><td>{pay_chip(s["payment"])}</td></tr>' for s in bs]
contacts = [('Sunita Rao', 'Owner', '+91 90000 31001'), ('Arjun Nair', 'Sales and Inventory Manager', '+91 90000 31002'), ('Rekha Sawant', 'Accountant', '+91 90000 31003')]
retailers = [('Retailer Charlie', 'Pune', 'Imran Sheikh'), ('Retailer Kiran Interiors', 'Pune', 'Kiran Desai'), ('Retailer Mehta Furniture', 'Pimpri', 'Nilesh Mehta')]
body = f'''  <div class="head">
    <div class="title-row"><h1>{b[1]}</h1>{chip('Active')}<span class="tag"><i data-icon="pin"></i>{b[2]}</span></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Download Statement</button><a class="btn pri" data-link="PRI-SAL-02"><i data-icon="plus"></i>Record Sale</a></div>
  </div>
  <div class="kpis">
    {kpi('Sales This Month', ML(b[7]), up(pct(b[7], b[8])))}
    {kpi('Owes', ML(owes))}
    {kpi('Credit Limit', ML(b[9]))}
    {kpi('Sheets This Month', N(DEALER_SHEETS['BRV']))}
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    {card('Sales by Month', chart('bars', MONTHS, [{'name': 'Sales to Dealer Bravo', 'values': bravo_month, 'color': 'var(--accent)'}], money=True, height=330))}
    {card('Account', kv([('Price Tier', 'Dealer Tier B'), ('Credit Limit', ML(b[9])), ('Credit Used', f'<span class="inline-meter"><span class="meter {meter_cls(cp)}"><i style="width:{cp}%"></i></span><b>{cp}%</b></span>'),
                         ('Credit Period', '30 days'), ('Customer Since', '03/09/2019'), ('Region', b[3]), ('Territory', 'Pune District'), ('Relationship Manager', 'Kavita Joshi'),
                         ('GST Number', '<span style="white-space:nowrap">27AAKFB3318D1ZP</span>'), ('Address', 'Shop 6, Laminate Market Road, Hadapsar, Pune, Postal Code 411028')]))}
  </div>
  <section class="card flush"><header><h2>Recent Sales</h2><a class="more" data-link="PRI-SAL-03">All sales</a></header>
    <div class="body">{table([('Sale Number',''), ('Date',''), ('Sheets','num'), ('Value','num'), ('Dispatch Number',''), ('Payment','')], sale_rows)}</div></section>
  <div class="grid g-2">
    <section class="card flush"><header><h2>Retailers</h2></header>
      <div class="body">{table([('Retailer',''), ('City',''), ('Contact Person',''), ('Status','')], [f'<tr><td><b>{n}</b></td><td>{c}</td><td>{p}</td><td>{chip("Active")}</td></tr>' for n, c, p in retailers])}</div></section>
    <section class="card flush"><header><h2>Contacts</h2></header>
      <div class="body">{table([('Name',''), ('Role',''), ('Phone','')], [f'<tr><td class="nowrap"><b>{n}</b></td><td>{r}</td><td class="nowrap">{p}</td></tr>' for n, r, p in contacts])}</div></section>
  </div>
'''
page('primary', 'dealer-details', 'PRI-DLR-02', 'Primary Customer — Owner — Dealer Details (PRI-DLR-02)', body)

# ---------- Add Dealer Request ----------
stepsl = [('Submit Request', 'Draft', 'plain'), ('Distributor Review: Kavita Joshi', 'Pending', 'warn'), ('Crestline Approval: Vikram Chopra', 'Pending', 'warn'), ('Dealer Activated', 'Pending', 'warn')]
approval = '<ul class="list">' + ''.join(f'<li><div class="grow"><b>{n}</b></div>{chip(c, k)}</li>' for n, c, k in stepsl) + '</ul>'
def upload(name, fname=None):
    inner = f'<span class="file"><i data-icon="doc"></i>{fname}</span>' if fname else ''
    return f'<div class="drop"><b>{name}</b>{inner}<button class="btn sm" type="button"><i data-icon="upload"></i>{"Replace" if fname else "Upload"}</button></div>'
body = f'''  <div class="head">
    <h1>Add Dealer Request</h1>
    <div class="acts"><a class="btn" data-link="PRI-DLR-01">Cancel</a><button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Submit Request</button></div>
  </div>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      {form('Business Details', fld('Dealer Business Name', 'bn', 'Dealer Lakshya'), fld('Legal Name', 'ln', 'Lakshya Laminates Private Limited'),
            fld('Business Type', 'bt', 'Dealer', 'select', ['Dealer', 'Wholesaler', 'Fabricator']), fld('GST Number', 'gst', '27AAHCL5521K1Z3'),
            fld('Permanent Account Number', 'pan', 'AAHCL5521K'), fld('Expected Monthly Volume in Sheets', 'vol', '150'))}
      {form('Owner Contact', fld('Owner Name', 'on', 'Lakshmikant Pawar'), fld('Mobile Number', 'mob', '+91 90000 41001'), fld('Email Address', 'em', 'lakshmikant.pawar@dealerlakshya.example', full=True))}
      {form('Address', fld('Address', 'ad', 'Shop 21, Station Road', full=True), fld('City', 'ct', 'Latur'), fld('District', 'ds', 'Latur'), fld('State', 'st', 'Maharashtra', 'select', ['Maharashtra', 'Goa']), fld('Postal Code', 'pc', '413512'))}
      {form('Proposed Terms', fld('Territory', 'tr', 'Latur and Osmanabad'), fld('Price Tier', 'pt', 'Dealer Tier B', 'select', ['Dealer Tier A', 'Dealer Tier B', 'Dealer Tier C']),
            fld('Requested Credit Limit', 'cl', '₹4,00,000'), fld('Credit Period', 'cp', '30 days', 'select', ['15 days', '30 days', '45 days']))}
      <section class="card"><header><h2>Documents</h2></header><div class="body"><div class="stack">
        {upload('GST Registration Certificate', 'gst-certificate.pdf')}{upload('Trade Licence', 'trade-licence.pdf')}{upload('Address Proof')}</div></div></section>
    </div>
    <div class="stack">{card('Approval Path', approval)}
      {card('Request Summary', kv([('Dealer', 'Dealer Lakshya'), ('City', 'Latur'), ('Requested Credit', ML(400000)), ('Documents Attached', '2 of 3')]))}</div>
  </div>
'''
page('primary', 'add-dealer-request', 'PRI-DLR-03', 'Primary Customer — Owner — Add Dealer Request (PRI-DLR-03)', body)

# ---------- Secondary Sales Overview ----------
share_rows = []
for d in sorted(DEALERS, key=lambda d: -d[7]):
    sh = d[7] / 3120000 * 100
    share_rows.append(f'<tr><td>{link("PRI-DLR-02", d[1])}</td><td>{d[2]}</td><td class="num">{N(DEALER_SHEETS[d[0]])}</td><td class="num"><b>{M(d[7])}</b></td>'
                      f'<td><span class="inline-meter"><span class="meter"><i style="width:{sh / 22 * 100:.0f}%"></i></span><b>{sh:.1f}%</b></span></td></tr>')
top = sorted(SOLD, key=lambda s: -SOLD[s])[:7]
top_rows = ''.join(f'<li>{sw(s, "", "width:2.5rem;height:2.5rem;flex:none")}<div class="grow"><b>{BY[s][1]}</b><span class="meter" style="margin-top:.5rem"><i style="width:{SOLD[s] / SOLD[top[0]] * 100:.0f}%"></i></span></div><b>{N(SOLD[s])}</b></li>' for s in top)
fin_colors = {'Woodgrain': '#0b8fa8', 'Matte': '#0a48fd', 'Gloss': '#e0a030', 'Texture': '#7a36fb', 'High Gloss': '#d43a2f', 'Suede': '#0c9b6a', 'Metallic': '#8b93a3'}
body = f'''  <div class="head">
    <h1>Secondary Sales Overview</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Download Report</button><a class="btn pri" data-link="PRI-SAL-02"><i data-icon="plus"></i>Record Sale</a></div>
  </div>
  <div class="kpis">
    {kpi('Sales This Month', ML(3120000), up('11.8%'))}
    {kpi('Sheets Sold', N(2195))}
    {kpi('Sales Recorded', str(SALE_COUNT))}
    {kpi('Average Sale Value', M(3120000 // SALE_COUNT))}
  </div>
  <div class="grid g-chart">
    {card('Sales to Dealers by Month', chart('bars', MONTHS, [{'name': 'Sales to Dealers', 'values': SALES_MONTH, 'color': 'var(--teal)'}], money=True, height=280))}
    <section class="card"><header><h2>Sheets Sold by Finish</h2></header><div class="body center">{chart('donut', series=[{'name': f, 'value': v, 'color': fin_colors[f]} for f, v in sorted(FINISH_SOLD.items(), key=lambda x: -x[1])], center='2,195', caption='sheets')}</div></section>
  </div>
  <div class="grid g-main-side" style="--side:26rem">
    <section class="card flush"><header><h2>Sales by Dealer</h2><a class="more" data-link="PRI-DLR-01">All dealers</a></header>
      <div class="body">{table([('Dealer',''), ('City',''), ('Sheets','num'), ('Sales','num'), ('Share of Sales','')], share_rows)}</div></section>
    {card('Top Products by Sheets', f'<ul class="list">{top_rows}</ul>')}
  </div>
'''
page('primary', 'secondary-sales-overview', 'PRI-SAL-01', 'Primary Customer — Owner — Secondary Sales Overview (PRI-SAL-01)', body)

# ---------- Secondary Sales Entry ----------
ENTRY = {'LM-WNT-001': 40, 'LM-ARC-002': 60, 'LM-CAL-003': 25, 'LM-OAK-004': 20}
e_sub = sum(q * dp(s) for s, q in ENTRY.items()); e_gst = round(e_sub * 0.09); e_total = e_sub + 2 * e_gst
assert (e_sub, e_gst, e_total) == (184275, 16585, 217445), (e_sub, e_gst, e_total)
lines = ''
for p in P:
    s = p[0]; q = ENTRY.get(s, 0)
    lines += (f'<tr><td><div class="prod">{sw(s)}<div><b>{p[1]}</b></div></div></td><td class="mono nowrap">{s}</td>'
              f'<td class="num">{M(dp(s))}</td><td>{qty(q)}</td><td class="num"><b>{M(q * dp(s)) if q else "—"}</b></td></tr>\n')
used = round((owes + e_total) / b[9] * 100)
body = f'''  <div class="head">
    <h1>Secondary Sales Entry</h1>
    <div class="acts"><a class="btn" data-link="PRI-SAL-03">Cancel</a><button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Record Sale</button></div>
  </div>
  <div class="grid g-main-side" style="--side:18rem">
    <div class="stack">
      {form('Sale Details', fld('Dealer', 'dl', 'Dealer Bravo, Pune', 'select', [f'{d[1]}, {d[2]}' for d in DEALERS]), fld('Sale Date', 'sd', '26/10/2026'),
            fld('Dispatch From', 'wh', 'Bhiwandi Warehouse', 'select', ['Bhiwandi Warehouse', 'Pune Warehouse']), fld('Payment Terms', 'pt', '30 days', 'select', ['Immediate', '15 days', '30 days']))}
      <section class="card flush"><header><h2>Products</h2><label class="finder" style="margin-left:auto;min-width:18rem"><i data-icon="search"></i><input type="search" placeholder="Search by name or SKU" aria-label="Search products"></label></header>
        <div class="body">{table([('Product',''), ('SKU',''), ('Dealer Price per Sheet','num'), ('Sheets',''), ('Amount','num')], [lines], 'stack-sm')}</div></section>
    </div>
    <div class="stack">
      {card('Sale Summary', kv([('Sheets', str(sum(ENTRY.values()))), ('Subtotal', M(e_sub)), ('Central GST 9%', M(e_gst)), ('State GST 9%', M(e_gst))]) + kv([('Total', M(e_total))], 'total'))}
      <section class="card"><header><h2>Dealer Credit</h2></header><div class="body">{kv([('Credit Limit', ML(b[9])), ('Owes', ML(owes)), ('This Sale', M(e_total))])}
        <span class="meter {meter_cls(used)}" style="margin-top:1rem"><i style="width:{used}%"></i></span>
        {kv([('Credit Available', ML(b[9] - owes - e_total))], 'total')}</div></section>
    </div>
  </div>
'''
page('primary', 'secondary-sales-entry', 'PRI-SAL-02', 'Primary Customer — Owner — Secondary Sales Entry (PRI-SAL-02)', body)

# ---------- Secondary Sales History ----------
cnt = lambda st: sum(1 for s in SALES if s['payment'] == st)
hist = ''.join(f'<tr><td class="mono nowrap"><b>{s["number"]}</b></td><td>{s["date"]}</td><td>{DLR[s["dealer"]][1]}</td><td class="num">{N(s["sheets"])}</td><td class="num"><b>{M(s["value"])}</b></td>'
               f'<td class="mono nowrap">{s["dispatch"]}</td><td>{pay_chip(s["payment"])}</td><td><div class="row-actions">{dl_btn("Download sale invoice")}</div></td></tr>\n' for s in SALES[:10])
body = f'''  <div class="head">
    <h1>Secondary Sales History</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Sales</button><a class="btn pri" data-link="PRI-SAL-02"><i data-icon="plus"></i>Record Sale</a></div>
  </div>
  <div class="kpis">
    {kpi('Sales This Month', ML(3120000), up('11.8%'))}
    {kpi('Sales Recorded', str(SALE_COUNT))}
    {kpi('Sheets Sold', N(2195))}
    {kpi('Awaiting Payment', ML(OWED_TOTAL))}
  </div>
  <section class="card flush">
    {tabs([('All Sales', SALE_COUNT, True), ('Paid', cnt('Paid'), False), ('Partly Paid', cnt('Partly Paid'), False), ('Unpaid', cnt('Unpaid'), False)])}
    {filters('Search by sale number or dealer', 'Search sales', ('Date Range', 'October 2026'), ('Dealer', 'All'), ('Payment', 'All'))}
    <div class="body">{table([('Sale Number',''), ('Date',''), ('Dealer',''), ('Sheets','num'), ('Value','num'), ('Dispatch Number',''), ('Payment',''), ('','')], [hist])}
      {pager(f'Showing 1 to 10 of {SALE_COUNT} sales')}</div>
  </section>
'''
page('primary', 'secondary-sales-history', 'PRI-SAL-03', 'Primary Customer — Owner — Secondary Sales History (PRI-SAL-03)', body)
