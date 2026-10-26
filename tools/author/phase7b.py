"""Phase 7, part B: Secondary Customer Sales and Inventory Manager (Arjun Nair, Dealer Bravo): Dispatch Management, Retailer Order Activity,
Retailer Performance, Pending Retailer Requests, Operational Reports. Design rule: no text under page titles, no captions beside card titles,
no helper sentences. Data: docs/DATA.md "Phase 5 data", "Phase 6 data" and "Phase 7 data"."""
from data import *

SQ = chr(0x2212)
def growth(a, b):
    v = (a - b) / b * 100
    return f'<span class="delta {"up" if v >= 0 else "down"}"><i data-icon="trend"></i>{abs(v):.1f}%</span>'
def rl(k): return link("SEC-RTL-02", RTL[k][1])
def rcnt(st): return sum(1 for s in TSALES if s['fstatus'] == st)
def ach_meter(a): return f'<span class="inline-meter"><span class="meter {"ok" if a >= 100 else "warn" if a >= 95 else "bad"}"><i style="width:{min(a, 100):.0f}%"></i></span><b>{a:.1f}%</b></span>'
VEH_USE = {v[0]: sum(1 for s in TSALES if s['vehicle'][0] == v[0]) for v in BVEHICLES}
assert sum(VEH_USE.values()) == 12

# ---------- Dispatch Management ----------
del_rows = ''.join(f'<tr><td class="mono nowrap"><b>{s["delivery"]}</b></td><td>{rl(s["retailer"])}</td><td class="num">{N(s["sheets"])}</td><td>{s["dispatched"]}</td><td>{s["expected"]}</td>'
                   f'<td>{s["delivered"] or "—"}</td><td class="nowrap">{s["vehicle"][0]}</td><td>{chip(s["fstatus"])}</td></tr>' for s in TSALES)
today_status = {s['vehicle'][0]: s for s in TSALES if s['fstatus'] != 'Delivered'}
veh_rows = ''
for v in BVEHICLES:
    cur = today_status.get(v[0])
    veh_rows += (f'<tr><td class="nowrap"><b>{v[0]}</b></td><td>{v[1]}</td><td class="nowrap">{v[2]}</td><td class="nowrap">{v[3]}</td><td class="num">{VEH_USE[v[0]]}</td>'
                 f'<td>{chip(cur["fstatus"]) if cur else chip("Available", "ok")}</td></tr>')
assert set(today_status) == {v[0] for v in BVEHICLES}
await_rows = (f'<tr><td class="mono nowrap"><b>{PEND_ORDER["number"]}</b></td><td>{rl("CHR")}</td><td class="num">{N(PEND_SHEETS)}</td><td>{PEND_ORDER["requested"]}</td><td>{chip("Awaiting Confirmation")}</td>'
              f'<td><div class="row-actions"><button class="btn sm" type="button">Reject</button><button class="btn sm pri" type="button">Confirm Order</button></div></td></tr>')
