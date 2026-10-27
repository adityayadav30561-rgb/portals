"""Phase 3, part C: Primary Customer Owner: Return Requests, Create Return Request, Support Ticket List, Create Support Ticket,
Support Ticket Details, User Management, Create User, User Details; shared with other roles: My Profile, Notifications.
Design rule: no text under page titles, no captions beside card titles, no helper sentences. Data: docs/DATA.md."""
from data import *

def cancel(sid): return f'<a class="btn" data-link="{sid}">Cancel</a>'

# ---------- Return Requests ----------
RET = [  # number, date, order, sku, sheets, reason, status
 ('RTN-2026-0412', '25/10/2026', 'ORD-2026-10431', 'LM-CAL-003', 12, 'Damaged in Transit', 'Under Review'),
 ('RTN-2026-0408', '22/10/2026', 'ORD-2026-10431', 'LM-WNT-001', 8, 'Surface Defect', 'Approved'),
 ('RTN-2026-0396', '16/10/2026', 'ORD-2026-10398', 'LM-ARC-002', 20, 'Wrong Product Delivered', 'Pickup Scheduled'),
 ('RTN-2026-0377', '09/10/2026', 'ORD-2026-10372', 'LM-OAK-004', 15, 'Damaged in Transit', 'Credit Issued'),
 ('RTN-2026-0361', '02/10/2026', 'ORD-2026-10341', 'LM-CHR-007', 10, 'Surface Defect', 'Credit Issued'),
 ('RTN-2026-0342', '26/09/2026', 'ORD-2026-10316', 'LM-SLT-005', 6, 'Shade Mismatch', 'Rejected'),
 ('RTN-2026-0319', '18/09/2026', 'ORD-2026-10290', 'LM-TEK-006', 14, 'Damaged in Transit', 'Credit Issued'),
]
credit = {r[0]: r[4] * BY[r[3]][4][1] for r in RET if r[6] == 'Credit Issued'}
assert sum(credit.values()) == 42340
OPEN = ('Under Review', 'Approved', 'Pickup Scheduled')
rows = [f'<tr><td class="mono nowrap"><b>{r[0]}</b></td><td>{r[1]}</td><td class="mono nowrap">{r[2]}</td><td>{BY[r[3]][1]}</td><td class="num">{r[4]}</td><td>{r[5]}</td><td>{chip(r[6])}</td><td class="num">{M(credit[r[0]]) if r[0] in credit else "—"}</td></tr>' for r in RET]
body = f'''  <div class="head">
    <h1>Return Requests</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="download"></i>Export Requests</button><a class="btn pri" data-link="PRI-RET-02"><i data-icon="plus"></i>Create Return Request</a></div>
  </div>
  <div class="kpis">
    {kpi('Open Requests', '3')}
    {kpi('Sheets Under Return', str(sum(r[4] for r in RET if r[6] in OPEN)))}
    {kpi('Credit Issued', M(sum(credit.values())), chip('3 requests', 'plain'))}
    {kpi('Requests This Year', '7')}
  </div>
  <section class="card flush">
    {tabs([('All Requests', 7, True), ('Open', 3, False), ('Credit Issued', 3, False), ('Rejected', 1, False)])}
    {filters('Search by return or order number', 'Search return requests', ('Date Range', 'Last 90 days'), ('Reason', 'All'))}
    <div class="body">{table([('Return Number',''), ('Date',''), ('Order Number',''), ('Product',''), ('Sheets','num'), ('Reason',''), ('Status',''), ('Credit Amount','num')], rows)}
      {pager('Showing 1 to 7 of 7 requests', 1)}</div>
  </section>
'''
page('primary', 'return-requests', 'PRI-RET-01', 'Primary Customer — Owner — Return Requests (PRI-RET-01)', body)

