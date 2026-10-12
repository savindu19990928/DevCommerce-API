# FLXCORE COMMON API Documentation

This document contains only the endpoints accessible by this user type.

# FLXCORE API Documentation

Base URL: `https://devcom.devrious.lk`

---


## 1. Authentication & User Management (`/api/users/`)

### 1.1 `POST /api/users/auth/token/`
- **Summary**: Obtains a JSON Web Token (JWT) access and refresh pair with encoded user role claims. Authentication is strictly performed via **`email` and `password`** (not username).
- **Permissions**: `ANY` (Public)
- **Request Body**:
```json
{
  "email": "customer@example.com",
  "password": "CustomerPassword123!"
}
```
- **Response (200 OK)**:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
- **Error Response (401 Unauthorized)**:
```json
{
  "detail": "No active account found with the given credentials"
}
```
- **Error Response (400 Bad Request - Missing Fields)**:
```json
{
  "detail": "Must include 'email' and 'password'."
}
```

---


### 1.2 `POST /api/users/auth/token/refresh/`
- **Summary**: Refreshes an expired JWT access token using a valid refresh token.
- **Permissions**: `ANY` (Public)
- **Request Body**:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
- **Response (200 OK)**:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---


### 1.4 `POST /api/users/auth/forgot-password/`
- **Summary**: Generates and sends a secure password reset token to the user's email address.
- **Permissions**: `ANY` (Public)
- **Request Body**:
```json
{
  "email": "customer@example.com"
}
```
- **Response (200 OK)**:
```json
{
  "message": "Password reset token sent to email."
}
```
- **Error Response (404 Not Found)**:
```json
{
  "error": "User with this email does not exist."
}
```

---


### 1.5 `POST /api/users/auth/reset-password/`
- **Summary**: Resets the user's password using the token received via email.
- **Permissions**: `ANY` (Public)
- **Request Body**:
```json
{
  "token": "c3f8d92a-6058-4541-b847-19597ebf2791",
  "new_password": "BrandNewPassword789!"
}
```
- **Response (200 OK)**:
```json
{
  "message": "Password has been reset."
}
```
- **Error Response (400 Bad Request)**:
```json
{
  "error": "Invalid or expired token."
}
```

---



## 2. Catalog & Products (`/api/catalog/`)

### 2.1 `GET /api/catalog/homepage/`
- **Summary**: Returns curated product groupings for the home screen (popular, trending, on sale, and personalized recommendations for authenticated users).
- **Permissions**: `ANY` (Public)
- **Scenario A: Anonymous Visitor**
  - **Request**: `GET /api/catalog/homepage/`
  - **Response (200 OK)**:
  ```json
  {
    "popular": [
      { "id": 1, "name": "Apple MacBook Pro 14", "price": "1999.00", "status": "ACTIVE" }
    ],
    "trending": [
      { "id": 2, "name": "Logitech MX Master 3S", "price": "99.00", "status": "ACTIVE" }
    ],
    "on_sale": [
      { "id": 3, "name": "Dell UltraSharp 27 4K", "price": "549.00", "sale_price": "479.00", "status": "ACTIVE" }
    ],
    "recommended": []
  }
  ```
- **Scenario B: Authenticated User (Personalized Suggestions Included)**
  - **Request**: `GET /api/catalog/homepage/` (`Authorization: Bearer <TOKEN>`)
  - **Response (200 OK)**:
  ```json
  {
    "popular": [
      { "id": 1, "name": "Apple MacBook Pro 14", "price": "1999.00", "status": "ACTIVE" }
    ],
    "trending": [
      { "id": 2, "name": "Logitech MX Master 3S", "price": "99.00", "status": "ACTIVE" }
    ],
    "on_sale": [
      { "id": 3, "name": "Dell UltraSharp 27 4K", "price": "549.00", "sale_price": "479.00", "status": "ACTIVE" }
    ],
    "recommended": [
      { "id": 4, "name": "Keychron K2 Mechanical Keyboard", "price": "89.00", "status": "ACTIVE" }
    ]
  }
  ```

---


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


