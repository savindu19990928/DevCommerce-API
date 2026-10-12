# FLXCORE PACKING API Documentation

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


### 3.6 `POST /api/orders/orders/<id>/mark_as_packed/`
- **Summary**: Finalizes packing phase, records serial numbers, changes order status to `IN_TRANSIT`, and logs audit trail.
- **Permissions**: `PACKING`, `ADMIN`, `SUPERUSER`
- **Scenario A: Successful Packing Execution**
  - **Request Body**:
  ```json
  {
    "items": [
      {
        "order_item_id": 201,
        "serial_numbers": [101]
      }
    ]
  }
  ```
  - **Response (200 OK)**:
  ```json
  {
    "message": "Order packed and marked as in transit."
  }
  ```
- **Scenario B: Unauthorized Staff Role Attempt**
  - **Response (403 Forbidden)**:
  ```json
  {
    "error": "Permission denied."
  }
  ```

---



## 5. Inventory & Stock Management (`/api/inventory/`)

### 5.2 `GET / POST / PUT / PATCH / DELETE /api/inventory/serials/`
- **Summary**: Registers and tracks individual item serial numbers (`IN_STOCK`, `RESERVED`, `PACKED`, `SOLD`, `DAMAGED`, `RETURNED`).
- **Permissions**: `STOCK`, `PACKING`, `ADMIN`, `SUPERUSER` (Requires `GranularPermission` for `SerialNumber`)
- **Query Parameters (GET)**: `status`, `product`
- **Scenario A: Register New Serial Number (`POST /api/inventory/serials/`)**
  - **Request Body**:
  ```json
  {
    "product": 1,
    "variant": 50,
    "serial_number": "MBP14-M3-9948201",
    "status": "IN_STOCK",
    "notes": "Shelf A-12"
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 101,
    "product": 1,
    "variant": 50,
    "serial_number": "MBP14-M3-9948201",
    "status": "IN_STOCK",
    "notes": "Shelf A-12",
    "created_at": "2026-02-28T18:15:00Z",
    "updated_at": "2026-02-28T18:15:00Z"
  }
  ```
- **Scenario B: Filter In-Stock Serials (`GET /api/inventory/serials/?product=1&status=IN_STOCK`)**
  - **Response (200 OK)**:
  ```json
  [
    {
      "id": 101,
      "product": 1,
      "variant": 50,
      "serial_number": "MBP14-M3-9948201",
      "status": "IN_STOCK",
      "notes": "Shelf A-12",
      "created_at": "2026-02-28T18:15:00Z",
      "updated_at": "2026-02-28T18:15:00Z"
    }
  ]
  ```

---


