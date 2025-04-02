from app.models.user import UserCreate
from app.db.user_store import create_user, get_user_by_username
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(user: UserCreate):
    existing = get_user_by_username(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    hashed_password = pwd_context.hash(user.password)
    create_user(user.username, hashed_password)

def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return None
    if not pwd_context.verify(password, user["password"]):
        return None
    return user
