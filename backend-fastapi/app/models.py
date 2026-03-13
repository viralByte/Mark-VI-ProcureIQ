from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, text
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    contact = Column(String(50)) # Added per PDF
    rating = Column(Integer, default=5) # Added per PDF (e.g., 1-5 stars)
    
    orders = relationship("PurchaseOrder", back_populates="vendor")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), unique=True, nullable=False) # Added per PDF
    category = Column(String(100))
    current_unit_price = Column(Numeric(10, 2), nullable=False)
    stock_level = Column(Integer, default=0) # Added per PDF

class PurchaseOrder(Base):
    __tablename__ = "purchaseorders"
    id = Column(Integer, primary_key=True, index=True)
    reference_no = Column(String(50), unique=True, nullable=False) # Added per PDF
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    status = Column(String(50), default="Draft")
    subtotal = Column(Numeric(10, 2), default=0.00)
    tax_amount = Column(Numeric(10, 2), default=0.00)
    grand_total = Column(Numeric(10, 2), default=0.00)
    
    vendor = relationship("Vendor", back_populates="orders")
    items = relationship("PO_Item", back_populates="order", cascade="all, delete")

class PO_Item(Base):
    __tablename__ = "po_items"
    id = Column(Integer, primary_key=True, index=True)
    po_id = Column(Integer, ForeignKey("purchaseorders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    line_total = Column(Numeric(10, 2), server_default=text("0")) 
    
    order = relationship("PurchaseOrder", back_populates="items")
    product = relationship("Product")