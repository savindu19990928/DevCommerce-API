# FLXCORE CUSTOMER API Documentation

This document contains only the endpoints accessible by this user type.

# FLXCORE API Documentation

Base URL: `https://devcom.devrious.lk`

---


## 1. Authentication & User Management (`/api/users/`)

### 1.3 `POST /api/users/auth/change-password/`
- **Summary**: Allows an authenticated user to update their account password.
- **Permissions**: `CUSTOMER`, `ADMIN`, `ASSISTANT`, `STOCK`, `PACKING`, `SUPERUSER` (Authenticated)
- **Request Body**:
```json
{
  "old_password": "OldSecurePassword123!",
  "new_password": "NewSecurePassword456!"
}
```
- **Response (200 OK)**:
```json
{
  "message": "Password updated successfully."
}
```
- **Error Response (400 Bad Request - Incorrect Old Password)**:
```json
{
  "error": "Incorrect old password."
}
```

---


### 1.6 `POST /api/users/auth/send-otp/`
- **Summary**: Generates a 6-digit verification OTP and delivers it via Email or SMS.
- **Permissions**: `CUSTOMER`, `ADMIN`, `ASSISTANT`, `STOCK`, `PACKING` (Authenticated)
- **Scenario A: Email Verification Request**
  - **Request Body**:
  ```json
  {
    "contact_type": "EMAIL"
  }
  ```
  - **Response (200 OK)**:
  ```json
  {
    "message": "OTP sent to email."
  }
  ```
- **Scenario B: Phone Verification Request**
  - **Request Body**:
  ```json
  {
    "contact_type": "PHONE"
  }
  ```
  - **Response (200 OK)**:
  ```json
  {
    "message": "OTP sent to phone."
  }
  ```
- **Scenario C: Already Verified Error**
  - **Response (400 Bad Request)**:
  ```json
  {
    "error": "Phone is already verified."
  }
  ```

---


### 1.7 `POST /api/users/auth/verify-otp/`
- **Summary**: Verifies the 6-digit OTP code and marks `is_email_verified` or `is_phone_verified` as `true`.
- **Permissions**: Authenticated User
- **Request Body**:
```json
{
  "contact_type": "PHONE",
  "otp_code": "849201"
}
```
- **Response (200 OK)**:
```json
{
  "message": "Phone verified successfully."
}
```
- **Error Response (400 Bad Request)**:
```json
{
  "error": "Invalid or expired OTP."
}
```

---


### 1.8 `GET /api/users/users/`
- **Summary**: Lists user accounts. Customers only see their own profile; Admins see all registered accounts.
- **Permissions**: `CUSTOMER` (filtered to self), `ADMIN` / `SUPERUSER` (all users)
- **Scenario A: Customer Request**
  - **Response (200 OK)**:
  ```json
  [
    {
      "id": 14,
      "username": "johndoe",
      "email": "johndoe@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "CUSTOMER",
      "phone_number": "+94771234567",
      "is_phone_verified": true,
      "is_email_verified": true,
      "profile": {
        "profile_photo": "https://devcom.devrious.lk/media/profiles/john.jpg",
        "bio": "DevCommerce frequent shopper"
      }
    }
  ]
  ```
