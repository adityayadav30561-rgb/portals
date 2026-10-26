"""Authoring aid (not needed to run the prototype): shared data and helpers for generating screen HTML.
Values come from docs/DATA.md. The generator scripts are the SOURCE for the screens they write: change the script and
run it again; never hand-edit a generated screen (it would be overwritten). Run from tools/author: python3 phase2a.py"""
import json, os

def M(n):
    """Money with Indian digit grouping: 949752 -> ₹9,49,752"""
    s = str(int(round(n)))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        s = ','.join(parts) + ',' + tail
    return '₹' + s

def ML(n):
    """Compact money with full words, for stat tiles, charts and summaries: 3352882 -> ₹33.53 lakh (halves round up)"""
    from decimal import Decimal, ROUND_HALF_UP
    q = lambda v: Decimal(v).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    if n >= 10000000: return f'\u20b9{q(Decimal(n) / 10000000)} crore'
    if n >= 100000: return f'\u20b9{q(Decimal(n) / 100000)} lakh'
    return M(n)

def N(n):
    return f'{int(n):,}'

# sku, name, finish, thickness, slabs, kind, colour, gloss, on_hand, reserved, available, on_order, reorder, status
P = [
 ('LM-WNT-001','Walnut Woodgrain Laminate','Woodgrain','1.0 mm',(1180,1140,1095),'wood','#5a3a22',False,1240,310,930,600,400,'In Stock'),
 ('LM-ARC-002','Arctic White Matte Laminate','Matte','1.0 mm',(940,905,870),'plain','#f3f5f7',False,1860,420,1440,0,500,'In Stock'),
 ('LM-CAL-003','Calacatta Marble Finish Laminate','High Gloss','1.0 mm',(1560,1510,1450),'marble','#eceeef',True,215,90,125,300,250,'Low Stock'),
 ('LM-OAK-004','Natural Oak Texture Laminate','Texture','1.0 mm',(1240,1200,1150),'wood','#b98a55',False,640,150,490,0,300,'In Stock'),
 ('LM-SLT-005','Slate Grey Suede Laminate','Suede','1.0 mm',(1320,1275,1225),'plain','#5b6470',False,410,120,290,0,200,'In Stock'),
 ('LM-TEK-006','Classic Teak Woodgrain Laminate','Woodgrain','0.8 mm',(1020,985,950),'wood','#9a6a3a',False,880,200,680,0,300,'In Stock'),
 ('LM-CHR-007','Charcoal Black Gloss Laminate','Gloss','1.0 mm',(1090,1055,1010),'plain','#23262b',True,120,60,60,200,200,'Low Stock'),
 ('LM-IVR-008','Ivory Cream Matte Laminate','Matte','0.8 mm',(810,780,750),'plain','#efe6d2',False,1050,260,790,0,400,'In Stock'),
 ('LM-STN-009','Carrara Stone Finish Laminate','Texture','1.0 mm',(1480,1430,1375),'stone','#c9ccd0',False,0,0,0,250,150,'Out of Stock'),
 ('LM-CPR-010','Brushed Copper Metallic Laminate','Metallic','1.0 mm',(1890,1830,1760),'metal','#b4764a',False,95,40,55,100,100,'Low Stock'),
 ('LM-WNG-011','Wenge Dark Woodgrain Laminate','Woodgrain','1.0 mm',(1210,1170,1125),'wood','#3b2a22',False,560,130,430,0,250,'In Stock'),
 ('LM-SKY-012','Sky Blue Gloss Laminate','Gloss','0.8 mm',(870,840,805),'plain','#8fc1e3',True,345,95,250,0,150,'In Stock'),
]
# Open orders (not yet delivered): the single source for every "on order" figure, so the stock tables, tiles and the
# shipments list always agree. Expected = the date the order is expected or planned to arrive.
OPEN_ORDERS = {
    'ORD-2026-10447': ('27/10/2026', 'In Transit', [('LM-WNT-001',100),('LM-ARC-002',150),('LM-CHR-007',60),('LM-WNG-011',50)]),
    'ORD-2026-10459': ('29/10/2026', 'Confirmed', [('LM-TEK-006',100),('LM-IVR-008',120),('LM-SKY-012',60)]),
    'ORD-2026-10482': ('31/10/2026', 'Awaiting Confirmation', [('LM-WNT-001',200),('LM-ARC-002',300),('LM-CAL-003',80),('LM-OAK-004',120),('LM-SLT-005',60)]),
}
ON_ORDER, ARRIVAL = {}, {}
for _o, (_d, _st, _lines) in OPEN_ORDERS.items():
    for _s, _q in _lines:
        ON_ORDER[_s] = ON_ORDER.get(_s, 0) + _q
        ARRIVAL.setdefault(_s, _d)
P = [p[:11] + (ON_ORDER.get(p[0], 0),) + p[12:] for p in P]
OPEN_SHEETS = sum(ON_ORDER.values())
BY = {p[0]: p for p in P}
def prod(sku): return BY[sku]
def slab(sku, qty):
    s = BY[sku][4]
    return s[2] if qty >= 200 else s[1] if qty >= 50 else s[0]

def sw(sku, cls='', extra=''):
    p = BY[sku]
    return f'<div class="sw {p[5]}{" gloss" if p[7] else ""} {cls}" style="--a:{p[6]};{extra}" role="img" aria-label="{p[1]} swatch"></div>'

STATUS_CHIP = {'In Stock':'ok','Low Stock':'warn','Out of Stock':'bad',
  'Awaiting Confirmation':'warn','Confirmed':'blue','In Transit':'blue','Delivered':'ok','Cancelled':'bad',
  'Paid':'ok','Partly Paid':'warn','Unpaid':'plain','Not Applicable':'plain'}
def chip(text, cls=None):
    c = cls or STATUS_CHIP.get(text, '')
    return f'<span class="chip {c}">{text}</span>'

def qty(v):
    return f'<span class="qty"><span>−</span><input value="{v}" aria-label="Sheets" inputmode="numeric"><span>+</span></span>'

def chart(kind, labels=None, series=None, money=False, height=260, area=False, center=None, caption=None):
    a = f' data-type="{kind}"'
    if labels is not None: a += f" data-labels='{json.dumps(labels)}'"
    a += f" data-series='{json.dumps(series)}'"
    if money: a += ' data-money="true"'
    if area: a += ' data-area="true"'
    if center: a += f' data-center="{center}"'
    if caption: a += f' data-caption="{caption}"'
    return f'<div class="chart"{a} data-height="{height}"></div>'

def page(portal_folder, filename, sid, title, body):
    script = os.path.basename(__import__('__main__').__file__)
    html = f'''<!doctype html>
<html lang="en">
<!-- Generated by tools/author/{script}: edit the generator, not this file. -->
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../../assets/fonts.css">
<link rel="stylesheet" href="../../assets/styles.css">
<link rel="stylesheet" href="../../assets/app.css">
</head>
<body data-screen="{sid}" data-layout="app">
<main>
{body}</main>
<script src="../../assets/registry.js"></script>
<script src="../../assets/shell.js"></script>
<script src="../../assets/chrome.js"></script>
<script src="../../assets/charts.js"></script>
</body>
</html>
'''
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'screens', portal_folder, filename + '.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(html)
    return path


# =====================================================================================================================
# Phase 3 data (docs/DATA.md: Dealers, Secondary sales, Invoices and payments, Schemes, Returns, Support, Users).
# Everything below reconciles with the figures already on the Phase 2 screens; the asserts at the end check it.
# =====================================================================================================================
def dp(sku):
    """Dealer price per sheet before GST (Dealer Tier B): Crestline 1-49 list price plus 10%, to the nearest rupee 5."""
    return round(BY[sku][4][0] * 1.10 / 5) * 5

MONTHS = ['May', 'June', 'July', 'August', 'September', 'October']
SALES_MONTH = [2480000, 2810000, 2240000, 3060000, 2790000, 3120000]       # sales to dealers by month (DATA.md)
PURCH_MONTH = [2210000, 2560000, 1980000, 2740000, 2430000, 3352882]

