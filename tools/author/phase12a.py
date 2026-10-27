"""Phase 12, part A: Company Administration, Super Admin: Dispatch Management and Inventory Overview (shared with the Operations Manager), Sales Analytics,
Primary, Secondary, Tertiary and Retail Sales Reports. Design rule: no text under page titles, no captions beside card titles, no helper sentences.
Data: docs/DATA.md "Phase 11 data" and "Phase 12 data"."""
from data import *

PLANT = 'Plant Warehouse, Vapi'
# ---------- Dispatch Management ----------
srows = ''.join(f'<tr><td class="mono nowrap">{link("CMP-OPS-04", s[0]) if s[0] != "—" else "—"}</td><td class="nowrap">{link("CMP-ORD-02", s[1])}</td><td>{PLANT}</td><td>{s[2]}</td>'
                f'<td class="num">{N(s[3])}</td><td>{'Planned ' + s[4] if s[6] == 'Being Packed' else s[4]}</td><td>{s[5]}</td><td>{chip(s[6])}</td></tr>' for s in SHIPMENTS)
wk_ship = [sum(s[3] for s in SHIP_OCT if a <= int(s[4][:2]) <= b) for _, a, b in WEEKS]; assert wk_ship == [400, 430, 520, 360]
trans = {}
for s in SHIPMENTS:
    if s[6] != 'Being Packed': t = trans.setdefault(s[2], [0, 0, 0]); t[0] += 1; t[1] += s[3]; t[2] += s[6] == 'In Transit'
trows = ''.join(f'<tr><td><b>{n}</b></td><td class="num">{v[0]}</td><td class="num">{N(v[1])}</td><td class="num">{v[2]}</td></tr>' for n, v in trans.items())
trans_foot = f'<tfoot><tr><td>Total</td><td class="num">{sum(v[0] for v in trans.values())}</td><td class="num">{N(sum(v[1] for v in trans.values()))}</td><td class="num">{sum(v[2] for v in trans.values())}</td></tr></tfoot>'
body = f'''  <div class="head">
    <h1>Dispatch Management</h1>
    <div class="acts"><span class="sel"><small>Warehouse</small> All Warehouses <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Shipments</button></div>
  </div>
  <div class="kpis">
    {kpi('Shipments in Transit', str(SHIP_STATUS['In Transit']), chip('Arriving 27/10/2026', 'blue'))}
    {kpi('Being Packed', str(SHIP_STATUS['Being Packed']), chip('Planned 26/10/2026', 'warn'))}
    {kpi('Dispatched This Month', str(len(SHIP_OCT)), chip(f'{N(SHIP_OCT_SHEETS)} sheets', 'plain'))}
    {kpi('Delivered On Time', f'{SHIP_STATUS["Delivered"]} of {SHIP_STATUS["Delivered"]}')}
  </div>
  <div class="grid g-chart">
    {card('Sheets Dispatched by Week', chart('bars', [w[0] for w in WEEKS], [{'name': 'Sheets dispatched', 'values': wk_ship, 'color': 'var(--teal)'}], height=260))}
    <section class="card flush"><header><h2>Shipments by Transporter</h2></header><div class="body">{table([('Transporter', ''), ('Shipments', 'num'), ('Sheets', 'num'), ('In Transit', 'num')], [trows], 'wrap', foot=trans_foot)}</div></section>
  </div>
  <section class="card flush">
    {tabs([('All Shipments', len(SHIPMENTS), True), ('Being Packed', SHIP_STATUS['Being Packed'], False), ('In Transit', SHIP_STATUS['In Transit'], False), ('Delivered', SHIP_STATUS['Delivered'], False)])}
    {filters('Search by dispatch number, order number or transporter', 'Search shipments', ('Date Range', 'Since 10/09/2026'), ('Warehouse', 'All'), ('Transporter', 'All'))}
    <div class="body">{table([('Dispatch Number', ''), ('Order Number', ''), ('Dispatched From', ''), ('Transporter', ''), ('Sheets', 'num'), ('Dispatched', ''), ('Expected Delivery', ''), ('Status', '')], [srows], 'wrap')}
      {pager(f'Showing 1 to {len(SHIPMENTS)} of {len(SHIPMENTS)} shipments', 1)}</div>
  </section>
'''
page('company', 'dispatch-management', 'CMP-DSP-01', 'Company Administration — Super Admin — Dispatch Management (CMP-DSP-01)', body)

