"""Phase 12, part C: Company Administration: Territory Management, Audit Activity, Portal Settings (Super Admin), My Profile and Notifications (all three roles).
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md "Phase 12 data"."""
from data import *

# ---------- Territory Management ----------
def terr_status(a, t):
    v = a / t * 100
    return chip('Above Target') if v >= 100 else chip('Near Target') if v >= 95 else chip('Below Target')
trows = ''
for t in TERRITORIES:
    ach = t['sales'] / t['target'] * 100
    trows += (f'<tr><td><b>{t["name"]}</b></td><td class="num">{t["dealers"]}</td><td class="num">{t["retailers"]}</td><td class="num"><b>{M(t["sales"])}</b></td><td class="num">{M(t["target"])}</td>'
              f'<td><span class="inline-meter"><span class="meter {"ok" if ach >= 100 else "warn" if ach >= 95 else "bad"}"><i style="width:{min(ach, 100):.0f}%"></i></span><b>{ach:.1f}%</b></span></td><td>{terr_status(t["sales"], t["target"])}</td><td class="nowrap">Vikram Chopra</td></tr>')
tfoot = (f'<tfoot><tr><td>Total</td><td class="num">8</td><td class="num">20</td><td class="num">{M(3120000)}</td><td class="num">{M(TARGET_TOTAL)}</td><td><b>{3120000 / TARGET_TOTAL * 100:.1f}%</b></td><td colspan="2"></td></tr></tfoot>')
drows = ''.join(f'<tr><td>{link("CMP-CUS-02", d[1])}</td><td>{d[3]}</td><td>{d[2]}</td><td class="num">{d[6]}</td><td class="num"><b>{M(d[7])}</b></td><td class="nowrap">Kavita Joshi</td></tr>' for d in sorted(DEALERS, key=lambda d: (d[3], -d[7])))
assert sum(TARGET.values()) == TARGET_TOTAL and round(3120000 / TARGET_TOTAL * 100, 1) == 99.4
body = f'''  <div class="head">
    <h1>Territory Management</h1>
    <div class="acts"><span class="sel"><small>Period</small> October 2026 <i data-icon="down"></i></span><button class="btn" type="button"><i data-icon="edit"></i>Reassign Manager</button><button class="btn pri" type="button"><i data-icon="plus"></i>Create Territory</button></div>
  </div>
  <div class="kpis">
    {kpi('Territories', str(len(TERRITORIES)))}
    {kpi('Sales to Dealers', ML(3120000), up('11.8%'))}
    {kpi('Target', ML(TARGET_TOTAL))}
    {kpi('Target Achievement', f'{3120000 / TARGET_TOTAL * 100:.1f}%', chip('Near Target', 'warn'))}
  </div>
  {card('Sales Against Target by Territory', chart('bars', [t['name'] for t in TERRITORIES], [{'name': 'Sales to dealers', 'values': [t['sales'] for t in TERRITORIES], 'color': 'var(--accent)'}, {'name': 'Target', 'values': [t['target'] for t in TERRITORIES], 'color': 'var(--bad)'}], money=True, height=280))}
  <section class="card flush"><header><h2>Territories</h2></header>
    <div class="body">{table([('Territory', ''), ('Dealers', 'num'), ('Retailers', 'num'), ('Sales to Dealers', 'num'), ('Target', 'num'), ('Achievement', ''), ('Status', ''), ('Account Manager', '')], [trows], 'wrap', foot=tfoot)}</div></section>
  <section class="card flush"><header><h2>Dealers by Territory</h2></header>
    <div class="body">{table([('Dealer', ''), ('Territory', ''), ('City', ''), ('Retailers', 'num'), ('Sales This Month', 'num'), ('Distributor Manager', '')], [drows], 'wrap')}</div></section>
'''
page('company', 'territory-management', 'CMP-TER-01', 'Company Administration — Super Admin — Territory Management (CMP-TER-01)', body)

