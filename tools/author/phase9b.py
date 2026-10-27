"""Phase 9, part B: Tertiary Customer Retailer Owner: Return Requests, Create Return Request, Support Ticket List, Create Support Ticket, Support Ticket Details (the three
support screens are shared with the Sales Executive), User Management, Create User, User Details, and My Profile and Notifications (shared with both Executives via
?role=SLS / ?role=PUR). Retailer Charlie, Camp, Pune; supplier Dealer Bravo. Design rule: no text under page titles, no captions beside card titles, no helper sentences.
Data: docs/DATA.md "Phase 8 data" and "Phase 9 data"."""
from data import *

SQ = chr(0x2212)
def cancel(sid): return f'<a class="btn" data-link="{sid}">Cancel</a>'
em = lambda n: n.lower().replace(' ', '.') + '@retailercharlie.example'
def radio(title, on=False, name='r'):
    return f'<label class="radio{" on" if on else ""}"><input type="radio" name="{name}"{" checked" if on else ""}><span><b>{title}</b></span></label>'

# ---------- Return Requests ----------
OPEN = ('Under Review', 'Approved', 'Pickup Scheduled')
RET_CHIP = {'Credit Issued': 'ok', 'Approved': 'blue', 'Under Review': 'warn', 'Rejected': 'bad'}
rows = [f'<tr><td class="mono nowrap"><b>{r[0]}</b></td><td>{r[1]}</td><td class="mono nowrap"><a data-link="TER-ORD-02">{r[2]}</a></td><td>{BY[r[3]][1]}</td><td class="num">{r[4]}</td><td>{r[5]}</td><td>{chip(r[6], RET_CHIP[r[6]])}</td><td class="num">{M(CCREDIT[r[0]]) if r[0] in CCREDIT else "—"}</td></tr>' for r in CRET]
body = f'''  <div class="head">
    <h1>Return Requests</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Requests</button><a class="btn pri" data-link="TER-RET-02"><i data-icon="plus"></i>Create Return Request</a></div>
  </div>
  <div class="kpis">
    {kpi('Open Requests', str(sum(1 for r in CRET if r[6] in OPEN)))}
    {kpi('Sheets Under Return', str(sum(r[4] for r in CRET if r[6] in OPEN)))}
    {kpi('Credit Issued', M(sum(CCREDIT.values())), chip('2 requests', 'plain'))}
    {kpi('Requests This Year', str(len(CRET)))}
  </div>
  <section class="card flush">
    {tabs([('All Requests', len(CRET), True), ('Open', 2, False), ('Credit Issued', 2, False)])}
    {filters('Search by return or order number', 'Search return requests', ('Date Range', 'Last 90 days'), ('Reason', 'All'))}
    <div class="body">{table([('Return Number', ''), ('Date', ''), ('Order Number', ''), ('Product', ''), ('Sheets', 'num'), ('Reason', ''), ('Status', ''), ('Credit Amount', 'num')], rows, 'wrap')}
      {pager(f'Showing 1 to {len(CRET)} of {len(CRET)} requests', 1)}</div>
  </section>
'''
page('tertiary', 'return-requests', 'TER-RET-01', 'Tertiary Customer — Retailer Owner — Return Requests (TER-RET-01)', body)

