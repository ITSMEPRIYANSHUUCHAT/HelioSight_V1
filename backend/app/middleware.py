# app/middleware.py
from fastapi import Request, HTTPException
from app.auth.dependencies import get_current_user  # Will be defined in Phase 3

async def tenant_middleware(request: Request, call_next):
    # Skip for public routes like /health, /docs
    if request.url.path in ["/health", "/docs", "/openapi.json"]:
        return await call_next(request)
    
    user = await get_current_user(request)  # From JWT, Phase 3
    if user.role != "super_admin" and "company_id" in request.path_params:
        if request.path_params["company_id"] != user.company_id:
            raise HTTPException(status_code=403, detail="Access denied: Tenant mismatch")
    
    request.state.user = user  # Attach for services
    return await call_next(request)