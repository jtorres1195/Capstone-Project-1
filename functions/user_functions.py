from models import db, User
import bcrypt

def create_user(username, password):
    hashed_password = hash_password(password)

    new_user = User(username=username, password=password)

    db.session.add(new_user)
    db.session.commit()

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user

def get_user_id_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.user_id
    return None

def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')

    if bcrypt.checkpw(password_bytes, hashed_password_bytes):
        return True
    else:
        return False