body = f'''  <div class="head">
    <h1>Dispatch Management</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Deliveries</button></div>
  </div>
  <div class="kpis">
    {kpi('Being Packed', str(rcnt('Being Packed')), chip('Dispatch Today', 'warn'))}
    {kpi('In Transit', str(rcnt('In Transit')), chip('Arriving Today', 'blue'))}
    {kpi('Delivered This Month', str(rcnt('Delivered')), chip(f'of {len(TSALES)} deliveries', 'plain'))}
    {kpi('On-Time Deliveries', f'{len(R_ONTIME) / len(R_DELIVERED) * 100:.1f}%', '<span class="delta down">2 Late</span>')}
  </div>
  <section class="card flush"><header><h2>Awaiting Confirmation</h2></header>
    <div class="body">{table([('Order Number', ''), ('Retailer', ''), ('Sheets', 'num'), ('Delivery Requested', ''), ('Status', ''), ('', '')], [await_rows], 'wrap')}</div></section>
  <section class="card flush"><header><h2>Vehicles</h2></header>
    <div class="body">{table([('Vehicle', ''), ('Type', ''), ('Driver', ''), ('Driver Phone', ''), ('Deliveries This Month', 'num'), ('Today', '')], [veh_rows], 'wrap')}</div></section>
  <section class="card flush"><header><h2>Deliveries to Retailers</h2></header>
    {tabs([('All Deliveries', len(TSALES), True), ('Being Packed', rcnt('Being Packed'), False), ('In Transit', rcnt('In Transit'), False), ('Delivered', rcnt('Delivered'), False)])}
    {filters('Search by delivery number or retailer', 'Search deliveries', ('Date Range', 'October 2026'), ('Retailer', 'All'), ('Vehicle', 'All'))}
    <div class="body">{table([('Delivery Number', ''), ('Retailer', ''), ('Sheets', 'num'), ('Dispatched', ''), ('Expected', ''), ('Delivered', ''), ('Vehicle', ''), ('Status', '')], [del_rows], 'wrap')}
      {pager(f'Showing 1 to {len(TSALES)} of {len(TSALES)} deliveries', 1)}</div></section>
'''
page('secondary', 'dispatch-management', 'SEC-DSP-01', 'Secondary Customer — Sales and Inventory Manager — Dispatch Management (SEC-DSP-01)', body)

# ---------- Retailer Order Activity ----------
act_rows = (f'<tr><td class="mono nowrap"><b>{PEND_ORDER["number"]}</b></td><td>{PEND_ORDER["date"]}</td><td>{rl("CHR")}</td><td class="num">{N(PEND_SHEETS)}</td><td class="num"><b>{M(PEND_TOTAL)}</b></td><td>{chip("Awaiting Confirmation")}</td><td>{pay_chip("Unpaid")}</td></tr>'
            + ''.join(f'<tr><td class="mono nowrap"><b>{s["number"]}</b></td><td>{s["date"]}</td><td>{rl(s["retailer"])}</td><td class="num">{N(s["sheets"])}</td><td class="num"><b>{M(s["value"])}</b></td><td>{chip(s["fstatus"])}</td><td>{pay_chip(s["payment"])}</td></tr>' for s in TSALES))
by_ret = sorted(RETAILERS, key=lambda r: -sum(1 for s in TSALES if s['retailer'] == r[0]))
mx = max(sum(1 for s in TSALES if s['retailer'] == r[0]) for r in RETAILERS)
ret_list = ''.join(f'<li><div class="grow"><div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap"><b>{r[1]}</b><span class="tag">{r[3]}</span></div><span class="meter" style="margin-top:.625rem"><i style="width:{sum(1 for s in TSALES if s["retailer"] == r[0]) / mx * 100:.0f}%"></i></span></div><b>{sum(1 for s in TSALES if s["retailer"] == r[0])}</b></li>' for r in by_ret)
body = f'''  <div class="head">
    <h1>Retailer Order Activity</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Orders</button></div>
  </div>
  <div class="kpis">
    {kpi('Confirmed Orders', str(len(TSALES)))}
    {kpi('Order Value', ML(630000), up(pct(630000, 600000)))}
    {kpi('Awaiting Confirmation', '1', chip(ML(PEND_TOTAL), 'warn'))}
    {kpi('Awaiting Dispatch', str(rcnt('Being Packed')), chip('Being Packed', 'warn'))}
  </div>
  <div class="grid g-main-side" style="--side:26rem">
    {card('Order Value by Week', chart('bars', [w[0] for w in WEEKS], [{'name': 'Order value', 'values': RWEEK_VALUE, 'color': 'var(--teal)'}], money=True, height=210))}
    {card('Orders by Retailer', f'<ul class="list">{ret_list}</ul>')}
  </div>
  <section class="card flush">
    {tabs([('All Orders', len(TSALES) + 1, True), ('Awaiting Confirmation', 1, False), ('Being Packed', rcnt('Being Packed'), False), ('In Transit', rcnt('In Transit'), False), ('Delivered', rcnt('Delivered'), False)])}
    {filters('Search by order number or retailer', 'Search retailer orders', ('Date Range', 'October 2026'), ('Retailer', 'All'), ('Payment', 'All'))}
    <div class="body">{table([('Order Number', ''), ('Date', ''), ('Retailer', ''), ('Sheets', 'num'), ('Value', 'num'), ('Fulfilment', ''), ('Payment', '')], [act_rows])}
      {pager(f'Showing 1 to {len(TSALES) + 1} of {len(TSALES) + 1} orders', 1)}</div>
  </section>
'''
page('secondary', 'retailer-order-activity', 'SEC-RTL-04', 'Secondary Customer — Sales and Inventory Manager — Retailer Order Activity (SEC-RTL-04)', body)

