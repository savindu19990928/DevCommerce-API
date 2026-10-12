# DevCommerce – Functional Requirements Specification

## 1. System Overview

**DevCommerce** is a general-purpose online e-commerce platform for selling physical products, supporting both normal orders and pre-orders.

The platform must support:

- Guest checkout and registered-customer checkout
- Product catalog, categorization, search, filtering, ratings, reviews, and recommendations
- Normal products and pre-order products
- Product-level estimated arrival times
- Order-level estimated arrival date based on the slowest product in the order
- PayPal Checkout
- Email and SMS receipts
- PDF receipt generation and downloading
- Order tracking and customer notifications
- Warranty tracking
- Customer care live chat and WhatsApp communication
- Customer care phone-call requests
- Role-based operational users
- Django Admin for administrators
- Front-end staff software consuming Django REST Framework API endpoints
- Audit logging for all actions
- Financial, inventory, product, order, customer-care, trending-product, and customer reports

---

# 2. User Roles

## 2.1 Customer User

A registered customer must be able to:

- Create an account
- Log in and log out
- Verify their phone number
- Verify their email address where applicable
- Manage their profile
- Upload/change a profile photo
- Manage addresses
- Manage saved contact information
- Manage notification preferences
- Browse products
- Search products
- Filter and sort products
- Add products to cart
- Add products to wishlist
- Place normal orders
- Place pre-orders
- Complete checkout using PayPal
- View order history
- View individual order history/timeline
- Track orders
- Download receipts
- Re-download receipts
- Request receipt delivery by email
- Request receipt delivery by SMS
- View warranty information for eligible products
- Rate eligible purchased products
- Write reviews where enabled
- Chat with customer care
- Contact customer care through WhatsApp
- Request a phone call
- Manage communication preferences
- Receive personalized recommendations
- Receive sale notifications for recommended products when enabled
- View relevant notifications

## 2.2 Guest Customer

A guest customer must be able to:

- Browse the website
- Search, filter, compare, and view products
- Add products to cart
- Checkout without creating an account
- Provide required contact and delivery information during checkout
- Pay using PayPal
- Receive order confirmation
- Receive receipt by email and/or SMS
- Download the receipt using links received by email/SMS
- Track an order using secure order tracking links
- Track warranty using the secure warranty link provided through email/SMS
- Request customer care assistance
- Request a phone call using a secure order-linked link received by email/SMS

Guest customers must not receive registered-user-only capabilities such as personalized account recommendations or product ratings unless the guest converts to a verified customer account.

## 2.3 Customer Care Assistant

Customer care assistants must work through the front-end operational application using API endpoints.

They must be able to:

- View assigned/permitted customer inquiries
- Search customers
- Search orders
- View order details
- View individual order history
- View shipment/tracking information
- View payment information relevant to support
- View customer communication history
- Communicate with customers
- Use live chat
- Use WhatsApp communication workflows where integrated
- Create urgent attention marks for administrators
- Escalate orders or issues to administrators
- Create support notes
- View relevant customer/order activity
- Process eligible full refunds
- Process partial refunds for specific products/line items within an order
- Record refund reasons
- View refund status
- Request phone calls on behalf of customers where permitted
- Mark support cases as resolved

Customer care assistants must not have unrestricted administrator access.

## 2.4 Order Packing User

Order packing users must work through the front-end operational application using API endpoints.

They must be able to:

- View orders waiting for packing
- View order items and quantities
- View product information required for packing
- Confirm items picked
- Confirm packing
- Enter the serial number of each serial-tracked product
- Validate entered serial numbers
- Flag missing, invalid, duplicate, or damaged serial numbers
- Record packing issues
- Mark an order/package as packed
- Prepare shipment/package information
- Hand the package to the delivery company
- Update package status when handed to the delivery company
- Enter or update courier/tracking information where applicable
- Confirm dispatch handover
- View packing history for an order

## 2.5 Stock Management User

Stock management users must work through the front-end operational application using API endpoints.

They must be able to:

- View stock levels
- View stock by product/variant
- Record stock additions
- Record stock removals
- Record damaged stock
- Record lost stock
- Record stock adjustments
- Manage stock movement records
- View low-stock items
- View out-of-stock items
- View reserved stock
- View stock allocated to orders
- View stock allocated to pre-orders where applicable
- Record serial numbers for applicable products
- Search serial numbers
- Track serial-number status
- Flag damaged/defective units
- View stock history
- Support stock-related reports

## 2.6 Administrator

Administrators must use the **Django Admin Panel**.

Depending on their permission level, administrators must be able to:

- Manage users and permissions
- Manage customers
- Manage staff users
- Manage products
- Manage product variants
- Manage brands
- Manage categories
- Manage product specifications
- Manage product images/media references
- Manage pricing
- Manage discounts and promotions
- Manage inventory-related master data
- Manage orders
- Manage payments/refunds
- Manage delivery/shipping settings
- Manage pre-order settings
- Manage warranties
- Manage notification templates
- Manage notification settings
- Manage recommendation configuration
- Review customer-care escalations
- Manage urgent attention cases
- View audit logs
- Generate reports
- Configure website content/settings
- Manage system configuration

Administrators must be able to control permissions so that different admin users can access only the areas assigned to them.

---

# 3. Authentication and Account Management

## 3.1 Customer Registration

The system must allow customers to:

- Register using required personal/contact details
- Create a password
- Verify email where enabled
- Verify phone number using a verification mechanism
- Log in
- Log out
- Recover forgotten passwords
- Reset passwords
- Change passwords
- Update profile information

## 3.2 Profile

Registered customers must be able to manage:

- Name
- Email
- Phone number
- Profile photo
- Saved addresses
- Default delivery address
- Notification preferences
- Communication preferences
- Other account settings configured by administrators

## 3.3 Phone Verification

The system must track whether a customer's phone number is verified.

Only customers with:

- A registered account
- A verified phone number
- A completed eligible purchase

may submit product ratings/reviews.

---

# 4. Product Catalog

## 4.1 Product Management

Administrators must be able to create and manage:

- Product name
- Product description
- Short description
- Brand
- SKU
- Product images
- Product media where supported
- Price
- Sale price
- Currency
- Product status
- Product availability
- Stock status
- Weight/dimensions where relevant
- Product attributes
- Warranty information
- Estimated arrival time
- Pre-order availability
- Pre-order status
- Serial-number tracking requirement
- Search metadata
- Related products
- Product tags
- Recommendation tags
- Other common e-commerce information

## 4.2 Product Categories

The system must support hierarchical categorization such as:

- Main category
- Subcategory
- Child category

A single product must be able to belong to **multiple categories**.

Administrators must be able to assign and remove multiple categories from the same product.

## 4.3 Brands

The platform must support:

- Brand creation
- Brand editing
- Brand activation/deactivation
- Brand-based filtering
- Brand pages/listings
- Brand association with products

## 4.4 Product Specifications

Administrators must be able to add flexible product specifications without requiring a fixed field for every possible specification.

The specification system must support:

- Specification key
- Specification value

Examples:

- Motor Power → 500W
- Battery Capacity → 48V 15Ah
- Material → Cotton
- Screen Size → 15.6 inches

A product may contain any number of specification key/value pairs.

---

# 5. Product Search, Filtering and Sorting

The system must provide strong catalog discovery similar to major e-commerce platforms.

## 5.1 Search

Customers must be able to search by:

- Product name
- SKU
- Brand
- Category
- Product keywords
- Tags
- Specifications where supported

Search must support relevant ordering of results.

## 5.2 Filters

The product listing must support filters including:

- Brand
- Category
- Multiple categories
- Price range
- Availability
- On-sale status
- Pre-order status
- Rating
- Color
- Size where applicable
- Product attributes
- Other configured product filters

## 5.3 Sorting

Customers must be able to sort products by options such as:

- Relevance
- Popularity
- Trending
- Newest
- Price low to high
- Price high to low
- Highest rating
- Most reviewed
- On sale

---

# 6. Product Variants

The system should support product variants where relevant, including:

- Color
- Size
- Model
- Capacity
- Other configurable variation attributes

Each variant may have:

- SKU
- Price
- Sale price
- Stock
- Images
- Availability
- Serial tracking configuration where applicable
- Other variant-specific details

---

# 7. Product Ratings and Reviews

