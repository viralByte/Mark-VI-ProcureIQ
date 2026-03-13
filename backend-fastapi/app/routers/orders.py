from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
import uuid # For generating Reference Numbers

router = APIRouter()
TAX_RATE = 0.05  # 5% Tax

@router.post("/")
def create_purchase_order(order_data: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    try:
        # Generate a unique Reference No (e.g., PO-A1B2C3D4)
        ref_no = f"PO-{str(uuid.uuid4())[:8].upper()}"
        
        # 1. Create the base PO
        new_po = models.PurchaseOrder(
            reference_no=ref_no, 
            vendor_id=order_data.vendor_id, 
            status="Draft"
        )
        db.add(new_po)
        db.flush() 
        
        subtotal = 0.0
        
        # 2. Process Items
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

        # 3. Calculate Totals
        tax_amount = subtotal * TAX_RATE
        grand_total = subtotal + tax_amount
        
        # 4. Update the PO
        new_po.subtotal = subtotal
        new_po.tax_amount = tax_amount
        new_po.grand_total = grand_total
        
        db.commit()
        db.refresh(new_po)
        
        return {"message": "Purchase Order Created!", "reference_no": new_po.reference_no, "grand_total": grand_total}
        
    except Exception as e:
        db.rollback() # Crucial: Undo any partial database changes if an error occurs
        raise HTTPException(status_code=500, detail=f"Failed to create PO: {str(e)}")