# ---------- Audit Activity ----------
arows = ''.join(f'<tr><td class="nowrap">{a[0]}</td><td class="nowrap"><b>{a[1]}</b></td><td>{a[2]}</td><td><span class="tag">{a[3]}</span></td><td>{a[4]}</td><td class="mono nowrap">{a[5]}</td></tr>' for a in AUDIT)
users = {a[1] for a in AUDIT}; staff = sum(1 for a in AUDIT if a[2] == 'Crestline Laminates')
body = f'''  <div class="head">
    <h1>Audit Activity</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Activity</button></div>
  </div>
  <div class="kpis">
    {kpi('Activities in Seven Days', str(len(AUDIT)))}
    {kpi('Users Active', str(len(users)))}
    {kpi('Crestline Staff Activities', str(staff))}
    {kpi('Customer Activities', str(len(AUDIT) - staff))}
  </div>
  <section class="card flush">
    {filters('Search by user, action or record', 'Search activity', ('Date Range', 'Last 7 Days'), ('User', 'All'), ('Area', 'All'), ('Organisation', 'All'))}
    <div class="body">{table([('Date and Time', ''), ('User', ''), ('Organisation', ''), ('Area', ''), ('Action', ''), ('Record', '')], [arows], 'wrap')}
      {pager(f'Showing 1 to {len(AUDIT)} of {len(AUDIT)} activities', 1)}</div>
  </section>
'''
page('company', 'audit-activity', 'CMP-AUD-01', 'Company Administration — Super Admin — Audit Activity (CMP-AUD-01)', body)

# ---------- Portal Settings ----------
tier_rows = ''.join(f'<tr><td><b>{t[0]}</b></td><td>{t[1]}</td><td>{t[2]}</td><td class="nowrap">{t[3]}</td><td class="num">{t[4]}</td></tr>' for t in CUST_TIERS)
EVENTS = [('Order Placed', 'Sales Manager, Super Admin', 1, 1), ('Order Confirmed', 'Customer', 1, 1), ('Shipment Dispatched', 'Customer, Operations Manager', 1, 1), ('Invoice Issued', 'Customer', 1, 1),
          ('Invoice Overdue', 'Customer, Super Admin', 1, 1), ('Low Stock', 'Operations Manager, Super Admin', 0, 1), ('Customer Request Waiting', 'Sales Manager, Super Admin', 1, 1), ('Support Ticket Reply', 'Customer', 1, 1)]
nrows = [f'<tr><td><b>{e}</b></td><td>{r}</td><td class="c"><label class="check"><input type="checkbox"{" checked" if a else ""} aria-label="{e} by email"></label></td><td class="c"><label class="check"><input type="checkbox"{" checked" if b else ""} aria-label="{e} in the portal"></label></td></tr>' for e, r, a, b in EVENTS]
body = f'''  <div class="head">
    <h1>Portal Settings</h1>
    <div class="acts"><button class="btn" type="button">Cancel</button><button class="btn pri" type="button">Save Settings</button></div>
  </div>
  <section class="card flush"><header><h2>Customer Tiers</h2></header><div class="body">{table([('Price Tier', ''), ('Applies To', ''), ('Price Basis', ''), ('Credit Period', ''), ('Customers', 'num')], [tier_rows], 'wrap')}</div></section>
  <div class="grid g-2">
    {form('Order Rules', fld('Free Freight Above', 'ff', '₹4,50,000'), fld('Freight Below That', 'fb', '₹4,500'), fld('Dispatch Lead Time', 'dl', '2 to 3 days'), fld('Order Confirmation', 'oc', 'Manual by Sales Manager', 'select', ['Manual by Sales Manager', 'Automatic']),
          fld('Credit Check on Orders', 'cc', 'Yes', 'select', ['Yes', 'No']), fld('Quantity Price Slabs', 'qs', '1 to 49, 50 to 199, 200 and above', full=True))}
    {form('Tax Settings', fld('GST Rate', 'gr', '18%'), fld('Central GST', 'cg', '9%'), fld('State GST', 'sg', '9%'), fld('Company GST Number', 'gn', '24AABCC7782M1Z4'), fld('Invoice Due After', 'id', '45 days', 'select', ['15 days', '30 days', '45 days']),
          fld('Issue Invoice On', 'io', 'Dispatch', 'select', ['Dispatch', 'Order Confirmation']))}
  </div>
  <section class="card flush"><header><h2>Notification Rules</h2></header><div class="body">{table([('Event', ''), ('Recipients', ''), ('Email', 'c'), ('In the Portal', 'c')], nrows, 'pref')}</div></section>
'''
page('company', 'portal-settings', 'CMP-SET-01', 'Company Administration — Super Admin — Portal Settings (CMP-SET-01)', body)

