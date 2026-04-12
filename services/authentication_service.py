from functools import wraps

import jwt
from flask import request

from exceptions.user_exceptions import InvalidCredentialsException
from services.user_service import SECRET_KEY, get_user


def token_required(func):
    @wraps(func)
    def decorated_function(*args, **keyword_args):
        token = request.headers.get('Authorization')

        if not token:
            raise InvalidCredentialsException("Token is missing")

        try:
            if token.startswith('Bearer '):
                token = token.split(" ")[1]
            data = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
            user_id = data['user_id']

            get_user(user_id)
        except:
            raise InvalidCredentialsException("Token is invalid or expired")
        return func(*args,user_id= user_id, **keyword_args)
    return decorated_function