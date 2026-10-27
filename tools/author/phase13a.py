"""Phase 13, part A: Company Administration, Sales Manager: Dashboard, Distributor, Dealer and Retailer Performance, Sales Targets, Regional Sales Analysis,
Product Sales Analysis, Customer Sales History, Sales Order Overview, Promotional Campaigns. Links go only to screens the Sales Manager can open.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md "Phase 11", "Phase 12" and "Phase 13 data"."""
from data import *

SQ = chr(0x2212)
STATUS_CHIP.update({'Fast Mover': 'ok', 'Slow Mover': 'warn', 'Steady': 'plain', 'No Sales': 'bad'})
def meter_ach(a): return f'<span class="inline-meter"><span class="meter {"ok" if a >= 100 else "warn" if a >= 95 else "bad"}"><i style="width:{min(a, 100):.0f}%"></i></span><b>{a:.1f}%</b></span>'
def nm(n): return f'<b>{n}</b>'
RET_NAME = {r[0]: r[1] for r in RETAILERS}; RET_NAME.update({r[0]: r[1] for r in NEW_RETAILERS})
RET_DEALER = {r[0]: 'Dealer Bravo' for r in RETAILERS}; RET_DEALER.update({r[0]: DLR[r[6]][1] for r in NEW_RETAILERS})
RET_CITY = {r[0]: r[3] for r in RETAILERS}; RET_CITY.update({r[0]: r[3] for r in NEW_RETAILERS})
AWAIT = [o for o in IN_PROGRESS if o[7] == 'Awaiting Confirmation']

# ---------- Dashboard ----------
below = sorted([(achievement(d[0]), d[1], 'Dealer') for d in DEALERS if achievement(d[0]) < 95] + [(rt_ach(k), RET_NAME[k], 'Retailer') for k in RTARGET_ALL if rt_status(k) == 'Below Target'])[:4]
att_rows = f'<tr><td>{link("CMP-CUS-03", "Dealer Omkar")}</td><td>{chip("Waiting for Decision")}</td><td class="num">{DAYS_WAITING} days</td></tr>'
att_rows += ''.join(f'<tr><td>{nm(n)}</td><td>{chip("Below Target")}</td><td class="num">{a:.1f}% of target</td></tr>' for a, n, t in below)
aw_rows = ''.join(f'<tr><td class="mono nowrap"><b>{o[0]}</b></td><td>{o[1]}</td><td>{o[3]}</td><td class="num"><b>{M(o[6])}</b></td></tr>' for o in AWAIT)
top = sorted(SOLD, key=lambda s: -SOLD[s])[:5]
top_rows = ''.join(f'<li>{sw(s, "", "width:2.5rem;height:2.5rem;flex:none")}<div class="grow"><b>{BY[s][1]}</b><span class="meter" style="margin-top:.5rem"><i style="width:{SOLD[s] / SOLD[top[0]] * 100:.0f}%"></i></span></div><b>{N(SOLD[s])}</b></li>' for s in top)
body = f'''  <div class="head">
    <h1>Dashboard</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><a class="btn" data-link="CMP-SAL-05">Sales Targets</a><a class="btn pri" data-link="CMP-SAL-09">Sales Order Overview</a></div>
  </div>
  <div class="kpis">
    {kpi('Sales to Dealers', ML(3120000), up('11.8%'))}
    {kpi('Target Achievement', f'{3120000 / TARGET_TOTAL * 100:.1f}%', chip('Near Target', 'warn'))}
    {kpi('Orders by Distributors', ML(PURCH_MONTH[-1]), up(pct(PURCH_MONTH[-1], PURCH_MONTH[-2])))}
    {kpi('Orders Awaiting Confirmation', str(len(AWAIT)), chip(ML(sum(o[6] for o in AWAIT)), 'warn'))}
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    {card('Sales Against Target by Territory', chart('bars', [t['name'] for t in TERRITORIES], [{'name': 'Sales to dealers', 'values': [t['sales'] for t in TERRITORIES], 'color': 'var(--accent)'}, {'name': 'Target', 'values': [t['target'] for t in TERRITORIES], 'color': '#c9ccd3'}], money=True, height=330))}
    {card('Top Products by Sheets', f'<ul class="list">{top_rows}</ul>')}
  </div>
  <div class="grid g-2">
    <section class="card flush"><header><h2>Customers Needing Attention</h2></header><div class="body">{table([('Customer', ''), ('Reason', ''), ('Detail', 'num')], [att_rows], 'wrap')}</div></section>
    <section class="card flush"><header><h2>Orders Awaiting Confirmation</h2><a class="more" data-link="CMP-SAL-09">All orders in progress</a></header><div class="body">{table([('Order Number', ''), ('Tier', ''), ('Buyer', ''), ('Value', 'num')], [aw_rows], 'wrap')}</div></section>
  </div>
'''
page('company', 'sales-manager-dashboard', 'CMP-SAL-01', 'Company Administration — Sales Manager — Dashboard (CMP-SAL-01)', body)

