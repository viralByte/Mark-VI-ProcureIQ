# Mark-VI-ProcureIQ
# ProcureIQ: Purchase Order (PO) Management System
**ERP System Assignment for IV INNOVATIONS PRIVATE LIMITED**

**Live Demo:** https://iq-procure.vercel.app/  
**Video Walkthrough:** [Insert Your YouTube/Loom Video URL Here]  
**Author:** Viral Dubey

## 📖 Project Overview
ProcureIQ is a full-stack, microservice-based Purchase Order Management System. It facilitates tight integration between Vendors, Products, and Orders, demonstrating a modern cloud-native architecture with real-time capabilities and AI integration.

## 🚀 Tech Stack & Microservice Architecture
* **Frontend:** Vanilla JS, HTML5, CSS3, Bootstrap (Hosted on Vercel). Features dynamic row generation for PO items.
* **Authentication:** JWT via Google OAuth.
* **Core Backend API:** Python (FastAPI) (Hosted on Render). Handles business logic, including the automatic 5% tax calculation.
* **Core Database:** PostgreSQL (Hosted on Neon).
* **Real-Time Service (Bonus):** Node.js with Socket.io (Hosted on Render) for real-time broadcast notifications upon PO status changes.
* **AI Logging Service (Bonus):** MongoDB Atlas (NoSQL) for asynchronously storing raw JSON logs of AI-generated descriptions.
* **Java Microservice (Bonus):** Java Spring Boot implementation of the Vendor Management service included in the `/backend-spring` directory.

## 🧠 The "Smart" Element (Gen AI Integration)
The application integrates the Google Gemini API to generate professional, 2-sentence marketing descriptions for products based on their name and category. To ensure performance, the AI generation runs asynchronously, and the raw output is logged to a separate NoSQL MongoDB database.

## 🗄️ Database Design & Logic
The PostgreSQL database is fully normalized to maintain strict data integrity. 
* **Vendors:** Stores supplier details (`Name`, `Contact`, `Rating`).
* **Products:** Stores inventory details (`Name`, `SKU`, `Unit Price`, `Stock Level`).
* **PurchaseOrders:** Stores the overarching order data (`Reference No`, `VendorID`, `Total Amount`, `Status`).
* **PurchaseOrderItems:** A bridging table mapping multiple products to a single PO, ensuring accurate line-item math and enabling the dynamic UI.

**Integrity Checks:** Foreign Keys are strictly enforced (e.g., `VendorID` in `PurchaseOrders` maps to `Vendors.id`), and `ON DELETE CASCADE` is utilized for PO items to prevent orphaned records. A full SQL schema export is provided in `schema.sql`.

## 💻 How to Run Locally

### 1. Python FastAPI Backend
```bash
cd backend-fastapi
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
# Ensure .env contains DATABASE_URL, MONGO_URL, and GEMINI_API_KEY
uvicorn main:app --reload