### 2.4 `GET /api/catalog/products/`
- **Summary**: Retrieves paginated catalog products. Public users only receive `ACTIVE` products. `ADMIN` and `STOCK` roles receive all products (including `DRAFT` and `ARCHIVED`).
- **Permissions**: `ANY` (Public)
- **Query Parameters**:
  - `search`: Keyword search across product name, sku, and description
  - `brand`: Filter by Brand ID
  - `categories`: Filter by Category ID
  - `main_category`: Filter products by Category ID (only matches if the category is a root/main category with no parent)
  - `is_preorder`: Filter boolean (`true` / `false`)
  - `preorder_arrival_days`: Filter integer arrival window
  - `stock_arrival_days`: Filter integer stock replenishment window
- **Scenario A: Public Product Search (`GET /api/catalog/products/?brand=1&is_preorder=false`)**
  - **Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "brand_details": {
        "id": 1,
        "name": "Apple",
        "slug": "apple",
        "logo": null
      },
      "images": [
        {
          "id": 101,
          "image": "https://devcom.devrious.lk/media/products/mbp14.jpg",
          "is_primary": true,
          "order": 0
        }
      ],
      "specifications": [
        { "id": 1, "key": "Processor", "value": "M3 Pro" },
        { "id": 2, "key": "RAM", "value": "18GB" }
      ],
      "variants": [
        {
          "id": 50,
          "name": "512GB Space Black",
          "sku": "MBP14-SB-512",
          "price_override": null,
          "stock_quantity": 8
        }
      ],
      "name": "Apple MacBook Pro 14",
      "sku": "MBP-14-M3",
      "description": "Apple M3 Pro Chip, 18GB Unified Memory",
      "price": "1999.00",
      "sale_price": null,
      "cost_price": "1650.00",
      "unit_of_measurement": "piece",
      "minimum_stock_level": 5,
      "maximum_stock_level": 50,
      "status": "ACTIVE",
      "is_preorder": false,
      "preorder_arrival_days": 14,
      "stock_arrival_days": 2,
      "brand": 1,
      "categories": [1, 2]
    }
  ]
  ```

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

### 3.1 `POST /api/orders/guest-checkout/`
- **Summary**: Completes instant guest checkout. Automatically calculates `estimated_arrival_date` based on item lead times, processes payment, triggers confirmation email with secure token links, and logs an audit trail.
- **Permissions**: `ANY` (Public)
- **Request Body**:
```json
{
  "guest_email": "guest.buyer@example.com",
  "guest_name": "Anura Senanayake",
  "guest_phone": "+94773334444",
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    },
    {
      "product_id": 2,
      "quantity": 2
    }
  ]
}
```
- **Response (201 Created)**:
```json
{
  "message": "Order placed successfully",
  "order_number": "550e8400-e29b-41d4-a716-446655440000",
  "tracking_token": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"
}
```

---


### 3.2 `GET /api/orders/track/<uuid:token>/`
- **Summary**: Public order tracking endpoint using the secure UUID token from confirmation emails.
- **Permissions**: `ANY` (Public)
- **Request**: `GET /api/orders/track/a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d/`
- **Response (200 OK)**:
```json
{
  "id": 105,
  "order_number": "550e8400-e29b-41d4-a716-446655440000",
  "guest_name": "Anura Senanayake",
  "status": "PENDING",
  "payment_status": "SUCCESS",
  "subtotal": "2197.00",
  "discount": "0.00",
  "total": "2197.00",
  "estimated_arrival_date": "2026-03-02",
  "is_overdue": false,
  "tracking_number": null,
  "courier": null,
  "items": [
    {
      "id": 201,
      "product": 1,
      "quantity": 1,
      "unit_price": "1999.00",
      "subtotal": "1999.00"
    },
    {
      "id": 202,
      "product": 2,
      "quantity": 2,
      "unit_price": "99.00",
      "subtotal": "198.00"
    }
  ]
}
```

---


### 3.3 `GET /api/orders/receipt/<uuid:token>/`
- **Summary**: Generates and downloads the official PDF order receipt.
- **Permissions**: `ANY` (Public)
- **Request**: `GET /api/orders/receipt/b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e/`
- **Response (200 OK)**:
  - **Headers**:
    ```http
    Content-Type: application/pdf
    Content-Disposition: attachment; filename="receipt_550e8400-e29b-41d4-a716-446655440000.pdf"
    ```
  - **Body**: Binary PDF stream.

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



## 8. System Diagnostics (`/health/`)

### 8.1 `GET /health/`
- **Summary**: Lightweight server heartbeat probe for load balancers and deployment pipelines.
- **Permissions**: `ANY` (Public)
- **Response (200 OK)**:
```text
OK
```

---


