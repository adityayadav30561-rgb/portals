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
| LM-WNT-001 | 1,240 | 310 | 930 | 300 | 400 | In Stock |
| LM-ARC-002 | 1,860 | 420 | 1,440 | 450 | 500 | In Stock |
| LM-CAL-003 | 215 | 90 | 125 | 80 | 250 | Low Stock |
| LM-OAK-004 | 640 | 150 | 490 | 120 | 300 | In Stock |
| LM-SLT-005 | 410 | 120 | 290 | 60 | 200 | In Stock |
| LM-TEK-006 | 880 | 200 | 680 | 100 | 300 | In Stock |
| LM-CHR-007 | 120 | 60 | 60 | 60 | 200 | Low Stock |
| LM-IVR-008 | 1,050 | 260 | 790 | 120 | 400 | In Stock |
| LM-STN-009 | 0 | 0 | 0 | 0 | 150 | Out of Stock |
| LM-CPR-010 | 95 | 40 | 55 | 0 | 100 | Low Stock |
| LM-WNG-011 | 560 | 130 | 430 | 50 | 250 | In Stock |
| LM-SKY-012 | 345 | 95 | 250 | 60 | 150 | In Stock |

**On order is computed from the three open orders** (below; `OPEN_ORDERS` in `tools/author/data.py`), total **1,400 sheets**, so the stock tables, the Arriving tile and the Incoming Shipments list always agree. Open orders: ORD-2026-10447 (in transit, expected 27/10/2026): WNT 100, ARC 150, CHR 60, WNG 50; ORD-2026-10459 (confirmed, planned 29/10/2026): TEK 100, IVR 120, SKY 60; ORD-2026-10482 (awaiting confirmation, requested 31/10/2026): the five lines of the order flow.

Total on hand **7,415 sheets**, stock value **₹78,42,000**. Warehouses: Bhiwandi Warehouse (main), Pune Warehouse.
By finish: Matte 2,910; Woodgrain 2,680; Texture 640; Gloss 465; Suede 410; High Gloss 215; Metallic 95.
Availability for the catalogue is the company's available stock, not Distributor Alpha's: use "In Stock" for all
except LM-STN-009 "Low Stock" (company side).

## Number series

Orders `ORD-2026-10482`; dealer requests `DRQ-2026-0019`; invoice disputes `DIS-2026-0014`; credit notes `CN-2026-0103`; stock adjustments `ADJ-2026-0034`; invoices `INV-2026-03318`; payments `PAY-2026-02217`; dispatches `DSP-2026-5521`;
returns `RTN-2026-0412`; support tickets `TKT-2026-0731`; schemes `SCH-2026-04`; sales to dealers `SAL-2026-3041`. Batches `B-2610-14`. Payment modes: Bank Transfer, Net Banking, Cheque (never UPI, NEFT, RTGS). Say "Bank Reference", not UTR or Ref.

## Distributor Alpha figures (Owner view)

- Credit limit ₹40,00,000; credit period 45 days; outstanding balance **₹14,86,320** (overdue ₹3,18,400).
- Purchases from Crestline by month: May 22,10,000; June 25,60,000; July 19,80,000; August 27,40,000; September 24,30,000; October **33,52,882** (to 26 October).
- Sales to dealers by month: May 24,80,000; June 28,10,000; July 22,40,000; August 30,60,000; September 27,90,000; October **31,20,000**.
- Orders: 142 in total: Awaiting Confirmation 2, Confirmed 3, In Transit 2, Delivered 132, Cancelled 3.
- Schemes: **Festive Volume Rebate** (`SCH-2026-04`): 2% rebate on orders once 2,500 sheets are reached across October and November (changed from 3,000 on 2026-10-26 by the user); progress 2,750 of 2,500 sheets: **target reached**, 250 above. ORD-2026-10482 is the order that takes the total over the target (1,990 before it), so the rebate applies to that order only (−₹16,426); earlier invoices are not changed. **Marble Finish Launch Incentive**: ₹25 per sheet of LM-CAL-003, progress 180 of 300 sheets.

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
| ORD-2026-10398 | 08/10/2026 | 430 | 5,24,100 | 13/10/2026 | Delivered | Partly Paid |
| ORD-2026-10372 | 01/10/2026 | 400 | 4,81,200 | 06/10/2026 | Delivered | Paid |
| ORD-2026-10341 | 24/09/2026 | 470 | 5,72,300 | 29/09/2026 | Delivered | Paid |
| ORD-2026-10316 | 17/09/2026 | 330 | 3,98,650 | 22/09/2026 | Delivered | Paid |
| ORD-2026-10290 | 10/09/2026 | 500 | 6,05,900 | 15/09/2026 | Delivered | Paid |
| ORD-2026-10265 | 03/09/2026 | 200 | 2,41,000 | none | Cancelled | Not Applicable |

