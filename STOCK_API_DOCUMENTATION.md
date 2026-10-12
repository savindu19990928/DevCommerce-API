# FLXCORE STOCK API Documentation

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



## 2. Catalog & Products (`/api/catalog/`)

### 2.6 Product Photo Management & Multi-Image Upload
Products support up to **5 photos maximum**. Staff can upload single or multiple photos simultaneously via multipart form requests.

#### 2.6.1 `POST /api/catalog/products/<id>/upload_images/`
- **Summary**: Uploads one or multiple photos directly to a specific product. Validates that the total number of images for the product does not exceed 5.
- **Permissions**: `ADMIN`, `SUPERUSER`, or `STOCK` (with granular permission)
- **Headers**:
  ```http
  Content-Type: multipart/form-data
  ```
- **Request Body (Multipart Form)**:
  - `images`: Binary file(s) (can provide multiple file entries under the `images` key)
- **Scenario A: Uploading 3 Product Photos Simultaneously**
  - **Response (201 Created)**:
  ```json
  [
    {
      "id": 101,
      "product": 1,
      "image": "https://devcom.devrious.lk/media/products/mbp14_front.jpg",
      "is_primary": true,
      "order": 0
    },
    {
      "id": 102,
      "product": 1,
      "image": "https://devcom.devrious.lk/media/products/mbp14_side.jpg",
      "is_primary": false,
      "order": 1
    },
    {
      "id": 103,
      "product": 1,
      "image": "https://devcom.devrious.lk/media/products/mbp14_keyboard.jpg",
      "is_primary": false,
      "order": 2
    }
  ]
  ```
- **Scenario B: Exceeding Max 5 Photos Limit Error**
  - *Context*: Attempting to upload 3 photos when the product already has 3 photos (total would be 6 > 5).
  - **Response (400 Bad Request)**:
  ```json
  {
    "error": "Cannot upload 3 photos. Product currently has 3 photos. Maximum allowed is 5 photos per product."
  }
  ```

#### 2.6.2 `GET / POST / PUT / PATCH / DELETE /api/catalog/product-images/`
- **Summary**: CRUD endpoint for product images. Supports single or multiple file uploads, setting primary display photo (`is_primary`), and custom ordering.
- **Permissions**: Read: `ANY`; Create/Update/Delete: `ADMIN` / `SUPERUSER` / `STOCK`
- **Query Parameters (GET)**: `product` (integer product ID), `is_primary` (boolean)
- **Scenario A: List Photos for Product (`GET /api/catalog/product-images/?product=1`)**
  - **Response (200 OK)**:
  ```json
  [
    {
      "id": 101,
      "product": 1,
      "image": "https://devcom.devrious.lk/media/products/mbp14_front.jpg",
      "is_primary": true,
      "order": 0
    },
    {
      "id": 102,
      "product": 1,
      "image": "https://devcom.devrious.lk/media/products/mbp14_side.jpg",
      "is_primary": false,
      "order": 1
    }
  ]
  ```
- **Scenario B: Upload Photos via Image Endpoint (`POST /api/catalog/product-images/`)**
  - **Request Body (Multipart Form)**:
    - `product`: `1`
    - `images`: file1.jpg, file2.jpg
    - `is_primary`: `false`
  - **Response (201 Created)**:
  ```json
  [
    {
      "id": 104,
      "product": 1,
      "image": "https://devcom.devrious.lk/media/products/mbp14_ports.jpg",
      "is_primary": false,
      "order": 2
    },
    {
      "id": 105,
      "product": 1,
      "image": "https://devcom.devrious.lk/media/products/mbp14_box.jpg",
      "is_primary": false,
      "order": 3
    }
  ]
  ```
- **Scenario C: Update Primary Photo (`PATCH /api/catalog/product-images/102/`)**
  - **Request Body**:
  ```json
  {
    "is_primary": true
  }
  ```
  - **Response (200 OK)**:
  ```json
  {
    "id": 102,
    "product": 1,
    "image": "https://devcom.devrious.lk/media/products/mbp14_side.jpg",
    "is_primary": true,
    "order": 1
  }
  ```
- **Scenario D: Delete Photo (`DELETE /api/catalog/product-images/105/`)**
  - **Response (204 No Content)**

---



## 5. Inventory & Stock Management (`/api/inventory/`)

### 5.1 `GET / POST / PUT / DELETE /api/inventory/movements/`
- **Summary**: Logs physical stock additions, deductions, damages, or adjustments.
- **Permissions**: `STOCK`, `ADMIN`, `SUPERUSER` (Requires `GranularPermission` for `StockMovement`)
- **Request Body (`POST /api/inventory/movements/`)**:
```json
{
  "product": 1,
  "variant": 50,
  "movement_type": "ADD",
  "quantity": 25,
  "notes": "Stock shipment batch #FLX-2026-88 arrived at warehouse."
}
```
- **Response (201 Created)**:
```json
{
  "id": 42,
  "product": 1,
  "variant": 50,
  "movement_type": "ADD",
  "quantity": 25,
  "notes": "Stock shipment batch #FLX-2026-88 arrived at warehouse.",
  "created_by": 22,
  "created_at": "2026-02-28T18:00:00Z"
}
```

---


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


