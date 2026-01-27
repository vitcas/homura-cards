# security.py
import os
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

async def api_key_guard(request: Request):
    if not API_KEY:
        raise RuntimeError("API_KEY não configurada")
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ausente"
        )
    token = auth.replace("Bearer ", "").strip()
    if token != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido"
        )
