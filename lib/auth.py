import jsonwebtoken
from dotenv import load_dotenv, find_dotenv
import os
from config.db import db
from bson import ObjectId
from fastapi import HTTPException, Response

# Load env
load_dotenv(find_dotenv())

# Get jwt secret
jwt_secret = os.environ.get('JWT_SECRET')
jwt_algorithm = os.environ.get('JWT_ALGORITHM')


# Set cookie
def set_cookie(response: Response, id: str):
    # Encode the token
    token = jsonwebtoken.encode(
        {'id': id},
        jwt_secret,
        algorithm=jwt_algorithm
    )

    # Set cookie to response
    response.set_cookie(
        'token',
        token,
        httponly=True,
        secure=True,
        samesite='strict',
        max_age=7 * 24 * 60 * 60,  # 7 days
    )


# Auth user
def auth_user(token: str):
    # Decode the token
    try:
        payload = jsonwebtoken.decode(
            token, jwt_secret, algorithms=[jwt_algorithm])
    except:
        raise HTTPException(status_code=401, detail='Invalid token')

    # Get user id
    user_id = payload['id']

    # Get and return the serialized user
    user = db.users.find_one(
        {
            '_id': ObjectId(user_id)
        },
        {
            'password': 0
        }
    )
    user['id'] = str(user.pop('_id'))
    return user
