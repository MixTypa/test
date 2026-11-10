import hashlib
import time
import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

SECRET_KEY = "change-me-in-production"
ALGORITHM = "HS256"
TOKEN_TTL = 3600

app = FastAPI(title="JWT auth demo")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

_users: dict[str, dict] = {}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class RegisterIn(BaseModel):
    username: str
    password: str
    email: EmailStr


def create_token(username: str, role: str) -> str:
    now = int(time.time())
    payload = {"sub": username, "role": role, "iat": now, "exp": now + TOKEN_TTL}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "invalid token")
    return payload


@app.post("/register", status_code=201)
def register(data: RegisterIn):
    if data.username in _users:
        raise HTTPException(400, "user already exists")
    _users[data.username] = {
        "password_hash": hash_password(data.password),
        "email": data.email,
        "role": "reader",
    }
    return {"username": data.username, "email": data.email, "role": "reader"}


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = _users.get(form.username)
    if not user or user["password_hash"] != hash_password(form.password):
        raise HTTPException(401, "bad username or password")
    token = create_token(form.username, user["role"])
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me")
def me(current: dict = Depends(get_current_user)):
    return {"username": current["sub"], "role": current["role"]}


@app.get("/admin")
def admin_only(current: dict = Depends(get_current_user)):
    if current["role"] != "admin":
        raise HTTPException(403, "forbidden")
    return {"ok": True}