# ---------- Create Return Request ----------
RQ = {'LM-OAK-004': 10, 'LM-TEK-006': 5}
lines = ''.join(f'<tr><td><div class="prod">{sw(s)}<div><b>{BY[s][1]}</b></div></div></td><td class="mono nowrap">{s}</td><td class="num">{N(q)}</td><td>{qty(RQ.get(s, 0))}</td></tr>' for s, q in ORDER_10431)
def radio(title, on=False, name='r'):
    return f'<label class="radio{" on" if on else ""}"><input type="radio" name="{name}"{" checked" if on else ""}><span><b>{title}</b></span></label>'
body = f'''  <div class="head">
    <h1>Create Return Request</h1>
    <div class="acts">{cancel('PRI-RET-01')}<button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Submit Return Request</button></div>
  </div>
  <div class="grid g-main-side" style="--side:20rem">
    <div class="stack">
      {form('Return Details', fld('Order', 'ord', 'ORD-2026-10431', 'select', ['ORD-2026-10431', 'ORD-2026-10398', 'ORD-2026-10372']), fld('Return Reason', 'rs', 'Surface Defect', 'select', ['Damaged in Transit', 'Surface Defect', 'Wrong Product Delivered', 'Shade Mismatch']),
            fld('Pickup Location', 'pl', 'Bhiwandi Warehouse', 'select', ['Bhiwandi Warehouse', 'Pune Warehouse']), fld('Contact for Pickup', 'cp', 'Kavita Joshi, +91 90000 21002'))}
      <section class="card flush"><header><h2>Items to Return</h2></header><div class="body">{table([('Product',''), ('SKU',''), ('Ordered Sheets','num'), ('Sheets to Return','')], [lines], 'stack-sm')}</div></section>
      <section class="card"><header><h2>Photos</h2></header><div class="body"><div class="drop"><span class="file"><i data-icon="doc"></i>surface-defect-1.jpg</span><span class="file"><i data-icon="doc"></i>surface-defect-2.jpg</span><button class="btn sm" type="button"><i data-icon="upload"></i>Upload Photos</button></div></div></section>
      <section class="card"><header><h2>Notes</h2></header><div class="body"><div class="field"><label for="nt">Notes for Crestline</label><textarea class="input" id="nt" placeholder="Describe the issue"></textarea></div></div></section>
    </div>
    <div class="stack">
      <section class="card"><header><h2>Preferred Resolution</h2></header><div class="body"><div class="stack">{radio('Credit Note', True, 'res')}{radio('Replacement Sheets', False, 'res')}</div></div></section>
      {card('Return Summary', kv([('Order', '<span class="mono">ORD-2026-10431</span>'), ('Products', '2'), ('Sheets to Return', '15'), ('Pickup Location', 'Bhiwandi Warehouse')]))}
    </div>
  </div>
'''
page('primary', 'create-return-request', 'PRI-RET-02', 'Primary Customer — Owner — Create Return Request (PRI-RET-02)', body)