# ---------- Retailer Performance ----------
rank = sorted(RETAILERS, key=lambda r: -r[9][-1])
perf_rows = ''
for n, r in enumerate(rank, 1):
    k = r[0]
    perf_rows += (f'<tr><td class="num">{n}</td><td>{rl(k)}</td><td>{r[2]}</td><td class="num"><b>{M(r[9][-1])}</b></td><td>{growth(r[9][-1], r[8])}</td>'
              f'<td class="num">{M(RTARGET[k])}</td><td>{ach_meter(r_ach(k))}</td><td>{chip(r_status(k))}</td></tr>')
above = sum(1 for k in RTL if r_ach(k) >= 100)
assert above == 1 and round(630000 / RTARGET_TOTAL * 100, 1) == 98.4
body = f'''  <div class="head">
    <h1>Retailer Performance</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Export Performance</button></div>
  </div>
  <div class="kpis">
    {kpi('Sales This Month', ML(630000), up(pct(630000, 600000)))}
    {kpi('Sales Target', ML(RTARGET_TOTAL))}
    {kpi('Target Achievement', f'{630000 / RTARGET_TOTAL * 100:.1f}%', chip('Near Target', 'warn'))}
    {kpi('Retailers Above Target', f'{above} <small>of 3</small>')}
  </div>
  <div class="grid g-2">
    {card('Sales Against Target by Retailer', chart('bars', [r[1].replace('Retailer ', '') for r in rank], [{'name': 'Sales', 'values': [r[9][-1] for r in rank], 'color': 'var(--accent)'}, {'name': 'Target', 'values': [RTARGET[r[0]] for r in rank], 'color': '#c9ccd3'}], money=True, height=300))}
    {card('Sales by Month', chart('bars', MONTHS, [{'name': r[1], 'values': r[9], 'color': c} for r, c in zip(RETAILERS, ('var(--accent)', 'var(--teal)', '#e0a030'))], money=True, height=300))}
  </div>
  <section class="card flush"><header><h2>Retailers Ranked by Sales</h2><a class="more" data-link="SEC-RTL-01">Retailer network</a></header>
    <div class="body">{table([('Rank', 'num'), ('Retailer', ''), ('Area', ''), ('Sales This Month', 'num'), ('Growth Over September', ''), ('Sales Target', 'num'), ('Target Achievement', ''), ('Status', '')], [perf_rows], 'wrap',
      foot=f'<tfoot><tr><td colspan="3">Total</td><td class="num">{M(630000)}</td><td></td><td class="num">{M(RTARGET_TOTAL)}</td><td colspan="2"></td></tr></tfoot>')}</div></section>
'''
page('secondary', 'retailer-performance', 'SEC-RTL-05', 'Secondary Customer — Sales and Inventory Manager — Retailer Performance (SEC-RTL-05)', body)

# ---------- Pending Retailer Requests ----------
def req_actions(r):
    if r[9] == 'Awaiting Your Review':
        return '<div class="row-actions"><button class="btn sm" type="button">Reject</button><button class="btn sm pri" type="button">Approve</button></div>'
    return f'<div class="row-actions">{chip(r[9])}</div>'