# ---------- Inventory Overview ----------
irows = ''.join(f'<tr><td>{prod_cell(p[0], "CMP-PRD-02")}</td><td class="mono nowrap">{p[0]}</td><td class="num">{N(CSTK[p[0]]["vapi"])}</td><td class="num">{N(CSTK[p[0]]["taloja"])}</td>'
                f'<td class="num">{N(CSTK[p[0]]["reserved"]) if CSTK[p[0]]["reserved"] else "—"}</td><td class="num"><b>{N(CSTK[p[0]]["available"])}</b></td><td class="num">{N(CSTK[p[0]]["level"])}</td><td>{chip(CSTK[p[0]]["status"])}</td></tr>\n' for p in P)
ifoot = (f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(CSTK_VAPI)}</td><td class="num">{N(CSTK_TALOJA)}</td><td class="num">{N(CSTK_RESERVED)}</td><td class="num">{N(CSTK_AVAIL)}</td><td colspan="2"></td></tr></tfoot>')
vap_res = CSTK_RESERVED
wrows = (f'<tr><td><b>{WAREHOUSES[0][0]}, Vapi</b></td><td class="num">{N(CSTK_VAPI)}</td><td class="num">{N(vap_res)}</td><td class="num"><b>{N(CSTK_VAPI - vap_res)}</b></td></tr>'
         f'<tr><td><b>{WAREHOUSES[1][0]}, Taloja</b></td><td class="num">{N(CSTK_TALOJA)}</td><td class="num">0</td><td class="num"><b>{N(CSTK_TALOJA)}</b></td></tr>')
wfoot = f'<tfoot><tr><td>Total</td><td class="num">{N(CSTK_ON_HAND)}</td><td class="num">{N(CSTK_RESERVED)}</td><td class="num">{N(CSTK_AVAIL)}</td></tr></tfoot>'
body = f'''  <div class="head">
    <h1>Inventory Overview</h1>
    <div class="acts"><span class="sel"><small>Warehouse</small> All Warehouses <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Stock</button></div>
  </div>
  <div class="kpis">
    {kpi('Sheets on Hand', N(CSTK_ON_HAND))}
    {kpi('Reserved for Orders', N(CSTK_RESERVED), chip('2 orders', 'plain'))}
    {kpi('Available Sheets', N(CSTK_AVAIL))}
    {kpi('Low Stock Products', str(CSTK_COUNT['Low Stock']), '<span class="delta down">Carrara Stone Finish</span>')}
  </div>
  <div class="grid g-2" style="--cols:.8fr 1.2fr">
    <section class="card"><header><h2>Stock by Finish</h2></header><div class="body center">{chart('donut', series=[{'name': f, 'value': v, 'color': FIN_COL[f]} for f, v in sorted(CSTK_FINISH.items(), key=lambda x: -x[1])], center=N(CSTK_ON_HAND), caption='sheets')}</div></section>
    <section class="card flush"><header><h2>Stock by Warehouse</h2></header><div class="body">{table([('Warehouse', ''), ('On Hand', 'num'), ('Reserved', 'num'), ('Available', 'num')], [wrows], 'wrap', foot=wfoot)}</div></section>
  </div>
  <section class="card flush">
    {tabs([('All Products', len(P), True), ('In Stock', CSTK_COUNT['In Stock'], False), ('Low Stock', CSTK_COUNT['Low Stock'], False), ('Out of Stock', 0, False)])}
    {filters('Search by product name or SKU', 'Search stock', ('Finish', 'All'), ('Thickness', 'All'), ('Warehouse', 'All'))}
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Plant Warehouse, Vapi', 'num'), ('Regional Warehouse, Taloja', 'num'), ('Reserved', 'num'), ('Available', 'num'), ('Reorder Level', 'num'), ('Status', '')], [irows], 'wrap', foot=ifoot)}</div>
  </section>
'''
page('company', 'inventory-overview', 'CMP-INV-01', 'Company Administration — Super Admin — Inventory Overview (CMP-INV-01)', body)

