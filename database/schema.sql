-- Database Schema for ProcureIQ

CREATE TABLE Vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    contact VARCHAR(50),
    rating INT CHECK (rating >= 1 AND rating <= 5)
);

CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(100),
    current_unit_price DECIMAL(10, 2) NOT NULL,
    stock_level INT NOT NULL
);

CREATE TABLE PurchaseOrders (
    id SERIAL PRIMARY KEY,
    reference_no VARCHAR(100) UNIQUE NOT NULL,
    vendor_id INT REFERENCES Vendors(id),
    subtotal DECIMAL(10, 2),
    tax DECIMAL(10, 2),
    grand_total DECIMAL(10, 2),
    status VARCHAR(50) DEFAULT 'Submitted'
);

CREATE TABLE PurchaseOrderItems (
    id SERIAL PRIMARY KEY,
    po_id INT REFERENCES PurchaseOrders(id) ON DELETE CASCADE,
    product_id INT REFERENCES Products(id),
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    line_total DECIMAL(10, 2) NOT NULL
);