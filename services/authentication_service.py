import bcrypt
from models.user import User
from database import db

def register_user(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user = User(username=username, password=hashed.decode())
    db.session.add(user)
    db.session.commit()

    return user