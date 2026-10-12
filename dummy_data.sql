-- Dummy Data for DevCommerce

-- Insert Users (All Roles)
-- Passwords are set to a dummy hash
INSERT INTO users_user (id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, role, phone_number, is_phone_verified, is_email_verified, notify_order_email, notify_order_sms, notify_receipt_email, notify_receipt_sms, notify_promotions_email, notify_promotions_sms) 
VALUES 
(1, 'pbkdf2_sha256$600000$dummyhash', 1, 'admin_user', 'Admin', 'User', 'admin@example.com', 1, 1, NOW(), 'ADMIN', '1000000001', 1, 1, 1, 0, 1, 0, 0, 0),
(2, 'pbkdf2_sha256$600000$dummyhash', 0, 'customer1', 'John', 'Doe', 'customer1@example.com', 0, 1, NOW(), 'CUSTOMER', '1000000002', 1, 1, 1, 0, 1, 0, 1, 0),
(3, 'pbkdf2_sha256$600000$dummyhash', 0, 'customer2', 'Jane', 'Smith', 'customer2@example.com', 0, 1, NOW(), 'CUSTOMER', '1000000003', 1, 1, 1, 0, 1, 0, 1, 0),
(4, 'pbkdf2_sha256$600000$dummyhash', 0, 'assistant1', 'Support', 'Staff', 'support@example.com', 1, 1, NOW(), 'ASSISTANT', '1000000004', 1, 1, 0, 0, 0, 0, 0, 0),
(5, 'pbkdf2_sha256$600000$dummyhash', 0, 'stock1', 'Stock', 'Manager', 'stock@example.com', 1, 1, NOW(), 'STOCK', '1000000005', 1, 1, 0, 0, 0, 0, 0, 0),
(6, 'pbkdf2_sha256$600000$dummyhash', 0, 'packer1', 'Packing', 'Staff', 'packing@example.com', 1, 1, NOW(), 'PACKING', '1000000006', 1, 1, 0, 0, 0, 0, 0, 0);

-- Insert Categories
INSERT INTO catalog_category (id, name, slug, description, parent_id)
VALUES
(1, 'Electronics', 'electronics', 'Electronic devices and accessories', NULL),
(2, 'Laptops', 'laptops', 'Laptops and notebooks', 1),
(3, 'Smartphones', 'smartphones', 'Mobile phones', 1),
(4, 'Audio', 'audio', 'Headphones, Speakers, etc.', 1),
(5, 'Clothing', 'clothing', 'Apparel and Fashion', NULL),
(6, 'Shoes', 'shoes', 'Footwear', 5);

-- Insert Brands
INSERT INTO catalog_brand (id, name, slug, description, logo)
VALUES
(1, 'Apple', 'apple', 'Apple Inc.', ''),
(2, 'Samsung', 'samsung', 'Samsung Electronics', ''),
(3, 'Dell', 'dell', 'Dell Computers', ''),
(4, 'Sony', 'sony', 'Sony Corporation', ''),
(5, 'Nike', 'nike', 'Nike Inc.', ''),
(6, 'Adidas', 'adidas', 'Adidas AG', '');