# ---------- Support Ticket List ----------
TK = [  # number, created, subject, category, priority, updated, status
 ('TKT-2026-0731', '24/10/2026', 'Damaged Sheets in ORD-2026-10431', 'Delivery', 'High', '26/10/2026', 'In Progress'),
 ('TKT-2026-0724', '22/10/2026', 'Invoice INV-2026-03264 Amount Query', 'Billing', 'Medium', '25/10/2026', 'Awaiting Your Reply'),
 ('TKT-2026-0702', '15/10/2026', 'Price Tier Review Request', 'Account', 'Low', '15/10/2026', 'Open'),
 ('TKT-2026-0688', '09/10/2026', 'Dispatch Delay on ORD-2026-10398', 'Delivery', 'Medium', '12/10/2026', 'Resolved'),
 ('TKT-2026-0655', '29/09/2026', 'GST Correction on INV-2026-03198', 'Billing', 'Medium', '03/10/2026', 'Closed'),
 ('TKT-2026-0631', '21/09/2026', 'Festive Scheme Eligibility', 'Schemes', 'Low', '22/09/2026', 'Closed'),
]
rows = [f'<tr><td class="mono nowrap">{link("PRI-SUP-03", t[0])}</td><td>{t[2]}</td><td>{t[3]}</td><td>{chip(t[4])}</td><td>{t[1]}</td><td>{t[5]}</td><td>{chip(t[6])}</td></tr>' for t in TK]
body = f'''  <div class="head">
    <h1>Support Ticket List</h1>
    <div class="acts"><a class="btn pri" data-link="PRI-SUP-02"><i data-icon="plus"></i>Create Support Ticket</a></div>
  </div>
  <div class="kpis">
    {kpi('Open Tickets', '3')}
    {kpi('Awaiting Your Reply', '1', chip('TKT-2026-0724', 'warn'))}
    {kpi('High Priority', '1')}
    {kpi('Resolved This Month', '1')}
  </div>
  <section class="card flush">
    {tabs([('All Tickets', 6, True), ('Open', 3, False), ('Resolved', 1, False), ('Closed', 2, False)])}
    {filters('Search by ticket number or subject', 'Search tickets', ('Category', 'All'), ('Priority', 'All'))}
    <div class="body">{table([('Ticket Number',''), ('Subject',''), ('Category',''), ('Priority',''), ('Created',''), ('Last Updated',''), ('Status','')], rows)}
      {pager('Showing 1 to 6 of 6 tickets', 1)}</div>
  </section>
'''
page('primary', 'support-ticket-list', 'PRI-SUP-01', 'Primary Customer — Owner — Support Ticket List (PRI-SUP-01)', body)

# ---------- Create Support Ticket ----------
body = f'''  <div class="head">
    <h1>Create Support Ticket</h1>
    <div class="acts">{cancel('PRI-SUP-01')}<button class="btn" type="button">Save Draft</button><button class="btn pri" type="button">Submit Ticket</button></div>
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      {form('Ticket Details', fld('Subject', 'sb', 'Credit Note Missing for RTN-2026-0377', full=True), fld('Category', 'cg', 'Billing', 'select', ['Delivery', 'Billing', 'Account', 'Schemes', 'Product']), fld('Priority', 'pr', 'Medium', 'select', ['Low', 'Medium', 'High']),
            fld('Related Order', 'ro', 'ORD-2026-10372', 'select', ['None', 'ORD-2026-10482', 'ORD-2026-10459', 'ORD-2026-10447', 'ORD-2026-10431', 'ORD-2026-10372']), fld('Related Invoice', 'ri', 'INV-2026-03233', 'select', ['None', 'INV-2026-03318', 'INV-2026-03291', 'INV-2026-03264', 'INV-2026-03233']),
            fld('Description', 'ds', 'The credit of ₹18,000 for return request RTN-2026-0377 is not shown against INV-2026-03233.', 'textarea', full=True))}
      <section class="card"><header><h2>Attachments</h2></header><div class="body"><div class="drop"><span class="file"><i data-icon="doc"></i>credit-note.pdf</span><button class="btn sm" type="button"><i data-icon="upload"></i>Upload Files</button></div></div></section>
    </div>
    <div class="stack">
      {card('Crestline Support', kv([('Account Manager', 'Vikram Chopra'), ('Phone', '+91 90000 11223'), ('Email', 'vikram.chopra@<wbr>crestlinelaminates.example'), ('Support Hours', 'Monday to Saturday, 09:30 to 18:30')]))}
    </div>
  </div>
'''
page('primary', 'create-support-ticket', 'PRI-SUP-02', 'Primary Customer — Owner — Create Support Ticket (PRI-SUP-02)', body)

# ---------- Support Ticket Details (TKT-2026-0731) ----------
def msg(who, init, when, text, me=False, files=()):
    fl = f'<div class="files">{"".join(f"<span class=file><i data-icon=doc></i>{f}</span>" for f in files)}</div>' if files else ''
    return f'<div class="msg{" me" if me else ""}"><div class="av">{init}</div><div><div class="top-line"><b>{who}</b><time>{when}</time></div><div class="bubble">{text}{fl}</div></div></div>'
