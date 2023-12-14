from fastapi import APIRouter, Response
from config.db import db
from models.users import User, LoginUser, UpdateUser
from schema.users import serialize_user, serialize_users
import bcrypt
from bson import ObjectId
from utils.tools import set_cookie

router = APIRouter()


# Get all users
@router.get('/users')
def get_users():
    users = serialize_users(db.users.find())
    return users


# Get a specific user
@router.get('/users/{user_id}')
def get_user(user_id: str):
    try:
        user = db.users.find_one({'_id': ObjectId(user_id)})
        return serialize_user(user)
    except Exception as gen_exc:
        print(gen_exc)


# Create a new user
@router.post('/users')
async def create_user(response: Response, user: User):
    # Create the user
    password_byte = user.password.encode('utf-8')

    # Hash password
    salt = bcrypt.gensalt(10)
    hashed_password = bcrypt.hashpw(password_byte, salt)

    # Update user with hashed password
    user_dict = dict(user)
    user_dict.update(password = hashed_password)

    # Insert the user to DB
    created_response = db.users.insert_one(user_dict)

    # Get the created user
    inserted_id = created_response.inserted_id
    user_response = db.users.find_one({'_id': inserted_id})

    # Set cookie and return the serialized user
    final_user = serialize_user(user_response)
    set_cookie(response, final_user['id'])
    return final_user


# Login a user
@router.post('/users/login')
def login_user(response: Response, user: LoginUser):
    # Create password byte
    user_dict = dict(user)
    password_byte = user_dict['password'].encode('utf-8')

    # Get the user
    user_response = db.users.find_one({'email': user.email})
    response_dict = dict(user_response)

    # Compare passwords
    if bcrypt.checkpw(password_byte, response_dict['password']):
        # Set cookie and return the serialized user
        final_user = serialize_user(response_dict)
        set_cookie(response, final_user['id'])
        return final_user
    else:
        print('Invalid credentials')
        return {'message': 'Invalid credentials'}

# Update a user
@router.put('/users/{user_id}')
async def update_user(user_id: str, user: UpdateUser):
    # Update the user
    user_dict = dict(user)
    db.users.find_one_and_update({'_id': ObjectId(user_id)}, {'$set': user_dict})

    # Get the updated user
    updated_response = db.users.find_one({'_id': ObjectId(user_id)})

    # Return the serialized user
    final_user = serialize_user(updated_response)
    return final_user

