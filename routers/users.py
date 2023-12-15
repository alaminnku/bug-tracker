from fastapi import APIRouter, Response, HTTPException
from config.db import db
from models.users import User, UserLogin, UserUpdate
from schema.users import serialize_user, serialize_users
import bcrypt
from bson import ObjectId
from lib.utils import set_cookie

router = APIRouter()


# Get all users
@router.get('/users')
def get_users():
    # Get and return serialized users
    response = db.users.find()
    serialized_users = serialize_users(response)
    return serialized_users


# Get a specific user
@router.get('/users/{user_id}')
def get_user(user_id: str):
    # Get and return serialized user
    user = db.users.find_one({'_id': ObjectId(user_id)})
    serialized_user = serialize_user(user)
    return serialized_user


# Create a new user
@router.post('/users', status_code=201)
def create_user(response: Response, user: User):
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
    serialized_user = serialize_user(user_response)
    set_cookie(response, serialized_user['id'])
    return serialized_user


# Login a user
@router.post('/users/login')
def login_user(response: Response, user: UserLogin):
    # Get the user
    user_response = db.users.find_one({'email': user.email})
    response_dict = dict(user_response)

    # Create password byte
    password_byte = user.password.encode('utf-8')

    # Compare passwords
    if user_response and bcrypt.checkpw(password_byte, response_dict['password']):
        # Set cookie and return the serialized user
        serialized_user = serialize_user(response_dict)
        set_cookie(response, serialized_user['id'])
        return serialized_user
    else:
        raise HTTPException(status_code=401, detail='Invalid credentials')


# Update a user
@router.put('/users/{user_id}')
def update_user(user_id: str, user: UserUpdate):
    # Convert the model
    user_dict = dict(user)

    # Update the user
    db.users.update_one({'_id': ObjectId(user_id)}, {'$set': user_dict})

    # Get the updated user
    updated_response = db.users.find_one({'_id': ObjectId(user_id)})

    # Return the serialized user
    serialized_user = serialize_user(updated_response)
    return serialized_user