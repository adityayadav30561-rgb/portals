# Prototype data and formats

Every screen uses this data, so the sessions that build the 196 screens agree. Fictional throughout. Read before
building a screen; add to it whenever a screen introduces data another screen will show.

## Formats

| Item | Rule |
|---|---|
| Today | **Monday, 26 October 2026**. Financial year 2026–27 (write "Financial Year 2026–27"). |
| Dates in text | 26 October 2026 |
| Dates in tables and compact places | 26/10/2026 (day/month/year). Time as 11:42 (24-hour). |
| Months | Full names everywhere, including chart axes. No three-letter month names. |
| Money | Exact: ₹ with Indian grouping, ₹9,49,752 (orders, invoices, prices, tables). Compact with full words in stat tiles, chart axes and summaries: ₹33.53 lakh, ₹1.25 crore (two decimals; helper `ML()` in tools/author/data.py). Under ₹1 lakh always exact. Never "L", "Cr", "K". |
| Quantities | Whole sheets: "760 sheets". Never "pcs", "Qty". |
| Units allowed | mm, ft, kg, %, SKU, GST, PDF. |
| Words to avoid (the checks scan for them) | Qty, Amt, Mgr, Acct, Dept, Cust, Dist, Approx, Misc, YTD, MTD, FY, ETA, PO, CGST, SGST, vs, L / Cr / K after a number, three-letter months, UPI, PAN, GSTIN, PIN. Write "Central GST", "State GST", "Postal Code", "Permanent Account Number", "compared with". |
| Tax | GST 18% shown as Central GST 9% and State GST 9%. |

## People and organisations (also in `assets/registry.js`)

| Portal | Organisation | Role: person |
|---|---|---|
| Company Administration | Crestline Laminates (plant warehouse: Vapi, Gujarat) | Super Admin: Anita Deshmukh; Sales Manager: Vikram Chopra; Operations Manager: Neha Kulkarni |
| Primary Customer | **Distributor Alpha Private Limited**, Bhiwandi, Maharashtra | Owner: Rajesh Menon; Sales and Operations Manager: Kavita Joshi; Accountant: Suresh Iyer |
| Secondary Customer | **Dealer Bravo**, Pune | Owner: Sunita Rao; Sales and Inventory Manager: Arjun Nair |
| Tertiary Customer | **Retailer Charlie**, Pune | Retailer Owner: Imran Sheikh; Sales Executive: Pooja Verma; Inventory and Purchasing Executive: Faisal Khan |

Email pattern: `first.last@<organisation without spaces>.example` (Company: `@crestlinelaminates.example`).

**Hierarchy.** Crestline Laminates → Distributor Alpha → dealers → retailers.
Dealers of Distributor Alpha (sales this month): Dealer Bravo, Pune ₹6,84,000; Dealer Delta, Nashik ₹5,92,000;
Dealer Foxtrot, Thane ₹4,76,000; Dealer Gopal, Kolhapur ₹4,11,000; Dealer Harsh, Nagpur ₹3,38,000.
Retailers of Dealer Bravo: Retailer Charlie, Pune; Retailer Kiran Interiors, Pune; Retailer Mehta Furniture, Pimpri.

## Products (the whole range in the prototype: 12 products)

Sheet size is 8 ft × 4 ft (2,440 mm × 1,220 mm). Price is per sheet before GST at the quantity slab: 1–49, 50–199, 200 and above.