# ---------- Sales Analytics ----------
OCT = dict(P=PURCH_MONTH[-1], S=3120000, T=2800000, R=RETAIL_OCT_TOTAL); SEP = dict(P=PURCH_MONTH[-2], S=2790000, T=2540000, R=RETAIL_SEPT_TOTAL)
reg_rows = ''.join(f'<tr><td><b>{t["name"]}</b></td><td class="num">{t["dealers"]}</td><td class="num">{t["retailers"]}</td><td class="num"><b>{M(t["sales"])}</b></td><td class="num">{M(t["sept"]) if t["sept"] else "—"}</td><td>{change(t["sales"], t["sept"])}</td>'
                   f'<td>{share_cell(t["sales"], 3120000, 1559000)}</td></tr>' for t in sorted(TERRITORIES, key=lambda t: -t['sales']))
assert sum(t['sept'] for t in TERRITORIES) == 2790000
tier_rows = ''.join(f'<tr><td>{prod_cell(p[0], "CMP-PRD-02")}</td><td class="mono nowrap">{p[0]}</td><td class="num">{N(BOUGHT.get(p[0], 0)) if BOUGHT.get(p[0], 0) else "—"}</td><td class="num">{N(SOLD[p[0]]) if SOLD[p[0]] else "—"}</td>'
                    f'<td class="num">{N(NET_TSOLD[p[0]]) if NET_TSOLD[p[0]] else "—"}</td><td class="num">{N(NET_RSOLD[p[0]]) if NET_RSOLD[p[0]] else "—"}</td></tr>' for p in P)
tier_foot = f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(sum(BOUGHT.values()))}</td><td class="num">{N(2195)}</td><td class="num">{N(NET_TERT_SHEETS)}</td><td class="num">{N(NET_RSHEETS)}</td></tr></tfoot>'
body = f'''  <div class="head">
    <h1>Sales Analytics</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><span class="sel"><small>Compared With</small> September 2026 <i data-icon="down"></i></span><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('Orders by Distributors', ML(OCT['P']), up(pct(OCT['P'], SEP['P'])))}
    {kpi('Sales to Dealers', ML(OCT['S']), up(pct(OCT['S'], SEP['S'])))}
    {kpi('Sales to Retailers', ML(OCT['T']), up(pct(OCT['T'], SEP['T'])))}
    {kpi('Sales to Customers', ML(OCT['R']), up(pct(OCT['R'], SEP['R'])))}
  </div>
  {card('Sales by Month', chart('bars', MONTHS, [{'name': 'Orders by distributors', 'values': PURCH_MONTH, 'color': 'var(--accent)'}, {'name': 'Sales to dealers', 'values': SALES_MONTH, 'color': 'var(--teal)'},
        {'name': 'Sales to retailers', 'values': NET_TERT_MONTH, 'color': '#7a36fb'}, {'name': 'Sales to customers', 'values': NET_RETAIL_MONTH, 'color': '#e0a030'}], money=True, height=320))}
  <section class="card flush"><header><h2>Sales by Territory</h2><a class="more" data-link="CMP-TER-01">Territory management</a></header>
    <div class="body">{table([('Territory', ''), ('Dealers', 'num'), ('Retailers', 'num'), ('Sales to Dealers', 'num'), ('September', 'num'), ('Change', ''), ('Share of Sales', '')], [reg_rows], 'wrap')}</div></section>
  <section class="card flush"><header><h2>Sheets by Product and Tier</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Ordered by Distributors', 'num'), ('Sold to Dealers', 'num'), ('Sold to Retailers', 'num'), ('Sold to Customers', 'num')], [tier_rows], 'wrap', foot=tier_foot)}</div></section>
'''
page('company', 'sales-analytics', 'CMP-ANL-01', 'Company Administration — Super Admin — Sales Analytics (CMP-ANL-01)', body)