# ---------- Create Return Request ----------
o09 = next(s for s in CHR_TS if s['number'] == 'TSL-2026-0409')
RQ = {'LM-IVR-008': 2, 'LM-WNT-001': 1}
assert all(q <= dict(o09['lines'])[s] for s, q in RQ.items())
lines = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num">{N(q)}</td><td>{qty(RQ.get(s, 0))}</td></tr>' for s, q in o09['lines'])
body = f'''  <div class="head">
    <h1>Create Return Request</h1>
    <div class="acts">{cancel('TER-RET-01')}<button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Submit Return Request</button></div>
  </div>
  <div class="grid g-main-side" style="--side:20rem">
    <div class="stack">
      {form('Return Details', fld('Order', 'ord', 'TSL-2026-0409', 'select', [s['number'] for s in CHR_TS]), fld('Return Reason', 'rs', 'Shade Mismatch', 'select', ['Damaged in Transit', 'Surface Defect', 'Wrong Product Delivered', 'Shade Mismatch']),
            fld('Pickup Location', 'pl', 'Shop 12, MG Road, Camp', 'select', ['Shop 12, MG Road, Camp']), fld('Contact for Pickup', 'cp', 'Faisal Khan, +91 90000 51003'))}
      <section class="card flush"><header><h2>Items to Return</h2></header><div class="body">{table([('Product', ''), ('SKU', ''), ('Ordered Sheets', 'num'), ('Sheets to Return', '')], [lines], 'stack-sm')}</div></section>
      <section class="card"><header><h2>Photos</h2></header><div class="body"><div class="drop"><span class="file"><i data-icon="doc"></i>shade-mismatch-1.jpg</span><span class="file"><i data-icon="doc"></i>shade-mismatch-2.jpg</span><button class="btn sm" type="button"><i data-icon="upload"></i>Upload Photos</button></div></div></section>
      <section class="card"><header><h2>Notes</h2></header><div class="body"><div class="field"><label for="nt">Notes for Dealer Bravo</label><textarea class="input" id="nt" placeholder="Describe the issue"></textarea></div></div></section>
    </div>
    <div class="stack">
      <section class="card"><header><h2>Preferred Resolution</h2></header><div class="body"><div class="stack">{radio('Credit Note', True, 'res')}{radio('Replacement Sheets', False, 'res')}</div></div></section>
      {card('Return Summary', kv([('Order', '<span class="mono">TSL-2026-0409</span>'), ('Products', '2'), ('Sheets to Return', str(sum(RQ.values()))), ('Pickup Location', 'Shop 12, MG Road, Camp')]))}
    </div>
  </div>
'''
page('tertiary', 'create-return-request', 'TER-RET-02', 'Tertiary Customer — Retailer Owner — Create Return Request (TER-RET-02)', body)

# ---------- Support Ticket List (shared with the Sales Executive) ----------
rows = [f'<tr><td class="mono nowrap">{link("TER-SUP-03", t[0])}</td><td>{t[2]}</td><td>{t[3]}</td><td>{chip(t[4])}</td><td>{t[1]}</td><td>{t[5]}</td><td>{chip(t[6])}</td></tr>' for t in CTK]
body = f'''  <div class="head">
    <h1>Support Ticket List</h1>
    <div class="acts"><a class="btn pri" data-link="TER-SUP-02"><i data-icon="plus"></i>Create Support Ticket</a></div>
  </div>
  <div class="kpis">
    {kpi('Open Tickets', '2')}
    {kpi('In Progress', '1', chip('TKT-2026-B0452', 'blue'))}
    {kpi('Resolved This Month', '1')}
    {kpi('Closed', '2')}
  </div>
  <section class="card flush">
    {tabs([('All Tickets', len(CTK), True), ('Open', 2, False), ('Resolved', 1, False), ('Closed', 2, False)])}
    {filters('Search by ticket number or subject', 'Search tickets', ('Category', 'All'), ('Priority', 'All'))}
    <div class="body">{table([('Ticket Number', ''), ('Subject', ''), ('Category', ''), ('Priority', ''), ('Created', ''), ('Last Updated', ''), ('Status', '')], rows, 'wrap')}
      {pager(f'Showing 1 to {len(CTK)} of {len(CTK)} tickets', 1)}</div>
  </section>
'''
page('tertiary', 'support-ticket-list', 'TER-SUP-01', 'Tertiary Customer — Retailer Owner — Support Ticket List (TER-SUP-01)', body)