In the prototype every row opens the same Order Details screen, which shows **ORD-2026-10447**. (Changed in Phase 3: ORD-2026-10398 was "Paid"; it is Partly Paid so the open invoices add up to the outstanding balance, see Invoices.)

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

## Dealers of Distributor Alpha (Phase 3; model in `tools/author/data.py`: `DEALERS`, `SALES`)

Eight dealers. "Sales" are the October 2026 amounts invoiced to the dealer, GST included, and add up to **₹31,20,000** (the
dashboard's Sales to Dealers, 2,195 sheets, **32 sales**, average ₹97,500). September sales add up to ₹27,90,000. "Owes" is
the unpaid part of the October sales (₹10,67,500 in all, compact ₹10.68 lakh). Retailers: Bravo's three are named in the hierarchy above.

| Dealer | City | Region | Status | Customer since | Retailers | Sales (October) | Sales (September) | Sheets | Owes | Credit limit |
|---|---|---|---|---|---|---|---|---|---|---|
| Dealer Bravo | Pune | West Maharashtra | Active | 03/09/2019 | 3 | 6,84,000 | 6,10,000 | 480 | 2,60,000 | 8,00,000 |
| Dealer Delta | Nashik | North Maharashtra | Active | 14/02/2019 | 4 | 5,92,000 | 5,20,000 | 410 | 1,89,500 | 7,00,000 |
| Dealer Foxtrot | Thane | Konkan | Active | 21/06/2020 | 3 | 4,76,000 | 4,35,000 | 335 | 1,66,500 | 6,00,000 |
| Dealer Gopal | Kolhapur | West Maharashtra | Active | 09/11/2020 | 3 | 4,11,000 | 3,85,000 | 290 | 1,15,000 | 5,00,000 |
| Dealer Harsh | Nagpur | Vidarbha | Active | 17/03/2021 | 2 | 3,38,000 | 3,60,000 | 240 | 1,01,500 | 5,00,000 |
| Dealer Indira | Satara | West Maharashtra | Active | 05/08/2022 | 2 | 2,46,000 | 2,35,000 | 175 | 98,500 | 4,00,000 |
| Dealer Jayant | Solapur | West Maharashtra | Active | 28/01/2023 | 2 | 2,18,000 | 2,45,000 | 155 | 43,500 | 4,00,000 |
| Dealer Kunal | Panaji | Goa | New | 02/10/2026 | 1 | 1,55,000 | none | 110 | 93,000 | 2,50,000 |

Dealer owners: Sunita Rao (Bravo), Prakash Jadhav, Mohan Patil, Gopal Kulkarni, Harsh Wankhede, Indira Bhosale, Jayant
Shinde, Kunal Naik. **Dealer Bravo details** (the one Dealer Details screen): price tier Dealer Tier B; credit period 30
days; GST Number 27AAKFB3318D1ZP; Shop 6, Laminate Market Road, Hadapsar, Pune, Postal Code 411028; contacts Sunita Rao (Owner,
sunita.rao@dealerbravo.example, +91 90000 31001) Arjun Nair (Sales and Inventory Manager, arjun.nair@dealerbravo.example, +91
90000 31002) and Rekha Sawant (Accountant, +91 90000 31003); retailers Retailer Charlie (Pune, Imran Sheikh), Retailer Kiran Interiors (Pune, Kiran Desai), Retailer Mehta
Furniture (Pimpri, Nilesh Mehta); relationship manager Kavita Joshi. Bravo's six October sales: 24/10 ₹1,37,000 (100 sheets,
DSP-2026-5527, unpaid); 17/10 ₹1,23,000 (unpaid); 13/10 ₹1,09,500; 08/10 ₹1,23,000 (DSP-2026-5471); 05/10 ₹96,000; 01/10
₹95,500. Bravo monthly sales: May 5,20,000; June 5,90,000; July 4,80,000; August 6,30,000; September 6,10,000; October 6,84,000.