# ---------- My Profile (all three roles) ----------
PEOPLE = [('ADM', 'Anita Deshmukh', '+91 90000 11221', '26/10/2026 08:30'), ('SAL', 'Vikram Chopra', '+91 90000 11223', '26/10/2026 09:10'), ('OPS', 'Neha Kulkarni', '+91 90000 11222', '26/10/2026 08:45')]
em = lambda n: n.lower().replace(' ', '.') + '@crestlinelaminates.example'
def per_role(fn): return ''.join(f'<div data-role="{r}">{fn(r, n, ph, ls)}</div>' for r, n, ph, ls in PEOPLE)
def pform(r, n, ph, ls):
    return f'<div class="form-grid">{fld("Full Name", "nm" + r, n)}{fld("Mobile Number", "mb" + r, ph)}{fld("Email Address", "em" + r, em(n), full=True)}{fld("Language", "lg" + r, "English", "select", ["English", "Hindi", "Gujarati", "Marathi"], full=True)}</div>'
prefs = [('Order Updates', 1, 1), ('Customer Requests', 1, 1), ('Invoice and Payment Updates', 1, 1), ('Stock Alerts', 0, 1), ('Support Replies', 1, 1)]
prow = [f'<tr><td><b>{e}</b></td><td class="c"><label class="check"><input type="checkbox"{" checked" if a else ""} aria-label="{e} by email"></label></td><td class="c"><label class="check"><input type="checkbox"{" checked" if b else ""} aria-label="{e} in the portal"></label></td></tr>' for e, a, b in prefs]
sess = [('Chrome on Windows', 'Vapi', chip('Current Session', 'ok')), ('Chrome on Android', 'Mumbai', '25/10/2026 19:12'), ('Safari on iPhone', 'Ahmedabad', '22/10/2026 08:03')]
srow = [f'<tr><td class="nowrap"><b>{a}</b></td><td>{b}</td><td class="nowrap">{c}</td></tr>' for a, b, c in sess]
body = f'''  <div class="head">
    <h1>My Profile</h1>
    <div class="acts"><button class="btn" type="button">Cancel</button><button class="btn pri" type="button">Save Changes</button></div>
  </div>
  <section class="card pad" style="flex-direction:row;align-items:center;gap:1.25rem;flex-wrap:wrap">
    <div class="av-lg" data-me="initials"></div>
    <div style="flex:1;min-width:14rem;display:grid;gap:.5rem"><h2 style="font-size:1.25rem" data-me="name"></h2>
      <div style="display:flex;flex-wrap:wrap;gap:.5rem">{chip('Active', 'ok')}<span class="tag" data-me="role"></span></div></div>
    <dl class="kv left" style="grid-template-columns:auto auto;gap:.5rem 1.25rem"><dt>Organisation</dt><dd>Crestline Laminates</dd><dt>Last Sign-In</dt><dd>{per_role(lambda r, n, ph, ls: ls).replace('<div', '<span').replace('</div>', '</span>')}</dd></dl>
  </section>
  <div class="grid g-2">
    <section class="card"><header><h2>Personal Details</h2></header><div class="body">{per_role(pform)}</div></section>
    <section class="card"><header><h2>Change Password</h2></header><div class="body"><div class="form-grid">
      <div class="field full"><label for="cur">Current Password</label><input class="input" id="cur" type="password" value="password"></div>
      <div class="field"><label for="new">New Password</label><input class="input" id="new" type="password" value="password"></div>
      <div class="field"><label for="con">Confirm New Password</label><input class="input" id="con" type="password" value="password"></div></div>
      <button class="btn block" type="button" style="margin-top:1rem"><i data-icon="lock"></i>Update Password</button></div></section>
  </div>
  <div class="grid g-2">
    <section class="card flush"><header><h2>Notification Preferences</h2></header><div class="body">{table([('Notification', ''), ('Email', 'c'), ('In the Portal', 'c')], prow, 'pref')}</div></section>
    <section class="card flush"><header><h2>Signed-In Devices</h2></header><div class="body">{table([('Device', ''), ('City', ''), ('Last Active', '')], srow)}</div></section>
  </div>
'''
page('company', 'my-profile', 'CMP-PRO-02', 'Company Administration — Super Admin — My Profile (CMP-PRO-02)', body)