# key, name, city, region, status, customer since, retailers, October sales, September sales, credit limit, owner
DEALERS = [
 ('BRV', 'Dealer Bravo',   'Pune',       'West Maharashtra',  'Active', '03/09/2019', 3, 684000, 610000, 800000, 'Sunita Rao'),
 ('DLT', 'Dealer Delta',   'Nashik',     'North Maharashtra', 'Active', '14/02/2019', 4, 592000, 520000, 700000, 'Prakash Jadhav'),
 ('FXT', 'Dealer Foxtrot', 'Thane',      'Konkan',            'Active', '21/06/2020', 3, 476000, 435000, 600000, 'Mohan Patil'),
 ('GPL', 'Dealer Gopal',   'Kolhapur',   'West Maharashtra',  'Active', '09/11/2020', 3, 411000, 385000, 500000, 'Gopal Kulkarni'),
 ('HRS', 'Dealer Harsh',   'Nagpur',     'Vidarbha',          'Active', '17/03/2021', 2, 338000, 360000, 500000, 'Harsh Wankhede'),
 ('IND', 'Dealer Indira',  'Satara',     'West Maharashtra',  'Active', '05/08/2022', 2, 246000, 235000, 400000, 'Indira Bhosale'),
 ('JYT', 'Dealer Jayant',  'Solapur',    'West Maharashtra',  'Active', '28/01/2023', 2, 218000, 245000, 400000, 'Jayant Shinde'),
 ('KNL', 'Dealer Kunal',   'Panaji',     'Goa',               'New',    '02/10/2026', 1, 155000,      0, 250000, 'Kunal Naik'),
]
DLR = {d[0]: d for d in DEALERS}
assert sum(d[7] for d in DEALERS) == 3120000 and sum(d[8] for d in DEALERS) == 2790000

# October sales per dealer: (day of October, relative size, payment: P paid / H half paid / U unpaid)
_SPEC = {
 'BRV': [(24,20,'U'), (17,18,'U'), (13,16,'P'), (8,18,'P'), (5,14,'P'), (1,14,'P')],
 'DLT': [(26,22,'U'), (20,20,'H'), (14,20,'P'), (9,20,'P'), (3,18,'P')],
 'FXT': [(22,24,'U'), (16,22,'H'), (11,20,'P'), (6,18,'P'), (2,16,'P')],
 'GPL': [(19,28,'U'), (12,26,'P'), (7,24,'P'), (2,22,'P')],
 'HRS': [(15,30,'U'), (10,26,'P'), (6,24,'P'), (1,20,'P')],
 'IND': [(21,40,'U'), (11,32,'P'), (4,28,'P')],
 'JYT': [(18,40,'H'), (9,34,'P'), (3,26,'P')],
 'KNL': [(23,60,'U'), (12,40,'P')],
}
# Dispatch numbers already shown in the Phase 2 stock movements of LM-CAL-003 (Inventory Item Details)
_ANCHOR = {('DLT',26): 5534, ('BRV',24): 5527, ('FXT',22): 5519, ('GPL',19): 5508, ('HRS',15): 5496, ('BRV',8): 5471, ('DLT',3): 5452}
_AVG = 3120000 / 2195                                             # average amount per sheet, GST included
SALES = []                                                        # newest first
for _k, _rows in _SPEC.items():
    _tot = DLR[_k][7]; _w = sum(r[1] for r in _rows); _vals = [round(_tot * r[1] / _w / 500) * 500 for r in _rows]
    _vals[-1] += _tot - sum(_vals)
    for (_day, _wt, _pay), _v in zip(_rows, _vals):
        _paid = _v if _pay == 'P' else round(_v / 2 / 500) * 500 if _pay == 'H' else 0
        SALES.append(dict(dealer=_k, day=_day, value=_v, paid=_paid, sheets=round(_v / _AVG / 5) * 5))
_order = list(DLR)
SALES.sort(key=lambda s: (s['day'], _order.index(s['dealer'])))   # oldest first, to number them
_n = 5440
for _i, _s in enumerate(SALES):
    _a = _ANCHOR.get((_s['dealer'], _s['day']))
    _n = _a if _a else _n + 1 + _i % 2
    if _n == 5521 and not _a: _n += 1                         # 5521 is Crestline's dispatch of ORD-2026-10447
    _s['dispatch'] = f'DSP-2026-{_n}'; _s['number'] = f'SAL-2026-{3010 + _i}'
    _s['date'] = f"{_s['day']:02d}/10/2026"
    _s['payment'] = 'Paid' if _s['paid'] == _s['value'] else 'Unpaid' if _s['paid'] == 0 else 'Partly Paid'
for _k in DLR:                                                    # per-dealer sheets add up exactly
    _mine = [s for s in SALES if s['dealer'] == _k]
    _target = round(DLR[_k][7] / 3120000 * 2195 / 5) * 5
    _mine[-1]['sheets'] += _target - sum(s['sheets'] for s in _mine)
_diff = 2195 - sum(s['sheets'] for s in SALES); SALES[-1]['sheets'] += _diff
SALES.reverse()                                                   # newest first
assert [s['dispatch'] for s in SALES] == sorted([s['dispatch'] for s in SALES], reverse=True), 'dispatch numbers out of order'
assert len({s['dispatch'] for s in SALES}) == len(SALES)
assert sum(s['value'] for s in SALES) == 3120000 and sum(s['sheets'] for s in SALES) == 2195
SALE_COUNT = len(SALES)
DEALER_SHEETS = {k: sum(s['sheets'] for s in SALES if s['dealer'] == k) for k in DLR}
DEALER_OWES = {k: sum(s['value'] - s['paid'] for s in SALES if s['dealer'] == k) for k in DLR}
DEALER_LAST = {k: next(s['date'] for s in SALES if s['dealer'] == k) for k in DLR}
OWED_TOTAL = sum(DEALER_OWES.values())

# Sheets sold to dealers in October by product (LM-CAL-003 = 165, the sum of its Phase 2 stock movements), and value
SOLD = {'LM-WNT-001':280, 'LM-ARC-002':405, 'LM-CAL-003':165, 'LM-OAK-004':205, 'LM-SLT-005':110, 'LM-TEK-006':220,
        'LM-CHR-007':100, 'LM-IVR-008':210, 'LM-STN-009':0, 'LM-CPR-010':35, 'LM-WNG-011':180, 'LM-SKY-012':285}
SOLD_VALUE = {s: round(q * dp(s) * 1.18) for s, q in SOLD.items()}
SOLD_VALUE['LM-ARC-002'] += 3120000 - sum(SOLD_VALUE.values())    # rounding difference goes to the largest line
assert sum(SOLD.values()) == 2195 and sum(SOLD_VALUE.values()) == 3120000 and abs(SOLD_VALUE['LM-ARC-002'] - round(405 * dp('LM-ARC-002') * 1.18)) < 3000
FINISH_SOLD = {}
for _s, _q in SOLD.items(): FINISH_SOLD[BY[_s][2]] = FINISH_SOLD.get(BY[_s][2], 0) + _q

# Invoices from Crestline: number, order, issued, due, amount, paid. Issued on the dispatch date, due 45 days later.
INVOICES = [
 ('INV-2026-03318', 'ORD-2026-10447', '24/10/2026', '08/12/2026', 442930, 0),
 ('INV-2026-03291', 'ORD-2026-10431', '18/10/2026', '02/12/2026', 618400, 200000),
 ('INV-2026-03264', 'ORD-2026-10398', '11/10/2026', '25/11/2026', 524100, 217510),
 ('INV-2026-03233', 'ORD-2026-10372', '04/10/2026', '18/11/2026', 481200, 481200),
 ('INV-2026-03198', 'ORD-2026-10341', '27/09/2026', '11/11/2026', 572300, 572300),
 ('INV-2026-03171', 'ORD-2026-10316', '20/09/2026', '04/11/2026', 398650, 398650),
 ('INV-2026-03140', 'ORD-2026-10290', '13/09/2026', '28/10/2026', 605900, 605900),
 ('INV-2026-03021', 'ORD-2026-10171', '12/08/2026', '26/09/2026', 132000, 0),
 ('INV-2026-02986', 'ORD-2026-10158', '05/08/2026', '19/09/2026', 186400, 0),
]
OPEN_INV = sorted([i for i in INVOICES if i[4] > i[5]], key=lambda i: i[3][6:] + i[3][3:5] + i[3][:2])
OUTSTANDING = sum(i[4] - i[5] for i in OPEN_INV)
OVERDUE = [i for i in OPEN_INV if i[3][6:] + i[3][3:5] + i[3][:2] < '20261026']
assert OUTSTANDING == 1486320 and sum(i[4] - i[5] for i in OVERDUE) == 318400 and len(OVERDUE) == 2
INV_ISSUED_OCT = sum(i[4] for i in INVOICES if i[2].endswith('/10/2026'))          # 20,66,630