thread = ''.join([
    msg('Rajesh Menon', 'RM', '24/10/2026 16:20', 'Twelve sheets of Calacatta Marble Finish Laminate arrived with cracked corners in ORD-2026-10431. Photos are attached.', True, ['damaged-corners-1.jpg', 'damaged-corners-2.jpg']),
    msg('Meera Kapoor, Crestline Customer Support', 'MK', '25/10/2026 10:05', 'Thank you, Rajesh. We have the photos and have asked the Vapi plant to check the batch. A return request is the fastest way to get a credit note.'),
    msg('Rajesh Menon', 'RM', '25/10/2026 11:20', 'Return request RTN-2026-0412 is raised for 12 sheets.', True, ['packing-list.pdf']),
    msg('Meera Kapoor, Crestline Customer Support', 'MK', '26/10/2026 09:40', 'The return request is under review. We will confirm the pickup date within two working days.'),
])
body = f'''  <div class="head">
    <div class="title-row"><h1>Damaged Sheets in ORD-2026-10431</h1>{chip('In Progress')}{chip('High')}</div>
    <div class="acts"><button class="btn" type="button"><i data-icon="check"></i>Close Ticket</button></div>
  </div>
  <div class="grid g-main-side" style="--side:22rem">
    <div class="stack">
      {card('Conversation', f'<div class="thread">{thread}</div>')}
      <section class="card"><header><h2>Reply</h2></header><div class="body"><div class="reply"><textarea class="input" aria-label="Reply" placeholder="Write a reply"></textarea>
        <div class="row"><button class="btn" type="button"><i data-icon="upload"></i>Attach Files</button><button class="btn pri" type="button">Send Reply</button></div></div></div></section>
    </div>
    <div class="stack">
      {card('Ticket Information', kv([('Ticket Number', '<span class="mono">TKT-2026-0731</span>'), ('Status', chip('In Progress')), ('Priority', chip('High')), ('Category', 'Delivery'), ('Created', '24/10/2026 16:20'), ('Last Updated', '26/10/2026 09:40'), ('Assigned To', 'Meera Kapoor')]))}
      {card('Related Records', kv([('Order', link('PRI-ORD-02', 'ORD-2026-10431', False)), ('Return Request', link('PRI-RET-01', 'RTN-2026-0412', False))]))}
    </div>
  </div>
'''
page('primary', 'support-ticket-details', 'PRI-SUP-03', 'Primary Customer — Owner — Support Ticket Details (PRI-SUP-03)', body)

# ---------- User Management ----------
US = [  # name, role, email, phone, last sign-in, status
 ('Rajesh Menon', 'Owner', '21001', '26/10/2026 09:05', 'Active'),
 ('Kavita Joshi', 'Sales and Operations Manager', '21002', '26/10/2026 08:40', 'Active'),
 ('Suresh Iyer', 'Accountant', '21003', '25/10/2026 17:30', 'Active'),
 ('Pooja Deshpande', 'Sales and Operations Manager', '21004', 'Not yet', 'Invited'),
 ('Amit Kulkarni', 'Accountant', '21005', '30/06/2026', 'Inactive'),
]
em = lambda n: n.lower().replace(' ', '.') + '@distributoralpha.example'
rows = [f'<tr><td>{link("PRI-USR-03", u[0])}</td><td>{u[1]}</td><td class="nowrap">{em(u[0])}</td><td class="nowrap">{u[3]}</td><td>{chip(u[4])}</td><td><div class="row-actions"><a class="btn sm" data-link="PRI-USR-03">View</a></div></td></tr>' for u in US]
roles = [('Owner', 1), ('Sales and Operations Manager', 2), ('Accountant', 2)]
body = f'''  <div class="head">
    <h1>User Management</h1>
    <div class="acts"><a class="btn pri" data-link="PRI-USR-02"><i data-icon="plus"></i>Create User</a></div>
  </div>
  <div class="kpis">
    {kpi('Users', '5')}
    {kpi('Active', '3')}
    {kpi('Invited', '1')}
    {kpi('Inactive', '1')}
  </div>
  <section class="card flush">
    {tabs([('All Users', 5, True), ('Active', 3, False), ('Invited', 1, False), ('Inactive', 1, False)])}
    {filters('Search by name or email address', 'Search users', ('Role', 'All'))}
    <div class="body">{table([('Name',''), ('Role',''), ('Email Address',''), ('Last Sign-In',''), ('Status',''), ('','')], rows)}</div>
  </section>
'''
page('primary', 'user-management', 'PRI-USR-01', 'Primary Customer — Owner — User Management (PRI-USR-01)', body)

