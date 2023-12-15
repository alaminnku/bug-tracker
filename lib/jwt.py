import jsonwebtoken
from dotenv import load_dotenv, find_dotenv
import os
from config.db import db
from bson import ObjectId
from fastapi import HTTPException

# Load env
load_dotenv(find_dotenv())

# Get jwt secret
jwt_secret = os.environ.get('JWT_SECRET')
jwt_algorithm = os.environ.get('JWT_ALGORITHM')


def auth_user(token: str):
    # Decode the token
    try:
        payload = jsonwebtoken.decode(token, jwt_secret, algorithms=[jwt_algorithm])
    except:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    # Get user id
    user_id = payload['_id']

    # Get and return the serialized user
    user = db.users.find_one({'_id': ObjectId(user_id)})
    user['_id'] = str(user['_id'])
    return user


