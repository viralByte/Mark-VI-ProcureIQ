from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
import uuid # For generating Reference Numbers

router = APIRouter()
TAX_RATE = 0.05  # 5% Tax

# 1. THE MISSING GET ROUTE: This sends the POs to your dashboard!
@router.get("/")
def get_all_orders(db: Session = Depends(get_db)):
    # Fetch all orders from the database and send them to the frontend
    orders = db.query(models.PurchaseOrder).all()
    return orders

# 2. YOUR EXISTING POST ROUTE: Creates the PO
@router.post("/")
def create_purchase_order(order_data: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    try:
        ref_no = f"PO-{str(uuid.uuid4())[:8].upper()}"
        
        new_po = models.PurchaseOrder(
            reference_no=ref_no, 
            vendor_id=order_data.vendor_id, 
            status="Draft"
        )
        db.add(new_po)
        db.flush() 
        
        subtotal = 0.0
        
        for item in order_data.items:
            line_total = item.unit_price * item.quantity
            subtotal += line_total
            
            po_item = models.PO_Item(
                po_id=new_po.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price 
            )
            db.add(po_item)

        tax_amount = subtotal * TAX_RATE
        grand_total = subtotal + tax_amount
        
        new_po.subtotal = subtotal
        new_po.tax_amount = tax_amount
        new_po.grand_total = grand_total
        
        db.commit()
        db.refresh(new_po)
        
        return {"message": "Purchase Order Created!", "reference_no": new_po.reference_no, "grand_total": grand_total}
        
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"Failed to create PO: {str(e)}")

# 3. THE NEW DELETE ROUTE: Connects to your red X button
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}