## 7.1 Ratings

Only customers who:

- Are logged in
- Have a verified phone number
- Have purchased the relevant product

may rate the product.

The maximum rating is **5 stars**.

The system should prevent unauthorized ratings.

## 7.2 Reviews

Where enabled, eligible customers may:

- Write a review
- Edit their review according to configured rules
- View their submitted reviews

Administrators must be able to:

- Moderate reviews
- Hide/remove inappropriate reviews
- Review reported reviews
- Review rating activity

The system should support rating summaries such as:

- Average rating
- Total ratings
- Rating breakdown by stars

---

# 8. Homepage and Discovery

The homepage must support sections such as:

- Most Popular
- Trending
- New Arrivals
- Recommended for You
- On Sale
- Featured Products
- Featured Brands
- Categories
- Promotional content

## 8.1 Personalized Recommendations

The system must provide recommendations only when enough customer behavior/profile data exists to make recommendations useful.

Example:

If a customer purchased or interacted strongly with products tagged with the category **eBike**, the system may recommend other eBike products.

Recommendation inputs may include:

- Previous purchases
- Product categories purchased
- Product categories viewed
- Product tags
- Wishlist activity
- Search activity
- Product interactions
- Other permitted customer behavior

The system must avoid displaying personalized recommendations when insufficient data exists.

## 8.2 Sale Recommendations

Where personalized recommendations are available, the system may show:

- Recommended products currently on sale
- Sale products related to customer interests

Customers must only receive sale notifications for recommended products when they explicitly allow such notifications in their settings.

---

# 9. Wishlist

Registered customers must be able to:

- Add products to wishlist
- Remove products from wishlist
- View wishlist
- Move wishlist products to cart
- Receive relevant notifications where configured

The system should support price-change or sale notifications according to customer settings.

---

# 10. Shopping Cart

Customers must be able to:

- Add products to cart
- Add product variants to cart
- Change quantities
- Remove products
- View subtotal
- View discounts
- View applicable charges
- View estimated arrival information
- View estimated order arrival date
- Proceed to checkout

The system must validate availability before order placement.

---

# 11. Pre-Orders

The platform must support pre-orders as a first-class ordering capability.

Administrators must be able to configure a product as:

- Available for immediate purchase
- Available for pre-order
- Temporarily unavailable
- Out of stock

For pre-order products, the product must display its estimated arrival time.

Examples:

- Within 7 days
- Within 30 days
- Within 60 days

The platform must clearly identify pre-order products during:

- Product display
- Cart
- Checkout
- Order confirmation
- Order details
- Notifications

---

# 12. Estimated Arrival Logic

Every product must have an **estimated arrival time**.

Examples:

- Within 5 days
- Within 14 days
- Within 30 days

For every order:

> **Order Estimated Arrival Date = the latest estimated arrival date among all products in the order.**

Example:

- Product A → arrives within 10 days
- Product B → arrives within 30 days
- Product C → arrives within 15 days

The order's estimated arrival date must use the date associated with **Product B (30 days)** because it is the slowest item.

The system must display the resulting estimated date in:

- Cart
- Checkout
- Order confirmation
- Order details
- Receipt
- Email notification
- SMS notification
- Tracking page

Where an order contains different products with different expected arrival periods, the system may also show item-level expected arrival dates.

---

# 13. Checkout

The platform must support two checkout modes.

## 13.1 Guest Checkout

Guests must be able to complete a purchase without creating an account.

Required information may include:

- Name
- Email
- Phone number
- Delivery address
- Billing details where required
- Payment information through PayPal

After successful checkout, the guest must receive secure links for order-related actions.

## 13.2 Registered Customer Checkout

Logged-in customers must be able to:

- Select saved addresses
- Add a new address
- Review cart
- Apply eligible promotions
- Review delivery information
- Review estimated arrival
- Pay through PayPal
- Place the order

---

# 14. Payments

## 14.1 PayPal

The system must integrate **PayPal Checkout**.

The payment system must support:

- Payment initiation
- Payment confirmation
- Successful payment
- Failed payment
- Cancelled payment
- Payment status tracking
- Payment transaction reference
- Refund processing
- Partial refunds
- Full refunds
- Payment-related order status updates

