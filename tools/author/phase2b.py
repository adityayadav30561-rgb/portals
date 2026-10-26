"""Phase 2, part B: Primary Customer Owner: Place Order, Order Builder, Order Confirmation (order ORD-2026-10482).
Design rule: no text under page titles, no captions beside card titles, no helper sentences."""
from data import *

LINES = [('LM-WNT-001',200),('LM-ARC-002',300),('LM-CAL-003',80),('LM-OAK-004',120),('LM-SLT-005',60)]
QTY = dict(LINES)
sub = sum(q*slab(s,q) for s,q in LINES); assert sub == 821300
rebate = round(sub*0.02); taxable = sub - rebate; gst = 72439
total = taxable + 2*gst; assert total == 949752, total

def steps(now):
    out = ''
    for i,n in enumerate(['Select Products','Order Details','Confirmation'], 1):
        cls = 'done' if i < now else 'now' if i == now else ''
        out += f'<li class="{cls}"><i>{"<i data-icon=check></i>" if i < now else i}</i>{n}</li>'
    return f'<ol class="steps" aria-label="Order steps">{out}</ol>'
steps = (lambda f: (lambda now: f(now).replace('<i data-icon=check></i>','<i data-icon="check"></i>')))(steps)

# ---------- Place Order ----------
rows = ''
for p in P:
    sku = p[0]; q = QTY.get(sku, 0)
    price = slab(sku, q) if q else p[4][0]
    rows += f'''<tr><td><div class="prod">{sw(sku)}<div><b>{p[1]}</b>{chip('Low Stock','warn') if sku=='LM-STN-009' else ''}</div></div></td><td class="mono nowrap">{sku}</td>
      <td class="num">{M(price)}</td><td>{qty(q)}</td><td class="num"><b>{M(q*price) if q else '—'}</b></td></tr>
'''
draft = ''.join(f'<tr><td><b>{BY[s][1]}</b></td><td class="num">{N(q)}</td><td class="num"><b>{M(q*slab(s,q))}</b></td></tr>' for s,q in LINES)
body = f'''  <div class="head">
    <h1>Place Order</h1>
    <div class="acts"><span class="sel"><i data-icon="repeat"></i>Reorder from a Previous Order <i data-icon="down"></i></span></div>
  </div>
  {steps(1)}
  <div class="grid g-main-side" style="--side:22rem">
    <section class="card flush">
      <header><h2>Products</h2>
        <label class="finder" style="margin-left:auto;min-width:18rem"><i data-icon="search"></i><input type="search" placeholder="Search by name or SKU" aria-label="Search products"></label></header>
      <div class="body"><div class="table-wrap"><table class="tbl stack-sm"><thead><tr><th>Product</th><th>SKU</th><th class="num">Price per Sheet</th><th>Sheets</th><th class="num">Amount</th></tr></thead><tbody>{rows}</tbody></table></div></div>
    </section>
    <aside class="card" style="align-self:start;position:sticky;top:calc(var(--review-h) + 4.5rem)"><header><h2>Order Draft</h2></header>
      <div class="body"><div class="table-wrap" style="margin:-.25rem -1.125rem 0"><table class="tbl"><thead><tr><th>Product</th><th class="num">Sheets</th><th class="num">Amount</th></tr></thead><tbody>{draft}</tbody></table></div>
        <dl class="kv" style="margin-top:1rem"><dt>Sheets</dt><dd>760</dd><dt>Freight</dt><dd>{chip('Free','ok')}</dd></dl>
        <dl class="kv total"><dt>Subtotal</dt><dd>{M(sub)}</dd></dl>
        <a class="btn pri block" data-link="PRI-ORD-04" style="margin-top:1.25rem">Continue to Order Details<i data-icon="arrow"></i></a>
        <button class="btn block" type="button" style="margin-top:.5rem">Save Draft</button></div></aside>
  </div>
'''
page('primary','place-order','PRI-ORD-03','Primary Customer — Owner — Place Order (PRI-ORD-03)', body)

