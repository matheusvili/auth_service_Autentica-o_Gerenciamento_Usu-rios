from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, auth
from .database import SessionLocal

router = APIRouter()

# Dependência de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = auth.create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return new_user

@router.post("/login", response_model=schemas.UserResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    auth_user = auth.authenticate_user(db, user.username, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return auth_user