# ---------- Notifications (three unread for each role, matching the bell badge) ----------
def n(sid, title, ref, when, icon, kind='', unread=False):
    return (f'<li{" class=unread" if unread else ""}><span class="dot {kind}"><i data-icon="{icon}"></i></span><div class="title"><a data-link="{sid}">{title}</a><span class="tag mono">{ref}</span></div><time>{when}</time></li>')
def day(label, *items): return f'<div class="day">{label}</div><ul class="feed ntf">{"".join(items)}</ul>'
ADM = (day('Today', n('CMP-ORD-02', 'Order Submitted', 'ORD-2026-10482', '11:42', 'cart', '', True), n('CMP-CUS-03', 'Customer Request Waiting', 'DRQ-2026-0017', '09:00', 'user', 'warn', True),
           n('CMP-BIL-01', 'Invoice Overdue', 'INV-2026-02986', '08:00', 'warn', 'bad'), n('CMP-INV-01', 'Low Stock', 'LM-STN-009', '07:45', 'warn', 'warn', True))
       + day('Yesterday', n('CMP-SUP-02', 'Customer Replied on Support Ticket', 'TKT-2026-0731', '11:20', 'help'))
       + day('24 October 2026', n('CMP-BIL-02', 'Invoice Issued', 'INV-2026-03318', '06:32', 'receipt'))
       + day('22 October 2026', n('CMP-BIL-01', 'Payment Confirmed', 'PAY-2026-02217', '16:30', 'cash', 'ok')))
SAL = (day('Today', n('CMP-ORD-02', 'Order Submitted', 'ORD-2026-10482', '11:42', 'cart', '', True), n('CMP-SCH-02', 'Scheme Target Reached', 'SCH-2026-04', '09:15', 'tag', 'ok', True),
           n('CMP-CUS-03', 'Customer Request Waiting', 'DRQ-2026-0017', '09:00', 'user', 'warn', True))
       + day('23 October 2026', n('CMP-ORD-02', 'Order Confirmed', 'ORD-2026-10459', '16:10', 'cart', 'ok'))
       + day('20 October 2026', n('CMP-ORD-02', 'Order Confirmed', 'ORD-2026-10447', '09:40', 'cart', 'ok')))
OPS = (day('Today', n('CMP-ORD-02', 'Packing Due Today', 'ORD-2026-10459', '08:00', 'box', 'warn', True), n('CMP-DSP-01', 'Shipment Arriving Tomorrow', 'DSP-2026-5521', '08:00', 'truck', '', True),
           n('CMP-INV-01', 'Low Stock', 'LM-STN-009', '07:45', 'warn', 'warn', True))
       + day('Yesterday', n('CMP-OPS-06', 'Return Request Submitted', 'RTN-2026-0412', '11:20', 'ret'))
       + day('24 October 2026', n('CMP-DSP-01', 'Shipment Dispatched', 'DSP-2026-5521', '06:30', 'truck', 'ok'))
       + day('23 October 2026', n('CMP-ORD-02', 'Order Confirmed', 'ORD-2026-10459', '16:10', 'cart', 'ok')))
body = f'''  <div class="head">
    <h1>Notifications</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="check"></i>Mark All as Read</button></div>
  </div>
  <section class="card flush">
    <div style="padding:0 1.125rem"><div class="tabs"><span class="on">All Notifications<b data-count=".ntf li"></b></span><span>Unread<b data-count=".ntf li.unread"></b></span></div></div>
    <div class="body" style="padding:0 1.125rem 1rem"><div data-role="ADM">{ADM}</div><div data-role="SAL">{SAL}</div><div data-role="OPS">{OPS}</div></div>
  </section>
'''
page('company', 'notifications', 'CMP-NTF-01', 'Company Administration — Super Admin — Notifications (CMP-NTF-01)', body)
