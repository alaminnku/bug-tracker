from fastapi import APIRouter, Response, HTTPException
from config.db import db
from models.users import User, UserLogin, UserUpdate
import bcrypt
from bson import ObjectId
from lib.utils import set_cookie

router = APIRouter()


# Get all users
@router.get('/users')
def get_users():
    # Get and return the users
    users_response = db.users.find()

    users = []
    for user in users_response:
        user['_id'] = str(user['_id'])
        del user['password']
        users.append(user)
    return users


# Get a specific user
@router.get('/users/{user_id}')
def get_user(user_id: str):
    # Get and return the user
    user = db.users.find_one({'_id': ObjectId(user_id)})
    user['_id'] = str(user['_id'])
    del user['password']
    return user


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
    inserted_id = created_response.inserted_id

    # Get the created user and delete the password
    user_response = db.users.find_one({'_id': inserted_id})
    user_response['_id'] = str(user_response['_id'])
    del user_response['password']

    # Set cookie and return the created user
    set_cookie(response, user_response['_id'])
    return user_response


# Login a user
@router.post('/users/login')
def login_user(response: Response, user: UserLogin):
    # Get the user
    user_response = db.users.find_one({'email': user.email})
    user_response['_id'] = str(user_response['_id'])

    # Create password byte
    password_byte = user.password.encode('utf-8')

    # Compare passwords
    if user_response and bcrypt.checkpw(password_byte, user_response['password']):
        # Set cookie and return the user
        del user_response['password']
        set_cookie(response, user_response['_id'])
        return user_response
    else:
        raise HTTPException(status_code=401, detail='Invalid credentials')


# Update a user
@router.put('/users/{user_id}')
def update_user(user_id: str, user: UserUpdate):
    # Convert the model
    user_dict = dict(user)

    # Update the user
    db.users.update_one({'_id': ObjectId(user_id)}, {'$set': user_dict})

    # Get and return the updated user
    updated_response = db.users.find_one({'_id': ObjectId(user_id)})
    updated_response['_id'] = str(updated_response['_id'])
    del updated_response['password']
    return updated_response