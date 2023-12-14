from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):   
        try:
            return await call_next(request)
        except HTTPException as http_exc:
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"error": http_exc.detail},
            )
        except Exception as gen_exc:
            print({'error': gen_exc})
            return JSONResponse(status_code=500, content={'error': 'Internal server error'})