# ---------- Create User ----------
MODS = [('Product Catalogue and Orders', 1, 1, 0), ('Inventory', 1, 1, 0), ('Dealers', 1, 1, 0), ('Secondary Sales', 1, 1, 0), ('Invoices and Payments', 1, 0, 1), ('Schemes and Incentives', 1, 0, 0),
        ('Reports', 1, 1, 1), ('Return Requests', 1, 1, 0), ('Support Tickets', 1, 0, 0), ('User Management', 1, 0, 0), ('Company Profile', 1, 0, 0), ('My Profile and Notifications', 1, 1, 1)]
tick = lambda v: '<i data-icon="check"></i>' if v else '<span class="no">—</span>'
mrows = [f'<tr><td><b>{m[0]}</b></td><td class="c">{tick(m[1])}</td><td class="c">{tick(m[2])}</td><td class="c">{tick(m[3])}</td></tr>' for m in MODS]
mtable = table([('Area',''), ('Owner','c'), ('Sales and Operations Manager','c'), ('Accountant','c')], mrows)
body = f'''  <div class="head">
    <h1>Create User</h1>
    <div class="acts">{cancel('PRI-USR-01')}<button class="btn pri" type="button">Send Invitation</button></div>
  </div>
  <div class="grid g-main-side" style="--side:20rem">
    {form('Personal Details', fld('First Name', 'fn', 'Pooja'), fld('Last Name', 'ln', 'Deshpande'), fld('Email Address', 'em', 'pooja.deshpande@distributoralpha.example'), fld('Mobile Number', 'mb', '+91 90000 21004'))}
    <section class="card"><header><h2>Role</h2></header><div class="body"><div class="stack">{radio('Owner', False, 'role')}{radio('Sales and Operations Manager', True, 'role')}{radio('Accountant', False, 'role')}</div></div></section>
  </div>
  <section class="card flush"><header><h2>Access by Role</h2></header><div class="body">{mtable}</div></section>
'''
page('primary', 'create-user', 'PRI-USR-02', 'Primary Customer — Owner — Create User (PRI-USR-02)', body)

# ---------- User Details (Kavita Joshi) ----------
act = [('26/10/2026 10:20', 'Recorded sale SAL-2026-3041'), ('26/10/2026 08:40', 'Signed in'), ('23/10/2026 11:05', 'Placed order ORD-2026-10459'), ('22/10/2026 15:30', 'Raised return request RTN-2026-0408'), ('20/10/2026 09:10', 'Signed in')]
arows = [f'<tr><td class="nowrap">{d}</td><td><b>{a}</b></td></tr>' for d, a in act]
accrows = [f'<tr><td><b>{m[0]}</b></td><td class="c">{tick(m[2])}</td></tr>' for m in MODS]
body = f'''  <div class="head">
    <div class="title-row"><h1>Kavita Joshi</h1>{chip('Active')}<span class="tag">Sales and Operations Manager</span></div>
    <div class="acts"><button class="btn" type="button"><i data-icon="lock"></i>Reset Password</button><button class="btn" type="button"><i data-icon="edit"></i>Edit User</button><button class="btn danger" type="button">Deactivate User</button></div>
  </div>
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      {card('Profile', kv([('Full Name', 'Kavita Joshi'), ('Email Address', em('Kavita Joshi')), ('Mobile Number', '+91 90000 21002'), ('Role', 'Sales and Operations Manager'), ('Added On', '15/05/2019'), ('Added By', 'Rajesh Menon'), ('Last Sign-In', '26/10/2026 08:40')]))}
      <section class="card flush"><header><h2>Recent Activity</h2></header><div class="body">{table([('Date',''), ('Activity','')], arows)}</div></section>
    </div>
    <section class="card flush"><header><h2>Access</h2></header><div class="body">{table([('Area',''), ('Access','c')], accrows)}</div></section>
  </div>
'''
page('primary', 'user-details', 'PRI-USR-03', 'Primary Customer — Owner — User Details (PRI-USR-03)', body)

