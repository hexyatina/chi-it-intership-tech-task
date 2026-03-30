import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()
key = os.getenv('SECRET_KEY')
time = os.getenv('ACCESS_TOKEN_EXPIRATION')
algo = os.getenv('ALGORITHM')


pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return pwd_context.hash(password)
def verify_password(plain, hashed) -> bool:
    return pwd_context.verify(plain, hashed)
def create_token(user_id, role):
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=20)
    }
    return jwt.encode(payload, key, algorithm=algo)
def decode_token(token)-> dict:
    try:
        return jwt.decode(token, key, algorithms=[algo])
    except JWTError:
        return None