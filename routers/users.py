from fastapi import APIRouter, Request

router = APIRouter()


# Get all users
@router.get('/users')
async def get_bugs(request: Request):
    return {'message': 'Get users'}

# Get a specific user
@router.get('/users/{user_id}')
async def get_bugs(request: Request, user_id):
    return {'message': 'Get a user'}


# Create a new user
@router.post('/users')
async def get_bugs(request: Request):
    return {'message': 'Create user'}


# Update a user
@router.put('/users/{user_id}')
async def get_bugs(request: Request, user_id):
    return {'message': 'Update user'}

