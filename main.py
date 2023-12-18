from fastapi import FastAPI
from middleware.exception import ExceptionMiddleware
from routers import users, projects, bugs, comments
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Origins
origins = ['http://localhost:8000']

# Middleware
app.add_middleware(ExceptionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Routers
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(bugs.router)
app.include_router(comments.router)