# ---------- Distributor Performance ----------
a = achievement  # dealer targets add up to the distributor's target
dist_rows = (f'<tr><td class="num">1</td><td>{nm("Distributor Alpha")}</td><td>Bhiwandi</td><td class="num"><b>{M(PURCH_MONTH[-1])}</b></td><td>{change(PURCH_MONTH[-1], PURCH_MONTH[-2])}</td><td class="num"><b>{M(3120000)}</b></td>'
             f'<td class="num">{M(TARGET_TOTAL)}</td><td>{meter_ach(3120000 / TARGET_TOTAL * 100)}</td><td>{chip("Near Target")}</td></tr>')
body = f'''  <div class="head">
    <h1>Distributor Performance</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Performance</button></div>
  </div>
  <div class="kpis">
    {kpi('Orders by Distributors', ML(PURCH_MONTH[-1]), up(pct(PURCH_MONTH[-1], PURCH_MONTH[-2])))}
    {kpi('Sales to Dealers', ML(3120000), up('11.8%'))}
    {kpi('Sales Target', ML(TARGET_TOTAL))}
    {kpi('Target Achievement', f'{3120000 / TARGET_TOTAL * 100:.1f}%', chip('Near Target', 'warn'))}
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    {card('Orders and Sales to Dealers by Month', chart('bars', MONTHS, [{'name': 'Orders by distributors', 'values': PURCH_MONTH, 'color': 'var(--accent)'}, {'name': 'Sales to dealers', 'values': SALES_MONTH, 'color': 'var(--teal)'}], money=True, height=300))}
    {card('Distributor Alpha', kv([('Customer Code', '<span class="mono">CUS-0018</span>'), ('Territory', 'Maharashtra and Goa'), ('Dealers', '8'), ('Retailers', '20'), ('Credit Limit', ML(CREDIT_LIMIT)), ('Credit Used', '37%'), ('Account Manager', 'Vikram Chopra')]))}
  </div>
  <section class="card flush"><header><h2>Distributors Ranked by Orders</h2></header>
    <div class="body">{table([('Rank', 'num'), ('Distributor', ''), ('City', ''), ('Orders This Month', 'num'), ('Growth Over September', ''), ('Sales to Dealers', 'num'), ('Sales Target', 'num'), ('Target Achievement', ''), ('Status', '')], [dist_rows], 'wrap')}</div></section>
'''
page('company', 'distributor-performance', 'CMP-SAL-02', 'Company Administration — Sales Manager — Distributor Performance (CMP-SAL-02)', body)

# ---------- Dealer Performance ----------
rank = sorted(DEALERS, key=lambda d: -d[7])
perf_rows = ''.join(f'<tr><td class="num">{n}</td><td>{nm(d[1])}</td><td>{d[2]}</td><td class="num">{d[6]}</td><td class="num"><b>{M(d[7])}</b></td><td>{change(d[7], d[8])}</td><td class="num">{M(TARGET[d[0]])}</td><td>{meter_ach(achievement(d[0]))}</td><td>{chip(perf_status(d[0]))}</td></tr>' for n, d in enumerate(rank, 1))
above = sum(1 for d in DEALERS if achievement(d[0]) >= 100); assert above == 4
body = f'''  <div class="head">
    <h1>Dealer Performance</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Performance</button></div>
  </div>
  <div class="kpis">
    {kpi('Sales to Dealers', ML(3120000), up('11.8%'))}
    {kpi('Sales Target', ML(TARGET_TOTAL))}
    {kpi('Target Achievement', f'{3120000 / TARGET_TOTAL * 100:.1f}%', chip('Near Target', 'warn'))}
    {kpi('Dealers Above Target', f'{above} <small>of 8</small>')}
  </div>
  {card('Sales Against Target by Dealer', chart('bars', [d[1] for d in rank], [{'name': 'Sales', 'values': [d[7] for d in rank], 'color': 'var(--accent)'}, {'name': 'Target', 'values': [TARGET[d[0]] for d in rank], 'color': '#c9ccd3'}], money=True, height=300))}
  <section class="card flush"><header><h2>Dealers Ranked by Sales</h2></header>
    <div class="body">{table([('Rank', 'num'), ('Dealer', ''), ('City', ''), ('Retailers', 'num'), ('Sales This Month', 'num'), ('Growth Over September', ''), ('Sales Target', 'num'), ('Target Achievement', ''), ('Status', '')], [perf_rows], 'wrap',
      foot=f'<tfoot><tr><td colspan="4">Total</td><td class="num">{M(3120000)}</td><td></td><td class="num">{M(TARGET_TOTAL)}</td><td colspan="2"></td></tr></tfoot>')}</div></section>
'''
page('company', 'dealer-performance', 'CMP-SAL-03', 'Company Administration — Sales Manager — Dealer Performance (CMP-SAL-03)', body)

