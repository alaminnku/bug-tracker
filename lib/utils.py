from fastapi import Response
import jsonwebtoken
import os
from dotenv import load_dotenv, find_dotenv
from pydantic import Field
from datetime import datetime, timezone

load_dotenv(find_dotenv())

# Get JWT secret
jwt_secret = os.environ.get('JWT_SECRET')
jwt_algorithm = os.environ.get('JWT_ALGORITHM')


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


def get_utc_now():
    return datetime.now(timezone.utc)


# Current UTC timestamp
utc_now = Field(get_utc_now())