**Sales to dealers.** Every sale has a sale number (`SAL-2026-3010` to `SAL-2026-3041`, newest 3041), a date, a dealer, sheets,
value, payment (Paid, Partly Paid, Unpaid) and a dispatch number. The dispatch numbers on the Phase 2 stock movements of LM-CAL-003
(5534, 5527, 5519, 5508, 5496, 5471, 5452) are real sales in this ledger. Monthly sales to dealers are the DATA.md figures above
(May 24,80,000 ... October 31,20,000).
**Dealer price list (Dealer Tier B), per sheet before GST:** the Crestline 1–49 price plus 10%, to the nearest ₹5 (`dp()`): WNT 1,300;
ARC 1,035; CAL 1,715; OAK 1,365; SLT 1,450; TEK 1,120; CHR 1,200; IVR 890; STN 1,630; CPR 2,080; WNG 1,330; SKY 955.
**October sheets sold to dealers by product** (2,195): WNT 280, ARC 405, CAL 165, OAK 205, SLT 110, TEK 220, CHR 100, IVR 210, STN 0, CPR 35, WNG 180, SKY 285.
By finish: Woodgrain 680, Matte 615, Gloss 385, Texture 205, High Gloss 165, Suede 110, Metallic 35. Regions (October): West Maharashtra
₹15,59,000; North Maharashtra ₹5,92,000; Konkan ₹4,76,000; Vidarbha ₹3,38,000; Goa ₹1,55,000.

## Invoices and payments (Phase 3; `INVOICES`, `PAYMENTS`)

Invoices from Crestline are issued on the dispatch date and fall due 45 days later. Today is 26/10/2026.

| Invoice | Order | Issued | Due | Amount | Paid | Balance | Status |
|---|---|---|---|---|---|---|---|
| INV-2026-03318 | ORD-2026-10447 | 24/10/2026 | 08/12/2026 | 4,42,930 | 0 | 4,42,930 | Unpaid |
| INV-2026-03291 | ORD-2026-10431 | 18/10/2026 | 02/12/2026 | 6,18,400 | 2,00,000 | 4,18,400 | Partly Paid |
| INV-2026-03264 | ORD-2026-10398 | 11/10/2026 | 25/11/2026 | 5,24,100 | 2,17,510 | 3,06,590 | Partly Paid |
| INV-2026-03233 | ORD-2026-10372 | 04/10/2026 | 18/11/2026 | 4,81,200 | 4,81,200 | 0 | Paid |
| INV-2026-03198 | ORD-2026-10341 | 27/09/2026 | 11/11/2026 | 5,72,300 | 5,72,300 | 0 | Paid |
| INV-2026-03171 | ORD-2026-10316 | 20/09/2026 | 04/11/2026 | 3,98,650 | 3,98,650 | 0 | Paid |
| INV-2026-03140 | ORD-2026-10290 | 13/09/2026 | 28/10/2026 | 6,05,900 | 6,05,900 | 0 | Paid |
| INV-2026-03021 | ORD-2026-10171 | 12/08/2026 | 26/09/2026 | 1,32,000 | 0 | 1,32,000 | Overdue 30 days |
| INV-2026-02986 | ORD-2026-10158 | 05/08/2026 | 19/09/2026 | 1,86,400 | 0 | 1,86,400 | Overdue 37 days |

**Open invoices add up to the outstanding balance: 4,42,930 + 4,18,400 + 3,06,590 + 1,32,000 + 1,86,400 = ₹14,86,320; the two overdue ones are ₹3,18,400.**
134 invoices in all (every delivered or in-transit order): 5 open, 2 of them overdue, 129 paid. ORD-2026-10459 and ORD-2026-10482 have no invoice yet.
Invoiced in October ₹20,66,630 (4 invoices). In the prototype every invoice row opens the same Invoice Details screen, which shows
**INV-2026-03318** (the four lines of ORD-2026-10447, Central GST ₹33,440, State GST ₹33,440, freight ₹4,500). Issued by Crestline Laminates, GST
Number 24AABCC7782M1Z4, Plant Warehouse, Vapi, Gujarat.

