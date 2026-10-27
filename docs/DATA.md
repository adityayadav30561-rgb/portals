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

Orders `ORD-2026-10482`; dealer requests `DRQ-2026-0019`; invoice disputes `DIS-2026-0014`; credit notes `CN-2026-0103`; stock adjustments `ADJ-2026-0034`; invoices `INV-2026-03318`; payments `PAY-2026-02217`; dispatches `DSP-2026-5523`;
returns `RTN-2026-0412`; support tickets `TKT-2026-0731`; schemes `SCH-2026-04`; sales to dealers `SAL-2026-3041`. Batches `B-2610-14`. **Dealer-level documents issued by Distributor Alpha carry a "D" before the number so they never collide with the Crestline series:** payments `PAY-2026-D0521`, returns `RTN-2026-D0508`, support tickets `TKT-2026-D0746` (Alpha's own are PAY-2026-02217, RTN-2026-0412, TKT-2026-0731); tertiary sales `TSL-2026-0412`; each series runs in date order (asserted). Payment modes: Bank Transfer, Net Banking, Cheque (never UPI, NEFT, RTGS). Say "Bank Reference", not UTR or Ref.

## Distributor Alpha figures (Owner view)

- Credit limit ₹40,00,000; credit period 45 days; outstanding balance **₹14,86,320** (overdue ₹3,18,400).
- Purchases from Crestline by month: May 22,10,000; June 25,60,000; July 19,80,000; August 27,40,000; September 24,30,000; October **33,52,882** (to 26 October).
- Sales to dealers by month: May 24,80,000; June 28,10,000; July 22,40,000; August 30,60,000; September 27,90,000; October **31,20,000**.
- Orders: 142 in total: Awaiting Confirmation 1, Confirmed 1, In Transit 1, Delivered 136, Cancelled 3 (changed from 2, 3, 2, 132 on 2026-10-27 so the counts match the orders listed: the latest ten orders hold every open order).
- Schemes: **Festive Volume Rebate** (`SCH-2026-04`): 2% rebate on orders once 2,500 sheets are reached across October and November (changed from 3,000 on 2026-10-26 by the user); progress 2,750 of 2,500 sheets: **target reached**, 250 above. ORD-2026-10482 is the order that takes the total over the target (1,990 before it), so the rebate applies to that order only (−₹16,426); earlier invoices are not changed. **Marble Finish Launch Incentive**: ₹25 per sheet of LM-CAL-003, progress 140 of 300 sheets.

## Order flow (Place Order → Order Builder → Order Confirmation)

**ORD-2026-10482**, placed 26/10/2026 11:42 by Rajesh Menon, delivery to Bhiwandi Warehouse requested 31/10/2026, Company Transport.

| SKU | Sheets | Price | Amount |
|---|---|---|---|
| LM-WNT-001 | 200 | 1,095 | 2,19,000 |
| LM-ARC-002 | 300 | 870 | 2,61,000 |
| LM-CAL-003 | 80 | 1,510 | 1,20,800 |
| LM-OAK-004 | 120 | 1,200 | 1,44,000 |
| LM-SLT-005 | 60 | 1,275 | 76,500 |

760 sheets; subtotal ₹8,21,300; Festive Volume Rebate 2% −₹16,426; taxable ₹8,04,874; Central GST ₹72,439; State GST ₹72,439; freight ₹0 (free above ₹4,50,000); **total ₹9,49,752**. Credit available after the order: ₹15,63,928.

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

Placed 19/10/2026 by Rajesh Menon; confirmed 20/10; packed 23/10; dispatched 24/10/2026 06:30 as `DSP-2026-5523` from
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
| SCH-2026-05 Marble Finish Launch Incentive | Product Incentive, ₹25 per sheet of LM-CAL-003 | 01/09/2026 to 31/12/2026 | Active | 140 of 300 sheets (60 delivered on 20/10 plus the 80 on ORD-2026-10482; changed from 180 on 2026-10-26 so it agrees with the stock history), earned ₹3,500 |
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

## Phase 5 data (Secondary Customer: Dealer Bravo, Pune; model in `tools/author/data.py`, section "Phase 5")

**Orders to Distributor Alpha are the Alpha sales ledger rows of Dealer Bravo.** The sale number is the order number and the invoice number (`SAL-2026-3040`).
Bravo's six October orders (SAL-2026-3010, 3017, 3021, 3029, 3033, 3040; 480 sheets, ₹6,84,000; owes ₹2,60,000 = 3033 + 3040); September ₹6,10,000; monthly purchases May to October
5,20,000; 5,90,000; 4,80,000; 6,30,000; 6,10,000; 6,84,000. Order History also shows SAL-2026-3006 (30/09, 95 sheets, ₹1,35,500), 2999 (22/09, 105, ₹1,48,000) and 2990 (14/09, 75, ₹1,06,500), all Paid.
Counts for the tabs: 212 orders (1 Awaiting Confirmation, 1 In Transit, 208 Delivered, 2 Cancelled). Orders This Month 6 (₹6.84 lakh); an order awaiting confirmation is not counted until confirmed.
**The order placed on 26/10/2026 16:05 by Sunita Rao is `SAL-2026-3042`** (Awaiting Confirmation, delivery requested 30/10): WNT 60, ARC 80, OAK 40, TEK 30 = 210 sheets at the dealer price (Dealer Tier B, `dp()`; no volume slabs): subtotal ₹2,49,000, Central GST ₹22,410, State GST ₹22,410, **total ₹2,93,820**, freight free; credit available after it ₹2,46,180 (limit ₹8,00,000, owes ₹2,60,000). Alpha's Dealer Order Activity and Manager Dashboard show it as the one order awaiting confirmation; the Alpha ledger (32 sales, ₹31,20,000) is unchanged.
**Order Details shows SAL-2026-3040** (CAL 25, SKY 10, ARC 65; subtotal ₹1,19,700 at dealer prices, trade discount −₹3,598, taxable ₹1,16,102, Central GST and State GST ₹10,449 each, total ₹1,37,000, issued 24/10, due 23/11, dispatched 24/10 17:45 as DSP-2026-5527, expected 26/10, vehicle MH 12 QR 4418, driver Santosh Gaikwad, +91 90000 12346).
Retailer price (Retailer Tier C, `rp()`) = dealer price + 12%, to the nearest ₹5.

**Bravo's stock (sheets; on hand / reserved for retailers / reorder level; on order from the two open orders):** WNT 180/45/80 (on order 60); ARC 240/60/100 (145); CAL 38/12/40 (25); OAK 95/20/60 (40); SLT 60/15/40; TEK 110/25/60 (30); CHR 22/10/40; IVR 140/30/80; STN 0/0/30; CPR 18/6/20; WNG 85/20/50; SKY 70/18/40 (10).
Total on hand **1,058**, reserved 261, on order 310, stock value at dealer price ₹12,55,785. Status rule: Out of Stock at 0 on hand; Low Stock when available is below the reorder level (CAL, CHR, CPR); 8 In Stock, 3 Low, 1 Out, as for Alpha.
**Inventory Item Details (LM-CAL-003):** 38 on hand, 26 available, receipt +25 on 10/10 (SAL-2026-3021), six sales to retailers (−33 in October), balance 46 at the start of October, batches B-2610-19 (10/10, 25) and B-2609-08 (12/09, 13), reorder 100 sheets, 2 days lead time, 20 days of cover.

**Retailers of Dealer Bravo** (Retailer Tier C, credit period 15 days): Retailer Charlie (Camp, Pune; Imran Sheikh; since 11/05/2021; limit ₹3,00,000; GST 27AAJCC4410E1ZK; Shop 12, MG Road, Camp, Pune, Postal Code 411001; contacts Imran Sheikh Retailer Owner +91 90000 51001, Pooja Verma Sales Executive 51002, Faisal Khan Inventory and Purchasing Executive 51003);
Retailer Kiran Interiors (Kothrud, Pune; Kiran Desai; 03/02/2022; ₹2,50,000); Retailer Mehta Furniture (Pimpri Chinchwad, Pimpri; Nilesh Mehta; 19/09/2022; ₹2,00,000).
**Bravo's sales to retailers (October ₹6,30,000, 370 sheets, September ₹6,00,000):** Charlie ₹2,64,000 (155 sheets; September 2,40,000), Kiran ₹2,10,000 (125; 1,95,000), Mehta ₹1,56,000 (90; 1,65,000). Monthly May to October: total 5,10,000; 5,60,000; 4,70,000; 6,00,000; 6,00,000; 6,30,000 (Charlie 1,90,000; 2,10,000; 1,75,000; 2,30,000; 2,40,000; 2,64,000).
Twelve sales `TSL-2026-0401` to `0412` (newest 0412, Charlie 25/10, ₹62,000, unpaid); owed ₹1,10,000 (Charlie ₹62,000 = TSL-0412, Kiran ₹48,000 = TSL-0411, Mehta nil). Phase 6 builds on this ledger.
**Dealer schemes from Distributor Alpha:** `SCH-2026-07` Dealer Festive Volume Rebate (1% once 750 sheets, 01/10 to 30/11/2026; progress 690 of 750 = 480 recorded + 210 on SAL-2026-3042, so the rebate is not yet earned); `SCH-2026-08` Marble Finish Dealer Incentive (₹15 per sheet of LM-CAL-003, 01/10 to 31/12/2026; 50 of 100 sheets, earned ₹750).
**Add Retailer Request:** Retailer Dhruv Interiors, Wakad, Pune, Dhruv Patil, GST 27AAHFD6620L1Z8, requested credit ₹1,50,000, 60 sheets a month, 2 of 3 documents; path: Dealer Review Arjun Nair, Distributor Approval Kavita Joshi.
**Dealer Bravo profile:** customer code CUS-0127, legal name Bravo Laminate Traders, established 2015, GST 27AAKFB3318D1ZP, credit used 32% (₹2,60,000 of ₹8,00,000).

## Phase 6 data (Secondary Owner, part 2; model in `tools/author/data.py`, section "Phase 6")

**Invoices from Distributor Alpha to Dealer Bravo** are the Alpha sales ledger rows (invoice number = sale number), issued on the sale date, due 30 days later: SAL-2026-3040 (24/10, due 23/11, ₹1,37,000, Unpaid), 3033 (17/10, due 16/11, ₹1,23,000, Unpaid), 3029, 3021, 3017, 3010, 3006, 2999, 2990 (all Paid).
**Open invoices ₹2,60,000 = the outstanding balance; none overdue.** 209 invoices in all (every in-transit or delivered order): 2 open, 207 paid. Invoice Details shows **SAL-2026-3040** with exactly the Order Details figures (subtotal ₹1,19,700, trade discount −₹3,598, Central GST and State GST ₹10,449, total ₹1,37,000). Issued by Distributor Alpha Private Limited, GST 27AABCD4521F1Z7, Bhiwandi Warehouse; billed to Bravo Laminate Traders, GST 27AAKFB3318D1ZP.
**Payments by Dealer Bravo to Distributor Alpha** (newest first; recorded by Sunita Rao): PAY-2026-D0521 22/10 ₹1,09,500 Bank Transfer (SAL-3029); D0517 17/10 ₹1,23,000 Cheque (3021); D0511 14/10 ₹96,000 Net Banking (3017); D0506 10/10 ₹95,500 Bank Transfer (3010); D0501 06/10 ₹1,35,500 Cheque (3006); D0494 29/09 ₹1,48,000 Bank Transfer (2999); D0488 24/09 ₹1,06,500 Net Banking (2990); D0479 15/09 ₹1,84,000 Bank Transfer (SAL-2026-2975); D0471 03/09 ₹1,62,000 Cheque (2962); D0462 28/08 ₹2,10,000 Net Banking (2948).
**Paid in October ₹5,59,500 in 5 payments** (Bank Transfer 2,05,000; Cheque 2,58,500; Net Banking 96,000). Paid by month May to October: 5,10,000; 5,85,000; 5,00,000; 6,10,000; 6,05,000; 5,59,500. 207 payments in all (one payment settles one paid invoice in full). **Payment Details shows PAY-2026-D0521:** recorded 22/10/2026 10:40 by Sunita Rao, received by Distributor Alpha 22/10 15:10, confirmed 23/10 09:20; paid from Sahyadri Bank, Hadapsar Branch; Bank Reference SB26102200318; settles SAL-2026-3029 in full.

**Sales to retailers by product (October, 370 sheets, ₹6,30,000):** WNT 60, ARC 85, CAL 33 (the six quantities on Inventory Item Details), OAK 25, SLT 15, TEK 40, CHR 18, IVR 35, STN 0, CPR 7, WNG 30, SKY 22; value allocated by sheets × retailer price with a rounding plug. Every `TSL` sale has product lines that add up to its sheets (`TSALES[..]['lines']`). Stock check (asserted): on hand now minus October receipts from the five delivered orders plus October retail sales is never negative; opening stock: WNT 135, ARC 240, CAL 46, OAK 110, SLT 65, TEK 80, CHR 40, IVR 165, STN 0, CPR 0, WNG 75, SKY 92 (this ignored adjustments; **replaced in Phase 7**: WNT 138, ARC 240, CAL 46, OAK 114, SLT 63, TEK 80, CHR 40, IVR 170, STN 0, CPR 0, WNG 78, SKY 92 = 1,061).
**Ageing of Bravo's stock (up to 30 days / 31 to 60 / over 60 days):** CAL 25 / 13 / 0 (batches B-2610-19 and B-2609-08); everything received in October sits in the youngest band for every product.
**Tertiary Sales Entry** (the example form): sale to Retailer Charlie, WNT 20, ARC 30, CAL 5, OAK 10 at the retailer price: subtotal ₹88,800, Central GST ₹7,992, State GST ₹7,992, total ₹1,04,784 (number TSL-2026-0413: the order Retailer Charlie placed on 26/10/2026 11:20, awaiting confirmation, see Phase 7 data); credit available after it ₹1,33,216.
**Dealer schemes** (issued by Distributor Alpha): SCH-2026-07 Dealer Festive Volume Rebate, 1% of order value, 01/10 to 30/11/2026, 690 of 750 sheets (the seven October orders including SAL-2026-3042); SCH-2026-08 Marble Finish Dealer Incentive ₹15 per sheet of LM-CAL-003, 01/10 to 31/12/2026, 50 of 100 sheets, earned ₹750; SCH-2026-09 Winter Season Dealer Bonus, 2% at 1,400 sheets, 01/12/2026 to 31/01/2027, Upcoming; SCH-2026-03 Monsoon Dealer Incentive ₹10 per sheet, 01/07 to 30/09/2026, 1,310 of 1,200 sheets, ₹13,100 credited, Completed. Incentives earned this year ₹13,850. **These are placeholders, to be confirmed by the user.**
**Returns to Distributor Alpha** (credit = sheets × dealer price, only once Credit Issued): RTN-2026-D0508 22/10 SAL-3033 WNT 6 Surface Defect, Under Review; D0503 16/10 SAL-3029 TEK 4 Damaged in Transit, Approved; D0494 14/10 SAL-3021 OAK 3 Damaged in Transit, Credit Issued ₹4,095; D0486 09/10 SAL-3017 CPR 2 Surface Defect, Credit Issued ₹4,160; D0479 04/10 SAL-3010 ARC 5 Shade Mismatch, Rejected. Credit issued ₹8,255; open 2 (10 sheets). Create Return Request is filled in for SAL-2026-3033 (WNT 35, TEK 40, IVR 10).
**Support tickets with Distributor Alpha** (agent Kavita Joshi): TKT-2026-D0746 25/10 Delivery Timing for SAL-2026-3040, Delivery, Medium, In Progress; D0737 23/10 Price Tier Review Request, Account, Low, Open; D0719 18/10 Surface Defect in SAL-2026-3033, Delivery, High, Resolved; D0696 10/10 Invoice SAL-2026-3021 Amount Query, Billing, Medium, Closed; D0661 30/09 Festive Scheme Eligibility, Schemes, Low, Closed. Ticket Details shows D0746 (four messages, one attachment).
**Users of Dealer Bravo** (two roles: Owner, Sales and Inventory Manager): Sunita Rao (Owner, Active), Arjun Nair (Sales and Inventory Manager, Active), Meena Kulkarni (Sales and Inventory Manager, Invited 24/10/2026), Rohit Pawar (Sales and Inventory Manager, Inactive, last signed in 30/06/2026). Phones +91 90000 31001, 31002, 31004, 31005; email `first.last@dealerbravo.example`. Rekha Sawant is a contact, not a user. User Details shows Arjun Nair.
**Notifications:** three unread for each of the Owner and the Manager (the bell badge says 3); every number in them exists in this file.

## Phase 7 data (Secondary Manager: Arjun Nair, Sales and Inventory Manager of Dealer Bravo; model in `tools/author/data.py`, section "Phase 7")

**New number series (documents Dealer Bravo issues itself; kept apart from Distributor Alpha's DRQ, ADJ-2026-00xx and DSP series and from the "D" series of documents Alpha issues to Bravo):** retailer requests `RRQ-2026-0005` to `0007`; deliveries to retailers `DLV-2026-0401` to `0412` (the number ends like its sale number); stock adjustments `ADJ-2026-B0011` to `B0015`.
**The retailer order awaiting confirmation is `TSL-2026-0413`:** placed 26/10/2026 11:20 by Imran Sheikh for Retailer Charlie (the Phase 8 Tertiary Retailer organisation), delivery requested 28/10: WNT 20, ARC 30, CAL 5, OAK 10 = 65 sheets, ₹1,04,784 (the Tertiary Sales Entry example of Phase 6, so Phase 8 inherits it). Like SAL-2026-3042 for Alpha it is **not** in the ledger: the 12 sales, ₹6,30,000, 370 sheets and ₹1,10,000 owed are unchanged; Charlie's credit after it is ₹1,33,216.

**Deliveries to retailers** (rule: dispatched on the sale date, except TSL-2026-0412, recorded Sunday 25/10 and dispatched Monday 26/10; expected = dispatch + days by area: Camp 1, Kothrud 2, Pimpri Chinchwad 2; Being Packed = dispatched today, Delivered = expected before today, else In Transit). Result: **1 Being Packed (TSL-0412, expected 27/10), 1 In Transit (TSL-0411, expected today), 10 Delivered**, plus 1 order awaiting confirmation (0413). Two vehicles of Bravo: MH 12 PQ 2204 (Tata Ace, driver Ramesh Kale, +91 90000 31011) and MH 12 RS 7716 (Mahindra Bolero Pickup, driver Sandeep Jagtap, +91 90000 31012), alternating by sale number (odd numbers MH 12 RS 7716).
**Actual delivery dates:** on the expected date except **TSL-2026-0404** (expected 07/10, delivered 08/10) and **TSL-2026-0407** (expected 15/10, delivered 16/10), both one day late. **8 of 10 delivered on time (80.0%)**; average delivery time from dispatch **1.8 days**. Weekly retail sales (1 to 7 / 8 to 14 / 15 to 21 / 22 to 26 October): ₹1,83,000; ₹1,62,000; ₹1,75,000; ₹1,10,000.
**Retailer targets (October):** Charlie ₹2,50,000 (105.6%, Above Target); Kiran ₹2,20,000 (95.5%, Near Target); Mehta ₹1,70,000 (91.8%, Below Target); total **₹6,40,000**, achievement 98.4% (Bravo's own purchase target from Alpha is ₹6,50,000). Growth is October against September: Charlie +10.0%, Kiran +7.7%, Mehta −5.5%.

**Stock adjustments of Dealer Bravo (October, net −13):** ADJ-2026-B0011 03/10 IVR −5, B0012 11/10 WNT −3, B0015 24/10 OAK −4 (all Damaged in Handling); B0013 20/10 SLT +2 and B0014 20/10 WNG −3 (Count Correction). None touches LM-CAL-003.
**October stock movements: 67** (receipts 15 lines, sales to retailers 47 lines, adjustments 5): received 380 (the five delivered orders SAL-3010, 3017, 3021, 3029, 3033 on their expected delivery dates 03, 07, 10, 15, 19/10; SAL-3040 arrives today and is not yet received), sold 370, adjusted −13, net −3: **1,061 sheets at the start of October, 1,058 now**. CAL rows equal Inventory Item Details exactly. Two of the 47 sale lines were swapped between sales (CPR is received on 07/10, so Mehta's and Charlie's earlier sales could not carry it): invisible on any earlier screen.
**Stock count of 20/10/2026** (all 12 products): system 1,163 sheets, two products differ: SLT 58 counted 60 (+2), WNG 88 counted 85 (−3) = 5 sheets of 1,163 = **stock count accuracy 99.6%**; 10 of 12 products matched.
**Returns to Distributor Alpha** (from Phase 6; direction always labelled; they are not stock movements, as in Phase 4): 5 requests, 20 sheets of the 480 sheets bought in October (4.2%), credit issued ₹8,255 (RTN-2026-D0494, D0486), 2 open, 1 rejected.

**Reorder rule (one line):** reorder quantity = 2.5 × reorder level to a multiple of 25 (CAL 100, as on Inventory Item Details; CHR 100; CPR 50; STN 75; the rest 200, 250, 150, 175, 150, 125, 100, 125, 100); recommended only when **available is below the reorder level** (CAL, CHR, CPR low; STN out); suggested quantity = the reorder quantity, limited to what Distributor Alpha has available (125 CAL, 60 CHR, 55 CPR, 0 STN) in multiples of 25, value at the dealer price: **CAL 100 (₹1,71,500), CHR 50 (₹60,000), CPR 50 (₹1,04,000) = 200 sheets, ₹3,35,500 before GST**; STN is "Distributor Alpha Out of Stock" (no order possible). Days of cover = available ÷ (October retail sheets ÷ 26): CAL 20, CHR 17, CPR 45. Sheets short of reorder level (the four low products): CAL 14 + CHR 28 + STN 30 + CPR 8 = **80**.
**Pending retailer requests** (all submitted by Sunita Rao; Dealer Review by Arjun Nair, then Distributor Approval by Kavita Joshi; Dhruv Interiors is a draft on Add Retailer Request and is not in the list, as with Dealer Lakshya in Phase 4): RRQ-2026-0007 Retailer Sahyadri Interiors, Baner, Pune, Anil Pingale, 24/10, ₹2,00,000, 70 sheets a month, 3 of 3 documents, Awaiting Your Review; RRQ-2026-0006 Retailer Ganesh Furniture Mart, Katraj, Pune, Ganesh Londhe, 22/10, ₹1,50,000, 50 sheets, 2 of 3, Awaiting Your Review; RRQ-2026-0005 Retailer Vishwas Decor, Hinjewadi, Pune, Vishal Thorat, 19/10, ₹2,50,000, 90 sheets, 3 of 3, Sent to Distributor Alpha (reviewed by Arjun Nair 21/10, waiting for Kavita Joshi). Requested credit ₹6,00,000.

## Phase 8 data (Tertiary Retailer Owner, part 1: Retailer Charlie, Camp, Pune; Owner Imran Sheikh; supplier Dealer Bravo; model in `tools/author/data.py`, section "Phase 8")

**Repeated from earlier phases (must agree everywhere):** credit limit ₹3,00,000, credit period 15 days, Retailer Tier C, customer since 11/05/2021, GST 27AAJCC4410E1ZK, Shop 12, MG Road, Camp, Pune, Postal Code 411001, contacts Imran Sheikh
(Retailer Owner, +91 90000 51001), Pooja Verma (Sales Executive, 51002), Faisal Khan (Inventory and Purchasing Executive, 51003), relationship manager Arjun Nair; owes ₹62,000 (21% of the limit, TSL-2026-0412 only).
**Number series Charlie issues itself:** sales to customers `RSL-2026-0361` to `0398` (newest 0398; Phase 9 continues at 0399); stock adjustments `ADJ-2026-C0004` to `C0006`. Offers from Dealer Bravo to its retailers `OFR-2026-01`, `02` (apart from the SCH-2026-xx schemes).
**Price rule (one line, `crp()`):** the price Charlie charges a customer per sheet before GST = the Retailer Tier C price (`rp()`) plus 25%, to the nearest ₹5; every retail sale = sheets × that price, then Central GST and State GST of 9% each (rounded), so it multiplies out exactly.

**Orders of Retailer Charlie = Bravo's TSL sales** (newest first): TSL-2026-0413 26/10 65 sheets ₹1,04,784 Awaiting Confirmation (requested delivery 28/10, placed 11:20 by Imran Sheikh: WNT 20, ARC 30, CAL 5, OAK 10 at the retailer price: subtotal ₹88,800, Central GST and State GST ₹7,992, freight free; credit available after it ₹1,33,216);
0412 25/10 35 sheets ₹62,000 Being Packed (placed 25/10 16:50 by Imran Sheikh, confirmed and recorded 25/10 17:20, packing started 26/10 10:15, dispatched 26/10 as DLV-2026-0412 on MH 12 PQ 2204, driver Ramesh Kale, expected 27/10, Unpaid); 0409 19/10 35 ₹58,000; 0406 12/10 30 ₹52,000; 0404 06/10 30 ₹49,000; 0401 01/10 25 ₹43,000 (all Delivered, Paid); September (all Delivered, Paid): 0400 29/09 35 ₹64,000; 0397 18/09 40 ₹66,000; 0394 11/09 35 ₹58,000; 0391 04/09 30 ₹52,000 (₹2,40,000).
**October: 5 confirmed orders, 155 sheets, ₹2,64,000 (the order awaiting confirmation is not counted).** 248 orders in all since 2021: 1 Awaiting Confirmation, 1 Being Packed, 244 Delivered, 2 Cancelled; 245 invoices (every dispatched or delivered order): 1 open (TSL-2026-0412), 244 paid.
Purchases by month May to October: 1,90,000; 2,10,000; 1,75,000; 2,30,000; 2,40,000; 2,64,000 (₹13,09,000). **TSL-2026-0412 (Order Details):** its ledger value does not multiply out from the lines (CAL 6, ARC 29), so, as in Phase 4, the taxable amount ₹52,542 is allocated to the lines with a rounding plug (no price-per-sheet column), Central GST and State GST ₹4,729 each, total ₹62,000; invoice number = order number, issued 25/10, due 09/11/2026.
Sheets bought in October by product: WNT 30, ARC 39, CAL 14, OAK 5, TEK 10, CHR 8, IVR 17, WNG 20, SKY 12 (= 155); money allocated like `SOLD_VALUE` (₹2,64,000).

**Charlie's stock (on hand / reserved for customers / reorder level; sheets sold to customers in October; on order):** WNT 42/6/30; 38; 20. ARC 38/4/30; 36; 59. CAL 9/2/10; 14; 11. OAK 11/2/10; 9; 10. SLT 8/0/6; 4. TEK 24/3/15; 17. CHR 6/1/8; 7. IVR 30/4/20; 15. STN 0/0/6; 0. CPR 4/0/3; 2. WNG 26/3/15; 12. SKY 18/2/12; 9.
Total on hand **216**, reserved 27, sold 163, on order **100** (0412: CAL 6, ARC 29; 0413: WNT 20, ARC 30, CAL 5, OAK 10); stock value at the retailer price in `CSTOCK_VALUE`. Status rule as before: 8 In Stock, 3 Low (CAL, OAK, CHR), 1 Out (STN).
**Receipts** are the delivered orders on Bravo's actual delivery dates: 0401 on 02/10 (WNT 10, ARC 10, OAK 5), 0404 on 08/10 (WNG 10, SKY 10, WNT 10), 0406 on 13/10 (CAL 8, TEK 7, CHR 8, IVR 7), 0409 on 20/10 (TEK 3, IVR 10, WNG 10, SKY 2, WNT 10) = 120 sheets.
**Adjustments (net −2):** ADJ-2026-C0004 07/10 WNG −1 and C0005 15/10 TEK −2 (Damaged in Handling); C0006 22/10 SLT +1 (Count Correction). Opening stock at the start of October **261** (= 216 − 120 + 163 + 2, per product in `C_OPENING`).
**Sales to customers in October (the ledger `CSALES`):** 38 sales (RSL-2026-0361 to 0398), 64 product lines, 163 sheets, ₹3,27,557 including GST (September ₹3,05,000; monthly May to October 2,45,000; 2,70,000; 2,30,000; 2,95,000; 3,05,000; 3,27,557); customers are individuals and small businesses, payment by Cash, Card, Bank Transfer or Cheque. Built without random numbers (an even spread of products over the days) so every run of the generator gives the same ledger. **October stock movements: 82** (receipts 15 lines, retail sales 64, adjustments 3); stock never goes negative at any point (asserted).
**Reorder rule (same as Dealer Bravo):** recommended when available is below the reorder level; reorder quantity = 2.5 × reorder level up to a multiple of 5; suggested quantity = the reorder quantity limited to what Dealer Bravo has available (multiples of 5); value at the retailer price. Result: **CAL 25 (₹48,000), OAK 25 (₹38,250), CHR 10 (₹13,450: Bravo has 12) = 60 sheets, ₹99,700 before GST (₹1,17,646 with GST, inside the ₹1,33,216 credit left)**; STN 15 would be needed but Dealer Bravo is out ("Out at Dealer Bravo"). CAL's reorder quantity on Inventory Item Details is 25, lead time 2 days. Days of cover = available ÷ (October sheets sold ÷ 26): CAL 13.
**Offers from Dealer Bravo (placeholders; progress = recorded orders plus the pending order, as for Bravo's schemes):** OFR-2026-01 Retailer Festive Volume Rebate, 1.5%, 01/10 to 30/11/2026, 220 of 250 sheets (155 + 65); OFR-2026-02 Marble Finish Retailer Incentive, ₹10 per sheet of LM-CAL-003, 01/10 to 31/12/2026, 19 of 50 sheets (14 recorded + 5), earned ₹140.
**Store Profile:** legal name Charlie Laminates Private Limited (the GST number's PAN, AAJCC, says company, C), retailer code RTL-0041, established 2018; contacts as above; documents GST Registration Certificate, Shop Licence, Retailer Agreement 2026–27.

**Changes to Phase 8 data made in Phase 9 (while only Phase 8 depended on them):** the last three sales to customers (RSL-2026-0396, 0397, 0398) are dated 26/10 (so "today" has three sales; 25/10 has none), every sale has a time and a recorder.
**Sale time and recorder rule:** the sales of a day are spaced through the shop day, starting 10:30 (fixed offset by day, 0 to 44 minutes); today's three are at 10:30, 13:10 and 15:50 (before 16:05, the time of Bravo's latest order); each sale is recorded by Pooja Verma, except every fourth sale in order (the 4th, 8th ... of the month) by Imran Sheikh. Customer phones `+91 98900 4xxxx`. The dashboard line "Incentive Earned" became "Earned on Active Offers" (₹140).

## Phase 9 data (Tertiary Retailer Owner, part 2: Retailer Charlie; model in `tools/author/data.py`, section "Phase 9")

**Letter rule for documents Dealer Bravo issues to its retailers (payments, returns, tickets): a "B" before the number** (PAY-2026-B0388, RTN-2026-B0214, TKT-2026-B0452), as Distributor Alpha's "D" for dealers; it never collides with Bravo's own ADJ-2026-B0011 to B0015 (different prefix). Charlie's own: RSL, ADJ-2026-C.
**Invoices from Dealer Bravo = Charlie's orders** (number = order number, issued on the order date, due 15 days later): 245 invoices, **1 open** (TSL-2026-0412, issued 25/10, due 09/11/2026, due in 14 days, ₹62,000 = the outstanding balance, none overdue), 244 paid. Invoice Details shows 0412 with the Order Details figures (CAL ₹13,403, ARC ₹39,139, taxable ₹52,542, Central GST and State GST ₹4,729, total ₹62,000; no price-per-sheet column). Issued by Bravo Laminate Traders, GST 27AAKFB3318D1ZP, Hadapsar Godown; billed to Charlie Laminates Private Limited. Two older invoices appear on the lists: TSL-2026-0385 (28/08, ₹58,000) and TSL-2026-0379 (18/08, ₹54,000).
**Payments by Charlie to Bravo** (one payment settles one paid invoice; newest first): PAY-2026-B0388 22/10 ₹58,000 Bank Transfer (0409); B0381 14/10 ₹52,000 Cheque (0406); B0376 10/10 ₹49,000 Net Banking (0404); B0369 05/10 ₹43,000 Bank Transfer (0401); B0364 03/10 ₹64,000 Cheque (0400); B0348 22/09 ₹66,000 Bank Transfer (0397); B0341 15/09 ₹58,000 Net Banking (0394); B0333 08/09 ₹52,000 Cheque (0391); B0326 02/09 ₹58,000 Bank Transfer (0385); B0319 25/08 ₹54,000 Net Banking (0379).
**Paid in October ₹2,66,000 in 5 payments** (Bank Transfer 1,01,000; Cheque 1,16,000; Net Banking 49,000). **Paid by month May to October: 1,40,000; 2,08,000; 1,72,000; 2,27,000; 2,34,000; 2,66,000** = purchases of the month + unpaid at the start − unpaid at the end (unpaid at the end of May ... October: 50,000; 52,000; 55,000; 58,000; 64,000; 62,000; **nothing unpaid before May, carry-in 0**), so six-month payments ₹12,47,000 = purchases ₹13,09,000 − ₹62,000. 244 payments in all.
**Payment Details shows PAY-2026-B0388:** recorded 22/10/2026 11:15 by Imran Sheikh, received by Dealer Bravo 22/10 15:40, confirmed 23/10 10:05; paid from Deccan Merchants Bank, Camp Branch; Bank Reference DM26102200211; settles TSL-2026-0409 in full.
**Offers** (placeholders): OFR-2026-01 Retailer Festive Volume Rebate 1.5%, 220 of 250 sheets (qualifying orders 0413 65, 0412 35, 0409 35, 0406 30, 0404 30, 0401 25), 35 days left; OFR-2026-02 Marble Finish Retailer Incentive ₹10 a sheet of LM-CAL-003, 19 of 50, earned ₹140;
OFR-2026-04 Winter Season Retailer Bonus 2% at 400 sheets, 01/12/2026 to 31/01/2027, Upcoming; OFR-2026-03 Monsoon Retailer Incentive ₹5 a sheet, 01/07 to 30/09/2026, 376 of 350 sheets (July 102 + August 134 + September 140), ₹1,880 credited, Completed. Incentives earned this year ₹2,020.
**Sales reports (sales to customers, October):** ₹3,27,557 including GST (up 7.4% on September's ₹3,05,000), 163 sheets, 38 sales, average ₹8,620 (₹8,619.92 rounded); **before GST ₹2,77,595 = sheets × crp() exactly; the product and finish tables are before GST and say so**. By week (1 to 7, 8 to 14, 15 to 21, 22 to 26 October, including GST): ₹97,726; ₹99,862; ₹73,644; ₹56,325. By payment mode (sales, value): Card 13, ₹1,12,808; Cash 13, ₹1,19,383; Cheque 6, ₹45,953; Bank Transfer 6, ₹49,413. **No profit or margin total anywhere** (Product Details' margin per sheet, based on the retailer price, is the only margin).
**Stock ageing** (up to 30 / 31 to 60 / over 60 days; October receipts in the youngest band): CAL 9 / 0 / 0 (batches B-2610-31 and B-2609-26); the rest in `CAGE` (sums to 216).
**Returns to Dealer Bravo** (credit = sheets × retailer price, only once issued; not stock movements): RTN-2026-B0214 25/10 TSL-0409 WNG 3 Surface Defect, Under Review; B0208 21/10 TSL-0406 CHR 2 Damaged in Transit, Approved; B0199 14/10 TSL-0404 SKY 2 Shade Mismatch, Credit Issued ₹2,140; B0186 08/10 TSL-0401 OAK 1 Surface Defect, Credit Issued ₹1,530. Credit issued ₹3,670; open 2 (5 sheets). Create Return Request is filled in for TSL-2026-0409 (IVR 2, WNT 1).
**Support tickets with Dealer Bravo** (agent Arjun Nair): TKT-2026-B0452 25/10 Delivery Timing for TSL-2026-0412, Delivery, Medium, In Progress; B0447 23/10 Price Tier Review Request, Account, Low, Open; B0441 20/10 Surface Defect in TSL-2026-0409, Delivery, High, Resolved; B0430 12/10 Invoice TSL-2026-0406 Amount Query, Billing, Medium, Closed; B0412 01/10 Festive Offer Eligibility, Schemes, Low, Closed. Ticket Details shows B0452 (four messages about vehicle MH 12 PQ 2204, driver Ramesh Kale, expected 27/10).
**Users of Retailer Charlie** (three roles: Retailer Owner, Sales Executive, Inventory and Purchasing Executive): Imran Sheikh (Owner, Active, last sign-in 26/10/2026 09:02), Pooja Verma (Sales Executive, Active, 26/10 09:40), Faisal Khan (Inventory and Purchasing Executive, Active, 26/10 09:15), Mohit Gawande (Sales Executive, Invited 24/10/2026), Sneha Ranpise (Inventory and Purchasing Executive, Inactive, last signed in 31/07/2026). Phones +91 90000 51001 to 51005; email `first.last@retailercharlie.example`. User Details shows Pooja Verma.
**Notifications:** three unread for each of the Owner, the Sales Executive and the Inventory and Purchasing Executive (the bell says 3); times agree with the events above.
**Record Retail Sale (the example form):** sale to a new customer Rakesh Bhalerao, ARC 3, WNT 1, TEK 3 at `crp()`, paid by Card (number RSL-2026-0399 on saving): subtotal ₹10,880, Central GST and State GST ₹979 each, total ₹12,838 (changed in Phase 10 so it matches no figure of today's sales). The form is unsaved, so Phase 10's Sales Executive screens count only today's three recorded sales.

## Phase 10 data (Tertiary Sales Executive and Inventory and Purchasing Executive; model in `tools/author/data.py`, sections "Phase 8" and "Phase 9"; nothing new is invented)

**Today (26/10/2026) at Retailer Charlie: 3 sales, ₹17,541 including GST, 10 sheets, average ₹5,847:** RSL-2026-0396 10:30 Rutuja Interiors 3 sheets ₹4,407 (recorded by Imran Sheikh); 0397 13:10 Dattatray Pawale 5 sheets ₹8,838 and 0398 15:50 Varsha Kulthe 2 sheets ₹4,296 (both by Pooja Verma). Last seven days (20 to 26 October) in ₹: 14,360; 3,422; 15,020; 6,584; 17,180; 0 (Sunday 25/10: no sale); 17,541 (asserted to equal the ledger rows of those days). Figures for "today" carry a count chip, never a comparison.
**Incoming deliveries (the same 100 sheets as My Inventory):** TSL-2026-0412 Being Packed, DLV-2026-0412, MH 12 PQ 2204, Ramesh Kale +91 90000 31011, from Hadapsar Godown, expected 27/10 (CAL 6, ARC 29, ₹62,000); TSL-2026-0413 Awaiting Confirmation, requested 28/10 (WNT 20, ARC 30, CAL 5, OAK 10, ₹1,04,784). **Value arriving ₹1,66,784 including GST, counting the unconfirmed order** (as Bravo's Incoming Stock counts SAL-2026-3042). No Receive button: neither is in transit. Recent receipts on Bravo's actual delivery dates: 0409 20/10, 0406 13/10, 0404 08/10, 0401 02/10.
**Link rule:** Sales Executive screens link only to retail sales, inventory (My Inventory, Item Details, Low Stock Overview), catalogue, support, profile and notifications (no order numbers as links, no ordering, no suggested quantity or cost); Inventory and Purchasing Executive screens link to orders (not Order Confirmation), inventory, Purchase History and the catalogue (never invoices, payments or retail sales).

## Phase 11 data (Company Administration, Super Admin part 1: Crestline Laminates; model in `tools/author/data.py`, section "Phase 11"; every figure ties to Phases 2 to 10, asserted)

**Scope decision (recommended, change if you disagree):** Crestline's customers are the chain already on screen: **one distributor (Distributor Alpha), 8 dealers, 20 retailers = 29 customers** (27 Active, 2 New: Dealer Kunal and its retailer). No other distributors are invented. Orders of the whole company are seen across three tiers (Primary: Crestline to Alpha, Secondary: Alpha to dealers, Tertiary: dealers to retailers).
**The 17 unnamed retailers are now named** (placeholders; owner, city, customer-since, October purchases from the dealer): Delta (Nashik): Godavari Interiors (Nashik Road, Santosh Pagar, 20/06/2019, ₹1,80,000), Panchavati Furnishings (Rahul Gaikwad, 11/11/2019, ₹1,50,000), Sinnar Wood Works (Sinnar, Dinesh Wagh, 08/02/2021, ₹1,20,000), Deolali Decor (Meena Sonawane, 25/09/2022, ₹90,000); Foxtrot (Thane): Majiwada Interiors (Ajay Chavan, 10/10/2020, ₹1,75,000), Kalyan Furniture House (Sagar Mhatre, 14/04/2021, ₹1,40,000), Dombivli Decor Studio (Nisha Chaudhari, 02/12/2023, ₹1,20,000); Gopal (Kolhapur): Rankala Interiors (Amol Patil, 16/02/2021, ₹1,50,000), Ichalkaranji Modular Works (Sanjay Kamble, 21/07/2021, ₹1,20,000), Shahupuri Furnishings (Vandana Jadhav, 05/05/2024, ₹1,00,000); Harsh (Nagpur): Sitabuldi Interiors (Rohit Meshram, 30/08/2021, ₹1,80,000), Dharampeth Wood Craft (Pranav Deshkar, 12/01/2023, ₹1,25,000); Indira (Satara): Karad Furniture Mart (Vijay Jagtap, 14/12/2022, ₹1,25,000), Koregaon Decor (Smita Mane, 09/06/2023, ₹95,000); Jayant (Solapur): Akkalkot Road Interiors (Mahesh Kothari, 18/05/2023, ₹1,10,000), Pandharpur Furniture Studio (Revati Bhagwat, 27/10/2023, ₹85,000); Kunal (Panaji): Fontainhas Interiors (Savio Fernandes, 14/10/2026, New, ₹1,05,000). Retailers' October purchases from their dealer total **₹28,00,000** (Bravo's three 2,64,000 + 2,10,000 + 1,56,000 = ₹6,30,000, the Phase 5 ledger); each dealer's retail sales are below what it bought from Alpha. Only the retailers' October purchases are defined; September and by-product splits are not (Phase 12 must define them before use).
**Customer codes** (Crestline's, unique, rising with the customer-since date): Alpha CUS-0018 (as on Alpha's Company Profile), Delta 0089, Bravo 0127 (as on Bravo's profile), Foxtrot 0164, Gopal 0188, Harsh 0215, Charlie 0231, Kiran 0268, Indira 0301, Mehta 0309, Jayant 0342, Kunal 0478; the 17 others in between or after (`_CODE`). RTL-0041 is Bravo's own code for Charlie, not Crestline's.
**Customer Approval Queue.** Only dealer requests reach Crestline (retailer requests stop at the dealer and the distributor). **DRQ-2026-0017 Dealer Omkar** (Jalgaon, North Maharashtra, Omkar Deshmukh, submitted 19/10 by Rajesh Menon, reviewed by Kavita Joshi 21/10, ₹4,00,000 credit, 150 sheets a month, 3 of 3 documents; legal name Omkar Laminate Traders, GST 27AAAPD4417H1Z6, Shop 9, Station Road, Jalgaon, Postal Code 425001, +91 90000 41002, Dealer Tier B, 30 days, territory Jalgaon and Dhule) waits for **Vikram Chopra** (assigned; the Super Admin can decide too), 7 days. Decided history: **DRQ-2026-0014 Dealer Kunal** (submitted 14/09, ₹2,50,000 = Kunal's limit, approved 30/09 by Vikram Chopra, customer since 02/10/2026) and **DRQ-2026-0011 Dealer Prasad Traders** (Ratnagiri, Konkan, 28/08, ₹3,00,000, 2 of 3 documents, rejected 09/09). Average days to decision 14 (16 and 12). DRQ-0018 and 0019 are still with Kavita Joshi at Alpha and are not shown; Dhruv Interiors is a draft.
**Perspective rule:** labels written for the customer are re-worded for Crestline: "Awaiting Your Reply" is **Awaiting Customer Reply**, "Sent to Crestline" is **Waiting for Decision**, Incoming Shipments are shipments.
**Users.** Crestline: Anita Deshmukh (Super Admin, 11221), Neha Kulkarni (Operations Manager, 11222), Vikram Chopra (Sales Manager, 11223), **Meera Kapoor (Customer Support Agent, 11224; a company role the portal has no screens for)**, all Active, `first.last@crestlinelaminates.example`. Then Alpha 5, Bravo 4, Charlie 5 as recorded; the other 7 dealers, Kiran Interiors, Mehta Furniture and the 17 other retailers have **2 users each, all Active** (counts only). **70 users: 64 Active, 3 Invited, 3 Inactive; 4 Crestline staff, 66 customer users.** User Details shows Vikram Chopra (added 15/05/2017 by Anita Deshmukh; activity ties to ORD-2026-10447 confirmed 20/10 09:40, ORD-2026-10459 confirmed 23/10 16:10, DRQ-2026-0017, DRQ-2026-0014).
**Warehouses and company stock (sheets).** Plant Warehouse, Vapi, Gujarat (Alpha's orders ship from here; the 12,400 sheets of LM-WNT-001 on the Primary Product Details are Vapi's available stock) and **Regional Warehouse, Taloja, Maharashtra**. On hand at Vapi / Taloja: WNT 12,600 / 1,800; ARC 18,500 / 2,400; CAL 3,000 / 420; OAK 6,500 / 900; SLT 4,500 / 650; TEK 9,000 / 1,300; CHR 5,200 / 700; IVR 7,500 / 1,100; STN 640 / 90; CPR 1,150 / 160; WNG 6,100 / 850; SKY 5,400 / 780. **Reserved at Vapi = lines of the orders awaiting confirmation or confirmed (ORD-2026-10482 and 10459):** WNT 200, ARC 300, CAL 80, OAK 120, SLT 60, TEK 100, IVR 120, SKY 60. Company reorder levels: WNT 4,000; ARC 6,000; CAL 1,500; OAK 2,500; SLT 2,000; TEK 3,000; CHR 2,000; IVR 3,000; STN 1,000; CPR 500; WNG 2,500; SKY 2,000. Available = on hand minus reserved; **LM-STN-009 is the only Low Stock product (730 of 1,000)**, as the Primary catalogue says: 11 In Stock, 1 Low Stock. Product Details (LM-WNT-001): 14,400 on hand, 200 reserved, 14,200 available; 600 sheets ordered in October on 5 orders. **Price by Tier shows who sets each price:** Primary Distributor Tier A ₹1,180 (Crestline), Dealer Tier B ₹1,300 (Distributor Alpha), Retailer Tier C ₹1,455 (Dealer Bravo). Create Product is an unsaved form for **LM-ASH-013 Nordic Ash Woodgrain Laminate** (1.0 mm, ₹1,150 / 1,110 / 1,065, Draft); Product Management still lists 12 products.
**Order Management (October 2026, awaiting confirmation counted, as Alpha counts ORD-2026-10482):** Primary 6 orders ₹33,52,882; Secondary 33 (the 32 recorded sales ₹31,20,000 plus SAL-2026-3042 ₹2,93,820 = ₹34,13,820); Tertiary 54 (53 recorded: Bravo 12, Delta 10, Foxtrot 8, Gopal 7, Harsh 6, Indira 4, Jayant 4, Kunal 2, plus TSL-2026-0413 ₹1,04,784; recorded ₹28,00,000 = ₹29,04,784). **93 orders (no value total across tiers: the tiers' values overlap); 3 awaiting confirmation** (ORD-2026-10482, SAL-2026-3042, TSL-2026-0413). The list shown is the Primary tab (Alpha's six October orders); the other tabs are not drawn. The Primary Order History's status tab counts (2 / 3 / 2) are all-time figures and are not repeated here.
**Order Details (shared by the Super Admin and the Operations Manager) shows ORD-2026-10459** (Confirmed, Unpaid): placed 23/10 11:05 by Kavita Joshi (as on her activity list), confirmed 23/10 16:10 by Vikram Chopra, stock reserved at Vapi 23/10 16:40 by Neha Kulkarni (changed in Phase 12: Alpha's notification "Order Confirmed" said 09:50, before the order was placed; it now says 16:10), packing and dispatch planned 26/10, expected 29/10, Western Freight Carriers, reference DA-2026-121; lines TEK 100, IVR 120, SKY 60 with the taxable ₹2,81,356 allocated to the lines (no price column; ₹1,14,282, ₹1,08,598, ₹58,476), Central GST and State GST ₹25,322 each, freight ₹4,500, total ₹3,36,500; no invoice yet. Credit check (Super Admin only): limit ₹40,00,000, outstanding ₹14,86,320, after this order ₹21,77,180 (Order Builder's rule: invoices only). The Operations Manager sees Download Packing List, Plan Dispatch and Mark as Packed; the Super Admin sees Download Order Copy and Cancel Order.
**Company Dashboard (26/10/2026):** orders this month 6 (1 awaiting), order value ₹33.53 lakh (+38.0%), customers 29 (2 new), 1 shipment in transit (DSP-2026-5523, arriving 27/10), **3 open support tickets** (TKT-2026-0731 High In Progress, 0724 Medium Awaiting Customer Reply, 0702 Low Open; agent Meera Kapoor, all from Distributor Alpha), 2 overdue invoices ₹3,18,400 (INV-2026-02986 37 days, 03021 30 days). Sales to dealers by region: West Maharashtra ₹15,59,000; North Maharashtra ₹5,92,000; Konkan ₹4,76,000; Vidarbha ₹3,38,000; Goa ₹1,55,000.

## Phase 12 data (Company Super Admin part 2; model in `tools/author/data.py`, section "Phase 12"; asserted against Phases 2 to 11; placeholders marked)

**Shipments from Crestline to Distributor Alpha** (dispatch numbers share the one running series with Alpha's dispatches to dealers; each new number sits between two of Alpha's dispatches of the right date, 5521 is the number earlier phases fixed): ORD-2026-10459 being packed (280 sheets, planned 26/10, expected 29/10, no dispatch number yet); DSP-2026-5523 ORD-10447 in transit (360, 24/10 to 27/10); **DSP-2026-5501** ORD-10431 (520, 18/10 to 20/10); **5476** ORD-10398 (430, 11/10 to 13/10); **5456** ORD-10372 (400, 04/10 to 06/10); **5427** ORD-10341 (470, 27/09 to 29/09); **5402** ORD-10316 (330, 20/09 to 22/09); **5377** ORD-10290 (500, 13/09 to 15/09). All ship from Plant Warehouse, Vapi; transporters Western Freight Carriers (as on ORD-10447) and **Konkan Roadlines** (ORD-10398 and 10341, placeholder); every delivery arrives on its expected date. The list covers shipments since 10/09/2026 (8; 1 being packed, 1 in transit, 6 delivered); October dispatches 4, 1,710 sheets.
**Company stock totals:** 91,240 sheets on hand (Vapi 80,090, Taloja 11,150), 1,040 reserved (orders 10482 and 10459), 90,200 available; by finish Woodgrain 34.7%, Matte 32.3%, Gloss 13.2%, Texture 8.9%, Suede 5.6%, High Gloss 3.7%, Metallic 1.4%.
**The four sales tiers (October, GST included, compared with September):** orders by distributors ₹33,52,882 (+38.0%); sales to dealers ₹31,20,000 (+11.8%); **sales to retailers ₹28,00,000** (+10.2% on ₹25,40,000), 1,644 sheets, 53 orders recorded; **sales to customers ₹34,72,557** (+10.0% on ₹31,56,000), 1,728 sheets. Retailers' September purchases (Bravo's three are the Phase 5 ledger; the rest are placeholders that add up to each dealer's September retail sales): Bravo 6,00,000; Delta 4,80,000; Foxtrot 4,00,000; Gopal 3,40,000; Harsh 3,20,000; Indira 1,95,000; Jayant 2,05,000; Kunal none. Network monthly May to October, to retailers: 21,30,000; 23,40,000; 20,10,000; 24,50,000; 25,40,000; 28,00,000; to customers (retail, includes Charlie's ledger): 26,41,000; 29,01,500; 24,92,500; 30,38,000; 31,56,000; 34,72,557. **Retail sales by store = purchases x 1.24 to the nearest ₹500** (Charlie's ratio; Charlie itself is the ledger ₹3,27,557, September ₹3,05,000). Sheets by product in the two lower tiers apply Bravo's mix (to retailers) and Charlie's mix (to customers) to the network totals (`NET_TSOLD`, `NET_RSOLD`); sell-out may exceed sell-in because stores draw down stock.
**Invoices:** Invoice Management is Crestline's view of the nine invoices in Phase 3 (open 5, overdue 2, paid 129, 134 in all); Invoice Details shows INV-2026-03318 as before, with "Send Payment Reminder" instead of "Raise Support Ticket". Outstanding by age as in Phase 4 (Not Yet Due ₹11,67,920; 1 to 30 days ₹1,32,000; 31 to 60 days ₹1,86,400).
**Schemes: Crestline's own only** (recommended, as proposed): SCH-2026-01, 02, 04, 05, 06 (SCH-2026-03 and 07 to 09 are Alpha's schemes to its dealers and stay on Alpha's and Bravo's screens). Credited this year ₹84,450 (38,250 + 46,200); accruing on active schemes ₹19,926 (₹3,500 earned on SCH-2026-05 + the ₹16,426 rebate on ORD-2026-10482, which is not yet confirmed). Create Scheme is an unsaved form for **SCH-2026-10 Spring Stock Incentive** (₹20 per sheet at 2,000 sheets, 01/03/2027 to 31/05/2027, maximum ₹1,00,000; placeholder).
**Support (Crestline's view):** the six tickets of Alpha (agent Meera Kapoor); open 3, high priority 1, awaiting customer reply 1, resolved this month 1; age in days = 26/10 minus created. Details shows TKT-2026-0731 with the Crestline messages on the right-hand (blue) side.
**Territories = the five regions of Alpha's dealers** (Account Manager Vikram Chopra for all; each dealer's Distributor Manager is Kavita Joshi, her title on Dealer Bravo's profile): targets are the sums of the Phase 4 dealer targets: West Maharashtra ₹15,65,000 (sales ₹15,59,000, 99.6%), North Maharashtra ₹6,00,000 (₹5,92,000, 98.7%), Konkan ₹4,50,000 (₹4,76,000, 105.8%), Vidarbha ₹3,75,000 (₹3,38,000, 90.1%), Goa ₹1,50,000 (₹1,55,000, 103.3%); total ₹31,40,000, 99.4%.
**Audit Activity (last seven days, 15 entries)** reuses events already on screen (orders placed and confirmed, stock reserved, dispatch and invoice of 24/10, payment recorded and confirmed, ticket and return request, dealer request reviewed and opened, reorder level of LM-STN-009 changed from 800 to 1,000 on 20/10 09:15 by Anita Deshmukh, placeholder).
**Portal Settings:** customer tiers as in `CUST_TIERS` (credit periods 45, 30 and 15 days; the 10% and 12% markups of `dp()` and `rp()`), free freight above an order total of ₹4,50,000 and ₹4,500 below (fits all six October orders: 10459 at ₹3,36,500 and 10447 at ₹4,42,930 carry it; 10372 at ₹4,81,200 and above do not; changed from ₹5,00,000 after review), dispatch 2 to 3 days, GST 18% (9% + 9%), invoices issued on dispatch and due after 45 days, eight notification rules. **My Profile and Notifications** for the three Crestline roles: three unread each (bell badge 3).

## Phase 13 data (Company Sales Manager Vikram Chopra and Operations Manager Neha Kulkarni; model in `tools/author/data.py`, section "Phase 13"; asserted; placeholders marked)

**Retailer targets (October) for the 17 other retailers (placeholders):** Godavari 1,75,000; Panchavati 1,60,000; Sinnar 1,10,000; Deolali 1,00,000; Majiwada 1,70,000; Kalyan 1,40,000; Dombivli 1,15,000; Rankala 1,45,000; Ichalkaranji 1,25,000; Shahupuri 95,000; Sitabuldi 1,90,000; Dharampeth 1,30,000; Karad 1,20,000; Koregaon 1,00,000; Akkalkot Road 1,15,000; Pandharpur 90,000; Fontainhas 1,00,000, plus the Phase 7 targets (Charlie 2,50,000; Kiran 2,20,000; Mehta 1,70,000): **total ₹28,20,000**, sales ₹28,00,000 (99.3%); 10 retailers Above Target, 5 Near, 5 Below (same 100% / 95% rule as dealers). Dealer targets and statuses as Phase 4 (4 of 8 above; total ₹31,40,000, 99.4%).
**Quarters of Financial Year 2026–27 (sales to dealers; placeholders for the targets):** Q2 July to September target ₹82,00,000, sales ₹80,90,000 (22,40,000 + 30,60,000 + 27,90,000), Completed; Q3 October to December target ₹96,00,000, sales so far ₹31,20,000, In Progress; Q4 January to March 2027 target ₹1,00,00,000, Upcoming. Q1 is not shown.
**Regional analysis:** by state Maharashtra ₹29,65,000 (September ₹27,90,000, +6.3%) and Goa ₹1,55,000 (new); by city the eight dealer cities. **Product movement rule:** Fast Mover = 250 sheets or more sold to dealers in the month (Arctic White Matte 405, Sky Blue Gloss 285, Walnut Woodgrain 280); Slow Mover = under 120 (Slate Grey Suede 110, Charcoal Black Gloss 100, Brushed Copper 35, Carrara Stone Finish none): 4 slow movers.
**Customer Sales History shows Dealer Bravo:** purchases ₹6,84,000 (September ₹6,10,000, +12.1%), 6 orders, 480 sheets, owes ₹2,60,000; money by product is allocated like `SOLD_VALUE` (sheets x dealer price, rounding plug).
**Orders in progress (Sales Order Overview): 16 orders, ₹28,93,786, 2,155 sheets:** Primary 3 (ORD-2026-10482 awaiting, 10459 confirmed, 10447 in transit), Secondary 4 (SAL-2026-3042 awaiting, 3041 being packed, 3040 and 3039 in transit), Tertiary 9 (TSL-2026-0413 awaiting, 0412 being packed, 0411 in transit, and six placeholder orders of other dealers' retailers, numbered `TSL-2026-<dealer code>-nnnn`: DLT-0108 Sinnar ₹44,000 and GPL-0079 Rankala ₹52,000 and HRS-0066 Sitabuldi ₹61,000 being packed; DLT-0107 Godavari ₹58,000, FXT-0091 Kalyan ₹46,000 and KNL-0002 Fontainhas ₹35,000 in transit). **3 awaiting confirmation, 5 being packed, 7 in transit** (no value or sheet total: the tiers' values overlap); the six placeholder orders are part of October's 53 recorded retailer orders. The Sales Manager confirms only the Primary order (credit after ₹15,63,928, rebate ₹16,426).
**Promotional Campaigns (marketing, not schemes; numbers PRM-2026-02 to 06; all placeholders):** 05 Festive Showroom Display Kits (retailers, 01/10 to 30/11, 20 reached, 7 orders influenced, ₹1,45,000 of ₹2,40,000), 04 Marble Finish Launch Samples (dealers, 01/09 to 31/12, 8 reached, 5 orders, ₹1,12,000 of ₹1,80,000), both Running; 06 Winter Bonus Announcement (01/12/2026 to 31/01/2027, ₹1,50,000, Planned; matches SCH-2026-06); 03 Monsoon Dealer Roadshow (₹1,86,000 of ₹2,00,000, 11 orders) and 02 Summer Sample Folder Mailer (₹1,18,000 of ₹1,20,000, 9 orders, 28 reached), Completed. Budget ₹8,90,000.
**Operations.** Promised and actual dispatch dates: all on time except **ORD-2026-10398** (promised 10/10, dispatched 11/10, reason "Batch Quality Check" is a placeholder; support ticket TKT-2026-0688, Resolved). October dispatches **3 of 4 on time = 75.0%** (September 3 of 3); every delivered order took 5 days from order to delivery; no order is delayed now; ORD-2026-10459 is due for packing and dispatch today (26/10, packing "Due Today"). **Order Processing Queue** holds only ORD-2026-10459 (stock reserved 23/10 16:40, confirmed 23/10 16:10). **Dispatch Details shows DSP-2026-5523** (ORD-2026-10447, 360 sheets, 2,196 kg at 6.1 kg a sheet; vehicle MH 04 KP 7712, driver Ramesh Pawar +91 90000 12345; confirmed 20/10 09:40, packed 23/10 17:05, dispatched 24/10 06:30, expected 27/10).
**Stock movements of Crestline in October (70 movements; placeholders except the four dispatches):** production receipts at Vapi in three batches (PRC-2026-0187 on 02/10, 0194 on 12/10, 0203 on 22/10; 40% / 30% / 30%) of 8,000 sheets in all (WNT 1,200; ARC 1,500; CAL 400; OAK 700; SLT 450; TEK 900; CHR 600; IVR 800; CPR 150; WNG 700; SKY 600; none for STN, which is why it is low); dispatches 1,710 sheets (the lines of ORD-10372, 10398, 10431 and 10447); transfers Vapi to Taloja STR-2026-0041 (08/10) and STR-2026-0044 (20/10), 2,100 sheets. Opening stock 84,950 + 8,000 − 1,710 = 91,240 on hand (asserted per product).
**Return Requests and Delivery Issues (Crestline's view of Alpha's returns):** 7 requests, 3 open (40 sheets), credit issued ₹42,340 on 3; October return requests 5, 65 sheets of 1,710 dispatched = 3.8%; October returns by reason (Operational Reports): Damaged in Transit 2 (27 sheets), Wrong Product Delivered 1 (20), Surface Defect 2 (18) = 65; all seven requests: Damaged in Transit 3 (41 sheets), Surface Defect 2 (18), Wrong Product Delivered 1 (20), Shade Mismatch 1 (6) = 85. Delivery Issues lists 5 (damaged x3, wrong product, quantity shortfall DIS-2026-0011 ₹16,992 on ORD-2026-10171), 3 open, 2 resolved with credit. **Stock count 19/10/2026 (placeholder):** variance 280 sheets at Vapi (99.7%) and 80 at Taloja (99.3%), accuracy 99.6% overall.