# ---------- Primary Sales Report (Crestline to distributors) ----------
fin_b = {}
for s, q in BOUGHT.items(): fin_b[BY[s][2]] = fin_b.get(BY[s][2], 0) + q
fin_bv = {}
for s, v in BOUGHT_VALUE.items(): fin_bv[BY[s][2]] = fin_bv.get(BY[s][2], 0) + v
dist_rows = (f'<tr><td>{link("CMP-CUS-02", "Distributor Alpha")}</td><td>Bhiwandi</td><td>Maharashtra and Goa</td><td class="num">6</td><td class="num">{N(2750)}</td><td class="num"><b>{M(PURCH_MONTH[-1])}</b></td>'
             f'<td class="num">{M(PURCH_MONTH[-2])}</td><td>{change(PURCH_MONTH[-1], PURCH_MONTH[-2])}</td></tr>')
pr = ''.join(f'<tr><td>{prod_cell(s, "CMP-PRD-02")}</td><td class="mono nowrap">{s}</td><td class="num">{N(BOUGHT[s])}</td><td class="num"><b>{M(BOUGHT_VALUE[s])}</b></td><td>{share_cell(BOUGHT_VALUE[s], PURCH_MONTH[-1], max(BOUGHT_VALUE.values()))}</td></tr>' for s in sorted((k for k in BOUGHT if BOUGHT[k]), key=lambda k: -BOUGHT_VALUE[k]))
body = f'''  <div class="head">
    <h1>Primary Sales Report</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><span class="sel"><small>Compared With</small> September 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('Order Value', ML(PURCH_MONTH[-1]), up(pct(PURCH_MONTH[-1], PURCH_MONTH[-2])))}
    {kpi('Sheets Ordered', N(2750), chip('6 orders', 'plain'))}
    {kpi('Invoiced', ML(INV_ISSUED_OCT), chip('4 invoices', 'plain'))}
    {kpi('Payments Received', ML(sum(p[2] for p in PAID_OCT)), chip('5 payments', 'plain'))}
  </div>
  <div class="grid g-2">
    {card('Order Value by Month', chart('bars', MONTHS, [{'name': 'Orders from distributors', 'values': PURCH_MONTH, 'color': 'var(--accent)'}], money=True, height=260))}
    <section class="card"><header><h2>Sheets Ordered by Finish</h2></header><div class="body center">{chart('donut', series=[{'name': f, 'value': v, 'color': FIN_COL[f]} for f, v in sorted(fin_b.items(), key=lambda x: -x[1])], center=N(2750), caption='sheets')}</div></section>
  </div>
  <section class="card flush"><header><h2>Sales by Distributor</h2></header>
    <div class="body">{table([('Distributor', ''), ('City', ''), ('Territory', ''), ('Orders', 'num'), ('Sheets', 'num'), ('Order Value', 'num'), ('September', 'num'), ('Change', '')], [dist_rows], 'wrap')}</div></section>
  <section class="card flush"><header><h2>Sales by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Order Value', 'num'), ('Share of Order Value', '')], [pr], 'wrap')}</div></section>
'''
page('company', 'primary-sales-report', 'CMP-RPT-01', 'Company Administration — Super Admin — Primary Sales Report (CMP-RPT-01)', body)