| SKU | Product | Finish | Thickness | Price slabs (₹) | Swatch |
|---|---|---|---|---|---|
| LM-WNT-001 | Walnut Woodgrain Laminate | Woodgrain | 1.0 mm | 1,180 / 1,140 / 1,095 | wood #5a3a22 |
| LM-ARC-002 | Arctic White Matte Laminate | Matte | 1.0 mm | 940 / 905 / 870 | plain #f3f5f7 |
| LM-CAL-003 | Calacatta Marble Finish Laminate | High Gloss | 1.0 mm | 1,560 / 1,510 / 1,450 | marble #eceeef |
| LM-OAK-004 | Natural Oak Texture Laminate | Texture | 1.0 mm | 1,240 / 1,200 / 1,150 | wood #b98a55 |
| LM-SLT-005 | Slate Grey Suede Laminate | Suede | 1.0 mm | 1,320 / 1,275 / 1,225 | plain #5b6470 |
| LM-TEK-006 | Classic Teak Woodgrain Laminate | Woodgrain | 0.8 mm | 1,020 / 985 / 950 | wood #9a6a3a |
| LM-CHR-007 | Charcoal Black Gloss Laminate | Gloss | 1.0 mm | 1,090 / 1,055 / 1,010 | plain #23262b |
| LM-IVR-008 | Ivory Cream Matte Laminate | Matte | 0.8 mm | 810 / 780 / 750 | plain #efe6d2 |
| LM-STN-009 | Carrara Stone Finish Laminate | Texture | 1.0 mm | 1,480 / 1,430 / 1,375 | stone #c9ccd0 |
| LM-CPR-010 | Brushed Copper Metallic Laminate | Metallic | 1.0 mm | 1,890 / 1,830 / 1,760 | metal #b4764a |
| LM-WNG-011 | Wenge Dark Woodgrain Laminate | Woodgrain | 1.0 mm | 1,210 / 1,170 / 1,125 | wood #3b2a22 |
| LM-SKY-012 | Sky Blue Gloss Laminate | Gloss | 0.8 mm | 870 / 840 / 805 | plain #8fc1e3 |

Specification details for Product Details: weight 6.1 kg per sheet (1.0 mm) or 5.0 kg (0.8 mm); grade Decorative; sold in packs of 25 sheets.

## Distributor Alpha stock (sheets)

| SKU | On hand | Reserved for dealers | Available | On order | Reorder level | Status |
|---|---|---|---|---|---|---|
| LM-WNT-001 | 1,240 | 310 | 930 | 600 (arrives 30/10/2026) | 400 | In Stock |
| LM-ARC-002 | 1,860 | 420 | 1,440 | 0 | 500 | In Stock |
| LM-CAL-003 | 215 | 90 | 125 | 300 (arrives 30/10/2026) | 250 | Low Stock |
| LM-OAK-004 | 640 | 150 | 490 | 0 | 300 | In Stock |
| LM-SLT-005 | 410 | 120 | 290 | 0 | 200 | In Stock |
| LM-TEK-006 | 880 | 200 | 680 | 0 | 300 | In Stock |
| LM-CHR-007 | 120 | 60 | 60 | 200 | 200 | Low Stock |
| LM-IVR-008 | 1,050 | 260 | 790 | 0 | 400 | In Stock |
| LM-STN-009 | 0 | 0 | 0 | 250 | 150 | Out of Stock |
| LM-CPR-010 | 95 | 40 | 55 | 100 | 100 | Low Stock |
| LM-WNG-011 | 560 | 130 | 430 | 0 | 250 | In Stock |
| LM-SKY-012 | 345 | 95 | 250 | 0 | 150 | In Stock |

Total on hand **7,415 sheets**, stock value **₹78,42,000**. Warehouses: Bhiwandi Warehouse (main), Pune Warehouse.
By finish: Matte 2,910; Woodgrain 2,680; Texture 640; Gloss 465; Suede 410; High Gloss 215; Metallic 95.
Availability for the catalogue is the company's available stock, not Distributor Alpha's: use "In Stock" for all
except LM-STN-009 "Low Stock" (company side).

## Number series

Orders `ORD-2026-10482`; invoices `INV-2026-03318`; payments `PAY-2026-02217`; dispatches `DSP-2026-5521`;
returns `RTN-2026-0412`; support tickets `TKT-2026-0731`; schemes `SCH-2026-04`. Batches `B-2610-14`.

## Distributor Alpha figures (Owner view)

- Credit limit ₹40,00,000; credit period 45 days; outstanding balance **₹14,86,320** (overdue ₹3,18,400).
- Purchases from Crestline by month: May 22,10,000; June 25,60,000; July 19,80,000; August 27,40,000; September 24,30,000; October **33,52,882** (to 26 October).
- Sales to dealers by month: May 24,80,000; June 28,10,000; July 22,40,000; August 30,60,000; September 27,90,000; October **31,20,000**.
- Orders: 142 in total: Awaiting Confirmation 2, Confirmed 3, In Transit 2, Delivered 132, Cancelled 3.
- Schemes: **Festive Volume Rebate** (`SCH-2026-04`): 2% rebate on orders of 3,000 sheets across October and November, progress 2,750 of 3,000 sheets. **Marble Finish Launch Incentive**: ₹25 per sheet of LM-CAL-003, progress 180 of 300 sheets.

