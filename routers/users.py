from fastapi import APIRouter, Response, HTTPException, Cookie
from config.db import db
from models.users import UserCreate, UserLogin, UserUpdate
import bcrypt
from bson import ObjectId
from lib.auth import set_cookie, auth_user

router = APIRouter()


# Get all users
@router.get('/users')
def get_users(token=Cookie(None)):
    # Auth user
    auth_user(token)

    # Get the users
    users_response = db.users.find(
        {},
        {
            'password': 0,
            'created_at': 0,
            'updated_at': 0
        }
    )

    # Serialize and return the users
    users = [{'id': str(user.pop('_id')), **user} for user in users_response]
    return users


# Get a specific user
@router.get('/users/{user_id}')
def get_user(user_id: str):
    # Get the user
    user = db.users.find_one(
        {
            '_id': ObjectId(user_id)
        },
        {
            'password': 0,
            'created_at': 0,
            'updated_at': 0,

        }
    )

    # Serialize and return the user
    user['id'] = str(user.pop('_id'))
    return user


# Create a new user
@router.post('/users', status_code=201)
def create_user(response: Response, user: UserCreate):
    # Convert the model
    user_dict = dict(user)

    # Create the user
    password_byte = user_dict['password'].encode('utf-8')

    # Hash password
    salt = bcrypt.gensalt(10)
    hashed_password = bcrypt.hashpw(password_byte, salt)

    # Update user with hashed password
    user_dict['password'] = hashed_password

    # Insert the user to DB
    created_response = db.users.insert_one(user_dict)
    inserted_id = created_response.inserted_id

    # Get the created user and delete the password
    user_response = db.users.find_one(
        {
            '_id': inserted_id
        },
        {
            'password': 0,
            'created_at': 0,
            'updated_at': 0,
        }
    )
    user_response['id'] = str(user_response.pop('_id'))

    # Set cookie and return the created user
    set_cookie(response, user_response['id'])
    return user_response


# Login a user
@router.post('/users/login')
def login_user(response: Response, user: UserLogin):
    # Convert the model
    user_dict = dict(user)

    # Get the user
    user_response = db.users.find_one(
        {
            'email': user_dict['email']
        },
        {

            'created_at': 0,
            'updated_at': 0
        }
    )
    user_response['id'] = str(user_response.pop('_id'))

    # Create password byte
    password_byte = user_dict['password'].encode('utf-8')

    # Compare passwords
    if user_response and bcrypt.checkpw(password_byte, user_response['password']):
        # Set cookie and return the user
        del user_response['password']
        set_cookie(response, user_response['id'])
        return user_response
    else:
        raise HTTPException(status_code=401, detail='Invalid credentials')


# Update a user
@router.put('/users/{user_id}')
def update_user(user_id: str, user: UserUpdate):
    # Convert the model
    user_dict = dict(user)

    # Update the user
    updated_response = db.users.find_one_and_update(
        {
            '_id': ObjectId(user_id)
        },
        {
            '$set': user_dict
        },
        {
            'password': 0,
            'created_at': 0,
            'updated_at': 0
        },
        return_document=True
    )

    # Return the updated user
    updated_response['id'] = str(updated_response.pop('_id'))
    return updated_response
