# app/services/google_sso.py
import os
from authlib.integrations.starlette_client import OAuth

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

oauth = OAuth()
# Register lazily; if creds missing, router will guard at runtime
if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

def verify_google_id_token(id_token_str: str) -> dict:
    """
    SPA path: verify a Google ID token (from @react-oauth/google).
    We import google-auth lazily to avoid startup failures if unused.
    """
    aud = os.getenv("GOOGLE_CLIENT_ID")
    if not aud:
        raise RuntimeError("GOOGLE_CLIENT_ID not set")

    try:
        from google.oauth2 import id_token
        from google.auth.transport import requests as grequests
    except Exception as e:
        raise RuntimeError(
            "google-auth not installed. Run: pip install google-auth"
        ) from e

    info = id_token.verify_oauth2_token(id_token_str, grequests.Request(), aud)
    return {
        "sub": info.get("sub"),
        "email": info.get("email"),
        "email_verified": info.get("email_verified", False),
        "name": info.get("name"),
        "picture": info.get("picture"),
    }
