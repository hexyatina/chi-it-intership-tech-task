from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from creating_tables import User
from auth import verify_password, create_token, decode_token

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@app.get("/health")
def health():
    return {"status":"staying alive"}
@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.get_or_none(User.username == form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_token(user.id, user.role)
    return {"access_token": token, "token_type": "bearer"}
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = User.get_or_none(User.id == int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
