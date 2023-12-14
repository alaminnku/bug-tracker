from fastapi import Response
import jsonwebtoken
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Get JWT secret
jwt_secret = os.environ.get('JWT_SECRET')


def set_cookie(response: Response, id: str):
    token = jsonwebtoken.encode({'id': id}, jwt_secret, algorithm='HS256')

    response.set_cookie(
        'token', 
        token, 
        httponly=True, 
        secure=True, 
        samesite='strict'
        )