PAYMENTS = [  # number, date, amount, mode, invoice
 ('PAY-2026-02217', '21/10/2026', 200000, 'Bank Transfer', 'INV-2026-03291'),
 ('PAY-2026-02204', '17/10/2026', 217510, 'Net Banking',   'INV-2026-03264'),
 ('PAY-2026-02188', '15/10/2026', 481200, 'Bank Transfer', 'INV-2026-03233'),
 ('PAY-2026-02143', '08/10/2026', 572300, 'Cheque',        'INV-2026-03198'),
 ('PAY-2026-02109', '02/10/2026', 398650, 'Bank Transfer', 'INV-2026-03171'),
 ('PAY-2026-02061', '24/09/2026', 605900, 'Net Banking',   'INV-2026-03140'),
 ('PAY-2026-01984', '12/09/2026', 543200, 'Bank Transfer', 'INV-2026-03109'),
 ('PAY-2026-01921', '02/09/2026', 476800, 'Cheque',        'INV-2026-03068'),
 ('PAY-2026-01866', '25/08/2026', 412000, 'Bank Transfer', 'INV-2026-03010'),
 ('PAY-2026-01802', '14/08/2026', 358400, 'Net Banking',   'INV-2026-02961'),
]
PAID_OCT = [p for p in PAYMENTS if p[1].endswith('/10/2026')]
assert sum(p[2] for p in PAID_OCT) == 1869660
for _i in INVOICES:                                                 # every payment of the listed invoices adds up to what is paid
    _got = sum(p[2] for p in PAYMENTS if p[4] == _i[0]); assert _got == _i[5], (_i[0], _got, _i[5])
PAID_MONTH = [2140000, 2410000, 2090000, 2530000, 2360000, 1869660]
MODE_OCT = {}
for _p in PAID_OCT: MODE_OCT[_p[3]] = MODE_OCT.get(_p[3], 0) + _p[2]

ORDER_10431 = [('LM-WNT-001', 120), ('LM-ARC-002', 150), ('LM-CAL-003', 60), ('LM-OAK-004', 100), ('LM-TEK-006', 90)]   # 520 sheets
assert sum(q for _, q in ORDER_10431) == 520
# October orders counted for the Festive Volume Rebate (2,750 sheets = 760 + 280 + 360 + 520 + 430 + 400)
FESTIVE_ORDERS = [('ORD-2026-10482','26/10/2026',760,'Awaiting Confirmation'), ('ORD-2026-10459','23/10/2026',280,'Confirmed'),
                  ('ORD-2026-10447','19/10/2026',360,'In Transit'), ('ORD-2026-10431','15/10/2026',520,'Delivered'),
                  ('ORD-2026-10398','08/10/2026',430,'Delivered'), ('ORD-2026-10372','01/10/2026',400,'Delivered')]
assert sum(o[2] for o in FESTIVE_ORDERS) == 2750

# Money in the compact format for text built from several amounts
def pct(a, b): return f'{(a - b) / b * 100:.1f}%'

STATUS_CHIP.update({'Active':'ok', 'New':'blue', 'Inactive':'plain', 'Invited':'warn', 'Overdue':'bad', 'Confirmed':'blue',
  'Under Review':'warn', 'Approved':'blue', 'Pickup Scheduled':'blue', 'Credit Issued':'ok', 'Rejected':'bad',
  'Open':'warn', 'In Progress':'blue', 'Awaiting Your Reply':'warn', 'Resolved':'ok', 'Closed':'plain',
  'Upcoming':'blue', 'Completed':'plain', 'Cleared':'ok', 'High':'bad', 'Medium':'warn', 'Low':'plain', 'Pending':'warn'})


# ---------- Phase 3 markup helpers ----------
def tabs(items):
    return '<div style="padding:0 1.125rem"><div class="tabs">' + ''.join(f'<span class="{"on" if on else ""}">{t}<b>{n}</b></span>' for t, n, on in items) + '</div></div>'

def kpi(label, value, foot=''):
    return f'<div class="card kpi"><label>{label}</label><strong>{value}</strong>' + (f'<div class="foot">{foot}</div>' if foot else '') + '</div>'

def up(text, tip='Compared with September'):
    return f'<span class="delta up" title="{tip}"><i data-icon="trend"></i>{text}</span>'

def sel(label, value):
    return f'<span class="sel"><small>{label}</small> {value} <i data-icon="down"></i></span>'

def finder(placeholder, label, grow=True):
    return f'<label class="finder{" grow" if grow else ""}"><i data-icon="search"></i><input type="search" placeholder="{placeholder}" aria-label="{label}"></label>'

def filters(search_ph, search_label, *sels):
    return '<div class="filters" style="padding:1rem 1.125rem 0">' + finder(search_ph, search_label) + ''.join(sel(a, b) for a, b in sels) + '</div>'

def pager(text, last=3):
    pages = '<span class="on">1</span><span>2</span><span>3</span>' if last == 3 else '<span class="on">1</span>'
    return f'<div class="pg"><span>{text}</span><div class="pages">{pages}</div></div>'

def kv(rows, cls=''):
    return f'<dl class="kv {cls}">' + ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows) + '</dl>'

def card(title, inner, more='', flush=False):
    return f'<section class="card{" flush" if flush else ""}"><header><h2>{title}</h2>{more}</header><div class="body">{inner}</div></section>'

def table(heads, rows, cls='', foot=''):
    """heads: list of (label, css class); rows: list of already-built <tr>…</tr> strings"""
    th = ''.join(f'<th{" class=" + chr(34) + c + chr(34) if c else ""}>{h}</th>' for h, c in heads)
    return f'<div class="table-wrap"><table class="tbl {cls}"><thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody>{foot}</table></div>'

def fld(label, fid, value='', kind='input', options=None, full=False, ph=''):
    cls = ' class="full"' if full else ''
    if kind == 'select':
        opts = ''.join(f'<option{" selected" if o == value else ""}>{o}</option>' for o in options)
        ctl = f'<select class="input" id="{fid}">{opts}</select>'
    elif kind == 'textarea':
        ctl = f'<textarea class="input" id="{fid}" placeholder="{ph}">{value}</textarea>'
    else:
        ctl = f'<input class="input" id="{fid}" value="{value}" placeholder="{ph}">'
    return f'<div class="field{" full" if full else ""}"><label for="{fid}">{label}</label>{ctl}</div>'

def form(title, *fields):
    return f'<section class="card"><header><h2>{title}</h2></header><div class="body"><div class="form-grid">{"".join(fields)}</div></div></section>'

def credit_pct(owes, limit):
    return round(owes / limit * 100)

def meter_cls(pct):
    return 'bad' if pct >= 80 else 'warn' if pct >= 50 else 'ok'

def link(sid, text, bold=True):
    inner = f'<b>{text}</b>' if bold else text
    return f'<a data-link="{sid}">{inner}</a>'

def pay_chip(s):
    return chip(s, {'Paid': 'ok', 'Partly Paid': 'warn', 'Unpaid': 'plain'}[s])

def dl_btn(label='Download'):
    return f'<button class="btn sm" type="button" aria-label="{label}"><i data-icon="download"></i></button>'