# ---------- Retailer Performance ----------
rrank = sorted(RTARGET_ALL, key=lambda k: -RETAIL_OCT[k])
rrows = ''.join(f'<tr><td class="num">{n}</td><td>{nm(RET_NAME[k])}</td><td>{RET_DEALER[k]}</td><td>{RET_CITY[k]}</td><td class="num"><b>{M(RETAIL_OCT[k])}</b></td><td>{change(RETAIL_OCT[k], RETAIL_SEPT_PURCH[k])}</td>'
                f'<td class="num">{M(RTARGET_ALL[k])}</td><td>{meter_ach(rt_ach(k))}</td><td>{chip(rt_status(k))}</td></tr>' for n, k in enumerate(rrank, 1))
body = f'''  <div class="head">
    <h1>Retailer Performance</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Performance</button></div>
  </div>
  <div class="kpis">
    {kpi('Sales to Retailers', ML(2800000), up(pct(2800000, 2540000)))}
    {kpi('Sales Target', ML(RT_TARGET_TOTAL))}
    {kpi('Target Achievement', f'{2800000 / RT_TARGET_TOTAL * 100:.1f}%', chip('Near Target', 'warn'))}
    {kpi('Retailers Above Target', f'{RT_STATUS_COUNT["Above Target"]} <small>of 20</small>')}
  </div>
  {card('Sales Against Target, Top Ten Retailers', chart('bars', [RET_NAME[k] for k in rrank[:10]], [{'name': 'Sales', 'values': [RETAIL_OCT[k] for k in rrank[:10]], 'color': '#7a36fb'}, {'name': 'Target', 'values': [RTARGET_ALL[k] for k in rrank[:10]], 'color': '#c9ccd3'}], money=True, height=320))}
  <section class="card flush"><header><h2>Retailers Ranked by Sales</h2></header>
    <div class="body">{table([('Rank', 'num'), ('Retailer', ''), ('Dealer', ''), ('City', ''), ('Sales This Month', 'num'), ('Growth Over September', ''), ('Sales Target', 'num'), ('Target Achievement', ''), ('Status', '')], [rrows], 'wrap',
      foot=f'<tfoot><tr><td colspan="4">Total</td><td class="num">{M(2800000)}</td><td></td><td class="num">{M(RT_TARGET_TOTAL)}</td><td colspan="2"></td></tr></tfoot>')}</div></section>
'''
page('company', 'retailer-performance', 'CMP-SAL-04', 'Company Administration — Sales Manager — Retailer Performance (CMP-SAL-04)', body)