Payments (newest first; 131 in all): PAY-2026-02217 21/10 ₹2,00,000 Bank Transfer (INV-2026-03291); 02204 17/10 ₹2,17,510 Net Banking (03264);
02188 15/10 ₹4,81,200 Bank Transfer (03233); 02143 08/10 ₹5,72,300 Cheque (03198); 02109 02/10 ₹3,98,650 Bank Transfer (03171); 02061 24/09 ₹6,05,900
Net Banking (03140); 01984 12/09 ₹5,43,200 Bank Transfer (03109); 01921 02/09 ₹4,76,800 Cheque (03068); 01866 25/08 ₹4,12,000 Bank Transfer (03010);
01802 14/08 ₹3,58,400 Net Banking (02961). **Paid in October ₹18,69,660 in 5 payments** (Bank Transfer 10,79,850; Net Banking 2,17,510; Cheque 5,72,300).
Paid by month: May 21,40,000; June 24,10,000; July 20,90,000; August 25,30,000; September 23,60,000; October 18,69,660.
**Payment Details shows PAY-2026-02217**: recorded 21/10/2026 14:20 by Suresh Iyer, received by Crestline 22/10/2026 10:05, confirmed
22/10/2026 16:30; paid from Sahyadri Bank, Bhiwandi Branch; Bank Reference SB26102100417; settles ₹2,00,000 of INV-2026-03291 (balance after ₹4,18,400).
ORD-2026-10431 lines (520 sheets): WNT 120, ARC 150, CAL 60, OAK 100, TEK 90 (the 60 sheets of CAL are received into stock on 20/10, see Phase 4 data).

## Schemes (Phase 3)

| Scheme | Type | Period | Status | Progress / result |
|---|---|---|---|---|
| SCH-2026-04 Festive Volume Rebate | Volume Rebate, 2% | 01/10/2026 to 30/11/2026 | Active | 2,750 of 2,500 sheets (the six October orders: 760 + 280 + 360 + 520 + 430 + 400), target reached, 250 above, 35 days left |
| SCH-2026-05 Marble Finish Launch Incentive | Product Incentive, ₹25 per sheet of LM-CAL-003 | 01/09/2026 to 31/12/2026 | Active | 180 of 300 sheets, earned ₹4,500 |
| SCH-2026-06 Winter Season Volume Bonus | Volume Bonus, 3% | 01/12/2026 to 31/01/2027 | Upcoming | target 3,500 sheets |
| SCH-2026-02 Monsoon Fast Mover Bonus | Product Incentive, ₹15 per sheet | 01/07/2026 to 30/09/2026 | Completed | 2,550 of 2,400 sheets, ₹38,250 credited |
| SCH-2026-01 Summer Stock Incentive | Volume Incentive, ₹20 per sheet | 01/04/2026 to 30/06/2026 | Completed | 2,310 of 2,000 sheets, ₹46,200 credited |

## Returns, support, users (Phase 3)

Return requests to Crestline (Credit Amount = sheets × the 50–199 price, only once credit is issued): RTN-2026-0412 25/10 ORD-2026-10431 CAL-003 12
sheets Damaged in Transit, Under Review; 0408 22/10 ORD-2026-10431 WNT-001 8 Surface Defect, Approved; 0396 16/10 ORD-2026-10398 ARC-002 20 Wrong Product
Delivered, Pickup Scheduled; 0377 09/10 ORD-2026-10372 OAK-004 15 Damaged in Transit, Credit Issued ₹18,000; 0361 02/10 ORD-2026-10341 CHR-007 10 Surface
Defect, Credit Issued ₹10,550; 0342 26/09 ORD-2026-10316 SLT-005 6 Shade Mismatch, Rejected; 0319 18/09 ORD-2026-10290 TEK-006 14 Damaged in Transit, Credit Issued ₹13,790.
Credit issued in all ₹42,340. Open requests 3 (40 sheets).

Support tickets (Crestline Customer Support, agent Meera Kapoor): TKT-2026-0731 24/10 Damaged Sheets in ORD-2026-10431, Delivery, High, In Progress;
0724 22/10 Invoice INV-2026-03264 Amount Query, Billing, Medium, Awaiting Your Reply; 0702 15/10 Price Tier Review Request, Account, Low, Open;
0688 09/10 Dispatch Delay on ORD-2026-10398, Delivery, Medium, Resolved; 0655 29/09 GST Correction on INV-2026-03198, Billing, Medium, Closed;
0631 21/09 Festive Scheme Eligibility, Schemes, Low, Closed. Ticket Details shows TKT-2026-0731 (four messages, three attachments).

