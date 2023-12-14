from fastapi import APIRouter, Request
from config.db import db

router = APIRouter()


# Get all users
@router.get('/users')
async def get_users(request: Request):
    cursor = db.users.find()
    for doc in cursor:
        print(doc)
    return {'message': 'Get users'}

# Get a specific user
@router.get('/users/{user_id}')
async def get_user(request: Request, user_id):
    return {'message': 'Get a user'}


# Create a new user
@router.post('/users')
async def create_user(request: Request):
    db.users.insert_one()
    return {'message': 'Create user'}


# Update a user
@router.put('/users/{user_id}')
async def update_user(request: Request, user_id):
    return {'message': 'Update user'}