# ---------- Create Support Ticket ----------
orders = ['None'] + [s['number'] for s in CHR_TS]
body = f'''  <div class="head">
    <h1>Create Support Ticket</h1>
    <div class="acts">{cancel('TER-SUP-01')}<button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Submit Ticket</button></div>
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      {form('Ticket Details', fld('Subject', 'sb', 'Credit Note Missing for RTN-2026-B0186', full=True), fld('Category', 'cg', 'Billing', 'select', ['Delivery', 'Billing', 'Account', 'Schemes', 'Product']), fld('Priority', 'pr', 'Medium', 'select', ['Low', 'Medium', 'High']),
            fld('Related Order', 'ro', 'TSL-2026-0401', 'select', ['None', PEND_ORDER['number']] + orders[1:]), fld('Related Invoice', 'ri', 'TSL-2026-0401', 'select', ['None'] + [s['number'] for s in CHR_TS]),
            fld('Description', 'ds', f'The credit of {M(CCREDIT["RTN-2026-B0186"])} for return request RTN-2026-B0186 is not shown against invoice TSL-2026-0401.', 'textarea', full=True))}
      <section class="card"><header><h2>Attachments</h2></header><div class="body"><div class="drop"><span class="file"><i data-icon="doc"></i>credit-note.pdf</span><button class="btn sm" type="button"><i data-icon="upload"></i>Upload Files</button></div></div></section>
    </div>
    <div class="stack">
      {card('Dealer Bravo Support', kv([('Relationship Manager', 'Arjun Nair'), ('Phone', '+91 90000 31002'), ('Email', 'arjun.nair@<wbr>dealerbravo.example'), ('Support Hours', 'Monday to Saturday, 09:30 to 18:30')]))}
    </div>
  </div>
'''
page('tertiary', 'create-support-ticket', 'TER-SUP-02', 'Tertiary Customer — Retailer Owner — Create Support Ticket (TER-SUP-02)', body)

# ---------- Support Ticket Details (TKT-2026-B0452) ----------
def msg(who, init, when, text, me=False, files=()):
    fl = f'<div class="files">{"".join(f"<span class=file><i data-icon=doc></i>{f}</span>" for f in files)}</div>' if files else ''
    return f'<div class="msg{" me" if me else ""}"><div class="av">{init}</div><div><div class="top-line"><b>{who}</b><time>{when}</time></div><div class="bubble">{text}{fl}</div></div></div>'
v = O12['vehicle']
thread = ''.join([
    msg('Imran Sheikh', 'IS', '25/10/2026 17:40', 'TSL-2026-0412 was confirmed today. Please let us know when it will be delivered to the shop.', True, ['order-copy.pdf']),
    msg('Arjun Nair, Dealer Bravo', 'AN', '25/10/2026 18:10', 'The order will be packed on Monday 26 October and delivered on 27 October.'),
    msg('Imran Sheikh', 'IS', '26/10/2026 10:20', 'Thank you. Please share the vehicle and driver details.', True),
    msg('Arjun Nair, Dealer Bravo', 'AN', '26/10/2026 10:45', f'The vehicle is {v[0]} and the driver is {v[2]}, {v[3]}. Delivery is expected on 27 October.'),
])
t0 = CTK[0]
body = f'''  <div class="head">
    <div class="title-row"><h1>{t0[2]}</h1>{chip(t0[6])}{chip(t0[4])}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="check"></i>Close Ticket</button></div>
  </div>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      {card('Conversation', f'<div class="thread">{thread}</div>')}
      <section class="card"><header><h2>Reply</h2></header><div class="body"><div class="reply"><textarea class="input" aria-label="Reply" placeholder="Write a reply"></textarea>
        <div class="row"><button class="btn" type="button"><i data-icon="upload"></i>Attach Files</button><button class="btn pri" type="button">Send Reply</button></div></div></div></section>
    </div>
    <div class="stack">
      {card('Ticket Information', kv([('Ticket Number', f'<span class="mono">{t0[0]}</span>'), ('Status', chip(t0[6])), ('Priority', chip(t0[4])), ('Category', t0[3]), ('Created', '25/10/2026 17:40'), ('Last Updated', '26/10/2026 10:45'), ('Assigned To', 'Arjun Nair')]))}
      <div data-role="OWN">{card('Related Records', kv([('Order', link('TER-ORD-02', 'TSL-2026-0412', False)), ('Invoice', link('TER-BIL-02', 'TSL-2026-0412', False))], ''))}</div>
    </div>
  </div>
'''
page('tertiary', 'support-ticket-details', 'TER-SUP-03', 'Tertiary Customer — Retailer Owner — Support Ticket Details (TER-SUP-03)', body)