# ---------- My Profile (Owner, Sales and Operations Manager, Accountant) ----------
PEOPLE = [('OWN', 'Rajesh Menon', '+91 90000 21001', '26/10/2026 09:05'), ('MGR', 'Kavita Joshi', '+91 90000 21002', '26/10/2026 08:40'), ('ACC', 'Suresh Iyer', '+91 90000 21003', '25/10/2026 17:30')]
def per_role(fn): return ''.join(f'<div data-role="{r}">{fn(r, n, ph, ls)}</div>' for r, n, ph, ls in PEOPLE)
def pform(r, n, ph, ls):
    return f'<div class="form-grid">{fld("Full Name", "nm" + r, n)}{fld("Mobile Number", "mb" + r, ph)}{fld("Email Address", "em" + r, em(n), full=True)}{fld("Language", "lg" + r, "English", "select", ["English", "Hindi", "Marathi"], full=True)}</div>'
prefs = [('Order Updates', 1, 1), ('Invoice and Payment Updates', 1, 1), ('Stock Alerts', 1, 1), ('Scheme Announcements', 0, 1), ('Support Replies', 1, 1)]
prow = [f'<tr><td><b>{e}</b></td><td class="c"><label class="check"><input type="checkbox"{" checked" if a else ""} aria-label="{e} by email"></label></td><td class="c"><label class="check"><input type="checkbox"{" checked" if b else ""} aria-label="{e} in the portal"></label></td></tr>' for e, a, b in prefs]
sess = [('Chrome on Windows', 'Bhiwandi', chip('Current Session', 'ok')), ('Chrome on Android', 'Thane', '25/10/2026 19:12'), ('Safari on iPhone', 'Mumbai', '22/10/2026 08:03')]
srow = [f'<tr><td class="nowrap"><b>{a}</b></td><td>{b}</td><td class="nowrap">{c}</td></tr>' for a, b, c in sess]
body = f'''  <div class="head">
    <h1>My Profile</h1>
    <div class="acts"><button class="btn" type="button">Cancel</button><button class="btn pri" type="button">Save Changes</button></div>
  </div>
  <section class="card pad" style="flex-direction:row;align-items:center;gap:1.25rem;flex-wrap:wrap">
    <div class="av-lg" data-me="initials"></div>
    <div style="flex:1;min-width:14rem;display:grid;gap:.5rem"><h2 style="font-size:1.25rem" data-me="name"></h2>
      <div style="display:flex;flex-wrap:wrap;gap:.5rem">{chip('Active', 'ok')}<span class="tag" data-me="role"></span></div></div>
    <dl class="kv left" style="grid-template-columns:auto auto;gap:.5rem 1.25rem"><dt>Organisation</dt><dd>Distributor Alpha Private Limited</dd><dt>Last Sign-In</dt><dd>{per_role(lambda r, n, ph, ls: ls).replace('<div', '<span').replace('</div>', '</span>')}</dd></dl>
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
    <section class="card flush"><header><h2>Notification Preferences</h2></header><div class="body">{table([('Notification',''), ('Email','c'), ('In the Portal','c')], prow, 'pref')}</div></section>
    <section class="card flush"><header><h2>Signed-In Devices</h2></header><div class="body">{table([('Device',''), ('City',''), ('Last Active','')], srow)}</div></section>
  </div>
'''
page('primary', 'my-profile', 'PRI-PRO-02', 'Primary Customer — Owner — My Profile (PRI-PRO-02)', body)