## Order flow (Place Order → Order Builder → Order Confirmation)

**ORD-2026-10482**, placed 26/10/2026 11:42 by Rajesh Menon, delivery to Bhiwandi Warehouse requested 31/10/2026, Company Transport.

| SKU | Sheets | Price | Amount |
|---|---|---|---|
| LM-WNT-001 | 200 | 1,095 | 2,19,000 |
| LM-ARC-002 | 300 | 870 | 2,61,000 |
| LM-CAL-003 | 80 | 1,510 | 1,20,800 |
| LM-OAK-004 | 120 | 1,200 | 1,44,000 |
| LM-SLT-005 | 60 | 1,275 | 76,500 |

760 sheets; subtotal ₹8,21,300; Festive Volume Rebate 2% −₹16,426; taxable ₹8,04,874; Central GST ₹72,439; State GST ₹72,439; freight ₹0 (free above ₹5,00,000); **total ₹9,49,752**. Credit available after the order: ₹15,63,928.

## Order History (Distributor Alpha, newest first)

| Order | Date | Sheets | Value | Delivery | Status | Payment |
|---|---|---|---|---|---|---|
| ORD-2026-10482 | 26/10/2026 | 760 | 9,49,752 | 31/10/2026 (requested) | Awaiting Confirmation | Unpaid |
| ORD-2026-10459 | 23/10/2026 | 280 | 3,36,500 | 29/10/2026 (planned) | Confirmed | Unpaid |
| ORD-2026-10447 | 19/10/2026 | 360 | 4,42,930 | 27/10/2026 (expected) | In Transit | Unpaid |
| ORD-2026-10431 | 15/10/2026 | 520 | 6,18,400 | 20/10/2026 | Delivered | Partly Paid |
| ORD-2026-10398 | 08/10/2026 | 430 | 5,24,100 | 13/10/2026 | Delivered | Paid |
| ORD-2026-10372 | 01/10/2026 | 400 | 4,81,200 | 06/10/2026 | Delivered | Paid |
| ORD-2026-10341 | 24/09/2026 | 470 | 5,72,300 | 29/09/2026 | Delivered | Paid |
| ORD-2026-10316 | 17/09/2026 | 330 | 3,98,650 | 22/09/2026 | Delivered | Paid |
| ORD-2026-10290 | 10/09/2026 | 500 | 6,05,900 | 15/09/2026 | Delivered | Paid |
| ORD-2026-10265 | 03/09/2026 | 200 | 2,41,000 | none | Cancelled | Not Applicable |

In the prototype every row opens the same Order Details screen, which shows **ORD-2026-10447**.

## Order Details order: ORD-2026-10447

Placed 19/10/2026 by Rajesh Menon; confirmed 20/10; packed 23/10; dispatched 24/10/2026 06:30 as `DSP-2026-5521` from
Crestline plant warehouse, Vapi to Bhiwandi Warehouse; expected 27/10/2026. Transporter Western Freight Carriers,
vehicle MH 04 KP 7712, driver Ramesh Pawar, +91 90000 12345 (fictional).

| SKU | Sheets | Price | Amount |
|---|---|---|---|
| LM-WNT-001 | 100 | 1,140 | 1,14,000 |
| LM-ARC-002 | 150 | 905 | 1,35,750 |
| LM-CHR-007 | 60 | 1,055 | 63,300 |
| LM-WNG-011 | 50 | 1,170 | 58,500 |

360 sheets; subtotal ₹3,71,550; no scheme; Central GST ₹33,440; State GST ₹33,440; freight ₹4,500; **total ₹4,42,930**.
Invoice `INV-2026-03318` issued 24/10/2026, due 08/12/2026, unpaid.

## Distributor Alpha company profile

Legal name Distributor Alpha Private Limited; customer since 12/04/2018; GST Number 27AABCD4521F1Z7; Permanent
Account Number AABCD4521F; registered address Plot 14, Bhiwandi Logistics Park, Thane District, Maharashtra, Postal
Code 421302; Pune Warehouse, Survey 88, Hadapsar Industrial Estate, Pune, Postal Code 411013. Price tier "Primary
Distributor Tier A"; territory Maharashtra and Goa; Crestline account manager Vikram Chopra. Documents: GST
Registration Certificate (18/04/2018), Trade Licence (renewed 02/04/2026), Distributor Agreement 2026–27 (signed 02/04/2026).
