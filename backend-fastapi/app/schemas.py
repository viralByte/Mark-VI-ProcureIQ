from pydantic import BaseModel
from typing import List, Optional

# --- Shared & Item Schemas ---
class POItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float # Received from frontend, verified in backend

# --- Purchase Order Schemas ---
class PurchaseOrderCreate(BaseModel):
    vendor_id: int
    items: List[POItemCreate]

class PurchaseOrderResponse(BaseModel):
    id: int
    vendor_id: int
    status: str
    subtotal: float
    tax_amount: float
    grand_total: float
    
    class Config:
        from_attributes = True # Tells Pydantic to read SQLAlchemy models