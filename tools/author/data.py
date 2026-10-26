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
    """Compact money with full words, for stat tiles, charts and summaries: 3352882 -> ₹33.53 lakh"""
    if n >= 10000000: return f'\u20b9{n/10000000:.2f} crore'
    if n >= 100000: return f'\u20b9{n/100000:.2f} lakh'
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
