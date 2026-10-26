/*
 * Screen registry: the single list of every screen in the prototype.
 * The directories, the review bar, the application menus and docs/SCREEN-INVENTORY.md (tools/inventory.mjs) all
 * read it. A classic script (no imports, no fetch) so pages open straight from disk.
 *
 * Row: [code, name, roles, group, kind, description, parent]
 *   code    unique within the portal; the screen ID is PORTALCODE-code (for example PRI-ORD-02)
 *   roles   space-separated role codes that see the screen; the first is the default when the file is opened alone
 *   group   menu section in the sidebar; a string, or { ROLE: 'Section' } when roles group it differently
 *   kind    'm' appears in the sidebar menu; 'd' is reached from another screen (details, create, confirmation)
 *   parent  code of the screen it is opened from (breadcrumbs), a string or { ROLE: 'code' }
 * A dashboard is named 'Dashboard' and belongs to exactly one role; its file is <role>-dashboard.html.
 */
(function () {
  var PORTALS = [
    { id: 'company', code: 'CMP', label: 'Company Administration', card: 'Company Administration', directory: 'Company Administration', org: 'Crestline Laminates', portalName: 'Company Administration',
      roles: [['ADM', 'Super Admin', 'Anita Deshmukh'], ['SAL', 'Sales Manager', 'Vikram Chopra'], ['OPS', 'Operations Manager', 'Neha Kulkarni']] },
    { id: 'primary', code: 'PRI', label: 'Primary Customer', card: 'Primary Distributor', directory: 'Primary Distributor', org: 'Distributor Alpha', portalName: 'Primary Customer Portal',
      roles: [['OWN', 'Owner', 'Rajesh Menon'], ['MGR', 'Sales and Operations Manager', 'Kavita Joshi'], ['ACC', 'Accountant', 'Suresh Iyer']] },
    { id: 'secondary', code: 'SEC', label: 'Secondary Customer', card: 'Secondary Dealer', directory: 'Secondary Dealer', org: 'Dealer Bravo', portalName: 'Secondary Customer Portal',
      roles: [['OWN', 'Owner', 'Sunita Rao'], ['MGR', 'Sales and Inventory Manager', 'Arjun Nair']] },
    { id: 'tertiary', code: 'TER', label: 'Tertiary Customer', card: 'Tertiary Retailer', directory: 'Tertiary Retailer', org: 'Retailer Charlie', portalName: 'Tertiary Customer Portal',
      roles: [['OWN', 'Retailer Owner', 'Imran Sheikh'], ['SLS', 'Sales Executive', 'Pooja Verma'], ['PUR', 'Inventory and Purchasing Executive', 'Faisal Khan']] },
    { id: 'authentication', code: 'AUT', label: 'Shared Authentication', card: 'Shared Sign-In Screens', directory: 'Shared Sign-In Screens', org: '', portalName: '',
      roles: [['ALL', 'All Users', '']] }
  ];

  var S = {};

  S.company = [
    ['ADM-01', 'Dashboard', 'ADM', 'Overview', 'm', 'Orders, customers, sales, dispatch and open support tickets across the whole company'],
    ['CUS-01', 'Customer Directory', 'ADM', 'Customers', 'm', 'Every distributor, dealer and retailer with status, region and parent customer'],
    ['CUS-02', 'Customer Details', 'ADM', 'Customers', 'd', 'One customer: profile, contacts, credit terms, hierarchy, recent orders', 'CUS-01'],
    ['CUS-03', 'Customer Approval Queue', 'ADM', 'Customers', 'm', 'New customer registrations waiting for review, with documents and decision buttons'],
    ['CUS-04', 'Customer Hierarchy Explorer', 'ADM', 'Customers', 'm', 'Expandable tree from company to distributors, dealers and retailers'],
    ['USR-01', 'User Directory', 'ADM', 'Users', 'm', 'All users across the company and customers with role, organisation and status'],
    ['USR-02', 'User Details', 'ADM', 'Users', 'd', 'One user: profile, role, organisation, access and recent activity', 'USR-01'],
    ['PRD-01', 'Product Management', 'ADM', 'Products', 'm', 'Laminate range with SKU, finish, thickness, price and availability'],
    ['PRD-02', 'Product Details', 'ADM', 'Products', 'd', 'One product: images, specifications, price tiers and stock by warehouse', 'PRD-01'],
    ['PRD-03', 'Create Product', 'ADM', 'Products', 'd', 'Form to add a laminate: specifications, pricing, images and availability', 'PRD-01'],
    ['PRD-04', 'Edit Product', 'ADM', 'Products', 'd', 'Form to change an existing product’s specifications, pricing and availability', 'PRD-02'],
    ['ORD-01', 'Order Management', 'ADM', { ADM: 'Orders and Dispatch' }, 'm', 'All orders from every customer tier with status, value and delivery date'],
    ['ORD-02', 'Order Details', 'ADM OPS', { ADM: 'Orders and Dispatch', OPS: 'Orders' }, 'd', 'One order: items, customer, status timeline, invoices and dispatch', { ADM: 'ORD-01', OPS: 'OPS-02' }],
    ['DSP-01', 'Dispatch Management', 'ADM OPS', { ADM: 'Orders and Dispatch', OPS: 'Dispatch and Delivery' }, 'm', 'Shipments by warehouse and transporter with status and expected delivery'],
    ['INV-01', 'Inventory Overview', 'ADM OPS', { ADM: 'Orders and Dispatch', OPS: 'Stock and Returns' }, 'm', 'Stock by product and warehouse with reserved, available and low-stock markers'],
    ['ANL-01', 'Sales Analytics', 'ADM', 'Sales Analytics', 'm', 'Sales trends by region, product and customer tier with period comparison'],
    ['RPT-01', 'Primary Sales Report', 'ADM', 'Sales Analytics', 'm', 'Sales from the company to primary distributors, by distributor and product'],
    ['RPT-02', 'Secondary Sales Report', 'ADM', 'Sales Analytics', 'm', 'Sales from primary distributors to secondary dealers, by dealer and product'],
    ['RPT-03', 'Tertiary Sales Report', 'ADM', 'Sales Analytics', 'm', 'Sales from secondary dealers to tertiary retailers, by retailer and product'],
    ['RPT-04', 'Retail Sales Report', 'ADM', 'Sales Analytics', 'm', 'Sales from retailers to end customers, by store and product'],
    ['BIL-01', 'Invoice Management', 'ADM', 'Finance and Schemes', 'm', 'Invoices issued to customers with amount, due date and payment status'],
    ['BIL-02', 'Invoice Details', 'ADM', 'Finance and Schemes', 'd', 'One invoice: line items, taxes, payments received and balance due', 'BIL-01'],
    ['SCH-01', 'Scheme Management', 'ADM', 'Finance and Schemes', 'm', 'Discount, rebate and incentive schemes with validity and participation'],
    ['SCH-02', 'Scheme Details', 'ADM', 'Finance and Schemes', 'd', 'One scheme: rules, eligible products and customers, and results so far', 'SCH-01'],
    ['SCH-03', 'Create Scheme', 'ADM', 'Finance and Schemes', 'd', 'Form to define a scheme: type, validity, eligible products and customers', 'SCH-01'],
    ['SUP-01', 'Support Ticket Management', 'ADM OPS', { ADM: 'Support', OPS: 'Reports and Support' }, 'm', 'All support tickets from customers with priority, owner and age'],
    ['SUP-02', 'Support Ticket Details', 'ADM OPS', { ADM: 'Support', OPS: 'Reports and Support' }, 'd', 'One ticket: conversation, linked order or invoice, assignment and status', 'SUP-01'],
    ['TER-01', 'Territory Management', 'ADM', 'Administration', 'm', 'Sales territories with assigned customers and managers'],
    ['AUD-01', 'Audit Activity', 'ADM', 'Administration', 'm', 'Chronological record of who changed what, with filters by user and area'],
    ['SET-01', 'Portal Settings', 'ADM', 'Administration', 'm', 'Customer tiers, order rules, tax settings and notification rules'],
    ['PRO-02', 'My Profile', 'ADM SAL OPS', 'Account', 'd', 'Your name, contact details, password and notification preferences'],
    ['NTF-01', 'Notifications', 'ADM SAL OPS', 'Account', 'd', 'Alerts and updates for the signed-in user, grouped by day'],

    ['SAL-01', 'Dashboard', 'SAL', 'Overview', 'm', 'Sales against target, top regions and products, and customers needing attention'],
    ['SAL-02', 'Distributor Performance', 'SAL', 'Performance', 'm', 'Primary distributors ranked by sales, growth and target achievement'],
    ['SAL-03', 'Dealer Performance', 'SAL', 'Performance', 'm', 'Secondary dealers ranked by sales, growth and target achievement'],
    ['SAL-04', 'Retailer Performance', 'SAL', 'Performance', 'm', 'Tertiary retailers ranked by sales, growth and target achievement'],
    ['SAL-05', 'Sales Targets', 'SAL', 'Performance', 'm', 'Targets and achievement by territory, customer and quarter'],
    ['SAL-06', 'Regional Sales Analysis', 'SAL', 'Analysis', 'm', 'Sales by state and city with comparison to the previous period'],
    ['SAL-07', 'Product Sales Analysis', 'SAL', 'Analysis', 'm', 'Sales by laminate, finish and thickness, with fast and slow movers'],
    ['SAL-08', 'Customer Sales History', 'SAL', 'Analysis', 'm', 'Purchase history of one customer by month, product and order'],
    ['SAL-09', 'Sales Order Overview', 'SAL', 'Orders and Campaigns', 'm', 'Orders in progress across all customers with status and value'],
    ['SAL-10', 'Promotional Campaigns', 'SAL', 'Orders and Campaigns', 'm', 'Running and planned promotions with reach, orders and spend'],

    ['OPS-01', 'Dashboard', 'OPS', 'Overview', 'm', 'Orders waiting to be processed, dispatches due today, delays and open returns'],
    ['OPS-02', 'Order Processing Queue', 'OPS', 'Orders', 'm', 'Confirmed orders waiting for stock check, packing and dispatch planning'],
    ['OPS-03', 'Delayed Orders', 'OPS', 'Orders', 'm', 'Orders past their promised date with the reason and the next action'],
    ['OPS-04', 'Dispatch Details', 'OPS', 'Dispatch and Delivery', 'd', 'One shipment: items, vehicle, transporter, route and delivery status', 'DSP-01'],
    ['OPS-05', 'Stock Movement History', 'OPS', 'Stock and Returns', 'm', 'Receipts, issues and transfers by product and warehouse'],
    ['OPS-06', 'Return Requests', 'OPS', 'Stock and Returns', 'm', 'Return requests from customers with reason, photos and decision'],
    ['OPS-07', 'Delivery Issues', 'OPS', 'Dispatch and Delivery', 'm', 'Damaged, short or wrong deliveries reported by customers'],
    ['OPS-08', 'Operational Reports', 'OPS', 'Reports and Support', 'm', 'Dispatch timeliness, order cycle time, returns and stock accuracy']
  ];

  S.primary = [
    ['OWN-01', 'Dashboard', 'OWN', 'Overview', 'm', 'Purchases, dealer sales, stock position, outstanding balance and active schemes'],
    ['MGR-01', 'Dashboard', 'MGR', 'Overview', 'm', 'Dealer order activity, low stock, pending dealer requests and dispatches in progress'],
    ['ACC-01', 'Dashboard', 'ACC', 'Overview', 'm', 'Outstanding balance, overdue invoices, payments this month and open disputes'],
    ['CAT-01', 'Product Catalogue', 'OWN MGR', 'Products', 'm', 'Laminates with image, SKU, finish, thickness, price and availability'],
    ['CAT-02', 'Product Details', 'OWN MGR', 'Products', 'd', 'One product: images, specifications, price tiers and stock', 'CAT-01'],
    ['ORD-03', 'Place Order', 'OWN MGR', 'Orders', 'm', 'Pick products and quantities to start a new order to the company'],
    ['ORD-04', 'Order Builder', 'OWN MGR', 'Orders', 'd', 'Order lines with delivery address, requested date, schemes applied and totals', 'ORD-03'],
    ['ORD-05', 'Order Confirmation', 'OWN MGR', 'Orders', 'd', 'Confirmation of the submitted order with its number and expected delivery', 'ORD-04'],
    ['ORD-01', 'Order History', 'OWN MGR', 'Orders', 'm', 'Past and current orders with status, value and delivery date'],
    ['ORD-02', 'Order Details', 'OWN MGR', 'Orders', 'd', 'One order: items, status timeline, invoice and delivery', 'ORD-01'],
    ['INV-01', 'Inventory Overview', 'OWN MGR', 'Inventory and Dispatch', 'm', 'Stock held by product with sheets available, reserved and on order'],
    ['INV-02', 'Inventory Item Details', 'OWN MGR', 'Inventory and Dispatch', 'd', 'One product’s stock by location, movement and reorder level', 'INV-01'],
    ['INV-03', 'Low Stock Overview', 'MGR', 'Inventory and Dispatch', 'm', 'Products below their reorder level with suggested order quantity'],
    ['INV-04', 'Stock Movement History', 'MGR', 'Inventory and Dispatch', 'm', 'Receipts, sales to dealers and adjustments by product and date'],
    ['DSP-01', 'Dispatch Overview', 'MGR', 'Inventory and Dispatch', 'm', 'Incoming shipments from the company and outgoing deliveries to dealers'],
    ['DLR-01', 'Dealer Network', 'OWN MGR', 'Dealers', 'm', 'Secondary dealers with region, status, sales and outstanding balance'],
    ['DLR-02', 'Dealer Details', 'OWN MGR', 'Dealers', 'd', 'One dealer: profile, contacts, order history, sales and retailers', 'DLR-01'],
    ['DLR-03', 'Add Dealer Request', 'OWN', 'Dealers', 'd', 'Form to request approval for a new secondary dealer', 'DLR-01'],
    ['DLR-04', 'Dealer Order Activity', 'MGR', 'Dealers', 'm', 'Recent orders placed by dealers with value and fulfilment status'],
    ['DLR-05', 'Dealer Performance', 'MGR', 'Dealers', 'm', 'Dealers ranked by sales, growth and target achievement'],
    ['DLR-06', 'Pending Dealer Requests', 'MGR', 'Dealers', 'm', 'New dealer requests waiting for a decision'],
    ['SAL-01', 'Secondary Sales Overview', 'OWN', 'Secondary Sales', 'm', 'Sales to dealers by month, product and dealer'],
    ['SAL-02', 'Secondary Sales Entry', 'OWN MGR', 'Secondary Sales', 'm', 'Form to record a sale to a dealer with products and quantities'],
    ['SAL-03', 'Secondary Sales History', 'OWN MGR', 'Secondary Sales', 'm', 'Recorded sales to dealers with date, dealer and value'],
    ['BIL-01', 'Invoices Overview', 'OWN ACC', { OWN: 'Invoices and Payments', ACC: 'Invoices' }, 'm', 'Invoices from the company with amount, due date and payment status'],
    ['BIL-02', 'Invoice Details', 'OWN ACC', { OWN: 'Invoices and Payments', ACC: 'Invoices' }, 'd', 'One invoice: line items, taxes, payments received and balance due', 'BIL-01'],
    ['BIL-03', 'Payments Overview', 'OWN ACC', { OWN: 'Invoices and Payments', ACC: 'Payments' }, 'm', 'Payments made to the company with date, mode and invoices covered'],
    ['BIL-04', 'Payment Details', 'OWN ACC', { OWN: 'Invoices and Payments', ACC: 'Payments' }, 'd', 'One payment: mode, reference, date and the invoices it settled', 'BIL-03'],
    ['BIL-05', 'Purchase History', 'ACC', 'Purchases', 'm', 'Purchases from the company by month, product and invoice'],
    ['BIL-06', 'Outstanding Balances', 'ACC', 'Payments', 'm', 'Amount owed to the company by age, with the invoices behind it'],
    ['BIL-07', 'Overdue Invoices', 'ACC', 'Invoices', 'm', 'Invoices past their due date with days overdue and amount'],
    ['BIL-08', 'Record Payment', 'ACC', 'Payments', 'm', 'Form to record a payment against one or more invoices'],
    ['BIL-09', 'Invoice Disputes', 'ACC', 'Invoices', 'm', 'Invoices under dispute with reason, status and company response'],
    ['BIL-10', 'Invoice Dispute Details', 'ACC', 'Invoices', 'd', 'One dispute: disputed lines, evidence, conversation and resolution', 'BIL-09'],
    ['RPT-01', 'Sales Reports', 'OWN MGR', 'Reports', 'm', 'Sales to dealers by period, product and region, ready to export'],
    ['RPT-02', 'Inventory Reports', 'OWN MGR', 'Reports', 'm', 'Stock levels, ageing and turnover by product'],
    ['RPT-03', 'Invoice Ageing Report', 'ACC', 'Reports', 'm', 'Unpaid invoices grouped by how long they have been outstanding'],
    ['RPT-04', 'Purchase Summary Report', 'ACC', 'Reports', 'm', 'Purchases from the company by month, product and tax'],
    ['RPT-05', 'Financial Reports', 'ACC', 'Reports', 'm', 'Payments, credit notes and balances for the financial year'],
    ['SCH-01', 'Schemes and Incentives', 'OWN', 'Schemes', 'm', 'Active schemes with your progress towards each incentive'],
    ['SCH-02', 'Scheme Details', 'OWN', 'Schemes', 'd', 'One scheme: rules, eligible products, validity and your progress', 'SCH-01'],
    ['RET-01', 'Return Requests', 'OWN MGR', 'Returns', 'm', 'Return requests raised with reason and status'],
    ['RET-02', 'Create Return Request', 'OWN MGR', 'Returns', 'd', 'Form to return damaged or wrong sheets with photos and quantities', 'RET-01'],
    ['SUP-01', 'Support Ticket List', 'OWN', 'Support', 'm', 'Support tickets raised with the company, with status and last reply'],
    ['SUP-02', 'Create Support Ticket', 'OWN', 'Support', 'd', 'Form to raise a support request about an order, invoice or product', 'SUP-01'],
    ['SUP-03', 'Support Ticket Details', 'OWN', 'Support', 'd', 'One ticket: conversation, attachments and status', 'SUP-01'],
    ['PRO-01', 'Company Profile', 'OWN', 'Account', 'm', 'Company details, addresses, tax registration, contacts and credit terms'],
    ['USR-01', 'User Management', 'OWN', 'Account', 'm', 'Users in your organisation with role and status'],
    ['USR-02', 'Create User', 'OWN', 'Account', 'd', 'Form to invite a user and assign a role', 'USR-01'],
    ['USR-03', 'User Details', 'OWN', 'Account', 'd', 'One user: profile, role, access and recent activity', 'USR-01'],
    ['PRO-02', 'My Profile', 'OWN MGR ACC', 'Account', 'd', 'Your name, contact details, password and notification preferences'],
    ['NTF-01', 'Notifications', 'OWN MGR ACC', 'Account', 'd', 'Alerts and updates for the signed-in user, grouped by day']
  ];

  S.secondary = [
    ['OWN-01', 'Dashboard', 'OWN', 'Overview', 'm', 'Purchases, retailer sales, stock position, outstanding balance and active schemes'],
    ['MGR-01', 'Dashboard', 'MGR', 'Overview', 'm', 'Incoming stock, low stock, reorder suggestions and retailer order activity'],
    ['CAT-01', 'Product Catalogue', 'OWN MGR', 'Products', 'm', 'Laminates with image, SKU, finish, thickness, price and availability'],
    ['CAT-02', 'Product Details', 'OWN MGR', 'Products', 'd', 'One product: images, specifications, price tiers and stock', 'CAT-01'],
    ['ORD-03', 'Place Order', 'OWN MGR', 'Orders', 'm', 'Pick products and quantities to start a new order to your distributor'],
    ['ORD-04', 'Order Builder', 'OWN MGR', 'Orders', 'd', 'Order lines with delivery address, requested date, schemes applied and totals', 'ORD-03'],
    ['ORD-05', 'Order Confirmation', 'OWN MGR', 'Orders', 'd', 'Confirmation of the submitted order with its number and expected delivery', 'ORD-04'],
    ['ORD-01', 'Order History', 'OWN MGR', 'Orders', 'm', 'Past and current orders with status, value and delivery date'],
    ['ORD-02', 'Order Details', 'OWN MGR', 'Orders', 'd', 'One order: items, status timeline, invoice and delivery', 'ORD-01'],
    ['INV-01', 'Inventory Overview', 'OWN MGR', 'Inventory and Dispatch', 'm', 'Stock held by product with sheets available, reserved and on order'],
    ['INV-02', 'Inventory Item Details', 'OWN MGR', 'Inventory and Dispatch', 'd', 'One product’s stock by location, movement and reorder level', 'INV-01'],
    ['INV-03', 'Low Stock Overview', 'MGR', 'Inventory and Dispatch', 'm', 'Products below their reorder level with suggested order quantity'],
    ['INV-04', 'Stock Movement History', 'MGR', 'Inventory and Dispatch', 'm', 'Receipts, sales to retailers and adjustments by product and date'],
    ['INV-05', 'Incoming Stock', 'MGR', 'Inventory and Dispatch', 'm', 'Shipments on their way from your distributor with expected arrival'],
    ['INV-06', 'Reorder Recommendations', 'MGR', 'Inventory and Dispatch', 'm', 'Suggested products and quantities to order, based on recent sales'],
    ['DSP-01', 'Dispatch Management', 'MGR', 'Inventory and Dispatch', 'm', 'Deliveries to retailers with vehicle, status and expected arrival'],
    ['RTL-01', 'Retailer Network', 'OWN MGR', 'Retailers', 'm', 'Tertiary retailers with area, status, sales and outstanding balance'],
    ['RTL-02', 'Retailer Details', 'OWN MGR', 'Retailers', 'd', 'One retailer: profile, contacts, order history and sales', 'RTL-01'],
    ['RTL-03', 'Add Retailer Request', 'OWN', 'Retailers', 'd', 'Form to request approval for a new tertiary retailer', 'RTL-01'],
    ['RTL-04', 'Retailer Order Activity', 'MGR', 'Retailers', 'm', 'Recent orders placed by retailers with value and fulfilment status'],
    ['RTL-05', 'Retailer Performance', 'MGR', 'Retailers', 'm', 'Retailers ranked by sales, growth and target achievement'],
    ['RTL-06', 'Pending Retailer Requests', 'MGR', 'Retailers', 'm', 'New retailer requests waiting for a decision'],
    ['TSL-01', 'Tertiary Sales Overview', 'OWN', 'Tertiary Sales', 'm', 'Sales to retailers by month, product and retailer'],
    ['TSL-02', 'Tertiary Sales Entry', 'OWN MGR', 'Tertiary Sales', 'm', 'Form to record a sale to a retailer with products and quantities'],
    ['TSL-03', 'Tertiary Sales History', 'OWN MGR', 'Tertiary Sales', 'm', 'Recorded sales to retailers with date, retailer and value'],
    ['BIL-01', 'Invoices Overview', 'OWN', 'Invoices and Payments', 'm', 'Invoices from your distributor with amount, due date and payment status'],
    ['BIL-02', 'Invoice Details', 'OWN', 'Invoices and Payments', 'd', 'One invoice: line items, taxes, payments made and balance due', 'BIL-01'],
    ['BIL-03', 'Payments Overview', 'OWN', 'Invoices and Payments', 'm', 'Payments made to your distributor with date, mode and invoices covered'],
    ['BIL-04', 'Payment Details', 'OWN', 'Invoices and Payments', 'd', 'One payment: mode, reference, date and the invoices it settled', 'BIL-03'],
    ['SCH-01', 'Schemes and Incentives', 'OWN', 'Schemes', 'm', 'Active schemes with your progress towards each incentive'],
    ['SCH-02', 'Scheme Details', 'OWN', 'Schemes', 'd', 'One scheme: rules, eligible products, validity and your progress', 'SCH-01'],
    ['RPT-01', 'Sales Reports', 'OWN', 'Reports', 'm', 'Sales to retailers by period, product and area, ready to export'],
    ['RPT-02', 'Inventory Reports', 'OWN', 'Reports', 'm', 'Stock levels, ageing and turnover by product'],
    ['RPT-03', 'Operational Reports', 'MGR', 'Reports', 'm', 'Delivery timeliness, order cycle time, stock accuracy and returns'],
    ['RET-01', 'Return Requests', 'OWN MGR', 'Returns', 'm', 'Return requests raised with reason and status'],
    ['RET-02', 'Create Return Request', 'OWN MGR', 'Returns', 'd', 'Form to return damaged or wrong sheets with photos and quantities', 'RET-01'],
    ['SUP-01', 'Support Ticket List', 'OWN', 'Support', 'm', 'Support tickets raised with your distributor, with status and last reply'],
    ['SUP-02', 'Create Support Ticket', 'OWN', 'Support', 'd', 'Form to raise a support request about an order, invoice or product', 'SUP-01'],
    ['SUP-03', 'Support Ticket Details', 'OWN', 'Support', 'd', 'One ticket: conversation, attachments and status', 'SUP-01'],
    ['PRO-01', 'Company Profile', 'OWN', 'Account', 'm', 'Company details, addresses, tax registration, contacts and credit terms'],
    ['USR-01', 'User Management', 'OWN', 'Account', 'm', 'Users in your organisation with role and status'],
    ['USR-02', 'Create User', 'OWN', 'Account', 'd', 'Form to invite a user and assign a role', 'USR-01'],
    ['USR-03', 'User Details', 'OWN', 'Account', 'd', 'One user: profile, role, access and recent activity', 'USR-01'],
    ['PRO-02', 'My Profile', 'OWN MGR', 'Account', 'd', 'Your name, contact details, password and notification preferences'],
    ['NTF-01', 'Notifications', 'OWN MGR', 'Account', 'd', 'Alerts and updates for the signed-in user, grouped by day']
  ];

  S.tertiary = [
    ['OWN-01', 'Dashboard', 'OWN', 'Overview', 'm', 'Retail sales, stock position, purchases, outstanding balance and active offers'],
    ['SLS-01', 'Dashboard', 'SLS', 'Overview', 'm', 'Today’s sales, recent transactions and products running low'],
    ['PUR-01', 'Dashboard', 'PUR', 'Overview', 'm', 'Incoming deliveries, products to reorder and recent purchase orders'],
    ['CAT-01', 'Product Catalogue', 'OWN SLS PUR', 'Products', 'm', 'Laminates with image, SKU, finish, thickness, price and availability'],
    ['CAT-02', 'Product Details', 'OWN SLS PUR', 'Products', 'd', 'One product: images, specifications, price and stock', 'CAT-01'],
    ['ORD-03', 'Place Order', 'OWN PUR', 'Orders', 'm', 'Pick products and quantities to start a new order to your dealer'],
    ['ORD-04', 'Order Builder', 'OWN PUR', 'Orders', 'd', 'Order lines with delivery address, requested date, offers applied and totals', 'ORD-03'],
    ['ORD-05', 'Order Confirmation', 'OWN', 'Orders', 'd', 'Confirmation of the submitted order with its number and expected delivery', 'ORD-04'],
    ['ORD-01', 'Order History', 'OWN PUR', 'Orders', 'm', 'Past and current orders with status, value and delivery date'],
    ['ORD-02', 'Order Details', 'OWN PUR', 'Orders', 'd', 'One order: items, status timeline, invoice and delivery', 'ORD-01'],
    ['INV-01', 'My Inventory', 'OWN SLS PUR', 'Inventory', 'm', 'Stock in your store by product with sheets available and reorder level'],
    ['INV-02', 'Inventory Item Details', 'OWN SLS PUR', 'Inventory', 'd', 'One product’s stock, movement and reorder level', 'INV-01'],
    ['INV-03', 'Stock Movement History', 'OWN PUR', 'Inventory', 'm', 'Receipts, retail sales and adjustments by product and date'],
    ['INV-04', 'Reorder Recommendations', 'OWN PUR', 'Inventory', 'm', 'Suggested products and quantities to order, based on recent sales'],
    ['INV-05', 'Low Stock Overview', 'SLS', 'Inventory', 'm', 'Products below their reorder level'],
    ['INV-06', 'Incoming Deliveries', 'PUR', 'Inventory', 'm', 'Shipments on their way from your dealer with expected arrival'],
    ['RTS-01', 'Record Retail Sale', 'OWN SLS', 'Retail Sales', 'm', 'Form to record a sale to an end customer with products and quantities'],
    ['RTS-02', 'Retail Sales History', 'OWN SLS', 'Retail Sales', 'm', 'Recorded sales with date, customer and value'],
    ['RTS-03', 'Retail Sale Details', 'OWN SLS', 'Retail Sales', 'd', 'One sale: products, quantities, price and payment', 'RTS-02'],
    ['RTS-04', 'Recent Transactions', 'SLS', 'Retail Sales', 'm', 'Latest sales from the store with time, items and value'],
    ['BIL-01', 'Invoices Overview', 'OWN', 'Invoices and Payments', 'm', 'Invoices from your dealer with amount, due date and payment status'],
    ['BIL-02', 'Invoice Details', 'OWN', 'Invoices and Payments', 'd', 'One invoice: line items, taxes, payments made and balance due', 'BIL-01'],
    ['BIL-03', 'Payments Overview', 'OWN', 'Invoices and Payments', 'm', 'Payments made to your dealer with date, mode and invoices covered'],
    ['BIL-05', 'Payment Details', 'OWN', 'Invoices and Payments', 'd', 'One payment: mode, reference, date and the invoices it settled', 'BIL-03'],
    ['BIL-04', 'Purchase History', 'OWN PUR', { OWN: 'Invoices and Payments', PUR: 'Orders' }, 'm', 'Purchases from your dealer by month, product and invoice'],
    ['SCH-01', 'Schemes and Offers', 'OWN', 'Offers', 'm', 'Active offers with your progress towards each reward'],
    ['SCH-02', 'Scheme Details', 'OWN', 'Offers', 'd', 'One offer: rules, eligible products, validity and your progress', 'SCH-01'],
    ['RPT-01', 'Sales Reports', 'OWN', 'Reports', 'm', 'Retail sales by period and product, ready to export'],
    ['RPT-02', 'Inventory Reports', 'OWN', 'Reports', 'm', 'Stock levels, ageing and turnover by product'],
    ['RET-01', 'Return Requests', 'OWN', 'Returns', 'm', 'Return requests raised with reason and status'],
    ['RET-02', 'Create Return Request', 'OWN', 'Returns', 'd', 'Form to return damaged or wrong sheets with photos and quantities', 'RET-01'],
    ['SUP-01', 'Support Ticket List', 'OWN SLS', 'Support', 'm', 'Support tickets raised with your dealer, with status and last reply'],
    ['SUP-02', 'Create Support Ticket', 'OWN SLS', 'Support', 'd', 'Form to raise a support request about an order, invoice or product', 'SUP-01'],
    ['SUP-03', 'Support Ticket Details', 'OWN SLS', 'Support', 'd', 'One ticket: conversation, attachments and status', 'SUP-01'],
    ['PRO-01', 'Store Profile', 'OWN', 'Account', 'm', 'Store details, address, tax registration and contacts'],
    ['USR-01', 'User Management', 'OWN', 'Account', 'm', 'Users in your store with role and status'],
    ['USR-02', 'Create User', 'OWN', 'Account', 'd', 'Form to invite a user and assign a role', 'USR-01'],
    ['USR-03', 'User Details', 'OWN', 'Account', 'd', 'One user: profile, role, access and recent activity', 'USR-01'],
    ['PRO-02', 'My Profile', 'OWN SLS PUR', 'Account', 'd', 'Your name, contact details, password and notification preferences'],
    ['NTF-01', 'Notifications', 'OWN SLS PUR', 'Account', 'd', 'Alerts and updates for the signed-in user, grouped by day']
  ];

  S.authentication = [
    ['01', 'Portal Selection', 'ALL', 'Sign In', 'm', 'Choose which portal to sign in to'],
    ['02', 'Company Login', 'ALL', 'Sign In', 'm', 'Sign-in form for company staff'],
    ['03', 'Primary Customer Login', 'ALL', 'Sign In', 'm', 'Sign-in form for primary distributors'],
    ['04', 'Secondary Customer Login', 'ALL', 'Sign In', 'm', 'Sign-in form for secondary dealers'],
    ['05', 'Tertiary Customer Login', 'ALL', 'Sign In', 'm', 'Sign-in form for tertiary retailers'],
    ['06', 'Forgot Password', 'ALL', 'Password', 'm', 'Ask for a password reset link by email address'],
    ['07', 'Password Reset Confirmation', 'ALL', 'Password', 'm', 'Confirms that the reset link has been sent'],
    ['08', 'Access Denied', 'ALL', 'Errors', 'm', 'Shown when a user opens a screen their role cannot use'],
    ['09', 'Not Found', 'ALL', 'Errors', 'm', 'Shown when the requested page does not exist']
  ];

  // Screens that exist as files today (sign-in screens; Phase 2: eleven Primary Owner screens; Phase 3: the Primary Owner's remaining screens; Phase 4: the Primary Manager and Accountant). Add an ID here when its file is built.
  var BUILT = ['PRI-OWN-01', 'PRI-PRO-01', 'PRI-CAT-01', 'PRI-CAT-02', 'PRI-ORD-03', 'PRI-ORD-04', 'PRI-ORD-05', 'PRI-ORD-01', 'PRI-ORD-02', 'PRI-INV-01', 'PRI-INV-02',
    'PRI-DLR-01', 'PRI-DLR-02', 'PRI-DLR-03', 'PRI-SAL-01', 'PRI-SAL-02', 'PRI-SAL-03',
    'PRI-BIL-01', 'PRI-BIL-02', 'PRI-BIL-03', 'PRI-BIL-04', 'PRI-SCH-01', 'PRI-SCH-02', 'PRI-RPT-01', 'PRI-RPT-02',
    'PRI-MGR-01', 'PRI-INV-03', 'PRI-INV-04', 'PRI-DSP-01', 'PRI-DLR-04', 'PRI-DLR-05', 'PRI-DLR-06',
    'PRI-RET-01', 'PRI-RET-02', 'PRI-SUP-01', 'PRI-SUP-02', 'PRI-SUP-03', 'PRI-USR-01', 'PRI-USR-02', 'PRI-USR-03', 'PRI-PRO-02', 'PRI-NTF-01',
    'AUT-01', 'AUT-02', 'AUT-03', 'AUT-04', 'AUT-05', 'AUT-06', 'AUT-07', 'AUT-08', 'AUT-09'];

  function slug(text) { return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }
  function pick(value, role) { return value && typeof value === 'object' ? value[role] : value; }

  var portals = PORTALS.map(function (p) {
    var roleName = {};
    p.roles.forEach(function (r) { roleName[r[0]] = r[1]; });
    var screens = S[p.id].map(function (row, i) {
      var roles = row[2].split(' ');
      var id = p.code + '-' + row[0];
      return {
        id: id, portal: p.id, code: row[0], name: row[1], roles: roles, group: row[3], kind: row[4], description: row[5],
        parent: row[6] || null, order: i, built: BUILT.indexOf(id) >= 0,
        file: 'screens/' + p.id + '/' + (row[1] === 'Dashboard' ? slug(roleName[roles[0]]) + '-dashboard' : slug(row[1])) + '.html'
      };
    });
    return { id: p.id, code: p.code, label: p.label, card: p.card, directory: p.directory, org: p.org, portalName: p.portalName, roles: p.roles.map(function (r) { return { code: r[0], label: r[1], person: r[2] }; }), screens: screens };
  });

  function P_parent(p, s, role) {
    var code = pick(s.parent, role);
    return code ? p.screens.filter(function (x) { return x.code === code; })[0] : null;
  }
  function portal(id) { return portals.filter(function (p) { return p.id === id; })[0]; }
  function roleLabel(p, role) { return p.roles.filter(function (r) { return r.code === role; })[0].label; }

  window.PORTAL = {
    portals: portals,
    portal: portal,
    roleLabel: roleLabel,
    // Screens a role sees, in menu order.
    forRole: function (p, role) { return p.screens.filter(function (s) { return s.roles.indexOf(role) >= 0; }); },
    // The screen's name as stakeholders say it: "Primary Customer — Owner — Order Details".
    fullName: function (p, s, role) {
      return p.id === 'authentication' ? p.label + ' — ' + s.name : p.label + ' — ' + roleLabel(p, role) + ' — ' + s.name;
    },
    group: function (s, role) { return pick(s.group, role); },
    parent: function (p, s, role) {
      var code = pick(s.parent, role);
      return code ? p.screens.filter(function (x) { return x.code === code; })[0] : null;
    },
    // Link from a page whose root folder is `root` (a URL ending in "/"). The role is added only when it is not the screen's default.
    href: function (root, s, role) { return root + s.file + (role && role !== s.roles[0] && role !== 'ALL' ? '?role=' + role : ''); },
    // Screens from the top of the parent chain down to s (loop-safe).
    chain: function (p, s, role) {
      var out = [s], seen = { };
      seen[s.id] = true;
      for (var up = P_parent(p, s, role); up && !seen[up.id] && out.length < 8; up = P_parent(p, up, role)) { seen[up.id] = true; out.unshift(up); }
      return out;
    },
    // The sidebar item that stands for s: the nearest screen up the chain that appears in the menu.
    menuScreen: function (p, s, role) {
      var c = this.chain(p, s, role);
      for (var i = c.length - 1; i >= 0; i--) if (c[i].kind === 'm') return c[i];
      return s;
    },
    // Finds a screen by its full ID, for example PRI-ORD-02.
    find: function (id) {
      for (var i = 0; i < portals.length; i++) for (var j = 0; j < portals[i].screens.length; j++)
        if (portals[i].screens[j].id === id) return { portal: portals[i], screen: portals[i].screens[j] };
      return null;
    },
    dashboard: function (p, role) {
      return p.screens.filter(function (s) { return s.name === 'Dashboard' && s.roles[0] === role; })[0] || null;
    },
    count: function () { return portals.reduce(function (n, p) { return n + p.screens.length; }, 0); },
    built: function () { return portals.reduce(function (n, p) { return n + p.screens.filter(function (s) { return s.built; }).length; }, 0); }
  };
})();