Order completion must be consistent with the actual payment result.

---

# 15. Orders

The system must create an order after successful checkout/payment according to the configured payment flow.

Order information should include:

- Order number
- Customer or guest identity
- Order items
- Item quantities
- Item prices
- Discounts
- Taxes/charges where applicable
- Delivery information
- Payment status
- Order status
- Estimated arrival date
- Shipment/tracking information
- Warranty information where applicable

## 15.1 Order Statuses

The system should support common order statuses such as:

- Pending
- Payment Processing
- Paid
- Confirmed
- Awaiting Stock
- Pre-order
- Processing
- Picking
- Packing
- Packed
- Ready for Dispatch
- Handed to Delivery Company
- In Transit
- Out for Delivery
- Delivered
- Delivery Failed
- Cancelled
- Refund Requested
- Partially Refunded
- Refunded
- Returned
- Completed

The exact status workflow must be configurable by administrators.

---

# 16. Order History and Order Timeline

Registered customers must be able to view:

- All previous orders
- Active orders
- Individual order details
- Individual order history/timeline

The individual order history must show important events such as:

- Order placed
- Payment received
- Order confirmed
- Packing started
- Packing completed
- Serial number recorded
- Package handed to delivery company
- Tracking updates
- Delivery attempts
- Delivered
- Refund events
- Return events
- Warranty-related events where applicable

Customers must see appropriate readable timestamps and status descriptions.

Administrators must be able to inspect an order's complete history.

---

# 17. Order Tracking

The system must provide order tracking for:

- Registered customers through their account
- Guests through secure links sent by email/SMS

Tracking should display:

- Order status
- Package status
- Tracking number where available
- Delivery company/courier information where available
- Shipment events
- Estimated arrival date
- Item-level information where useful

---

# 18. Guest Secure Order Links

Guest customers must receive secure order-related links through email and SMS.

The links must be associated with the correct order in the backend and securely authorize the intended action.

The system must support at least these **three guest-access links**:

1. **Order Tracking Link**
2. **Receipt Download Link**
3. **Warranty Tracking Link**

A secure phone-call request link may also be included as an additional order-linked action.

Guest links must have appropriate security protections such as:

- Secure random/tokenized access
- Expiration where appropriate
- Order association
- Access control
- Protection against unauthorized access

---

# 19. Receipts

The system must generate a receipt for completed purchases according to the configured payment/order workflow.

## 19.1 Receipt Contents

Receipts should contain:

- Store/business information
- Receipt/order number
- Customer/guest information
- Billing information where applicable
- Delivery information where applicable
- Products
- Quantities
- Unit prices
- Discounts
- Taxes/charges where applicable
- Total
- Payment status
- Payment reference where appropriate
- Order estimated arrival date
- Relevant warranty information where applicable

## 19.2 PDF Receipt

The receipt must be available as a downloadable PDF.

Customers must be able to:

- Download the receipt
- Re-download the receipt
- Request the receipt again

## 19.3 Email Receipt

The platform must be able to send the receipt by email.

The email must contain a secure link to download the PDF receipt.

## 19.4 SMS Receipt

The platform must be able to send an SMS receipt message.

The SMS must contain a secure link to download the PDF receipt.

## 19.5 Registered Customer Receipt Management

A logged-in customer must be able to:

- Download the receipt
- Re-download the receipt
- Resend the receipt by email
- Resend the receipt by SMS

---

# 20. Notifications

The platform must support both **email** and **SMS** notifications.

Notifications should be event-based and configurable.

## 20.1 Order Notifications

Customers should be notified about important events such as:

- Order placed
- Payment successful
- Payment failed where relevant
- Order confirmed
- Processing started
- Packing started/completed where appropriate
- Package dispatched
- Package handed to delivery company
- Tracking updates
- Delivery attempt
- Delivered
- Cancellation
- Refund
- Partial refund
- Return-related status
- Other important order events

## 20.2 Receipt Notifications

Receipts may be sent by:

- Email
- SMS

Both channels must include secure PDF receipt download links.

## 20.3 Sale Notifications

Customers may receive notifications for sale items from their personalized recommendations.

These notifications must only be sent when the customer's settings allow them.