-- Insert Products (All Statuses)
INSERT INTO catalog_product (id, name, sku, slug, short_description, description, brand_id, cost_price, price, sale_price, unit_of_measurement, minimum_stock_level, maximum_stock_level, expiry_date, status, is_preorder, preorder_arrival_days, stock_arrival_days, requires_serial_tracking, created_at, updated_at)
VALUES
(1, 'MacBook Pro 14"', 'SKU-MAC14', 'macbook-pro-14', 'M2 Pro chip', 'The latest MacBook Pro with M2 Pro chip, 16GB RAM, 512GB SSD.', 1, 1500.00, 1999.00, NULL, 'piece', 5, 50, NULL, 'ACTIVE', 0, 14, 2, 1, NOW(), NOW()),
(2, 'iPhone 14 Pro', 'SKU-IP14P', 'iphone-14-pro', 'A16 Bionic chip', 'The new iPhone 14 Pro with Dynamic Island.', 1, 800.00, 999.00, NULL, 'piece', 10, 100, NULL, 'ACTIVE', 0, 14, 2, 1, NOW(), NOW()),
(3, 'Galaxy S23 Ultra', 'SKU-S23U', 'galaxy-s23-ultra', 'Snapdragon 8 Gen 2', 'Samsung Galaxy S23 Ultra with S-Pen.', 2, 900.00, 1199.00, 1099.00, 'piece', 5, 100, NULL, 'ACTIVE', 0, 14, 2, 1, NOW(), NOW()),
(4, 'Dell XPS 13', 'SKU-XPS13', 'dell-xps-13', 'Intel Core i7', 'Dell XPS 13 thin and light laptop.', 3, 1000.00, 1299.00, NULL, 'piece', 5, 30, NULL, 'ACTIVE', 0, 14, 2, 1, NOW(), NOW()),
(5, 'Sony WH-1000XM5', 'SKU-SONYXM5', 'sony-wh-1000xm5', 'Noise Cancelling', 'Sony premium noise cancelling headphones.', 4, 200.00, 399.00, NULL, 'piece', 5, 50, NULL, 'DRAFT', 0, 14, 2, 0, NOW(), NOW()),
(6, 'Nike Air Max', 'SKU-NIKEAIR', 'nike-air-max', 'Running Shoes', 'Nike Air Max running shoes for men.', 5, 50.00, 120.00, NULL, 'pair', 10, 200, NULL, 'ACTIVE', 0, 14, 2, 0, NOW(), NOW()),
(7, 'Adidas Ultraboost', 'SKU-ADIBOOST', 'adidas-ultraboost', 'Comfortable Shoes', 'Adidas Ultraboost running shoes.', 6, 60.00, 150.00, NULL, 'pair', 5, 100, NULL, 'UNAVAILABLE', 0, 14, 2, 0, NOW(), NOW());

-- Insert Product Categories (Many-to-Many)
INSERT INTO catalog_product_categories (id, product_id, category_id)
VALUES
(1, 1, 1), (2, 1, 2),
(3, 2, 1), (4, 2, 3),
(5, 3, 1), (6, 3, 3),
(7, 4, 1), (8, 4, 2),
(9, 5, 1), (10, 5, 4),
(11, 6, 5), (12, 6, 6),
(13, 7, 5), (14, 7, 6);

-- Insert Product Images
INSERT INTO catalog_productimage (id, product_id, image, is_primary, `order`)
VALUES
(1, 1, 'products/macbook14.jpg', 1, 1),
(2, 2, 'products/iphone14pro.jpg', 1, 1),
(3, 3, 'products/s23ultra.jpg', 1, 1),
(4, 4, 'products/xps13.jpg', 1, 1),
(5, 5, 'products/sonyxm5.jpg', 1, 1),
(6, 6, 'products/nikeair.jpg', 1, 1),
(7, 7, 'products/adidasultra.jpg', 1, 1);