# ---------- User Management ----------
rows = [f'<tr><td>{link("TER-USR-03", u[0])}</td><td>{u[1]}</td><td class="nowrap">{em(u[0])}</td><td class="nowrap">{u[3]}</td><td>{chip(u[4])}</td><td><div class="row-actions"><a class="btn sm" data-link="TER-USR-03">View</a></div></td></tr>' for u in CUSERS]
body = f'''  <div class="head">
    <h1>User Management</h1>
    <div class="acts"><a class="btn pri" data-link="TER-USR-02"><i data-icon="plus"></i>Create User</a></div>
  </div>
  <div class="kpis">
    {kpi('Users', str(len(CUSERS)))}
    {kpi('Active', '3')}
    {kpi('Invited', '1')}
    {kpi('Inactive', '1')}
  </div>
  <section class="card flush">
    {tabs([('All Users', len(CUSERS), True), ('Active', 3, False), ('Invited', 1, False), ('Inactive', 1, False)])}
    {filters('Search by name or email address', 'Search users', ('Role', 'All'))}
    <div class="body">{table([('Name', ''), ('Role', ''), ('Email Address', ''), ('Last Sign-In', ''), ('Status', ''), ('', '')], rows, 'wrap')}</div>
  </section>
'''
page('tertiary', 'user-management', 'TER-USR-01', 'Tertiary Customer — Retailer Owner — User Management (TER-USR-01)', body)

# ---------- Create User ----------
MODS = [('Product Catalogue', 1, 1, 1), ('Orders and Purchase History', 1, 0, 1), ('Inventory', 1, 1, 1), ('Stock Movements and Reorders', 1, 0, 1), ('Retail Sales', 1, 1, 0), ('Invoices and Payments', 1, 0, 0),
        ('Offers', 1, 0, 0), ('Reports', 1, 0, 0), ('Return Requests', 1, 0, 0), ('Support Tickets', 1, 1, 0), ('User Management', 1, 0, 0), ('Store Profile', 1, 0, 0), ('My Profile and Notifications', 1, 1, 1)]
tick = lambda v_: '<i data-icon="check"></i>' if v_ else '<span class="no">—</span>'
mrows = [f'<tr><td><b>{m[0]}</b></td><td class="c">{tick(m[1])}</td><td class="c">{tick(m[2])}</td><td class="c">{tick(m[3])}</td></tr>' for m in MODS]
mtable = table([('Area', ''), ('Retailer Owner', 'c'), ('Sales Executive', 'c'), ('Inventory and Purchasing Executive', 'c')], mrows, 'wrap')
body = f'''  <div class="head">
    <h1>Create User</h1>
    <div class="acts">{cancel('TER-USR-01')}<button class="btn pri" type="button">Send Invitation</button></div>
  </div>
  <div class="grid g-main-side" style="--side:20rem">
    {form('Personal Details', fld('First Name', 'fn', 'Mohit'), fld('Last Name', 'ln', 'Gawande'), fld('Email Address', 'em', em('Mohit Gawande')), fld('Mobile Number', 'mb', '+91 90000 51004'))}
    <section class="card"><header><h2>Role</h2></header><div class="body"><div class="stack">{radio('Retailer Owner', False, 'role')}{radio('Sales Executive', True, 'role')}{radio('Inventory and Purchasing Executive', False, 'role')}</div></div></section>
  </div>
  <section class="card flush"><header><h2>Access by Role</h2></header><div class="body">{mtable}</div></section>
'''
page('tertiary', 'create-user', 'TER-USR-02', 'Tertiary Customer — Retailer Owner — Create User (TER-USR-02)', body)

