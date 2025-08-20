from sqlalchemy.orm import Session
from . import models, schemas, utils

def create_user(db: Session, user: schemas.UserCreate):
    # Verifica se o usuário já existe
    db_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    if db_user:
        return None  # já existe usuário

    hashed_password = utils.hash_password(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    if not utils.verify_password(password, user.hashed_password):
        return None
    return user