Users of Distributor Alpha: Rajesh Menon (Owner, Active), Kavita Joshi (Sales and Operations Manager, Active), Suresh Iyer (Accountant, Active), Pooja
Deshpande (Sales and Operations Manager, Invited 24/10/2026), Amit Kulkarni (Accountant, Inactive, last signed in 30/06/2026). Phones +91 90000 21001 to 21005.
Notifications: the bell badge says 3, so each of the three roles has exactly three unread notifications.

## Phase 4 data (Manager and Accountant; model in `tools/author/data.py`, section "Phase 4")

**Lines of the six October orders** (purchases ₹33,52,882 = 9,49,752 + 3,36,500 + 4,42,930 + 6,18,400 + 5,24,100 + 4,81,200; 2,750 sheets).
10482, 10459, 10447 and 10431 as above. **10398 (430):** WNT 100, ARC 130, OAK 90, SLT 60, TEK 50. **10372 (400):** WNT 80, ARC 100, OAK 80, IVR 80, WNG 60.
Sheets purchased by product (October): WNT 600, ARC 830, CAL 140, OAK 390, SLT 120, TEK 240, IVR 200, SKY 60, CHR 60, WNG 110, STN 0, CPR 0.
Rule: never show sheets × price for a past order or invoice unless it multiplies out exactly; by-product money is allocated in proportion with a rounding plug (as `SOLD_VALUE`).

**Receipts at Bhiwandi Warehouse in October** (the delivered orders, on their delivery dates): 10372 on 06/10, 10398 on 13/10, 10431 on 20/10 = **1,350 sheets**.
**Stock adjustments (October, net −30):** ADJ-2026-0031 02/10 ARC −8 and 0036 23/10 TEK −10, 0035 21/10 WNT −6, 0034 12/10 CAL −5 (all Damaged in Handling); 0032 06/10 OAK −4 and 0033 09/10 SLT +3 (Count Correction).
**October stock movements: 108** (receipts 15 lines, sales to dealers 87 lines, adjustments 6): received 1,350, sold 2,195, adjusted −30, net −875 (8,290 at the start of October, 7,415 now).
Every dealer sale is split into product lines (`SALES[..]['lines']`; sum per sale = its sheets, sum per product = October sheets sold; CAL appears only on the seven dispatches already shown on Inventory Item Details).
**Inventory Item Details (LM-CAL-003) changed in Phase 4:** the 60 sheets of ORD-2026-10431 are received on 20/10 (Receipt from Crestline, +60), so balances before 20/10 are 60 lower (opening 325 before 03/10; 300, 275, 270, 245, 215, then 275, 260, 235, 215); batches B-2610-14 (20/10, 60), B-2608-07 (24/08, 100), B-2606-11 (14/06, 55); Inventory Reports ageing for CAL is 60 / 0 / 155.

**Dispatch status of dealer sales.** Expected delivery = sale date + days by city (Pune 2, Thane 3, Nashik 3, Kolhapur 4, Satara 4, Solapur 4, Nagpur 6, Panaji 5). Being Packed = dispatched today (26/10); Delivered = expected before today; otherwise In Transit. Result: 1 Being Packed (SAL-2026-3041), 2 In Transit, 29 Delivered. Incoming from Crestline: the three open orders (1,400 sheets) as on Inventory Overview.

**Low stock (Low Stock Overview).** Products below their reorder level: LM-CAL-003 (available 125, level 250), LM-CHR-007 (60, 200), LM-CPR-010 (55, 100) = Low Stock; LM-STN-009 (0, 150) = Out of Stock. Reorder quantity: CAL 400 (as on Item Details), CHR 300, STN 300, CPR 150; value at the slab price of that quantity: 5,80,000 + 3,03,000 + 4,12,500 + 2,74,500 = **₹15,70,000** (before GST). Sheets short of reorder level 460.

