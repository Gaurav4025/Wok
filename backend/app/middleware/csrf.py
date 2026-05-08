from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

SAFE_METHODS = {'GET', 'HEAD', 'OPTIONS'}


class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method not in SAFE_METHODS and request.url.path.startswith('/api/v1'):
            csrf_cookie = request.cookies.get('csrf_token')
            csrf_header = request.headers.get('X-CSRF-Token')
            auth_header = request.headers.get('Authorization', '')

            # Skip when not browser cookie-based auth. JWT Bearer clients can proceed.
            if csrf_cookie and csrf_cookie != csrf_header and not auth_header.startswith('Bearer '):
                return JSONResponse(status_code=403, content={'detail': 'CSRF validation failed'})

        return await call_next(request)
