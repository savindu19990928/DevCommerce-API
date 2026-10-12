# FLXCORE User Roles & Permissions Guide

The FLXCORE API uses a hybrid **Role-Based Access Control (RBAC)** and **Attribute-Based Access Control (ABAC)** system. This means that users have a primary `role`, but staff users must also be assigned explicit `GranularPermission` database records to interact with the backend data.

## 1. Django Superusers (`is_superuser=True`)
- **Abilities**: Ultimate authority in the system.
- **Bypasses**: Bypasses all granular permission checks.
- **Specific Access**: Only superusers can access the `/api/users/superusers/` endpoint to promote/demote user roles and manage core user data.

## 2. Administrator (`ADMIN`)
- **Default Access**: Has global access to all endpoints (Orders, Catalog, Inventory, Support, Marketing, Reports).
- **Delegation**: Can assign any `GranularPermission` to ANY user regardless of their role.
- **Restrictions**: Cannot create or delete other superusers unless they themselves are a superuser.

## 3. Customer (`CUSTOMER`)
- **Default Access**: Customers have hardcoded, secure access strictly to their own data. They **do not** require granular permissions.
- **Abilities**:
  - View and place Orders.
  - Manage their own Cart and Wishlist.
  - Open Customer Care Cases and view their own case communications.
  - Submit Phone Call Requests.
  - Write Reviews (Requires `is_phone_verified=True`).

## 4. Customer Care Assistant (`ASSISTANT`)
- **Default Access**: Default **DENY**. They cannot view or manage any cases until they are granted `GranularPermission` by an Admin or a delegated peer.
- **Target Abilities (Once Granted)**:
  - View all customer orders (to assist with queries).
  - View and respond to Phone Call Requests.
  - Authorize and initiate Refunds or Warranty claims.
  - Manage Customer Care Cases and Communication History.
- **Delegation**: If granted a permission with `can_delegate=True`, they can use the `/api/users/permissions/` endpoint to assign that exact same permission (e.g., viewing cases) to another `ASSISTANT`.

## 5. Stock Management (`STOCK`)
- **Default Access**: Default **DENY**. Requires explicit `GranularPermission` assignment.
- **Target Abilities (Once Granted)**:
  - Full CRUD on Products, Categories, and Brands.
  - View and log `StockMovements` (Additions, damages, removals).
  - Manage and track `SerialNumber` lifecycles.
- **Granular Example**: An Admin can grant a Stock user the ability to only view/change **Category ID 4**, but not delete it.
- **Delegation**: A Stock user with `can_delegate=True` over all Products can grant another `STOCK` user the ability to view all products, or restrict them to viewing only **Product ID 5**.

## 6. Order Packing (`PACKING`)
- **Default Access**: Default **DENY**. Requires explicit `GranularPermission` assignment.
- **Target Abilities (Once Granted)**:
  - View active Orders.
  - Execute the `mark_as_packed` action which attaches inventory serial numbers to order items and updates the order status to `IN_TRANSIT`.
- **Delegation**: Can delegate their packing permissions to other `PACKING` users if they have `can_delegate=True`.

---

## How the Granular Delegation Engine Works

The granular permission engine operates via the `/api/users/permissions/` endpoint. It uses generic foreign keys, meaning it can target **any** model in the database either globally or specifically.

### Example: Peer-to-Peer Delegation
If `ASSISTANT A` is given global delegation rights over the `CustomerCareCase` model, they can assign permissions to `ASSISTANT B`.

**Payload sent by ASSISTANT A:**
```json
{
    "user": 25,                       // ID of ASSISTANT B
    "model_name": "customercarecase", // Targets the Customer Care Case model
    "object_id": null,                // Null means global access (All Cases)
    "can_view": true,
    "can_add": false,
    "can_change": true,
    "can_delete": false,
    "can_delegate": false             // B cannot pass this to someone else
}
```

### Security Guarantees
- A non-admin user can **never** delegate permissions to a user with a different role. (e.g. `STOCK` cannot delegate to `PACKING`).
- A user cannot grant a permission that they themselves do not have.
- A user cannot grant delegation rights (`can_delegate=True`) unless they have delegation rights.

## Strict Admin-Only Models
While the Granular Permission system is highly flexible, certain core models are completely locked down and **do not use** granular permissions. They are strictly restricted to the `ADMIN` role. 

Even if a user attempts to delegate access to these models, the endpoints will reject the request.

The strictly locked Admin-only models are:
- `Product`
- `Category`
- `Brand`
- `Coupon`
- `RecommendationTag` (Promotions)

*(Note: Users with the `is_superuser` flag in Django also bypass all restrictions and can manage these models).*