# ---------- Sales Targets ----------
q_rows = ''.join(f'<tr><td><b>{n}</b></td><td class="num">{M(t)}</td><td class="num"><b>{M(act) if act else "—"}</b></td><td>{meter_ach(act / t * 100) if act else "—"}</td></tr>' for n, t, act, st in QUARTERS)
t_rows = ''.join(f'<tr><td><b>{t["name"]}</b></td><td class="num">{t["dealers"]}</td><td class="num"><b>{M(t["sales"])}</b></td><td class="num">{M(t["target"])}</td><td>{meter_ach(t["sales"] / t["target"] * 100)}</td><td class="num">{M(t["sales"] - t["target"]) if t["sales"] >= t["target"] else SQ + M(t["target"] - t["sales"])}</td></tr>' for t in TERRITORIES)
d_rows = ''.join(f'<tr><td>{nm(d[1])}</td><td>{d[3]}</td><td class="num"><b>{M(d[7])}</b></td><td class="num">{M(TARGET[d[0]])}</td><td>{meter_ach(achievement(d[0]))}</td><td>{chip(perf_status(d[0]))}</td></tr>' for d in sorted(DEALERS, key=lambda d: -achievement(d[0])))
gap = TARGET_TOTAL - 3120000; assert gap == 20000
body = f'''  <div class="head">
    <h1>Sales Targets</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Targets</button><button class="btn pri" type="button"><i data-icon="edit"></i>Set Targets</button></div>
  </div>
  <div class="kpis">
    {kpi('October Target', ML(TARGET_TOTAL))}
    {kpi('Sales to Dealers', ML(3120000), up('11.8%'))}
    {kpi('Target Achievement', f'{3120000 / TARGET_TOTAL * 100:.1f}%', chip('Near Target', 'warn'))}
    {kpi('Short of Target', M(gap))}
  </div>
  <div class="grid g-2" style="--cols:.8fr 1.2fr">
    {card('Sales Against Target by Quarter', chart('bars', [q[0].split(' (')[0] for q in QUARTERS], [{'name': 'Sales to dealers', 'values': [q[2] for q in QUARTERS], 'color': 'var(--accent)'}, {'name': 'Target', 'values': [q[1] for q in QUARTERS], 'color': '#c9ccd3'}], money=True, height=260))}
    <section class="card flush"><header><h2>Quarters of Financial Year 2026–27</h2></header><div class="body">{table([('Quarter', ''), ('Target', 'num'), ('Sales to Dealers', 'num'), ('Achievement', '')], [q_rows], 'wrap')}</div></section>
  </div>
  <section class="card flush"><header><h2>Targets by Territory</h2></header><div class="body">{table([('Territory', ''), ('Dealers', 'num'), ('Sales to Dealers', 'num'), ('Target', 'num'), ('Achievement', ''), ('Difference', 'num')], [t_rows], 'wrap',
      foot=f'<tfoot><tr><td>Total</td><td class="num">8</td><td class="num">{M(3120000)}</td><td class="num">{M(TARGET_TOTAL)}</td><td></td><td class="num">{SQ}{M(gap)}</td></tr></tfoot>')}</div></section>
  <section class="card flush"><header><h2>Targets by Dealer</h2></header><div class="body">{table([('Dealer', ''), ('Territory', ''), ('Sales to Dealers', 'num'), ('Target', 'num'), ('Achievement', ''), ('Status', '')], [d_rows], 'wrap')}</div></section>
'''
page('company', 'sales-targets', 'CMP-SAL-05', 'Company Administration — Sales Manager — Sales Targets (CMP-SAL-05)', body)

# ---------- Regional Sales Analysis ----------
by_city = sorted(DEALERS, key=lambda d: -d[7])
c_rows = ''.join(f'<tr><td><b>{d[2]}</b></td><td>{STATE(d)}</td><td>{d[3]}</td><td>{d[1]}</td><td class="num"><b>{M(d[7])}</b></td><td class="num">{M(d[8]) if d[8] else "—"}</td><td>{change(d[7], d[8])}</td><td>{share_cell(d[7], 3120000, by_city[0][7])}</td></tr>' for d in by_city)
s_rows = ''.join(f'<tr><td><b>{st}</b></td><td class="num">{sum(1 for d in DEALERS if STATE(d) == st)}</td><td class="num"><b>{M(v[0])}</b></td><td class="num">{M(v[1]) if v[1] else "—"}</td><td>{change(v[0], v[1])}</td><td>{share_cell(v[0], 3120000, STATE_SALES["Maharashtra"][0])}</td></tr>' for st, v in STATE_SALES.items())
body = f'''  <div class="head">
    <h1>Regional Sales Analysis</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><span class="sel"><small>Compared With</small> September 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button></div>
  </div>
  <div class="kpis">
    {kpi('Sales to Dealers', ML(3120000), up('11.8%'))}
    {kpi('Maharashtra', ML(STATE_SALES['Maharashtra'][0]), up(pct(*STATE_SALES['Maharashtra'])))}
    {kpi('Goa', ML(STATE_SALES['Goa'][0]), chip('New', 'blue'))}
    {kpi('Cities', str(len(DEALERS)))}
  </div>
  {card('Sales to Dealers by City', chart('bars', [d[2] for d in by_city], [{'name': 'October', 'values': [d[7] for d in by_city], 'color': 'var(--accent)'}, {'name': 'September', 'values': [d[8] for d in by_city], 'color': '#c9ccd3'}], money=True, height=300))}
  <section class="card flush"><header><h2>Sales by State</h2></header><div class="body">{table([('State', ''), ('Dealers', 'num'), ('October', 'num'), ('September', 'num'), ('Change', ''), ('Share of Sales', '')], [s_rows], 'wrap')}</div></section>
  <section class="card flush"><header><h2>Sales by City</h2></header><div class="body">{table([('City', ''), ('State', ''), ('Territory', ''), ('Dealer', ''), ('October', 'num'), ('September', 'num'), ('Change', ''), ('Share of Sales', '')], [c_rows], 'wrap')}</div></section>
'''
page('company', 'regional-sales-analysis', 'CMP-SAL-06', 'Company Administration — Sales Manager — Regional Sales Analysis (CMP-SAL-06)', body)

