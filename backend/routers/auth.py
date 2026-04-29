import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
expiration = os.getenv('ACCESS_TOKEN_EXPIRATION')
algorithm = os.getenv('ALGORITHM')


pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return pwd_context.hash(password)
def verify_password(plain, hashed) -> bool:
    return pwd_context.verify(plain, hashed)
def create_token(user_id, role):
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=int(expiration or 20))
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)
def decode_token(token)-> dict:
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except JWTError:
        return None