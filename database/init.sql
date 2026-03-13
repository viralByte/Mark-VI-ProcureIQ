-- PostgreSQL Schema Export for PO Management System

CREATE TABLE Vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    contact VARCHAR(50),
    rating INT DEFAULT 5 CHECK (rating >= 1 AND rating <= 5)
);

CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(100),
    current_unit_price DECIMAL(10, 2) NOT NULL,
    stock_level INT DEFAULT 0
);

CREATE TABLE PurchaseOrders (
    id SERIAL PRIMARY KEY,
    reference_no VARCHAR(50) UNIQUE NOT NULL,
    vendor_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'Draft',
    subtotal DECIMAL(10, 2) DEFAULT 0.00,
    tax_amount DECIMAL(10, 2) DEFAULT 0.00,
    grand_total DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_vendor FOREIGN KEY (vendor_id) REFERENCES Vendors(id) ON DELETE RESTRICT
);

CREATE TABLE PO_Items (
    id SERIAL PRIMARY KEY,
    po_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    line_total DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    CONSTRAINT fk_po FOREIGN KEY (po_id) REFERENCES PurchaseOrders(id) ON DELETE CASCADE,
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES Products(id) ON DELETE RESTRICT
);