Customers must be able to control notification preferences.

---

# 21. Notification Settings

The customer settings area must allow customers to control notification preferences.

Preferences should include, where supported:

- Order updates by email
- Order updates by SMS
- Receipt by email
- Receipt by SMS
- Promotional emails
- Promotional SMS
- Recommended-product sale notifications
- Other marketing/notification categories

System-critical transactional notifications may be handled separately according to business rules.

---

# 22. Warranty Management

Products may have a warranty period.

Administrators must be able to configure:

- Warranty duration
- Warranty eligibility
- Warranty start rule
- Warranty end rule
- Warranty-related product information

## 22.1 Registered Customers

Logged-in customers must be able to view their warranty information from the website settings/account area.

The system must show:

- Covered product
- Serial number where applicable
- Warranty start date
- Warranty end date
- Remaining warranty period
- Warranty status

## 22.2 Guest Warranty Tracking

Guest customers must be able to track warranty information using the secure **Warranty Tracking Link** received through email or SMS.

The warranty tracking page must be securely associated with the correct order/product.

---

# 23. Serial Number Management

For products requiring serial numbers:

- Packing staff must enter the serial number after packing
- Serial numbers must be associated with the relevant product/order item
- Duplicate serial numbers must be prevented or flagged
- Invalid serial numbers must be prevented or flagged
- Serial numbers must be traceable through stock and order history
- Warranty records should use the relevant serial number where applicable

The system must support serial-number history/status such as:

- In stock
- Reserved
- Packed
- Sold
- Delivered
- Returned
- Damaged
- Warranty-related status

---

# 24. Inventory and Stock Management

The system must support:

- Product stock
- Variant stock
- Reserved stock
- Available stock
- Damaged stock
- Lost stock
- Stock adjustments
- Stock movements
- Serial-number stock tracking
- Low-stock monitoring
- Out-of-stock monitoring

The system must maintain stock-related history.

Inventory changes must be traceable to the user/action that performed them.

---

# 25. Packing and Dispatch Workflow

Order packing users must have a front-end workflow such as:

1. Open order awaiting packing
2. Review order items
3. Confirm item picking
4. Check quantities
5. Enter serial numbers for serial-tracked products
6. Record packing issues if any
7. Confirm package creation
8. Mark order/package as packed
9. Hand package to delivery company
10. Update package/delivery status
11. Add tracking information where applicable

The system must log each significant action.

---

# 26. Delivery Management

The system should support:

- Delivery company/courier information
- Tracking number
- Delivery status
- Shipment/package status
- Delivery events
- Estimated delivery information
- Delivery failure
- Delivery attempts
- Successful delivery
- Return-to-sender where applicable

Where a third-party courier integration is used, tracking information should be synchronized where supported.

---

# 27. Customer Care

## 27.1 Live Chat

The website must provide a live-chat capability for customer support.

Customers must be able to:

- Start a conversation
- Send messages
- Receive responses
- See conversation history during/after the session according to policy

Customer care assistants must be able to handle conversations through the operational front end.

## 27.2 WhatsApp

The system must provide a WhatsApp customer-care contact method.

The implementation may use an appropriate WhatsApp integration or click-to-chat workflow.

Relevant order context should be included where possible.

## 27.3 Phone Call Requests

Customers must be able to request a phone call:

- While logged in
- Through a secure link received in an order-related email/SMS

The phone-call request must be associated with the correct customer/order where applicable.

Customer care staff must be able to manage call requests.

---

# 28. Customer Care Escalation

Customer care assistants must be able to mark cases as:

- Normal
- Urgent attention

Urgent cases must be visible to administrators.

An urgent attention record should include:

- Reason
- Related customer
- Related order where applicable
- Created by
- Date/time
- Current status
- Resolution information

Administrators should be able to review and manage escalations.

---

# 29. Refunds

Customer care assistants may refund eligible orders according to their permissions and configured business rules.

The system must support:

- Full order refund
- Partial refund
- Product/line-item-specific refund
- Refund reason
- Refund amount
- Refund status
- Refund date/time
- Related payment transaction
- User who initiated the refund

For partial refunds, a customer care assistant must be able to refund **only selected products/line items** within an order rather than the entire order.