# =====================================================================================================================
# Phase 4 data (docs/DATA.md: "Phase 4 data"). Manager: stock movements, dispatches, dealer orders and targets, dealer requests.
# Accountant: ageing, purchases and tax, credit notes, disputes. Everything reconciles with Phases 2 and 3; asserts check it.
# =====================================================================================================================
import datetime
TODAY = datetime.date(2026, 10, 26)
def pd(s): return datetime.date(int(s[6:]), int(s[3:5]), int(s[:2]))
def fd(x): return x.strftime('%d/%m/%Y')

# ---- Lines of the six October orders (ORD-2026-10482/10459/10447 from OPEN_ORDERS; the delivered three are new in Phase 4) ----
ORDER_LINES = {o: l for o, (_d, _st, l) in OPEN_ORDERS.items()}
ORDER_LINES['ORD-2026-10431'] = ORDER_10431
ORDER_LINES['ORD-2026-10398'] = [('LM-WNT-001', 100), ('LM-ARC-002', 130), ('LM-OAK-004', 90), ('LM-SLT-005', 60), ('LM-TEK-006', 50)]
ORDER_LINES['ORD-2026-10372'] = [('LM-WNT-001', 80), ('LM-ARC-002', 100), ('LM-OAK-004', 80), ('LM-IVR-008', 80), ('LM-WNG-011', 60)]
ORDER_VALUE = {'ORD-2026-10482': 949752, 'ORD-2026-10459': 336500, 'ORD-2026-10447': 442930, 'ORD-2026-10431': 618400,
               'ORD-2026-10398': 524100, 'ORD-2026-10372': 481200}
ORDER_SHEETS = {o: sum(q for _, q in l) for o, l in ORDER_LINES.items()}
assert ORDER_SHEETS == {'ORD-2026-10482': 760, 'ORD-2026-10459': 280, 'ORD-2026-10447': 360, 'ORD-2026-10431': 520, 'ORD-2026-10398': 430, 'ORD-2026-10372': 400}
assert sum(ORDER_VALUE.values()) == PURCH_MONTH[-1]
# Receipts: the three delivered October orders arrive at Bhiwandi Warehouse on their delivery dates
RECEIPTS = [('ORD-2026-10431', '20/10/2026'), ('ORD-2026-10398', '13/10/2026'), ('ORD-2026-10372', '06/10/2026')]
RECEIVED = sum(ORDER_SHEETS[o] for o, _ in RECEIPTS)                                   # 1,350
assert RECEIVED == 1350
# Sheets purchased in October by product (all six orders, 2,750) and the allocated value (same method as SOLD_VALUE)
BOUGHT = {}
for _o, _l in ORDER_LINES.items():
    for _s, _q in _l: BOUGHT[_s] = BOUGHT.get(_s, 0) + _q
assert sum(BOUGHT.values()) == 2750
_w = {s: q * BY[s][4][1] for s, q in BOUGHT.items()}
BOUGHT_VALUE = {s: round(PURCH_MONTH[-1] * w / sum(_w.values())) for s, w in _w.items()}
_big = max(BOUGHT_VALUE, key=BOUGHT_VALUE.get); BOUGHT_VALUE[_big] += PURCH_MONTH[-1] - sum(BOUGHT_VALUE.values())
assert sum(BOUGHT_VALUE.values()) == 3352882

# ---- Stock adjustments (October) ----
ADJUSTMENTS = [('ADJ-2026-0036', '23/10/2026', 'LM-TEK-006', -10, 'Damaged in Handling'), ('ADJ-2026-0035', '21/10/2026', 'LM-WNT-001', -6, 'Damaged in Handling'),
               ('ADJ-2026-0034', '12/10/2026', 'LM-CAL-003', -5, 'Damaged in Handling'), ('ADJ-2026-0033', '09/10/2026', 'LM-SLT-005', 3, 'Count Correction'),
               ('ADJ-2026-0032', '06/10/2026', 'LM-OAK-004', -4, 'Count Correction'), ('ADJ-2026-0031', '02/10/2026', 'LM-ARC-002', -8, 'Damaged in Handling')]
ADJUSTED = sum(a[3] for a in ADJUSTMENTS)                                              # -30
assert ADJUSTED == -30

# ---- Dealer sales: delivery status, expected delivery and the product lines of every sale ----
LEAD = {'Pune': 2, 'Thane': 3, 'Nashik': 3, 'Kolhapur': 4, 'Satara': 4, 'Solapur': 4, 'Nagpur': 6, 'Panaji': 5}   # days from dispatch to delivery
for _s in SALES:
    _dt = pd(_s['date']); _exp = _dt + datetime.timedelta(days=LEAD[DLR[_s['dealer']][2]])
    _s['expected'] = fd(_exp); _s['status'] = 'Being Packed' if _dt == TODAY else 'Delivered' if _exp < TODAY else 'In Transit'
    _s['city'] = DLR[_s['dealer']][2]
_CAL_SALE = {('DLT', 26): 20, ('BRV', 24): 25, ('FXT', 22): 15, ('GPL', 19): 30, ('HRS', 15): 25, ('BRV', 8): 25, ('DLT', 3): 25}   # as in Inventory Item Details
assert sum(_CAL_SALE.values()) == SOLD['LM-CAL-003']
_left = {s: SOLD[s] for s in ['LM-ARC-002', 'LM-WNT-001', 'LM-TEK-006', 'LM-IVR-008', 'LM-SKY-012', 'LM-OAK-004', 'LM-WNG-011', 'LM-SLT-005', 'LM-CHR-007', 'LM-CPR-010']}
_queue = []                                                                            # chunks of up to 40 sheets, products taken in turn, so each sale mixes products
while any(_left.values()):
    for _k in _left:
        if _left[_k]: _t = min(40, _left[_k]); _queue.append([_k, _t]); _left[_k] -= _t
_qi = 0
for _s in reversed(SALES):                                                             # oldest first
    _s['lines'] = []; _c = _CAL_SALE.get((_s['dealer'], _s['day']), 0)
    if _c: _s['lines'].append(('LM-CAL-003', _c))
    _need = _s['sheets'] - _c
    while _need > 0:
        _take = min(_need, _queue[_qi][1])
        _same = [n for n, l in enumerate(_s['lines']) if l[0] == _queue[_qi][0]]
        if _same: _s['lines'][_same[0]] = (_queue[_qi][0], _s['lines'][_same[0]][1] + _take)
        else: _s['lines'].append((_queue[_qi][0], _take))
        _queue[_qi][1] -= _take; _need -= _take
        if _queue[_qi][1] == 0: _qi += 1
assert all(q == 0 for _, q in _queue) and all(sum(q for _, q in s['lines']) == s['sheets'] for s in SALES)
_chk = {}
for _s in SALES:
    for _k, _q in _s['lines']: _chk[_k] = _chk.get(_k, 0) + _q
assert all(_chk.get(k, 0) == v for k, v in SOLD.items())
STATUS_COUNT = {st: sum(1 for s in SALES if s['status'] == st) for st in ('Being Packed', 'In Transit', 'Delivered')}

# ---- Every stock movement of October (newest first): receipts, sales to dealers, adjustments ----
MOVES = []
for _o, _dt in RECEIPTS:
    for _k, _q in ORDER_LINES[_o]: MOVES.append(dict(date=_dt, type='Receipt', sku=_k, who='Crestline Laminates', ref=_o, sheets=_q))
for _s in SALES:
    for _k, _q in _s['lines']: MOVES.append(dict(date=_s['date'], type='Sale to Dealer', sku=_k, who=DLR[_s['dealer']][1], ref=_s['dispatch'], sheets=-_q))
