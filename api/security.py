import os
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

API_KEYS = {
    key.strip()
    for key in os.getenv("API_KEYS", "").split(",")
    if key.strip()
}

async def api_key_guard(request: Request):
    if not API_KEYS:
        raise RuntimeError("API_KEYS não configurada")
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ausente"
        )
    token = auth[7:].strip()
    if token not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido"
        )