The system must prevent refunding more than the refundable amount.

Refund actions must be audit logged.

---

# 30. Returns

The platform should support common e-commerce return capabilities, including:

- Return requests
- Return reason
- Return status
- Items being returned
- Return approval/rejection
- Return tracking information where applicable
- Refund linkage
- Return history

Administrators must be able to configure return rules.

---

# 31. Product Recommendations

The system must support recommendation logic based on customer behavior and product metadata.

Possible recommendation signals include:

- Purchased categories
- Viewed categories
- Product tags
- Purchase frequency
- Wishlist activity
- Searches
- Related-product relationships
- Brand interests
- Other permitted engagement signals

The recommendation system must allow category/tag-based logic such as:

> Customer purchased an item tagged `ebike` → recommend products tagged/category-linked to `ebike`.

Recommendations should be personalized only when sufficient data exists.

---

# 32. Trending Products

The platform must support a trending-products feature.

Trending calculations may consider:

- Recent sales
- Sales volume
- Recent views
- Wishlist activity
- Search activity
- Ratings/reviews
- Other configured popularity signals

Administrators must be able to review trending information through reports.

---

# 33. Promotions, Discounts and Sales

The platform must support common e-commerce promotion capabilities, such as:

- Sale pricing
- Discount pricing
- Promotional campaigns
- Coupon/promo codes
- Time-limited offers
- Product-specific promotions
- Category-specific promotions
- Brand-specific promotions where applicable
- Minimum-order promotions where applicable

The final discount must be clearly displayed during checkout.

---

# 34. Product Comparison

The platform should support common e-commerce product comparison functionality where appropriate.

Customers may compare selected products using information such as:

- Price
- Brand
- Ratings
- Specifications
- Availability
- Other comparable attributes

---

# 35. Common E-Commerce Features

DevCommerce should include standard capabilities expected from modern e-commerce platforms, including:

- Responsive website
- Product image galleries
- Product zoom where appropriate
- Breadcrumb navigation
- Search suggestions/autocomplete
- Recently viewed products
- Related products
- Frequently bought together
- Wishlist
- Product comparison
- Clear stock status
- Clear sale pricing
- Clear pre-order labels
- Secure checkout
- Order confirmation
- Customer account area
- Order history
- Address book
- Notification preferences
- Product ratings/reviews
- Promotions
- Returns
- Refunds
- Customer support
- Delivery tracking
- Warranty tracking where applicable

---

# 36. Customer Account Settings

The registered customer settings panel must include relevant sections such as:

- Personal information
- Profile photo
- Phone number
- Email address
- Password/security
- Addresses
- Notification preferences
- Marketing preferences
- Order history
- Warranty information
- Wishlist
- Reviews/ratings
- Communication preferences

The warranty section must allow customers to see active and historical warranty information for eligible products.

---

# 37. Audit Logging

**All important actions in the platform must be audit logged.**

Each audit log record must include at least:

- Action ID
- Action
- User who performed the action
- Date/time
- Related order, if the action is related to an order

The system may additionally record:

- Related customer
- Related product
- Related payment/refund
- Previous value/state where applicable
- New value/state where applicable
- Additional context

Examples of auditable actions include:

- Login/security actions where configured
- Order creation
- Order status change
- Payment status change
- Refund
- Partial refund
- Product change
- Price change
- Stock adjustment
- Damaged stock record
- Serial number assignment
- Packing confirmation
- Package handover
- Tracking update
- Customer profile change
- Recommendation-related administrative changes
- Warranty change
- Notification resend
- Admin permission change
- Customer care escalation
- Other important system actions

Audit logs must be protected from unauthorized modification.

---

# 38. Order History Audit View

Administrators and permitted internal users must be able to inspect an individual order's history.

The order history view should show:

- Order status changes
- Payment events
- Packing events
- Serial-number actions
- Dispatch/handover events
- Delivery events
- Refund events
- Customer-care actions
- Relevant audit events
- Timestamps
- User responsible for each action

---

# 39. Reporting and Analytics

Administrators must be able to generate and view reports.

## 39.1 Financial Reports

Reports should include:

- Sales
- Revenue
- Discounts
- Refunds
- Partial refunds
- Net sales
- Payment totals
- Order value summaries
- Sales over time
- Other configured financial metrics

