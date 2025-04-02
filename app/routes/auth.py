from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.users import register_user, authenticate_user
from app.auth.auth_handler import create_access_token
from app.models.user import UserCreate, Token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate):
    register_user(user)
    return {"message": "Usuário registrado com sucesso."}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token(user_id=user["id"])
    return {"access_token": token, "token_type": "bearer"}