# ---------- Secondary Sales Report (distributors to dealers) ----------
fin_val = {}
for s_, v in SOLD_VALUE.items(): fin_val[BY[s_][2]] = fin_val.get(BY[s_][2], 0) + v
dr = ''.join(f'<tr><td>{link("CMP-CUS-02", dd[1])}</td><td>{dd[2]}</td><td>{dd[3]}</td><td class="num">{N(DEALER_SHEETS[dd[0]])}</td><td class="num"><b>{M(dd[7])}</b></td><td class="num">{M(dd[8]) if dd[8] else "—"}</td><td>{change(dd[7], dd[8])}</td></tr>' for dd in sorted(DEALERS, key=lambda x: -x[7]))
pr = ''.join(f'<tr><td>{prod_cell(s_, "CMP-PRD-02")}</td><td class="mono nowrap">{s_}</td><td class="num">{N(SOLD[s_])}</td><td class="num"><b>{M(SOLD_VALUE[s_])}</b></td><td>{share_cell(SOLD_VALUE[s_], 3120000, max(SOLD_VALUE.values()))}</td></tr>' for s_ in sorted(SOLD, key=lambda x: -SOLD_VALUE[x]))
body = f'''  <div class="head">
    <h1>Secondary Sales Report</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><span class="sel"><small>Compared With</small> September 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('Sales to Dealers', ML(3120000), up('11.8%'))}
    {kpi('Sheets Sold', N(2195))}
    {kpi('Sales Recorded', str(SALE_COUNT))}
    {kpi('Active Dealers', '8', chip('1 New', 'blue'))}
  </div>
  <div class="grid g-2">
    {card('Sales by Finish', chart('bars', list(fin_val), [{'name': 'Sales', 'values': list(fin_val.values()), 'color': 'var(--accent)'}], money=True, height=260))}
    <section class="card"><header><h2>Sales by Territory</h2></header><div class="body center">{chart('donut', series=[{'name': r, 'value': v, 'color': REG_COL[r]} for r, v in sorted(REGION_SALES.items(), key=lambda x: -x[1])], center='5', caption='territories')}</div></section>
  </div>
  <section class="card flush"><header><h2>Sales by Dealer</h2></header>
    <div class="body">{table([('Dealer', ''), ('City', ''), ('Territory', ''), ('Sheets', 'num'), ('Sales', 'num'), ('September', 'num'), ('Change', '')], [dr], 'wrap')}</div></section>
  <section class="card flush"><header><h2>Sales by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Sales', 'num'), ('Share of Sales', '')], [pr], 'wrap')}</div></section>
'''
page('company', 'secondary-sales-report', 'CMP-RPT-02', 'Company Administration — Super Admin — Secondary Sales Report (CMP-RPT-02)', body)

# ---------- Tertiary and Retail Sales Reports (by retailer and product) ----------
ALL_RTL = [(r[0], r[1], r[3], r[2], 'BRV' if r[0] in ('CHR', 'KIR', 'MEH') else None) for r in RETAILERS] + [(r[0], r[1], r[3], r[2], r[6]) for r in NEW_RETAILERS]
ALL_RTL = [(k, n, c, DLR[par or next(x[6] for x in NEW_RETAILERS if x[0] == k)][1], c) for k, n, c, _a, par in ALL_RTL]
def store_rows(oct_, sept_, key):
    rows = ''
    for k, n, city, dealer, _c in sorted(ALL_RTL, key=lambda r: -oct_[r[0]]):
        sp = sept_[k]
        rows += f'<tr><td>{link("CMP-CUS-02", n)}</td><td>{dealer}</td><td>{city}</td><td class="num"><b>{M(oct_[k])}</b></td><td class="num">{M(sp) if sp else "—"}</td><td>{change(oct_[k], sp)}</td></tr>'
    return rows
dealer_t = {DLR[k][1]: DEALER_RETAIL[k] for k in DLR}
rp_rows = ''.join(f'<tr><td>{prod_cell(s, "CMP-PRD-02")}</td><td class="mono nowrap">{s}</td><td class="num">{N(NET_TSOLD[s])}</td><td class="num"><b>{M(NET_TSOLD_VALUE[s])}</b></td><td>{share_cell(NET_TSOLD_VALUE[s], 2800000, max(NET_TSOLD_VALUE.values()))}</td></tr>' for s in sorted((k for k in NET_TSOLD if NET_TSOLD[k]), key=lambda k: -NET_TSOLD_VALUE[k]))
body = f'''  <div class="head">
    <h1>Tertiary Sales Report</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><span class="sel"><small>Compared With</small> September 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('Sales to Retailers', ML(2800000), up(pct(2800000, 2540000)))}
    {kpi('Sheets Sold', N(NET_TERT_SHEETS))}
    {kpi('Orders Recorded', str(sum(TERTIARY_COUNT.values())))}
    {kpi('Retailers Buying', str(len(ALL_RTL)), chip('1 New', 'blue'))}
  </div>
  <div class="grid g-2">
    {card('Sales to Retailers by Month', chart('bars', MONTHS, [{'name': 'Sales to retailers', 'values': NET_TERT_MONTH, 'color': '#7a36fb'}], money=True, height=260))}
    <section class="card"><header><h2>Sales by Dealer</h2></header><div class="body center">{chart('donut', series=[{'name': n, 'value': v, 'color': c} for (n, v), c in zip(sorted(dealer_t.items(), key=lambda x: -x[1]), ['#0a48fd', '#0b8fa8', '#7a36fb', '#e0a030', '#0c9b6a', '#d43a2f', '#8b93a3', '#3d4366'])], center='8', caption='dealers')}</div></section>
  </div>
  <section class="card flush"><header><h2>Sales by Retailer</h2></header>
    <div class="body">{table([('Retailer', ''), ('Dealer', ''), ('City', ''), ('Sales', 'num'), ('September', 'num'), ('Change', '')], [store_rows(RETAIL_OCT, RETAIL_SEPT_PURCH, 't')], 'wrap',
      foot=f'<tfoot><tr><td colspan="3">Total</td><td class="num">{M(2800000)}</td><td class="num">{M(2540000)}</td><td></td></tr></tfoot>')}</div></section>
  <section class="card flush"><header><h2>Sales by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Sales', 'num'), ('Share of Sales', '')], [rp_rows], 'wrap')}</div></section>
'''
page('company', 'tertiary-sales-report', 'CMP-RPT-03', 'Company Administration — Super Admin — Tertiary Sales Report (CMP-RPT-03)', body)