-- Insert Orders (All Kinds of Statuses)
INSERT INTO orders_order (id, order_number, user_id, guest_email, guest_phone, guest_name, subtotal, discount, total, status, payment_status, payment_transaction_id, requires_urgent_attention, estimated_arrival_date, created_at, updated_at, tracking_number, courier, guest_tracking_token, receipt_token)
VALUES
(1, 'ORD-001-PENDING', 2, NULL, NULL, NULL, 1999.00, 0.00, 1999.00, 'PENDING', 'PENDING', NULL, 0, NULL, NOW(), NOW(), NULL, NULL, REPLACE(UUID(), '-', ''), REPLACE(UUID(), '-', '')),
(2, 'ORD-002-PAID', 3, NULL, NULL, NULL, 999.00, 0.00, 999.00, 'PACKING', 'SUCCESS', 'TXN-002', 0, NULL, NOW(), NOW(), NULL, NULL, REPLACE(UUID(), '-', ''), REPLACE(UUID(), '-', '')),
(3, 'ORD-003-DELIVERED', 2, NULL, NULL, NULL, 1099.00, 0.00, 1099.00, 'DELIVERED', 'SUCCESS', 'TXN-003', 0, '2023-01-01', NOW(), NOW(), 'TRK-003', 'FedEx', REPLACE(UUID(), '-', ''), REPLACE(UUID(), '-', '')),
(4, 'ORD-004-CANCELLED', 3, NULL, NULL, NULL, 1299.00, 0.00, 1299.00, 'CANCELLED', 'FAILED', 'TXN-004', 0, NULL, NOW(), NOW(), NULL, NULL, REPLACE(UUID(), '-', ''), REPLACE(UUID(), '-', '')),
(5, 'ORD-005-REFUNDED', 2, NULL, NULL, NULL, 1999.00, 0.00, 1999.00, 'REFUNDED', 'REFUNDED', 'TXN-005', 0, NULL, NOW(), NOW(), NULL, NULL, REPLACE(UUID(), '-', ''), REPLACE(UUID(), '-', '')),
(6, 'ORD-006-PARTIAL_REF', 3, NULL, NULL, NULL, 2198.00, 0.00, 2198.00, 'PARTIALLY_REFUNDED', 'SUCCESS', 'TXN-006', 0, NULL, NOW(), NOW(), NULL, NULL, REPLACE(UUID(), '-', ''), REPLACE(UUID(), '-', '')),
(7, 'ORD-007-TRANSIT', 2, NULL, NULL, NULL, 120.00, 0.00, 120.00, 'IN_TRANSIT', 'SUCCESS', 'TXN-007', 0, '2026-12-01', NOW(), NOW(), 'TRK-007', 'UPS', REPLACE(UUID(), '-', ''), REPLACE(UUID(), '-', '')),
(8, 'ORD-008-GUEST', NULL, 'guest@example.com', '1000000008', 'Guest User', 399.00, 0.00, 399.00, 'CONFIRMED', 'SUCCESS', 'TXN-008', 0, NULL, NOW(), NOW(), NULL, NULL, REPLACE(UUID(), '-', ''), REPLACE(UUID(), '-', ''));

-- Insert Order Items
INSERT INTO orders_orderitem (id, order_id, product_id, variant_id, quantity, unit_price, subtotal)
VALUES
(1, 1, 1, NULL, 1, 1999.00, 1999.00), -- ORD 1
(2, 2, 2, NULL, 1, 999.00, 999.00),   -- ORD 2
(3, 3, 3, NULL, 1, 1099.00, 1099.00), -- ORD 3
(4, 4, 4, NULL, 1, 1299.00, 1299.00), -- ORD 4
(5, 5, 1, NULL, 1, 1999.00, 1999.00), -- ORD 5
(6, 6, 2, NULL, 1, 999.00, 999.00),   -- ORD 6
(7, 6, 3, NULL, 1, 1199.00, 1199.00), -- ORD 6
(8, 7, 6, NULL, 1, 120.00, 120.00),   -- ORD 7
(9, 8, 5, NULL, 1, 399.00, 399.00);   -- ORD 8

-- Insert Refunds
INSERT INTO orders_refund (id, order_id, amount, reason, status, initiated_by_id, created_at)
VALUES
(1, 5, 1999.00, 'Customer requested full refund, item damaged.', 'COMPLETED', 1, NOW()),
(2, 6, 999.00, 'Partial refund for iPhone out of stock.', 'COMPLETED', 4, NOW());

-- Map Refunds to Order Items (Many-to-Many)
INSERT INTO orders_refund_items (id, refund_id, orderitem_id)
VALUES
(1, 1, 5),
(2, 2, 6);
