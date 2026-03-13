-- PostgreSQL Schema for ProcureIQ

CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    contact VARCHAR NOT NULL,
    rating INTEGER DEFAULT 5
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    sku VARCHAR NOT NULL UNIQUE,
    current_unit_price FLOAT NOT NULL,
    stock_level INTEGER DEFAULT 0
);

CREATE TABLE purchase_orders (
    id SERIAL PRIMARY KEY,
    reference_no VARCHAR NOT NULL UNIQUE,
    vendor_id INTEGER NOT NULL,
    total_amount FLOAT NOT NULL,
    tax_amount FLOAT NOT NULL,
    grand_total FLOAT NOT NULL,
    status VARCHAR DEFAULT 'Draft',
    FOREIGN KEY (vendor_id) REFERENCES vendors (id)
);