reg_ret = {}
for k, n, city, dealer, _c in ALL_RTL:
    dk = next(d[0] for d in DEALERS if d[1] == dealer); reg_ret[DLR[dk][3]] = reg_ret.get(DLR[dk][3], 0) + RETAIL_SALES_OCT[k]
assert sum(reg_ret.values()) == RETAIL_OCT_TOTAL
rr_rows = ''.join(f'<tr><td>{prod_cell(s, "CMP-PRD-02")}</td><td class="mono nowrap">{s}</td><td class="num">{N(NET_RSOLD[s])}</td><td class="num"><b>{M(NET_RSOLD_VALUE[s])}</b></td><td>{share_cell(NET_RSOLD_VALUE[s], RETAIL_OCT_TOTAL, max(NET_RSOLD_VALUE.values()))}</td></tr>' for s in sorted((k for k in NET_RSOLD if NET_RSOLD[k]), key=lambda k: -NET_RSOLD_VALUE[k]))
body = f'''  <div class="head">
    <h1>Retail Sales Report</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><span class="sel"><small>Compared With</small> September 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button><button class="btn pri" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('Sales to Customers', ML(RETAIL_OCT_TOTAL), up(pct(RETAIL_OCT_TOTAL, RETAIL_SEPT_TOTAL)))}
    {kpi('Sheets Sold', N(NET_RSHEETS))}
    {kpi('Stores Selling', str(len(ALL_RTL)))}
    {kpi('Average Sales per Store', ML(RETAIL_OCT_TOTAL // len(ALL_RTL)))}
  </div>
  <div class="grid g-2">
    {card('Sales to Customers by Month', chart('bars', MONTHS, [{'name': 'Sales to customers', 'values': NET_RETAIL_MONTH, 'color': '#e0a030'}], money=True, height=260))}
    <section class="card"><header><h2>Sales by Territory</h2></header><div class="body center">{chart('donut', series=[{'name': r, 'value': v, 'color': REG_COL[r]} for r, v in sorted(reg_ret.items(), key=lambda x: -x[1])], center='5', caption='territories')}</div></section>
  </div>
  <section class="card flush"><header><h2>Sales by Store</h2></header>
    <div class="body">{table([('Store', ''), ('Dealer', ''), ('City', ''), ('Sales', 'num'), ('September', 'num'), ('Change', '')], [store_rows(RETAIL_SALES_OCT, RETAIL_SALES_SEPT, 'r')], 'wrap',
      foot=f'<tfoot><tr><td colspan="3">Total</td><td class="num">{M(RETAIL_OCT_TOTAL)}</td><td class="num">{M(RETAIL_SEPT_TOTAL)}</td><td></td></tr></tfoot>')}</div></section>
  <section class="card flush"><header><h2>Sales by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Sales', 'num'), ('Share of Sales', '')], [rr_rows], 'wrap')}</div></section>
'''
page('company', 'retail-sales-report', 'CMP-RPT-04', 'Company Administration — Super Admin — Retail Sales Report (CMP-RPT-04)', body)
