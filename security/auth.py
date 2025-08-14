import hmac
import hashlib
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from config.constants import GITHUB_WEBHOOK_SECRET
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        if not GITHUB_WEBHOOK_SECRET:
            raise HTTPException(status_code=500, detail="Webhook secret not configured")
        
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        protected_paths = ["/webhook/github"] 

        if request.url.path in protected_paths:
            signature = request.headers.get("x-hub-signature-256")

            if not signature:
                return JSONResponse(status_code=401, content={"detail": "Missing signature"})
            
            payload = await request.body()

            expected_signature = hmac.new(
                GITHUB_WEBHOOK_SECRET.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            expected_signature = f"sha256={expected_signature}"

            if not hmac.compare_digest(signature, expected_signature):
                return JSONResponse(status_code=401, content={"detail": "Invalid signature"})

        response = await call_next(request)

        return response