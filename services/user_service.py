
import bcrypt
import re

from flask_jwt_extended import create_access_token

from exceptions.user_exceptions import *
from repositories.user_repo import *


def register_user(data):
    if not data:
        raise InvalidCredentialsException("Data is Required")
    if "username" not in data or "password" not in data or "email" not in data:
        raise InvalidCredentialsException("Missing required fields")
    if get_user_by_username(data['username']):
        raise UserAlreadyExistsException("Username already exists")
    if get_user_by_email(data['email']):
        raise UserAlreadyExistsException("Email already exists")
    validated_password = __validate_password(data["password"])

    hashed = bcrypt.hashpw(validated_password.encode("utf-8"), bcrypt.gensalt())
    validated_email = __validate_email(data['email'])

    user = User(username=data['username'], password=hashed.decode("utf-8"),email=validated_email)

    return save(user)


def login_user(data):
    if not data or "username" not in data or "password" not in data:
        raise InvalidCredentialsException("Username and password required")

    user = get_user_by_username(data['username'])
    if not user or not bcrypt.checkpw(data['password'].encode("utf-8"), user.password.encode("utf-8")):
        raise InvalidCredentialsException("Invalid username or password")

    token = create_access_token(identity=str(user.user_id))

    return {
        "token":token,
        "user_id": user.user_id
            }

def get_user(user_id):
    user = get_user_by_id(user_id)

    if not user:
        raise UserNotFoundException("User not found")
    return user

def delete_user(user_id):
    user = get_user(user_id)
    delete(user)
    return True

def update_user(user_id, data):
    user = get_user(user_id)

    if "username" in data:
        existing_user = get_user_by_username(data["username"])
        if existing_user and existing_user.user_id != user_id:
            raise UserAlreadyExistsException("Username already taken")
        user.username = data["username"]

    if "email" in data:
        __validate_email(data["email"])
        if get_user_by_email(data["email"]):
            raise UserAlreadyExistsException("Email already taken")
        user.email = data["email"]

    return save(user)

def reset_password(user_id,data):
    if not data or "password" not in data:
        raise InvalidCredentialsException("Password required")

    user = get_user(user_id)
    if bcrypt.checkpw(data['password'].encode(), user.password.encode()):
        raise InvalidCredentialsException("password cannot be the same with old password")

    validated_password = __validate_password(data["password"])
    hashed = bcrypt.hashpw(validated_password.encode(), bcrypt.gensalt())

    user.password = hashed.decode("utf-8")
    return save(user)


def __validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, email):
        raise InvalidCredentialsException("Invalid email format")
    return email

def __validate_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    if not re.match(pattern, password):
        raise InvalidCredentialsException(
            "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character"
        )
    return password