req_rows = ''.join(f'<tr><td class="mono nowrap"><b>{r[0]}</b></td><td><b>{r[1]}</b> <span class="tag">{r[2]}</span></td><td>{r[4]}</td><td>{r[5]}</td><td class="num">{M(r[6])}</td><td class="num">{N(r[7])}</td>'
                   f'<td>{chip(f"{r[8]} of 3", "ok" if r[8] == 3 else "warn")}</td><td>{req_actions(r)}</td></tr>' for r in RREQUESTS)
body = f'''  <div class="head">
    <h1>Pending Retailer Requests</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Requests</button></div>
  </div>
  <div class="kpis">
    {kpi('Pending Requests', str(len(RREQUESTS)))}
    {kpi('Awaiting Your Review', '2', chip('Decision needed', 'warn'))}
    {kpi('Sent to Distributor Alpha', '1', chip('Kavita Joshi', 'blue'))}
    {kpi('Requested Credit', ML(sum(r[6] for r in RREQUESTS)))}
  </div>
  <section class="card flush">
    {tabs([('All Pending', len(RREQUESTS), True), ('Awaiting Your Review', 2, False), ('Sent to Distributor Alpha', 1, False)])}
    {filters('Search by retailer name or area', 'Search retailer requests', ('Area', 'All'), ('Submitted', 'Last 30 days'))}
    <div class="body">{table([('Request Number', ''), ('Retailer', ''), ('Owner', ''), ('Submitted', ''), ('Requested Credit', 'num'), ('Sheets per Month', 'num'), ('Documents', ''), ('Decision', '')], [req_rows], 'wrap')}
      {pager('Showing 1 to 3 of 3 requests', 1)}</div>
  </section>
'''
page('secondary', 'pending-retailer-requests', 'SEC-RTL-06', 'Secondary Customer — Sales and Inventory Manager — Pending Retailer Requests (SEC-RTL-06)', body)

# ---------- Operational Reports ----------
wk_on = [sum(1 for s in R_ONTIME if a <= int(s['dispatched'][:2]) <= b) for _, a, b in WEEKS]
wk_late = [sum(1 for s in R_DELIVERED if s not in R_ONTIME and a <= int(s['dispatched'][:2]) <= b) for _, a, b in WEEKS]
assert sum(wk_on) == 8 and sum(wk_late) == 2
tl_rows = ''
for r in RETAILERS:
    k = r[0]; d = [s for s in R_DELIVERED if s['retailer'] == k]; on = [s for s in d if s in R_ONTIME]
    rate = len(on) / len(d) * 100; avg = sum(R_DAYS[s['number']] for s in d) / len(d)
    tl_rows += (f'<tr><td>{rl(k)}</td><td class="num">{len(d)}</td><td class="num">{len(on)}</td><td class="num">{len(d) - len(on) or "—"}</td>'
                f'<td><span class="inline-meter"><span class="meter {"ok" if rate >= 90 else "warn" if rate >= 70 else "bad"}"><i style="width:{rate:.0f}%"></i></span><b>{rate:.1f}%</b></span></td><td class="num">{avg:.1f}</td></tr>')
late_rows = ''.join(f'<tr><td class="mono nowrap"><b>{s["delivery"]}</b></td><td>{rl(s["retailer"])}</td><td>{s["expected"]}</td><td>{s["delivered"]}</td><td class="num"><b>{(pd(s["delivered"]) - pd(s["expected"])).days}</b></td></tr>' for s in R_DELIVERED if s not in R_ONTIME)
cnt_rows = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num">{N(v[0])}</td><td class="num">{N(v[1])}</td>'
                   f'<td class="num"><b>{"+" if v[1] > v[0] else SQ if v[1] < v[0] else ""}{abs(v[1] - v[0]) or "0"}</b></td><td>{chip("Matched", "ok") if v[0] == v[1] else chip("Corrected", "warn")}</td></tr>' for s, v in BCOUNT.items())