# ---------- User Details (Pooja Verma) ----------
mine = [s for s in CSALES if s['by'] == 'Pooja Verma']
act = [(f'{s["date"]} {s["time"]}', f'Recorded sale {s["number"]}') for s in mine[:2]] + [('26/10/2026 09:40', 'Signed in')] + [(f'{s["date"]} {s["time"]}', f'Recorded sale {s["number"]}') for s in mine[2:4]]
assert [a[0] for a in act] == sorted((a[0] for a in act), key=lambda d: (pd(d[:10]), d[11:]), reverse=True)
arows = [f'<tr><td class="nowrap">{d}</td><td><b>{a}</b></td></tr>' for d, a in act]
accrows = [f'<tr><td><b>{m[0]}</b></td><td class="c">{tick(m[2])}</td></tr>' for m in MODS]
body = f'''  <div class="head">
    <div class="title-row"><h1>Pooja Verma</h1>{chip('Active')}<span class="tag">Sales Executive</span></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="lock"></i>Reset Password</button><button class="btn" type="button"><i data-icon="edit"></i>Edit User</button><button class="btn danger" type="button">Deactivate User</button></div>
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      {card('Profile', kv([('Full Name', 'Pooja Verma'), ('Email Address', em('Pooja Verma')), ('Mobile Number', '+91 90000 51002'), ('Role', 'Sales Executive'), ('Added On', '14/03/2023'), ('Added By', 'Imran Sheikh'), ('Last Sign-In', '26/10/2026 09:40')]))}
      <section class="card flush"><header><h2>Recent Activity</h2></header><div class="body">{table([('Date', ''), ('Activity', '')], arows)}</div></section>
    </div>
    <section class="card flush"><header><h2>Access</h2></header><div class="body">{table([('Area', ''), ('Access', 'c')], accrows)}</div></section>
  </div>
'''
page('tertiary', 'user-details', 'TER-USR-03', 'Tertiary Customer — Retailer Owner — User Details (TER-USR-03)', body)

# ---------- My Profile (all three roles) ----------
PEOPLE = [('OWN', 'Imran Sheikh', '+91 90000 51001', '26/10/2026 09:02'), ('SLS', 'Pooja Verma', '+91 90000 51002', '26/10/2026 09:40'), ('PUR', 'Faisal Khan', '+91 90000 51003', '26/10/2026 09:15')]
assert all(u[3] == p[3] for u in CUSERS for p in PEOPLE if u[0] == p[1])
def per_role(fn): return ''.join(f'<div data-role="{r}">{fn(r, n, ph, ls)}</div>' for r, n, ph, ls in PEOPLE)
def pform(r, n, ph, ls):
    return f'<div class="form-grid">{fld("Full Name", "nm" + r, n)}{fld("Mobile Number", "mb" + r, ph)}{fld("Email Address", "em" + r, em(n), full=True)}{fld("Language", "lg" + r, "English", "select", ["English", "Hindi", "Marathi"], full=True)}</div>'
