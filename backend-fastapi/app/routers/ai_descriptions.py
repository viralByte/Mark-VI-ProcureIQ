import os
import datetime
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from app.database import ai_logs_collection

# Force Python to read the .env file
load_dotenv()

router = APIRouter()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class ProductInfo(BaseModel):
    name: str
    category: str

@router.post("/generate-description")
async def generate_product_description(product: ProductInfo):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key missing in .env")

    prompt = (
        f"Write a professional, 2-sentence marketing description for a product "
        f"named '{product.name}' in the '{product.category}' category. "
        f"Do not include any extra conversational text."
    )
    
    try:
        # THE NUCLEAR OPTION: Direct REST API Call (No SDK required!)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        # Catch explicit API errors (like bad keys or unsupported regions)
        if response.status_code != 200:
            error_msg = response_data.get('error', {}).get('message', 'Unknown API Error')
            raise HTTPException(status_code=500, detail=f"Google API Error: {error_msg}")
            
        generated_text = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Log to MongoDB (fails gracefully if Mongo isn't running)
        try:
            log_entry = {
                "product": product.name, "prompt": prompt, "response": generated_text,
                "timestamp": datetime.datetime.now(datetime.timezone.utc)
            }
            await ai_logs_collection.insert_one(log_entry)
        except Exception:
            pass 
            
        return {"success": True, "description": generated_text}
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Network Error: {str(e)}")
    except KeyError:
        raise HTTPException(status_code=500, detail="Unexpected response format from Google.")