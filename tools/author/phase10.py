"""Phase 10: Tertiary Customer Sales Executive (Dashboard, Low Stock Overview, Recent Transactions) and Inventory and Purchasing Executive (Dashboard, Incoming Deliveries).
Retailer Charlie, Camp, Pune; supplier Dealer Bravo. Links stay inside what each role can open. Design rule: no text under page titles, no captions beside card titles,
no helper sentences. Data: docs/DATA.md "Phase 8 data", "Phase 9 data", "Phase 10 data"."""
from data import *

SQ = chr(0x2212)
def prod_cell(s, sid=None):
    name = f'<a data-link="{sid}"><b>{BY[s][1]}</b></a>' if sid else f'<b>{BY[s][1]}</b>'
    return f'<div class="prod">{sw(s)}<div>{name}</div></div>'
def cover_text(s):
    c = c_cover(s); return '—' if c is None else str(round(c))
PAYMODES = ['Cash', 'Card', 'Bank Transfer', 'Cheque']
TODAY_S = [s for s in CSALES if s['day'] == 26]
T_VALUE = sum(s['total'] for s in TODAY_S); T_SHEETS = sum(s['sheets'] for s in TODAY_S)
assert (len(TODAY_S), T_VALUE, T_SHEETS, T_VALUE // len(TODAY_S) * len(TODAY_S)) == (3, 17541, 10, T_VALUE) and [s['number'] for s in TODAY_S] == ['RSL-2026-0398', 'RSL-2026-0397', 'RSL-2026-0396']
DAYS7 = list(range(20, 27))
DAY_VALUE = [sum(s['total'] for s in CSALES if s['day'] == d) for d in DAYS7]
assert DAY_VALUE == [14360, 3422, 15020, 6584, 17180, 0, 17541] and sum(DAY_VALUE) == sum(s['total'] for s in CSALES if s['day'] >= 20)
N7 = sum(1 for s in CSALES if s['day'] >= 20)
INCOMING = [(O12['number'], O12['delivery'], O12['sheets'], O12['value'], O12['expected'], 'Being Packed', O12['lines']),
            (PEND_ORDER['number'], '—', PEND_SHEETS, PEND_TOTAL, PEND_ORDER['requested'], 'Awaiting Confirmation', PEND_ORDER['lines'])]
assert sum(i[2] for i in INCOMING) == 100 == sum(b['on_order'] for b in CSTOCK.values())
VALUE_ARRIVING = sum(i[3] for i in INCOMING); assert VALUE_ARRIVING == 166784
fin_col = {'Matte': '#0a48fd', 'Woodgrain': '#0b8fa8', 'Texture': '#7a36fb', 'Gloss': '#e0a030', 'Suede': '#0c9b6a', 'High Gloss': '#d43a2f', 'Metallic': '#8b93a3'}
URGENT = sorted(CSTOCK, key=lambda s: (CREC[s]['action'] == 'No Order Needed', CSTOCK[s]['status'] != 'Out of Stock', c_cover(s) if c_cover(s) is not None else 0))
ORDER_NOW = [s for s in URGENT if CREC[s]['action'] != 'No Order Needed']; assert len(ORDER_NOW) == 4
LOWS = sorted(CLOW, key=lambda s: (CSTOCK[s]['status'] != 'Out of Stock', CSTOCK[s]['available'] / CSTOCK[s]['level']))
def tx_rows(sales, links=True):
    return ''.join(f'<tr><td class="mono nowrap"><a data-link="TER-RTS-03"><b>{s["number"]}</b></a></td><td class="nowrap">{s["date"]} {s["time"]}</td><td>{s["customer"]}</td><td class="num">{N(s["sheets"])}</td><td class="num"><b>{M(s["total"])}</b></td><td>{chip(s["pay"], "plain")}</td></tr>' for s in sales)

# ---------- Sales Executive Dashboard ----------
top = sorted((s for s in CSOLD if CSOLD[s]), key=lambda s: -CSOLD[s])[:5]
top_rows = ''.join(f'<li>{sw(s, "", "width:2.5rem;height:2.5rem;flex:none")}<div class="grow"><b>{BY[s][1]}</b><span class="meter" style="margin-top:.5rem"><i style="width:{CSOLD[s] / CSOLD[top[0]] * 100:.0f}%"></i></span></div><b>{N(CSOLD[s])}</b></li>' for s in top)
low_rows = ''.join(f'<tr><td>{prod_cell(s, "TER-INV-02")}</td><td class="mono nowrap">{s}</td><td class="num"><b>{N(CSTOCK[s]["available"])}</b></td><td class="num">{N(CSTOCK[s]["level"])}</td><td>{chip(CSTOCK[s]["status"])}</td></tr>' for s in LOWS)
body = f'''  <div class="head">
    <h1>Dashboard</h1>
    <div class="acts"><span class="sel"><small>Day</small> 26 October 2026 <i data-icon="down"></i></span><a class="btn" data-link="TER-RTS-04">Recent Transactions</a><a class="btn pri" data-link="TER-RTS-01"><i data-icon="plus"></i>Record Retail Sale</a></div>
  </div>
  <div class="kpis">
    {kpi('Sales Today', M(T_VALUE), chip(f'{len(TODAY_S)} sales', 'blue'))}
    {kpi('Sheets Sold Today', f'{T_SHEETS} <small>sheets</small>')}
    {kpi('Sales This Month', ML(CRETAIL_OCT), chip(f'{len(CSALES)} sales', 'plain'))}
    {kpi('Products Running Low', str(len(CLOW)), '<span class="delta down">1 Out of Stock</span>')}
  </div>
  <div class="grid g-main-side" style="--side:22rem">
    {card('Sales in the Last 7 Days', chart('bars', [f'{d} October' for d in DAYS7], [{'name': 'Sales', 'values': DAY_VALUE, 'color': 'var(--teal)'}], money=True, height=340))}
    <section class="card"><header><h2>Best Selling Products This Month</h2></header><div class="body"><ul class="list">{top_rows}</ul>{kv([('Sheets Sold', N(163))], 'total')}</div></section>
  </div>
  <div class="stack">
    <section class="card flush"><header><h2>Recent Transactions</h2><a class="more" data-link="TER-RTS-04">All transactions</a></header>
      <div class="body">{table([('Sale Number', ''), ('Date and Time', ''), ('Customer', ''), ('Sheets', 'num'), ('Value', 'num'), ('Payment Mode', '')], [tx_rows(CSALES[:6])], 'wrap')}</div></section>
    <section class="card flush"><header><h2>Products Running Low</h2><a class="more" data-link="TER-INV-05">Low stock overview</a></header>
      <div class="body">{table([('Product', ''), ('SKU', ''), ('Available', 'num'), ('Reorder Level', 'num'), ('Status', '')], [low_rows], 'wrap tight')}</div></section>
  </div>
'''
page('tertiary', 'sales-executive-dashboard', 'TER-SLS-01', 'Tertiary Customer — Sales Executive — Dashboard (TER-SLS-01)', body)

# ---------- Low Stock Overview (Sales Executive) ----------
ARRIVE = {s: [] for s in CSTOCK}
for _no, _dl, _sh, _v, _exp, _st, _lines in INCOMING:
    for k, q in _lines: ARRIVE[k].append((q, _exp))
assert sum(q for k in CLOW for q, _ in ARRIVE[k]) == 21
def arrive_text(s): return '<br>'.join(f'{q} on {e}' for q, e in ARRIVE[s]) or '—'
low_tbl = ''.join(f'<tr><td>{prod_cell(s, "TER-INV-02")}</td><td class="mono nowrap">{s}</td><td class="num"><b>{N(CSTOCK[s]["available"])}</b></td><td class="num">{N(CSTOCK[s]["level"])}</td>'
                  f'<td class="num">{N(CSTOCK[s]["on_order"]) if CSTOCK[s]["on_order"] else "—"}</td><td class="nowrap">{arrive_text(s)}</td><td class="num">{cover_text(s)}</td><td>{chip(CSTOCK[s]["status"])}</td></tr>\n' for s in LOWS)
body = f'''  <div class="head">
    <h1>Low Stock Overview</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Low Stock</button><a class="btn pri" data-link="TER-INV-01"><i data-icon="stack"></i>My Inventory</a></div>
  </div>
  <div class="kpis">
    {kpi('Products Below Reorder Level', str(len(CLOW)), chip('3 Low Stock', 'warn'))}
    {kpi('Out of Stock', '1', '<span class="delta down">LM-STN-009</span>')}
    {kpi('Sheets Short of Reorder Level', N(CSHORT))}
    {kpi('Sheets on Order', f'{N(sum(CSTOCK[s]["on_order"] for s in CLOW))} <small>sheets</small>')}
  </div>
  {card('Available Sheets Against Reorder Level', chart('bars', LOWS, [{'name': 'Available', 'values': [CSTOCK[s]['available'] for s in LOWS], 'color': 'var(--accent)'}, {'name': 'Reorder level', 'values': [CSTOCK[s]['level'] for s in LOWS], 'color': 'var(--bad)'}], height=230))}
  <section class="card flush">
    {tabs([('All Products', len(CLOW), True), ('Low Stock', 3, False), ('Out of Stock', 1, False)])}
    {filters('Search by product name or SKU', 'Search low stock products', ('Finish', 'All'), ('Sort by', 'Urgency'))}
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Available', 'num'), ('Reorder Level', 'num'), ('On Order', 'num'), ('Arriving', ''), ('Days of Cover', 'num'), ('Status', '')], [low_tbl], 'wrap')}</div>
  </section>
'''
page('tertiary', 'low-stock-overview', 'TER-INV-05', 'Tertiary Customer — Sales Executive — Low Stock Overview (TER-INV-05)', body)

# ---------- Recent Transactions (Sales Executive) ----------
def sku_tags(s): return ''.join('<span class="tag mono">' + k + '</span>' for k, _ in s['lines'])
tx = ''.join(f'<tr><td class="mono nowrap"><a data-link="TER-RTS-03"><b>{s["number"]}</b></a></td><td class="nowrap">{s["date"]} {s["time"]}</td><td>{s["customer"]}</td>'
             f'<td><div style="display:flex;flex-wrap:wrap;gap:.25rem">{sku_tags(s)}</div></td>'
             f'<td class="num">{N(s["sheets"])}</td><td class="num"><b>{M(s["total"])}</b></td><td>{chip(s["pay"], "plain")}</td><td class="nowrap">{s["by"]}</td></tr>\n' for s in CSALES[:12])
body = f'''  <div class="head">
    <h1>Recent Transactions</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Transactions</button><a class="btn pri" data-link="TER-RTS-01"><i data-icon="plus"></i>Record Retail Sale</a></div>
  </div>
  <div class="kpis">
    {kpi('Sales Today', M(T_VALUE), chip(f'{len(TODAY_S)} sales', 'blue'))}
    {kpi('Sheets Sold Today', f'{T_SHEETS} <small>sheets</small>')}
    {kpi('Average Sale Today', M(T_VALUE // len(TODAY_S)))}
    {kpi('Last Sale Today', TODAY_S[0]['time'], chip(TODAY_S[0]['number'], 'plain'))}
  </div>
  <section class="card flush">
    {tabs([('Latest Sales', 12, True), ('Today', len(TODAY_S), False), ('Last 7 Days', N7, False)])}
    {filters('Search by sale number, customer or product', 'Search transactions', ('Payment Mode', 'All'), ('Recorded By', 'All'))}
    <div class="body">{table([('Sale Number', ''), ('Date and Time', ''), ('Customer', ''), ('Items', ''), ('Sheets', 'num'), ('Value', 'num'), ('Payment Mode', ''), ('Recorded By', '')], [tx], 'wrap')}
      {pager(f'Showing 1 to 12 of {len(CSALES)} sales', 4)}</div>
  </section>
'''
page('tertiary', 'recent-transactions', 'TER-RTS-04', 'Tertiary Customer — Sales Executive — Recent Transactions (TER-RTS-04)', body)

# ---------- Inventory and Purchasing Executive Dashboard ----------
recent = ''.join(f'<tr><td><a data-link="TER-ORD-02"><b>{o}</b></a></td><td>{d}</td><td class="num">{N(sh)}</td><td class="num"><b>{M(v)}</b></td><td>{chip(st)}</td></tr>' for o, d, sh, v, dl, st, pay in CHR_ORDERS[:6])
inc_rows = ''.join(f'<tr><td><a data-link="TER-ORD-02"><b>{i[0]}</b></a></td><td class="mono nowrap">{i[1]}</td><td class="num">{N(i[2])}</td><td>{i[4]}</td><td>{chip(i[5])}</td></tr>' for i in INCOMING)
rec_rows = ''.join(f'<tr><td>{prod_cell(s, "TER-INV-02")}</td><td class="mono nowrap">{s}</td><td class="num"><b>{N(CSTOCK[s]["available"])}</b></td><td class="num">{N(CSTOCK[s]["level"])}</td><td class="num">{N(CREC[s]["qty"]) if CREC[s]["qty"] else "—"}</td><td>{chip(CREC[s]["action"])}</td></tr>' for s in ORDER_NOW)
n_in = sum(1 for b in CSTOCK.values() if b['status'] == 'In Stock')
body = f'''  <div class="head">
    <h1>Dashboard</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><a class="btn pri" data-link="TER-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Incoming Deliveries', str(len(INCOMING)), chip('1 Arriving Tomorrow', 'blue'))}
    {kpi('Products to Reorder', str(sum(1 for r in CREC.values() if r['action'] == 'Order Now')), '<span class="delta down">1 Not Available</span>')}
    {kpi('Suggested Order Value', ML(CREC_VALUE), chip('Before GST', 'plain'))}
    {kpi('Orders This Month', '5', chip(ML(264000), 'plain'))}
  </div>
  <div class="grid g-chart">
    {card('Purchases by Month', chart('bars', MONTHS, [{'name': 'Purchases from Dealer Bravo', 'values': CHR_BUY_MONTH, 'color': 'var(--accent)'}], money=True, height=280))}
    <section class="card"><header><h2>Stock Health</h2></header><div class="body center">{chart('donut', series=[{'name': 'In Stock', 'value': n_in, 'color': 'var(--ok)'}, {'name': 'Low Stock', 'value': 3, 'color': '#e0a030'}, {'name': 'Out of Stock', 'value': 1, 'color': 'var(--bad)'}], center='12', caption='products')}</div></section>
  </div>
  <div class="stack">
    <section class="card flush"><header><h2>Recent Orders</h2><a class="more" data-link="TER-ORD-01">All orders</a></header>
      <div class="body">{table([('Order Number', ''), ('Date', ''), ('Sheets', 'num'), ('Value', 'num'), ('Status', '')], [recent], 'wrap')}</div></section>
    <section class="card flush"><header><h2>Incoming Deliveries</h2><a class="more" data-link="TER-INV-06">All deliveries</a></header>
      <div class="body">{table([('Order', ''), ('Delivery', ''), ('Sheets', 'num'), ('Expected', ''), ('Status', '')], [inc_rows], 'wrap')}</div></section>
  </div>
  <section class="card flush"><header><h2>Reorder Suggestions</h2><a class="more" data-link="TER-INV-04">All recommendations</a></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Available', 'num'), ('Reorder Level', 'num'), ('Suggested Quantity', 'num'), ('Action', '')], [rec_rows], 'wrap')}</div></section>
'''
page('tertiary', 'inventory-and-purchasing-executive-dashboard', 'TER-PUR-01', 'Tertiary Customer — Inventory and Purchasing Executive — Dashboard (TER-PUR-01)', body)

# ---------- Incoming Deliveries (Inventory and Purchasing Executive) ----------
ship_rows = ''.join(f'<tr><td><a data-link="TER-ORD-02"><b>{i[0]}</b></a></td><td class="mono nowrap">{i[1]}</td><td class="num">{N(i[2])}</td><td class="num"><b>{M(i[3])}</b></td><td>{i[4]}</td><td>{chip(i[5])}</td></tr>' for i in INCOMING)
arr_prod = ''
for s in CSTOCK:
    b = CSTOCK[s]
    if not b['on_order']: continue
    a12 = dict(INCOMING[0][6]).get(s, 0); a13 = dict(INCOMING[1][6]).get(s, 0); after = b['available'] + b['on_order']
    assert a12 + a13 == b['on_order']
    arr_prod += (f'<tr><td>{prod_cell(s, "TER-INV-02")}</td><td class="mono nowrap">{s}</td><td class="num">{N(b["available"])}</td><td class="num">{N(a12) if a12 else "—"}</td><td class="num">{N(a13) if a13 else "—"}</td>'
                 f'<td class="num"><b>{N(after)}</b></td><td>{chip("In Stock" if after >= b["level"] else "Low Stock")}</td></tr>')
rec_hist = ''.join(f'<tr><td><a data-link="TER-ORD-02"><b>{s["number"]}</b></a></td><td>{s["delivered"]}</td><td class="num">{N(s["sheets"])}</td><td class="num">{M(s["value"])}</td></tr>' for s in CHR_TS if s['fstatus'] == 'Delivered')
assert [s['delivered'] for s in CHR_TS if s['fstatus'] == 'Delivered'] == ['20/10/2026', '13/10/2026', '08/10/2026', '02/10/2026']
v = O12['vehicle']
body = f'''  <div class="head">
    <h1>Incoming Deliveries</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Deliveries</button><a class="btn pri" data-link="TER-ORD-03"><i data-icon="plus"></i>Place Order</a></div>
  </div>
  <div class="kpis">
    {kpi('Deliveries Arriving', str(len(INCOMING)))}
    {kpi('Sheets Arriving', f'{N(100)} <small>sheets</small>')}
    {kpi('Arriving Tomorrow', f'{O12["sheets"]} <small>sheets</small>', chip(O12['delivery'], 'blue'))}
    {kpi('Value Arriving', ML(VALUE_ARRIVING), chip('GST Included', 'plain'))}
  </div>
  <section class="card flush"><header><h2>Deliveries From Dealer Bravo</h2></header>
    <div class="body">{table([('Order Number', ''), ('Delivery Number', ''), ('Sheets', 'num'), ('Value', 'num'), ('Expected Arrival', ''), ('Status', '')], [ship_rows], 'wrap')}</div></section>
  <section class="card flush"><header><h2>Arriving by Product</h2></header>
    <div class="body">{table([('Product', ''), ('SKU', ''), ('Available Now', 'num'), ('Arriving 27 October', 'num'), ('Arriving 28 October', 'num'), ('Available After Both', 'num'), ('Status After Arrival', '')], [arr_prod], 'wrap',
      foot=f'<tfoot><tr><td colspan="3">Total</td><td class="num">{N(O12["sheets"])}</td><td class="num">{N(PEND_SHEETS)}</td><td colspan="2"></td></tr></tfoot>')}</div></section>
  <div class="grid g-2">
    {card('Arriving Tomorrow', kv([('Order Number', f'<span class="mono">{O12["number"]}</span>'), ('Delivery Number', f'<span class="mono">{O12["delivery"]}</span>'), ('Dispatched From', 'Hadapsar Godown'), ('Deliver To', 'Shop 12, MG Road, Camp, Pune'),
                                    ('Vehicle', v[0]), ('Driver', v[2]), ('Driver Phone', v[3])]))}
    <section class="card flush"><header><h2>Recent Receipts</h2></header><div class="body">{table([('Order Number', ''), ('Received', ''), ('Sheets', 'num'), ('Value', 'num')], [rec_hist])}</div></section>
  </div>
'''
page('tertiary', 'incoming-deliveries', 'TER-INV-06', 'Tertiary Customer — Inventory and Purchasing Executive — Incoming Deliveries (TER-INV-06)', body)
