import os
import jwt
import datetime
from fastapi import APIRouter, Depends, HTTPException, Header
from google.oauth2 import id_token
from google.auth.transport import requests
from pydantic import BaseModel

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-fallback-key")
ALGORITHM = "HS256"

class TokenRequest(BaseModel):
    google_token: str

@router.post("/login")
def login_with_google(request: TokenRequest):
    try:
        # 1. Verify the token with Google
        idinfo = id_token.verify_oauth2_token(
            request.google_token, requests.Request(), GOOGLE_CLIENT_ID
        )
        user_email = idinfo['email']
        
        # 2. Create our own JWT payload
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        jwt_payload = {
            "sub": user_email,
            "exp": expiration
        }
        
        # 3. Sign and return our JWT
        encoded_jwt = jwt.encode(jwt_payload, JWT_SECRET, algorithm=ALGORITHM)
        return {"access_token": encoded_jwt, "token_type": "bearer", "email": user_email}
        
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")

# Dependency to protect other routes
def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload["sub"] # Returns the user's email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")