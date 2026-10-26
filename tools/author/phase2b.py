"""Phase 2, part B: Primary Customer Owner: Place Order, Order Builder, Order Confirmation (order ORD-2026-10482)."""
from data import *

LINES = [('LM-WNT-001',200),('LM-ARC-002',300),('LM-CAL-003',80),('LM-OAK-004',120),('LM-SLT-005',60)]
QTY = dict(LINES)
sub = sum(q*slab(s,q) for s,q in LINES)            # 821300
assert sub == 821300
rebate = round(sub*0.02)                            # 16426
taxable = sub - rebate                              # 804874
gst = 72439
total = taxable + 2*gst                             # 949752
assert total == 949752, total

def steps(now):
    names = ['Select Products','Order Details','Confirmation']
    out = ''
    for i,n in enumerate(names, 1):
        cls = 'done' if i < now else 'now' if i == now else ''
        mark = '<i data-icon="check"></i>' if i < now else str(i)
        out += f'<li class="{cls}"><i>{mark}</i>{n}</li>'
    return f'<ol class="steps" aria-label="Order steps">{out}</ol>'

# ---------- Place Order ----------
rows = ''
for p in P:
    sku = p[0]; q = QTY.get(sku, 0)
    price = slab(sku, q) if q else p[4][0]
    amt = M(q*price) if q else '—'
    rows += f'''<tr><td><div class="prod">{sw(sku)}<div><b>{p[1]}</b><small>{sku} \u00b7 {p[2]}, {p[3]}</small>{chip('Low Stock','warn') if sku=='LM-STN-009' else ''}</div></div></td>
      <td class="num">{M(price)}<small>{'slab applied' if q else 'per sheet'}</small></td><td>{qty(q)}</td><td class="num"><b>{amt}</b></td></tr>
'''
draft = ''.join(f'<li><div class="grow"><b>{BY[s][1]}</b><span class="sub">{N(q)} sheets × {M(slab(s,q))}</span></div><b>{M(q*slab(s,q))}</b></li>' for s,q in LINES)
body = f'''  <div class="head">
    <div><h1>Place Order</h1><p>Step 1 of 3 · prices per sheet before GST</p></div>
    <div class="acts"><span class="sel"><i data-icon="repeat"></i>Reorder from a Previous Order <i data-icon="down"></i></span></div>
  </div>
  {steps(1)}
  <div class="grid g-main-side" style="--side:22rem">
    <section class="card flush">
      <header><h2>Products</h2><span class="meta">12 products</span>
        <label class="finder" style="margin-left:auto;min-width:18rem"><i data-icon="search"></i><input type="search" placeholder="Search by name or SKU" aria-label="Search products"></label></header>
      <div class="body"><div class="table-wrap"><table class="tbl stack-sm"><thead><tr><th>Product</th><th class="num">Price per Sheet</th><th>Sheets</th><th class="num">Amount</th></tr></thead><tbody>{rows}</tbody></table></div></div>
    </section>
    <aside class="card" style="align-self:start;position:sticky;top:calc(var(--review-h) + 4.5rem)"><header><h2>Order Draft</h2><span class="meta">5 products · 760 sheets</span></header>
      <div class="body"><ul class="list" style="margin-top:-.5rem">{draft}</ul>
        <dl class="kv total" style="margin-top:.25rem"><dt>Subtotal</dt><dd>{M(sub)}</dd></dl>
        <div class="alert ok" style="margin-top:.875rem"><i data-icon="check"></i><span>Free delivery applies above {M(500000)}</span></div>
        <a class="btn pri block" data-link="PRI-ORD-04" style="margin-top:1rem">Continue to Order Details<i data-icon="arrow"></i></a>
        <button class="btn block" type="button" style="margin-top:.5rem">Save Draft</button></div></aside>
  </div>
'''
page('primary','place-order','PRI-ORD-03','Primary Customer — Owner — Place Order (PRI-ORD-03)', body)