# ---------- Product Sales Analysis ----------
def mover(s): return 'No Sales' if not SOLD[s] else 'Fast Mover' if SOLD[s] >= 250 else 'Slow Mover' if SOLD[s] < 120 else 'Steady'
assert [s for s in SOLD if mover(s) == 'Fast Mover'] == ['LM-WNT-001', 'LM-ARC-002', 'LM-SKY-012'] and sorted(s for s in SOLD if mover(s) in ('Slow Mover', 'No Sales')) == ['LM-CHR-007', 'LM-CPR-010', 'LM-SLT-005', 'LM-STN-009']
p_rows = ''.join(f'<tr><td>{prod_cell(s)}</td><td class="mono nowrap">{s}</td><td>{BY[s][2]}</td><td>{BY[s][3]}</td><td class="num">{N(SOLD[s]) if SOLD[s] else "—"}</td><td class="num"><b>{M(SOLD_VALUE[s]) if SOLD[s] else "—"}</b></td><td>{share_cell(SOLD_VALUE[s], 3120000, max(SOLD_VALUE.values()))}</td><td>{chip(mover(s))}</td></tr>' for s in sorted(SOLD, key=lambda x: -SOLD[x]))
fin_v = {}
for s, v in SOLD_VALUE.items(): fin_v[BY[s][2]] = fin_v.get(BY[s][2], 0) + v
thick = {}
for s, q in SOLD.items(): thick[BY[s][3]] = thick.get(BY[s][3], 0) + q
assert sum(thick.values()) == 2195
body = f'''  <div class="head">
    <h1>Product Sales Analysis</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Data</button></div>
  </div>
  <div class="kpis">
    {kpi('Sales to Dealers', ML(3120000), up('11.8%'))}
    {kpi('Sheets Sold', N(2195))}
    {kpi('Fast Movers', '3', chip('250 Sheets or More', 'ok'))}
    {kpi('Slow Movers', '4', chip('Under 120 Sheets', 'warn'))}
  </div>
  <div class="grid g-2">
    {card('Sales by Finish', chart('bars', list(fin_v), [{'name': 'Sales', 'values': list(fin_v.values()), 'color': 'var(--accent)'}], money=True, height=260))}
    <section class="card"><header><h2>Sheets by Thickness</h2></header><div class="body center">{chart('donut', series=[{'name': t, 'value': v, 'color': c} for (t, v), c in zip(sorted(thick.items(), key=lambda x: -x[1]), ['#0a48fd', '#0b8fa8'])], center=N(2195), caption='sheets')}</div></section>
  </div>
  <section class="card flush"><header><h2>Sales by Laminate</h2></header><div class="body">{table([('Product', ''), ('SKU', ''), ('Finish', ''), ('Thickness', ''), ('Sheets', 'num'), ('Sales', 'num'), ('Share of Sales', ''), ('Movement', '')], [p_rows], 'wrap')}</div></section>
'''
page('company', 'product-sales-analysis', 'CMP-SAL-07', 'Company Administration — Sales Manager — Product Sales Analysis (CMP-SAL-07)', body)

# ---------- Customer Sales History (Dealer Bravo) ----------
b = DLR['BRV']; bs = BRV_SALES
bprod = {}
for s in bs:
    for k, q in s['lines']: bprod[k] = bprod.get(k, 0) + q