for _a in ADJUSTMENTS: MOVES.append(dict(date=_a[1], type='Stock Adjustment', sku=_a[2], who=_a[4], ref=_a[0], sheets=_a[3]))
_kind = {'Sale to Dealer': 0, 'Receipt': 1, 'Stock Adjustment': 2}
MOVES.sort(key=lambda m: m['sku'])
MOVES.sort(key=lambda m: (pd(m['date']), _kind[m['type']], m['ref']), reverse=True)
assert sum(m['sheets'] for m in MOVES) == RECEIVED - 2195 + ADJUSTED
# Inventory Item Details (LM-CAL-003): the movements walk back from 215 on hand to 325 before 03/10
CAL_MOVES = [m for m in MOVES if m['sku'] == 'LM-CAL-003']
_bal = 215
for _m in CAL_MOVES: _m['balance'] = _bal; _bal -= _m['sheets']
CAL_OPENING = _bal
assert CAL_OPENING == 325 and len(CAL_MOVES) == 9
MOVE_BY = {s: dict(received=0, sold=0, adjusted=0) for s in BY}
for _m in MOVES:
    MOVE_BY[_m['sku']]['received' if _m['type'].startswith('Receipt') else 'sold' if _m['type'].startswith('Sale') else 'adjusted'] += abs(_m['sheets']) if not _m['type'].startswith('Stock') else _m['sheets']
assert all(MOVE_BY[s]['sold'] == SOLD[s] for s in SOLD)

# ---- Low stock: reorder quantity per product (CAL-003 = 400 as on Inventory Item Details); suggested value at the quantity's slab price ----
REORDER_QTY = {'LM-STN-009': 300, 'LM-CHR-007': 300, 'LM-CAL-003': 400, 'LM-CPR-010': 150}
LOW = [p for p in P if p[13] in ('Low Stock', 'Out of Stock')]
assert [p[0] for p in LOW] == ['LM-CAL-003', 'LM-CHR-007', 'LM-STN-009', 'LM-CPR-010'] and set(REORDER_QTY) == {p[0] for p in LOW}
LOW_VALUE = {s: q * slab(s, q) for s, q in REORDER_QTY.items()}
assert sum(LOW_VALUE.values()) == 1570000

# ---- Dealer targets (October) and performance ----
TARGET = {'BRV': 650000, 'DLT': 600000, 'FXT': 450000, 'GPL': 425000, 'HRS': 375000, 'IND': 240000, 'JYT': 250000, 'KNL': 150000}
TARGET_TOTAL = sum(TARGET.values()); assert TARGET_TOTAL == 3140000
def achievement(k): return DLR[k][7] / TARGET[k] * 100
def perf_status(k):
    a = achievement(k); return 'Above Target' if a >= 100 else 'Near Target' if a >= 95 else 'Below Target'
STATUS_CHIP.update({'Above Target': 'ok', 'Near Target': 'warn', 'Below Target': 'bad', 'Being Packed': 'warn', 'Awaiting Your Review': 'warn',
                    'Sent to Crestline': 'blue', 'Awaiting Your Reply': 'warn', 'Under Review': 'warn', 'Not Yet Due': 'plain'})
WEEKS = [('1 to 7 October', 1, 7), ('8 to 14 October', 8, 14), ('15 to 21 October', 15, 21), ('22 to 26 October', 22, 26)]
def week_sales(a, b): return [s for s in SALES if a <= s['day'] <= b]
assert sum(len(week_sales(a, b)) for _, a, b in WEEKS) == 32

# ---- Pending dealer requests (Add Dealer Request, approved by the Sales and Operations Manager, then Crestline) ----
REQUESTS = [  # number, dealer, city, region, owner, submitted, submitted by, credit requested, expected sheets per month, documents, status
 ('DRQ-2026-0019', 'Dealer Mahesh', 'Amravati', 'Vidarbha', 'Mahesh Gaikwad', '24/10/2026', 'Rajesh Menon', 300000, 120, 3, 'Awaiting Your Review'),
 ('DRQ-2026-0018', 'Dealer Navin', 'Sangli', 'West Maharashtra', 'Navin Kamble', '22/10/2026', 'Rajesh Menon', 350000, 100, 2, 'Awaiting Your Review'),
 ('DRQ-2026-0017', 'Dealer Omkar', 'Jalgaon', 'North Maharashtra', 'Omkar Deshmukh', '19/10/2026', 'Rajesh Menon', 400000, 150, 3, 'Sent to Crestline'),
]
assert sum(r[7] for r in REQUESTS) == 1050000

# ---- Accountant: ageing of the open invoices, credit, tax split, credit notes, disputes ----
CREDIT_LIMIT = 4000000
def days_over(i): return (TODAY - pd(i[3])).days            # negative: days until due
def bucket(i):
    o = days_over(i)
    return 'Not Yet Due' if o <= 0 else '1 to 30 Days Overdue' if o <= 30 else '31 to 60 Days Overdue' if o <= 60 else '61 to 90 Days Overdue' if o <= 90 else 'Over 90 Days Overdue'
BUCKETS = ['Not Yet Due', '1 to 30 Days Overdue', '31 to 60 Days Overdue', '61 to 90 Days Overdue', 'Over 90 Days Overdue']
AGE = {b: [i for i in OPEN_INV if bucket(i) == b] for b in BUCKETS}
AGE_AMT = {b: sum(i[4] - i[5] for i in v) for b, v in AGE.items()}
assert sum(AGE_AMT.values()) == OUTSTANDING and AGE_AMT['Not Yet Due'] == 1167920 and AGE_AMT['1 to 30 Days Overdue'] == 132000 and AGE_AMT['31 to 60 Days Overdue'] == 186400
CREDIT_AVAILABLE = CREDIT_LIMIT - OUTSTANDING                # 25,13,680; after ORD-2026-10482 it is 15,63,928 as on Order Builder
assert CREDIT_AVAILABLE - 949752 == 1563928

def tax_split(total, free_above=500000):
    """taxable + 2 x round(9%) + freight = total. Freight is 4,500 below the free-freight limit when an exact split exists, else 0."""
    for f in ([4500, 0] if total < free_above else [0]):
        t0 = int((total - f) / 1.18)
        for t in range(t0 - 3, t0 + 4):
            if t + 2 * round(0.09 * t) + f == total: return dict(taxable=t, gst=round(0.09 * t), freight=f, total=total)
    raise ValueError(total)
ORDER_TAX = {o: tax_split(v) for o, v in ORDER_VALUE.items()}
assert ORDER_TAX['ORD-2026-10482'] == dict(taxable=804874, gst=72439, freight=0, total=949752)            # Order Builder
assert ORDER_TAX['ORD-2026-10447'] == dict(taxable=371550, gst=33440, freight=4500, total=442930)         # Invoice Details
def _sum_tax(rows): return {k: sum(r[k] for r in rows) for k in ('taxable', 'gst', 'freight', 'total')}
# Months May to September: totals are the DATA.md purchases; freight is 4,500 for each order below the limit (count chosen so a split exists)
MONTH_TAX = []
for _m, _tot in zip(MONTHS[:-1], PURCH_MONTH[:-1]):
    for _k in range(2, 7):
        _f = 4500 * _k; _t0 = int((_tot - _f) / 1.18)
        _hit = [t for t in range(_t0 - 3, _t0 + 4) if t + 2 * round(0.09 * t) + _f == _tot]
        if _hit: MONTH_TAX.append(dict(taxable=_hit[0], gst=round(0.09 * _hit[0]), freight=_f, total=_tot)); break
    else: raise ValueError(_m)
MONTH_TAX.append(_sum_tax(list(ORDER_TAX.values())))
assert MONTH_TAX[-1]['total'] == 3352882 and sum(m['total'] for m in MONTH_TAX) == sum(PURCH_MONTH)
assert all(m['taxable'] + 2 * m['gst'] + m['freight'] == m['total'] for m in MONTH_TAX)

CREDIT_NOTES = [  # number, date, return request, order, credit amount (sheets x the 50-199 price: the Phase 3 return credits)
 ('CN-2026-0103', '16/10/2026', 'RTN-2026-0377', 'ORD-2026-10372', 18000), ('CN-2026-0098', '09/10/2026', 'RTN-2026-0361', 'ORD-2026-10341', 10550),
 ('CN-2026-0091', '24/09/2026', 'RTN-2026-0319', 'ORD-2026-10290', 13790)]
assert sum(c[4] for c in CREDIT_NOTES) == 42340