ret_rows = ''.join(f'<tr><td>{link("SEC-RET-01", r[0])}</td><td>{r[1]}</td><td class="mono nowrap">{r[2]}</td><td>{BY[r[3]][1]}</td><td class="num">{r[4]}</td><td>{r[5]}</td><td>{chip(r[6], {"Credit Issued": "ok", "Approved": "blue", "Under Review": "warn", "Rejected": "bad"}[r[6]])}</td></tr>' for r in BRET)
ret_sheets = sum(r[4] for r in BRET); ret_rate = ret_sheets / 480 * 100
assert (ret_sheets, round(ret_rate, 1), sum(BCREDIT.values())) == (20, 4.2, 8255)
body = f'''  <div class="head">
    <h1>Operational Reports</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="download"></i>Download Report</button></div>
  </div>
  <div class="kpis">
    {kpi('On-Time Delivery', f'{len(R_ONTIME) / len(R_DELIVERED) * 100:.1f}%', chip(f'{len(R_ONTIME)} of {len(R_DELIVERED)} deliveries', 'plain'))}
    {kpi('Average Order to Delivery Time', f'{R_AVG_DAYS:.1f} <small>days</small>')}
    {kpi('Stock Count Accuracy', f'{B_COUNT_ACC:.1f}%', chip('2 Corrections', 'warn'))}
    {kpi('Return Rate to Distributor Alpha', f'{ret_rate:.1f}%', chip(f'{ret_sheets} sheets', 'plain'))}
  </div>
  {card('Deliveries by Dispatch Week', chart('bars', [w[0] for w in WEEKS], [{'name': 'On time', 'values': wk_on, 'color': 'var(--ok)'}, {'name': 'Late', 'values': wk_late, 'color': '#e0a030'}], height=240))}
  <section class="card flush"><header><h2>Late Deliveries</h2></header><div class="body">{table([('Delivery Number', ''), ('Retailer', ''), ('Expected', ''), ('Delivered', ''), ('Days Late', 'num')], [late_rows])}</div></section>
  <section class="card flush"><header><h2>Delivery Timeliness by Retailer</h2></header>
    <div class="body">{table([('Retailer', ''), ('Deliveries', 'num'), ('On Time', 'num'), ('Late', 'num'), ('On-Time Rate', ''), ('Average Days to Deliver', 'num')], [tl_rows],
      foot=f'<tfoot><tr><td>Total</td><td class="num">{len(R_DELIVERED)}</td><td class="num">{len(R_ONTIME)}</td><td class="num">{len(R_DELIVERED) - len(R_ONTIME)}</td><td class="num">{len(R_ONTIME) / len(R_DELIVERED) * 100:.1f}%</td><td class="num">{R_AVG_DAYS:.1f}</td></tr></tfoot>')}</div></section>
  <section class="card flush"><header><h2>Stock Count of {COUNT_DATE}</h2><a class="more" data-link="SEC-INV-04">Stock movement history</a></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('System Count', 'num'), ('Physical Count', 'num'), ('Difference', 'num'), ('Result', '')], [cnt_rows],
      foot=f'<tfoot><tr><td colspan="2">Total</td><td class="num">{N(B_COUNT_SYSTEM)}</td><td class="num">{N(sum(v[1] for v in BCOUNT.values()))}</td><td class="num">{SQ}1</td><td>Accuracy {B_COUNT_ACC:.1f}%</td></tr></tfoot>')}</div></section>
  <section class="card flush"><header><h2>Returns to Distributor Alpha</h2><a class="more" data-link="SEC-RET-01">Return requests</a></header>
    <div class="body">{table([('Return Request', ''), ('Date', ''), ('Order', ''), ('Product', ''), ('Sheets', 'num'), ('Reason', ''), ('Status', '')], [ret_rows],
      foot=f'<tfoot><tr><td colspan="4">Total</td><td class="num">{ret_sheets}</td><td>Credit Issued</td><td class="num">{M(sum(BCREDIT.values()))}</td></tr></tfoot>')}</div></section>
'''
page('secondary', 'operational-reports', 'SEC-RPT-03', 'Secondary Customer — Sales and Inventory Manager — Operational Reports (SEC-RPT-03)', body)
