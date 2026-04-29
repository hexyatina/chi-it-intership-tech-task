from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth import decode_token
from creating_tables import User
