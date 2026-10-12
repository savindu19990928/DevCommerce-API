# FLXCORE ADMIN API Documentation

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


### 1.14 `GET / POST / PUT / DELETE /api/users/permissions/`
- **Summary**: Granular ABAC permissions management engine. Superusers can grant permissions globally or per-object. Staff with `can_delegate=True` can delegate matching permissions to peers sharing their exact role.
- **Permissions**: `SUPERUSER`, `ADMIN`, or Staff with `can_delegate=True`
- **Scenario A: Admin Grants Global Stock Management Access (`POST /api/users/permissions/`)**
  - **Request Body**:
  ```json
  {
    "user": 22,
    "model_name": "product",
    "object_id": null,
    "can_view": true,
    "can_add": true,
    "can_change": true,
    "can_delete": false,
    "can_delegate": true
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 5,
    "user": 22,
    "content_type": 12,
    "object_id": null,
    "can_view": true,
    "can_add": true,
    "can_change": true,
    "can_delete": false,
    "can_delegate": true
  }
  ```
- **Scenario B: Staff Peer-to-Peer Delegation (`POST /api/users/permissions/`)**
  - *Context*: `STOCK` user ID 22 delegates object-level view permission on Product 9 to peer `STOCK` user ID 25.
  - **Request Body**:
  ```json
  {
    "user": 25,
    "model_name": "product",
    "object_id": 9,
    "can_view": true,
    "can_add": false,
    "can_change": false,
    "can_delete": false,
    "can_delegate": false
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 6,
    "user": 25,
    "content_type": 12,
    "object_id": 9,
    "can_view": true,
    "can_add": false,
    "can_change": false,
    "can_delete": false,
    "can_delegate": false
  }
  ```
- **Scenario C: Invalid Cross-Role Delegation Attempt**
  - *Context*: `STOCK` user tries to delegate to an `ASSISTANT` user.
  - **Response (403 Forbidden)**:
  ```json
  {
    "detail": "You can only delegate to users with your exact same role."
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

### 2.2 `GET / POST / PUT / PATCH / DELETE /api/catalog/categories/`
- **Summary**: Retrieves product categories (hierarchical parent-child support) or allows Admins to manage them.
- **Permissions**: Read: `ANY`; Write/Update/Delete: `ADMIN` / `SUPERUSER`
- **Query Parameters (GET)**: `parent` (integer category ID)
- **Scenario A: Public List Categories (`GET /api/catalog/categories/`)**
  - **Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "name": "Computers & Laptops",
      "slug": "computers-laptops",
      "description": "Laptops, Desktops, and Workstations",
      "parent": null
    },
    {
      "id": 2,
      "name": "MacBooks",
      "slug": "macbooks",
      "description": "Apple Silicon MacBooks",
      "parent": 1
    }
  ]
  ```
- **Scenario B: Admin Create Category (`POST /api/catalog/categories/`)**
  - **Request Body**:
  ```json
  {
    "name": "Monitors & Displays",
    "slug": "monitors-displays",
    "description": "High resolution gaming and productivity monitors",
    "parent": null
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 3,
    "name": "Monitors & Displays",
    "slug": "monitors-displays",
    "description": "High resolution gaming and productivity monitors",
    "parent": null
  }
  ```

---