# ---------- Order Builder ----------
item_rows = ''
for s,q in LINES:
    p = BY[s]; pr = slab(s,q)
    item_rows += f'''<tr><td><div class="prod">{sw(s)}<div><b>{p[1]}</b><small>{s}</small></div></div></td><td>{qty(q)}</td><td class="num">{M(pr)}</td>
      <td class="num"><b>{M(q*pr)}</b></td><td><button class="icon-btn" type="button" aria-label="Remove {p[1]}"><i data-icon="trash"></i></button></td></tr>
'''
body = f'''  <div class="head">
    <div><h1>Order Builder</h1><p>Step 2 of 3 · draft for 760 sheets</p></div>
    <div class="acts"><a class="btn" data-link="PRI-ORD-03"><i data-icon="back"></i>Back to Products</a><button class="btn" type="button">Save Draft</button><a class="btn pri" data-link="PRI-ORD-05">Submit Order</a></div>
  </div>
  {steps(2)}
  <div class="grid g-main-side" style="--side:20rem">
    <div class="stack">
      <section class="card flush"><header><h2>Order Items</h2><span class="meta">5 products</span><span style="margin-left:auto">{chip('Festive Volume Rebate 2% applied','blue')}</span></header>
        <div class="body"><div class="table-wrap"><table class="tbl stack-sm"><thead><tr><th>Product</th><th>Sheets</th><th class="num">Price per Sheet</th><th class="num">Amount</th><th></th></tr></thead><tbody>{item_rows}</tbody></table></div></div></section>
      <section class="card"><header><h2>Delivery</h2></header><div class="body"><div class="form-grid">
        <div class="field"><label for="loc">Delivery Location</label><select class="input" id="loc"><option>Bhiwandi Warehouse, Thane District</option><option>Pune Warehouse, Hadapsar</option></select></div>
        <div class="field"><label for="date">Requested Delivery Date</label><input class="input" id="date" value="31/10/2026"></div>
        <div class="field"><label for="ref">Your Reference Number</label><input class="input" id="ref" placeholder="Reference from your records"></div>
        <div class="field"><label for="contact">Receiving Contact</label><input class="input" id="contact" value="Kavita Joshi, +91 90000 21002"></div>
        <div class="full"><span class="label">Transport</span><div class="form-grid" style="margin-top:.375rem">
          <label class="radio on"><input type="radio" name="t" checked><span><b>Company Transport</b><small>Free above {M(500000)}; this order qualifies</small></span></label>
          <label class="radio"><input type="radio" name="t"><span><b>Self Pickup</b><small>Collect from the Vapi plant warehouse</small></span></label></div></div>
        <div class="field full"><label for="notes">Order Notes</label><textarea class="input" id="notes" placeholder="Anything the dispatch team should know"></textarea></div>
      </div></div></section>
    </div>
    <div class="stack">
      <section class="card"><header><h2>Order Summary</h2></header><div class="body">
        <dl class="kv"><dt>Subtotal (760 sheets)</dt><dd>{M(sub)}</dd><dt>Festive Volume Rebate 2%</dt><dd style="color:var(--ok)">−{M(rebate)}</dd><dt>Taxable Amount</dt><dd>{M(taxable)}</dd><dt>Central GST 9%</dt><dd>{M(gst)}</dd><dt>State GST 9%</dt><dd>{M(gst)}</dd><dt>Freight</dt><dd>{M(0)}</dd></dl>
        <dl class="kv total"><dt>Total</dt><dd>{M(total)}</dd></dl></div></section>
      <section class="card"><header><h2>Credit</h2></header><div class="body">
        <dl class="kv"><dt>Credit Limit</dt><dd>{M(4000000)}</dd><dt>Outstanding Balance</dt><dd>{M(1486320)}</dd><dt>This Order</dt><dd>{M(total)}</dd></dl>
        <span class="meter ok" style="margin-top:.875rem"><i style="width:61%"></i></span>
        <p class="sub" style="margin-top:.375rem"><b style="color:var(--ink)">{M(1563928)}</b> credit available after this order</p></div></section>
    </div>
  </div>
'''
page('primary','order-builder','PRI-ORD-04','Primary Customer — Owner — Order Builder (PRI-ORD-04)', body)

# ---------- Order Confirmation ----------
line_rows = ''.join(f'<li><div class="grow"><b>{BY[s][1]}</b><span class="sub">{N(q)} sheets</span></div><b>{M(q*slab(s,q))}</b></li>' for s,q in LINES)
body = f'''  <div class="head"><div><h1>Order Confirmation</h1></div></div>
  {steps(4)}
  <div class="grid g-main-side" style="--side:24rem">
    <div class="stack">
      <section class="card pad" style="display:grid;justify-items:center;gap:1rem;text-align:center;padding:2rem 1.5rem">
        <div class="state" style="padding:0;gap:.75rem"><div class="badge"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg></div>
          <h2 style="font-size:1.375rem">Order submitted</h2>
          <p>Order <b class="mono">ORD-2026-10482</b> was placed on 26 October 2026 at 11:42 and is waiting for confirmation from Crestline Laminates.</p></div>
        <div class="actions" style="display:flex;flex-wrap:wrap;gap:.75rem;justify-content:center"><a class="btn pri" data-link="PRI-ORD-02">View Order Details</a><a class="btn" data-link="PRI-ORD-03">Place Another Order</a><button class="btn" type="button"><i data-icon="download"></i>Download Order Copy</button></div>
      </section>
      <section class="card"><header><h2>What Happens Next</h2></header><div class="body">
        <ol class="track"><li class="done"><i></i><b>Order Placed</b><span>26/10/2026 11:42</span></li><li class="now"><i></i><b>Confirmation</b><span>within 1 working day</span></li><li class="todo"><i></i><b>Packing</b><span>planned 28/10/2026</span></li><li class="todo"><i></i><b>Dispatch</b><span>planned 29/10/2026</span></li><li class="todo"><i></i><b>Delivery</b><span>requested 31/10/2026</span></li></ol></div></section>
    </div>
    <div class="stack">
      <section class="card"><header><h2>Order Summary</h2></header><div class="body"><ul class="list" style="margin-top:-.5rem">{line_rows}</ul>
        <dl class="kv total"><dt>Total</dt><dd>{M(total)}</dd></dl>
        <p class="sub" style="margin-top:.375rem;text-align:right">760 sheets · including Central GST and State GST</p></div></section>
      <section class="card"><header><h2>Delivery</h2></header><div class="body"><dl class="kv"><dt>Location</dt><dd>Bhiwandi Warehouse</dd><dt>Requested Date</dt><dd>31/10/2026</dd><dt>Transport</dt><dd>Company Transport</dd><dt>Payment Terms</dt><dd>45 days from invoice</dd></dl></div></section>
    </div>
  </div>
'''
page('primary','order-confirmation','PRI-ORD-05','Primary Customer — Owner — Order Confirmation (PRI-ORD-05)', body)