DISPUTES = [  # number, invoice, raised, reason, invoice amount, disputed amount, status, company response
 ('DIS-2026-0014', 'INV-2026-03264', '22/10/2026', 'Wrong Product Delivered', 524100, 21358, 'Awaiting Your Reply', 'Pickup scheduled, credit note to follow'),
 ('DIS-2026-0011', 'INV-2026-03021', '10/10/2026', 'Quantity Shortfall', 132000, 16992, 'Under Review', 'Delivery challan being checked'),
 ('DIS-2026-0007', 'INV-2026-03198', '29/09/2026', 'Tax Amount Mismatch', 572300, 4284, 'Resolved', 'Corrected invoice issued'),
]
assert 20 * 905 + 2 * round(0.09 * 20 * 905) == 21358                                  # 20 sheets of LM-ARC-002 at the 50-199 price, with Central and State GST
OPEN_DISPUTES = [d for d in DISPUTES if d[6] != 'Resolved']
assert len(OPEN_DISPUTES) == 2 and sum(d[5] for d in OPEN_DISPUTES) == 38350


# =====================================================================================================================
# Phase 5 data (docs/DATA.md: "Phase 5 data"). Secondary Customer: Dealer Bravo, Pune. Orders to Distributor Alpha are the Alpha
# sales ledger rows of Dealer Bravo (the sale number is the order number and the invoice number); retailers and their sales are new.
# =====================================================================================================================
def rp(sku):
    """Retailer price per sheet before GST (Retailer Tier C): the Dealer Tier B price plus 12%, to the nearest rupee 5."""
    return round(dp(sku) * 1.12 / 5) * 5

BRV_SALES = [s for s in SALES if s['dealer'] == 'BRV']                      # newest first, 6 orders, 480 sheets, ₹6,84,000
assert len(BRV_SALES) == 6 and sum(s['sheets'] for s in BRV_SALES) == 480
BRV_PURCH_MONTH = [520000, 590000, 480000, 630000, 610000, 684000]
BRV_RETAIL_MONTH = [510000, 560000, 470000, 600000, 600000, 630000]       # Bravo's sales to its retailers by month

# The order placed on 26/10/2026 (Place Order, Order Builder, Order Confirmation); awaiting confirmation, so not yet a sale in the Alpha ledger
NEW_ORDER = 'SAL-2026-3042'
NEW_LINES = [('LM-WNT-001', 60), ('LM-ARC-002', 80), ('LM-OAK-004', 40), ('LM-TEK-006', 30)]
NEW_SUB = sum(q * dp(s) for s, q in NEW_LINES); NEW_GST = round(NEW_SUB * 0.09); NEW_TOTAL = NEW_SUB + 2 * NEW_GST
assert (NEW_SUB, NEW_GST, NEW_TOTAL) == (249000, 22410, 293820) and sum(q for _, q in NEW_LINES) == 210
BRV_LIMIT = 800000; BRV_OWES = DEALER_OWES['BRV']
assert BRV_OWES == 260000 and BRV_LIMIT - BRV_OWES - NEW_TOTAL == 246180
# Order SAL-2026-3040 (Order Details): dealer-price lines, a trade discount (the difference to the ledger value), then GST
O40 = BRV_SALES[0]; assert O40['number'] == 'SAL-2026-3040' and O40['value'] == 137000
O40_SUB = sum(q * dp(s) for s, q in O40['lines']); O40_TAX = 116102; O40_GST = round(0.09 * O40_TAX)
O40_DISC = O40_SUB - O40_TAX
assert (O40_SUB, O40_DISC, O40_GST) == (119700, 3598, 10449) and O40_TAX + 2 * O40_GST == 137000

# ---- Bravo's stock (sheets): sku -> on hand, reserved for retailers, reorder level. On order = the two open orders above. ----
_BS = {'LM-WNT-001': (180, 45, 80), 'LM-ARC-002': (240, 60, 100), 'LM-CAL-003': (38, 12, 40), 'LM-OAK-004': (95, 20, 60), 'LM-SLT-005': (60, 15, 40),
       'LM-TEK-006': (110, 25, 60), 'LM-CHR-007': (22, 10, 40), 'LM-IVR-008': (140, 30, 80), 'LM-STN-009': (0, 0, 30), 'LM-CPR-010': (18, 6, 20),
       'LM-WNG-011': (85, 20, 50), 'LM-SKY-012': (70, 18, 40)}
BRV_ON_ORDER = {}
for _s, _q in O40['lines'] + NEW_LINES: BRV_ON_ORDER[_s] = BRV_ON_ORDER.get(_s, 0) + _q
BSTOCK = {}
for _s, (_h, _r, _l) in _BS.items():
    _av = _h - _r
    BSTOCK[_s] = dict(on_hand=_h, reserved=_r, available=_av, on_order=BRV_ON_ORDER.get(_s, 0), level=_l,
                      status='Out of Stock' if _h == 0 else 'Low Stock' if _av < _l else 'In Stock')
assert sum(b['on_hand'] for b in BSTOCK.values()) == 1058 and sum(b['reserved'] for b in BSTOCK.values()) == 261
assert sum(b['on_order'] for b in BSTOCK.values()) == 310
assert [s for s, b in BSTOCK.items() if b['status'] == 'Low Stock'] == ['LM-CAL-003', 'LM-CHR-007', 'LM-CPR-010'] and BSTOCK['LM-STN-009']['status'] == 'Out of Stock'
BSTOCK_VALUE = sum(b['on_hand'] * dp(s) for s, b in BSTOCK.items())             # at Bravo's cost (dealer price)
BFINISH = {}
for _s, _b in BSTOCK.items(): BFINISH[BY[_s][2]] = BFINISH.get(BY[_s][2], 0) + _b['on_hand']
assert sum(BFINISH.values()) == 1058

# ---- Retailers of Dealer Bravo and the October sales to them (newest first; numbers TSL-2026-0401 to 0412) ----
# key, name, area, city, owner, since, credit limit, credit period (days), September sales, monthly sales May to October
RETAILERS = [
 ('CHR', 'Retailer Charlie', 'Camp', 'Pune', 'Imran Sheikh', '11/05/2021', 300000, 15, 240000, [190000, 210000, 175000, 230000, 240000, 264000]),
 ('KIR', 'Retailer Kiran Interiors', 'Kothrud', 'Pune', 'Kiran Desai', '03/02/2022', 250000, 15, 195000, [165000, 180000, 150000, 185000, 195000, 210000]),
 ('MEH', 'Retailer Mehta Furniture', 'Pimpri Chinchwad', 'Pimpri', 'Nilesh Mehta', '19/09/2022', 200000, 15, 165000, [155000, 170000, 145000, 185000, 165000, 156000]),
]
RTL = {r[0]: r for r in RETAILERS}
assert [sum(r[9][i] for r in RETAILERS) for i in range(6)] == BRV_RETAIL_MONTH and sum(r[8] for r in RETAILERS) == 600000
_TSPEC = {'CHR': [(25, 62000, 'U'), (19, 58000, 'P'), (12, 52000, 'P'), (6, 49000, 'P'), (1, 43000, 'P')],
          'KIR': [(24, 48000, 'U'), (16, 55000, 'P'), (9, 60000, 'P'), (2, 47000, 'P')],
          'MEH': [(21, 62000, 'P'), (13, 50000, 'P'), (4, 44000, 'P')]}
_TSHEETS = {'CHR': 155, 'KIR': 125, 'MEH': 90}
TSALES = []
for _k, _rows in _TSPEC.items():
    assert sum(r[1] for r in _rows) == RTL[_k][9][-1]
    _sh = [round(v / (630000 / 370) / 5) * 5 for _, v, _p in _rows]; _sh[-1] += _TSHEETS[_k] - sum(_sh)
    for (_d, _v, _p), _n in zip(_rows, _sh):
        TSALES.append(dict(retailer=_k, day=_d, value=_v, paid=_v if _p == 'P' else 0, sheets=_n, date=f'{_d:02d}/10/2026', payment='Paid' if _p == 'P' else 'Unpaid'))