## 39.2 Stock Reports

Reports should include:

- Current stock
- Stock movement
- Low stock
- Out of stock
- Damaged stock
- Lost stock
- Reserved stock
- Stock adjustments
- Serial-number inventory
- Stock valuation where supported

## 39.3 Product Reports

Reports should include:

- Product sales
- Product performance
- Product views where tracked
- Ratings
- Rating distribution
- Review counts
- Damaged stock by product
- Refund/return data by product
- Product popularity
- Product performance by category/brand

## 39.4 Order Reports

Reports should include:

- Orders by date
- Orders by status
- Orders by customer
- Orders by product
- Pre-orders
- Completed orders
- Cancelled orders
- Returned orders
- Refunded orders
- Delivery performance
- Estimated-vs-status information where supported

## 39.5 Customer Care Assistant Reports

Reports should include:

- Customer-care cases handled
- Cases by status
- Urgent attention cases
- Refunds processed
- Partial refunds processed
- Customer ratings/feedback related to customer-care assistants
- Customer-care performance metrics where supported

## 39.6 Trending Product Reports

Reports should include:

- Trending products
- Trending categories
- Recent popularity
- Sales-driven trends
- Engagement-driven trends
- Other configured trending indicators

## 39.7 Customer Reports

Reports should include:

- Customer registrations
- Active customers
- Purchase activity
- Spending summaries
- Order frequency
- Customer segmentation information
- Guest vs registered sales
- Customer engagement
- Other configured customer metrics

---

# 40. Reporting Filters and Export

Reports should support:

- Date range
- Product
- Brand
- Category
- Customer
- Order status
- Payment status
- Staff user
- Other relevant filters

Reports should be exportable in common formats where required, such as:

- CSV
- Excel
- PDF

---

# 41. Customer Communication History

The system should retain relevant communication history including:

- Email notifications
- SMS notifications
- Receipt sends/resends
- Order notifications
- Customer-care conversations
- Call requests
- Important support actions

Where supported, administrators/permitted staff should be able to view communication history related to a customer/order.

---

# 42. Email and SMS Templates

Administrators should be able to manage configurable notification templates for:

- Order confirmation
- Payment confirmation
- Receipt
- Receipt resend
- Order status changes
- Shipment/tracking updates
- Delivery updates
- Refund notifications
- Warranty notifications where needed
- Promotional notifications
- Recommended-product sale notifications
- Customer-care events where appropriate

Templates should support order/customer placeholders.

---

# 43. Security and Access Control

The system must enforce role-based access control.

Users must only be allowed to perform actions permitted by their role and permissions.

Security requirements should include:

- Secure authentication
- Password security
- Permission checks
- Secure guest access tokens
- Secure receipt links
- Secure warranty links
- Secure order tracking links
- Protection against unauthorized order access
- Protection against unauthorized refund actions
- Audit logging
- Session/security controls
- Secure handling of payment integration data

---

# 44. Front-End Operational Applications

The following non-admin roles must perform their daily work through front-end software:

- Customer care assistants
- Order packing users
- Stock management users

The front-end applications must communicate with the backend through **Django REST Framework API endpoints**.

These users must not require direct Django Admin access for normal operational work.

---

# 45. Administrator Interface

Administrators must use the **Django Admin Panel** for administration tasks.

The Django Admin should provide management interfaces for:

- Customers
- Staff users
- Permissions
- Products
- Categories
- Brands
- Product specifications
- Variants
- Promotions
- Orders
- Payments
- Refunds
- Inventory master data
- Warranties
- Notifications/templates
- Customer-care escalations
- Audit logs
- Reports/analytics access
- Site configuration

---

# 46. Technology Constraints

The system must use:

- **Backend:** Django + Django REST Framework
- **Database:** MySQL
- **Storage:** Google Cloud Storage (GCP Cloud Storage)
- **Payment Gateway:** PayPal Checkout

Cloud storage should be used for appropriate uploaded/media files such as:

- Customer profile photos
- Product images/media
- Generated receipt PDFs
- Other application files where applicable

---

# 47. Receipt and Document Storage

The platform should retain generated receipt documents according to business retention requirements.