_w = {k: q * dp(k) for k, q in bprod.items()}; bval = {k: round(b[7] * w / sum(_w.values())) for k, w in _w.items()}
bval[max(bval, key=bval.get)] += b[7] - sum(bval.values())
assert sum(bprod.values()) == 480 and sum(bval.values()) == 684000
bp_rows = ''.join(f'<tr><td>{prod_cell(k)}</td><td class="mono nowrap">{k}</td><td class="num">{N(bprod[k])}</td><td class="num"><b>{M(bval[k])}</b></td><td>{share_cell(bval[k], b[7], max(bval.values()))}</td></tr>' for k in sorted(bprod, key=lambda x: -bval[x]))
bo_rows = ''.join(f'<tr><td class="mono nowrap"><b>{s["number"]}</b></td><td>{s["date"]}</td><td class="num">{N(s["sheets"])}</td><td class="num"><b>{M(s["value"])}</b></td><td class="mono nowrap">{s["dispatch"]}</td><td>{chip(s["status"])}</td><td>{pay_chip(s["payment"])}</td></tr>' for s in bs)
body = f'''  <div class="head">
    <h1>Customer Sales History</h1>
    <div class="acts"><span class="sel"><small>Customer</small> Dealer Bravo, Pune <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export History</button></div>
  </div>
  <div class="kpis">
    {kpi('Purchases This Month', ML(b[7]), up(pct(b[7], b[8])))}
    {kpi('Orders This Month', str(len(bs)))}
    {kpi('Sheets Bought', N(DEALER_SHEETS['BRV']))}
    {kpi('Owes', ML(DEALER_OWES['BRV']), chip('2 unpaid sales', 'warn'))}
  </div>
  {card('Purchases by Month', chart('bars', MONTHS, [{'name': 'Purchases by Dealer Bravo', 'values': BRV_PURCH_MONTH, 'color': 'var(--accent)'}], money=True, height=280))}
  <section class="card flush"><header><h2>Purchases by Product</h2></header><div class="body">{table([('Product', ''), ('SKU', ''), ('Sheets', 'num'), ('Purchases', 'num'), ('Share of Purchases', '')], [bp_rows], 'wrap',
    foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">480</td><td class="num">{M(b[7])}</td><td></td></tr></tfoot>')}</div></section>
  <section class="card flush"><header><h2>Orders This Month</h2></header><div class="body">{table([('Sale Number', ''), ('Date', ''), ('Sheets', 'num'), ('Value', 'num'), ('Dispatch Number', ''), ('Fulfilment', ''), ('Payment', '')], [bo_rows], 'wrap')}</div></section>
'''
page('company', 'customer-sales-history', 'CMP-SAL-08', 'Company Administration — Sales Manager — Customer Sales History (CMP-SAL-08)', body)

