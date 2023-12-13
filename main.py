from fastapi import FastAPI
from middleware.auth import AuthMiddleware
from middleware.exception import ExceptionMiddleware
from routers import tasks


app = FastAPI()

# Middleware
app.add_middleware(AuthMiddleware)
app.add_middleware(ExceptionMiddleware)

# Routers
app.include_router(tasks.router)