TSALES.sort(key=lambda s: (s['day'], list(RTL).index(s['retailer'])))
for _i, _s in enumerate(TSALES): _s['number'] = f'TSL-2026-{401 + _i:04d}'
TSALES.reverse()
assert len(TSALES) == 12 and sum(s['value'] for s in TSALES) == 630000 and sum(s['sheets'] for s in TSALES) == 370 and TSALES[0]['number'] == 'TSL-2026-0412'
RTL_SHEETS = {k: sum(s['sheets'] for s in TSALES if s['retailer'] == k) for k in RTL}
RTL_OWES = {k: sum(s['value'] - s['paid'] for s in TSALES if s['retailer'] == k) for k in RTL}
RTL_LAST = {k: next(s['date'] for s in TSALES if s['retailer'] == k) for k in RTL}
assert RTL_OWES == {'CHR': 62000, 'KIR': 48000, 'MEH': 0} and RTL_SHEETS == _TSHEETS

# ---- Inventory Item Details for Bravo (LM-CAL-003): receipt from Alpha, sales to retailers, balance walking back from 38 on hand ----
_CAL_RETAIL = {'TSL-2026-0412': 6, 'TSL-2026-0410': 4, 'TSL-2026-0408': 5, 'TSL-2026-0406': 8, 'TSL-2026-0405': 6, 'TSL-2026-0402': 4}
BCAL = []
for _s in TSALES:
    if _s['number'] in _CAL_RETAIL:
        assert _CAL_RETAIL[_s['number']] <= _s['sheets']
        BCAL.append(dict(date=_s['date'], type='Sale to Retailer', who=RTL[_s['retailer']][1], ref=_s['number'], sheets=-_CAL_RETAIL[_s['number']]))
BCAL.append(dict(date='10/10/2026', type='Receipt', who='Distributor Alpha', ref='SAL-2026-3021', sheets=25))      # delivered two days after the 08/10 dispatch
BCAL.sort(key=lambda m: pd(m['date']), reverse=True)
_b = 38
for _m in BCAL: _m['balance'] = _b; _b -= _m['sheets']
BCAL_OPEN = _b
assert BCAL_OPEN == 46
BCAL_SOLD = -sum(m['sheets'] for m in BCAL if m['sheets'] < 0)

# ---- Bravo's retailer request (Add Retailer Request) and schemes from Distributor Alpha ----
RETAILER_REQUEST = ('Retailer Dhruv Interiors', 'Wakad', 'Pune', 'Dhruv Patil', '27AAHFD6620L1Z8', 150000, 60)


# =====================================================================================================================
# Phase 6 data (docs/DATA.md: "Phase 6 data"). Dealer Bravo's invoices and payments (to Distributor Alpha), tertiary sale lines,
# returns, tickets, users and schemes. Dealer-level documents issued by Distributor Alpha carry a "D" before the number
# (PAY-2026-D0521, RTN-2026-D0508, TKT-2026-D0746) so they never collide with the Crestline series used by Distributor Alpha.
# =====================================================================================================================
SCH_FESTIVE = ('SCH-2026-07', 'Dealer Festive Volume Rebate', 690, 750, '30/11/2026')      # 480 sheets recorded + 210 on SAL-2026-3042
SCH_MARBLE = ('SCH-2026-08', 'Marble Finish Dealer Incentive', 50, 100, '31/12/2026')       # 25 + 25 sheets of LM-CAL-003 since 01/10
assert SCH_FESTIVE[2] == sum(s['sheets'] for s in BRV_SALES) + 210 and SCH_MARBLE[2] == sum(q for s in BRV_SALES for k, q in s['lines'] if k == 'LM-CAL-003')

# Bravo's orders, newest first (the order number is the Distributor Alpha sale number and invoice number)
BRV_ORDERS = [(NEW_ORDER, '26/10/2026', 210, NEW_TOTAL, '30/10/2026', 'Awaiting Confirmation', 'Unpaid')]
for _s in BRV_SALES: BRV_ORDERS.append((_s['number'], _s['date'], _s['sheets'], _s['value'], _s['expected'], _s['status'], _s['payment']))
BRV_ORDERS += [('SAL-2026-3006', '30/09/2026', 95, 135500, '02/10/2026', 'Delivered', 'Paid'), ('SAL-2026-2999', '22/09/2026', 105, 148000, '24/09/2026', 'Delivered', 'Paid'),
               ('SAL-2026-2990', '14/09/2026', 75, 106500, '16/09/2026', 'Delivered', 'Paid')]
assert len(BRV_ORDERS) == 10 and sum(o[3] for o in BRV_ORDERS[1:7]) == 684000

# ---- Invoices from Distributor Alpha: number, order, issued, due (30 days), amount, paid ----
BINV = []
for _o in BRV_ORDERS[1:]:
    _paid = _o[3] if _o[6] == 'Paid' else 0
    BINV.append((_o[0], _o[0], _o[1], fd(pd(_o[1]) + datetime.timedelta(days=30)), _o[3], _paid))
BOPEN = [i for i in BINV if i[4] > i[5]]
assert [i[0] for i in BOPEN] == ['SAL-2026-3040', 'SAL-2026-3033'] and sum(i[4] - i[5] for i in BOPEN) == BRV_OWES == 260000
assert all(pd(i[3]) >= TODAY for i in BOPEN)                                                  # nothing overdue
B_ORDER_COUNT = dict(awaiting=1, transit=1, delivered=208, cancelled=2)
B_INV_COUNT = B_ORDER_COUNT['transit'] + B_ORDER_COUNT['delivered']                             # 209 invoices: 2 open, 207 paid
assert B_INV_COUNT == 209 and B_INV_COUNT - len(BOPEN) == 207

# ---- Payments to Distributor Alpha (newest first): number, date, amount, mode, invoice ----
BPAY = [('PAY-2026-D0521', '22/10/2026', 109500, 'Bank Transfer', 'SAL-2026-3029'), ('PAY-2026-D0517', '17/10/2026', 123000, 'Cheque', 'SAL-2026-3021'),
        ('PAY-2026-D0511', '14/10/2026', 96000, 'Net Banking', 'SAL-2026-3017'), ('PAY-2026-D0506', '10/10/2026', 95500, 'Bank Transfer', 'SAL-2026-3010'),
        ('PAY-2026-D0501', '06/10/2026', 135500, 'Cheque', 'SAL-2026-3006'), ('PAY-2026-D0494', '29/09/2026', 148000, 'Bank Transfer', 'SAL-2026-2999'),
        ('PAY-2026-D0488', '24/09/2026', 106500, 'Net Banking', 'SAL-2026-2990'), ('PAY-2026-D0479', '15/09/2026', 184000, 'Bank Transfer', 'SAL-2026-2975'),
        ('PAY-2026-D0471', '03/09/2026', 162000, 'Cheque', 'SAL-2026-2962'), ('PAY-2026-D0462', '28/08/2026', 210000, 'Net Banking', 'SAL-2026-2948')]
for _i in BINV:
    _got = sum(p[2] for p in BPAY if p[4] == _i[0]); assert _got == _i[5], (_i[0], _got, _i[5])
_dates = [pd(p[1]) for p in BPAY]; assert _dates == sorted(_dates, reverse=True) and len({p[0] for p in BPAY}) == 10
assert [p[0] for p in BPAY] == sorted((p[0] for p in BPAY), reverse=True)
BPAY_OCT = [p for p in BPAY if p[1].endswith('/10/2026')]
BPAID_OCT = sum(p[2] for p in BPAY_OCT)
BMODE_OCT = {}
for _p in BPAY_OCT: BMODE_OCT[_p[3]] = BMODE_OCT.get(_p[3], 0) + _p[2]
assert len(BPAY_OCT) == 5 and BPAID_OCT == 559500 and BMODE_OCT == {'Bank Transfer': 205000, 'Cheque': 258500, 'Net Banking': 96000}
BPAID_MONTH = [510000, 585000, 500000, 610000, 605000, BPAID_OCT]