# ---------- Notifications (role-aware: three unread for each role, matching the bell badge) ----------
def n(sid, title, ref, when, icon, kind='', unread=False):
    return (f'<li{" class=unread" if unread else ""}><span class="dot {kind}"><i data-icon="{icon}"></i></span><div class="title"><a data-link="{sid}">{title}</a><span class="tag mono">{ref}</span></div><time>{when}</time></li>')
def day(label, *items): return f'<div class="day">{label}</div><ul class="feed ntf">{"".join(items)}</ul>'
OWN = (day('Today', n('PRI-ORD-02', 'Order Submitted', 'ORD-2026-10482', '11:42', 'cart', '', True), n('PRI-SCH-02', 'Scheme Target Reached', 'SCH-2026-04', '09:15', 'tag', 'ok', True), n('PRI-INV-02', 'Low Stock', 'LM-CAL-003', '08:30', 'warn', 'warn', True))
       + day('Yesterday', n('PRI-SUP-03', 'New Reply on Support Ticket', 'TKT-2026-0731', '16:10', 'help'), n('PRI-RET-01', 'Return Request Submitted', 'RTN-2026-0412', '11:20', 'ret'))
       + day('24 October 2026', n('PRI-BIL-02', 'Invoice Issued', 'INV-2026-03318', '06:32', 'receipt'))
       + day('23 October 2026', n('PRI-ORD-02', 'Order Confirmed', 'ORD-2026-10459', '16:10', 'cart', 'ok'))
       + day('22 October 2026', n('PRI-BIL-04', 'Payment Confirmed', 'PAY-2026-02217', '16:30', 'cash', 'ok')))
MGR = (day('Today', n('PRI-SAL-03', 'Sale Recorded', 'SAL-2026-3041', '10:20', 'trend', '', True), n('PRI-RET-01', 'Return Request Approved', 'RTN-2026-0408', '09:40', 'ret', 'ok', True), n('PRI-INV-02', 'Low Stock', 'LM-CAL-003', '08:30', 'warn', 'warn', True))
       + day('24 October 2026', n('PRI-ORD-02', 'Order In Transit', 'ORD-2026-10447', '06:30', 'truck'))
       + day('23 October 2026', n('PRI-ORD-02', 'Order Confirmed', 'ORD-2026-10459', '16:10', 'cart', 'ok')))
ACC = (day('Today', n('PRI-BIL-01', 'Invoice Overdue', 'INV-2026-02986', '08:00', 'warn', 'bad', True))
       + day('24 October 2026', n('PRI-BIL-02', 'Invoice Issued', 'INV-2026-03318', '06:32', 'receipt', '', True))
       + day('22 October 2026', n('PRI-BIL-04', 'Payment Confirmed', 'PAY-2026-02217', '16:30', 'cash', 'ok', True))
       + day('21 October 2026', n('PRI-BIL-04', 'Payment Recorded', 'PAY-2026-02217', '14:20', 'cash'))
       + day('17 October 2026', n('PRI-BIL-03', 'Payment Confirmed', 'PAY-2026-02204', '15:10', 'cash', 'ok')))
body = f'''  <div class="head">
    <h1>Notifications</h1>
    <div class="acts"><button class="btn" type="button"><i data-icon="check"></i>Mark All as Read</button></div>
  </div>
  <section class="card flush">
    <div style="padding:0 1.125rem"><div class="tabs"><span class="on">All Notifications<b data-count=".ntf li"></b></span><span>Unread<b data-count=".ntf li.unread"></b></span></div></div>
    <div class="body" style="padding:0 1.125rem 1rem"><div data-role="OWN">{OWN}</div><div data-role="MGR">{MGR}</div><div data-role="ACC">{ACC}</div></div>
  </section>
'''
page('primary', 'notifications', 'PRI-NTF-01', 'Primary Customer — Owner — Notifications (PRI-NTF-01)', body)