**Dealer targets (October).** BRV 6,50,000; DLT 6,00,000; FXT 4,50,000; GPL 4,25,000; HRS 3,75,000; IND 2,40,000; JYT 2,50,000; KNL 1,50,000 = ₹31,40,000. Achievement = sales ÷ target: 99.4% overall; Above Target (100% or more) Bravo 105.2%, Foxtrot 105.8%, Indira 102.5%, Kunal 103.3%; Near Target (95% to 99%) Delta 98.7%, Gopal 96.7%; Below Target Harsh 90.1%, Jayant 87.2%. Growth is October against September sales (Kunal is New).

**Pending dealer requests** (number series `DRQ-2026-0019`): DRQ-2026-0019 Dealer Mahesh, Amravati, Mahesh Gaikwad, 24/10, ₹3,00,000 credit, 120 sheets a month, 3 of 3 documents, Awaiting Your Review; DRQ-2026-0018 Dealer Navin, Sangli, Navin Kamble, 22/10, ₹3,50,000, 100 sheets, 2 of 3 documents, Awaiting Your Review; DRQ-2026-0017 Dealer Omkar, Jalgaon, Omkar Deshmukh, 19/10, ₹4,00,000, 150 sheets, 3 of 3, Sent to Crestline (reviewed by Kavita Joshi 21/10, waiting for Vikram Chopra). All submitted by Rajesh Menon. Requested credit ₹10,50,000.

**Accountant.** Credit limit ₹40,00,000; outstanding ₹14,86,320 (37%); credit available ₹25,13,680 (₹15,63,928 after ORD-2026-10482). **Ageing of the open invoices** (days past due date, today 26/10): Not Yet Due ₹11,67,920 (INV-03264, 03291, 03318); 1 to 30 days overdue ₹1,32,000 (INV-03021, 30 days); 31 to 60 days overdue ₹1,86,400 (INV-02986, 37 days); 61 to 90 and over 90: none. Overdue ₹3,18,400 = 21.4% of the balance.
**Tax split** (taxable + 2 × 9% + freight = total, freight ₹4,500 on an order below ₹5,00,000 when an exact split exists, else ₹0): October orders — 10482 taxable 8,04,874 GST 72,439 each, freight 0; 10459 2,81,356 / 25,322 / 4,500; 10447 3,71,550 / 33,440 / 4,500; 10431 5,24,068 / 47,166 / 0; 10398 4,44,152 / 39,974 / 0; 10372 4,07,796 / 36,702 / 0 (October: taxable ₹28,33,796, Central GST ₹2,55,043, State GST ₹2,55,043, freight ₹9,000). May to September totals are solved the same way in `MONTH_TAX` (freight 9,000 / 9,000 / 13,500 / 9,000 / 13,500). **Purchases are orders placed (₹33,52,882 in October); "Invoiced" is ₹20,66,630 (4 invoices, two October orders have no invoice yet). Screens name the basis.** Six-month purchases ₹1,52,72,882; payments ₹1,33,99,660.
**Credit notes** (the Phase 3 return credits, ₹42,340): CN-2026-0103 16/10 RTN-2026-0377 ORD-2026-10372 ₹18,000; CN-2026-0098 09/10 RTN-2026-0361 ORD-2026-10341 ₹10,550; CN-2026-0091 24/09 RTN-2026-0319 ORD-2026-10290 ₹13,790.
**Invoice disputes** (series `DIS-2026-0014`; disputed amounts stay inside the invoice balances): DIS-2026-0014 INV-2026-03264, 22/10, Wrong Product Delivered (20 sheets of LM-ARC-002 from ORD-2026-10398, return RTN-2026-0396; 20 × ₹905 = ₹18,100 + Central GST ₹1,629 + State GST ₹1,629 = **₹21,358**), Awaiting Your Reply, related ticket TKT-2026-0724; DIS-2026-0011 INV-2026-03021, 10/10, Quantity Shortfall, ₹16,992, Under Review; DIS-2026-0007 INV-2026-03198, 29/09, Tax Amount Mismatch, ₹4,284, Resolved. **Open disputes 2, ₹38,350.** Dispute Details shows DIS-2026-0014 (four messages, two attachments).
**Record Payment** is pre-filled with the two overdue invoices (₹1,86,400 + ₹1,32,000 = ₹3,18,400), Bank Transfer from Sahyadri Bank, Bhiwandi Branch; after it the balance would be ₹11,67,920 and nothing overdue.