Stored receipt files should be linked to the relevant order and customer/guest order context.

The system must allow secure retrieval without exposing unrelated files.

---

# 48. Product and Content Administration

Administrators must be able to maintain the online catalog without code changes for normal catalog operations.

This includes:

- Creating products
- Editing products
- Activating/deactivating products
- Assigning categories
- Assigning multiple categories
- Assigning brands
- Adding specifications
- Managing pricing
- Managing sale pricing
- Managing images
- Managing warranty settings
- Managing estimated arrival times
- Managing pre-order settings
- Managing recommendation tags
- Managing related products

---

# 49. Recommended Order and Customer Experience Flow

## Guest Purchase Flow

1. Customer browses products
2. Customer searches/filters products
3. Customer views product
4. Customer adds item(s) to cart
5. Customer reviews estimated arrival
6. Customer proceeds to guest checkout
7. Customer enters delivery/contact information
8. Customer pays with PayPal
9. Order is created
10. Receipt PDF is generated
11. Email/SMS confirmation is sent
12. Email/SMS contains secure receipt download link
13. Email/SMS contains secure order tracking link
14. Email/SMS contains secure warranty tracking link when applicable
15. Customer tracks the order through the secure link

## Registered Customer Purchase Flow

1. Customer logs in
2. Customer browses/searches
3. Personalized sections may appear when sufficient data exists
4. Customer adds items to cart
5. Customer reviews estimated arrival
6. Customer checks out
7. Customer pays with PayPal
8. Order is created
9. Receipt is generated
10. Email/SMS notifications are sent according to preferences
11. Customer can access the order from the account
12. Customer can download/re-download the receipt
13. Customer can resend receipt by email/SMS
14. Customer can track the order
15. Customer can track warranty from account settings
16. Customer can later rate eligible purchased products

---

# 50. Key Business Rules

1. A product may belong to multiple categories.
2. Every product must have an estimated arrival time.
3. Pre-order products must clearly indicate that they are pre-orders.
4. An order's estimated arrival date must be based on the product in the order with the longest estimated arrival time.
5. Guest customers must be able to complete checkout without an account.
6. PayPal Checkout must be the payment gateway.
7. Receipts must be available as downloadable PDFs.
8. Receipt links in email/SMS must securely reference the correct order.
9. Registered customers must be able to re-download and resend receipts.
10. Registered customers must be able to track orders from their account.
11. Guests must be able to track orders through secure links sent by email/SMS.
12. Guests must be able to track warranty through the separate secure warranty link.
13. Product ratings must be restricted to logged-in customers with verified phone numbers who purchased the relevant product.
14. The maximum product rating is 5 stars.
15. Customer care assistants can refund eligible products, including partial/product-specific refunds when authorized.
16. Order packing users must record serial numbers for serial-tracked products after packing.
17. Order packing users must update package status after handing packages to the delivery company.
18. Stock management users must be able to manage stock through the front-end operational application.
19. Customer care assistants must be able to escalate urgent matters to administrators.
20. Personalized recommendations should only be displayed when sufficient customer data exists.
21. Sale notifications for personalized recommendations must respect customer notification settings.
22. Warranty information must be visible to registered customers through the website settings/account area.
23. All important system actions must be audit logged.
24. Audit records must include action ID, action, acting user, and related order when applicable.
25. Administrators use the Django Admin Panel.
26. Customer care, packing, and stock users use front-end software through API endpoints.
27. MySQL is the primary database.
28. GCP Cloud Storage is used for application file storage.
29. Django REST Framework provides the API layer.
30. The platform must support common e-commerce capabilities expected by customers of major marketplaces such as product search, filtering, wishlist, ratings, reviews, promotions, order tracking, returns, refunds, recommendations, and customer support.

---

# 51. Non-Functional Expectations

Although this document focuses on functional requirements, DevCommerce should also be designed to provide:

- Responsive user experience
- Fast product discovery
- Reliable checkout
- Reliable order processing
- Reliable notification delivery
- Secure payment workflows
- Secure customer/order data access
- Scalable API architecture
- Reliable file storage
- Traceable operational actions
- Clear error handling
- High availability appropriate to business needs
- Maintainable role-based workflows

