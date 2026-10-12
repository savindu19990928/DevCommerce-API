# FLXCORE ASSISTANT API Documentation

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


