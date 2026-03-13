from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vendors, products, orders, ai_descriptions
from app.database import engine, Base, SessionLocal
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ProcureIQ PO Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vendors.router, prefix="/api/vendors", tags=["Vendors"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(ai_descriptions.router, prefix="/api/ai", tags=["AI"])

@app.get("/")
def read_root():
    return {"message": "Purchase Order API is running."}

@app.get("/seed")
def seed_database():
    db = SessionLocal()
    try:
        if db.query(models.Vendor).first():
            return {"message": "Database already seeded!"}
            
        v1 = models.Vendor(name="Acme Royal Suppliers", email="contact@acme.com", contact="1-800-555-0199", rating=5)
        v2 = models.Vendor(name="Globex Premium", email="sales@globex.com", contact="1-800-555-0188", rating=4)
        db.add_all([v1, v2])
        
        p1 = models.Product(name="Titanium Widget", sku="TW-1001", category="Hardware", current_unit_price=250.00, stock_level=150)
        p2 = models.Product(name="Silk Drape", sku="SD-2002", category="Materials", current_unit_price=140.00, stock_level=80)
        p3 = models.Product(name="Gold Inlay Screws", sku="GIS-3003", category="Fasteners", current_unit_price=45.00, stock_level=500)
        db.add_all([p1, p2, p3])
        
        db.commit()
        return {"message": "Database seeded successfully! You can now use the frontend."}
    finally:
        db.close()