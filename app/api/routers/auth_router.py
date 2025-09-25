import os
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from google.oauth2 import id_token
from google.auth.transport import requests
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.get("/login")
async def login():
    """
    Instead of redirecting, return the Google OAuth2 URL that the frontend should open.
    """
    google_client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback")

    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={google_client_id}"
        f"&response_type=id_token"
        f"&scope=openid%20email%20profile"
        f"&redirect_uri={redirect_uri}"
        f"&nonce=12345"
    )
    return {"auth_url": auth_url}


@router.get("/callback")
async def auth_callback(id_token_param: str = Query(..., alias="id_token")):
    """
    Google will return an `id_token` → verify it and issue our own JWT.
    """
    google_client_id = os.getenv("GOOGLE_CLIENT_ID")

    try:
        idinfo = id_token.verify_oauth2_token(
            id_token_param, requests.Request(), google_client_id
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    # Issue our own JWT with Google email as subject
    jwt_token = auth_service.create_jwt_token({"sub": idinfo["email"], "role": "driver"})
    return {"access_token": jwt_token, "token_type": "bearer", "user": idinfo}


@router.get("/me")
async def me(token: str = Depends(oauth2_scheme)):
    payload = auth_service.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return payload