# ---------- Sales Order Overview ----------
o10482 = IN_PROGRESS[0]; assert o10482[0] == 'ORD-2026-10482'
io_rows = ''.join(f'<tr><td class="mono nowrap"><b>{o[0]}</b></td><td>{o[1]}</td><td>{o[2]}</td><td>{o[3]}</td><td>{o[4]}</td><td class="num">{N(o[5])}</td><td class="num"><b>{M(o[6])}</b></td><td>{chip(o[7])}</td></tr>' for o in IN_PROGRESS)
cnt_t = lambda t: sum(1 for o in IN_PROGRESS if o[1] == t)
body = f'''  <div class="head">
    <h1>Sales Order Overview</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Orders</button></div>
  </div>
  <div class="kpis">
    {kpi('Orders in Progress', str(len(IN_PROGRESS)), chip(ML(IN_PROGRESS_VALUE), 'plain'))}
    {kpi('Awaiting Confirmation', str(len(AWAIT)), chip(ML(sum(o[6] for o in AWAIT)), 'warn'))}
    {kpi('Being Packed', str(sum(1 for o in IN_PROGRESS if o[7] == 'Being Packed')))}
    {kpi('In Transit', str(sum(1 for o in IN_PROGRESS if o[7] == 'In Transit')))}
  </div>
  <section class="card"><header><h2>Order Awaiting Your Confirmation</h2><span style="margin-left:auto">{chip('Awaiting Confirmation')}</span></header><div class="body">
    <div class="grid g-2" style="gap:2rem">
      {kv([('Order Number', f'<span class="mono">{o10482[0]}</span>'), ('Customer', 'Distributor Alpha'), ('Placed', '26/10/2026 11:42 by Rajesh Menon'), ('Sheets', '760'), ('Value', M(o10482[6])), ('Requested Delivery', '31/10/2026')])}
      {kv([('Credit Limit', ML(CREDIT_LIMIT)), ('Outstanding Balance', ML(OUTSTANDING)), ('Credit Available After', ML(CREDIT_LIMIT - OUTSTANDING - o10482[6])), ('Festive Volume Rebate', M(REBATE_10482)), ('Stock at Plant Warehouse', chip('In Stock', 'ok'))])}
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:.5rem;justify-content:flex-end;margin-top:1.25rem"><button class="btn" type="button">Hold Order</button><button class="btn pri" type="button">Confirm Order</button></div></div></section>
  <section class="card flush">
    {tabs([('All in Progress', len(IN_PROGRESS), True), ('Primary', cnt_t('Primary'), False), ('Secondary', cnt_t('Secondary'), False), ('Tertiary', cnt_t('Tertiary'), False)])}
    {filters('Search by order number or customer', 'Search orders', ('Status', 'All'), ('Tier', 'All'), ('Sort by', 'Status'))}
    <div class="body">{table([('Order Number', ''), ('Tier', ''), ('Seller', ''), ('Buyer', ''), ('Order Date', ''), ('Sheets', 'num'), ('Value', 'num'), ('Status', '')], [io_rows], 'wrap',
      foot=f'<tfoot><tr><td colspan="5">Total</td><td class="num">{N(sum(o[5] for o in IN_PROGRESS))}</td><td class="num">{M(IN_PROGRESS_VALUE)}</td><td></td></tr></tfoot>')}
      {pager(f'Showing 1 to {len(IN_PROGRESS)} of {len(IN_PROGRESS)} orders', 1)}</div>
  </section>
'''
page('company', 'sales-order-overview', 'CMP-SAL-09', 'Company Administration — Sales Manager — Sales Order Overview (CMP-SAL-09)', body)

# ---------- Promotional Campaigns ----------
cp_rows = ''.join(f'<tr><td><b>{c[1]}</b></td><td class="mono nowrap">{c[0]}</td><td>{c[2]}</td><td class="num">{c[5] if c[5] else "—"}</td><td class="num">{c[6] if c[6] else "—"}</td><td>'
                  f'{"—" if not c[8] else f"""<span class="inline-meter" style="justify-content:flex-start"><span class="meter {"warn" if c[8] / c[7] > .9 else ""}"><i style="width:{c[8] / c[7] * 100:.0f}%"></i></span><span style="white-space:nowrap"><b style="min-width:0">{M(c[8])}</b> of {M(c[7])}</span></span>"""}</td><td>{chip(c[9])}</td></tr>' for c in CAMPAIGNS)
body = f'''  <div class="head">
    <h1>Promotional Campaigns</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Campaigns</button><button class="btn pri" type="button"><i data-icon="plus"></i>Create Campaign</button></div>
  </div>
  <div class="kpis">
    {kpi('Running Campaigns', str(len(CAMP_RUNNING)))}
    {kpi('Planned Campaigns', '1')}
    {kpi('Spent on Running Campaigns', M(sum(c[8] for c in CAMP_RUNNING)))}
    {kpi('Orders Influenced This Year', str(sum(c[6] for c in CAMPAIGNS)))}
  </div>
  {card('Spent Against Budget by Campaign', chart('bars', [c[0] for c in CAMPAIGNS if c[8]], [{'name': 'Spent', 'values': [c[8] for c in CAMPAIGNS if c[8]], 'color': 'var(--accent)'}, {'name': 'Budget', 'values': [c[7] for c in CAMPAIGNS if c[8]], 'color': '#c9ccd3'}], money=True, height=260))}
  <section class="card flush">
    {tabs([('All Campaigns', len(CAMPAIGNS), True), ('Running', len(CAMP_RUNNING), False), ('Planned', 1, False), ('Completed', 2, False)])}
    <div class="body" style="margin-top:1rem">{table([('Campaign', ''), ('Campaign Number', ''), ('Audience', ''), ('Customers Reached', 'num'), ('Orders Influenced', 'num'), ('Spent Against Budget', ''), ('Status', '')], [cp_rows], 'wrap')}</div>
  </section>
'''
page('company', 'promotional-campaigns', 'CMP-SAL-10', 'Company Administration — Sales Manager — Promotional Campaigns (CMP-SAL-10)', body)