# ---------- Order Builder ----------
item_rows = ''
for s,q in LINES:
    p = BY[s]; pr = slab(s,q)
    item_rows += f'''<tr><td><div class="prod">{sw(s)}<div><b>{p[1]}</b></div></div></td><td class="mono nowrap">{s}</td><td>{qty(q)}</td><td class="num">{M(pr)}</td>
      <td class="num"><b>{M(q*pr)}</b></td><td><button class="icon-btn" type="button" aria-label="Remove {p[1]}"><i data-icon="trash"></i></button></td></tr>
'''
body = f'''  <div class="head">
    <h1>Order Builder</h1>
    <div class="acts"><a class="btn" data-link="PRI-ORD-03"><i data-icon="back"></i>Back to Products</a><button class="btn" type="button">Save Draft</button><a class="btn pri" data-link="PRI-ORD-05">Submit Order</a></div>
  </div>
  {steps(2)}
  <div class="grid g-main-side" style="--side:18rem">
    <div class="stack">
      <section class="card flush"><header><h2>Order Items</h2><span style="margin-left:auto">{chip('Festive Volume Rebate 2%','blue')}</span></header>
        <div class="body"><div class="table-wrap"><table class="tbl stack-sm"><thead><tr><th>Product</th><th>SKU</th><th>Sheets</th><th class="num">Price per Sheet</th><th class="num">Amount</th><th></th></tr></thead><tbody>{item_rows}</tbody></table></div></div></section>
      <section class="card"><header><h2>Delivery</h2></header><div class="body"><div class="form-grid">
        <div class="field"><label for="loc">Delivery Location</label><select class="input" id="loc"><option>Bhiwandi Warehouse, Thane District</option><option>Pune Warehouse, Hadapsar</option></select></div>
        <div class="field"><label for="date">Requested Delivery Date</label><input class="input" id="date" value="31/10/2026"></div>
        <div class="field"><label for="ref">Your Reference Number</label><input class="input" id="ref" placeholder="Reference from your records"></div>
        <div class="field"><label for="contact">Receiving Contact</label><input class="input" id="contact" value="Kavita Joshi, +91 90000 21002"></div>
        <div class="full"><span class="label">Transport</span><div class="form-grid" style="margin-top:.375rem">
          <label class="radio on"><input type="radio" name="t" checked><span style="flex:1;display:flex;align-items:center;justify-content:space-between;gap:.75rem"><b>Company Transport</b>{chip('Free','ok')}</span></label>
          <label class="radio"><input type="radio" name="t"><span><b>Self Pickup</b></span></label></div></div>
        <div class="field full"><label for="notes">Order Notes</label><textarea class="input" id="notes" placeholder="Notes for the dispatch team"></textarea></div>
      </div></div></section>
    </div>
    <div class="stack">
      <section class="card"><header><h2>Order Summary</h2></header><div class="body">
        <dl class="kv"><dt>Sheets</dt><dd>760</dd><dt>Subtotal</dt><dd>{M(sub)}</dd><dt>Festive Volume Rebate</dt><dd style="color:var(--ok)">−{M(rebate)}</dd><dt>Taxable Amount</dt><dd>{M(taxable)}</dd><dt>Central GST 9%</dt><dd>{M(gst)}</dd><dt>State GST 9%</dt><dd>{M(gst)}</dd><dt>Freight</dt><dd>{chip('Free','ok')}</dd></dl>
        <dl class="kv total"><dt>Total</dt><dd>{M(total)}</dd></dl></div></section>
      <section class="card"><header><h2>Credit</h2></header><div class="body">
        <dl class="kv"><dt>Credit Limit</dt><dd>{ML(4000000)}</dd><dt>Outstanding Balance</dt><dd>{ML(1486320)}</dd><dt>This Order</dt><dd>{ML(total)}</dd></dl>
        <span class="meter ok" style="margin-top:1rem"><i style="width:61%"></i></span>
        <dl class="kv total"><dt>Credit Available</dt><dd>{ML(1563928)}</dd></dl></div></section>
    </div>
  </div>
'''
page('primary','order-builder','PRI-ORD-04','Primary Customer — Owner — Order Builder (PRI-ORD-04)', body)

# ---------- Order Confirmation ----------
line_rows = ''.join(f'<tr><td><b>{BY[s][1]}</b></td><td class="num">{N(q)}</td><td class="num"><b>{M(q*slab(s,q))}</b></td></tr>' for s,q in LINES)
body = f'''  <div class="head"><h1>Order Confirmation</h1></div>
  {steps(4)}
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      <section class="card pad" style="display:grid;justify-items:center;gap:1.5rem;text-align:center;padding:2.25rem 1.5rem">
        <div class="state" style="padding:0;gap:.75rem"><div class="badge"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg></div>
          <h2 style="font-size:1.5rem">Order Submitted</h2><div class="big-value mono" style="font-size:1.375rem">ORD-2026-10482</div></div>
        <div class="stats" style="--cols:1.6fr 2fr .8fr 1.3fr"><div><span>Placed</span><b>26/10/2026 11:42</b></div><div><span>Status</span>{chip('Awaiting Confirmation')}</div><div><span>Sheets</span><b>760</b></div><div><span>Total</span><b>{M(total)}</b></div></div>
        <div class="actions" style="display:flex;flex-wrap:wrap;gap:.75rem;justify-content:center"><a class="btn pri" data-link="PRI-ORD-02">View Order Details</a><a class="btn" data-link="PRI-ORD-03">Place Another Order</a><button class="btn" type="button"><i data-icon="download"></i>Download Order Copy</button></div>
      </section>
      <section class="card"><header><h2>Order Progress</h2></header><div class="body">
        <ol class="track"><li class="done"><i></i><b>Placed</b><span>26/10/2026</span></li><li class="now"><i></i><b>Confirmation</b><span>Pending</span></li><li class="todo"><i></i><b>Packing</b><span>28/10/2026</span></li><li class="todo"><i></i><b>Dispatch</b><span>29/10/2026</span></li><li class="todo"><i></i><b>Delivery</b><span>31/10/2026</span></li></ol></div></section>
    </div>
    <div class="stack">
      <section class="card"><header><h2>Order Summary</h2></header><div class="body"><div class="table-wrap" style="margin:-.25rem -1.125rem 0"><table class="tbl"><thead><tr><th>Product</th><th class="num">Sheets</th><th class="num">Amount</th></tr></thead><tbody>{line_rows}</tbody></table></div>
        <dl class="kv" style="margin-top:1rem"><dt>Rebate</dt><dd style="color:var(--ok)">−{M(rebate)}</dd><dt>Central GST 9%</dt><dd>{M(gst)}</dd><dt>State GST 9%</dt><dd>{M(gst)}</dd></dl>
        <dl class="kv total"><dt>Total</dt><dd>{M(total)}</dd></dl></div></section>
      <section class="card"><header><h2>Delivery</h2></header><div class="body"><dl class="kv"><dt>Location</dt><dd>Bhiwandi Warehouse</dd><dt>Requested Date</dt><dd>31/10/2026</dd><dt>Transport</dt><dd>Company Transport</dd><dt>Payment Terms</dt><dd>45 days</dd></dl></div></section>
    </div>
  </div>
'''
page('primary','order-confirmation','PRI-ORD-05','Primary Customer — Owner — Order Confirmation (PRI-ORD-05)', body)