# ---- Tertiary sale lines: October sheets sold to retailers by product (CAL = the six quantities on Inventory Item Details) ----
TSOLD = {'LM-WNT-001': 60, 'LM-ARC-002': 85, 'LM-CAL-003': 33, 'LM-OAK-004': 25, 'LM-SLT-005': 15, 'LM-TEK-006': 40, 'LM-CHR-007': 18, 'LM-IVR-008': 35,
         'LM-STN-009': 0, 'LM-CPR-010': 7, 'LM-WNG-011': 30, 'LM-SKY-012': 22}
assert sum(TSOLD.values()) == 370 and TSOLD['LM-CAL-003'] == BCAL_SOLD
_w = {s: q * rp(s) for s, q in TSOLD.items()}
TSOLD_VALUE = {s: round(630000 * w / sum(_w.values())) for s, w in _w.items()}
_big = max(TSOLD_VALUE, key=TSOLD_VALUE.get); TSOLD_VALUE[_big] += 630000 - sum(TSOLD_VALUE.values())
assert sum(TSOLD_VALUE.values()) == 630000
_left = {s: q for s, q in TSOLD.items() if s != 'LM-CAL-003' and q}
_queue = []
while any(_left.values()):
    for _k in _left:
        if _left[_k]: _t = min(10, _left[_k]); _queue.append([_k, _t]); _left[_k] -= _t
_qi = 0
for _s in reversed(TSALES):                                                                   # oldest first
    _c = _CAL_RETAIL.get(_s['number'], 0); _s['lines'] = [('LM-CAL-003', _c)] if _c else []
    _need = _s['sheets'] - _c
    while _need > 0:
        _take = min(_need, _queue[_qi][1]); _same = [n for n, l in enumerate(_s['lines']) if l[0] == _queue[_qi][0]]
        if _same: _s['lines'][_same[0]] = (_queue[_qi][0], _s['lines'][_same[0]][1] + _take)
        else: _s['lines'].append((_queue[_qi][0], _take))
        _queue[_qi][1] -= _take; _need -= _take
        if _queue[_qi][1] == 0: _qi += 1
assert all(q == 0 for _, q in _queue) and all(sum(q for _, q in s['lines']) == s['sheets'] for s in TSALES)
_chk = {}
for _s in TSALES:
    for _k, _q in _s['lines']: _chk[_k] = _chk.get(_k, 0) + _q
assert all(_chk.get(k, 0) == v for k, v in TSOLD.items())
# Stock must be possible: on hand now - October receipts from delivered orders + October sales to retailers >= 0
B_RECV = {}
for _s in BRV_SALES:
    if _s['status'] == 'Delivered':
        for _k, _q in _s['lines']: B_RECV[_k] = B_RECV.get(_k, 0) + _q
B_OPENING = {s: BSTOCK[s]['on_hand'] - B_RECV.get(s, 0) + TSOLD[s] for s in BSTOCK}
assert all(v >= 0 for v in B_OPENING.values()) and B_OPENING['LM-CAL-003'] == BCAL_OPEN
# Ageing of Bravo's stock (up to 30 days / 31 to 60 / over 60); everything received in October is in the youngest band
def b_ageing(s):
    on = BSTOCK[s]['on_hand']
    if s == 'LM-CAL-003': return (25, 13, 0)                                                   # batches B-2610-19 (10/10) and B-2609-08 (12/09)
    a = min(on, max(round(on * 0.62 / 5) * 5, B_RECV.get(s, 0))); b = min(round(on * 0.26 / 5) * 5, on - a)
    return (a, b, on - a - b)
BAGE = {s: b_ageing(s) for s in BSTOCK}
assert all(sum(v) == BSTOCK[s]['on_hand'] and min(v) >= 0 and v[0] >= min(B_RECV.get(s, 0), BSTOCK[s]['on_hand']) for s, v in BAGE.items())

# ---- Returns to Distributor Alpha: number, date, order, sku, sheets, reason, status. Credit (only once issued) = sheets x dealer price ----
BRET = [('RTN-2026-D0508', '22/10/2026', 'SAL-2026-3033', 'LM-WNT-001', 6, 'Surface Defect', 'Under Review'), ('RTN-2026-D0503', '16/10/2026', 'SAL-2026-3029', 'LM-TEK-006', 4, 'Damaged in Transit', 'Approved'),
        ('RTN-2026-D0494', '14/10/2026', 'SAL-2026-3021', 'LM-OAK-004', 3, 'Damaged in Transit', 'Credit Issued'), ('RTN-2026-D0486', '09/10/2026', 'SAL-2026-3017', 'LM-CPR-010', 2, 'Surface Defect', 'Credit Issued'),
        ('RTN-2026-D0479', '04/10/2026', 'SAL-2026-3010', 'LM-ARC-002', 5, 'Shade Mismatch', 'Rejected')]
_lines = {s['number']: dict(s['lines']) for s in BRV_SALES}
assert all(r[3] in _lines[r[2]] and r[4] <= _lines[r[2]][r[3]] for r in BRET)
BCREDIT = {r[0]: r[4] * dp(r[3]) for r in BRET if r[6] == 'Credit Issued'}
assert BCREDIT == {'RTN-2026-D0494': 4095, 'RTN-2026-D0486': 4160} and sum(BCREDIT.values()) == 8255
assert [pd(r[1]) for r in BRET] == sorted(pd(r[1]) for r in BRET)[::-1]

# ---- Support tickets with Distributor Alpha: number, created, subject, category, priority, updated, status ----
BTK = [('TKT-2026-D0746', '25/10/2026', 'Delivery Timing for SAL-2026-3040', 'Delivery', 'Medium', '26/10/2026', 'In Progress'),
       ('TKT-2026-D0737', '23/10/2026', 'Price Tier Review Request', 'Account', 'Low', '23/10/2026', 'Open'),
       ('TKT-2026-D0719', '18/10/2026', 'Surface Defect in SAL-2026-3033', 'Delivery', 'High', '22/10/2026', 'Resolved'),
       ('TKT-2026-D0696', '10/10/2026', 'Invoice SAL-2026-3021 Amount Query', 'Billing', 'Medium', '13/10/2026', 'Closed'),
       ('TKT-2026-D0661', '30/09/2026', 'Festive Scheme Eligibility', 'Schemes', 'Low', '01/10/2026', 'Closed')]
assert [pd(t[1]) for t in BTK] == sorted((pd(t[1]) for t in BTK), reverse=True) and [t[0] for t in BTK] == sorted((t[0] for t in BTK), reverse=True)

# ---- Users of Dealer Bravo (the portal has two roles: Owner, Sales and Inventory Manager): name, role, phone, last sign-in, status ----
BUSERS = [('Sunita Rao', 'Owner', '31001', '26/10/2026 09:12', 'Active'), ('Arjun Nair', 'Sales and Inventory Manager', '31002', '26/10/2026 08:55', 'Active'),
          ('Meena Kulkarni', 'Sales and Inventory Manager', '31004', 'Not yet', 'Invited'), ('Rohit Pawar', 'Sales and Inventory Manager', '31005', '30/06/2026', 'Inactive')]

# ---- Dealer schemes issued by Distributor Alpha (Schemes and Incentives): number, name, type, start, end, status, done, goal, reward ----
BSCH = [SCH_FESTIVE[:2] + ('Volume Rebate', '01/10/2026', '30/11/2026', 'Active', 690, 750, '1% rebate'),
        SCH_MARBLE[:2] + ('Product Incentive', '01/10/2026', '31/12/2026', 'Active', 50, 100, f'{M(750)} earned'),
        ('SCH-2026-09', 'Winter Season Dealer Bonus', 'Volume Bonus', '01/12/2026', '31/01/2027', 'Upcoming', 0, 1400, '2% bonus'),
        ('SCH-2026-03', 'Monsoon Dealer Incentive', 'Volume Incentive', '01/07/2026', '30/09/2026', 'Completed', 1310, 1200, f'{M(13100)} credited')]
assert 50 * 15 == 750 and 1310 * 10 == 13100
B_INCENTIVES = 750 + 13100
