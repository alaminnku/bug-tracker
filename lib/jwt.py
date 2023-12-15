import jsonwebtoken
from dotenv import load_dotenv, find_dotenv
import os
from config.db import db
from bson import ObjectId
from schema.users import serialize_user
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
    user_id = payload['id']

    # Get and return the serialized user
    user = db.users.find_one({'_id': ObjectId(user_id)})
    final_user = serialize_user(user)
    return final_user