prefs = [('Order Updates', 1, 1), ('Invoice and Payment Updates', 1, 1), ('Stock Alerts', 1, 1), ('Offer Announcements', 0, 1), ('Support Replies', 1, 1)]
prow = [f'<tr><td><b>{e}</b></td><td class="c"><label class="check"><input type="checkbox"{" checked" if a else ""} aria-label="{e} by email"></label></td><td class="c"><label class="check"><input type="checkbox"{" checked" if b else ""} aria-label="{e} in the portal"></label></td></tr>' for e, a, b in prefs]
sess = [('Chrome on Windows', 'Pune', chip('Current Session', 'ok')), ('Chrome on Android', 'Pune', '25/10/2026 19:12'), ('Safari on iPhone', 'Pune', '22/10/2026 08:03')]
srow = [f'<tr><td class="nowrap"><b>{a}</b></td><td>{b}</td><td class="nowrap">{c}</td></tr>' for a, b, c in sess]
body = f'''  <div class="head">
    <h1>My Profile</h1>
    <div class="acts"><button class="btn" type="button">Cancel</button><button class="btn pri" type="button">Save Changes</button></div>
  </div>
  <section class="card pad" style="flex-direction:row;align-items:center;gap:1.25rem;flex-wrap:wrap">
    <div class="av-lg" data-me="initials"></div>
    <div style="flex:1;min-width:14rem;display:grid;gap:.5rem"><h2 style="font-size:1.25rem" data-me="name"></h2>
      <div style="display:flex;flex-wrap:wrap;gap:.5rem">{chip('Active', 'ok')}<span class="tag" data-me="role"></span></div></div>
    <dl class="kv left" style="grid-template-columns:auto auto;gap:.5rem 1.25rem"><dt>Organisation</dt><dd>Retailer Charlie</dd><dt>Last Sign-In</dt><dd>{per_role(lambda r, n, ph, ls: ls).replace('<div', '<span').replace('</div>', '</span>')}</dd></dl>
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
page('tertiary', 'my-profile', 'TER-PRO-02', 'Tertiary Customer — Retailer Owner — My Profile (TER-PRO-02)', body)

# ---------- Notifications (three unread for each role, matching the bell badge) ----------
def n(sid, title, ref, when, icon, kind='', unread=False):
    return (f'<li{" class=unread" if unread else ""}><span class="dot {kind}"><i data-icon="{icon}"></i></span><div class="title"><a data-link="{sid}">{title}</a><span class="tag mono">{ref}</span></div><time>{when}</time></li>')
def day(label, *items): return f'<div class="day">{label}</div><ul class="feed ntf">{"".join(items)}</ul>'
OWN = (day('Today', n('TER-ORD-02', 'Order Submitted', PEND_ORDER['number'], '11:20', 'cart', '', True), n('TER-SUP-03', 'New Reply on Support Ticket', 'TKT-2026-B0452', '10:45', 'help', '', True), n('TER-INV-02', 'Low Stock', 'LM-CAL-003', '08:30', 'warn', 'warn', True))
       + day('25 October 2026', n('TER-ORD-02', 'Order Confirmed', 'TSL-2026-0412', '17:20', 'truck'), n('TER-RET-01', 'Return Request Submitted', 'RTN-2026-B0214', '14:30', 'ret'))
       + day('23 October 2026', n('TER-BIL-05', 'Payment Confirmed', 'PAY-2026-B0388', '10:05', 'cash', 'ok')))
SLS = (day('Today', n('TER-INV-02', 'Low Stock', 'LM-CAL-003', '08:30', 'warn', 'warn', True), n('TER-INV-02', 'Low Stock', 'LM-CHR-007', '08:30', 'warn', 'warn', True), n('TER-SUP-03', 'New Reply on Support Ticket', 'TKT-2026-B0452', '10:45', 'help', '', True))
       + day('24 October 2026', n('TER-RTS-03', 'Sale Recorded', 'RSL-2026-0395', '11:03', 'trend')))
PUR = (day('Today', n('TER-ORD-02', 'Order Submitted', PEND_ORDER['number'], '11:20', 'cart', '', True), n('TER-INV-02', 'Low Stock', 'LM-CAL-003', '08:30', 'warn', 'warn', True), n('TER-INV-06', 'Delivery Arriving Tomorrow', 'TSL-2026-0412', '08:00', 'truck', '', True))
       + day('20 October 2026', n('TER-ORD-02', 'Order Delivered', 'TSL-2026-0409', '14:20', 'truck', 'ok')))
body = f'''  <div class="head">
    <h1>Notifications</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="check"></i>Mark All as Read</button></div>
  </div>
  <section class="card flush">
    <div style="padding:0 1.125rem"><div class="tabs"><span class="on">All Notifications<b data-count=".ntf li"></b></span><span>Unread<b data-count=".ntf li.unread"></b></span></div></div>
    <div class="body" style="padding:0 1.125rem 1rem"><div data-role="OWN">{OWN}</div><div data-role="SLS">{SLS}</div><div data-role="PUR">{PUR}</div></div>
  </section>
'''
page('tertiary', 'notifications', 'TER-NTF-01', 'Tertiary Customer — Retailer Owner — Notifications (TER-NTF-01)', body)
