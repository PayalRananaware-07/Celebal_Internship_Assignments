CREATE TABLE customers (
    customer_id INTEGER,
    customer_name TEXT,
    email TEXT,
    registration_date TEXT,
    customer_type TEXT
);

CREATE TABLE products (
    product_id INTEGER,
    product_name TEXT,
    category TEXT,
    subcategory TEXT,
    cost_price REAL
);

CREATE TABLE orders (
    order_id INTEGER,
    customer_id INTEGER,
    order_date TEXT,
    status TEXT,
    region_code TEXT
);

CREATE TABLE order_items (
    item_id INTEGER,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    discount_percent REAL
);