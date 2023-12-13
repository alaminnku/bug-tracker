from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


app = FastAPI()


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        is_authenticated = False
        user = {"id": 1, "name": "Alamin"}

        if is_authenticated:
            request.state.user = user
            print("User authenticated")
        else:
            raise HTTPException(status_code=401, detail="Not authorized")

        return await call_next(request)