- **Scenario B: Admin Request**
  - **Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@devcom.lk",
      "first_name": "System",
      "last_name": "Admin",
      "role": "ADMIN",
      "phone_number": "+94770000000",
      "is_phone_verified": true,
      "is_email_verified": true,
      "profile": null
    },
    {
      "id": 14,
      "username": "johndoe",
      "email": "johndoe@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "CUSTOMER",
      "phone_number": "+94771234567",
      "is_phone_verified": true,
      "is_email_verified": true,
      "profile": {
        "profile_photo": "https://devcom.devrious.lk/media/profiles/john.jpg",
        "bio": "DevCommerce frequent shopper"
      }
    }
  ]
  ```

---


### 1.9 `GET /api/users/users/<id>/`
- **Summary**: Retrieves profile details for a specific user ID.
- **Permissions**: `CUSTOMER` (only own ID), `ADMIN` (any ID)
- **Response (200 OK)**:
```json
{
  "id": 14,
  "username": "johndoe",
  "email": "johndoe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "CUSTOMER",
  "phone_number": "+94771234567",
  "is_phone_verified": true,
  "is_email_verified": true,
  "profile": {
    "profile_photo": "https://devcom.devrious.lk/media/profiles/john.jpg",
    "bio": "DevCommerce frequent shopper"
  }
}
```

---


### 1.10 `PUT / PATCH /api/users/users/<id>/`
- **Summary**: Updates user profile fields. Role and verification flags are read-only here.
- **Permissions**: `CUSTOMER` (own ID), `ADMIN`
- **Request Body (PATCH)**:
```json
{
  "first_name": "Jonathan",
  "phone_number": "+94779876543"
}
```
- **Response (200 OK)**:
```json
{
  "id": 14,
  "username": "johndoe",
  "email": "johndoe@example.com",
  "first_name": "Jonathan",
  "last_name": "Doe",
  "role": "CUSTOMER",
  "phone_number": "+94779876543",
  "is_phone_verified": false,
  "is_email_verified": true,
  "profile": null
}
```

---


### 1.11 `GET /api/users/users/<id>/wishlist/`
- **Summary**: Retrieves the wishlist and nested wishlist items for a specific customer.
- **Permissions**: `CUSTOMER` (own ID), `ADMIN`
- **Response (200 OK)**:
```json
{
  "id": 3,
  "user": 14,
  "created_at": "2026-01-15T08:30:00Z",
  "items": [
    {
      "id": 18,
      "wishlist": 3,
      "product": 5,
      "added_at": "2026-02-01T10:15:00Z"
    }
  ]
}
```

---


### 1.12 `GET / POST / PUT / DELETE /api/users/addresses/`
- **Summary**: Manages user delivery and billing addresses.
- **Permissions**: `CUSTOMER` (own addresses), `ADMIN` (all addresses)
- **Scenario A: List Customer Addresses (`GET /api/users/addresses/`)**
  - **Response (200 OK)**:
  ```json
  [
    {
      "id": 8,
      "user": 14,
      "address_line_1": "No. 45 Galle Road",
      "address_line_2": "Apt 3B",
      "city": "Colombo",
      "state": "Western",
      "postal_code": "00300",
      "country": "Sri Lanka",
      "is_default_shipping": true,
      "is_default_billing": true
    }
  ]
  ```
- **Scenario B: Create Address (`POST /api/users/addresses/`)**
  - **Request Body**:
  ```json
  {
    "address_line_1": "No. 12 Kandy Road",
    "address_line_2": "",
    "city": "Kiribathgoda",
    "state": "Western",
    "postal_code": "11600",
    "country": "Sri Lanka",
    "is_default_shipping": false,
    "is_default_billing": false
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 9,
    "user": 14,
    "address_line_1": "No. 12 Kandy Road",
    "address_line_2": "",
    "city": "Kiribathgoda",
    "state": "Western",
    "postal_code": "11600",
    "country": "Sri Lanka",
    "is_default_shipping": false,
    "is_default_billing": false
  }
  ```

---


### 1.15 `GET / POST / DELETE /api/users/wishlist/` & `/wishlist-items/`
- **Summary**: Manages customer wishlists and items.
- **Permissions**: `CUSTOMER`, `ADMIN`
- **Scenario A: Add Product to Wishlist (`POST /api/users/wishlist-items/`)**
  - **Request Body**:
  ```json
  {
    "product": 5
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 19,
    "wishlist": 3,
    "product": 5,
    "added_at": "2026-02-28T14:20:00Z"
  }
  ```
- **Scenario B: Remove Product from Wishlist (`DELETE /api/users/wishlist-items/19/`)**
  - **Response (204 No Content)**

---



## 2. Catalog & Products (`/api/catalog/`)

### 2.7 `GET / POST / PUT / DELETE /api/catalog/reviews/`
- **Summary**: Manages product reviews. Customers can only post reviews if their phone number is verified (`is_phone_verified=True`).
- **Permissions**: Read: `ANY` (approved reviews); Create/Update/Delete: `CUSTOMER` (own reviews), `ADMIN`
- **Scenario A: Phone-Verified Customer Posts Review (`POST /api/catalog/reviews/`)**
  - **Request Body**:
  ```json
  {
    "product": 1,
    "rating": 5,
    "comment": "Incredible performance and battery life. Highly recommended!"
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 12,
    "product": 1,
    "user": 14,
    "rating": 5,
    "comment": "Incredible performance and battery life. Highly recommended!",
    "is_approved": true,
    "created_at": "2026-02-28T15:00:00Z"
  }
  ```
- **Scenario B: Unverified Customer Attempt (`POST /api/catalog/reviews/`)**
  - **Response (403 Forbidden)**:
  ```json
  {
    "detail": "You must verify your phone number to leave a review."
  }
  ```

---



## 3. Order Management & Checkout (`/api/orders/`)

### 3.4 `GET /api/orders/orders/`
- **Summary**: Retrieves orders. Customers only see their own order history; Staff (`ADMIN`, `ASSISTANT`, `PACKING`) see all system orders.
- **Permissions**: `CUSTOMER` (own orders), `ADMIN` / `ASSISTANT` / `PACKING` / `SUPERUSER`
- **Scenario A: Customer View (`GET /api/orders/orders/`)**
  - **Response (200 OK)**:
  ```json
  [
    {
      "id": 88,
      "order_number": "ORD-20260228-88",
      "status": "CONFIRMED",
      "payment_status": "SUCCESS",
      "subtotal": "1999.00",
      "discount": "100.00",
      "total": "1899.00",
      "estimated_arrival_date": "2026-03-05",
      "is_overdue": false,
      "created_at": "2026-02-28T10:00:00Z"
    }
  ]
  ```
- **Scenario B: Staff / Admin View (`GET /api/orders/orders/`)**
  - **Response (200 OK)**:
  ```json
  [
    {
      "id": 88,
      "order_number": "ORD-20260228-88",
      "user": 14,
      "guest_email": null,
      "status": "CONFIRMED",
      "payment_status": "SUCCESS",
      "subtotal": "1999.00",
      "discount": "100.00",
      "total": "1899.00",
      "requires_urgent_attention": false,
      "estimated_arrival_date": "2026-03-05",
      "is_overdue": false,
      "created_at": "2026-02-28T10:00:00Z"
    },
    {
      "id": 89,
      "order_number": "550e8400-e29b-41d4-a716-446655440000",
      "user": null,
      "guest_email": "guest.buyer@example.com",
      "status": "PENDING",
      "payment_status": "SUCCESS",
      "subtotal": "2197.00",
      "discount": "0.00",
      "total": "2197.00",
      "requires_urgent_attention": true,
      "estimated_arrival_date": "2026-03-02",
      "is_overdue": false,
      "created_at": "2026-02-28T11:30:00Z"
    }
  ]
  ```

---


### 3.5 `POST /api/orders/orders/<id>/resend_receipt/`
- **Summary**: Retriggers the notification service to resend the PDF receipt link via Email to the order's owner or guest email.
- **Permissions**: `CUSTOMER` (own order), `ADMIN`, `ASSISTANT`
- **Request**: `POST /api/orders/orders/88/resend_receipt/`
- **Response (200 OK)**:
```json
{
  "message": "Receipt resent via email."
}
```

---


### 3.7 `GET / POST / DELETE /api/orders/cart/` & `POST /cart/<id>/checkout/`
- **Summary**: Manages customer cart and completes registered checkout with optional coupon promo code validation.
- **Permissions**: `CUSTOMER`, `ADMIN`
- **Scenario A: View Cart (`GET /api/orders/cart/`)**
  - **Response (200 OK)**:
  ```json
  [
    {
      "id": 12,
      "user": 14,
      "items": [
        {
          "id": 45,
          "cart": 12,
          "product": 1,
          "variant": null,
          "quantity": 1
        }
      ]
    }
  ]
  ```
- **Scenario B: Registered User Cart Checkout (`POST /api/orders/cart/12/checkout/`)**
  - **Request Body**:
  ```json
  {
    "promo_code": "DEVCOM10"
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 92,
    "order_number": "3c90a12e-1d54-44b2-9f36-9b5129671182",
    "subtotal": "1999.00",
    "discount": "199.90",
    "total": "1799.10",
    "status": "PENDING",
    "payment_status": "PENDING",
    "estimated_arrival_date": "2026-03-02",
    "items": [
      {
        "id": 210,
        "product": 1,
        "quantity": 1,
        "unit_price": "1999.00",
        "subtotal": "1999.00"
      }
    ]
  }
  ```
- **Scenario C: Invalid / Expired Promo Code Error**
  - **Request Body**:
  ```json
  {
    "promo_code": "INVALID_CODE"
  }
  ```
  - **Response (400 Bad Request)**:
  ```json
  {
    "error": "Invalid or expired promo code"
  }
  ```

---


### 3.9 `GET / POST / PUT / DELETE /api/orders/phone-call-requests/`
- **Summary**: Allows customers to request a callback from staff regarding an order.
- **Permissions**: `CUSTOMER` (own requests), `ASSISTANT`, `ADMIN`
- **Scenario A: Customer Submits Callback Request (`POST /api/orders/phone-call-requests/`)**
  - **Request Body**:
  ```json
  {
    "order": 88,
    "phone_number": "+94771234567",
    "reason": "Need to update shipping address before dispatch."
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 5,
    "order": 88,
    "user": 14,
    "phone_number": "+94771234567",
    "reason": "Need to update shipping address before dispatch.",
    "is_resolved": false,
    "created_at": "2026-02-28T16:00:00Z"
  }
  ```
- **Scenario B: Assistant Marks Request Resolved (`PATCH /api/orders/phone-call-requests/5/`)**
  - **Request Body**:
  ```json
  {
    "is_resolved": true
  }
  ```
  - **Response (200 OK)**:
  ```json
  {
    "id": 5,
    "order": 88,
    "user": 14,
    "phone_number": "+94771234567",
    "reason": "Need to update shipping address before dispatch.",
    "is_resolved": true,
    "created_at": "2026-02-28T16:00:00Z"
  }
  ```

---


### 3.10 `GET / POST / PUT / DELETE /api/orders/warranties/`
- **Summary**: Manages product warranty records linked to specific order items and serial numbers.
- **Permissions**: `CUSTOMER` (own warranties), `ASSISTANT`, `ADMIN`
- **Request Body (`POST /api/orders/warranties/`)**:
```json
{
  "order_item": 201,
  "serial_number": 101,
  "start_date": "2026-02-28",
  "end_date": "2027-02-28",
  "status": "ACTIVE"
}
```
- **Response (201 Created)**:
```json
{
  "id": 14,
  "order_item": 201,
  "serial_number": 101,
  "start_date": "2026-02-28",
  "end_date": "2027-02-28",
  "status": "ACTIVE"
}
```

---


### 3.11 `GET / POST / PUT / DELETE /api/orders/refunds/`
- **Summary**: Handles order item refund requests and approval workflows.
- **Permissions**: `CUSTOMER` (initiate for own order), `ASSISTANT`, `ADMIN`
- **Scenario A: Customer Requests Refund (`POST /api/orders/refunds/`)**
  - **Request Body**:
  ```json
  {
    "order": 88,
    "items": [201],
    "amount": "1999.00",
    "reason": "Item arrived with cosmetic damage.",
    "status": "REQUESTED"
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 6,
    "order": 88,
    "items": [201],
    "amount": "1999.00",
    "reason": "Item arrived with cosmetic damage.",
    "status": "REQUESTED",
    "initiated_by": 14,
    "created_at": "2026-02-28T16:30:00Z"
  }
  ```
- **Scenario B: Assistant Approves Refund (`PATCH /api/orders/refunds/6/`)**
  - **Request Body**:
  ```json
  {
    "status": "COMPLETED"
  }
  ```
  - **Response (200 OK)**:
  ```json
  {
    "id": 6,
    "order": 88,
    "items": [201],
    "amount": "1999.00",
    "reason": "Item arrived with cosmetic damage.",
    "status": "COMPLETED",
    "initiated_by": 14,
    "created_at": "2026-02-28T16:30:00Z"
  }
  ```

---



## 4. Support & Customer Care (`/api/support/`)

### 4.1 `GET / POST / PUT / PATCH / DELETE /api/support/cases/`
- **Summary**: Opens and manages customer support tickets.
- **Permissions**: `CUSTOMER` (own cases), `ASSISTANT`, `ADMIN`
- **Scenario A: Customer Opens Ticket (`POST /api/support/cases/`)**
  - **Request Body**:
  ```json
  {
    "order": 88,
    "subject": "Inquiry about delivery schedule",
    "is_urgent": false,
    "status": "OPEN"
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 10,
    "customer": 14,
    "guest_email": null,
    "order": 88,
    "assigned_assistant": null,
    "status": "OPEN",
    "subject": "Inquiry about delivery schedule",
    "is_urgent": false,
    "created_at": "2026-02-28T17:00:00Z",
    "updated_at": "2026-02-28T17:00:00Z",
    "communications": []
  }
  ```
- **Scenario B: Assistant Assigns Case to Self and Updates Status (`PATCH /api/support/cases/10/`)**
  - **Request Body**:
  ```json
  {
    "status": "IN_PROGRESS"
  }
  ```
  - **Response (200 OK)**:
  ```json
  {
    "id": 10,
    "customer": 14,
    "guest_email": null,
    "order": 88,
    "assigned_assistant": 4,
    "status": "IN_PROGRESS",
    "subject": "Inquiry about delivery schedule",
    "is_urgent": false,
    "created_at": "2026-02-28T17:00:00Z",
    "updated_at": "2026-02-28T17:05:00Z",
    "communications": []
  }
  ```

---


### 4.2 `GET / POST / DELETE /api/support/communications/`
- **Summary**: Appends message threads to an active customer care case.
- **Permissions**: `CUSTOMER` (own cases), `ASSISTANT`, `ADMIN`
- **Scenario A: Customer Sends Message (`POST /api/support/communications/`)**
  - **Request Body**:
  ```json
  {
    "care_case": 10,
    "message": "Hi, could you let me know if this order will arrive before Friday?",
    "channel": "CHAT"
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 25,
    "care_case": 10,
    "sender": 14,
    "is_customer": true,
    "message": "Hi, could you let me know if this order will arrive before Friday?",
    "channel": "CHAT",
    "created_at": "2026-02-28T17:10:00Z"
  }
  ```
- **Scenario B: Assistant Replies to Customer (`POST /api/support/communications/`)**
  - **Request Body**:
  ```json
  {
    "care_case": 10,
    "message": "Hello John, yes your package is scheduled for delivery on Thursday.",
    "channel": "CHAT"
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 26,
    "care_case": 10,
    "sender": 4,
    "is_customer": false,
    "message": "Hello John, yes your package is scheduled for delivery on Thursday.",
    "channel": "CHAT",
    "created_at": "2026-02-28T17:15:00Z"
  }
  ```

---