### 2.3 `GET / POST / PUT / PATCH / DELETE /api/catalog/brands/`
- **Summary**: Retrieves brand catalog or allows Admins to create/modify brands.
- **Permissions**: Read: `ANY`; Write/Update/Delete: `ADMIN` / `SUPERUSER`
- **Scenario A: List Brands (`GET /api/catalog/brands/`)**
  - **Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "name": "Apple",
      "slug": "apple",
      "logo": "https://devcom.devrious.lk/media/brands/apple.png"
    }
  ]
  ```
- **Scenario B: Admin Create Brand (`POST /api/catalog/brands/`)**
  - **Request Body**:
  ```json
  {
    "name": "Logitech",
    "slug": "logitech"
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 2,
    "name": "Logitech",
    "slug": "logitech",
    "logo": null
  }
  ```

---


### 2.5 `POST / PUT / PATCH / DELETE /api/catalog/products/`
- **Summary**: Creates, updates, or archives products in the catalog.
- **Permissions**: `ADMIN` / `SUPERUSER` ONLY
- **Create Product Request (`POST /api/catalog/products/`)**:
```json
{
  "name": "Sony WH-1000XM5 Wireless Headphones",
  "sku": "SONY-WH1000XM5-BLK",
  "description": "Industry leading noise canceling headphones",
  "price": "399.00",
  "cost_price": "280.00",
  "sale_price": "349.00",
  "unit_of_measurement": "piece",
  "minimum_stock_level": 10,
  "maximum_stock_level": 100,
  "status": "ACTIVE",
  "is_preorder": true,
  "preorder_arrival_days": 7,
  "stock_arrival_days": 2,
  "brand": 2,
  "categories": [3]
}
```
- **Response (201 Created)**:
```json
{
  "id": 15,
  "name": "Sony WH-1000XM5 Wireless Headphones",
  "sku": "SONY-WH1000XM5-BLK",
  "price": "399.00",
  "sale_price": "349.00",
  "cost_price": "280.00",
  "status": "ACTIVE",
  "is_preorder": true,
  "brand": 2,
  "categories": [3],
  "images": [],
  "specifications": [],
  "variants": []
}
```


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


### 3.8 `GET / POST / PUT / DELETE /api/orders/coupons/`
- **Summary**: Manages discount promo codes. Public users only receive active coupons.
- **Permissions**: Read: `ANY` (active only); Create/Update/Delete: `ADMIN` / `SUPERUSER`
- **Scenario A: Public List Active Coupons (`GET /api/orders/coupons/`)**
  - **Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "code": "DEVCOM10",
      "discount_percentage": "10.00",
      "valid_from": "2026-01-01T00:00:00Z",
      "valid_until": "2026-12-31T23:59:59Z",
      "active": true
    }
  ]
  ```
- **Scenario B: Admin Create Coupon (`POST /api/orders/coupons/`)**
  - **Request Body**:
  ```json
  {
    "code": "FLASH25",
    "discount_percentage": "25.00",
    "valid_from": "2026-03-01T00:00:00Z",
    "valid_until": "2026-03-05T23:59:59Z",
    "active": true
  }
  ```
  - **Response (201 Created)**:
  ```json
  {
    "id": 2,
    "code": "FLASH25",
    "discount_percentage": "25.00",
    "valid_from": "2026-03-01T00:00:00Z",
    "valid_until": "2026-03-05T23:59:59Z",
    "active": true
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



## 6. Marketing & Promotions (`/api/marketing/`)

### 6.1 `GET / POST / PUT / PATCH / DELETE /api/marketing/tags/`
- **Summary**: Manages recommendation tags and dynamic promotional product groupings.
- **Permissions**: `ADMIN` / `SUPERUSER` ONLY
- **Request Body (`POST /api/marketing/tags/`)**:
```json
{
  "name": "Trending Developer Tools",
  "products": [1, 2, 4]
}
```
- **Response (201 Created)**:
```json
{
  "id": 3,
  "name": "Trending Developer Tools",
  "products": [1, 2, 4]
}
```

---



## 7. Reports & Analytics (`/api/reports/`)

### 7.1 `GET /api/reports/`
- **Summary**: Returns aggregate analytics for the administrator dashboard, including gross revenue from paid orders, total order count, active products count, and low stock warnings.
- **Permissions**: `ADMIN` / `SUPERUSER` ONLY
- **Scenario A: Admin Dashboard View**
  - **Response (200 OK)**:
  ```json
  {
    "financials": {
      "total_revenue": "145890.50",
      "total_orders": 342
    },
    "inventory": {
      "total_products": 128,
      "low_stock_alerts": 7
    },
    "message": "Full PDF/CSV exports can be built from this endpoint."
  }
  ```
- **Scenario B: Non-Admin Access Attempt**
  - **Response (403 Forbidden)**:
  ```json
  {
    "detail": "Only admins can access reports."
  }
  ```

---


